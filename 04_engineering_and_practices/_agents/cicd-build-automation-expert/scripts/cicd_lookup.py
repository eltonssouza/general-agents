# -*- coding: utf-8 -*-
"""
cicd_lookup.py - topic -> source and (PDF) pages lookup in the collection of the cicd-build-automation-expert package.

Usage:
  python -I scripts/cicd_lookup.py "gradle wrapper"
  python -I scripts/cicd_lookup.py --topic "presubmit"
  python -I scripts/cicd_lookup.py --list

Convention: pages = PDF PAGE (GRADLE: printed = PDF - 8; SWE-G: 408-page PDF with no printed page number).
If the subject is not in the sources, it answers "NOT COVERED" (exit 1) and explains; this means the answer
must be labeled [extrapolation] or refused as an attribution to the book.
Read-only, no network. Source: scripts/cicd_index.json.
The index keeps Portuguese keywords (user input) alongside English ones.
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

INDEX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cicd_index.json")


def load_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def has_word(text, kw):
    kw = norm(kw)
    if not kw:
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(kw) + r"(?![a-z0-9])", text) is not None


def search(query, data):
    q = norm(query)
    scored = []
    for t in data["topics"]:
        score = 0
        if has_word(q, t["id"].replace("-", " ")):
            score += 3
        for kw in t["keywords"]:
            if has_word(q, kw):
                score += 2 if len(kw) > 3 else 1
        # short query contained in the title/id
        if len(q) >= 4 and (q in norm(t["title"])):
            score += 2
        if score:
            scored.append((score, t))
    scored.sort(key=lambda x: (-x[0], x[1]["id"]))
    gaps = [g for g in data["not_in_book"] if any(has_word(q, term) for term in g["terms"])]
    return [t for _, t in scored], gaps


def fmt_refs(refs):
    return "; ".join("%s p.%s" % (s, p) for s, p in refs)


def main():
    ap = argparse.ArgumentParser(description="Topic -> source/pages (PDF) lookup in the CI/CD collection")
    ap.add_argument("query", nargs="*", help="term to search")
    ap.add_argument("--topic", help="term to search (alternative to the positional argument)")
    ap.add_argument("--list", action="store_true", help="list all indexed topics")
    a = ap.parse_args()
    data = load_index()

    if a.list:
        print("Convention: PDF pages.")
        print("Sources:")
        for k, v in data["sources"].items():
            print("  %-6s %s (%s p.; %s)" % (k, v["title"], v["pages"], v["kind"]))
        print("Indexed topics: %d" % len(data["topics"]))
        for t in data["topics"]:
            print("- %s: %s | %s | ref: %s" % (t["id"], t["title"], fmt_refs(t["refs"]), t["file"]))
        print("Outside the collection (NOT COVERED): %d term groups; run a query to see them." % len(data["not_in_book"]))
        return 0

    query = a.topic or " ".join(a.query)
    if not query.strip():
        ap.print_help()
        return 2

    topics, gaps = search(query, data)
    rc = 0
    if gaps:
        rc = 1
        print("NOT COVERED: '%s'" % query)
        for g in gaps:
            print("  - %s" % g["note"])
        print("  Label the answer [extrapolation] or say the sources do not cover the subject.")
        if topics:
            print("Related topics (they do NOT cover the term above):")
    elif not topics:
        print("NOT COVERED: '%s' (no topic in the collection matches)." % query)
        print("  Label it [extrapolation] or say the sources do not cover the subject. Use --list to see the topics.")
        return 1
    else:
        print("Found %d topic(s) for '%s' (PDF pages):" % (len(topics), query))
    for t in topics[:6]:
        print("ID: %s" % t["id"])
        print("  Title: %s" % t["title"])
        print("  Sources and pages: %s" % fmt_refs(t["refs"]))
        print("  Reference: references/%s" % t["file"])
    return rc


if __name__ == "__main__":
    sys.exit(main())
