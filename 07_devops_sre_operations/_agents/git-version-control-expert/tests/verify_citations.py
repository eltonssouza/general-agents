# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package citations against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/devops [--pkg PACKAGE_PATH]
  (the --src folder must contain Git-Pro-Git-EN.txt and Git-Pro-Git-PT-BR.txt, with "=== PAGE N ===" markers)

1) Range: every citation (PGEN|PGBR) p.N[-M][, ...] must exist (PGEN 1-501, PGBR 1-500).
2) Positive content: each "checks" item in tests/citation-checks.json requires the page to contain
   ALL the substrings (case-insensitive; whitespace/NBSP collapsed; typographic quotes normalized).
3) NEGATIVE checks: each "negatives" item requires that NONE of the substrings appears on ANY page of the
   range (proves that the book does NOT contain the plausible claim).
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

FILES = {"PGEN": "Git-Pro-Git-EN.txt", "PGBR": "Git-Pro-Git-PT-BR.txt"}
MAXP = {"PGEN": 501, "PGBR": 500}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("�", "?")
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
    cite_re = re.compile(r"\b(PGEN|PGBR)\s+p\.\s*([\d][\d\s,\-–]*)")
    total, per = 0, {k: set() for k in FILES}
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py")) or fn == "verify_citations.py":
                continue
            fp = os.path.join(root, fn)
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

    data = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))

    # 2) positive content
    ok = 0
    checks = data["checks"]
    for c in checks:
        m = re.fullmatch(r"(PGEN|PGBR) p\.(\d+)", c["cite"])
        src, p = m.group(1), int(m.group(2))
        body = norm(pages[src].get(p, ""))
        miss = [s for s in c["contains"] if norm(s) not in body]
        if miss:
            fails += 1
            print(f"FAIL content: {c['cite']} ({c['claim']}) does not contain {miss}")
        else:
            ok += 1
    print(f"Content: {ok}/{len(checks)} checks OK")

    # 3) negatives
    nok = 0
    negs = data["negatives"]
    for n in negs:
        src = n["scope"]
        rng = expand(n.get("pages", f"1-{MAXP[src]}"))
        hits = []
        for p in sorted(rng):
            body = norm(pages[src].get(p, ""))
            for s in n["absent"]:
                if norm(s) in body:
                    hits.append((s, p))
        if hits:
            fails += 1
            print(f"FAIL negative: {src} '{n['claim']}' but found {hits[:4]}")
        else:
            nok += 1
    print(f"Negatives: {nok}/{len(negs)} OK (the book does NOT contain the term in the range)")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
