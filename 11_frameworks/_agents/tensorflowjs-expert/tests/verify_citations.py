# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (CODE p.N) against the extracted text of the TensorFlow.js captures.

Usage: python -I tests/verify_citations.py --src PATH/scratch/frameworks [--pkg PACKAGE_ROOT] [--checks file.json ...]

Codes -> file: TFJG Guide (2 pages), TFJL Landing (9), TFJS Tutorial-Setup (7), TFJI Tutorials-Index (5).
TFJB (404) can never be used as a source for a claim (only cited as "404 page").
Page convention: N = PDF page (marker "=== PAGE N ===").

1) Range: every citation "CODE p.N[-M][, ...]" in the package .md/.json/.py files must be within the source's page range.
2) Positive: {"cite","contains":[...]} -> the cited pages contain ALL the substrings (normalized). The substrings are verbatim Portuguese source text.
3) Negative: {"cite","absent":[...]} -> NO term (whole word) appears on the cited pages.
Read-only, no network. Exit 0 if everything passes.
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

FILES = {"TFJG": ("TensorFlowJS-Guide.txt", 2), "TFJL": ("TensorFlowJS-Landing.txt", 9),
         "TFJS": ("TensorFlowJS-Tutorial-Setup.txt", 7), "TFJI": ("TensorFlowJS-Tutorials-Index.txt", 5)}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("−", "-").replace("–", "-").replace("—", "-").replace("’", "'").replace("“", '"').replace("”", '"')
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
            pages.extend(range(a, int(m.group(2) or a) + 1))
    return pages


def parse_cite(c):
    m = re.fullmatch(r"(TFJ[GLSIB])\s+pp?\.\s*(.+)", c.strip())
    return (m.group(1), expand(m.group(2))) if m else (None, [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    pages = {}
    for sig, (fn, n) in FILES.items():
        p = load_pages(os.path.join(a.src, fn))
        if len(p) != n:
            print(f"WARNING: {sig} has {len(p)} pages (expected {n})")
        pages[sig] = {k: norm(v) for k, v in p.items()}
    fails = 0

    # 1) range
    cite_re = re.compile(r"\b(TFJ[GLSIB])\s+pp?\.\s*(\d[\d\s,\-–]*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")):
                continue
            fp = os.path.join(root, fn)
            t = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(t):
                total += 1
                sig = m.group(1)
                for p in expand(m.group(2)):
                    if sig == "TFJB":
                        if p not in (1, 2):
                            fails += 1
                            print(f"FAIL range: {sig} p.{p} in {os.path.relpath(fp, a.pkg)}")
                    elif p < 1 or p > FILES[sig][1]:
                        fails += 1
                        print(f"FAIL range: {sig} p.{p} outside 1..{FILES[sig][1]} in {os.path.relpath(fp, a.pkg)}")
    print(f"citations found in the package: {total}")

    checks = []
    paths = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    for cp in paths:
        checks += json.load(open(cp, encoding="utf-8"))["checks"]
    pos = neg = 0
    for c in checks:
        sig, pgs = parse_cite(c["cite"])
        if sig is None or sig == "TFJB" or not pgs:
            fails += 1
            print("FAIL invalid citation:", c["cite"])
            continue
        text = " ".join(pages[sig].get(p, "") for p in pgs)
        if "contains" in c:
            pos += 1
            miss = [t for t in c["contains"] if norm(t) not in text]
            if miss:
                fails += 1
                print(f"FAIL positive {c['cite']} ({c.get('claim','')}): missing {miss}")
        if "absent" in c:
            neg += 1
            hit = [t for t in c["absent"] if re.search(r"(?<![\w.])" + re.escape(norm(t)) + r"(?![\w])", text)]
            if hit:
                fails += 1
                print(f"FAIL negative {c['cite']} ({c.get('claim','')}): present {hit}")
    print(f"positive checks: {pos}; negative: {neg}; failures: {fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
