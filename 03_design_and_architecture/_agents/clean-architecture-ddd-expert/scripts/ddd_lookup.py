#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ddd_lookup.py - topic lookup in the curated corpus index (DDD, CA11, CA12, SRP, OCP, SREL, TARPIT, REACT).

Source: scripts/cleanarch_index.json, built by hand from reading the PDFs (no automatic keyword search).
Page convention: N = PDF page (DDD: printed = N - 7). All entries are [from source].
When the topic is NOT in the corpus (or is only mentioned), the script says "NOT COVERED" and exits with code 1.
Queries may be written in English or Portuguese (aliases in both languages are indexed).

Usage:
  python -I scripts/ddd_lookup.py --list
  python -I scripts/ddd_lookup.py --concept aggregate
  python -I scripts/ddd_lookup.py --query "dependency rule"
  python -I scripts/ddd_lookup.py "screaming architecture"        # forma posicional = --query
No network; read-only.
"""
import argparse
import json
import os
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "cleanarch_index.json")


def fold(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


def load():
    with open(INDEX, encoding="utf-8") as f:
        return json.load(f)


def show(topic):
    print("=== %s [%s] ===" % (topic["title"], topic["key"]))
    for e in topic["entries"]:
        print("  %s (%s p.%s): %s" % (e["label"], e["sigla"], e["pages"], e["summary"]))


def find(data, q):
    qf = fold(q)
    # 1) exact key or exact alias
    for tp in data["topics"]:
        if qf == fold(tp["key"]) or qf in [fold(a) for a in tp["aliases"]]:
            return [tp]
    # 2) partial match on key, title or aliases
    hits = []
    for tp in data["topics"]:
        hay = [fold(tp["key"]), fold(tp["title"])] + [fold(a) for a in tp["aliases"]]
        if any(qf in h or (len(h) > 3 and h in qf) for h in hay):
            hits.append(tp)
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("term", nargs="*", help="term (same as --query)")
    ap.add_argument("--list", action="store_true", help="list the indexed topics")
    ap.add_argument("--concept", help="topic by key or alias")
    ap.add_argument("--query", help="search by term (key, title or alias)")
    ap.add_argument("--not-covered", action="store_true", help="list topics known to be outside the corpus")
    a = ap.parse_args()
    data = load()

    if a.list:
        print("Convention: %s" % data["convencao_de_pagina"])
        for tp in data["topics"]:
            print(" - %-28s %s (%d refs)" % (tp["key"], tp["title"], len(tp["entries"])))
        return 0
    if a.not_covered:
        for k, v in data["not_covered"].items():
            print(" - %s: %s" % (k, v))
        return 0
    q = a.concept or a.query or " ".join(a.term)
    if not q:
        ap.print_help()
        return 2
    qf = fold(q)
    # out-of-corpus has precedence when the term matches exactly
    for k, v in data["not_covered"].items():
        if fold(k) == qf:
            print("NOT COVERED: '%s'. %s" % (q, v))
            return 1
    hits = find(data, q)
    if not hits:
        for k, v in data["not_covered"].items():
            if qf in fold(k) or fold(k) in qf:
                print("NOT COVERED: '%s'. %s" % (q, v))
                return 1
        print("NOT COVERED: '%s' is not in the corpus index. Label any answer as [extrapolation] or say that the corpus does not cover the topic." % q)
        return 1
    print("Convention: N = PDF page (DDD: printed = N - 7)")
    for tp in hits[:5]:
        show(tp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
