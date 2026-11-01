#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_composer.py - read-only checklist for composer.json. No network, stdlib.
Each rule declares its origin (book / inference / extrapolation) and the PRW page (PDF page).

Usage:
  python -I audit_composer.py [caminho/composer.json]
  python -I audit_composer.py --rules
  python -I audit_composer.py --json caminho/composer.json
Output: 0 = no findings; 1 = findings; 2 = usage error/invalid JSON.
"""
import argparse
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEV_TOOLS = ("phpunit/phpunit", "phpstan/phpstan", "vimeo/psalm", "squizlabs/php_codesniffer",
             "friendsofphp/php-cs-fixer", "mockery/mockery", "pestphp/pest", "phpspec/phpspec")

RULES = [
    ("COMP-LOCK", "MEDIUM", "book", "p.16", "composer.lock missing next to composer.json",
     "If the project is shared, include composer.lock so everyone gets the same versions; on deploy use composer install, not update. (The book does not distinguish libraries; for libraries many do not version the lock: extrapolation.)"),
    ("COMP-PSR4", "LOW", "book", "p.12", "no psr-4 autoload",
     "The book recommends PSR-4 for new code (without explaining the mapping)."),
    ("COMP-PSR0", "LOW", "book", "p.12", "psr-0 autoload",
     "PSR-0 was deprecated by PHP-FIG in 2014 (still usable); prefer PSR-4 for new code."),
    ("COMP-PEARREPO", "MEDIUM", "book", "p.18", "repositories of type pear",
     "PEAR repositories are no longer supported directly by Composer 2; the book shows the manual workaround with a repository of type package."),
    ("COMP-PHPVER", "INFO", "extrapolation", "-", "PHP version not declared in require",
     "NOT in the PRW. Declaring the PHP constraint avoids installing on an incompatible runtime."),
    ("COMP-DEVTOOL", "INFO", "extrapolation", "-", "test/style tool in require (instead of require-dev)",
     "NOT in the PRW (the book only shows composer global require phpunit/phpunit, p.17). Development tools usually go in require-dev."),
    ("COMP-WILDCARD", "INFO", "extrapolation", "-", "version constraint '*' or dev-master",
     "The book explains ~ and the 1.8.* wildcard (p.17) and uses '*' in a PEAR example (p.19); '*'/dev-master accept any version and weaken predictability."),
]


def audit(path):
    if not os.path.isfile(path):
        return {"error": f"file not found: {path}"}
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"error": f"invalid JSON: {e}"}
    if not isinstance(data, dict):
        return {"error": "composer.json must be a JSON object"}
    meta = {r[0]: r for r in RULES}
    findings = []

    def add(rid, extra=""):
        r = meta[rid]
        findings.append({"id": rid, "level": r[1], "origin": r[2], "page": r[3], "title": r[4] + extra, "detail": r[5]})

    req = data.get("require", {}) or {}
    reqdev = data.get("require-dev", {}) or {}
    if "php" not in req:
        add("COMP-PHPVER")
    for pkg in req:
        if pkg in DEV_TOOLS:
            add("COMP-DEVTOOL", f": {pkg}")
    for pkg, ver in list(req.items()):
        if isinstance(ver, str) and (ver.strip() in ("*", "dev-master", "dev-main") or ver.strip().startswith("dev-")):
            add("COMP-WILDCARD", f": {pkg} = {ver}")
    auto = data.get("autoload", {}) or {}
    if "psr-0" in auto:
        add("COMP-PSR0")
    if not auto.get("psr-4"):
        add("COMP-PSR4")
    for repo in data.get("repositories", []) or []:
        if isinstance(repo, dict) and repo.get("type") == "pear":
            add("COMP-PEARREPO")
    if not os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(path)), "composer.lock")):
        add("COMP-LOCK")
    return {"file": path, "name": data.get("name", "(unnamed)"), "type": data.get("type", "library"),
            "n_require": len(req), "n_require_dev": len(reqdev), "findings": findings}


def tag(f):
    if f["origin"] == "book":
        return f"[from source] (PRW {f['page']})"
    if f["origin"] == "inference":
        return f"[inference] (basis: PRW {f['page']})"
    return "[extrapolation] (outside the PRW)"


def main():
    ap = argparse.ArgumentParser(description="composer.json checklist with the origin of each rule.")
    ap.add_argument("file", nargs="?", default="composer.json")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.rules:
        for r in RULES:
            print(f"{r[0]:<14} {r[1]:<6} {r[2]:<13} PRW {r[3]:<6} {r[4]}")
        return 0
    res = audit(a.file)
    if "error" in res:
        print("Error: " + res["error"], file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 1 if res["findings"] else 0
    print(f"=== composer.json: {res['name']} (type={res['type']}; require={res['n_require']}, require-dev={res['n_require_dev']}) ===")
    if not res["findings"]:
        print("No findings by the rules (this is not a dependency security audit).")
        return 0
    for f in res["findings"]:
        print(f"\n[{f['level']}] {f['id']} {f['title']}\n   {f['detail']}\n   origin: {tag(f)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
