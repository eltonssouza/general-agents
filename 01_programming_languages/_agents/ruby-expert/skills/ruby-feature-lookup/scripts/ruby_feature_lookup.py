#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ruby_feature_lookup.py - topic lookup in the index of the official Ruby 3.0 to 3.4 release notes (R30 to R34).

Read-only, no network. Usage:
  python -I ruby_feature_lookup.py yjit
  python -I ruby_feature_lookup.py "regexp timeout"
  python -I ruby_feature_lookup.py --list
  python -I ruby_feature_lookup.py gvl          # NOT COVERED (the notes do not contain it)

Each result carries the PDF page (package convention: PDF page) and the [from source] label.
If the topic is not in the index, it prints NOT COVERED and exits with code 1.
Search terms may be Portuguese or English (the index keeps keywords in both).
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


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def has_term(text, term):
    """Whole-word match (avoids 'dap' inside 'adaptive')."""
    return re.search(r"(?<![\w])" + re.escape(term) + r"(?![\w])", text) is not None


def fmt_cite(cite):
    parts = []
    for rel, pages in cite:
        pages = sorted(pages)
        ranges, start, prev = [], pages[0], pages[0]
        for p in pages[1:]:
            if p == prev + 1:
                prev = p
                continue
            ranges.append((start, prev))
            start = prev = p
        ranges.append((start, prev))
        txt = ", ".join(str(a) if a == b else "%d-%d" % (a, b) for a, b in ranges)
        parts.append("%s p.%s" % (rel, txt))
    return "; ".join(parts)


def load():
    with open(os.path.join(HERE, "ruby_feature_index.json"), encoding="utf-8") as f:
        return json.load(f)


def search(query, data):
    q = norm(query)
    for nc in data["not_covered"]:
        if any(has_term(q, norm(t)) for t in nc["terms"]):
            return None, nc["note"]
    hits = []
    for ft in data["features"]:
        score = 0
        if q == ft["id"] or q in [norm(k) for k in ft["keywords"]]:
            score = 3
        elif q in norm(ft["name"]) or any(q in norm(k) or (len(norm(k)) > 3 and norm(k) in q) for k in ft["keywords"]):
            score = 2
        elif q in norm(ft["summary"]):
            score = 1
        if score:
            hits.append((score, ft))
    hits.sort(key=lambda x: -x[0])
    return [h[1] for h in hits], None


def main():
    ap = argparse.ArgumentParser(description="Topic search in the official Ruby 3.0-3.4 notes.")
    ap.add_argument("query", nargs="*", help="term (e.g. yjit, ractor, regexp timeout, prism)")
    ap.add_argument("--list", "-l", action="store_true", help="list all topics")
    ap.add_argument("--json", action="store_true", help="JSON output")
    a = ap.parse_args()
    data = load()
    if a.list:
        for ft in data["features"]:
            print("%-22s %-48s %-24s [from source] (%s)" % (ft["id"], ft["name"], ft["version"], fmt_cite(ft["cite"])))
        return 0
    if not a.query:
        ap.print_help()
        return 2
    q = " ".join(a.query)
    hits, note = search(q, data)
    if note is not None or not hits:
        msg = note or "The R30-R34 notes index does not contain this topic."
        if a.json:
            print(json.dumps({"query": q, "coverage": "NOT COVERED", "note": msg}, ensure_ascii=False))
        else:
            print("NOT COVERED: '%s'. %s" % (q, msg))
            print("If you answer, label it [extrapolation] and ask for a check against the version documentation.")
        return 1
    if a.json:
        print(json.dumps([dict({k: h[k] for k in ("id", "name", "version", "summary")}, cite=fmt_cite(h["cite"])) for h in hits], ensure_ascii=False, indent=1))
        return 0
    print("Results for '%s' (pages = PDF pages):\n" % q)
    for h in hits:
        print("--- %s [%s] ---" % (h["name"], h["version"]))
        print("[from source] (%s): %s\n" % (fmt_cite(h["cite"]), h["summary"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
