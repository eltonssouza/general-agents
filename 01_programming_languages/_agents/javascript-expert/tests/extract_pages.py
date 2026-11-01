# -*- coding: utf-8 -*-
"""
extract_pages.py - extracts the text of the 3 source PDFs to .txt with markers "=== PAGE N ===" (N = PDF page).

Usage:
  python -I tests/extract_pages.py <PDF folder> <output folder>

The PDF folder is `01_programming_languages/` (one level above `_agents/`). Generates in the output folder:
  ecma262.txt (Spec, JavaScript-ECMA-262-Spec.pdf), ejs-pt.txt (EJpt, JavaScript-Eloquent-JS-PTBR.pdf),
  ejs-en.txt (EJ1, JavaScript-Eloquent-JS-EN-3ed.pdf, which is actually the 1st edition).
Requires PyMuPDF (`pip install pymupdf`); NOT needed to use the agent, only to audit the package.
Read-only on the PDFs; no network.
"""
import os
import sys

PDFS = [
    ("JavaScript-ECMA-262-Spec.pdf", "ecma262.txt", 876),
    ("JavaScript-Eloquent-JS-PTBR.pdf", "ejs-pt.txt", 504),
    ("JavaScript-Eloquent-JS-EN-3ed.pdf", "ejs-en.txt", 247),
]


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF not found: pip install pymupdf")
        return 2
    src, out = argv
    os.makedirs(out, exist_ok=True)
    rc = 0
    for pdf, txt, expected in PDFS:
        path = os.path.join(src, pdf)
        if not os.path.isfile(path):
            print("missing:", path)
            rc = 1
            continue
        doc = fitz.open(path)
        with open(os.path.join(out, txt), "w", encoding="utf-8", newline="\n") as f:
            for i, page in enumerate(doc, 1):
                f.write("=== PAGE %d ===\n%s\n" % (i, page.get_text()))
        flag = "" if len(doc) == expected else "  (WARNING: expected %d)" % expected
        print("%s -> %s: %d pages%s" % (pdf, txt, len(doc), flag))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
