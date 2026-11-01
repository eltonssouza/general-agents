#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cs_concept_lookup.py - topic search in the section map of the C# Yellow Book (CSYB); read-only, no network.

Usage:
  python -I cs_concept_lookup.py "struct"        # sections whose title/keywords/summary match
  python -I cs_concept_lookup.py --list          # all sections and pages
  python -I cs_concept_lookup.py "boxing"        # NOT COVERED: the book does not cover it (with a note)

Pages = PDF pages (printed = PDF - 5). Index origin: reading the book's pages
(cs_concept_index.json). The index maps WHERE to look; the summary is a guide and does not replace reading.
Keywords may be given in English or Portuguese (the index keeps both).
Exit code 0 = covered; 1 = NOT COVERED (topic absent from the book or not mapped).
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
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def load_index():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cs_concept_index.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def search(query, data):
    q = norm(query).strip()
    hits = []
    for sec in data["sections"]:
        hay = [norm(sec["title"]), norm(sec["summary"]), sec["id"].lower()] + [norm(k) for k in sec.get("keywords", [])]
        if any(q in h for h in hay):
            hits.append(sec)
    return hits


def absent(query, data):
    q = norm(query).strip()
    out = []
    for item in data.get("not_in_book", []):
        parts = [norm(p) for p in item["term"].replace("/", " ").replace(";", " ").split()]
        if q and (q in norm(item["term"]) or q in parts):
            out.append(item)
    return out


def main():
    ap = argparse.ArgumentParser(description="Topic search in the C# Yellow Book (CSYB) map.")
    ap.add_argument("query", nargs="?", help="topic, keyword or section id (e.g. struct, threads, 4.9)")
    ap.add_argument("--list", "-l", action="store_true", help="list all mapped sections")
    args = ap.parse_args()
    data = load_index()
    src = data["source"]

    if args.list:
        print("=== %s (%d p.) | %s ===" % (src["title"], src["pdf_pages"], src["page_convention"]))
        for s in data["sections"]:
            print("%-8s %-45s [from source] (CSYB p.%s)" % (s["id"], s["title"], s["pages"]))
        return 0
    if not args.query:
        ap.print_help()
        return 1

    # a term marked as absent from the book takes priority (avoids matching "using" with "using System")
    gone = absent(args.query, data)
    hits = search(args.query, data)
    if gone:
        print("NOT COVERED in the book for: '%s'" % args.query)
        for g in gone:
            print("  - %s: %s" % (g["term"], g["note"]))
        print("Answer with [extrapolation] (general knowledge) or say the book does not cover it.")
        if not hits:
            return 1
        print("Related sections (they may cover a nearby subject, not the term itself):")
    elif not hits:
        print("NOT COVERED: no section of the C# Yellow Book matches '%s'." % args.query)
        print("If it is a version feature (record, nullable, async, LINQ), use cs_version_lookup.py (CSHist/CS12/CS13).")
        return 1
    else:
        print("Results for '%s' (PDF pages; printed = PDF - 5):" % args.query)
    for s in hits:
        print("--- Section %s: %s ---" % (s["id"], s["title"]))
        print("Location: [from source] (CSYB p.%s)" % s["pages"])
        print("Guide summary: %s" % s["summary"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
