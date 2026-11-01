#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analytics_lookup.py - topic lookup in the package page index (KIMBALL, STREAM); also lists what the collection does NOT cover.

Usage:
  python -I analytics_lookup.py "<termo>"      # search by topic/keyword
  python -I analytics_lookup.py --list          # list all topics
  python -I analytics_lookup.py --not-covered   # known terms the collection does not cover

Pages = PDF (KIMBALL: printed = PDF - 3; STREAM: PDF = printed). Helland has no pages (the collection PDF is a different paper).
No network, read-only. Exit 0 if found; exit 1 with "NOT COVERED" if not found.
Input keywords: the index keeps Portuguese keywords and also has English ones; accents are ignored.
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


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def load():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics_index.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def word_in(term, text):
    return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", text) is not None


def search(q, data):
    qn = norm(q).strip()
    hits = []
    for key, t in data["topics"].items():
        score = 0
        if qn == norm(key):
            score += 10
        elif word_in(qn, norm(key).replace("_", " ")):
            score += 5
        if word_in(qn, norm(t["title"])):
            score += 4
        for kw in t["keywords"]:
            k = norm(kw)
            if qn == k:
                score += 3
            elif word_in(qn, k):
                score += 1
        if score:
            hits.append((score, key, t))
    hits.sort(key=lambda x: -x[0])
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("term", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--not-covered", action="store_true")
    a = ap.parse_args()
    data = load()
    if a.list:
        for k, t in data["topics"].items():
            pg = "; ".join("%s p.%s" % (s["sigla"], s["pages"]) for s in t["sources"]) or "NO PAGES"
            print("%-36s %s  [%s]" % (k, t["title"], pg))
        return 0
    if a.not_covered:
        print("The collection does NOT cover (or covers only in part) - label [extrapolation] or say 'the collection does not cover this':")
        for k, v in data["not_in_book_terms"].items():
            print("  - %s: %s" % (k, v))
        return 0
    if not a.term:
        ap.print_help()
        return 2
    q = " ".join(a.term)
    qn = norm(q)
    notes = [(k, v) for k, v in data["not_in_book_terms"].items() if word_in(norm(k), qn)]
    hits = search(q, data)
    if notes and any(word_in(norm(k), qn) and qn == norm(k) for k, _ in notes):
        hits = []
    if notes:
        print("=== Collection boundary for '%s' ===" % q)
        for k, v in notes:
            print("  [%s] %s" % (k, v))
    if not hits:
        if not notes:
            print("NOT COVERED: '%s' is not in the collection index (KIMBALL, STREAM). Label it [extrapolation] or say the collection does not cover it." % q)
        return 1
    print("=== Topics for '%s' (%d) ===" % (q, len(hits)))
    for _, k, t in hits[:8]:
        print("\n[%s] %s" % (k, t["title"]))
        if t["sources"]:
            for s in t["sources"]:
                print("  [%s] p.%s (PDF)" % (s["sigla"], s["pages"]))
        else:
            print("  NO PAGES (source absent from the corpus)")
        print("  reference: references/%s" % t["reference"])
        if t.get("note"):
            print("  note: %s" % t["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
