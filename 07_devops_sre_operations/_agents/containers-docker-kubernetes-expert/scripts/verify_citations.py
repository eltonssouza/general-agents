# -*- coding: utf-8 -*-
"""
verify_citations.py: checks page citations against the source text.
Deterministic, no network. Input: citation-checks.json (same directory).
  - "pos" check: all the terms in "all" must appear on the cited page (PDF).
  - "neg" check: NONE of the terms in "none_of" may appear on any page of the source
    (plausible claims the book does NOT make).
Sources: text with "=== PAGE N ===" markers (extracted with PyMuPDF) OR the PDF itself
(if PyMuPDF/fitz is installed). Usage:
  python -I verify_citations.py --dockhb Docker-Handbook-freeCodeCamp.txt --k8sb Kubernetes-Basics-docs.txt
  python -I verify_citations.py --pdf-dir <folder with the PDFs>
Output: list of failures and a summary; exit code 1 if there is a failure.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_NAMES = {"DOCKHB": "Docker-Handbook-freeCodeCamp", "K8SB": "Kubernetes-Basics-docs"}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("‌", "").replace("​", "")).lower()


def load_txt(path):
    t = open(path, encoding="utf-8").read()
    parts = re.split(r"=== PAGE (\d+) ===", t)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def load_pdf(path):
    import fitz  # optional
    doc = fitz.open(path)
    return {i + 1: norm(p.get_text()) for i, p in enumerate(doc)}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dockhb")
    ap.add_argument("--k8sb")
    ap.add_argument("--pdf-dir")
    ap.add_argument("--checks", default=os.path.join(HERE, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    paths = {"DOCKHB": a.dockhb, "K8SB": a.k8sb}
    books = {}
    for src, p in paths.items():
        if p:
            books[src] = load_txt(p)
        elif a.pdf_dir:
            try:
                books[src] = load_pdf(os.path.join(a.pdf_dir, PDF_NAMES[src] + ".pdf"))
            except Exception as e:  # noqa
                print(f"ERROR opening PDF of {src}: {e}")
                return 2
    if not books:
        print("Provide --dockhb/--k8sb (txt with page markers) or --pdf-dir.")
        return 2
    checks = json.load(open(a.checks, encoding="utf-8"))
    fails, npos, nneg, skipped = [], 0, 0, 0
    for c in checks:
        book = books.get(c["src"])
        if book is None:
            skipped += 1
            continue
        if c["type"] == "pos":
            npos += 1
            page = book.get(c["page"], "")
            miss = [t for t in c["all"] if norm(t) not in page]
            if miss:
                fails.append((c["id"], f"{c['src']} p.{c['page']} missing {miss} :: {c['claim']}"))
            elif a.verbose:
                print(f"OK  {c['id']} {c['src']} p.{c['page']}")
        else:
            nneg += 1
            whole = " ".join(book.values())
            found = [t for t in c["none_of"] if norm(t) in whole]
            if found:
                fails.append((c["id"], f"NEGATIVE violated ({c['src']}): terms present {found} :: {c['claim']}"))
            elif a.verbose:
                print(f"OK  {c['id']} (negative) {c['claim']}")
    for i, m in fails:
        print(f"FAILURE {i}: {m}")
    print(f"Positive: {npos}  Negative: {nneg}  Skipped: {skipped}  Failures: {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
