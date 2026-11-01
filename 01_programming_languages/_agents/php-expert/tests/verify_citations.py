# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the php-expert package citations against the text extracted from the PDF (PRW).

Usage:
  python -I tests/verify_citations.py --text prw.txt [--checks tests/citation-checks.json] [-v]

Checks:
  1. POSITIVE: all 'terms' must appear (case-insensitive, whitespace normalized) in the set of
     cited pages ('pages'). Terms with the 're:' prefix are regular expressions.
  2. NEGATIVE: none of the 'terms' may appear in ANY page of the book (plausible claims that the
     book does NOT cover: strict_types, Throwable, CSRF, Singleton...).
  3. RANGES: every citation "(PRW p.N[-M], ...)" in agents/, references/, skills/*/SKILL.md, README.md, AGENTS.md
     and .github/ has a page between 1 and the total number of pages of the text, and M >= N.
No network; read-only. Exit 0 if everything passed, 1 otherwise.
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


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("�", "'").replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
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


CITE = re.compile(r"\(PRW p\.([^)]+)\)")


def check_ranges(pkg, total):
    bad = []
    n = 0
    files = []
    for root, _d, names in os.walk(pkg):
        if os.sep + "tests" in root + os.sep and False:
            continue
        for nm in names:
            if nm.endswith(".md"):
                files.append(os.path.join(root, nm))
    for path in files:
        rel = os.path.relpath(path, pkg)
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            for m in CITE.finditer(line):
                n += 1
                for part in re.split(r"[;,]", m.group(1)):
                    part = re.sub(r"^p\.", "", part.strip())
                    mm = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", part)
                    if not mm:
                        if part and part != "N":
                            bad.append(f"{rel}:{ln}: unreadable page '{part}'")
                        continue
                    a = int(mm.group(1))
                    b = int(mm.group(2) or a)
                    if a < 1 or b > total or b < a:
                        bad.append(f"{rel}:{ln}: invalid range p.{part} (book has {total} pages)")
    return n, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("--pkg", default=os.path.dirname(here))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    pages = load_pages(a.text)
    total = max(pages)
    checks = json.load(open(a.checks, encoding="utf-8"))
    fails = []

    for c in checks["positive"]:
        blob = " ".join(pages.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s" % missing))
        if not ok:
            fails.append(c["id"])

    whole = " ".join(pages.values())
    for c in checks["negative"]:
        present = [t for t in c["terms"] if has(whole, t)]
        ok = not present
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "-", c["claim"],
                  ("" if ok else "| FOUND in the book: %s" % present))
        if not ok:
            fails.append(c["id"])

    ncite, bad = check_ranges(a.pkg, total)
    for b in bad:
        print("FAIL range:", b)
        fails.append("range")

    print("Positive: %d; negative: %d; citations in the package (ranges checked): %d; failures: %d"
          % (len(checks["positive"]), len(checks["negative"]), ncite, len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
