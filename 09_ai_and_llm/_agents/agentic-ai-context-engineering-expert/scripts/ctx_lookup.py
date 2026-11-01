# -*- coding: utf-8 -*-
"""
ctx_lookup.py - locates topics in BAAS ("Building Agentic AI Systems", Biswas and Talukdar, Packt, Apr/2025)
and CE2 ("Context Engineering 2.0: The Context of Context Engineering", arXiv 2510.26493, Oct/2025).

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/ctx_lookup.py TERM
Page convention: BAAS = PDF page (printed = PDF - 25 in the body); CE2 = PDF page = printed page.
Origin of the result: [inference] over the index; the page shows where the topic was read. Confirm in the reference before citing.
Queries may be in English or Portuguese (accents are ignored).

Options:
  TERM [TERM...]        search by topic (accents ignored); --fonte BAAS|CE2; --top N (default 6); --json
  --page N --fonte F    chapter/section, printed page and topics covered by PDF page N
  --printed N           (BAAS) printed page N -> PDF page (N + 25 in the body)
  --chapters            table of chapters and sections with page range and reference file
  --gaps                NOT COVERED terms and what was not read (figures, references)
  --datado              [DATED] items (reads references/datado.md)
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
    with io.open(os.path.join(HERE, "ctx_index.json"), encoding="utf-8") as f:
        return json.load(f)


def ranges(spec):
    out = []
    for tok in spec.split(","):
        m = re.fullmatch(r"\s*(\d+)(?:-(\d+))?\s*", tok)
        if m:
            a = int(m.group(1))
            out.append((a, int(m.group(2) or a)))
    return out


def in_ranges(p, spec):
    return any(a <= p <= b for a, b in ranges(spec))


def tokens(q):
    return [t for t in re.split(r"[^a-z0-9+#.\-/*_%]+", norm(q)) if t]


def whole(needle, hay):
    return re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", hay) is not None


def score(entry, qn, qtoks):
    best = 0
    terms = entry["termos"] + [entry["topico"]]
    for term in terms:
        tn = norm(term)
        if qn == tn:
            best = max(best, 100)
        elif len(qn) >= 2 and whole(qn, tn):
            best = max(best, 60 if tn in [norm(x) for x in entry["termos"]] else 40)
        elif len(tn) >= 3 and whole(tn, qn):
            best = max(best, 50)
    ttoks = set()
    for term in terms:
        ttoks.update(tokens(term))
    hits = [t for t in qtoks if len(t) >= 3 and t in ttoks]
    if hits:
        best = max(best, 10 * len(hits))
    return best


def find_gap(idx, qn):
    for g in idx["lacunas"]:
        gn = norm(g["termo"])
        parts = [norm(x) for x in re.split(r"[/(),]", g["termo"]) if len(x.strip()) >= 3]
        parts += [norm(b) for b in g.get("busca", []) if len(b) >= 3]
        if qn == gn or any(p and whole(p, qn) for p in parts):
            return g
    return None


def cap_of(idx, fonte, p):
    for c in idx["capitulos"]:
        if c["fonte"] == fonte and c["pdf_ini"] <= p <= c["pdf_fim"] and c["cap"] != "Index" and c["cap"] != "Refs":
            return c
    for c in idx["capitulos"]:
        if c["fonte"] == fonte and c["pdf_ini"] <= p <= c["pdf_fim"]:
            return c
    return None


def cmd_search(idx, a):
    q = " ".join(a.termo)
    qn = norm(q)
    qt = tokens(q)
    res = []
    for i, e in enumerate(idx["topicos"]):
        if a.fonte and e["fonte"] != a.fonte:
            continue
        s = score(e, qn, qt)
        if s > 0:
            res.append((s, i, e))
    res.sort(key=lambda x: (-x[0], x[1]))
    res = res[: a.top]
    gap = find_gap(idx, qn)
    if a.json:
        print(json.dumps({"consulta": q, "resultados": [dict(score=s, **e) for s, _, e in res], "sem_cobertura": gap,
                          "convencao": "pages = PDF; BAAS printed = PDF - 25; CE2 PDF = printed"},
                         ensure_ascii=False, indent=1))
        return 0
    if gap:
        print(f"NOT COVERED (or partially covered): '{gap['termo']}' - {gap['nota']}")
    if not res:
        if not gap:
            print(f"NOT COVERED: no indexed topic matches '{q}'. See --chapters and --gaps; any answer about it is [extrapolation].")
        return 0
    for s, _, e in res:
        extra = f" | note: {e['nota']}" if e.get("nota") else ""
        print(f"- [{e['fonte']}] {e['topico']}")
        print(f"    {e['fonte']} p.{e['paginas']} (PDF) | references/{e['ref']}{extra}")
    print("Origin: [inference] over the index; confirm the text in the reference before citing. Items with [DATED] reflect 2025.")
    return 0


def cmd_page(idx, p, fonte):
    if not fonte:
        print("use --fonte BAAS or --fonte CE2 together with --page")
        return 2
    lim = 289 if fonte == "BAAS" else 28
    if p < 1 or p > lim:
        print(f"{fonte} p.{p}: outside the PDF (1-{lim}).")
        return 0
    c = cap_of(idx, fonte, p)
    if not c:
        print(f"{fonte} p.{p}: no mapped chapter (front matter, blank pages, part dividers, or back cover).")
    else:
        off = idx["fontes"][fonte]["offset_corpo"]
        imp = f" | printed {p - off}" if fonte == "BAAS" and p >= 28 else ""
        print(f"{fonte} PDF p.{p} | {c['cap']}: {c['titulo']}{imp} | reading: {c['leitura']} | references/{c['ref']}")
    for e in idx["topicos"]:
        if e["fonte"] == fonte and in_ranges(p, e["paginas"]):
            print(f"  - {e['topico']} ({fonte} p.{e['paginas']})")
    return 0


def cmd_printed(idx, n):
    p = n + idx["fontes"]["BAAS"]["offset_corpo"]
    if n < 1 or p > 289:
        print(f"printed {n}: outside the BAAS body (printed 3-247 in the body; index 249-257).")
        return 0
    print(f"BAAS printed {n} -> PDF p.{p} (offset 25 in the body; valid for Arabic-numbered pages)")
    return 0


def cmd_chapters(idx):
    for c in idx["capitulos"]:
        print(f"{c['fonte']} {c['cap']:>6} {c['titulo']} | PDF {c['pdf_ini']}-{c['pdf_fim']} | starting printed page {c['impressa_ini']} | {c['leitura']} | references/{c['ref']}")
    for k, v in idx["fontes"].items():
        print(f"\n{k}: {v['titulo']} | {v['autores']} | {v['editora']} | {v['ano']} | {v['paginas_pdf']} pp. | {v['convencao']}")
    return 0


def cmd_gaps(idx):
    print("NOT COVERED (terms absent from the body of the texts, verified by searching the extracted text; see tests/citation-checks.json):")
    for g in idx["lacunas"]:
        print(f"- {g['termo']} [{g['alvo']}]: {g['nota']}")
    print("\nNOT READ / NOT INSPECTED by this package (may exist in the PDFs; do not use as [from source]):")
    for g in idx["nao_lido"]:
        print(f"- {g['paginas']}: {g['tema']}")
    return 0


def cmd_datado():
    fp = os.path.join(PKG, "references", "datado.md")
    if not os.path.exists(fp):
        print("references/datado.md missing")
        return 1
    for line in io.open(fp, encoding="utf-8"):
        if line.startswith("#") or line.startswith("|"):
            print(line.rstrip())
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("termo", nargs="*")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fonte", choices=["BAAS", "CE2"])
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--datado", action="store_true")
    a = ap.parse_args()
    idx = load()
    if a.page is not None:
        return cmd_page(idx, a.page, a.fonte)
    if a.printed is not None:
        return cmd_printed(idx, a.printed)
    if a.chapters:
        return cmd_chapters(idx)
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
