# -*- coding: utf-8 -*-
"""
ods_cost_lookup.py - deterministic lookup of data-structure costs in the book
"Open Data Structures" (Pat Morin, Edition 0.1Gbeta, 326 pages). Pages = PDF (printed = N - 12).

Usage:
  python -I scripts/ods_cost_lookup.py "treap"
  python -I scripts/ods_cost_lookup.py "arraystack" --op add
  python -I scripts/ods_cost_lookup.py --kind worst            # filter by guarantee type
  python -I scripts/ods_cost_lookup.py "tombstone"             # term not in the book -> NOT COVERED
  python -I scripts/ods_cost_lookup.py --list

Data origin: Tables 1.1 and 1.2 (ODS p.36 and p.38) and the theorem/lemma statements of each chapter, with the page
(scripts/ods_costs.json). Nothing here comes from the model's memory: each row was checked against the cited page.
Queries may be in English or Portuguese (aliases such as "pilha em array", "espaco", "altura" are still recognized).
Exit 0 if found, 1 if NOT COVERED. No network; read-only.
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
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def load(path=None):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(path or os.path.join(here, "ods_costs.json"), encoding="utf-8") as f:
        return json.load(f)


# Portuguese --op words still accepted (the data file now uses English operation names)
OP_ALIASES = {"espaco": "space", "altura": "height", "tamanho": "size"}


def fmt_pages(pages):
    return "; ".join("ODS p.%d" % p for p in pages)


def search(data, query, op=None, kind=None):
    q = norm(query) if query else ""
    out = []
    for e in data["entries"]:
        hay = [norm(e["structure"])] + [norm(k) for k in e.get("keys", [])]
        if q and not any(q in h or h in q for h in hay):
            continue
        if op and OP_ALIASES.get(norm(op), norm(op)) not in norm(e["op"]):
            continue
        if kind and e["kind"] != kind:
            continue
        out.append(e)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cost lookup in the book Open Data Structures (Morin)")
    ap.add_argument("query", nargs="*", help="structure, operation or term (e.g. treap, 'linear probing', radix)")
    ap.add_argument("--op", help="filter by operation (e.g. add, find, space)")
    ap.add_argument("--kind", choices=["worst", "amortized", "expected", "amortized+expected", "bound"])
    ap.add_argument("--list", action="store_true", help="list all covered structures")
    ap.add_argument("--json", default=None, help="alternative path to ods_costs.json")
    a = ap.parse_args(argv)
    data = load(a.json)

    if a.list:
        print("Covered structures/algorithms (%d entries):" % len(data["entries"]))
        seen = []
        for e in data["entries"]:
            if e["structure"] not in seen:
                seen.append(e["structure"])
        print(", ".join(seen))
        print("Terms the book does NOT use: " + ", ".join(sorted(data["not_in_book"])))
        return 0

    query = " ".join(a.query).strip()
    if query:
        nq = norm(query)
        for term, why in data["not_in_book"].items():
            if norm(term) == nq or norm(term) in nq.split(" and "):
                print("NOT COVERED: '%s'. %s" % (query, why))
                print("Label it [extrapolation] or say the book does not cover it.")
                return 1
    res = search(data, query, a.op, a.kind)
    if not res:
        print("NOT COVERED: no entry for '%s'%s. The book may not cover it; label it [extrapolation]."
              % (query, " (op=%s)" % a.op if a.op else ""))
        return 1
    print("=== %s (pages = PDF; printed = N - 12) ===" % (query or "all entries"))
    for e in res:
        print("- %s | %s: %s [%s] -> %s | source: %s"
              % (e["structure"], e["op"], e["bound"], data["kinds"][e["kind"]], fmt_pages(e["pages"]), e["src"]))
    print("Label: [from source] for what is listed above; any additional conclusion is [inference] or [extrapolation].")
    return 0


if __name__ == "__main__":
    sys.exit(main())
