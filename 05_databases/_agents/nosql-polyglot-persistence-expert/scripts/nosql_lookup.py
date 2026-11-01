# -*- coding: utf-8 -*-
"""
nosql_lookup.py - topic lookup in the package index (nosql_index.json).

Usage:
  python -I nosql_lookup.py "quorum"            # search by term (also: --topic "quorum")
  python -I nosql_lookup.py --list              # list all indexed topics
  python -I nosql_lookup.py "pacelc"            # term known to be absent from the sources

Output: id, title, sources and pages (p.N = PDF page; see references/INDEX.md) and the reference
file. If nothing is found it prints "NOT COVERED" (exit 1). Terms listed in `not_in_book`
print "NOT IN THE SOURCE" with the explanation. The index is the origin of the pages; nothing is invented here.
Search keywords are bilingual: the Portuguese input keywords are kept and English ones were added.
Read-only, no network.
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

INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nosql_index.json")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_refs(refs):
    return "; ".join("%s p.%s" % (r["src"], r["pages"]) for r in refs)


def search(data, query):
    q = norm(query)
    qwords = [w for w in re.split(r"[^a-z0-9+/._|-]+", q) if len(w) >= 3]
    results = []
    for t in data["topics"]:
        score = 0
        hay_id = norm(t["id"])
        hay_title = norm(t["title"])
        if q and q in hay_id:
            score += 5
        if q and q in hay_title:
            score += 4
        for kw in t.get("keywords", []):
            k = norm(kw)
            if q == k:
                score += 6
            elif q and (q in k or k in q):
                score += 3
            else:
                for w in qwords:
                    if w == k or (len(w) >= 4 and (w in k or k in w)):
                        score += 1
        for w in qwords:
            if len(w) >= 4 and (w in hay_title):
                score += 1
            if len(w) >= 4 and (w in hay_id):
                score += 2
        if score:
            results.append((score, t))
    results.sort(key=lambda x: (-x[0], x[1]["id"]))
    return results


def absent_notes(data, query):
    q = norm(query)
    out = []
    for item in data.get("not_in_book", []):
        for term in item["terms"]:
            tn = norm(term)
            if re.search(r"(?<![a-z0-9])" + re.escape(tn) + r"(?![a-z0-9])", q):
                out.append((term, item["msg"]))
                break
    return out


def main():
    ap = argparse.ArgumentParser(description="Topic lookup in the NoSQL collection (PDF page)")
    ap.add_argument("query", nargs="*", help="search term")
    ap.add_argument("--topic", help="search term (alternative to the positional argument)")
    ap.add_argument("--list", action="store_true", help="list all topics")
    a = ap.parse_args()

    data = load_index()
    if a.list:
        print("Indexed topics: %d (p.N = PDF page)" % len(data["topics"]))
        for t in data["topics"]:
            print("- %s: %s (%s)" % (t["id"], t["title"], fmt_refs(t["refs"])))
        return 0

    query = a.topic or " ".join(a.query)
    if not query.strip():
        ap.print_help()
        return 2

    scored = search(data, query)
    notes = absent_notes(data, query)
    if notes:
        for term, msg in notes:
            print("NOT IN THE SOURCE: '%s' - %s" % (term, msg))
        # known-absent term: only show topics with a strong match (avoids false positives from a loose word)
        scored = [(s, t) for s, t in scored if s >= 6]
    results = [t for _, t in scored]
    if not results:
        print("NOT COVERED: no topic in the collection matches '%s'." % query)
        return 1
    print("%d topic(s) for '%s' (p.N = PDF page):\n" % (len(results), query))
    for t in results[:8]:
        print("ID: %s" % t["id"])
        print("Title: %s" % t["title"])
        print("Sources: %s" % fmt_refs(t["refs"]))
        print("Reference: references/%s" % t["file"])
        print("-" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
