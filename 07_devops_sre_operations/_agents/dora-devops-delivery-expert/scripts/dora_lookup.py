# -*- coding: utf-8 -*-
"""
dora_lookup.py - finds DORA24 (Accelerate State of DevOps 2024) topics and their pages.

Usage:
  python -I scripts/dora_lookup.py TERM [TERM ...]
  python -I scripts/dora_lookup.py --list
  python -I scripts/dora_lookup.py --json TERM

Terms can be typed in English or Portuguese (the index keeps both).
Page convention: PDF page = printed number (checked). Read-only, no network.
When the collection does not cover the subject, it prints "NOT COVERED" (exit 2).
"""
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
INDEX = os.path.join(HERE, "dora_index.json")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def term_hits(q, term):
    t = norm(term)
    if q == t:
        return True
    if len(q) >= 3 and q in t:
        return True
    if len(t) >= 4 and t in q:
        return True
    return False


def search(data, query):
    q = norm(query)
    hits, ghits = [], []
    for e in data["entries"]:
        if any(term_hits(q, t) for t in e["terms"]) or (q and q in norm(e["id"])):
            hits.append(e)
    if not hits and len(q) >= 4:  # fallback: search the summary
        hits = [e for e in data["entries"] if q in norm(e["summary"])]
    for g in data["gaps"]:
        if any(term_hits(q, t) for t in g["terms"]):
            ghits.append(g)
    return hits, ghits


def fmt_pages(pages):
    pages = sorted(set(pages))
    out, start, prev = [], None, None
    for p in pages:
        if start is None:
            start = prev = p
        elif p == prev + 1:
            prev = p
        else:
            out.append(f"{start}" if start == prev else f"{start}-{prev}")
            start = prev = p
    if start is not None:
        out.append(f"{start}" if start == prev else f"{start}-{prev}")
    return ", ".join(out)


def main(argv):
    if not os.path.exists(INDEX):
        print("ERROR: dora_index.json not found", file=sys.stderr)
        return 1
    data = json.load(open(INDEX, encoding="utf-8"))
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    if "--list" in argv or not args:
        print(f"Source: {data['source']}")
        for e in data["entries"]:
            print(f"- {e['id']}: DORA24 p.{fmt_pages(e['pages'])}")
        return 0
    rc = 0
    results = {}
    for query in args:
        hits, ghits = search(data, query)
        results[query] = {"entries": [{"id": e["id"], "pages": e["pages"], "summary": e["summary"]} for e in hits],
                          "gaps": [g["hint"] for g in ghits]}
        if as_json:
            continue
        print(f"## {query}")
        if not hits and not ghits:
            print("NOT COVERED: no DORA24 topic matches. Do not cite a page; "
                  "answer only with a labeled [extrapolation] or say the report does not cover it.")
            rc = 2
            continue
        for e in hits:
            print(f"- [{e['id']}] DORA24 p.{fmt_pages(e['pages'])}: {e['summary']}")
        for g in ghits:
            print(f"- GAP: {g['hint']}")
        if not hits and ghits:
            print("NOT COVERED (content): see the gap above.")
            rc = 2
    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        if all(not v["entries"] for v in results.values()):
            rc = 2
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
