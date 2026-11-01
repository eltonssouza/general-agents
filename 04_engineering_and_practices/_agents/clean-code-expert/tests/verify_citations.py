# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the citations of the clean-code-expert package against the book text.

The PDF of "Código Limpo" is scanned (398 image pages, no text). The text comes from per-page OCR:
  1. images: python -I -c "import fitz; d=fitz.open(PDF); [p.get_pixmap(dpi=200, colorspace=fitz.csGRAY).save('pages/p%03d.png' % i) for i, p in enumerate(d, 1)]"
  2. OCR (Windows, pt-BR): powershell -File tests/ocr_pdf_windows.ps1 -InDir pages -OutDir txt
  3. join into <SRC>/CL.txt with "=== PAGE N ===" markers (N = PDF page), in order.
Default --src: <collection>/scratch/engineering (the book text is NOT versioned in the collection).

POSITIVE checks: all 'terms' must appear (case-insensitive; whitespace normalized) in the set of the cited
pages. NEGATIVE checks: no 'term' may appear on any page (or in 'page_range'); terms with the 're:' prefix
are regular expressions. The 'terms' are literal OCR text of the Portuguese book and stay in Portuguese;
the 'claim' fields are English summaries.
No network; read-only. Exit 0 if everything passed, 1 if some check failed, 2 if the text was not found.

Usage: python -I tests/verify_citations.py [--src DIR_WITH_CL.txt] [--checks tests/citation-checks.json] [-v]
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

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "scratch", "engineering"))


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("\xa0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def has(text, term):
    term = norm(term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--checks", default=os.path.join(HERE, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    cache = {}

    def pages_of(src):
        if src not in cache:
            cache[src] = load_pages(os.path.join(a.src, src + ".txt"))
        return cache[src]

    try:
        pages_of("CL")
    except OSError:
        print("Extracted text not found: %s (use --src; see the header of this file)" % os.path.join(a.src, "CL.txt"))
        return 2
    fails = []
    for c in checks["positive"]:
        pg = pages_of(c["src"])
        missing_pages = [p for p in c["pages"] if p not in pg]
        blob = " ".join(pg.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing and not missing_pages
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("| nonexistent pages: %s" % missing_pages) if missing_pages else "")))
        if not ok:
            fails.append(c["id"])
    for c in checks["negative"]:
        pg = pages_of(c["src"])
        lo, hi = c.get("page_range", [min(pg), max(pg)])
        found = [(n, t) for n, txt in pg.items() if lo <= n <= hi for t in c["terms"] if has(txt, t)]
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
