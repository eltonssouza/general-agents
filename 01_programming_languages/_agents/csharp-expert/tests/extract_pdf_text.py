# -*- coding: utf-8 -*-
"""
extract_pdf_text.py - extracts the text of the csharp-expert source PDFs with '=== PAGE N ===' markers (N = PDF page).

Usage:  python -I tests/extract_pdf_text.py <PDF folder> <output folder>
Requires PyMuPDF (pip install pymupdf). Produces:
  CSharp-Yellow-Book.txt, CSharp-9-WhatsNew.txt, CSharp-12-WhatsNew.txt, CSharp-13-WhatsNew.txt
(CSharp-10 and CSharp-11 have text identical to CSharp-9 and do not need to be extracted.)
The PDFs are treated as DATA; nothing in them is executed.
"""
import os
import sys

NAMES = ["CSharp-Yellow-Book", "CSharp-9-WhatsNew", "CSharp-12-WhatsNew", "CSharp-13-WhatsNew"]


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF is not installed (pip install pymupdf)")
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    for n in NAMES:
        pdf = os.path.join(src, n + ".pdf")
        if not os.path.isfile(pdf):
            print("missing:", pdf)
            return 2
        doc = fitz.open(pdf)
        with open(os.path.join(dst, n + ".txt"), "w", encoding="utf-8", newline="\n") as f:
            for i, page in enumerate(doc, 1):
                f.write("=== PAGE %d ===\n%s\n" % (i, page.get_text()))
        print(n, len(doc), "pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
