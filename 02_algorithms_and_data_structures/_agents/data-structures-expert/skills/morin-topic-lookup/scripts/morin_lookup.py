# -*- coding: utf-8 -*-
"""
morin_lookup.py - deterministic topic/page lookup in "Open Data Structures" (Pat Morin, Edition 0.1Gbeta).
Pages = PDF (printed = N - 12).

The index (morin_index.json) has two parts: "toc" (sections of the PDF table of contents, with the PDF page checked) and
"topics" (curated topics, with terms in English and Portuguese and the page where the book covers them, checked by reading).
Terms the book does not use (tombstone, primary clustering...) return NOT COVERED and exit code 1.
Queries may be in English or Portuguese.
Usage: python -I morin_lookup.py "treap" | "del" | "linear" --chapter "Hash Tables"
No network; read-only.
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


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def load():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "morin_index.json"), encoding="utf-8") as f:
        return json.load(f)


def ranges(pages):
    """[121, 122, 123, 130] -> 'ODS p.121-123; ODS p.130'."""
    out, i = [], 0
    pages = sorted(set(pages))
    while i < len(pages):
        j = i
        while j + 1 < len(pages) and pages[j + 1] == pages[j] + 1:
            j += 1
        out.append("ODS p.%d" % pages[i] if i == j else "ODS p.%d-%d" % (pages[i], pages[j]))
        i = j + 1
    return "; ".join(out)


def match(q, text):
    """Short queries (<= 3 letters, such as del or q) match only as a whole word."""
    if len(q) <= 3:
        return re.search(r"(?<![a-z0-9_])" + re.escape(q) + r"(?![a-z0-9_])", text) is not None
    return q in text


def search(idx, query, chapter=None):
    q = norm(query)
    res = []
    for it in idx["toc"]:
        if chapter and norm(chapter) not in norm(it["capitulo"]):
            continue
        if match(q, norm(it["topico"])) or match(q, norm(it["capitulo"])):
            res.append(("toc", it["level"], it["topico"], it["capitulo"], [it["pagina_pdf"]], ""))
    for it in idx["topics"]:
        if chapter and norm(chapter) not in norm(it["capitulo"]):
            continue
        hay = [norm(it["topico"])] + [norm(k) for k in it["termos"]]
        if any(match(q, h) for h in hay):
            res.append(("topic", 4, it["topico"], it["capitulo"], it["paginas"], it.get("nota", "")))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Topic and page lookup in the book Open Data Structures (Morin)")
    ap.add_argument("query", nargs="+", help="term (e.g. treap, rootish, del, 'potential method')")
    ap.add_argument("--chapter", help="filter by chapter (e.g. 'Hash Tables')")
    a = ap.parse_args(argv)
    idx = load()
    query = " ".join(a.query)
    nq = norm(query)
    for term, why in idx["not_in_book"].items():
        if norm(term) == nq:
            print("NOT COVERED: '%s'. %s" % (query, why))
            print("Label it [extrapolation] or say the book does not cover it.")
            return 1
    res = search(idx, query, a.chapter)
    print("=== SEARCH: '%s' (pages = PDF; printed = N - 12) ===" % query)
    if not res:
        print("NOT COVERED: no topic found. Label it [extrapolation] or say the book does not cover it.")
        return 1
    for kind, level, topic, chapter, pages, note in res:
        ind = "  " * (level - 1)
        pg = ranges(pages)
        print("%s- [%s] %s (Chapter: %s) -> %s%s" % (ind, kind, topic, chapter, pg, (" | " + note) if note else ""))
    print("Label: [from source] (page above). Extra conclusions: [inference] or [extrapolation].")
    return 0


if __name__ == "__main__":
    sys.exit(main())
