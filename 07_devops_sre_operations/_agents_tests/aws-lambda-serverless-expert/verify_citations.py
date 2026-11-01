# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package citations against the text extracted from the PDF (read-only, no network).

Usage:
  python -I tests/verify_citations.py [--text PATH/AWS-Lambda-Developer-Guide.txt] [--pkg PACKAGE_ROOT] [-v]

1) Range: every citation 'LAMBDA p.N[-M][, ...]' in agents/, references/, scripts/, tests/*.md, README and AGENTS must be between 1 and 1297.
2) Content (positives): each item of tests/citation-checks.json requires the cited page/range to contain ALL the substrings
   (NFKC comparison, lowercase, collapsed whitespace - PDF ligatures handled). The `claim` field is a human-readable
   description (English); `contains` holds the verbatim source-text substrings.
3) Negatives: plausible claims that the book does NOT contain; no substring may appear in the indicated range.
Exit 0 if everything passes, 1 otherwise; 2 if the extracted text is missing (the test runner then skips this check).
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

MAXP = 1297


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = set()
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.update(range(a, b + 1))
    return pages


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkg", default=os.path.dirname(here))
    default_txt = os.path.normpath(os.path.join(here, "..", "..", "..", "..", "scratch", "devops", "AWS-Lambda-Developer-Guide.txt"))
    ap.add_argument("--text", default=default_txt)
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(a.text):
        print("Extracted text not found:", a.text)
        return 2
    pages = load_pages(a.text)
    if len(pages) != MAXP:
        print(f"WARNING: {len(pages)} pages in the text (expected {MAXP})")
    bad = 0

    # 1) range
    cite_re = re.compile(r"LAMBDA pp?\.\s*(\d+(?:\s*[-–]\s*\d+)?(?:,\s*\d+(?:\s*[-–]\s*\d+)?)*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        if "__pycache__" in root:
            continue
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")) or fn == "citation-checks.json":
                continue
            fp = os.path.join(root, fn)
            for i, line in enumerate(open(fp, encoding="utf-8", errors="replace"), 1):
                for m in cite_re.finditer(line):
                    total += 1
                    for pg in expand(m.group(1)):
                        if pg < 1 or pg > MAXP:
                            bad += 1
                            print(f"RANGE: {os.path.relpath(fp, a.pkg)}:{i}: p.{pg} outside 1-{MAXP}")
    print(f"[1] citations scanned in files: {total}; out of range: {bad}")

    # 2) positives
    data = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))
    pos = data["checks"]
    pf = 0
    for c in pos:
        spec = c["cite"].replace("LAMBDA p.", "")
        pgs = expand(spec)
        if not pgs or any(p not in pages for p in pgs):
            pf += 1
            print(f"PAGE NOT FOUND: {c['cite']} :: {c['claim'][:70]}")
            continue
        ok = all(any(norm(k) in pages[p] for p in pgs) for k in c["contains"])
        if not ok:
            pf += 1
            miss = [k for k in c["contains"] if not any(norm(k) in pages[p] for p in pgs)]
            print(f"FAIL: {c['cite']} :: missing {miss} :: {c['claim'][:70]}")
        elif a.v:
            print("ok", c["cite"])
    print(f"[2] positive checks: {len(pos)}; failures: {pf}")
    bad += pf

    # 3) negatives
    nf = 0
    for n in data["negatives"]:
        pgs = expand(n["range"])
        for term in n["absent"]:
            nt = norm(term)
            hit = [p for p in sorted(pgs) if nt in pages.get(p, "")]
            if hit:
                nf += 1
                print(f"NEGATIVE FAILED (#{n['id']}): '{term}' appears in p.{hit[:5]} :: {n['claim']}")
    print(f"[3] negative checks: {len(data['negatives'])} claims ({sum(len(n['absent']) for n in data['negatives'])} terms); failures: {nf}")
    bad += nf
    print("RESULT:", "OK" if bad == 0 else f"{bad} problem(s)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
