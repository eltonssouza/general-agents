# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the curated citations of the cicd-build-automation-expert package against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src <pasta com CICD.txt GRADLE.txt GHA.txt SWEG.txt> [--checks tests/citation-checks.json] [-v]

Each .txt file has "=== PAGE N ===" markers with N = PDF page (the package convention).
POSITIVE checks ("src", "pages", "terms"): all the terms must appear (case-insensitive; whitespace and
ligatures normalized) in at least one of the cited pages (the set of pages; each term may be on any of them).
NEGATIVE checks ("srcs", "terms", optional "pages"): NONE of the terms may appear in the given sources (on any
page, or only on the given pages). Terms prefixed with 're:' are regular expressions.
No network; read-only. Exit 0 if everything passed; 1 otherwise.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FILES = {"CICD": "CICD.txt", "GRADLE": "GRADLE.txt", "GHA": "GHA.txt", "SWE-G": "SWEG.txt"}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\ufffd", "'").replace("\xa0", " ")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("−", "-")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def load_pages(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def has(text, term):
    term = norm(term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in FILES.items()}
    checks = json.load(open(a.checks, encoding="utf-8"))
    fails = []
    for c in checks["positive"]:
        pg = pages[c["src"]]
        blob = " ".join(pg.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL"), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  "" if ok else "| missing: %s" % missing)
        if not ok:
            fails.append(c["id"])
    for c in checks["negative"]:
        found = []
        for sig in c["srcs"]:
            pg = pages[sig]
            for n, txt in pg.items():
                if "pages" in c and n not in c["pages"]:
                    continue
                for t in c["terms"]:
                    if has(txt, t):
                        found.append((sig, n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL"), c["id"], "(negative)", c["srcs"], "-", c["claim"],
                  "" if ok else "| found in %s" % found[:5])
        if not ok:
            fails.append(c["id"])
    print("Summary: %d positive, %d negative, %d failures" % (len(checks["positive"]), len(checks["negative"]), len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
