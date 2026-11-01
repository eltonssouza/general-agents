# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (WSTG p.N) against the text extracted from the OWASP WSTG 4.2 PDF.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/security [--pkg PACKAGE_ROOT] [--checks file.json ...]

Page convention: N = PDF page ("=== PAGE N ===" marker of the extracted text); printed page = N - 2.

1) Range: every citation "WSTG p.N[-M]" or "(p.N[-M])" in the package .md/.py files must be in 1..465; also checks
   that the scripts/wstg_index.json index has valid pages and that each WSTG-XXXX-NN ID of the index appears in the PDF text
   within the declared page range (structural check of the ID map).
2) Positive content: item {"cite","contains":[...]} -> the cited pages contain ALL the substrings (normalized).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (whole word) in the cited pages
   (plausible claims that the guide does NOT make in that passage).
The "contains"/"absent" strings are verbatim source text (English) and must not be translated. Read-only, no network.
Exit 0 if everything passes, 1 otherwise.
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

SRC_FILE = "OWASP-WSTG-4.2.txt"
MAXP = 465


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[‐‑­]\s*\n\s*", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff").replace("ﬃ", "ffi").replace("ﬄ", "ffl")
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
    pages = load_pages(os.path.join(a.src, SRC_FILE))
    npages = {k: norm(v) for k, v in pages.items()}
    if len(pages) != MAXP:
        print(f"WARNING: text has {len(pages)} pages (expected {MAXP})")
    fails = 0

    cite_re = re.compile(r"(?:\bWSTG\s+p{1,2}\.\s*|\(p{1,2}\.\s*)(\d[\d\s,\-–]*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py")) or fn in ("verify_citations.py", "run_script_tests.py", "run_case_checks.py"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(1)):
                    total += 1
                    if p < 1 or p > MAXP:
                        fails += 1
                        print(f"FAIL range: p.{p} outside 1-{MAXP} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages cited in package text.")

    # ID map: each index ID must appear in the PDF within the declared range
    idx = json.load(open(os.path.join(a.pkg, "scripts", "wstg_index.json"), "r", encoding="utf-8"))["entries"]
    mapped = 0
    for e in idx:
        i = e["id"]
        a0, b0 = e["pages"]
        if not (1 <= a0 <= b0 <= MAXP):
            fails += 1
            print(f"FAIL index invalid range: {i} {e['pages']}")
            continue
        if re.fullmatch(r"WSTG-[A-Z]{4}-\d{2}", i):
            blob = " ".join(npages[p] for p in range(a0, b0 + 1))
            if i.lower() not in blob:
                fails += 1
                print(f"FAIL index: {i} does not appear on pages {a0}-{b0}")
            else:
                mapped += 1
    print(f"Index: {mapped} IDs verified in the PDF text.")

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
