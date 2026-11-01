# -*- coding: utf-8 -*-
"""
extract_pdf_text.py - extracts the text of the go-expert source PDFs with "=== PAGE N ===" markers (N = PDF page).

Requires PyMuPDF (pip install pymupdf). Usage:
  python -I tests/extract_pdf_text.py --pdfs PDF_FOLDER --out OUTPUT_FOLDER
Writes, in OUTPUT_FOLDER, one .txt per PDF: Go-Effective-Go, Go-Language-Specification, Go-The-Little-Go-Book and
Go-1.20 ... Go-1.24-Release-Notes. The PDFs are not modified. The .txt files are the input of verify_citations.py,
audit_tokens.py and run_script_tests.py.
"""
import argparse
import os
import sys

NAMES = ["Go-Effective-Go", "Go-Language-Specification", "Go-The-Little-Go-Book", "Go-1.20-Release-Notes",
         "Go-1.21-Release-Notes", "Go-1.22-Release-Notes", "Go-1.23-Release-Notes", "Go-1.24-Release-Notes"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdfs", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF missing: pip install pymupdf", file=sys.stderr)
        return 2
    os.makedirs(a.out, exist_ok=True)
    for n in NAMES:
        src = os.path.join(a.pdfs, n + ".pdf")
        if not os.path.exists(src):
            print("PDF missing:", src, file=sys.stderr)
            return 2
        doc = fitz.open(src)
        with open(os.path.join(a.out, n + ".txt"), "w", encoding="utf-8") as f:
            for i, page in enumerate(doc, 1):
                f.write("\n=== PAGE %d ===\n%s" % (i, page.get_text()))
        print(n, len(doc), "pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
