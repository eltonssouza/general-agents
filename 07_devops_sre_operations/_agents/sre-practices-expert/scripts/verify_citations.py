# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the sre-practices-expert package citations against the text extracted from the PDF.

Usage:
  python -I verify_citations.py --text <Google-SRE-Book.txt> [--checks citation-checks.json] [-v]
  (exists in scripts/ and in tests/, identical; default --checks = citation-checks.json alongside or in ../scripts, ../tests)

POSITIVE checks: all 'terms' must appear (case-insensitive, whitespace normalized)
in at least one of the cited 'pages' (page set: each term may be on any of them).
NEGATIVE checks: none of the 'terms' may appear on ANY page of the book
(terms with the 're:' prefix are regular expressions).
PER-PAGE NEGATIVE checks (optional key "negative_pages"): none of the 'terms' may appear on the given 'pages'
(guards against an already-fixed wrong page).
Offline; read-only. Exit code 0 if everything passed, 1 otherwise.
"""
import argparse
import json
import os
import re
import sys
import unicodedata


def load_pages(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    pages = {}
    for i in range(1, len(parts), 2):
        pages[int(parts[i])] = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", parts[i + 1]))
    return pages


def has(text, term):
    term = unicodedata.normalize("NFKC", term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    # works from both locations: scripts/ (original) and tests/ (copy); uses the first one that exists
    cands = [os.path.join(here, "citation-checks.json"),
             os.path.join(here, "..", "scripts", "citation-checks.json"),
             os.path.join(here, "..", "tests", "citation-checks.json")]
    default_checks = next((c for c in cands if os.path.exists(c)), cands[0])
    ap.add_argument("--checks", default=default_checks)
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    pages = load_pages(a.text)
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)

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

    for c in checks["negative"]:
        found = []
        for n, txt in pages.items():
            for t in c["terms"]:
                if has(txt, t):
                    found.append((n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])

    # PER-PAGE NEGATIVES (optional, round 5): none of the 'terms' may appear on the cited 'pages' (known wrong page)
    for c in checks.get("negative_pages", []):
        blob = " ".join(pages.get(p, "") for p in c["pages"])
        found = [t for t in c["terms"] if has(blob, t)]
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "(per-page negative) p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| found: %s" % found))
        if not ok:
            fails.append(c["id"])

    npos, nneg = len(checks["positive"]), len(checks["negative"]) + len(checks.get("negative_pages", []))
    print("Summary: %d positive, %d negative, %d failures" % (npos, nneg, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
