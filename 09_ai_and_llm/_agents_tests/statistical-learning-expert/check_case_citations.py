# -*- coding: utf-8 -*-
"""
check_case_citations.py - checks that every page listed under "Expected citations:" in tests/casos-de-teste.md
appears in some citation of the package references (references/*.md) or of the agent. Read-only, no network.
Usage: python -I tests/check_case_citations.py
"""
import os
import re
import sys

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cite_re = re.compile(r"\b(ISLR|ESL)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")


def expand(spec):
    out = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            out.extend(range(a, int(m.group(2) or a) + 1))
    return out


def collect():
    have = {"ISLR": set(), "ESL": set()}
    files = [os.path.join(PKG, "agents", "statistical-learning-expert.md")]
    for fn in os.listdir(os.path.join(PKG, "references")):
        if fn.endswith(".md"):
            files.append(os.path.join(PKG, "references", fn))
    for fp in files:
        for m in cite_re.finditer(open(fp, encoding="utf-8").read()):
            have[m.group(1)].update(expand(m.group(2)))
    return have


def main():
    have = collect()
    txt = open(os.path.join(PKG, "tests", "casos-de-teste.md"), encoding="utf-8").read()
    cases = re.split(r"\n### ", txt)[1:]
    bad = 0
    n = 0
    for c in cases:
        cid = c.split(" ", 1)[0]
        m = re.search(r"(?:Expected citations|Citações esperadas):\s*(.+)", c)
        if not m or "none" in m.group(1).lower() or "nenhuma" in m.group(1):
            continue
        n += 1
        for mm in cite_re.finditer(m.group(1)):
            for p in expand(mm.group(2)):
                if p not in have[mm.group(1)]:
                    bad += 1
                    print(f"FAIL {cid}: {mm.group(1)} p.{p} expected but absent from the references")
    print(f"Cases with expected citations: {n}; pages absent from the references: {bad}; total cases: {len(cases)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
