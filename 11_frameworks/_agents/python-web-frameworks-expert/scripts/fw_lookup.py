# -*- coding: utf-8 -*-
"""
fw_lookup.py - locates topics in the three sources of the python-web-frameworks-expert package:
  DJT  = Django, "Writing your first Django app, part 1" (docs 5.0; 8 pp.)
  FLT  = Flask, "Tutorial" landing page (docs 3.1.x; 3 pp.; ONLY an index/introduction)
  FAPI = FastAPI, documentation landing page (v0.141.1; 21 pp.)

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/fw_lookup.py TERM
Convention: pages = PDF page (the sources are captures of web pages and have no printed page numbers).
Input terms may be Portuguese or English (accents are ignored).

Options:
  TERM [TERM...]      search by topic (accents ignored); --source DJT|FLT|FAPI; --top N (default 6); --json
  --page N --source S topics that cover page N of source S
  --sources           identify the sources
  --gaps              NOT COVERED topics
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
SOURCES = ["DJT", "FLT", "FAPI"]


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "fw_index.json"), encoding="utf-8") as f:
        return json.load(f)


def fmt_pages(p):
    p = sorted(p)
    out = []
    i = 0
    while i < len(p):
        j = i
        while j + 1 < len(p) and p[j + 1] == p[j] + 1:
            j += 1
        out.append(str(p[i]) if i == j else f"{p[i]}-{p[j]}")
        i = j + 1
    return ",".join(out)


# Stop words: Portuguese (input keywords still accepted) and English
STOP = {"de", "da", "do", "das", "dos", "e", "o", "a", "as", "os", "em", "no", "na", "nos", "nas", "para", "com", "por", "que",
        "um", "uma", "ao", "se", "ou", "the", "of", "to", "in", "an", "and", "is", "how", "como", "qual", "quais", "meu", "minha",
        "does", "do", "what", "about", "are", "for", "with", "on", "my", "which"}


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9:.+#_\[\]-]+", norm(text)) if t and t not in STOP]


def gap_hits(idx, terms):
    q = " " + norm(" ".join(terms)) + " "
    hits = []
    for g in idx["sem_cobertura"]:
        for ph in g["termos"].split("|"):
            ph = norm(ph)
            if (" " + ph + " ") in q:
                hits.append(g)
                break
    return hits


def search(idx, terms, top, source=None):
    toks = tokens(" ".join(terms))
    scored = []
    for t in idx["topicos"]:
        if source and t["fonte"] != source:
            continue
        hay = set(tokens(t["tema"] + " " + t["chaves"]))
        th = set(tokens(t["tema"]))
        sc = 0
        for tk in toks:
            if tk in hay or (len(tk) >= 5 and any(w.startswith(tk) for w in hay)):
                sc += 2 if tk in th else 1
        if sc:
            scored.append((sc, t))
    scored.sort(key=lambda x: (-x[0], x[1]["fonte"], x[1]["paginas"][0]))
    return scored[:top]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--source", choices=SOURCES)
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", type=int)
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    a = ap.parse_args()
    idx = load()

    if a.sources:
        for k, v in idx["meta"]["fontes"].items():
            print(f"{k}: {v}")
        return 0
    if a.gaps:
        print("NOT COVERED in this package:")
        for g in idx["sem_cobertura"]:
            print(" -", g["tema"])
        for k, v in idx["meta"]["paginas_nao_tecnicas"].items():
            if v:
                print(f"Pages with no technical content (sponsors/navigation) in {k}:", ",".join(map(str, v)))
        return 0
    if a.page is not None:
        if not a.source:
            print("Use --page N --source DJT|FLT|FAPI.")
            return 2
        mx = idx["meta"]["paginas_max"][a.source]
        if not 1 <= a.page <= mx:
            print(f"Page outside 1-{mx} in {a.source}.")
            return 1
        if a.page in idx["meta"]["paginas_nao_tecnicas"].get(a.source, []):
            print(f"{a.source} p.{a.page}: page with no technical content (sponsors, navigation, footer or testimonial).")
            return 0
        found = [t for t in idx["topicos"] if t["fonte"] == a.source and a.page in t["paginas"]]
        if not found:
            print(f"{a.source} p.{a.page}: no indexed topic.")
            return 0
        for t in found:
            print(f"- {t['tema']}  [{a.source} p.{fmt_pages(t['paginas'])}]  -> references/{t['ref']}")
        return 0
    if not a.terms:
        ap.print_help()
        return 0
    gaps = gap_hits(idx, a.terms)
    scored = search(idx, a.terms, a.top, a.source)
    if gaps:  # with a declared gap, show only topics scoring at least 3 (reduces noise)
        scored = [x for x in scored if x[0] >= 3]
    hits = [t for _, t in scored]
    if a.json:
        print(json.dumps({"achados": hits, "sem_cobertura": gaps}, ensure_ascii=False, indent=1))
        return 0
    if not hits and not gaps:
        print("NOT COVERED: no index topic matches. The sources (DJT, FLT, FAPI) may not address the subject; "
              "check --gaps. Answer as [extrapolation] only if the user asks.")
        return 0
    for g in gaps:
        print("NOT COVERED:", g["tema"])
    for t in hits:
        print(f"- {t['tema']}  [from source: {t['fonte']} p.{fmt_pages(t['paginas'])}]  -> references/{t['ref']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
