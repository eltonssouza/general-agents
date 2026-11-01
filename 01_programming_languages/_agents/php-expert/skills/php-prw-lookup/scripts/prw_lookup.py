#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prw_lookup.py - topic search in the index of "PHP: The Right Way" (PRW). Read-only, no network.

Usage:
  python -I prw_lookup.py "pdo"            # topics and pages (PDF)
  python -I prw_lookup.py "strict_types"   # -> NOT COVERED (not in the book)
  python -I prw_lookup.py --list           # list the topics
  python -I prw_lookup.py --not-in-book    # list what the book does NOT cover
  python -I prw_lookup.py --json "composer"

Queries may be in English or Portuguese (the index keeps Portuguese keywords alongside English ones).

Origin: the index (prw_index.json) was built by reading the PDF pages (convention: PDF page).
When there is no topic, the script says NOT COVERED instead of inventing a page.
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


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def load():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "prw_index.json"), encoding="utf-8") as f:
        return json.load(f)


def _bounded(needle, hay):
    """needle inside hay, without sticking to letters/digits (avoids 'throw' matching 'throwable')."""
    return re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", hay) is not None


def kw_match(q, kw):
    """True if the query q matches the keyword kw (short ones only by equality)."""
    kw = fold(kw)
    if q == kw:
        return True
    if len(kw) < 4 or len(q) < 3:
        return False
    return _bounded(kw, q) or _bounded(q, kw)


def search(q, data):
    q = fold(q)
    notes = [n["note"] for n in data["not_in_book"] if any(kw_match(q, k) for k in n["keywords"])]
    topics = []
    for t in data["topics"]:
        score = 0
        if any(kw_match(q, k) for k in t["keywords"]):
            score += 3
        if len(q) >= 3 and (_bounded(q, fold(t["title"])) or _bounded(q, fold(t["id"]))):
            score += 2
        if not notes and len(q) >= 4 and _bounded(q, fold(t["summary"])):
            score += 1
        if score:
            topics.append((score, t))
    topics.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [t for _, t in topics], notes


def main():
    ap = argparse.ArgumentParser(description="Topic search in the PRW (page = PDF).")
    ap.add_argument("query", nargs="*", help="search term")
    ap.add_argument("--list", "-l", action="store_true")
    ap.add_argument("--not-in-book", action="store_true", help="list what the book does not cover")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    data = load()
    b = data["book"]

    if a.list:
        for t in data["topics"]:
            print(f"{t['id']:<28} PRW p.{t['pages']:<8} {t['title']}")
        return 0
    if a.not_in_book:
        for n in data["not_in_book"]:
            print("- " + ", ".join(n["keywords"][:6]) + "\n    " + n["note"])
        return 0
    if not a.query:
        ap.print_help()
        return 1

    q = " ".join(a.query)
    topics, notes = search(q, data)
    if a.json:
        print(json.dumps({"query": q, "topics": topics, "not_in_book": notes}, ensure_ascii=False, indent=2))
        return 0 if topics or notes else 2
    print(f"Query: {q!r}   (convention: PDF page; {b['snapshot']})")
    if not topics and not notes:
        print("NOT COVERED: the PRW index has no topic for this term. If you answer, label it [extrapolation].")
        return 2
    for t in topics[:6]:
        print(f"\n[{t['id']}] {t['title']}  -> [from source] (PRW p.{t['pages']})")
        print(f"  {t['summary']}")
    if notes:
        print("\nNOT COVERED BY THE BOOK (only [extrapolation]):")
        for n in notes:
            print(f"  - {n}")
        if not topics:
            print("NOT COVERED: there is no page to cite.")
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
