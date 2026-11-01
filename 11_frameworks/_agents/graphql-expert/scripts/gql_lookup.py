#!/usr/bin/env python3
"""gql_lookup.py - deterministic search in the GQL capture index (graphql.org/learn, 6 pages).

Usage (python -I, stdlib, no network):
  gql_lookup.py TERM...             search by topic (entries + NOT COVERED gaps)
  gql_lookup.py --page N            show the entries that touch page N (1-6)
  gql_lookup.py --list              list all entries (id, section, pages)
  gql_lookup.py --gaps              list what the source does NOT cover
  gql_lookup.py --json ...          JSON output
Page = PDF page. The index is a paraphrase; it is not the source text.
Queries are matched against Portuguese and English keywords.
"""
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "gql_index.json")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", s).strip()


def has_term(query_n, term):
    t = norm(term)
    if not t:
        return False
    return re.search(r"(?<![a-z0-9@])" + re.escape(t) + r"(?![a-z0-9])", query_n) is not None


def load():
    with open(INDEX, encoding="utf-8") as f:
        return json.load(f)


def search(data, query):
    q = norm(query)
    hits = []
    for e in data["entries"]:
        matched = [t for t in e["terms"] if has_term(q, t)]
        # bonus if the title appears
        score = len(matched) + (2 if has_term(q, norm(e["title"].split(":")[-1])) else 0)
        if matched:
            hits.append((score, e, matched))
    hits.sort(key=lambda x: (-x[0], x[1]["pages"][0], x[1]["id"]))
    gaps = []
    for g in data["gaps"]:
        matched = [t for t in g["terms"] if has_term(q, t)]
        if matched:
            gaps.append((g, matched))
    return hits, gaps


def fmt_pages(p):
    return "p." + (str(p[0]) if len(p) == 1 else f"{p[0]}-{p[-1]}")


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    data = load()
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--list":
        for e in data["entries"]:
            print(f"{e['id']:11} {fmt_pages(e['pages']):8} [{e['section']}] {e['title']}")
        return 0
    if args[0] == "--gaps":
        if as_json:
            print(json.dumps(data["gaps"], ensure_ascii=False, indent=2))
        else:
            print("NOT COVERED in the GQL source (lesson index capture):")
            for g in data["gaps"]:
                print(" -", g["topic"])
        return 0
    if args[0] == "--page":
        try:
            n = int(args[1])
        except (IndexError, ValueError):
            print("usage: --page N (1-6)")
            return 2
        if not 1 <= n <= 6:
            print("NOT COVERED: the PDF has 6 pages.")
            return 1
        es = [e for e in data["entries"] if n in e["pages"] and e["id"] != "meta"]
        if as_json:
            print(json.dumps(es, ensure_ascii=False, indent=2))
        else:
            for e in es:
                print(f"[{e['id']}] {e['title']} ({fmt_pages(e['pages'])})\n  {e['summary']}\n")
        return 0
    query = " ".join(args)
    hits, gaps = search(data, query)
    if as_json:
        print(json.dumps({
            "query": query,
            "entries": [{"id": e["id"], "title": e["title"], "pages": e["pages"], "summary": e["summary"],
                         "matched": m} for _, e, m in hits[:5]],
            "gaps": [{"topic": g["topic"], "matched": m} for g, m in gaps],
            "not_covered": (not hits) or bool(gaps),
        }, ensure_ascii=False, indent=2))
        return 0
    for g, m in gaps:
        print(f"NOT COVERED (detail): {g['topic']}  [terms: {', '.join(m)}]")
    if not hits and not gaps:
        print("NOT COVERED: no index topic matches the query. The source only brings titles and descriptions of graphql.org/learn lessons.")
        return 1
    for _, e, m in hits[:5]:
        print(f"\n[{e['id']}] {e['title']} (GQL {fmt_pages(e['pages'])}) [matched: {', '.join(m[:4])}]")
        print("  " + e["summary"])
    if gaps and hits:
        print("\nWarning: the source names the lesson/section above but does not bring the detailed content requested; any explanation is [extrapolation].")
    elif gaps:
        print("\nNo index lesson names this topic; any explanation is a labeled [extrapolation].")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
