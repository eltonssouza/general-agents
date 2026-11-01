# -*- coding: utf-8 -*-
"""
nx_lookup.py - locates topics in the 6 sources of the collection (NX13, NX14, NX15, NX16 = release posts; NXHB = Next.js
Handbook freeCodeCamp 2019 [DATED]; RCTHB = React Handbook freeCodeCamp 2020 [DATED]). Read-only, stdlib,
no network, deterministic. Run with: python -I scripts/nx_lookup.py TERM...

Page convention: PDF page (the 6 PDFs have no printed number).
Options:
  TERM [TERM...]       topic search (accents ignored; Portuguese and English terms); --top N (default 8); --source NX15|NXHB|...; --json
  --page SOURCE N      what page N of that source covers (e.g. --page NX16 12)
  --sources            sources, dates, useful pages
  --conflicts          DATED (NXHB/RCTHB) x release conflicts/evolutions, with pages
  --gaps               NOT COVERED topics
"""
import argparse, io, json, os, re, sys, unicodedata

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
    with io.open(os.path.join(HERE, "nx_index.json"), encoding="utf-8") as f:
        idx = json.load(f)
    with io.open(os.path.join(HERE, "nx_changes.json"), encoding="utf-8") as f:
        ch = json.load(f)
    for e in ch["entries"]:
        idx["topicos"].append({"fonte": f"NX{e['v']}", "tema": e["title"] + f" ({e['kind']})", "paginas": e["pages"],
                               "chaves": e["kw"] + " " + " ".join(e["thread"])})
    return idx


def pg(p):
    return ",".join(str(i) for i in p)


def tag(f):
    return " [DATED]" if f in ("NXHB", "RCTHB") else ""


def words(s):
    return set(re.findall(r"[a-z0-9@./_\-]+", norm(s)))


def search(idx, terms, top, src):
    q = norm(" ".join(terms))
    toks = [t for t in re.findall(r"[a-z0-9@./_\-]+", q)]
    gap_hit = [g for g in idx["sem_cobertura"] if any(("|" + ph + "|") in ("|" + q + "|") or ph in q for ph in g["termos"].split("|"))]
    scored = []
    for t in idx["topicos"]:
        if src and t["fonte"] != src:
            continue
        hay = words(t["tema"] + " " + t["chaves"])
        hay_s = norm(t["tema"] + " " + t["chaves"])
        th = words(t["tema"])
        sc = 0
        for tk in toks:
            if tk in hay:
                sc += 2 if tk in th else 1
            elif len(tk) >= 5 and tk in hay_s:
                sc += 1
        if sc:
            scored.append((sc, t))
    scored.sort(key=lambda x: (-x[0], x[1]["fonte"], x[1]["paginas"][0]))
    return [t for _, t in scored[:top]], gap_hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--source")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", nargs=2, metavar=("FONTE", "N"))
    ap.add_argument("--sources", action="store_true")
    ap.add_argument("--conflicts", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    a = ap.parse_args()
    idx = load()
    if a.sources:
        for k, v in idx["fontes"].items():
            print(f"{k}: {v['pdf']} | {v['tipo']} | {v['data']} | {v['paginas']} pages (useful: {v['uteis']})")
        return
    if a.gaps:
        print("NOT COVERED in the collection (NX13-NX16 posts + NXHB 2019 + RCTHB 2020):")
        for g in idx["sem_cobertura"]:
            print(" -", g["tema"])
        return
    if a.conflicts:
        for c in idx["conflitos"]:
            d, r = c["datado"], c["release"]
            print(f"{c['id']} [{c['tipo']}] {c['tema']}")
            print(f"   [DATED] {d['fonte']} p.{pg(d['paginas'])}: {d['afirma']}")
            print(f"   [release] {r['fonte']} p.{pg(r['paginas'])}: {r['afirma']}")
            print(f"   note: {c['nota']}")
        return
    if a.page:
        f = a.page[0].upper()
        n = int(a.page[1])
        if f not in idx["fontes"]:
            print("Invalid source. Use:", ", ".join(idx["fontes"]))
            sys.exit(1)
        m = idx["fontes"][f]
        if not 1 <= n <= m["paginas"]:
            print(f"{f} has {m['paginas']} pages.")
            sys.exit(1)
        hits = [t for t in idx["topicos"] if t["fonte"] == f and n in t["paginas"]]
        if not hits:
            print(f"{f} p.{n}: no indexed topic (cover page, footer, contributor list or image only).")
        for t in hits:
            print(f"{f} p.{n}: {t['tema']} (p.{pg(t['paginas'])}){tag(f)}")
        return
    if not a.terms:
        ap.print_help()
        return
    hits, gaps = search(idx, a.terms, a.top, a.source.upper() if a.source else None)
    if a.json:
        print(json.dumps({"achados": hits, "sem_cobertura": gaps}, ensure_ascii=False, indent=1))
        return
    if not hits and not gaps:
        print("NOT COVERED: no topic in the index matches. The collection (4 Next 13-16 release posts, NXHB 2019, "
              "RCTHB 2020) may not cover the topic; check --gaps and use [extrapolation] only if the user asks.")
        return
    for g in gaps:
        print("NOT COVERED:", g["tema"])
    for t in hits:
        print(f"- [{t['fonte']}{tag(t['fonte'])}] {t['tema']}  [p.{pg(t['paginas'])}]")
    if hits:
        print("For the evolution by version use: python -I scripts/nx_changes.py topic TERM")


if __name__ == "__main__":
    main()
