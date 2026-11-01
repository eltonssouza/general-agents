# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (N8N p.N / HERMES p.N) against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src CAMINHO/scratch/frameworks [--pkg PACKAGE_ROOT] [--checks arq.json ...]

Page convention: N = PDF page (the "=== PAGE N ===" marker of the extracted text). N8N and HERMES have 4 pages each.
1) Range: every citation "N8N p.N[-M]" / "HERMES p.N[-M]" in the package's .md/.json/.py files must be in 1..4.
2) Positive: {"cite","contains":[...]}: the cited page(s) contain ALL the substrings (normalized: lowercase,
   collapsed whitespace, line-break hyphenation removed, straight quotes).
3) Negative: {"cite","absent":[...]}: NONE of the terms appears (whole word) in the cited pages.
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
The "claim" fields of citation-checks.json are descriptive only (English); "contains"/"absent" are verbatim source terms.
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

SRC = {"N8N": "n8n-Docs.txt", "HERMES": "Hermes-Agent-Docs.txt"}
MAXP = 4


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("​", "")
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in SRC.items()}
    npages = {k: {n: norm(t) for n, t in d.items()} for k, d in pages.items()}
    fails = 0
    for k, d in pages.items():
        if len(d) != MAXP:
            print(f"WARNING: {k} has {len(d)} pages (expected {MAXP})")

    cite_re = re.compile(r"\b(N8N|HERMES)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(2)):
                    total += 1
                    if p < 1 or p > MAXP:
                        fails += 1
                        print(f"FAIL range: {m.group(1)} p.{p} outside 1-{MAXP} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages in 'N8N p.N'/'HERMES p.N' citations in the package files.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.fullmatch(r"(N8N|HERMES)\s+p{1,2}\.\s*(\S.*)", cite)
            if not m:
                fails += 1
                print(f"FAIL invalid cite: {cite}")
                continue
            src, plist = m.group(1), expand(m.group(2))
            if not plist or any(p not in npages[src] for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite}")
                continue
            blob = " ".join(npages[src][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", blob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
