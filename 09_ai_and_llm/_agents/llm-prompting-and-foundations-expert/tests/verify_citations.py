# -*- coding: utf-8 -*-
"""
verify_citations.py - audits "LLMS p.N" and "PES p.N" citations against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/ai [--pkg PACKAGE_ROOT] [--checks file1.json ...]

Sources (text per page with the marker "=== PAGE N ===", N = PDF page = printed page):
  LLMS -> LLM-Survey-of-Large-Language-Models-arxiv.txt (144 pages; body 1-99; 100-144 = bibliographic references, do NOT cite as content)
  PES  -> Prompt-Engineering-Survey-arxiv.txt (12 pages; body 1-10)

1) Range: every "LLMS p.N[-M]" / "PES p.N[-M]" citation in .md/.json/.py files of the package must be in the body (LLMS 1-99, PES 1-10).
   In addition, in references 01-03 (PES) and 04-12 (LLMS), every bare "p.N" must be in the body of the file's source.
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings
   (normalized: lowercase, collapsed whitespace, straight quotes; line-break hyphenation is tested in both readings: split word and compound word).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (whole word) on the cited pages.
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

SRC = {"LLMS": "LLM-Survey-of-Large-Language-Models-arxiv.txt", "PES": "Prompt-Engineering-Survey-arxiv.txt"}
EXPECT = {"LLMS": 144, "PES": 12}
BODY = {"LLMS": (1, 99), "PES": (1, 10)}


def norm(s, keep_hyphen=False, drop_all=False):
    """Line-break hyphen: by default removed only between lowercase letters (split word); keep_hyphen=True keeps it (compound word); drop_all=True always removes it."""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[‐‑­]\s*\n\s*", "", s)
    if drop_all:
        s = re.sub(r"-\n", "", s)
    elif keep_hyphen:
        s = re.sub(r"-\n", "-", s)
    else:
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
    npages2 = {}
    npages3 = {}
    for k, fn in SRC.items():
        pages[k] = load_pages(os.path.join(a.src, fn))
        npages[k] = {n: norm(v) for n, v in pages[k].items()}
        npages2[k] = {n: norm(v, keep_hyphen=True) for n, v in pages[k].items()}
        npages3[k] = {n: norm(v, drop_all=True) for n, v in pages[k].items()}
        if len(pages[k]) != EXPECT[k]:
            print(f"WARNING: {k} has {len(pages[k])} pages (expected {EXPECT[k]})")
    fails = 0

    cite_re = re.compile(r"\b(LLMS|PES)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    bare_re = re.compile(r"(?<![A-Za-z0-9])p{1,2}\.\s*(\d+(?:\s*[-–]\s*\d+)?)")
    total = bare_total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                src = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    lo, hi = BODY[src]
                    if p < lo or p > hi:
                        fails += 1
                        print(f"FAIL range: {src} p.{p} outside {lo}-{hi} in {os.path.relpath(fp, a.pkg)}")
            base = os.path.basename(fn)
            m0 = re.match(r"(\d\d)-", base)
            if os.sep + "references" + os.sep in fp and m0:
                num = int(m0.group(1))
                src = "PES" if num <= 3 else "LLMS"
                lo, hi = BODY[src]
                for m in bare_re.finditer(text):
                    for p in expand(m.group(1)):
                        bare_total += 1
                        if p < lo or p > hi:
                            fails += 1
                            print(f"FAIL bare range: p.{p} outside the body of {src} ({lo}-{hi}) in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages cited with a source prefix; {bare_total} bare pages in the references.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.match(r"(LLMS|PES)\s+p{1,2}\.\s*(\S.*)$", cite)
            if not m:
                fails += 1
                print(f"FAIL invalid cite: {cite}")
                continue
            src = m.group(1)
            plist = expand(m.group(2))
            if not plist or any(p not in npages[src] for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            blob = " ".join(npages[src][p] for p in plist)
            blob2 = " ".join(npages2[src][p] for p in plist)
            blob3 = " ".join(npages3[src][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob and norm(t) not in blob2 and norm(t) not in blob3:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    pat = r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])"
                    if re.search(pat, blob) or re.search(pat, blob2) or re.search(pat, blob3):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
