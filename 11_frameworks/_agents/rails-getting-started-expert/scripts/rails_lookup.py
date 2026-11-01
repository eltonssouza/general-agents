# -*- coding: utf-8 -*-
"""
rails_lookup.py - locates topics of the RGS guide (Getting Started with Rails, Rails 8.1.0+) with pages.

Usage:
  python -I scripts/rails_lookup.py TERMO [TERMO ...] [--json]
  python -I scripts/rails_lookup.py --topics        # lists all topics
  python -I scripts/rails_lookup.py --page N        # topics that touch page N (1-72)
  python -I scripts/rails_lookup.py --gaps          # list of NOT COVERED themes
Page convention: PDF page = printed "Page N of 72". Read-only, no network, deterministic.
Terms may be given in English or Portuguese (the index keeps keywords in both).
Outputs "NOT COVERED" when the term is a known gap or matches no topic.
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
MAXP = 72


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def parse_pages(spec):
    out = set()
    for tok in re.split(r"\s*,\s*", spec):
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", tok.strip())
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            out.update(range(a, b + 1))
    return out


def load():
    with open(os.path.join(HERE, "rails_index.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def has_word(q, kw):
    kw = norm(kw)
    return re.search(r"(?<![a-z0-9_])" + re.escape(kw) + r"(?![a-z0-9_])", q) is not None


def search(idx, term):
    q = norm(term)
    gap_hit = [g for g in idx["gaps"] if any(has_word(q, k) for k in g["keywords"])]
    hits = []
    for t in idx["topics"]:
        score = 0
        if q and q in norm(t["title"]):
            score += 3
        for k in t["keywords"]:
            nk = norm(k)
            if not nk:
                continue
            if nk == q:
                score += 5
            elif has_word(q, nk) or (len(q) >= 4 and q in nk):
                score += 2
        if score:
            hits.append((score, t))
    hits.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [t for _, t in hits], gap_hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--topics", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--page", type=int)
    a = ap.parse_args()
    idx = load()

    if a.topics:
        for t in idx["topics"]:
            print(f"{t['id']:16} RGS p.{t['pages']:12} {t['title']}  -> references/{t['ref']}")
        return
    if a.gaps:
        print("NOT COVERED in the RGS guide (Rails 8.1.0+):")
        for g in idx["gaps"]:
            print(f" - {g['term']}")
        return
    if a.page is not None:
        if not 1 <= a.page <= MAXP:
            print(f"Page outside 1-{MAXP}.")
            sys.exit(1)
        found = [t for t in idx["topics"] if a.page in parse_pages(t["pages"])]
        if not found:
            print(f"No topic indexed for RGS p.{a.page}.")
        for t in found:
            print(f"RGS p.{a.page}: {t['title']} (pages {t['pages']}) -> references/{t['ref']}")
        return
    if not a.terms:
        ap.print_help()
        sys.exit(2)

    result = []
    rc = 0
    for term in a.terms:
        topics, gaps = search(idx, term)
        result.append({"termo": term, "topicos": topics, "sem_cobertura": [g["term"] for g in gaps]})
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return
    for r in result:
        print(f"== {r['termo']}")
        if r["sem_cobertura"]:
            print("NOT COVERED: " + "; ".join(r["sem_cobertura"]) + " (the guide does not cover this; any answer is [extrapolation]).")
        for t in r["topicos"][:6]:
            print(f" - {t['title']}: RGS p.{t['pages']} -> references/{t['ref']}")
        if not r["topicos"] and not r["sem_cobertura"]:
            print("NOT COVERED: no topic of the guide matches this term.")


if __name__ == "__main__":
    main()
