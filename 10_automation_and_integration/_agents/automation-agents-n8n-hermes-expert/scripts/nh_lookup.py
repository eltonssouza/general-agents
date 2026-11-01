# -*- coding: utf-8 -*-
"""
nh_lookup.py - deterministic topic lookup over the two landing pages (N8N, HERMES).

Usage (from the package root; always with python -I):
  python -I scripts/nh_lookup.py TERMO [TERMO ...] [--fonte N8N|HERMES] [--json]
  python -I scripts/nh_lookup.py --list [--fonte F]       # all covered topics
  python -I scripts/nh_lookup.py --gaps [--fonte F]       # known gaps (NOT COVERED)
  python -I scripts/nh_lookup.py --page FONTE N           # what page N of the source contains
  python -I scripts/nh_lookup.py --fontes                 # what each PDF is

Page convention: N = PDF page (the "=== PAGE N ===" marker of the extracted text).
Rules: only reports what is in nh_index.json (built from the 8 pages).
If nothing matches, prints "NOT COVERED". If the term matches a known gap, prints
"NOT COVERED" with the note, even if merely related topics exist.
Read-only, no network, executes nothing. Exit: 0 = covered; 1 = NOT COVERED.
Search terms may be in Portuguese or English (the index keeps both sets of keywords).
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
INDEX = os.path.join(HERE, "nh_index.json")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with open(INDEX, "r", encoding="utf-8") as f:
        return json.load(f)


def kw_in(kw, q):
    kw = norm(kw)
    return re.search(r"(?<![a-z0-9_])" + re.escape(kw) + r"(?![a-z0-9_])", q) is not None


def search(idx, terms, fonte=None):
    q = norm(" ".join(terms))
    hits = []
    for t in idx["topicos"]:
        if fonte and t["fonte"] != fonte:
            continue
        matched = [k for k in t["palavras"] if kw_in(k, q)]
        # whole term equal to a keyword (e.g. short-phrase search)
        if matched:
            score = sum(len(norm(k)) for k in matched)
            hits.append((score, t, matched))
    hits.sort(key=lambda x: (-x[0], x[1]["id"]))
    gaps = []
    for g in idx["lacunas"]:
        if fonte and g["fonte"] not in (fonte, "AMBAS"):
            continue
        matched = [k for k in g["palavras"] if kw_in(k, q)]
        if matched:
            gaps.append((g, matched))
    return hits, gaps


def cite(t):
    ps = t["paginas"]
    return f"{t['fonte']} p.{ps[0]}" + (f"-{ps[-1]}" if len(ps) > 1 and ps == list(range(ps[0], ps[-1] + 1)) else
                                          ("," + ",".join(map(str, ps[1:])) if len(ps) > 1 else ""))


def show_topic(t, matched=None, rel=False):
    tag = "[from source]"
    print(f"- {t['id']} {tag} ({cite(t)}) depth={t['profundidade']}: {t['titulo']}")
    print(f"    {t['resumo']}")
    if matched:
        print(f"    (matched: {', '.join(matched)})")


def main():
    ap = argparse.ArgumentParser(description="Search the n8n/Hermes landing pages.")
    ap.add_argument("termos", nargs="*")
    ap.add_argument("--fonte", choices=["N8N", "HERMES"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--fontes", action="store_true")
    ap.add_argument("--page", nargs=2, metavar=("FONTE", "N"))
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    idx = load()

    if a.fontes:
        for k, v in idx["fontes"].items():
            print(f"{k}: {v['arquivo']} ({v['paginas']} pages) - {v['descricao']} Usefulness: {v['util']}")
        return 0
    if a.list:
        for t in idx["topicos"]:
            if a.fonte and t["fonte"] != a.fonte:
                continue
            print(f"{t['id']}\t{cite(t)}\t{t['profundidade']}\t{t['titulo']}")
        return 0
    if a.gaps:
        for g in idx["lacunas"]:
            if a.fonte and g["fonte"] not in (a.fonte, "AMBAS"):
                continue
            print(f"NOT COVERED [{g['fonte']}]: {', '.join(g['palavras'])}\n    {g['nota']}")
        return 0
    if a.page:
        fonte, n = a.page[0].upper(), int(a.page[1])
        ts = [t for t in idx["topicos"] if t["fonte"] == fonte and n in t["paginas"]]
        if fonte not in idx["fontes"] or not 1 <= n <= idx["fontes"][fonte]["paginas"]:
            print(f"NOT COVERED: {fonte} p.{n} does not exist (each source has 4 pages).")
            return 1
        print(f"{fonte} p.{n}: {len(ts)} topic(s)")
        for t in ts:
            show_topic(t)
        return 0
    if not a.termos:
        ap.error("provide a TERM, or --list/--gaps/--page/--fontes")

    hits, gaps = search(idx, a.termos, a.fonte)
    if a.json:
        out = {
            "consulta": " ".join(a.termos),
            "sem_cobertura": bool(gaps) or not hits,
            "lacunas": [{"fonte": g["fonte"], "nota": g["nota"], "casou": m} for g, m in gaps],
            "topicos": [{"id": t["id"], "fonte": t["fonte"], "paginas": t["paginas"], "profundidade": t["profundidade"],
                         "titulo": t["titulo"], "resumo": t["resumo"], "casou": m} for _, t, m in hits[: a.top]],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1 if out["sem_cobertura"] and not hits else 0

    if gaps:
        for g, m in gaps:
            print(f"NOT COVERED [{g['fonte']}] (term: {', '.join(m)}): {g['nota']}")
    if not hits:
        if not gaps:
            print(f"NOT COVERED: no topic of the two landing pages matches '{' '.join(a.termos)}'. "
                  "Answer 'NOT COVERED'; only a labeled [extrapolation] if the user asks.")
        return 1
    print(("Related topics (they do NOT answer the uncovered part above):" if gaps else "Coverage found:"))
    for _, t, m in hits[: a.top]:
        show_topic(t, m)
    if len(hits) > a.top:
        print(f"... {len(hits) - a.top} more topic(s); use --top N")
    if any(t["profundidade"] == "title-only" for _, t, _ in hits[: a.top]):
        print("Warning: depth=title-only means the source only gives the link/section name, without the content.")
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main())
