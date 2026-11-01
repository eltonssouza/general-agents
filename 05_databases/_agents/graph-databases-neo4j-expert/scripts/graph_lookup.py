# -*- coding: utf-8 -*-
"""
graph_lookup.py - topic lookup in the NEO4J book index (Robinson, Webber, Eifrem, 2nd ed.).

Usage:
  python -I graph_lookup.py "ifa"            keyword search
  python -I graph_lookup.py --list           list the topics
  python -I graph_lookup.py --topic storage  show one topic by key

Output: title, pages (PDF; printed = N - 18), summary and reference file.
If nothing matches: prints 'NOT COVERED in the collection' (exit code 1): the agent must not invent a page;
it must label [extrapolation] or say the book does not cover it.
If the term is in the not_in_book list, prints the specific warning (exit code 1).
Read-only, no network. Index origin: reading the PDF pages (see tests/relatorio-de-fidelidade.md).
Portuguese and English keywords are both recognized (accents are ignored).
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


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def load():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "graph_index.json"), encoding="utf-8") as f:
        return json.load(f)


def show(key, t):
    print("[%s] %s" % (key, t["title"]))
    print("  Pages   : %s   (PDF; printed = N - 18)" % t["pages"])
    print("  Summary : %s" % t["summary"])
    print("  Detail  : %s" % t["ref"])


def search(data, q):
    q = norm(q).strip()
    hits = []
    for key, t in data["topics"].items():
        score = 0
        if q == norm(key):
            score += 10
        elif q and q in norm(key):
            score += 5
        if q and q in norm(t["title"]):
            score += 3
        for kw in t["keywords"]:
            k = norm(kw)
            if q == k:
                score += 4
            elif len(q) >= 3 and (q in k or (len(k) >= 4 and k in q)):
                score += 1
        if score:
            hits.append((score, key, t))
    hits.sort(key=lambda x: -x[0])
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--topic")
    a = ap.parse_args()
    data = load()
    if a.list:
        for k, t in data["topics"].items():
            print("%-18s %s  [%s]" % (k, t["title"], t["pages"]))
        return 0
    if a.topic:
        t = data["topics"].get(a.topic)
        if not t:
            print("NOT COVERED in the collection: topic '%s' does not exist (use --list)." % a.topic)
            return 1
        show(a.topic, t)
        return 0
    q = " ".join(a.query).strip()
    if not q:
        ap.print_help()
        return 2
    nq = norm(q)
    warned = []
    for term, msg in data["not_in_book"].items():
        if norm(term) in nq:
            warned.append((term, msg))
    hits = search(data, q)
    for term, msg in warned:
        print("NOT IN THE SOURCE '%s': %s" % (term, msg))
    if not hits:
        print("NOT COVERED in the collection for '%s'. Do not cite a page; label it [extrapolation] or say the book does not cover it." % q)
        return 1
    if warned:
        print("Nearby topics that the book covers:")
    for _, key, t in hits[:5]:
        show(key, t)
    return 1 if warned else 0


if __name__ == "__main__":
    sys.exit(main())
