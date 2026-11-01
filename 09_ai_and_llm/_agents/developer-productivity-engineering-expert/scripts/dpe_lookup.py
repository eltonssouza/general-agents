# -*- coding: utf-8 -*-
"""
dpe_lookup.py - deterministic topic search in the DPE corpus (Developer Productivity Engineering Handbook, Gradle Inc., 2022).
Stdlib, no network, read-only. Pages = PDF; printed = PDF - 5.
Search terms may be in English or Portuguese (the index keeps both).

Usage:
  python -I scripts/dpe_lookup.py TERM [--top N] [--json]
  python -I scripts/dpe_lookup.py --page N        # chapter and printed page
  python -I scripts/dpe_lookup.py --printed N     # converts printed -> PDF
  python -I scripts/dpe_lookup.py --chapters | --chapter ID | --gaps | --datado
Prints "NOT COVERED" when the term is in the verified gaps or there is no match.
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

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "dpe_index.json"), encoding="utf-8"))
OFF = DATA["offset_impressa"]
NPAGES = DATA["total_paginas"]

# terms verified as absent from the text -> NOT COVERED (compared accent-free, lowercase); English and Portuguese alternates
ABSENT = [
    "data platform", "plataforma de dados", "data lake", "etl", "airflow", "spark", "kafka", "mlops", "dbt", "warehouse",
    "dora", "space framework", "deployment frequency", "lead time", "develocity", "platform engineering",
    "internal developer platform", "github actions", "kubernetes", "docker", "terraform", "bazel", "monorepo", "copilot", "llm",
    "inteligencia artificial", "artificial intelligence", "machine learning", "tdd", "piramide de testes", "test pyramid",
    "pyramid", "sonar", "mutation",
]


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def chapter_of(p):
    for c in DATA["chapters"]:
        if c["pdf"][0] <= p <= c["pdf"][1]:
            return c
    return None


def score(topic, q):
    nq = norm(q)
    toks = [t for t in re.split(r"\W+", nq) if t]
    best = 0
    hay = norm(topic["topic"])
    kws = [norm(k) for k in topic["keywords"]]
    if nq in hay:
        best += 5
    for k in kws:
        if nq == k:
            best += 6
        elif nq in k or (len(k) > 3 and k in nq):
            best += 3
    for t in toks:
        if len(t) < 3:
            continue
        if t in hay:
            best += 1
        if any(t in k for k in kws):
            best += 1
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("term", nargs="?")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--chapter")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--datado", action="store_true", help="list the [DATED] items")
    a = ap.parse_args()

    if a.page is not None:
        p = a.page
        if not 1 <= p <= NPAGES:
            print(f"Page {p} is outside the PDF (1-{NPAGES}).")
            return 1
        c = chapter_of(p)
        pr = p - OFF
        printed = f"printed {pr}" if pr >= 1 else "no printed number (cover/title page/table of contents)"
        if c:
            print(f"PDF p.{p} = {printed}; Ch.{c['id']}: {c['title']} -> references/{c['ref']}")
        else:
            print(f"PDF p.{p} = {printed}; page without a chapter (blank, table of contents or part divider)")
        return 0
    if a.printed is not None:
        p = a.printed + OFF
        print(f"printed {a.printed} = PDF p.{p}" if 1 <= p <= NPAGES else f"printed {a.printed} is outside the book")
        return 0
    if a.chapters:
        for c in DATA["chapters"]:
            print(f"Ch.{c['id']}: {c['title']} | PDF {c['pdf'][0]}-{c['pdf'][1]} (printed {c['pdf'][0]-OFF}-{c['pdf'][1]-OFF}) | references/{c['ref']}")
        return 0
    if a.chapter:
        for c in DATA["chapters"]:
            if c["id"] == a.chapter:
                print(f"Ch.{c['id']}: {c['title']} | PDF {c['pdf'][0]}-{c['pdf'][1]} | references/{c['ref']}")
                return 0
        print("NOT COVERED: nonexistent chapter (use --chapters)")
        return 1
    if a.gaps:
        print("Verified gaps (NOT COVERED):")
        for g in DATA["gaps"]:
            print(f"- {g['term']}: {g['why']}")
        return 0
    if a.datado:
        print("[DATED] items:")
        for d in DATA["datado"]:
            print("- " + d)
        return 0
    if not a.term:
        ap.print_help()
        return 2

    nq = norm(a.term)
    for ab in ABSENT:
        if re.search(r"(?<![a-z0-9])" + re.escape(ab) + r"(?![a-z0-9])", nq):
            msg = (f"NOT COVERED: '{a.term}' does not appear in the DPE corpus (Developer Productivity Engineering, Gradle, 2022). "
                   "Use [extrapolation] only if the user asks, without a page.")
            if "data" in nq or "dados" in nq:
                msg += (" Note: the file is named Data-Platform-Engineering..., but the content is different "
                        "(see references/INDEX.md §1).")
            print(msg)
            return 0
    ranked = sorted(((score(t, a.term), t) for t in DATA["topics"]), key=lambda x: -x[0])
    ranked = [(s, t) for s, t in ranked if s > 0][: a.top]
    if not ranked:
        print(f"NOT COVERED: no topic matches '{a.term}'. Try --chapters or --gaps.")
        return 0
    if a.json:
        print(json.dumps([dict(t, score=s) for s, t in ranked], ensure_ascii=False, indent=1))
        return 0
    for s, t in ranked:
        print(f"[{s}] {t['topic']} | DPE p.{t['pages']} (PDF) | references/{t['ref']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
