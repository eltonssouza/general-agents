# -*- coding: utf-8 -*-
"""
cc_lookup.py - deterministic lookup of the topics of "Código Limpo" (Clean Code, Robert C. Martin,
Brazilian Portuguese edition) covered by the clean-code-expert agent, with PDF pages.

Reads cc_index.json (same directory). Read-only, no network.
Convention: (CL p.N) = page of the scanned PDF (the printed page is not used; see references/INDEX.md).
Search keywords work in Portuguese and in English.

Usage:
  python -I cc_lookup.py "parâmetros lógicos"     keyword search (Portuguese or English: "flag arguments")
  python -I cc_lookup.py --list                   list the topics
  python -I cc_lookup.py --list --chapter 3       list the topics of one chapter
  python -I cc_lookup.py --topic funcoes-pequenas show one topic by its key
Output: rules WITH page and what the book does NOT say. No match: "NOT COVERED"
(exit 1); the agent must label [extrapolation] or refuse to attribute it to the book. Usage error: exit 2.
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
    with open(os.path.join(here, "cc_index.json"), encoding="utf-8") as f:
        return json.load(f)


def show(key, t):
    print("TOPIC: %s [%s] (ch. %s)" % (t["name"], key, t.get("chapter", "?")))
    print("CITATION: [from source] (CL %s)" % t["citation"].replace("CL ", ""))
    print("\nSUMMARY: %s" % t["summary"])
    print("\nRULES FROM THE BOOK (with PDF page):")
    for r in t["rules"]:
        print("  * [from source] %s" % r)
    if t.get("not_in_book"):
        print("\nNOT IN THE SOURCE (label [extrapolation] or refuse to attribute it to the book):")
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
        elif len(qn) >= 3 and (qn in kn or kn in qn):
            s += 20
    for tok in qn.split():
        if len(tok) > 3 and any(tok in norm(k) for k in t.get("keywords", [])):
            s += 5
    if len(qn) >= 4 and qn in norm(" ".join(t["rules"]) + " " + t["summary"]):
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
    ap.add_argument("--chapter", help="filter by chapter (1-17, A, B, C)")
    ap.add_argument("--max", type=int, default=3)
    a = ap.parse_args(argv)
    data = load()
    topics = data["topics"]
    if a.chapter:
        topics = {k: t for k, t in topics.items() if str(t.get("chapter")) == a.chapter.upper()}
    if a.list:
        if not topics:
            print("No topics for chapter %s." % a.chapter)
            return 2
        for k, t in topics.items():
            print("%-40s ch.%-3s %s (CL %s)" % (k, t.get("chapter", "?"), t["name"], t["citation"].replace("CL ", "")))
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
        print("NOT COVERED in the book for: %s" % query)
        for n in notes:
            print("NOTE: %s" % n)
        print("Código Limpo does not address this topic; any answer must be [extrapolation] or referred to another agent.")
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
