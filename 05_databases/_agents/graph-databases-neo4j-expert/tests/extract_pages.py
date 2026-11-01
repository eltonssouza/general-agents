# -*- coding: utf-8 -*-
"""
extract_pages.py - extracts the text of a PDF with "=== PAGE N ===" markers (N = PDF page, starting at 1).

Requires PyMuPDF (pip install pymupdf). Usage:
  python -I tests/extract_pages.py CAMINHO/NoSQL-Neo4j-Graph-Databases-2e.pdf NEO4J.txt
  python -I tests/extract_pages.py CAMINHO/NoSQL-Neo4j-Getting-Started.pdf NEO_START.txt
The PDFs are not part of the package (authors' rights). The generated .txt files are used by verify_citations.py and audit_tokens.py.
"""
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF missing: pip install pymupdf")
        return 2
    doc = fitz.open(sys.argv[1])
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as f:
        for i, page in enumerate(doc, 1):
            f.write("\n=== PAGE %d ===\n" % i)
            f.write(page.get_text())
    print("%d pages -> %s" % (len(doc), sys.argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
