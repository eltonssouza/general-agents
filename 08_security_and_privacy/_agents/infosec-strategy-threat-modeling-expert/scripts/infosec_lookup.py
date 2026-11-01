# -*- coding: utf-8 -*-
"""
infosec_lookup.py - locates topics of the collection (DZ = Infosec Strategies and Best Practices, MacMillan, Packt 2021;
TMM = Threat Modeling Manifesto) and the PDF pages.

Usage (Python 3, stdlib, no network, read-only; run with `python -I`):
  python -I scripts/infosec_lookup.py "risk appetite" [--top N] [--json] [--source DZ|TMM]   (queries in English or Portuguese)
  python -I scripts/infosec_lookup.py --chapters        # chapter map -> PDF/printed pages -> reference
  python -I scripts/infosec_lookup.py --page 33         # converts a DZ PDF page into printed page + chapter
  python -I scripts/infosec_lookup.py --printed 16      # converts a DZ printed page into PDF
  python -I scripts/infosec_lookup.py --chapter 5       # indexed topics of the chapter
  python -I scripts/infosec_lookup.py --tmm             # lists the TMM topics
  python -I scripts/infosec_lookup.py --datado          # topics marked [DATED] (flag name kept for compatibility)
  python -I scripts/infosec_lookup.py --gaps            # terms verified ABSENT from the full text of the two sources

Convention: PDF page ("=== PAGE N ===" marker of the extracted text); DZ printed = PDF - 17 (in the body, from
Ch.1 on); TMM: PDF = document (3 pages).
When the collection does not cover the term, it prints "NOT COVERED" (and refers on when the topic belongs to another agent).
Exit code: 0 whenever the script runs; "NOT COVERED" is informational.
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
INDEX = os.path.join(HERE, "infosec_index.json")

STOP = set("a o as os de da do das dos e em no na nos nas um uma uns umas para por com sem que se ao aos ou the of and to in on for with is are how what why como que qual quais quando onde livro dz tmm sobre pagina paginas".split())


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9+#./ -]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load():
    with io.open(INDEX, "r", encoding="utf-8") as f:
        return json.load(f)


def tokens(q):
    return [t for t in norm(q).split() if len(t) >= 2 and t not in STOP]


def stem(w):
    if len(w) > 4 and w.endswith("eis"):
        return w[:-3] + "el"
    if len(w) > 4 and w.endswith("ais"):
        return w[:-3] + "al"
    if len(w) > 4 and w.endswith("oes"):
        return w[:-3] + "ao"
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def score_entry(e, qn, toks):
    kw = [norm(k) for k in e.get("keywords", [])]
    te = [norm(k) for k in e.get("terms_en", [])]
    topic = norm(e.get("topic", ""))
    summ = norm(e.get("summary", ""))
    kwords = [[stem(w) for w in k.split()] for k in kw + te]
    tw = [stem(w) for w in topic.split()]
    sw = set(stem(w) for w in summ.split())
    sc = 0
    qs = " ".join(stem(w) for w in qn.split())
    if qn:
        for k, ws in zip(kw + te, kwords):
            ks = " ".join(ws)
            if qn == k or qs == ks:
                sc += 10
            elif (qn in k or qs in ks) or (k in qn and len(k) > 3):
                sc += 6
        if qn in topic or qs in " ".join(tw):
            sc += 6
    for t in toks:
        st = stem(t)
        for k, ws in zip(kw + te, kwords):
            if st in ws:
                sc += 4 if len(ws) == 1 else 3
            elif len(st) >= 4 and any(st in w for w in ws):
                sc += 2
        if st in tw:
            sc += 2
        elif len(st) >= 4 and any(st in w for w in tw):
            sc += 1
        if len(st) >= 4 and st in sw:
            sc += 1
    return sc


def pdf_to_printed(p):
    if 20 <= p <= 252:
        return str(p - 17)
    if p > 252:
        return "(editorial material/index; printed ~%d)" % (p - 17)
    return "(front matter, roman numerals)"


def chapter_of(idx, p):
    for c in idx["capitulos"]:
        a, b = [int(x) for x in c["pdf"].split("-")]
        if a <= p <= b:
            return c
    return None


def label(e):
    return "[%s]" % e["source"] + (" " + e["label"] if e.get("label") else "")


def main():
    ap = argparse.ArgumentParser(description="Topic lookup for the DZ + TMM collection")
    ap.add_argument("query", nargs="*", help="search terms (pt or en)")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--source", choices=["DZ", "TMM"])
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--tmm", action="store_true")
    ap.add_argument("--datado", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    a = ap.parse_args()
    idx = load()

    if a.chapters:
        for c in idx["capitulos"]:
            print("DZ Ch.%-2d PDF p.%-8s printed p.%-8s %s -> references/%s" % (c["n"], c["pdf"], c["impressa"], c["titulo"], c["ref"]))
        print("TMM p.1-3 -> references/tmm-manifesto.md")
        return
    if a.page is not None:
        c = chapter_of(idx, a.page)
        print("DZ PDF p.%d = printed page %s%s" % (a.page, pdf_to_printed(a.page), (" | Ch.%d %s (references/%s)" % (c["n"], c["titulo"], c["ref"])) if c else ""))
        return
    if a.printed is not None:
        p = a.printed + 17
        c = chapter_of(idx, p)
        print("DZ printed page %d = PDF p.%d%s" % (a.printed, p, (" | Ch.%d %s" % (c["n"], c["titulo"])) if c else ""))
        return
    if a.chapter is not None:
        n = 0
        for e in idx["entradas"]:
            if e["source"] == "DZ" and str(e.get("chapter", "")) == str(a.chapter):
                n += 1
                print("- %s (DZ p.%s) -> references/%s %s" % (e["topic"], e["pages"], e["ref"], e.get("label", "")))
        if not n:
            print("NOT COVERED: no indexed topic for chapter %d" % a.chapter)
        return
    if a.tmm:
        for e in idx["entradas"]:
            if e["source"] == "TMM":
                print("- %s (TMM p.%s) -> references/%s" % (e["topic"], e["pages"], e["ref"]))
        return
    if a.datado:
        for e in idx["entradas"]:
            if "DATADO" in e.get("label", ""):
                print("- [DATED] %s (DZ p.%s) -> references/%s" % (e["topic"], e["pages"], e["ref"]))
        print("See references/datado-desde-2021.md for what has changed since the edition ([extrapolation]).")
        return
    if a.gaps:
        print("Terms verified ABSENT from the full text of the two sources (DZ 272 pages + TMM 3 pages):")
        print(", ".join(idx["gaps_globais"]))
        print("If the user asks about them, answer NOT COVERED and mark [extrapolation] (e.g., STRIDE/DFD).")
        return

    if not a.query:
        ap.print_help()
        return
    q = " ".join(a.query)
    qn = norm(q)
    toks = tokens(q)

    results = []
    for e in idx["entradas"]:
        if a.source and e["source"] != a.source:
            continue
        s = score_entry(e, qn, toks)
        if s >= 4:
            results.append((s, e))
    results.sort(key=lambda x: (-x[0], x[1]["topic"]))

    notes = []
    for g in idx["gaps_globais"]:
        gn = norm(g)
        if gn and re.search(r"(?<![a-z0-9])" + re.escape(gn) + r"(?![a-z0-9])", qn):
            notes.append("The term '%s' does NOT appear in the text of the DZ or the TMM (verified)." % g)
    for fw in idx.get("encaminhar", []):
        for t in fw["termos"]:
            if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", qn):
                notes.append("BOUNDARY: %s Refer to %s. The DZ touches the topic at: %s." % (fw["nota"], fw["agente"], fw["citas"]))
                break

    if a.json:
        out = {"query": q, "resultados": [dict(score=s, **e) for s, e in results[: a.top]], "notas": notes, "sem_cobertura": not results}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return

    if not results:
        print("NOT COVERED: the collection (DZ + TMM) has no indexed topic for '%s'." % q)
        for n in notes:
            print("  - " + n)
        print("  Tip: try the author's English terms or use --chapters; treat any answer as [extrapolation].")
        return
    for s, e in results[: a.top]:
        print("[%d] %s %s" % (s, e["topic"], label(e)))
        print("    %s p.%s (Ch.%s) -> references/%s" % (e["source"], e["pages"], e.get("chapter", "-"), e["ref"]))
        print("    %s" % e.get("summary", ""))
    for n in notes:
        print("  * " + n)


if __name__ == "__main__":
    main()
