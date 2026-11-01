# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (SBR p.N) against the text extracted from the PDF.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/frameworks [--pkg PACKAGE_ROOT] [--checks file1.json ...]

Page convention: N = PDF page (marker "=== PAGE N ===" of the extracted text); printed number = N - 20.

1) Range: every citation "SBR p.N[-M][, ...]" in the package .md/.json/.py files must be within 1..882; in the
   references/ files the loose "p.N" citations (without the prefix) are also checked within 1..882.
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings
   (normalized: lowercase, collapsed spaces; it also compares the "no-spaces" version to tolerate line breaks
   in the middle of identifiers).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (whole word, and also in the
   no-spaces version) on the cited pages (plausible claims that the book does NOT carry in that passage).
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

SRC_FILE = "Spring-Boot-Reference.txt"
MAXP = 882
BODY_MIN, BODY_MAX = 1, 882


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("�", "'").replace("\xa0", " ")
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("​", "")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"\s+", "", s)


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
    spages = {k: squash(v) for k, v in npages.items()}
    if len(pages) != MAXP:
        print(f"WARNING: text has {len(pages)} pages (expected {MAXP})")
    fails = 0

    cite_re = re.compile(r"\bSBR\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    bare_re = re.compile(r"(?<![A-Za-z])pp?\.\s*(\d[\d\s,\-–]*)")
    total = 0
    bare = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json", "sbr_index.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            in_refs = os.sep + "references" + os.sep in fp
            for m in cite_re.finditer(text):
                for p in expand(m.group(1)):
                    total += 1
                    if p < 1 or p > MAXP:
                        fails += 1
                        print(f"FAIL range: SBR p.{p} outside 1-{MAXP} in {os.path.relpath(fp, a.pkg)}")
            if in_refs and not fn.startswith("INDEX"):
                for m in bare_re.finditer(text):
                    for p in expand(m.group(1)):
                        bare += 1
                        if p < BODY_MIN or p > BODY_MAX:
                            fails += 1
                            print(f"FAIL range: p.{p} outside {BODY_MIN}-{BODY_MAX} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages in 'SBR p.N' citations; {bare} in loose 'p.N' in the references.")

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
            sblob = "".join(spages[p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    nt = norm(t)
                    if nt not in blob and squash(nt) not in sblob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    nt = norm(t)
                    if re.search(r"(?<![a-z0-9])" + re.escape(nt) + r"(?![a-z0-9])", blob) or (len(squash(nt)) >= 6 and squash(nt) in sblob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
