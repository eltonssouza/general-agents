# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package's citations against the text extracted from the PDF.

Usage (from the package folder):
  python -I tests/verify_citations.py --src CAMINHO/scratch/devops [--pkg CAMINHO_DO_PACOTE]
  (--src is the folder that contains Linux-Introduction-to-Linux-TLDP.txt, with '=== PAGE N ===' markers)

Checks:
 1) Range: every citation 'p.N' or 'p.N-M' (and lists 'p.N, M') in the package's .md/.json/.py files must exist (1..223).
 2) Content (positive): each item of citation-checks.json['checks'] requires the page to contain all the substrings.
 3) Negative: 'absent' (terms absent from the whole PDF body 9-211) and 'absent_on_page' (absent from the page).
 4) Index: the command pages of scripts/linux_index.json are recomputed from the text and compared.
 5) Topics: every topic page exists and the pages cited in the 'points' belong to the PDF range.
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

FILE = "Linux-Introduction-to-Linux-TLDP.txt"
MAXP = 223


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
    pages = load_pages(os.path.join(a.src, FILE))
    if len(pages) != MAXP:
        print(f"WARNING: the text has {len(pages)} pages (expected {MAXP})")
    fails = 0

    # 1) range
    cite_re = re.compile(r"(?<![\w.])p\.\s*(\d[\d\s,\-–]*)")
    total, distinct = 0, set()
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(1).rstrip(" ,-–")):
                    total += 1
                    distinct.add(p)
                    if p < 1 or p > MAXP:
                        fails += 1
                        print(f"FAIL range: p.{p} outside 1..{MAXP} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} page numbers checked; distinct pages cited: {len(distinct)}")

    chk = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))

    # 2) positive
    ok = 0
    for c in chk["checks"]:
        m = re.fullmatch(r"TLDP p\.(\d+)", c["cite"])
        p = int(m.group(1))
        body = norm(pages.get(p, ""))
        miss = [s for s in c["contains"] if norm(s) not in body]
        if miss:
            fails += 1
            print(f"FAIL content: {c['cite']} ({c['claim']}) does not contain {miss}")
        else:
            ok += 1
    print(f"Positive: {ok}/{len(chk['checks'])} checks OK")

    # 3) negative
    nok = ntot = 0
    for n in chk.get("negative_checks", []):
        if n["type"] == "absent":
            body = norm(" ".join(pages[p] for p in range(9, 212) if p in pages))
        else:
            p = int(re.fullmatch(r"TLDP p\.(\d+)", n["cite"]).group(1))
            body = norm(pages.get(p, ""))
        for t in n["terms"]:
            ntot += 1
            if norm(t) in body:
                fails += 1
                print(f"FAIL negative: '{t}' APPEARS in the book ({n.get('cite', 'body')}); claim '{n['claim']}' is wrong")
            else:
                nok += 1
    print(f"Negative: {nok}/{ntot} terms absent as claimed")

    # 4) command index
    idx = json.load(open(os.path.join(a.pkg, "scripts", "linux_index.json"), encoding="utf-8"))
    bad = 0
    for name, c in idx["commands"].items():
        rx = re.compile(r"(?<![\w.\-/])" + re.escape(name) + r"(?![\w\-])")
        pg = [p for p in range(9, 208) if p in pages and rx.search(pages[p])]
        if pg != c["pages"]:
            bad += 1
            fails += 1
            print(f"FAIL index: command '{name}' pages differ")
    print(f"Command index: {len(idx['commands']) - bad}/{len(idx['commands'])} OK")

    # 5) topics
    tbad = 0
    for k, t in idx["topics"].items():
        for p in t["pages"]:
            if p not in pages:
                tbad += 1
                fails += 1
                print(f"FAIL topic {k}: page {p} does not exist")
        for pt in t["points"]:
            for m in re.finditer(r"\(p\.([\d,\s\-–]+)\)", pt):
                for p in expand(m.group(1)):
                    if p not in pages:
                        tbad += 1
                        fails += 1
                        print(f"FAIL topic {k}: point cites nonexistent p.{p}")
    print(f"Topics: {len(idx['topics'])} checked, {tbad} problems")

    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
