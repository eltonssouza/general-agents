# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the clean-architecture-ddd-expert package citations against the PDF text.

Usage (from the package root):
  python -I tests/extract_pdfs.py --pdf-dir <folder with the PDFs> --out <src-dir>     # once
  python -I tests/verify_citations.py --src <src-dir> [--checks tests/citation-checks.json] [-v]

<src-dir> contains DDD.txt, CA11.txt, CA12.txt, SRP.txt, OCP.txt, SREL.txt, TARPIT.txt, REACT.txt, with
"=== PAGE N ===" markers (N = PDF page, the package convention).

POSITIVE checks: all 'terms' must appear in some of the 'pages' of source 'src' (each term may be on any of the
listed pages). NEGATIVE checks: no 'term' may appear on any page of the sources listed in 'src' (a list). Terms
prefixed with 're:' are regular expressions over the normalized text (lowercase, collapsed whitespace). The others
are compared without spaces, hyphens and quote punctuation (robust to line breaks).
No network; read-only. Exit 0 if everything passed.
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
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("↓", "").replace("↵", "ff")  # '↵' is the 'ff' ligature wrongly mapped in TARPIT
    s = s.replace(" ", " ").replace("­", "-").replace("‐", "-").replace("‑", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("�", "'")
    s = re.sub(r"-{2,}", "-", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def squash(s):
    return re.sub(r"[\s\-]+", "", s)


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    pages = {}
    for i in range(1, len(parts), 2):
        n = norm(parts[i + 1])
        pages[int(parts[i])] = (n, squash(n))
    return pages


def has(page, term):
    n, sq = page
    if term.startswith("re:"):
        return re.search(term[3:], n, re.IGNORECASE) is not None
    return squash(norm(term)) in sq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder with DDD.txt, CA11.txt, ... (markers === PAGE N ===)")
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    cache = {}

    def src(sigla):
        if sigla not in cache:
            p = os.path.join(a.src, sigla + ".txt")
            if not os.path.exists(p):
                print("ERROR: source text missing: %s" % p, file=sys.stderr)
                sys.exit(2)
            cache[sigla] = load_pages(p)
        return cache[sigla]

    fails = []
    for c in checks["positive"]:
        pages = src(c["src"])
        bad_pages = [p for p in c["pages"] if p not in pages]
        missing = []
        for t in c["terms"]:
            if not any(has(pages[p], t) for p in c["pages"] if p in pages):
                missing.append(t)
        ok = not missing and not bad_pages
        if a.verbose or not ok:
            print(("OK    " if ok else "FAIL  "), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("nonexistent page: %s" % bad_pages) if bad_pages else "")))
        if not ok:
            fails.append(c["id"])

    for c in checks["negative"]:
        found = []
        for sg in c["src"]:
            for n, pg in src(sg).items():
                for t in c["terms"]:
                    if has(pg, t):
                        found.append((sg, n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK    " if ok else "FAIL  "), c["id"], "(negative)", c["src"], "-", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])

    print("Summary: %d positive, %d negative, %d failures" % (len(checks["positive"]), len(checks["negative"]), len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
