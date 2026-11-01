# -*- coding: utf-8 -*-
"""
verify_citations.py - audits "NGnn p.N" citations against the text extracted from the 5 Angular-NN-Overview PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/frameworks [--pkg PACKAGE_ROOT] [--checks file.json ...]

Page convention: N = PDF page (marker "=== PAGE N ===" in the extracted text). There is no printed numbering.
Pages per version: NG18=6, NG19=7, NG20=7, NG21=9, NG22=9.

1) Range: every citation "NGnn p.N[-M][, ...]" in the package's .md/.json/.py files must fall within 1..pages of the version.
2) Positive {"cite","contains":[...]} : the cited page(s) contain ALL substrings (normalized: lowercase,
   collapsed whitespace, "-\\n" break becomes "-", straight quotes). {"contains_cs":[...]} checks case-sensitively (raw text, collapsed whitespace).
3) Negative {"cite","absent":[...]} : NO term (whole word) appears in the cited pages
   (plausible claims that the capture does NOT contain; absence in the capture is not absence in the framework).
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

NPAGES = {18: 6, 19: 7, 20: 7, 21: 9, 22: 9}
FILE = "Angular-{v}-Overview.txt"


def norm(s, lower=True):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"-\s*\n\s*", "-", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.lower() if lower else s


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    raw = {v: load_pages(os.path.join(a.src, FILE.format(v=v))) for v in NPAGES}
    low = {v: {k: norm(t) for k, t in raw[v].items()} for v in raw}
    cs = {v: {k: norm(t, lower=False) for k, t in raw[v].items()} for v in raw}
    fails = 0
    for v in NPAGES:
        if len(raw[v]) != NPAGES[v]:
            print(f"WARNING: NG{v} has {len(raw[v])} pages (expected {NPAGES[v]})")

    cite_re = re.compile(r"\bNG(1[89]|2[0-2])\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json", "ng_index.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                v = int(m.group(1))
                for p in expand(m.group(2)):
                    total += 1
                    if p < 1 or p > NPAGES[v]:
                        fails += 1
                        print(f"FAILURE range: NG{v} p.{p} outside 1-{NPAGES[v]} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages in 'NGnn p.N' citations inside the package.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.fullmatch(r"NG(\d\d)\s+p{1,2}\.\s*(\S.*)", cite)
            if not m or int(m.group(1)) not in NPAGES:
                fails += 1
                print(f"FAILURE invalid cite: {cite}")
                continue
            v = int(m.group(1))
            plist = expand(m.group(2))
            if not plist or any(p not in low[v] for p in plist):
                fails += 1
                print(f"FAILURE invalid cite: {cite}")
                continue
            blob = " ".join(low[v][p] for p in plist)
            blob_cs = " ".join(cs[v][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob:
                        fails += 1
                        print(f"FAILURE positive: {cite} does not contain '{t}' -- {it.get('claim', '')}")
            if "contains_cs" in it:
                pos += 1
                for t in it["contains_cs"]:
                    if norm(t, lower=False) not in blob_cs:
                        fails += 1
                        print(f"FAILURE positive (case-sensitive): {cite} does not contain '{t}' -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", blob):
                        fails += 1
                        print(f"FAILURE negative: {cite} CONTAINS '{t}' -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
