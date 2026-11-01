# -*- coding: utf-8 -*-
"""
os_lookup.py - looks up OSTEP (Operating Systems: Three Easy Pieces) topics and PDF pages.

Usage (from the package folder):
  python -I scripts/os_lookup.py TERMO [TERMO ...]
  python -I scripts/os_lookup.py --list
  python -I scripts/os_lookup.py --chapters

Output: topic, chapter, PDF pages (convention p.N = PDF page), reference file and note.
Queries may be English or Portuguese (Portuguese topic names are kept as aliases).
If the term is in the gap list, it says "NOT COVERED" (the book does not treat the subject).
If nothing is found, it also says "NOT COVERED in the index" and suggests nearby terms.
Read-only, no network, deterministic.
"""
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

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip()


def load():
    with open(os.path.join(HERE, "os_index.json"), encoding="utf-8") as f:
        return json.load(f)


def score(q, e):
    qn = norm(q)
    names = [norm(e["topic"])] + [norm(a) for a in e["aliases"]]
    best = 0
    for n in names:
        if qn == n:
            best = max(best, 100)
        elif re.search(r"(?<![a-z0-9])" + re.escape(qn) + r"(?![a-z0-9])", n):
            best = max(best, 70)
        elif qn in n or n in qn and len(n) >= 4:
            best = max(best, 40)
    qt = set(re.findall(r"[a-z0-9_\-/]+", qn))
    for n in names:
        nt = set(re.findall(r"[a-z0-9_\-/]+", n))
        if qt and nt and qt & nt and best < 30:
            best = max(best, 15 + 5 * len(qt & nt))
    return best


def main(argv):
    idx = load()
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        for e in idx["topics"]:
            print(f"ch.{e['chapter']:>2} p.{e['pages']:<9} {e['topic']}")
        return 0
    if argv[0] == "--chapters":
        print("See references/INDEX.md (chapter → PDF pages map).")
        return 0
    rc = 0
    for q in argv:
        qn = norm(q)
        for s in idx["sem_cobertura"]:
            for t in s["terms"]:
                if qn == norm(t) or re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", qn):
                    print(f"[{q}] NOT COVERED: OSTEP does not treat '{s['topic']}'. Answer as [extrapolation] or hand off "
                          f"(see references/12-seguranca-labs-e-lacunas-do-acervo.md).")
                    rc = 2
                    break
            else:
                continue
            break
        else:
            res = sorted(((score(q, e), e) for e in idx["topics"]), key=lambda x: -x[0])
            res = [(s, e) for s, e in res if s >= 15]
            if res and res[0][0] >= 70:
                res = [(s, e) for s, e in res if s >= 40]
            res = res[:5]
            if not res:
                print(f"[{q}] NOT COVERED in the package index (no topic matches). Check the spelling or use --list; "
                      f"if it is a general OS subject outside the book, label it [extrapolation].")
                rc = 2
                continue
            print(f"[{q}]")
            for s, e in res:
                print(f"  - {e['topic']} (ch.{e['chapter']}; OSTEP p.{e['pages']}) -> {e['ref']}\n      {e['note']}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
