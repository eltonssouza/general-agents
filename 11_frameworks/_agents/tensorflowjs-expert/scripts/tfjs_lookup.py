# -*- coding: utf-8 -*-
"""
tfjs_lookup.py - locates topics in the 5 captures of tensorflow.org/js (pt-br) and answers NOT COVERED.

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/tfjs_lookup.py TERM...
Convention: citation = CODE + PDF page of the capture (e.g. TFJS p.4). Codes: TFJG guide, TFJL landing,
TFJS setup, TFJI getting started/tutorial index, TFJB = 404 page (do not use).
Terms may be given in Portuguese or English (the index keeps Portuguese keywords and adds English ones).

Options:
  TERM [TERM...]     search by topic (accents ignored); --top N (default 5); --json
  --sources          inventory of the sources (date, usefulness)
  --page CODE N      topics that cite that page
  --gaps             NOT COVERED topics
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
    with io.open(os.path.join(HERE, "tfjs_index.json"), encoding="utf-8") as f:
        return json.load(f)


def gap_hits(idx, terms):
    q = " " + norm(" ".join(terms)) + " "
    hits = []
    for g in idx["sem_cobertura"]:
        for ph in g["termos"].split("|"):
            if (" " + ph + " ") in q or ph in q.split():
                hits.append(g)
                break
    return hits


def search(idx, terms, top):
    toks = [t for t in re.findall(r"[a-z0-9.@/+-]+", norm(" ".join(terms))) if len(t) > 1]
    scored = []
    for t in idx["topicos"]:
        hay = set(re.findall(r"[a-z0-9.@/+-]+", norm(t["tema"] + " " + t["chaves"])))
        th = set(re.findall(r"[a-z0-9.@/+-]+", norm(t["tema"])))
        sc = 0
        for tk in toks:
            if tk in hay or (len(tk) >= 5 and any(w.startswith(tk) for w in hay)):
                sc += 2 if tk in th else 1
        if sc:
            scored.append((sc, t))
    scored.sort(key=lambda x: (-x[0], x[1]["tema"]))
    return [t for _, t in scored[:top]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--page", nargs=2, metavar=("CODE", "N"))
    ap.add_argument("--gaps", action="store_true")
    a = ap.parse_args()
    idx = load()

    if a.sources:
        for k, v in idx["fontes"].items():
            flag = "" if v["util"] else "  [DO NOT USE]"
            print(f"{k}  {v['pdf']}  ({v['paginas']} pages)  date: {v['data']}  - {v['descricao']}{flag}")
        return 0
    if a.gaps:
        print("NOT COVERED in the TensorFlow.js captures:")
        for g in idx["sem_cobertura"]:
            print(" -", g["tema"])
        return 0
    if a.page:
        sig = a.page[0].upper()
        if sig not in idx["fontes"]:
            print("Unknown code:", sig)
            return 1
        try:
            n = int(a.page[1])
        except ValueError:
            print("Invalid page.")
            return 1
        f = idx["fontes"][sig]
        if not 1 <= n <= f["paginas"]:
            print(f"{sig} has {f['paginas']} pages.")
            return 1
        if not f["util"]:
            print(f"{sig} p.{n}: source discarded (404).")
            return 0
        tag = f"{sig} p.{n}"
        found = [t for t in idx["topicos"] if tag in t["cites"]]
        if not found:
            print(f"{tag}: no indexed topic (navigation page, license or fragment).")
        for t in found:
            print(f"{tag}: {t['tema']} -> references/{t['ref']}")
        return 0
    if not a.terms:
        ap.print_help()
        return 1

    gaps = gap_hits(idx, a.terms)
    res = search(idx, a.terms, a.top)
    if a.json:
        print(json.dumps({"resultados": res, "sem_cobertura": [g["tema"] for g in gaps]}, ensure_ascii=False, indent=1))
        return 0
    for g in gaps:
        print(f"NOT COVERED: {g['tema']} (the queried term is not addressed in the captures)")
    for t in res:
        print(f"- {t['tema']}  [{'; '.join(t['cites'])}]  -> references/{t['ref']}")
    if not res and not gaps:
        print("NOT COVERED: no indexed topic matches; see --gaps and references/INDEX.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
