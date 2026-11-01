# -*- coding: utf-8 -*-
"""
verify_citations.py - audits claims of the csharp-expert package against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src <folder with the extracted .txt files> [--checks tests/citation-checks.json] [-v]

The --src folder must contain (markers '=== PAGE N ===', N = PDF page; see tests/extract_pdf_text.py):
  CSharp-Yellow-Book.txt  (CSYB)     CSharp-9-WhatsNew.txt (CSHist, = CSharp-10/11)
  CSharp-12-WhatsNew.txt  (CS12)     CSharp-13-WhatsNew.txt (CS13)

POSITIVE checks: every 'term' must appear (case-insensitive, whitespace normalized) in the set of 'pages' of
the 'src' source. NEGATIVE checks: no 'term' may appear on ANY page of the source (terms with the 're:'
prefix are regular expressions). No network; read-only.
Exit code 0 if everything passed, 1 otherwise.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

FILES = {
    "CSYB": "CSharp-Yellow-Book.txt",
    "CSHist": "CSharp-9-WhatsNew.txt",
    "CS12": "CSharp-12-WhatsNew.txt",
    "CS13": "CSharp-13-WhatsNew.txt",
}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("�", "'").replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s)


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
    ap.add_argument("--src", required=True, help="folder with the extracted texts")
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    books = {}
    for sig, fn in FILES.items():
        p = os.path.join(a.src, fn)
        if not os.path.isfile(p):
            print("Missing file: %s" % p)
            return 2
        books[sig] = load_pages(p)
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)

    fails = []
    for c in checks["positive"]:
        pages = books[c["src"]]
        blob = " ".join(pages.get(n, "") for n in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s" % missing))
        if not ok:
            fails.append(c["id"])
    for c in checks["negative"]:
        found = []
        for n, txt in books[c["src"]].items():
            for t in c["terms"]:
                if has(txt, t):
                    found.append((n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])
    print("Summary: %d positive, %d negative, %d failures" % (len(checks["positive"]), len(checks["negative"]), len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
