# -*- coding: utf-8 -*-
"""
verify_citations.py - verifies the curated citation checks of the javascript-expert package against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src <folder with ecma262.txt, ejs-pt.txt, ejs-en.txt> [--checks tests/citation-checks.json] [-v]

The .txt files come from `python -I tests/extract_pages.py <PDF folder> <output folder>` (PyMuPDF) and use markers
"=== PAGE N ===" with N = PDF page (the package convention).

POSITIVES: each item has `book` (Spec | EJpt | EJ1), `pages` (cited PDF pages) and `terms`. ALL terms must
appear (case-insensitive, whitespace normalized) in the union of the cited pages, and ONLY in them (no +-1 page
tolerance). A term with the `re:` prefix is a regular expression.
NEGATIVES: none of the `terms` may appear in ANY page of the indicated book (plausible claims that the source does not carry).
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

BOOKS = {"Spec": "ecma262.txt", "EJpt": "ejs-pt.txt", "EJ1": "ejs-en.txt"}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\xa0", " ")
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
          .replace("–", "-").replace("—", "-"))
    return re.sub(r"\s+", " ", s).strip()


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def has(text, term):
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return norm(term).lower() in text.lower()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    books = {k: load_pages(os.path.join(a.src, v)) for k, v in BOOKS.items()}
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    fails = []
    for c in checks["positive"]:
        pages = books[c["book"]]
        bad_pages = [p for p in c["pages"] if p not in pages]
        blob = " ".join(pages.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing and not bad_pages
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["book"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("nonexistent page: %s" % bad_pages) if bad_pages else "")))
        if not ok:
            fails.append(c["id"])
    for c in checks["negative"]:
        pages = books[c["book"]]
        found = []
        for num, txt in pages.items():
            for t in c["terms"]:
                if has(txt, t):
                    found.append((num, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["book"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])
    npos, nneg = len(checks["positive"]), len(checks["negative"])
    print("Summary: %d positives, %d negatives, %d failures" % (npos, nneg, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
