# -*- coding: utf-8 -*-
"""
mob_lookup.py - locates topics in the three sources of the mobile collection (read-only, stdlib, no network, deterministic).
  RN  = React-Native-Getting-Started (4 pages; docs v0.87, Aug 12, 2026)
  FLT = Flutter-Docs (4 pages; landing page, no version)
  SWT = Swift-A-Tour-of-Swift (19 pages; Swift version NOT stated; code in images)
Page convention: PDF page (the sources have no printed numbering). [DATED] to 2026.

Usage: python -I scripts/mob_lookup.py TERM [TERM...]
  --source RN|FLT|SWT   filter by source
  --page SIGLA N        topics on page N of the source
  --gaps                list NOT COVERED topics
  --sources             sources, versions and dates
  --json                JSON output
  --top N               maximum number of results (default 6)
A term without coverage prints "NOT COVERED" (it may come together with partial results).
Search terms are matched in Portuguese and in English.
"""
import argparse
import io
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


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "mob_index.json"), encoding="utf-8") as f:
        return json.load(f)


def words(s):
    return set(re.findall(r"[a-z0-9$?<>.:\\()!\[\]_-]+", norm(s)))


def fmt_pages(p):
    return ",".join(str(x) for x in p)


def gaps_for(idx, terms):
    q = " " + norm(" ".join(terms)) + " "
    hit = []
    for g in idx["sem_cobertura"]:
        for ph in g["termos"].split("|"):
            if (" " + ph + " ") in q or q.strip() == ph:
                hit.append(g)
                break
    return hit


def search(idx, terms, source, top):
    toks = [t for t in words(" ".join(terms)) if t]
    scored = []
    for t in idx["topicos"]:
        if source and t["fonte"] != source:
            continue
        hay = words(t["tema"] + " " + t["chaves"])
        th = words(t["tema"])
        sc = 0
        for tk in toks:
            if tk in hay or (len(tk) >= 4 and any(w.startswith(tk) for w in hay)):
                sc += 2 if tk in th else 1
        if sc:
            scored.append((sc, t))
    scored.sort(key=lambda x: (-x[0], x[1]["fonte"], x[1]["paginas"][0]))
    return [t for _, t in scored[:top]]


def show(t):
    print(f"- [{t['fonte']} p.{fmt_pages(t['paginas'])}] {t['tema']} -> references/{t['arquivo']}\n    {t['resumo']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--source", choices=["RN", "FLT", "SWT"])
    ap.add_argument("--page", nargs=2, metavar=("SIGLA", "N"))
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    idx = load()
    if a.sources:
        for k, v in idx["fontes"].items():
            print(f"{k}: {v['arquivo']} ({v['paginas']} pages; useful {v['uteis']}) - {v['descricao']} [DATED: {v['datado']}]")
        return 0
    if a.gaps:
        print("NOT COVERED in the three sources (answer this way; any detail is [extrapolation]):")
        for g in idx["sem_cobertura"]:
            print(f"- {g['termos'].replace('|', ', ')}: {g['nota']}")
        return 0
    if a.page:
        sig, n = a.page[0].upper(), a.page[1]
        if sig not in idx["fontes"] or not n.isdigit():
            print("Usage: --page RN|FLT|SWT N", file=sys.stderr)
            return 1
        n = int(n)
        if not 1 <= n <= idx["fontes"][sig]["paginas"]:
            print(f"Error: {sig} has {idx['fontes'][sig]['paginas']} pages.", file=sys.stderr)
            return 1
        ts = [t for t in idx["topicos"] if t["fonte"] == sig and n in t["paginas"]]
        if not ts:
            print(f"{sig} p.{n}: no useful technical topic (footer/navigation/image).")
            return 0
        for t in ts:
            show(t)
        return 0
    if not a.terms:
        ap.print_help()
        return 1
    res = search(idx, a.terms, a.source, a.top)
    gaps = gaps_for(idx, a.terms)
    if a.json:
        print(json.dumps({"achados": res, "sem_cobertura": [g["termos"] for g in gaps]}, ensure_ascii=False, indent=1))
        return 0
    for t in res:
        show(t)
    for g in gaps:
        print(f"NOT COVERED: {g['nota']}")
    if not res and not gaps:
        print("NOT COVERED: the term matches no topic in the sources (RN, FLT, SWT). Any answer is [extrapolation].")
    return 0


if __name__ == "__main__":
    sys.exit(main())
