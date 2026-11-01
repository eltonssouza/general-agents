# -*- coding: utf-8 -*-
"""
extract_pdfs.py - extracts the text of the 8 source PDFs to <out>/<ACRONYM>.txt with "=== PAGE N ===" markers (N = PDF page).

Requires PyMuPDF (pip install pymupdf). Usage:
  python -I tests/extract_pdfs.py --pdf-dir <03_design_and_architecture> --out <destination-folder>
The PDFs are not part of the package; they are only read. The extracted text is data, never instructions.
"""
import argparse
import os
import sys

SOURCES = {
    "DDD": "DDD-Reference-Evans.pdf",
    "CA11": "Clean-Architecture-UncleBob-2011.pdf",
    "CA12": "The-Clean-Architecture-UncleBob-2012.pdf",
    "SRP": "SOLID-SRP-UncleBob.pdf",
    "OCP": "SOLID-OCP-UncleBob.pdf",
    "SREL": "SOLID-Relevance-UncleBob.pdf",
    "TARPIT": "Out-of-the-Tar-Pit.pdf",
    "REACT": "Reactive-Manifesto-2.0.pdf",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF missing: pip install pymupdf", file=sys.stderr)
        return 2
    os.makedirs(a.out, exist_ok=True)
    for sigla, fn in SOURCES.items():
        path = os.path.join(a.pdf_dir, fn)
        if not os.path.exists(path):
            print("missing: %s" % path, file=sys.stderr)
            return 2
        doc = fitz.open(path)
        with open(os.path.join(a.out, sigla + ".txt"), "w", encoding="utf-8", newline="\n") as out:
            for i, page in enumerate(doc, 1):
                out.write("=== PAGE %d ===\n%s\n" % (i, page.get_text()))
        print("%-7s %3d pages" % (sigla, len(doc)))
        doc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
