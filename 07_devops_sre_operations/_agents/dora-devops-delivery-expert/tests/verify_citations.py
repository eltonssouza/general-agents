# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package's citations against the text extracted from the DORA24 PDF.

Usage:
  python -I tests/verify_citations.py --src PATH/DORA-State-of-DevOps-Report-2024.txt [--pkg PACKAGE_ROOT]

1) Range: every citation "DORA24 p.N[-M][, ...]" must be within 1-120; any stray "p.N" > 120 fails.
2) Content (positive): each item of citation-checks.json["checks"] requires the page to contain ALL substrings.
3) Content (negative): each item of ["negative"] requires the substrings to be ABSENT from the cited page
   (or from the whole text when cite = "DORA24 all"): plausible claims that the report does not make.
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

MAXP = 120


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


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
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    pages = load_pages(a.src)
    if len(pages) != MAXP:
        print(f"WARNING: text has {len(pages)} pages (expected {MAXP})")
    fails = 0

    cite_re = re.compile(r"\bDORA24\s+p\.\s*(\d[\d\s,\-–]*)")
    bare_re = re.compile(r"(?<![A-Za-z0-9])p\.\s*(\d+)")
    total, distinct = 0, set()
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn == "verify_citations.py":
                continue
            fp = os.path.join(root, fn)
            if fn == "citation-checks.json":
                continue
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(1)):
                    total += 1
                    distinct.add(p)
                    if p < 1 or p > MAXP:
                        fails += 1
                        print(f"FAIL range: DORA24 p.{p} in {os.path.relpath(fp, a.pkg)}")
            for m in bare_re.finditer(text):
                p = int(m.group(1))
                if p > MAXP:
                    fails += 1
                    print(f"FAIL range: stray p.{p} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} page numbers checked; distinct pages cited: {len(distinct)}")

    data = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))
    ok = 0
    for c in data["checks"]:
        m = re.fullmatch(r"DORA24 p\.(\d+)", c["cite"])
        p = int(m.group(1))
        body = norm(pages.get(p, ""))
        miss = [s for s in c["contains"] if norm(s) not in body]
        if miss:
            fails += 1
            print(f"FAIL positive: {c['cite']} ({c['claim']}) does not contain {miss}")
        else:
            ok += 1
    print(f"Positive: {ok}/{len(data['checks'])} OK")

    nok = 0
    for c in data["negative"]:
        if c["cite"] == "DORA24 all":
            body = norm(" ".join(pages.values()))
        else:
            m = re.fullmatch(r"DORA24 p\.(\d+)", c["cite"])
            body = norm(pages.get(int(m.group(1)), ""))
        present = [s for s in c["absent"] if norm(s) in body]
        if present:
            fails += 1
            print(f"FAIL negative: {c['cite']} ({c['claim']}) contains {present}")
        else:
            nok += 1
    print(f"Negative: {nok}/{len(data['negative'])} OK (plausible claims that the report does NOT make)")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
