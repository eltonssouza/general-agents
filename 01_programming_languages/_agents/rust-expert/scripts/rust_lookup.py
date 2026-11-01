# -*- coding: utf-8 -*-
"""
rust_lookup.py - topic lookup in the rust-expert package index (scripts/rust_index.json).

Usage:
  python -I scripts/rust_lookup.py "lifetimes"          # search by term/alias (Portuguese or English)
  python -I scripts/rust_lookup.py --topic ownership    # lookup by id
  python -I scripts/rust_lookup.py --list               # list the topics
  python -I scripts/rust_lookup.py "tokio" --json       # JSON output

Output: the references/ file and section where the topic lives, the PDF pages (Book/Ref/RBE), and a summary.
When the index does not cover the term, prints "NOT COVERED" and exits with code 1 (never invents pages).
For terms known to be out of scope or only partially covered (e.g., tokio, atomics), prints the note
about what the sources do provide. Pages are PDF pages (not the printed numbering). No network; read-only.
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
NOT_COVERED = "not covered"  # value of the "cobertura" field for terms the sources do not address


def fold(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


def score(query, alias):
    q, a = fold(query), fold(alias)
    if q == a:
        return 100 + len(a)
    if len(a) >= 3 and re.search(r"(?<![\w])" + re.escape(a) + r"(?![\w])", q):
        return 50 + len(a)
    if len(q) >= 3 and re.search(r"(?<![\w])" + re.escape(q) + r"(?![\w])", a):
        return 30 + len(q)
    return 0


def find(idx, query, top=3):
    hits = []
    for e in idx["entradas"]:
        s = max([score(query, a) for a in e["aliases"] + [e["id"], e["titulo"]]] or [0])
        if s:
            hits.append((s, "entrada", e))
    for l in idx["limites"]:
        s = max([score(query, a) for a in l["aliases"]] or [0])
        if s:
            hits.append((s + 1, "limite", l))
    hits.sort(key=lambda h: -h[0])
    return hits[:top]


def show_entry(e):
    print("## %s [%s] — coverage: %s" % (e["titulo"], e["id"], e["cobertura"]))
    print("   Summary: %s" % e["resumo"])
    for o in e["onde"]:
        print("   Where: %s, section \"%s\"" % (o["arquivo"], o["secao"]))
    print("   Pages (PDF): %s" % "; ".join(e["paginas"]))
    if e.get("nota"):
        print("   Note: %s" % e["nota"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*")
    ap.add_argument("--topic")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--index", default=os.path.join(HERE, "rust_index.json"))
    a = ap.parse_args()
    with open(a.index, encoding="utf-8") as f:
        idx = json.load(f)
    if a.list:
        for e in idx["entradas"]:
            print("%-22s %s" % (e["id"], e["titulo"]))
        print("\n(out of scope/partial: %s)" % ", ".join(l["id"] for l in idx["limites"]))
        return 0
    if a.topic:
        for e in idx["entradas"]:
            if e["id"] == a.topic:
                if a.json:
                    json.dump(e, sys.stdout, ensure_ascii=False, indent=1)
                    print()
                else:
                    show_entry(e)
                return 0
        print("NOT COVERED: topic '%s' does not exist in the index (use --list)." % a.topic)
        return 1
    q = " ".join(a.query).strip()
    if not q:
        ap.error("provide a term, --topic ID, or --list")
    hits = find(idx, q)
    if a.json:
        json.dump([dict(tipo=t, **{k: v for k, v in d.items() if k != "termos"}) for _, t, d in hits], sys.stdout,
                  ensure_ascii=False, indent=1)
        print()
        return 0 if hits and not all(t == "limite" and d["cobertura"] == NOT_COVERED for _, t, d in hits[:1]) else 1
    if not hits:
        print("NOT COVERED: no index topic matches '%s'." % q)
        print("The index covers %d topics; the sources are Book/Ref/RBE (see references/INDEX.md). "
              "Answer as an [extrapolation] or say the sources do not address the subject." % len(idx["entradas"]))
        return 1
    best = hits[0]
    rc = 0
    for _, tipo, d in hits:
        if tipo == "entrada":
            show_entry(d)
        else:
            print("## %s — coverage: %s" % (d["id"], d["cobertura"].upper()))
            print("   %s" % d["nota"])
            if d["cobertura"] == NOT_COVERED:
                print("NOT COVERED in the sources for '%s'." % q)
    if best[1] == "limite" and best[2]["cobertura"] == NOT_COVERED:
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
