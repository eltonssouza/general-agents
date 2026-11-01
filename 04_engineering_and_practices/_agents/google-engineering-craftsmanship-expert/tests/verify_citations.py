# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package's citations against the text of the source PDFs.

Pages = PDF. Sources: SWE-G, SWE-PREV, CC2, 97TH (see references/INDEX.md).

Usage:
  python -I tests/verify_citations.py [--src DIR_WITH_TXT] [--checks tests/citation-checks.json] [-v]

Text: uses DIR/<name>.txt with "=== PAGE N ===" markers if it exists (--src); otherwise extracts from the PDFs
at ../../*.pdf (relative to the package) with PyMuPDF (pip install pymupdf). Offline; read-only.

POSITIVE checks: all 'terms' must appear (case-insensitive, whitespace normalized) in the set of cited
pages of the given source. NEGATIVE checks: no 'term' may appear in the source (or only in the given 'pages',
if any); terms prefixed with 're:' are regular expressions.
Exit code 0 if everything passed, 1 otherwise.
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

PDFS = {
    "SWE-G": "Software-Engineering-at-Google-completo",
    "SWE-PREV": "Software-Engineering-at-Google",
    "CC2": "Code-Complete-SampleChapter-Pearson",
    "97TH": "97-Things-Every-Programmer-Should-Know",
}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("�", "'").replace("\xa0", " ")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-")):
        s = s.replace(a, b)
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)  # rejoin words hyphenated at a line break
    return re.sub(r"\s+", " ", s)


def load_txt(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def load_pdf(path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF missing: install 'pip install pymupdf' or pass --src with the extracted .txt files")
    doc = fitz.open(path)
    return {i: norm(pg.get_text()) for i, pg in enumerate(doc, 1)}


def load_source(sigla, src):
    name = PDFS[sigla]
    if src:
        t = os.path.join(src, name + ".txt")
        if os.path.exists(t):
            return load_txt(t)
    here = os.path.dirname(os.path.abspath(__file__))
    pdf = os.path.normpath(os.path.join(here, "..", "..", "..", name + ".pdf"))
    if os.path.exists(pdf):
        return load_pdf(pdf)
    sys.exit("Source not found for %s: provide --src or place the PDF at %s" % (sigla, pdf))


def has(text, term):
    term = norm(term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=None)
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    cache = {}

    def pages_of(sig):
        if sig not in cache:
            cache[sig] = load_source(sig, a.src)
        return cache[sig]

    fails = []
    for c in checks["positive"]:
        pg = pages_of(c["source"])
        blob = " ".join(pg.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["source"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s" % missing))
        if not ok:
            fails.append(c["id"])
    for c in checks["negative"]:
        pg = pages_of(c["source"])
        scope = c.get("pages") or list(pg.keys())
        found = [(n, t) for n in scope for t in c["terms"] if has(pg.get(n, ""), t)]
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["source"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])
    print("Summary: %d positive, %d negative, %d failures" % (len(checks["positive"]), len(checks["negative"]), len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
