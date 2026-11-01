# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the citations of the data-structures-expert package against the text extracted from the PDF
of "Open Data Structures" (Pat Morin, Edition 0.1Gbeta, 326 pages).

Usage:
  python -I tests/verify_citations.py --text <Open-Data-Structures.txt> [--checks tests/citation-checks.json] [-v]

The text must have "=== PAGE N ===" markers with N = PDF page (printed = N - 12), for example generated with PyMuPDF.

POSITIVE checks: all 'terms' must appear in at least one of the cited 'pages' (taken as a set:
each term may be on any of them). NEGATIVE checks: none of the 'terms' may appear on ANY
page of the book (terms prefixed with 're:' are regular expressions over the whitespace-normalized text).
Normalization: NFKC (ligatures), lowercase, math symbols unified (>= <= <- * -), spaces and underscores
ignored (the PDF loses '_' and breaks lines in the middle of expressions).
No network; read-only. Exit code 0 if everything passed, 1 otherwise.
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

MAP = {"≥": ">=", "≤": "<=", "←": "<-", "·": "*", "×": "*", "−": "-", "–": "-",
       "—": "-", "’": "'", "‘": "'", "“": '"', "”": '"', "∗": "*"}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for k, v in MAP.items():
        s = s.replace(k, v)
    return s.lower()


def squash(s):
    return re.sub(r"[\s_]+", "", norm(s))


def load_pages(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def has(page_raw, page_sq, term):
    if term.startswith("re:"):
        return re.search(term[3:], re.sub(r"\s+", " ", norm(page_raw)), re.IGNORECASE) is not None
    return squash(term) in page_sq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    pages = load_pages(a.text)
    sq = {n: squash(t) for n, t in pages.items()}
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)

    fails = []
    for c in checks["positive"]:
        blob_sq = "".join(sq.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if squash(t) not in blob_sq]
        ok = not missing
        if a.verbose or not ok:
            print("%s %s p. %s - %s%s" % ("OK   " if ok else "FAIL ", c["id"], c["pages"], c["claim"],
                                          "" if ok else " | missing: %s" % missing))
        if not ok:
            fails.append(c["id"])

    for c in checks["negative"]:
        found = []
        for n, txt in pages.items():
            for t in c["terms"]:
                if has(txt, sq[n], t):
                    found.append((n, t))
        ok = not found
        if a.verbose or not ok:
            print("%s %s (negative) - %s%s" % ("OK   " if ok else "FAIL ", c["id"], c["claim"],
                                              "" if ok else " | found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])

    npos, nneg = len(checks["positive"]), len(checks["negative"])
    print("Summary: %d positive, %d negative, %d failures" % (npos, nneg, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
