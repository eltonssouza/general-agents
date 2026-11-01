# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package citations against the extracted OSTEP text.

Usage:
  python -I tests/verify_citations.py --src PATH/OSTEP-Operating-Systems-Three-Easy-Pieces.txt [--pkg PACKAGE_PATH]

Checks (read-only, no network; exit 0 if everything passes, 1 otherwise):
 1) RANGE: every citation "OSTEP p.N[-M][, ...]" in the package files must be between 1 and 834.
 2) CONTENT (positive): each item of tests/citation-checks.json "checks" requires the PDF page to contain ALL the substrings.
 3) NEGATIVES: "negative_checks" assert absence (regex over the whole book, or terms absent from specific pages).
 4) INDEX: each topic of scripts/os_index.json must have its "check" terms present on some page of the "pages" range.
 5) CHAPTER MAP: the title of each chapter in the INDEX.md map appears on the starting page (page convention).
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

MAXP = 834
LIG = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}


def norm(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def variants(raw):
    return [norm(raw), norm(raw.replace("-\n", ""))]


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


def has(pages, p, term):
    return any(norm(term) in v for v in variants(pages.get(p, "")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="text file extracted from OSTEP (markers === PAGE N ===)")
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    pages = load_pages(a.src)
    if len(pages) != MAXP:
        print(f"WARNING: the text has {len(pages)} pages (expected {MAXP})")
    fails = 0

    # 1) range
    cite_re = re.compile(r"\b(?:OSTEP\s+)?p\.\s*(\d[\d\s,\-–]*)")
    total = 0
    distinct = set()
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")) or fn == "verify_citations.py":
                continue
            fp = os.path.join(root, fn)
            if os.sep + "tests" + os.sep in fp and fn.endswith(".json"):
                continue
            if os.sep + "fixtures" + os.sep in fp:
                continue
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(1)):
                    total += 1
                    distinct.add(p)
                    if p < 1 or p > MAXP:
                        fails += 1
                        print(f"FAIL range: p.{p} outside 1-{MAXP} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} page numbers checked; distinct pages cited: {len(distinct)}")

    cj = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))

    # 2) positive
    ok = 0
    for c in cj["checks"]:
        m = re.fullmatch(r"OSTEP p\.(\d+)", c["cite"])
        p = int(m.group(1))
        miss = [s for s in c["contains"] if not has(pages, p, s)]
        if miss:
            fails += 1
            print(f"FAIL content: {c['cite']} ({c['claim']}) does not contain {miss}")
        else:
            ok += 1
    print(f"Content (positive): {ok}/{len(cj['checks'])} checks OK")

    # 3) negatives
    nok = 0
    for n in cj.get("negative_checks", []):
        if "regex_absent_everywhere" in n:
            rx = re.compile(n["regex_absent_everywhere"], re.I)
            hit = [p for p, t in pages.items() if rx.search(norm(t))]
            if hit:
                fails += 1
                print(f"FAIL negative: '{n['claim']}' but the pattern appears on p.{hit[:6]}")
            else:
                nok += 1
        else:
            ps = expand(n["pages"])
            bad = [(p, t) for p in ps for t in n["absent"] if has(pages, p, t)]
            if bad:
                fails += 1
                print(f"FAIL negative: '{n['claim']}' but found {bad[:4]}")
            else:
                nok += 1
    print(f"Content (negative): {nok}/{len(cj.get('negative_checks', []))} checks OK")

    # 4) index
    ij = json.load(open(os.path.join(a.pkg, "scripts", "os_index.json"), encoding="utf-8"))
    iok = 0
    for e in ij["topics"]:
        ps = expand(e["pages"])
        miss = [t for t in e["check"] if not any(has(pages, p, t) for p in ps)]
        if any(p < 1 or p > MAXP for p in ps):
            fails += 1
            print(f"FAIL index: pages out of range in '{e['topic']}'")
        elif miss:
            fails += 1
            print(f"FAIL index: '{e['topic']}' p.{e['pages']} does not contain {miss}")
        else:
            iok += 1
    print(f"Index: {iok}/{len(ij['topics'])} topics OK")
    # index gaps: absent from the book
    sok = 0
    for s in ij["sem_cobertura"]:
        bad = []
        for t in s["terms"]:
            rx = re.compile(r"(?<![a-z0-9_])" + re.escape(norm(t)) + r"(?![a-z0-9_])")
            if any(rx.search(norm(tx)) for tx in pages.values()):
                bad.append(t)
        if bad:
            fails += 1
            print(f"FAIL sem_cobertura: terms {bad} of '{s['topic']}' appear in the book")
        else:
            sok += 1
    print(f"Gaps (sem_cobertura): {sok}/{len(ij['sem_cobertura'])} OK")

    # 5) chapter map
    idx = open(os.path.join(a.pkg, "references", "INDEX.md"), encoding="utf-8").read()
    cok = ctot = 0
    for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*(\d+)-(\d+)\s*\|", idx, re.M):
        n, title, a0, b0 = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
        ctot += 1
        words = [w for w in re.findall(r"[A-Za-z]+", title) if len(w) > 3][:3]
        body = norm(pages.get(a0, ""))
        if n in (1, 3, 12, 25, 35, 47, 52):
            ok_title = "dialogue" in body or "dialogue" in norm(pages.get(a0 + 0, ""))
        else:
            ok_title = all(w.lower() in body for w in words)
        if ok_title and 1 <= a0 <= b0 <= MAXP:
            cok += 1
        else:
            fails += 1
            print(f"FAIL map: ch.{n} '{title}' p.{a0}-{b0}: title not found on the starting page")
    print(f"Chapter map: {cok}/{ctot} OK")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
