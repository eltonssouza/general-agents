# -*- coding: utf-8 -*-
"""
dlb_lookup.py - locates topics of "Deep Learning" (Goodfellow, Bengio, Courville, MIT Press, 2016; abbreviated DLB) by topic, page or chapter.

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/dlb_lookup.py TERM
Page convention: PDF (marker "=== PAGE N ===" of the extracted text). Printed page = PDF - 15 (constant on p.16-735).
Source of the findings: [from source] = the index points to the page where the topic was read; the classification of the topic itself is [inference].

Options:
  TERM [TERM...]     search by topic (accents ignored; PT or EN); --top N (default 6); --json
  --page N           chapter, printed page, whether the page was READ and topics covered
  --printed N        PDF page corresponding to printed page N
  --chapters         chapter table: PDF range, part, reading, reference file
  --chapter N        topics of chapter N
  --gaps             NOT COVERED terms and NOT READ ranges
  --datado           [DATED] blocks (reads references/datado-desde-2016.md)
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
PKG = os.path.dirname(HERE)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "dlb_index.json"), encoding="utf-8") as f:
        return json.load(f)


def ranges(spec):
    out = []
    for tok in spec.split(","):
        tok = tok.strip()
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", tok)
        if m:
            a = int(m.group(1))
            out.append((a, int(m.group(2) or a)))
    return out


def in_ranges(p, spec):
    return any(a <= p <= b for a, b in ranges(spec))


def chapter_of(idx, p):
    for c in idx["capitulos"]:
        if c["pdf_ini"] <= p <= c["pdf_fim"]:
            return c
    return None


def tokens(q):
    return [t for t in re.split(r"[^a-z0-9+#.\-/^]+", norm(q)) if t]


def score(entry, qn, qtoks):
    best = 0
    for term in entry["termos"] + [entry["topico"]]:
        tn = norm(term)
        if qn == tn:
            best = max(best, 100)
        elif len(qn) >= 2 and re.search(r"(?<![a-z0-9])" + re.escape(qn) + r"(?![a-z0-9])", tn):
            best = max(best, 60 if tn in [norm(x) for x in entry["termos"]] else 40)
        elif len(tn) >= 3 and re.search(r"(?<![a-z0-9])" + re.escape(tn) + r"(?![a-z0-9])", qn):
            best = max(best, 50)
    ttoks = set()
    for term in entry["termos"] + [entry["topico"]]:
        ttoks.update(tokens(term))
    hits = [t for t in qtoks if len(t) >= 3 and t in ttoks]
    if hits:
        best = max(best, 10 * len(hits))
    return best


def find_gap(idx, qn):
    for g in idx["lacunas"]:
        for term in g["busca"]:
            tn = norm(term)
            if qn == tn or re.search(r"(?<![a-z0-9])" + re.escape(tn) + r"(?![a-z0-9])", qn):
                return g
    return None


def cmd_search(idx, args):
    q = " ".join(args.termo)
    qn = norm(q)
    qt = tokens(q)
    res = []
    for e in idx["entradas"]:
        s = score(e, qn, qt)
        if s > 0:
            res.append((s, e))
    res.sort(key=lambda x: (-x[0], x[1]["cap"]))
    res = res[: args.top]
    gap = find_gap(idx, qn)
    if args.json:
        print(json.dumps({"consulta": q, "resultados": [dict(score=s, **e) for s, e in res],
                          "sem_cobertura": gap, "aviso": "2016 book [DATED]"}, ensure_ascii=False, indent=1))
        return 0
    if gap:
        print(f"NOT COVERED: '{gap['termo']}' - {gap['nota']} [verified by search in the extracted text]")
    if not res:
        if not gap:
            print(f"NOT COVERED: no indexed topic matches '{q}'. See --chapters/--gaps; any answer about it is [extrapolation] or [DATED].")
        return 0
    for s, e in res:
        c = next(x for x in idx["capitulos"] if x["cap"] == e["cap"])
        print(f"- {e['topico']}")
        print(f"    DLB p.{e['paginas']} (PDF; printed = PDF - 15) | Cap.{e['cap']} {c['titulo']} (Part {c['parte']}) | ref: references/{e['ref']} | chapter reading: {c['leitura']}")
    print("Source: [inference] over the index; confirm the text in the reference before citing. 2016 book [DATED].")
    return 0


def cmd_page(idx, p):
    c = chapter_of(idx, p)
    if not c:
        if 736 <= p <= 800:
            print(f"PDF p.{p}: Bibliography/Index (not used as a source).")
        else:
            print(f"PDF p.{p}: outside the mapped chapters (p.1-15 front matter; p.44-45, 181-182, 502-503 Part openers; p.736-800 bibliography and index).")
        return 0
    lido = any(a <= p <= b for a, b in c["lido"])
    print(f"PDF p.{p} | Cap.{c['cap']} {c['titulo']} (Part {c['parte']}) | printed {p - idx['offset']} | chapter reading: {c['leitura']}")
    print("  page READ by this package" if lido else "  page NOT READ by this package (no direct coverage)")
    for e in idx["entradas"]:
        if in_ranges(p, e["paginas"]):
            print(f"  - {e['topico']} (p.{e['paginas']}) -> references/{e['ref']}")
    return 0


def cmd_printed(idx, n):
    p = n + idx["offset"]
    c = chapter_of(idx, p)
    print(f"printed {n} -> PDF p.{p}" + (f" (Cap.{c['cap']} {c['titulo']})" if c else " (outside the mapped chapters)"))
    return 0


def cmd_chapters(idx):
    for c in idx["capitulos"]:
        print(f"Cap.{c['cap']:>2} {c['titulo']} | Part {c['parte']} | PDF {c['pdf_ini']}-{c['pdf_fim']} | {c['leitura']} | references/{c['ref']}")
    return 0


def cmd_chapter(idx, n):
    c = next((x for x in idx["capitulos"] if x["cap"] == n), None)
    if not c:
        print("invalid chapter (1-20)")
        return 1
    print(f"Cap.{n} {c['titulo']} | PDF {c['pdf_ini']}-{c['pdf_fim']} | reading: {c['leitura']} | read: {c['lido']}")
    k = 0
    for e in idx["entradas"]:
        if e["cap"] == n:
            k += 1
            print(f"- {e['topico']} | DLB p.{e['paginas']} | references/{e['ref']}")
    if not k:
        print("(no indexed topics for this chapter)")
    return 0


def cmd_gaps(idx):
    print("NOT COVERED (terms absent from the book, verified by search in the extracted text; the book is from 2016):")
    for g in idx["lacunas"]:
        print(f"- {g['termo']}: {g['nota']}")
    print("\nRANGES NOT READ by this package (may exist in the book; do not use as [from source]):")
    for g in idx["nao_lido"]:
        print(f"- PDF p.{g['paginas']}: {g['tema']}")
    return 0


def cmd_datado():
    fp = os.path.join(PKG, "references", "datado-desde-2016.md")
    if not os.path.exists(fp):
        print("references/datado-desde-2016.md missing")
        return 1
    for line in io.open(fp, encoding="utf-8"):
        if line.startswith("#") or line.startswith("- **"):
            print(line.rstrip())
    return 0


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("termo", nargs="*")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--datado", action="store_true")
    a = ap.parse_args()
    idx = load()
    if a.page is not None:
        return cmd_page(idx, a.page)
    if a.printed is not None:
        return cmd_printed(idx, a.printed)
    if a.chapters:
        return cmd_chapters(idx)
    if a.chapter is not None:
        return cmd_chapter(idx, a.chapter)
    if a.gaps:
        return cmd_gaps(idx)
    if a.datado:
        return cmd_datado()
    if not a.termo:
        ap.print_help()
        return 1
    return cmd_search(idx, a)


if __name__ == "__main__":
    sys.exit(main())
