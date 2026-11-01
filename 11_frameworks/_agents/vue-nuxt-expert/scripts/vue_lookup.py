# -*- coding: utf-8 -*-
"""
vue_lookup.py - locates topics in the 3 sources of the vue-nuxt-expert collection:
  VUEHB = Vue Handbook (freeCodeCamp, 5 Jul 2018, Vue 2 by inference, 133 pages)
  VUE3G = Vue 3 documentation introduction (2026 capture, 8 pages)
  NUXT  = "Get Started with Nuxt v4" introduction (v4.5.2, 6 pages)

Read-only, stdlib, no network, deterministic. Run: python -I scripts/vue_lookup.py TERM
Page convention: PDF page (marker "=== PAGE N ===").
[DATED] each source is relative to its own date.
Queries may be in English or Portuguese (index keywords are bilingual).

Options:
  TERM [TERM...]        topic search (accents ignored); --top N (default 6); --json; --source VUEHB|VUE3G|NUXT
  --page SOURCE N       topics that cover page N of the source
  --sources             list the sources
  --gaps                NOT COVERED topics
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
    with io.open(os.path.join(HERE, "vue_index.json"), encoding="utf-8") as f:
        return json.load(f)


def words(s):
    return set(re.findall(r"[a-z0-9$:@._/-]+", norm(s)))


def fmt_pages(p):
    return ",".join(str(x) for x in p)


def search(idx, terms, top, source):
    q = norm(" ".join(terms))
    qpad = " " + re.sub(r"[^a-z0-9$:@._/-]+", " ", q) + " "
    toks = [t for t in re.findall(r"[a-z0-9$:@._/-]+", q) if t]
    gaps = []
    for g in idx["sem_cobertura"]:
        if any((" " + ph + " ") in qpad for ph in g["termos"].split("|")):
            gaps.append(g)
    scored = []
    for t in idx["topicos"]:
        if source and t["fonte"] != source:
            continue
        hay = words(t["tema"] + " " + t["chaves"])
        th = words(t["tema"])
        sc = 0
        for tk in toks:
            if tk in hay or (len(tk) >= 5 and any(w.startswith(tk) for w in hay)):
                sc += 2 if tk in th else 1
        if sc:
            scored.append((sc, t))
    scored.sort(key=lambda x: (-x[0], x[1]["fonte"], x[1]["paginas"][0]))
    return [t for _, t in scored[:top]], gaps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--source", choices=["VUEHB", "VUE3G", "NUXT"])
    ap.add_argument("--page", nargs=2, metavar=("FONTE", "N"))
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    a = ap.parse_args()
    idx = load()

    if a.sources:
        for k, v in idx["fontes"].items():
            print(f"{k}: {v}")
        print("Convention: PDF page; the sources have no printed page numbers.")
        return
    if a.gaps:
        print("NOT COVERED in the collection (VUEHB 2018 / VUE3G / NUXT v4.5.2):")
        for g in idx["sem_cobertura"]:
            print(" -", g["tema"])
        for k, v in idx["paginas_sem_texto_util"].items():
            if v:
                print(f"Pages without useful text in {k}: {fmt_pages(v)}")
        return
    if a.page:
        src = a.page[0].upper()
        try:
            n = int(a.page[1])
        except ValueError:
            print("N must be an integer.")
            sys.exit(1)
        if src not in idx["paginas_totais"]:
            print("Invalid source (VUEHB, VUE3G, NUXT).")
            sys.exit(1)
        if not 1 <= n <= idx["paginas_totais"][src]:
            print(f"Page outside 1-{idx['paginas_totais'][src]} for {src}.")
            sys.exit(1)
        if n in idx["paginas_sem_texto_util"][src]:
            print(f"{src} p.{n}: page without useful technical text (screenshot, footer or empty).")
        hit = False
        for t in idx["topicos"]:
            if t["fonte"] == src and n in t["paginas"]:
                hit = True
                print(f"{src} p.{n}: {t['tema']} (p.{fmt_pages(t['paginas'])}) -> references/{t['ref']}")
        if not hit:
            print(f"{src} p.{n}: no indexed topic (cover, divider or auxiliary text).")
        return
    if not a.terms:
        ap.print_help()
        return
    hits, gaps = search(idx, a.terms, a.top, a.source)
    if a.json:
        print(json.dumps({"achados": hits, "sem_cobertura": gaps}, ensure_ascii=False, indent=1))
        return
    if not hits and not gaps:
        print("NOT COVERED: no index topic matches. The sources are short (2018 handbook, "
              "Vue 3 intro and Nuxt v4 intro); answer [extrapolation] only if the user asks. See --gaps.")
        return
    for g in gaps:
        print("NOT COVERED:", g["tema"])
    for t in hits:
        print(f"- {t['tema']}  [from source: {t['fonte']} p.{fmt_pages(t['paginas'])}]  -> references/{t['ref']}")


if __name__ == "__main__":
    main()
