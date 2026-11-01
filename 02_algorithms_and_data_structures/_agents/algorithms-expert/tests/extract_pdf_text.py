# -*- coding: utf-8 -*-
"""
extract_pdf_text.py - extracts the PDF text into a .txt with "=== PAGE N ===" markers (N = PDF page, 1-based).

Usage: python -I tests/extract_pdf_text.py PATH/Algorithms-Erickson.pdf output.txt
Requires PyMuPDF (pip install pymupdf). The extracted text must NOT be redistributed (author's rights; the book is licensed
CC BY 4.0, but keep the attribution). No network.
"""
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF is not installed: pip install pymupdf")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    doc = fitz.open(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as out:
        for i, page in enumerate(doc, 1):
            out.write("=== PAGE %d ===\n%s\n" % (i, page.get_text()))
    print("%d pages extracted to %s" % (len(doc), sys.argv[2]))


if __name__ == "__main__":
    main()
