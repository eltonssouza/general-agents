# -*- coding: utf-8 -*-
"""
testing_lookup.py - deterministic lookup of the topics covered by the sources of the
software-testing-qa-expert agent (JUNIT, MOCK, TDM, JMETER, SWE-G ch. 11-14), with pages.

Reads testing_index.json (same directory). Read-only, no network.
Page convention: PDF (printed JMETER = N-7; see references/INDEX.md).
Queries may be written in English or Portuguese (the index keeps both keyword sets).

Usage:
  python -I testing_lookup.py "data masking"        search by keyword
  python -I testing_lookup.py --list                list the topics
  python -I testing_lookup.py --topic fakes         show one topic by key
  python -I testing_lookup.py "flaky" --book SWE-G  filter by source acronym
Output: rules WITH page and what the source does NOT say. No match: "NOT COVERED"
(exit 1); the agent must label the answer [extrapolation] or refuse the attribution.
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

BOOKS = ("JUNIT", "MOCK", "TDM", "JMETER", "SWE-G")


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def load():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "testing_index.json"), encoding="utf-8") as f:
        return json.load(f)


def show(key, t):
    print("TOPIC: %s [%s]" % (t["name"], key))
    print("CITATION: [from source] (%s)" % t["citation"])
    print("\nSUMMARY: %s" % t["summary"])
    print("\nRULES FROM THE SOURCES (with page):")
    for r in t["rules"]:
        print("  * [from source] %s" % r)
    if t.get("not_in_book"):
        print("\nNOT IN THE SOURCE (label [extrapolation] or refuse the attribution):")
        for n in t["not_in_book"]:
            print("  - %s" % n)


def score(q, key, t):
    qn = norm(q)
    s = 0
    if qn == norm(key):
        s += 100
    if qn in norm(t["name"]):
        s += 40
    for k in t.get("keywords", []):
        kn = norm(k)
        if qn == kn:
            s += 50
        elif qn in kn or kn in qn:
            s += 20
    for tok in qn.split():
        if len(tok) > 3 and any(tok in norm(k) for k in t.get("keywords", [])):
            s += 5
    blob = norm(" ".join(t["rules"]) + " " + t["summary"])
    if qn in blob:
        s += 10
    return s


def uncovered_note(q, uncovered):
    qn = norm(q)
    notes = []
    for u in uncovered:
        for k in u["keywords"]:
            kn = norm(k)
            if qn == kn or (len(qn) >= 4 and (qn in kn or kn in qn)) or kn in qn.split():
                notes.append(u["note"])
                break
    return notes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*", help="term(s); several words are joined")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--topic")
    ap.add_argument("--book", choices=BOOKS, help="filter by acronym (matched against the citation)")
    ap.add_argument("--max", type=int, default=3)
    a = ap.parse_args(argv)
    data = load()
    topics = data["topics"]
    if a.book:
        topics = {k: t for k, t in topics.items() if a.book in t["citation"]}
    if a.list:
        for k, t in topics.items():
            print("%-34s %s (%s)" % (k, t["name"], t["citation"]))
        return 0
    if a.topic:
        if a.topic not in data["topics"]:
            print("Unknown topic: %s. Use --list." % a.topic)
            return 2
        show(a.topic, data["topics"][a.topic])
        return 0
    query = " ".join(a.query).strip()
    if not query:
        ap.print_help()
        return 2
    ranked = sorted(((score(query, k, t), k) for k, t in topics.items()), reverse=True)
    hits = [(s, k) for s, k in ranked if s > 0][: a.max]
    notes = uncovered_note(query, data.get("uncovered", []))
    if not hits:
        print("NOT COVERED in the collection for: %s" % query)
        for n in notes:
            print("NOTE: %s" % n)
        print("The sources (JUNIT/MOCK/TDM/JMETER/SWE-G ch. 11-14) do not cover this topic; any answer must be an [extrapolation] or be referred to another agent.")
        return 1
    for i, (s, k) in enumerate(hits):
        if i:
            print("\n" + "-" * 60 + "\n")
        show(k, topics[k])
    for n in notes:
        print("\nCOVERAGE NOTE: %s" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
