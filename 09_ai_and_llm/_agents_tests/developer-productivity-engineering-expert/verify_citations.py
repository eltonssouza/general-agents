# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (DPE p.N) against the text extracted from the PDF.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/ai [--pkg PACKAGE_ROOT] [--checks file.json ...]

Page convention: N = PDF page ("=== PAGE N ===" marker of the extracted text). Printed = N - 5.

1) Range: every citation "DPE p.N[-M][, ...]" (and bare "p.N" in the references) must be in 1..91; in the references, in the body 8..91.
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings (normalized).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (whole word) in the cited pages.
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

SRC_FILE = "Data-Platform-Engineering-Handbook-2022.txt"
MAXP = 91
BODY_MIN, BODY_MAX = 8, 91


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
        tok = re.sub(r"^p{1,2}\.\s*", "", tok)
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.extend(range(a, b + 1))
    return pages


NUM = r"\d+(?:\s*[-–]\s*\d+)?"
CITE_RE = re.compile(r"\bp{1,2}\.\s*(" + NUM + r"(?:\s*,\s*(?:p\.\s*)?" + NUM + r")*)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    pages = load_pages(os.path.join(a.src, SRC_FILE))
    npages = {k: norm(v) for k, v in pages.items()}
    if len(pages) != MAXP:
        print(f"WARNING: text has {len(pages)} pages (expected {MAXP})")
    fails = 0
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json", "run_script_tests.py"):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, a.pkg)
            if rel.startswith("tests"):
                continue
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            in_refs = os.sep + "references" + os.sep in fp and fn != "INDEX.md"
            for m in CITE_RE.finditer(text):
                for p in expand(m.group(1)):
                    total += 1
                    lo, hi = (BODY_MIN, BODY_MAX) if in_refs else (1, MAXP)
                    if p < lo or p > hi:
                        fails += 1
                        ctx = text[max(0, m.start() - 20): m.end() + 10].replace("\n", " ")
                        print(f"FAIL range: p.{p} outside {lo}-{hi} in {rel}: ...{ctx}...")
    print(f"Range: {total} pages cited in package text.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.search(r"p{1,2}\.\s*(\S.*)$", cite)
            plist = expand(m.group(1)) if m else []
            if not plist or any(p not in npages for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            blob = " ".join(npages[p] for p in plist)
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
