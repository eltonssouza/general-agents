# -*- coding: utf-8 -*-
"""
go_lookup.py - deterministic topic lookup for go-expert (no network, read-only).

Given a free-text subject, shows the topics of the scripts/go_index.json index that match, with the sources and the PDF PAGES
(Little: printed page = N - 1), the label of each source ([from source] or [inference]) and the reference file to read more.
If the subject falls in a known gap, it prints NOT COVERED with the reason; if nothing matches, it also says NOT COVERED
(do not invent content or pages). The index is a curated list: it does not replace reading references/.
Queries may be written in English or Portuguese (the index keywords are bilingual).

Usage:
  python -I scripts/go_lookup.py "receiver ponteiro"
  python -I scripts/go_lookup.py --list
  python -I scripts/go_lookup.py --json "panic(nil)"
Exit code: 0 = topic found; 3 = NOT COVERED (nothing indexed); 2 = usage.
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
STOP = {"de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "um", "uma", "que", "com", "para", "por", "como",
        "qual", "quais", "esse", "essa", "isso", "isto", "ser", "uso", "usar", "the", "and", "for", "sobre", "sem", "mais",
        "are", "how", "what", "which", "with", "does", "this", "that", "about", "use", "using", "when", "from", "into"}
LABEL = {"from source": "[from source]", "inference": "[inference]"}
SIGLA_NOME = {"Eff": "Effective Go (2009)", "Spec": "Go Spec (go1.26)", "Little": "The Little Go Book (go1.3.3)",
              "RN1.20": "Release notes 1.20", "RN1.21": "Release notes 1.21", "RN1.22": "Release notes 1.22",
              "RN1.23": "Release notes 1.23", "RN1.24": "Release notes 1.24"}


def fold(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def tokens(q):
    return [t for t in re.findall(r"[a-z0-9_.()\-/~]+", fold(q)) if len(t) >= 3 and t not in STOP]


def score(topic, q, toks):
    s = 0
    kws = [fold(k) for k in topic["keywords"]] + [fold(topic["id"]), fold(topic["titulo"])]
    for kw in kws:
        if len(kw) >= 3 and kw in q:
            s += 3 if " " in kw or len(kw) >= 6 else 2
    for t in toks:
        for kw in kws:
            if t == kw:
                s += 2
                break
            if len(t) >= 4 and len(kw) >= 4 and (t in kw or kw in t):
                s += 1
                break
    return s


def pages(p):
    return ", ".join("p.%d" % n for n in p)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*")
    ap.add_argument("--index", default=os.path.join(HERE, "go_index.json"))
    ap.add_argument("--list", action="store_true", help="list the indexed topics")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=3)
    a = ap.parse_args()
    with open(a.index, encoding="utf-8") as f:
        idx = json.load(f)
    if a.list:
        for t in idx["topicos"]:
            print("- %-24s %s%s" % (t["id"], t["titulo"], "  [DATED]" if t.get("dated") else ""))
        print("\nKnown gaps (NOT COVERED):")
        for g in idx["sem_cobertura"]:
            print("- %s" % ", ".join(g["termos"]))
        return 0
    if not a.query:
        ap.print_usage(sys.stderr)
        return 2
    q = fold(" ".join(a.query))
    toks = tokens(q)
    gaps = [g for g in idx["sem_cobertura"] if any(re.search(r"(?<![a-z0-9])" + re.escape(fold(t)) + r"(?![a-z0-9])", q) for t in g["termos"])]
    ranked = sorted(((score(t, q, toks), t) for t in idx["topicos"]), key=lambda x: -x[0])
    hits = [(s, t) for s, t in ranked if s >= 2][: a.top]
    if a.json:
        json.dump({"query": " ".join(a.query), "topicos": [t for _, t in hits], "sem_cobertura": gaps}, sys.stdout,
                  ensure_ascii=False, indent=2)
        print()
        return 0 if hits else 3
    print("Page convention: PDF (Little: printed = N - 1). Curated index; confirm in references/.")
    for s, t in hits:
        print("\n## %s%s  (id=%s, score %d)" % (t["titulo"], "  [DATED]" if t.get("dated") else "", t["id"], s))
        for f in t["fontes"]:
            pg = pages(f["paginas"])
            print("- %s %s %s: %s" % (LABEL.get(f["label"], f["label"]), f["sigla"], pg, f["resumo"]))
        print("  read more: %s" % t["ref"])
    for g in gaps:
        print("\nNOT COVERED: %s" % g["mensagem"])
    if not hits and not gaps:
        print("\nNOT COVERED: no indexed topic matches \"%s\". Do not invent content or pages: search with Grep in "
              "references/ (INDEX.md) and, if nothing is there, say the sources do not cover it." % " ".join(a.query))
    return 0 if hits else 3


if __name__ == "__main__":
    sys.exit(main())
