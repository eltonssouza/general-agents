# -*- coding: utf-8 -*-
"""
nbf_lookup.py - locates topics, sources and pages in the Node/Express/Fastify/NestJS collection.

Sources (acronyms): NODEHB (Node Handbook, 2018), EXPHB (Express Handbook, 2022),
FSTF (Fastify Getting Started, v5.12.x), NEST (NestJS First steps).
Page convention: N = PDF page (marker "=== PAGE N ==="). The PDFs have no printed page numbers.

Usage:
  python -I scripts/nbf_lookup.py TERM [TERM ...] [--src NODEHB|EXPHB|FSTF|NEST] [--json]
  python -I scripts/nbf_lookup.py --page N --src ACRONYM
  python -I scripts/nbf_lookup.py --topics [--src ACRONYM]
  python -I scripts/nbf_lookup.py --sources
  python -I scripts/nbf_lookup.py --gaps

Deterministic, stdlib, no network. Prints "NOT COVERED" when the term belongs to a known gap
in the collection (and, if any, the few points of contact). Does not execute anything from the target.
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
INDEX = os.path.join(HERE, "nbf_index.json")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def load():
    with open(INDEX, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_pages(p):
    return f"p.{p[0]}" if p[0] == p[1] else f"p.{p[0]}-{p[1]}"


def score(topic, q):
    qn = norm(q)
    if not qn:
        return 0
    sc = 0
    for k in topic["kw"]:
        kn = norm(k)
        if qn == kn:
            sc += 10
        elif len(qn) >= 3 and (qn in kn or kn in qn):
            sc += 4
    if len(qn) >= 3 and qn in norm(topic["title"]):
        sc += 5
    if len(qn) >= 3 and qn in norm(topic["summary"]):
        sc += 2
    if qn == norm(topic["id"]):
        sc += 20
    return sc


def gap_hits(data, q):
    qn = norm(q)
    hits = []
    for g in data["gaps"]:
        for t in g["terms"]:
            tn = norm(t)
            if qn == tn or re.search(r"(?<![a-z0-9])" + re.escape(tn) + r"(?![a-z0-9])", qn):
                hits.append(g)
                break
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--src")
    ap.add_argument("--page", type=int)
    ap.add_argument("--topics", action="store_true")
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max", type=int, default=8)
    a = ap.parse_args(argv)
    data = load()
    src = a.src.upper() if a.src else None
    if src and src not in data["sources"]:
        print(f"Unknown source: {src}. Use one of {', '.join(data['sources'])}.")
        return 2

    if a.sources:
        for k, v in data["sources"].items():
            print(f"{k}: {v['file']}.pdf | {v['pdf_pages']} pages | date: {v['date'] or 'not declared'} | {v['note']}")
        return 0
    if a.gaps:
        for g in data["gaps"]:
            print(f"NOT COVERED [{g['id']}]: {g['note']}")
            print("   terms: " + ", ".join(g["terms"]))
        return 0
    if a.topics:
        for t in data["topics"]:
            if src and t["src"] != src:
                continue
            print(f"{t['src']} {fmt_pages(t['pages'])}\t{t['id']}\t{t['title']}\t-> references/{t['ref']}")
        return 0
    if a.page is not None:
        if not src:
            print("--page requires --src ACRONYM")
            return 2
        res = [t for t in data["topics"] if t["src"] == src and t["pages"][0] <= a.page <= t["pages"][1]]
        if not res:
            print(f"NOT COVERED in the index for {src} p.{a.page} (may be an empty page, figure, footer or outside the topics).")
            return 1
        for t in res:
            print(f"{t['src']} {fmt_pages(t['pages'])}: {t['title']} -> references/{t['ref']}\n   {t['summary']}")
        return 0
    if not a.terms:
        ap.print_help()
        return 2

    out = []
    code = 0
    for q in a.terms:
        gh = gap_hits(data, q)
        ranked = []
        for t in data["topics"]:
            if src and t["src"] != src:
                continue
            s = score(t, q)
            if s > 0:
                ranked.append((s, t))
        ranked.sort(key=lambda x: (-x[0], x[1]["src"], x[1]["pages"][0]))
        ranked = ranked[: a.max]
        out.append({"termo": q, "sem_cobertura": [g["note"] for g in gh],
                    "resultados": [{"src": t["src"], "pages": t["pages"], "id": t["id"], "title": t["title"],
                                    "ref": t["ref"], "score": s} for s, t in ranked]})
        if not args_json(a):
            print(f"== {q} ==")
            for g in gh:
                print(f"NOT COVERED / partial coverage: {g['note']}")
            if not ranked:
                print("NOT COVERED: no topic in the collection matches this term.")
                code = max(code, 1)
            for s, t in ranked:
                print(f"- {t['src']} {fmt_pages(t['pages'])} [{t['id']}] {t['title']} -> references/{t['ref']}")
                print(f"    {t['summary']}")
    if args_json(a):
        print(json.dumps(out, ensure_ascii=False, indent=1))
    return code


def args_json(a):
    return a.json


if __name__ == "__main__":
    sys.exit(main())
