# -*- coding: utf-8 -*-
"""
erickson_lookup.py - deterministic lookup of topics and pages of "Algorithms" (Jeff Erickson, 2019).

Index source: erickson_index.json (hand-curated from reading the pages; see tests/verify_citations.py).
Pages = PDF (printed page = PDF - 18). No network; read-only.

Usage:
  python -I erickson_lookup.py "dijkstra"                  # search by topic/word (English or Portuguese, accents ignored)
  python -I erickson_lookup.py "subset sum" --chapter 3    # filter by chapter (number)
  python -I erickson_lookup.py --list                      # list curated topics + what the book does NOT cover
  python -I erickson_lookup.py --page 130                  # what the index knows about PDF page 130
  python -I erickson_lookup.py --printed 112               # convert a printed page to PDF
Output "NOT COVERED" (exit code 1) when the book does not treat the topic.
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

OFFSET = 18
HERE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with open(os.path.join(HERE, "erickson_index.json"), encoding="utf-8") as f:
        return json.load(f)


def pg(p):
    return "JE p.%d" % p[0] if p[0] == p[1] else "JE p.%d-%d" % (p[0], p[1])


def match_tema(q, e):
    hay = [norm(e["titulo"]), norm(e["titulo_en"]), norm(e["id"])] + [norm(w) for w in e["palavras"]]
    if any(q in h for h in hay):
        return True
    toks = [t for t in q.split() if len(t) > 2]
    return bool(toks) and all(any(t in h for h in hay) for t in toks)


def main():
    ap = argparse.ArgumentParser(description="Lookup of topics and pages of Erickson's book (page = PDF).")
    ap.add_argument("query", nargs="?")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--page", type=int, help="PDF page")
    ap.add_argument("--printed", type=int, help="printed page -> PDF")
    a = ap.parse_args()
    data = load()

    if a.printed is not None:
        print("printed page %d = PDF %d (JE p.%d)" % (a.printed, a.printed + OFFSET, a.printed + OFFSET))
        return 0
    if a.list:
        print("Convention: pages = PDF; printed = PDF - %d" % OFFSET)
        print("\nChapters:")
        for c in data["capitulos"]:
            print("  Ch. %-2d %-34s PDF p.%d-%d (printed %d)  -> references/%s" %
                  (c["capitulo"], c["titulo"], c["pagina_pdf"], c["fim_pdf"], c["pagina_impressa"], c["referencia"]))
        print("\nCurated topics (%d):" % len(data["temas"]))
        for e in data["temas"]:
            print("  [%s] Ch.%d %s (%s) - %s" % (e["id"], e["capitulo"], e["titulo_en"], e["tipo"], pg(e["paginas"])))
        print("\nThe book does NOT cover (NOT COVERED):")
        for n in data["nao_coberto"]:
            print("  - %s: %s" % (", ".join(n["palavras"][:3]), n["nota"]))
        return 0
    if a.page is not None:
        found = False
        for c in data["capitulos"]:
            if c["pagina_pdf"] <= a.page <= c["fim_pdf"]:
                print("PDF p.%d (printed %d): Ch. %d %s -> references/%s" %
                      (a.page, a.page - OFFSET, c["capitulo"], c["titulo"], c["referencia"]))
                found = True
        for e in data["temas"]:
            if e["paginas"][0] <= a.page <= e["paginas"][1]:
                print("  topic: %s (%s)" % (e["titulo_en"], pg(e["paginas"])))
        for s in data["secoes"]:
            if s["pagina_pdf"] == a.page:
                print("  section %s %s starts here" % (s["numero"], s["titulo"]))
        if not found:
            print("NOT COVERED: page outside the indexed chapters (preface/table of contents/indexes, or nonexistent).")
            return 1
        return 0
    if not a.query:
        ap.print_help()
        return 2

    q = norm(a.query)
    # 1) topics outside the book
    nc = [n for n in data["nao_coberto"] if any(q in norm(w) or norm(w) in q for w in n["palavras"])]
    temas = [e for e in data["temas"] if match_tema(q, e) and (a.chapter is None or e["capitulo"] == a.chapter)]
    secoes = [s for s in data["secoes"] if q in norm(s["titulo"]) and (a.chapter is None or s["capitulo"] == a.chapter)]
    print("=== SEARCH: '%s' (pages = PDF; printed = PDF - %d) ===" % (a.query, OFFSET))
    for n in nc:
        print("NOT COVERED in the book: %s" % n["nota"])
    for e in temas:
        print("- Ch.%d %s [%s] -> (%s)  [from source, per reading of the page]" %
              (e["capitulo"], e["titulo_en"], e["tipo"], pg(e["paginas"])))
        if e.get("nota"):
            print("    note: %s" % e["nota"])
    for s in secoes:
        print("- section %s %s -> (JE p.%d) (printed %d)" % (s["numero"], s["titulo"], s["pagina_pdf"], s["pagina_impressa"]))
    if not temas and not secoes:
        if not nc:
            print("NOT COVERED: no indexed topic matches the query. It may be in the book without being in the index;"
                  " check references/INDEX.md and the PDF before stating that the book does not treat the subject.")
        return 1
    return 1 if nc and not temas else 0


if __name__ == "__main__":
    sys.exit(main())
