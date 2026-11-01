# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (DZ p.N / TMM p.N) against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/security [--pkg PACKAGE_ROOT] [--checks file1.json ...]

Files expected in --src (text per page, marker "=== PAGE N ==="):
  InfoSec-Strategy-DZone.txt   (DZ, 272 pages)
  Threat-Modeling-Manifesto.txt (TMM, 3 pages)

Page convention: N = PDF page. DZ: printed = N - 17 in the body. TMM: PDF = document.

1) Range: every citation "DZ p.N[-M][, ...]" or "TMM p.N..." in the package .md/.json/.py files must be within 1..272 (DZ) or 1..3 (TMM).
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings
   (normalized: lowercase, collapsed whitespace, line-break hyphenation removed, straight quotes).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (as a whole word) in the cited pages
   (plausible claims that the source does NOT make in that passage).
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
"""
import argparse, json, os, re, sys, unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SRC = {"DZ": ("InfoSec-Strategy-DZone.txt", 272), "TMM": ("Threat-Modeling-Manifesto.txt", 3)}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[‐‑­]\s*\n\s*", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
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
        a = int(m.group(1)); b = int(m.group(2) or a)
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
    for k, (fn, n) in SRC.items():
        pages[k] = load_pages(os.path.join(a.src, fn))
        npages[k] = {p: norm(v) for p, v in pages[k].items()}
        if len(pages[k]) != n:
            print(f"WARNING: {k} has {len(pages[k])} pages (expected {n})")
    fails = 0

    cite_re = re.compile(r"\b(DZ|TMM)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py")) or fn == "verify_citations.py":
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                src = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    if p < 1 or p > SRC[src][1]:
                        fails += 1
                        print(f"FAIL range: {src} p.{p} outside 1-{SRC[src][1]} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages cited in package text.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.match(r"\s*(DZ|TMM)\s+p{1,2}\.\s*(\S.*)$", cite)
            if not m:
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            src = m.group(1)
            plist = expand(m.group(2))
            if not plist or any(p not in npages[src] for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            blob = " ".join(npages[src][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' -- {it.get('claim','')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", blob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' -- {it.get('claim','')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
