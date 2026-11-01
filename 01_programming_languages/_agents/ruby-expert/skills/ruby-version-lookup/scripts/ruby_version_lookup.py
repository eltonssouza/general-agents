#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ruby_version_lookup.py - what each release note (Ruby 3.0 to 3.4) brings, with the PDF page.

Read-only, no network. Usage:
  python -I ruby_version_lookup.py --version 3.2
  python -I ruby_version_lookup.py --query yjit
  python -I ruby_version_lookup.py --all
  python -I ruby_version_lookup.py --version 4.0     # NOT COVERED (exit 1)

Page convention: PDF page of the respective note. All items are [from source].
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

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


# Portuguese input aliases (the highlights are in English; Portuguese queries keep working)
ALIASES = {"memoria": "memory", "tipos": "type", "depreciado": "deprecated", "depreciacao": "deprecat", "removido": "removed",
           "removidos": "removed", "aviso": "warning", "ator": "actor", "atores": "actor", "congelado": "frozen",
           "mutar": "mutating", "bibliotecas": "librar", "velocidade": "speed", "depurador": "debugger",
           "desempenho": "performance", "concorrencia": "concurrency", "paralelismo": "parallelism"}


def fmt_cite(cite):
    out = []
    for rel, pages in cite:
        pages = sorted(pages)
        runs, a, b = [], pages[0], pages[0]
        for p in pages[1:]:
            if p == b + 1:
                b = p
            else:
                runs.append((a, b))
                a = b = p
        runs.append((a, b))
        out.append("%s p.%s" % (rel, ", ".join(str(x) if x == y else "%d-%d" % (x, y) for x, y in runs)))
    return "; ".join(out)


def load():
    with open(os.path.join(HERE, "ruby_version_data.json"), encoding="utf-8") as f:
        return json.load(f)


def show_version(v):
    print("=== %s (%s) | %s, %d pages ===" % (v["name"], v["release_date"], v["sigla"], v["pages"]))
    for h in v["highlights"]:
        print("- [from source] (%s) %s" % (fmt_cite(h["cite"]), h["text"]))


def main():
    ap = argparse.ArgumentParser(description="Ruby 3.0-3.4 timeline from the official notes.")
    ap.add_argument("--version", "-v", help="3.0, 3.1, 3.2, 3.3 or 3.4")
    ap.add_argument("--query", "-q", help="term (e.g. yjit, prism, regexp)")
    ap.add_argument("--all", "-a", action="store_true", help="list the versions")
    a = ap.parse_args()
    data = load()
    if a.version:
        v = a.version.lower().replace("ruby", "").strip()
        found = [x for x in data["versions"] if x["version"] == v or x["name"].lower() in ("ruby " + v, "ruby " + v + ".0")]
        if not found:
            print("NOT COVERED: version '%s' is not in the notes (covered: 3.0 to 3.4). [DATED] if later than 3.4." % a.version)
            return 1
        for x in found:
            show_version(x)
        return 0
    if a.query:
        q = norm(a.query)
        q = ALIASES.get(q, q)
        n = 0
        for v in data["versions"]:
            hits = [h for h in v["highlights"] if q in norm(h["text"]) or any(q in norm(t) for t in h["terms"])]
            if hits:
                print("--- %s (%s) ---" % (v["name"], v["release_date"]))
                for h in hits:
                    print("- [from source] (%s) %s" % (fmt_cite(h["cite"]), h["text"]))
                n += len(hits)
        if not n:
            print("NOT COVERED: '%s' does not appear in the R30-R34 note highlights." % a.query)
            print("Outside the notes: " + "; ".join(data["not_in_notes"]))
            return 1
        return 0
    if a.all:
        for v in data["versions"]:
            print("%s: %s | %s | %d pages | %d highlights" % (v["name"], v["release_date"], v["sigla"], v["pages"], len(v["highlights"])))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
