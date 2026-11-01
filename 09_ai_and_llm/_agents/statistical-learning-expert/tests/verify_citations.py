# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (ISLR p.N / ESL p.N) against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/ai [--pkg PACKAGE_ROOT] [--checks file.json ...]

Page convention: N = PDF page (marker "=== PAGE N ===" of the extracted text). Printed ISLR = N - 15; printed ESL = N - 19.

1) Range: every citation "ISLR p.N[-M][, ...]" or "ESL p.N..." in the package .md/.json/.py files must be within the book page range
   and, in the references (references/*.md) and the guide, on READ pages ("read" ranges of scripts/slr_index.json) or in the cited frontmatter list.
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings
   (normalized: lowercase, collapsed whitespace, line-break hyphenation removed, ligatures and quotes normalized).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (whole word) in the cited pages
   (plausible claims that the book does NOT make in that passage).
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

FILES = {"ISLR": "ML-Intro-to-Statistical-Learning-ISLR.txt", "ESL": "ML-Elements-of-Statistical-Learning.txt"}
NPAGES = {"ISLR": 441, "ESL": 764}
BODY = {"ISLR": (16, 433), "ESL": (20, 717)}
FRONT_OK = {"ISLR": {4, 5, 8, 10, 11, 12, 13, 14, 15}, "ESL": {1, 5, 6, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    pages = {}
    npages = {}
    for k, fn in FILES.items():
        pages[k] = load_pages(os.path.join(a.src, fn))
        npages[k] = {p: norm(v) for p, v in pages[k].items()}
        if len(pages[k]) != NPAGES[k]:
            print(f"WARNING: {k} text has {len(pages[k])} pages (expected {NPAGES[k]})")
    idx = json.load(open(os.path.join(a.pkg, "scripts", "slr_index.json"), encoding="utf-8"))
    read_pages = {}
    for k in FILES:
        s = set()
        for c in idx["books"][k]["chapters"]:
            for x, y in c["read"]:
                s.update(range(x, y + 1))
        read_pages[k] = s
    fails = 0

    cite_re = re.compile(r"\b(ISLR|ESL)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = 0
    unread = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json", "slr_index.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            in_refs = os.sep + "references" + os.sep in fp or fn == "slr_guide.json"
            for m in cite_re.finditer(text):
                bk = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    lo, hi = BODY[bk]
                    if p < 1 or p > NPAGES[bk]:
                        fails += 1
                        print(f"FAIL range: {bk} p.{p} outside the book in {os.path.relpath(fp, a.pkg)}")
                    elif in_refs and not (lo <= p <= hi or p in FRONT_OK[bk]):
                        fails += 1
                        print(f"FAIL body: {bk} p.{p} outside the body {lo}-{hi} in {os.path.relpath(fp, a.pkg)}")
                    elif in_refs and p not in read_pages[bk] and p not in FRONT_OK[bk]:
                        unread += 1
                        fails += 1
                        print(f"FAIL unread: {bk} p.{p} cited but outside the READ ranges in {os.path.relpath(fp, a.pkg)}")
    print(f"Range/reading: {total} pages cited in package text; cited on unread pages: {unread}.")

    # index ranges within the books
    ixfail = 0
    for e in idx["entries"]:
        for k, key in (("ISLR", "islr"), ("ESL", "esl")):
            for p in expand(e[key]) if e[key] else []:
                lo, hi = BODY[k]
                if not (lo <= p <= hi or p in FRONT_OK[k]):
                    ixfail += 1
                    print(f"FAIL index: {k} p.{p} outside the body in '{e['topic']}'")
    fails += ixfail

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.match(r"(ISLR|ESL)\s+p{1,2}\.\s*(\S.*)$", cite)
            if not m:
                fails += 1
                print(f"FAIL invalid cite: {cite}")
                continue
            bk = m.group(1)
            plist = expand(m.group(2))
            if not plist or any(p not in npages[bk] for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            blob = " ".join(npages[bk][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", blob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
