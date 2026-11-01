# -*- coding: utf-8 -*-
"""
eng_lookup.py - deterministic topic lookup in the package's eng_index.json index.

Pages = PDF (see references/INDEX.md). Offline; read-only.
Usage:
  python -I scripts/eng_lookup.py "hyrum law"
  python -I scripts/eng_lookup.py "piramide de testes" --book SWE-G
  python -I scripts/eng_lookup.py --list
If nothing is found it prints NOT COVERED (exit code 1). Items the book does NOT contain
(not_in_book) print the corresponding note.
Queries may be in English or Portuguese: the index keeps Portuguese keywords as aliases.
Origin of the rules: the ranking is only a term count (technical extrapolation, not from a book).
"""
import argparse
import json
import os
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def load():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "eng_index.json"), encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description="Topic search in SWE-G, SWE-PREV, CC2 and 97TH (PDF pages).")
    ap.add_argument("query", nargs="?", help="search term (English or Portuguese)")
    ap.add_argument("--book", choices=["SWE-G", "SWE-PREV", "CC2", "97TH"])
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--list", action="store_true", help="list all entries")
    a = ap.parse_args()

    data = load()
    entries = data["entries"]
    if a.list:
        for e in entries:
            print("%-8s p.%-12s %s [%s]" % (e["book"], e["pages"], e["title"], e["ref"]))
        print("Declared items without coverage: %d" % len(data["not_in_book"]))
        return 0
    if not a.query:
        ap.error("provide a search term or --list")

    q = norm(a.query)
    tokens = q.split()

    notes = []
    for nb in data["not_in_book"]:
        if any(norm(t) in q for t in nb["terms"]):
            notes.append(nb["note"])

    scored = []
    for e in entries:
        if a.book and e["book"] != a.book:
            continue
        title = norm(e["title"])
        kws = [norm(k) for k in e["keywords"]]
        text = norm(" ".join([e["title"], e["chapter"], " ".join(e["keywords"]), e["summary"]]))
        score = 0
        for t in tokens:
            if t in text:
                score += 1
                if t in title or any(t in k for k in kws):
                    score += 2
        if any(norm(k) in q for k in e["keywords"] if len(k) > 3):
            score += 3
        if score:
            scored.append((score, e))
    scored.sort(key=lambda x: -x[0])

    for n in notes:
        print("NOT IN THE SOURCE: " + n)
    if not scored:
        print("NOT COVERED: the collection (SWE-G, SWE-PREV, CC2 Chapter 5 sample, 97TH Extended) does not cover '%s'." % a.query)
        return 1
    print("Results for '%s' (PDF pages):\n" % a.query)
    for s, e in scored[: a.limit]:
        print("[%s] %s - %s" % (e["book"], e["chapter"], e["title"]))
        print("    Citation: %s (%s p.%s)" % (e["label"], e["book"], e["pages"]))
        print("    Summary: %s" % e["summary"])
        print("    Detail: references/%s\n" % e["ref"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
