# -*- coding: utf-8 -*-
"""
fw_lookup.py - locates topics in the three sources of the java-backend-frameworks-expert package:
  SB3G = "Mastering Spring Boot 3.0" (Ahmet Meric, Packt, 2024; 256 pp.)
  QRK  = DZone Refcard "Getting Started With Quarkus Serverless Functions" (Daniel Oh, Red Hat, 2021; 9 pp.)
  MPS  = "MapStruct 1.6.3 Reference Guide" (2024-11-09; 96 pp.)

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/fw_lookup.py TERM
Convention: pages = PDF page (SB3G: printed = PDF - 19 in the chapters).

Options:
  TERM [TERM...]     search by topic (accents ignored); --source SB3G|QRK|MPS; --top N (default 6); --json
  --page N --source S   topics that cover page N of source S
  --sources             identify the sources
  --gaps                topics NOT COVERED
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


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9:.+#]+", norm(text)) if t]


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
    ap.add_argument("--source", choices=["SB3G", "QRK", "MPS"])
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
        return
    if a.gaps:
        print("NOT COVERED in this package:")
        for g in idx["sem_cobertura"]:
            print(" -", g["tema"])
        for k, v in idx["meta"]["paginas_sem_conteudo"].items():
            if v:
                print(f"Blank/no-content pages in {k}:", ",".join(map(str, v)))
        for k, v in idx["meta"].get("paginas_promocionais", {}).items():
            if v:
                print(f"Promotional/advertisement pages in {k}:", ",".join(map(str, v)))
        return
    if a.page is not None:
        if not a.source:
            print("Use --page N --source SB3G|QRK|MPS.")
            sys.exit(2)
        mx = idx["meta"]["paginas_max"][a.source]
        if not 1 <= a.page <= mx:
            print(f"Page outside 1-{mx} in {a.source}.")
            sys.exit(1)
        if a.page in idx["meta"]["paginas_sem_conteudo"].get(a.source, []):
            print(f"{a.source} p.{a.page}: blank/divider page (no content).")
            return
        if a.page in idx["meta"].get("paginas_promocionais", {}).get(a.source, []):
            print(f"{a.source} p.{a.page}: promotional/advertisement page (no technical content).")
            return
        found = [t for t in idx["topicos"] if t["fonte"] == a.source and a.page in t["paginas"]]
        if not found:
            print(f"{a.source} p.{a.page}: no indexed topic (front matter, table of contents, back-of-book index or not covered).")
            return
        for t in found:
            print(f"- {t['tema']}  [{a.source} p.{fmt_pages(t['paginas'])}]  -> references/{t['ref']}")
        return
    if not a.terms:
        ap.print_help()
        return
    gaps = gap_hits(idx, a.terms)
    scored = search(idx, a.terms, a.top, a.source)
    if gaps:  # with a declared gap, only show topics with at least 3 points (reduces noise)
        scored = [x for x in scored if x[0] >= 3]
    hits = [t for _, t in scored]
    if a.json:
        print(json.dumps({"achados": hits, "sem_cobertura": gaps}, ensure_ascii=False, indent=1))
        return
    if not hits and not gaps:
        print("NOT COVERED: no topic in the index matches. The sources (SB3G, QRK, MPS) may not address the topic; "
              "check --gaps. Answer as [extrapolation] only if the user asks.")
        return
    for g in gaps:
        print("NOT COVERED:", g["tema"])
    for t in hits:
        print(f"- {t['tema']}  [from source: {t['fonte']} p.{fmt_pages(t['paginas'])}]  -> references/{t['ref']}")


if __name__ == "__main__":
    main()
