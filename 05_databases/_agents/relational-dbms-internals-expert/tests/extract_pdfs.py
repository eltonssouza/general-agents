# -*- coding: utf-8 -*-
"""
extract_pdfs.py - extracts the text of this agent's 7 source PDFs to .txt files with "=== PAGE N ===" markers (N = PDF
page), which are the input of verify_citations.py and audit_tokens.py.

Requires PyMuPDF (pip install pymupdf). Usage:
  python -I tests/extract_pdfs.py --pdf-dir <05_databases folder with the PDFs> --out <output folder>
The PDFs are not modified. No network.
"""
import argparse
import os
import sys

NAMES = [
    "Architecture-of-a-Database-System",
    "PostgreSQL-16-Docs",
    "Readings-in-Database-Systems-RedBook-5th",
    "SQL-Antipatterns-injection-chapter",
    "SQL-Antipatterns-introduction-chapter",
    "SQL-Antipatterns-toc-chapter",
    "SQL-Antipatterns-trees-chapter",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF not installed: pip install pymupdf", file=sys.stderr)
        return 2
    os.makedirs(a.out, exist_ok=True)
    for name in NAMES:
        pdf = os.path.join(a.pdf_dir, name + ".pdf")
        doc = fitz.open(pdf)
        with open(os.path.join(a.out, name + ".txt"), "w", encoding="utf-8", newline="\n") as f:
            for i, page in enumerate(doc, 1):
                f.write("=== PAGE %d ===\n%s\n" % (i, page.get_text()))
        print("%s: %d pages" % (name, len(doc)))
        doc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
