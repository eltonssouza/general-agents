# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (UDL p.N / NNDL p.N) against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py [--src PATH/scratch/ai] [--pkg PACKAGE_ROOT] [--checks arq.json ...]

Page convention: N = PDF page (the "=== PAGE N ===" marker of the extracted text).
  UDL (541 pages): printed page = N - 14.  NNDL (303 pages): there is no printed page.

1) Range: every citation "UDL p.N[-M][, ...]" or "NNDL p.N[-M]" in the package .md/.json/.py files must be within 1..541 (UDL)
   or 1..303 (NNDL) and, in the references, the endpoints must not fall on an unread page (see the list below).
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings
   (normalized: lowercase, collapsed whitespace, NFKC ligatures, line-break hyphenation removed, straight quotes).
3) Negative content: item {"negativos": {"cite","absent":[...]}} -> NONE of the terms appears (whole word) on the cited pages.
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
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

FILES = {"UDL": "DL-Understanding-Deep-Learning-Prince.txt", "NNDL": "NN-Neural-Networks-and-Deep-Learning-Nielsen.txt"}
MAXP = {"UDL": 541, "NNDL": 303}
UNREAD = {"UDL": [(174, 174), (197, 199), (253, 253), (278, 281), (315, 316), (413, 414), (453, 469), (476, 541)], "NNDL": []}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[‐‑­]\s*\n\s*", "", s)
    s = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.extend(range(a, b + 1))
    return pages


def is_unread(book, p):
    return any(a <= p <= b for a, b in UNREAD[book])


def whole(term, text):
    return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", text) is not None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_default = os.path.dirname(here)
    root = os.path.abspath(os.path.join(pkg_default, "..", "..", ".."))
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(root, "scratch", "ai"))
    ap.add_argument("--pkg", default=pkg_default)
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()

    pages = {}
    npages = {}
    for b, fn in FILES.items():
        pages[b] = load_pages(os.path.join(a.src, fn))
        npages[b] = {k: norm(v) for k, v in pages[b].items()}
        if len(pages[b]) != MAXP[b]:
            print(f"WARNING: {b} text has {len(pages[b])} pages (expected {MAXP[b]})")
    fails = 0

    cite_re = re.compile(r"\b(UDL|NNDL)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = 0
    for root_dir, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root_dir, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            in_refs = os.sep + "references" + os.sep in fp
            for m in cite_re.finditer(text):
                book = m.group(1)
                pl = expand(m.group(2))
                for p in (pl[:1] + pl[-1:] if pl else []):
                    total += 1
                    if p < 1 or p > MAXP[book]:
                        fails += 1
                        print(f"FAIL range {fp}: {book} p.{p} outside 1..{MAXP[book]}")
                    elif in_refs and is_unread(book, p):
                        fails += 1
                        print(f"FAIL unread page cited in {fp}: {book} p.{p}")
    print(f"[range] {total} citation endpoints checked in the package files")

    check_files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    npos = nneg = 0
    for cf in check_files:
        data = json.load(open(cf, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            m = re.match(r"(UDL|NNDL)\s+p\.(.+)", it["cite"])
            if not m:
                print(f"FAIL cite format: {it['cite']}")
                fails += 1
                continue
            book = m.group(1)
            pl = expand(m.group(2))
            blob = " ".join(npages[book].get(p, "") for p in pl)
            npos += 1
            for term in it["contains"]:
                if norm(term) not in blob:
                    fails += 1
                    print(f"FAIL positive {it['cite']}: term missing: {term!r}")
        for it in data.get("negativos", []):
            m = re.match(r"(UDL|NNDL)\s+p\.(.+)", it["cite"])
            book = m.group(1)
            pl = expand(m.group(2))
            blob = " ".join(npages[book].get(p, "") for p in pl)
            nneg += 1
            for term in it["absent"]:
                if whole(norm(term), blob):
                    fails += 1
                    print(f"FAIL negative {it['cite']}: term PRESENT (the package claims absence): {term!r}")
    print(f"[content] {npos} positive checks, {nneg} negative")
    print("OK" if fails == 0 else f"{fails} failure(s)")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
