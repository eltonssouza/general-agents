# -*- coding: utf-8 -*-
"""
bsrs_lookup.py - finds topics of "Building Secure and Reliable Systems" (BSRS) and the PDF pages.

Usage (Python 3, stdlib, no network, read-only; run with `python -I`):
  python -I scripts/bsrs_lookup.py "menor privilegio" [--top N] [--json]   # queries in Portuguese or English
  python -I scripts/bsrs_lookup.py --chapters            # chapter map -> PDF/printed pages -> reference
  python -I scripts/bsrs_lookup.py --page 465            # converts a PDF page into printed page + chapter
  python -I scripts/bsrs_lookup.py --printed 429         # converts a printed page into a PDF page
  python -I scripts/bsrs_lookup.py --chapter 14          # lists the indexed topics of the chapter
  python -I scripts/bsrs_lookup.py --datado              # topics marked [DATED] (alias: --dated)
  python -I scripts/bsrs_lookup.py --gaps                # terms verified ABSENT from the full text of the book

Convention: PDF page ("=== PAGE N ===" marker); printed = PDF - 36 in the body (chs. 1-21).
The topic index (bsrs_index.json) is generated and keeps the Portuguese-edition keywords of the book (topic titles and summaries are in English);
queries may be in Portuguese or English (English terms come from `terms_en`).
When the collection does not cover the term, prints "NOT COVERED" (and forwards SRE topics).
Exit code: 0 whenever the script runs; the "NOT COVERED" result is informational.
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
INDEX = os.path.join(HERE, "bsrs_index.json")

STOP = set("a o as os de da do das dos e em no na nos nas um uma uns umas para por com sem que se ao aos ou the of and to in on for with is are how what why como que qual quais quando onde livro bsrs sobre pagina paginas".split())


def en_label(label):
    """Maps legacy Portuguese labels (if any) in the index to the English glossary."""
    return label.replace("[do livro]", "[from source]").replace("[DATADO]", "[DATED]")


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
    """Light stemming (pt/en) only to match plural/singular."""
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
    if 39 <= p <= 536:
        return str(p - 36)
    if 25 <= p <= 38:
        roman = ["xxiii", "xxiv", "xxv", "xxvi", "xxvii", "xxviii", "xxix", "xxx", "xxxi", "xxxii", "xxxiii", "xxxiv", "xxxv", "xxxvi"]
        i = p - 25
        return roman[i] if 0 <= i < len(roman) else "(front matter)"
    if p > 536:
        return "(index, printed p.%d)" % (p - 36)
    return "(front matter)"


def chapter_of(idx, p):
    for c in idx["capitulos"]:
        a, b = [int(x) for x in c["pdf"].split("-")]
        if a <= p <= b:
            return c
    return None


def main():
    ap = argparse.ArgumentParser(description="BSRS topic lookup")
    ap.add_argument("query", nargs="*", help="search terms (pt or en)")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--datado", "--dated", dest="datado", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    a = ap.parse_args()
    idx = load()

    if a.chapters:
        for c in idx["capitulos"]:
            print("Ch.%-2d  PDF p.%-8s printed p.%-8s %s -> references/%s" % (c["n"], c["pdf"], c["impressa"], c["titulo"], c["ref"]))
        return
    if a.page is not None:
        c = chapter_of(idx, a.page)
        print("PDF p.%d = printed page %s%s" % (a.page, pdf_to_printed(a.page), (" | Ch.%d %s (references/%s)" % (c["n"], c["titulo"], c["ref"])) if c else ""))
        return
    if a.printed is not None:
        p = a.printed + 36
        c = chapter_of(idx, p)
        print("printed page %d = PDF p.%d%s" % (a.printed, p, (" | Ch.%d %s" % (c["n"], c["titulo"])) if c else ""))
        return
    if a.chapter is not None:
        n = 0
        for e in idx["entradas"]:
            if str(e.get("chapter", "")).lstrip("0") == str(a.chapter):
                n += 1
                print("- %s (BSRS p.%s) -> references/%s %s" % (e["topic"], e["pages"], e["ref"], en_label(e.get("label", ""))))
        if not n:
            print("NOT COVERED: no indexed topic for chapter %d" % a.chapter)
        return
    if a.datado:
        for e in idx["entradas"]:
            if "DATADO" in e.get("label", "") or "DATED" in e.get("label", ""):
                print("- [DATED] %s (BSRS p.%s) -> references/%s" % (e["topic"], e["pages"], e["ref"]))
        print("See references/datado-desde-2020.md for what has changed since 2020 ([extrapolation]).")
        return
    if a.gaps:
        print("Terms verified ABSENT from the full text of the BSRS (whole-word search across the 557 pages):")
        print(", ".join(idx["gaps_globais"]))
        print("If the user asks about them, answer NOT COVERED in the book and mark [extrapolation]/[DATED].")
        return

    if not a.query:
        ap.print_help()
        return
    q = " ".join(a.query)
    qn = norm(q)
    toks = tokens(q)

    results = []
    for e in idx["entradas"]:
        s = score_entry(e, qn, toks)
        if s >= 4:
            results.append((s, e))
    results.sort(key=lambda x: (-x[0], x[1]["topic"]))

    notes = []
    for g in idx["gaps_globais"]:
        gn = norm(g)
        if gn and re.search(r"(?<![a-z0-9])" + re.escape(gn) + r"(?![a-z0-9])", qn):
            notes.append("The term '%s' does NOT appear in any of the 557 pages of the BSRS (verified)." % g)
    for fw in idx.get("encaminhar", []):
        for t in fw["termos"]:
            if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", qn):
                notes.append("BOUNDARY: %s Forward to %s. The book mentions it at: %s." % (fw["nota"], fw["agente"], fw["citas"]))
                break

    if a.json:
        out = {"query": q, "results": [dict(score=s, **e) for s, e in results[: a.top]], "notes": notes, "not_covered": not results}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return

    if not results:
        print("NOT COVERED: the collection (BSRS) has no indexed topic for '%s'." % q)
        for n in notes:
            print("  - " + n)
        print("  Tip: try the author's English terms or use --chapters; treat any answer as [extrapolation].")
        return
    for s, e in results[: a.top]:
        print("[%d] %s %s" % (s, e["topic"], en_label(e.get("label", ""))))
        print("    BSRS p.%s (Ch.%s) -> references/%s" % (e["pages"], str(e.get("chapter", "")).lstrip("0") or "-", e["ref"]))
        print("    %s" % e.get("summary", ""))
    for n in notes:
        print("  * " + n)


if __name__ == "__main__":
    main()
