# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package citations against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src CAMINHO/css_a11y_design [--pkg PACKAGE_PATH]

1) Range: every citation (CSSHB|MDNFS|MDNL) p.N[-M][, ...] must exist (CSSHB 1-214, MDNFS 1-4, MDNL 1-3).
2) Content: each item of tests/citation-checks.json requires the page to contain the substrings.
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

FILES = {"CSSHB": "Modern-CSS-Handbook-freeCodeCamp.txt", "MDNFS": "Modern-CSS-MDN-First-Steps.txt",
         "MDNL": "Modern-CSS-MDN-Layout.txt"}
MAXP = {"CSSHB": 214, "MDNFS": 4, "MDNL": 3}


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
    ap.add_argument("--src", required=True, help="folder with the extracted .txt files")
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in FILES.items()}
    for k, p in pages.items():
        if len(p) != MAXP[k]:
            print(f"WARNING: {k} has {len(p)} pages in the text (expected {MAXP[k]})")
    fails = 0

    # 1) range
    cite_re = re.compile(r"\b(CSSHB|MDNFS|MDNL)\s+p\.\s*([\d][\d\s,\-–]*)")
    total, per = 0, {k: set() for k in FILES}
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")) or fn == "verify_citations.py":
                continue
            fp = os.path.join(root, fn)
            if os.sep + "tests" + os.sep in fp and fn.endswith(".json"):
                continue
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(2)):
                    total += 1
                    per[m.group(1)].add(p)
                    if p < 1 or p > MAXP[m.group(1)]:
                        fails += 1
                        print(f"FAIL range: {m.group(1)} p.{p} out of range in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} page numbers checked; distinct pages cited: "
          + ", ".join(f"{k}={len(v)}" for k, v in per.items()))

    # 2) content
    checks = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))["checks"]
    ok = 0
    for c in checks:
        m = re.fullmatch(r"(CSSHB|MDNFS|MDNL) p\.(\d+)", c["cite"])
        src, p = m.group(1), int(m.group(2))
        body = norm(pages[src].get(p, ""))
        miss = [s for s in c["contains"] if norm(s) not in body]
        if miss:
            fails += 1
            print(f"FAIL content: {c['cite']} ({c['claim']}) does not contain {miss}")
        else:
            ok += 1
    print(f"Content: {ok}/{len(checks)} checks OK")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
