# -*- coding: utf-8 -*-
"""
mly_lookup.py - locates topics of "Machine Learning Yearning" (Andrew Ng, 2018 DRAFT; MLY).

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/mly_lookup.py TERM
Page convention: PDF page = printed number "Page N" (no offset; 118 pages).
[DATED] the book is a 2018 draft (pre-Transformer deep learning).
Input terms may be English or Portuguese (accents ignored); the index keeps both sets of keywords.

Options:
  TERM [TERM...]     search by topic (accents ignored); --top N (default 5); --json
  --page N           chapter and topics of page N
  --chapter N        pages and topics of chapter N (1-58)
  --chapters         chapter table
  --gaps             topics NOT COVERED by the book
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
    with io.open(os.path.join(HERE, "mly_index.json"), encoding="utf-8") as f:
        return json.load(f)


def cap_of(idx, page):
    return [c for c in idx["capitulos"] if c["pdf_ini"] <= page <= c["pdf_fim"]]


def fmt_pages(p):
    return ",".join(str(x) for x in p)


def search(idx, terms, top):
    toks = [t for t in norm(" ".join(terms)).replace("-", " ").split() if t]
    gap_hit = []
    q = " " + norm(" ".join(terms)) + " "
    for g in idx["sem_cobertura"]:
        if any((" " + ph + " ") in q or q.strip() == ph for ph in g["termos"].split("|")):
            gap_hit.append(g)
    scored = []
    for t in idx["topicos"]:
        hay = set(re.findall(r"[a-z0-9%/]+", norm(t["tema"] + " " + t["chaves"]).replace("-", " ")))
        th = set(re.findall(r"[a-z0-9%/]+", norm(t["tema"]).replace("-", " ")))
        sc = 0
        for tk in toks:
            if tk in hay or (len(tk) >= 5 and any(w.startswith(tk) for w in hay)):
                sc += 2 if tk in th else 1
        if sc:
            scored.append((sc, t))
    scored.sort(key=lambda x: (-x[0], x[1]["paginas"][0]))
    return [t for _, t in scored[:top]], gap_hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", type=int)
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    a = ap.parse_args()
    idx = load()

    if a.chapters:
        for c in idx["capitulos"]:
            print(f"cap {c['cap']:>2}  MLY p.{c['pdf_ini']}-{c['pdf_fim']}  {c['titulo']}  -> references/{c['ref']}")
        return
    if a.gaps:
        print("NOT COVERED in the MLY (2018 draft):")
        for g in idx["sem_cobertura"]:
            print(" -", g["tema"])
        print("Section-divider-only pages (no content):", fmt_pages(idx["paginas_divisorias"]))
        print("Note:", idx["paginas_so_figura"])
        return
    if a.page is not None:
        if not 1 <= a.page <= 118:
            print("Page out of range 1-118.")
            sys.exit(1)
        if a.page in idx["paginas_divisorias"]:
            print(f"MLY p.{a.page}: section divider page (no content).")
            return
        cs = cap_of(idx, a.page)
        for c in cs:
            print(f"MLY p.{a.page}: cap {c['cap']} - {c['titulo']} (p.{c['pdf_ini']}-{c['pdf_fim']}) -> references/{c['ref']}")
        for t in idx["topicos"]:
            if a.page in t["paginas"]:
                print("  topic:", t["tema"], "(p." + fmt_pages(t["paginas"]) + ")")
        if not cs:
            print("  (no chapter; cover, table of contents or page without content)")
        return
    if a.chapter is not None:
        cs = [c for c in idx["capitulos"] if c["cap"] == a.chapter]
        if not cs:
            print("Chapter out of range 1-58.")
            sys.exit(1)
        c = cs[0]
        print(f"cap {c['cap']} - {c['titulo']} (MLY p.{c['pdf_ini']}-{c['pdf_fim']}) -> references/{c['ref']}")
        for t in idx["topicos"]:
            if t["cap"] == a.chapter:
                print("  topic:", t["tema"], "(p." + fmt_pages(t["paginas"]) + ")")
        return
    if not a.terms:
        ap.print_help()
        return
    hits, gaps = search(idx, a.terms, a.top)
    if a.json:
        print(json.dumps({"matches": hits, "not_covered": gaps}, ensure_ascii=False, indent=1))
        return
    if not hits and not gaps:
        print("NOT COVERED: no index topic matches. The MLY (2018 draft) may not address the subject; "
              "check --gaps and answer as [extrapolation] only if the user asks.")
        return
    for g in gaps:
        print("NOT COVERED:", g["tema"])
    for t in hits:
        cs = cap_of(idx, t["paginas"][0])
        ref = cs[0]["ref"] if cs else "-"
        print(f"- {t['tema']}  [from source: MLY p.{fmt_pages(t['paginas'])}]  cap {t['cap']}  -> references/{ref}")


if __name__ == "__main__":
    main()
