# -*- coding: utf-8 -*-
"""
privacy_lookup.py - look up the LGPD (Lei Geral de Proteção de Dados, Brazil's General Data Protection Law; compiled text)
and NIST IR 8062 by article/topic, with PDF page numbers.

Usage (Python 3, stdlib, no network, read-only; run with `python -I`). Queries accept Portuguese terms (the
source language) and common English terms:
  python -I scripts/privacy_lookup.py "consentimento"                 # search by topic/term in both sources
  python -I scripts/privacy_lookup.py "art. 7 inciso IX"              # search by article (and unit)
  python -I scripts/privacy_lookup.py --art 18 [--unit III]           # entries of the article
  python -I scripts/privacy_lookup.py --src LGPD|NIST8062 "termo"     # restrict to one source
  python -I scripts/privacy_lookup.py --page 17 --src LGPD            # what is on the PDF page
  python -I scripts/privacy_lookup.py --page 26 --src NIST8062        # converts PDF -> printed page and lists topics
  python -I scripts/privacy_lookup.py --printed 18 --src NIST8062     # printed -> PDF (body: PDF = printed + 8)
  python -I scripts/privacy_lookup.py --amendments [--art 52]         # amendment notes of the compiled text (LGPD)
  python -I scripts/privacy_lookup.py --chapters                      # LGPD chapter map
  python -I scripts/privacy_lookup.py --themes                        # list of themes
  python -I scripts/privacy_lookup.py --gaps                          # terms verified ABSENT from each source
  [--json] prints JSON.

Page convention: PDF page (marker "=== PAGE N ==="). LGPD: there is no printed numbering of its own.
NIST8062: printed = PDF - 8 in the body (PDF 9 = printed 1).
When nothing is found it prints "NOT COVERED". This script gives no legal advice.
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
INDEX = os.path.join(HERE, "privacy_index.json")
STOP = set("a o as os de da do das dos e em no na nos nas um uma para por com sem que se ao aos ou the of and to in on for with is are lgpd nist qual quais como quando onde lei artigo inciso paragrafo sobre pagina paginas what which how when where law article item paragraph about page pages does do can".split())
# English query terms -> Portuguese terms of the source text (the indexes are in Portuguese)
ALIAS = [
    ("legitimate interest", "legitimo interesse"), ("sensitive data", "sensiveis"), ("data subject rights", "direitos do titular"),
    ("data subject", "titular"), ("international transfer", "transferencia internacional"), ("cross-border", "transferencia internacional"),
    ("impact report", "relatorio de impacto ripd"), ("impact assessment", "relatorio de impacto ripd"), ("dpia", "relatorio de impacto ripd"),
    ("public authority", "poder publico"), ("automated decision", "decisoes automatizadas"), ("data breach", "incidentes seguranca"),
    ("security incident", "incidentes seguranca"), ("incident", "incidentes seguranca"), ("consent", "consentimento"),
    ("anonymization", "anonimizacao"), ("anonymisation", "anonimizacao"), ("pseudonymization", "anonimizacao pseudonimizacao"),
    ("children", "criancas adolescentes"), ("sanctions", "sancoes"), ("sanction", "sancoes"), ("penalty", "sancoes"), ("fine", "sancoes multa"),
    ("controller", "controlador"), ("processor", "operador"), ("dpo", "encarregado"), ("data protection officer", "encarregado"),
    ("security", "seguranca"), ("deletion", "eliminacao"), ("erasure", "eliminacao"), ("purpose", "finalidade"), ("necessity", "necessidade"),
    ("data minimization", "necessidade"), ("records of processing", "registro operacoes"), ("portability", "portabilidade"),
    ("legal basis", "bases legais hipoteses tratamento"), ("legal bases", "bases legais hipoteses tratamento"), ("retention", "termino tratamento eliminacao"),
    ("scope", "escopo aplicacao"), ("liability", "responsabilidade ressarcimento"), ("governance", "governanca boas praticas"),
    ("effective date", "vigencia"), ("principles", "principios"),
]
AVISO = "Notice: support material; not legal advice. Refer to a lawyer/the encarregado (DPO) and check the current version of the law and ANPD (Autoridade Nacional de Proteção de Dados, the national data protection authority) regulations."


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9§./ -]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load():
    with io.open(INDEX, "r", encoding="utf-8") as f:
        return json.load(f)


def stem(w):
    if len(w) > 4 and w.endswith("oes"):
        return w[:-3] + "ao"
    if len(w) > 4 and w.endswith("ais"):
        return w[:-3] + "al"
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def expand(qn):
    """Appends the Portuguese equivalents of English terms found in the (normalized) query."""
    extra = []
    for en, pt in ALIAS:
        if re.search(r"\b%s\b" % re.escape(en), qn):
            extra.append(pt)
    return (qn + " " + " ".join(extra)).strip() if extra else qn


def toks(q):
    return [stem(t) for t in expand(norm(q)).split() if len(t) >= 2 and t not in STOP]


def score(e, qn, qt):
    kw = [norm(k) for k in e.get("kw", [])]
    topic = norm(e["id"])
    summ = norm(e["resumo"])
    temas = [norm(t) for t in e.get("temas", [])]
    sw = set(stem(w) for w in summ.split())
    sc = 0
    best = 0
    for k in kw:
        if qn and (qn == k):
            best = max(best, 12)
        elif qn and (qn in k or k in qn) and len(k) >= 4:
            best = max(best, 8)
    sc += best
    if qn and any(qn == t for t in temas):
        sc += 6
    kws = set(stem(w) for k in kw for w in k.split())
    for t in qt:
        if t in kws:
            sc += 3
        if t in sw:
            sc += 1
        if any(t in tw for tw in temas):
            sc += 2
        if t in stem(topic):
            sc += 2
    return sc


def parse_art(q):
    m = re.search(r"\bart(?:icle|igo)?s?\.?\s*(\d+)(?:\s*-?\s*([a-z])\b)?", norm(q))
    if not m:
        return None, None
    art = m.group(1) + ("-" + m.group(2).upper() if m.group(2) else "")
    rest = norm(q)[m.end():]
    mu = re.search(r"(?:inciso|inc\.?|item)\s*([ivxl]+)\b", rest)
    mp = re.search(r"(?:§|paragrafo|paragraph|par\.?)\s*(\d+)", rest)
    unit = None
    if mu:
        unit = mu.group(1).upper()
    elif mp:
        unit = "§ " + mp.group(1)
    return art, unit


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}


def roman(s):
    v = 0
    prev = 0
    for ch in reversed(s):
        x = ROMAN.get(ch, 0)
        v = v - x if x < prev else v + x
        prev = max(prev, x)
    return v


def unit_matches(entry_id, unit):
    """Matches a unit (Roman-numeral inciso or § N) against the entry id (which may be a range, e.g. 'IV-VII', '§§ 1º-5º')."""
    tail = entry_id.split(",", 1)[1] if "," in entry_id else ""
    if not unit:
        return True
    if unit.startswith("§"):
        n = int(unit.split()[1])
        for a, b in re.findall(r"(\d+)º?\s*-\s*(\d+)º?", tail):
            if int(a) <= n <= int(b):
                return True
        return bool(re.search(r"§\s*%dº" % n, tail) or re.search(r"§§[^;]*\b%dº" % n, tail))
    target = roman(unit)
    for m in re.finditer(r"\b([IVXL]+)(?:\s*(?:-|a|e)\s*([IVXL]+))?\b", tail):
        a = roman(m.group(1))
        b = roman(m.group(2)) if m.group(2) else a
        if a <= target <= b:
            return True
    return False


def fmt_pages(p):
    return "p." + ("-".join(str(x) for x in (p if len(p) < 3 else [p[0], p[-1]])) if len(p) > 1 else str(p[0]))


def show(entries, as_json, label=None):
    if as_json:
        print(json.dumps([{k: e[k] for k in ("src", "id", "pages", "resumo", "ref")} for e in entries], ensure_ascii=False, indent=1))
        return
    for e in entries:
        src = "LGPD" if e["src"] == "LGPD" else "NIST8062"
        print("[%s] %s (%s%s)" % (src, e["id"], "PDF " if src else "", fmt_pages(e["pages"])))
        print("   " + e["resumo"])
        print("   -> references/%s" % e["ref"])
    print(AVISO)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*")
    ap.add_argument("--src", choices=["LGPD", "NIST8062"])
    ap.add_argument("--art")
    ap.add_argument("--unit")
    ap.add_argument("--page", type=int)
    ap.add_argument("--printed", type=int)
    ap.add_argument("--amendments", action="store_true")
    ap.add_argument("--chapters", action="store_true")
    ap.add_argument("--themes", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    d = load()
    E = d["entries"]
    if a.src:
        E = [e for e in E if e["src"] == a.src]

    if a.chapters:
        for c in d["capitulos"]:
            print("Chap. %-4s Art. %-7s PDF p.%s-%s  %s" % (c["cap"], c["arts"], c["paginas"][0], c["paginas"][1], c["titulo"]))
        return 0
    if a.themes:
        for k, v in d["temas"].items():
            print("%-30s %s" % (k, v))
        return 0
    if a.gaps:
        print("Terms VERIFIED ABSENT from the text of each source (whole-word search, accent-insensitive; see tests/citation-checks.json):")
        for s, terms in d["gaps"].items():
            if a.src and s != a.src:
                continue
            print("  %s: %s" % (s, "; ".join(terms)))
        print("LGPD note: 'encarregado' is the term used by the law (DPO does not appear); 'relatório de impacto' is the term used by the law (DPIA/avaliação de impacto do not appear).")
        print("NIST note: 'Privacy Framework' appears only as the ISO Privacy Framework (p.16 note 25, p.21), not the NIST Privacy Framework. All of this is NOT COVERED in the sources; answers about them are [extrapolation].")
        return 0
    if a.amendments:
        rows = d["amendments"]
        if a.art:
            rows = [r for r in rows if r["art"] == a.art or a.art in r["art"].replace(" a ", " ").split()]
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print("Amendment notes as given in the compiled PDF text (check the current version; [DATED] for what changed later):")
            for r in rows:
                lei = ("Lei %s/%s" % (r["lei"], r["ano"])) if r["lei"] else "(no law cited)"
                print("  Art. %-12s %-30s p.%-2s %-45s %s" % (r["art"], r["unit"], r["page"], r["tipo"], lei))
        return 0
    if a.page is not None:
        src = a.src or "LGPD"
        hits = [e for e in d["entries"] if e["src"] == src and a.page in range(e["pages"][0], e["pages"][-1] + 1) and a.page in e["pages"]]
        if src == "NIST8062":
            if a.page >= 9:
                print("NIST8062 PDF p.%d = printed %d" % (a.page, a.page - 8))
            else:
                print("NIST8062 PDF p.%d = front matter in Roman numerals (p.4 = ii; p.8 = vi)" % a.page)
        if not hits:
            print("NOT COVERED by the index for %s p.%d (the page may exist; check the text)." % (src, a.page))
        else:
            show(hits, a.json)
        return 0
    if a.printed is not None:
        src = a.src or "NIST8062"
        if src != "NIST8062":
            print("The LGPD PDF has no printed numbering of its own; use the PDF page.")
            return 0
        print("NIST8062 printed %d = PDF p.%d (body; valid for printed 1-41)" % (a.printed, a.printed + 8))
        return 0

    q = " ".join(a.query) if a.query else ""
    art, unit = (a.art, a.unit) if a.art else parse_art(q)
    if unit and re.fullmatch(r"§?\s*\d+º?", unit.strip()):
        unit = "§ " + re.sub(r"\D", "", unit)
    if unit and not unit.startswith("§"):
        unit = unit.strip().upper()
    if a.art:
        art = re.sub(r"^art\.?\s*", "", a.art.strip(), flags=re.I).upper()
    if art:
        hits = [e for e in E if e["src"] == "LGPD" and art in e.get("arts", [])]
        if unit:
            hits = [e for e in hits if unit_matches(e["id"], unit)]
        if hits:
            show(hits, a.json)
            return 0
        print("NOT COVERED by the index for Art. %s%s. The article may exist in the text; check the compiled law." % (art, (" " + unit) if unit else ""))
        return 0
    if not q:
        ap.print_help()
        return 0
    qn = norm(q)
    qt = toks(q)
    ranked = sorted(((score(e, qn, qt), e) for e in E), key=lambda x: -x[0])
    ranked = [(s, e) for s, e in ranked if s >= 3][: a.top]
    if not ranked:
        print("NOT COVERED in the collection for: %r. If the topic is in neither the LGPD (compiled text) nor NIST IR 8062, any answer is [extrapolation]." % q)
        print("Use --gaps to see terms verified as absent.")
        return 0
    show([e for _, e in ranked], a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
