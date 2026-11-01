# -*- coding: utf-8 -*-
"""
extract_pages.py - extracts the text of the 5 release-note PDFs with "=== PAGE N ===" markers (N = PDF page).

Requires PyMuPDF (pip install pymupdf). The PDFs are NOT part of this package.
Usage:
  python -I extract_pages.py --pdfs CAMINHO/01_programming_languages --out CAMINHO/saida
Generates Ruby-3.0-Release-Notes.txt ... Ruby-3.4-Release-Notes.txt in --out.
"""
import argparse
import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF not installed: pip install pymupdf")

NAMES = ["Ruby-3.%d-Release-Notes" % i for i in range(5)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdfs", required=True, help="folder with the PDFs")
    ap.add_argument("--out", required=True, help="output folder (will be created)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for n in NAMES:
        src = os.path.join(a.pdfs, n + ".pdf")
        if not os.path.isfile(src):
            print("missing:", src)
            continue
        doc = fitz.open(src)
        with open(os.path.join(a.out, n + ".txt"), "w", encoding="utf-8") as f:
            for i, page in enumerate(doc, 1):
                f.write("=== PAGE %d ===\n%s\n" % (i, page.get_text()))
        print("%s: %d pages" % (n, len(doc)))


if __name__ == "__main__":
    main()
