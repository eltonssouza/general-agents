# -*- coding: utf-8 -*-
"""
build_ref_index.py - generates scripts/ref_terms.json, the TERM INDEX OF THE SUMMARIES: the normalized text of each excerpt (list item,
paragraph, table row) of the references/*.md files, split into two classes:

  b = summary BODY: text of a "[from source]", "[inference]", "[derived]", "[DATED]" section or an unlabeled one (glossary, procedures,
      cases) that really summarizes the content of the sources. It is the ONLY class that can make a term COVERED in relational_lookup.py.
  p = POINTER/MAP: the whole INDEX.md (except the boundary sections), metadata blocks at the top of each file (lines with '>'),
      "navigation map", "where to open", "pointer" sections, and any line that says "pointer only"/"no summary" (or their pt-BR forms). A term that only
      appears here is POINTER ONLY.
  (discarded) "[extrapolação]" sections, "what the sources do NOT say", "boundary" and lines labeled [extrapolação]: they are not content
      of the sources; a term that only appears there is neither covered nor a pointer.

(The section markers and labels above are the literal strings used inside references/*.md; the classifier recognizes both the English and the original pt-BR headings.)
The index is generated ONLY from the content of the references (not from the PDF source text; build_term_index.py does that). No file
name, topic id or topic title: the lookup matches the whole term (delimited phrase) against the text of the excerpts.
Each excerpt keeps the pages cited (SIGLA p.N-M) on its own line (or, failing that, in the section title), to link the excerpt to the
curated topics.

Usage (from the package root):
  python -I scripts/build_ref_index.py [--refs references] [--out scripts/ref_terms.json]
Deterministic, no network. The generated file is versioned with the package (tests/run_script_tests.py checks that it is reproducible).
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

VERSION = "1.0"
SIGLAS = ("ANTI-INJ", "ANTI-TREE", "ANTI-INT", "ANTI-TOC", "ARCH", "PG16", "REDBK")
CITE_RE = re.compile(r"\b(" + "|".join(SIGLAS) + r")\s+p\.(\d+)(?:\s*[-–]\s*(\d+))?((?:\s*[,;]\s*p\.\d+(?:\s*[-–]\s*\d+)?)*)")
EXTRA_RE = re.compile(r"p\.(\d+)(?:\s*[-–]\s*(\d+))?")
LIT_RE = re.compile(r"[A-Za-z_][\w.]*\(\s*\*\s*\)")


def norm_match(s):
    """matching normalization: no accents, lowercase; everything that is not [a-z0-9_] becomes a space; spaces collapsed."""
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return " ".join(re.sub(r"[^a-z0-9_]+", " ", s).split())


def classify_heading(h):
    n = norm_match(h)
    if re.search(r"nao (dizem|diz|trazem|traz|vem|vêm)\b|\bfronteira\b|\blimites$|\bdo(es)? not (say|contain|bring)\b|\bboundary\b|\blimits$", n):
        return "n"
    if "[extrapola" in h.lower() or n.startswith("extrapolacao") or n.startswith("extrapolation"):
        return "n"
    if re.search(r"ponteiro|mapa de navegacao|mapa de capitulos|mapa de cobertura|quando abrir|onde cada tema|onde ficou cada coisa|^scripts\b|pointer|navigation map|chapter map|coverage map|when to open|where each (topic|thing)|^\d+\w*\s+scripts\b", n):
        return "p"
    return "b"


def pages_of(text):
    """{sigla: 'p.1-2, p.9'} with the pages cited in the text."""
    out = {}
    for m in CITE_RE.finditer(text):
        specs = [(m.group(2), m.group(3))] + EXTRA_RE.findall(m.group(4) or "")
        for a, b in specs:
            out.setdefault(m.group(1), set()).update(range(int(a), int(b or a) + 1))
    return _fmt(out)


def _fmt(out):
    res = {}
    for sig, ps in out.items():
        ps = sorted(ps)
        rng, start, prev = [], None, None
        for p in ps:
            if start is None:
                start = prev = p
            elif p == prev + 1:
                prev = p
            else:
                rng.append((start, prev))
                start = prev = p
        rng.append((start, prev))
        res[sig] = ", ".join("p.%d" % a if a == b else "p.%d-%d" % (a, b) for a, b in rng)
    return res


def strip_md(s):
    return s.replace("**", "").replace("`", "").replace("*", " ")


def lead_of(s):
    """subject of the excerpt: text (without markdown or citations) up to the first ':' if it comes within the first 80 characters; otherwise, the first 50."""
    t = strip_md(s).lstrip("-*>| ").strip()
    t = " ".join(CITE_RE.sub("", t).split())
    i = t.find(":")
    return t[:i] if 0 <= i <= 80 else t[:50]


def no_cites(s):
    """text without the citations (SIGLA p.N): the pages stay in the 'pg' field; avoids truncated citations in the displayed excerpts."""
    s = CITE_RE.sub("", s)
    s = re.sub(r"\(\s*[;,]?\s*\)", "", s)
    return " ".join(s.split())


def chunks_of(fn, text):
    """list of dicts {k, h, pg, t, x} for a reference file."""
    is_index = fn.upper().startswith("INDEX")
    out = []
    cls = {}            # level -> class
    cur_h, cur_pages = "", {}
    seen_h2 = False
    in_fence = False
    sec = 0
    sec_pages = {}      # section -> {sigla: {pages}} (union of the section's citations, for excerpts without their own citation)
    for line in text.splitlines():
        raw = line.rstrip()
        s = raw.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s) if not in_fence else None
        if m:
            lvl = len(m.group(1))
            c = classify_heading(m.group(2))
            if lvl >= 3 and c == "b":
                c = cls.get(lvl - 1, cls.get(2, "b"))
            if lvl == 1:
                c = "b"
            cls[lvl] = c
            for k in [k for k in cls if k > lvl]:
                del cls[k]
            if lvl >= 2:
                seen_h2 = True
            cur_h = no_cites(strip_md(m.group(2))).strip()
            cur_pages = pages_of(m.group(2))
            sec += 1
            continue
        if not s or s == "---" or re.match(r"^\|[\s:|-]+\|$", s):
            continue
        eff = cls.get(max(cls) if cls else 1, "b") if cls else "b"
        if not seen_h2:
            kind = "p" if s.startswith(">") else None      # metadata block at the top
            if kind is None:
                continue
        else:
            kind = eff
            if is_index and kind == "b":
                kind = "p"                                 # INDEX.md is a map
            if s.startswith(">") and kind == "b" and re.search(r"ponteiro|sem resumo|pointer|no summary|,\s*not summari[sz]ed here", s, re.I):
                kind = "p"
        if kind == "b":
            if "[extrapola" in s.lower():
                kind = "n"
            elif re.search(r"s[oó] ponteiro|sem resumo|n[aã]o resumid|pointer only|only a pointer|no summary|,\s*not summari[sz]ed here", s, re.I):
                kind = "p"
        if kind == "n":
            continue
        t = norm_match(CITE_RE.sub(" ", s))
        if not t:
            continue
        own = pages_of(s)
        for sig, spec in (own or cur_pages).items():
            for a, b in EXTRA_RE.findall(spec):
                sec_pages.setdefault(sec, {}).setdefault(sig, set()).update(range(int(a), int(b or a) + 1))
        x = no_cites(strip_md(s).lstrip("-*>| "))[:150]
        item = {"k": kind, "h": cur_h[:80], "pg": own, "t": t, "x": x, "l": norm_match(lead_of(s)),
                "hn": norm_match(cur_h) if kind == "b" else "", "_sec": sec}
        lit = sorted(set(re.sub(r"\s+", "", m.lower()) for m in LIT_RE.findall(s.replace("`", "").replace("**", ""))))
        if lit:
            item["lit"] = lit                              # literal calls with (*), such as count(*): the normalized text loses the symbol
        out.append(item)
    for c in out:
        sp = sec_pages.get(c.pop("_sec"), {})
        if not c["pg"] and sp:
            c["pg"] = _fmt(sp)
    return out


def build(refs_dir):
    result = {"_meta": {
        "version": VERSION,
        "generator": "scripts/build_ref_index.py",
        "note": "Indice de termos gerado do CONTEUDO dos resumos em references/*.md (nao do texto-fonte dos PDFs). k=b: corpo de resumo "
                "(unica classe que torna um termo COBERTO); k=p: ponteiro/mapa (SO PONTEIRO). Secoes [extrapolacao], 'nao dizem' e "
                "'fronteira' sao descartadas.",
        "fingerprint": {},
    }, "files": {}}
    for fn in sorted(os.listdir(refs_dir)):
        if not fn.endswith(".md"):
            continue
        path = os.path.join(refs_dir, fn)
        with open(path, "rb") as f:
            data = f.read()
        result["_meta"]["fingerprint"][fn] = hashlib.sha1(data).hexdigest()[:12]
        result["files"][fn] = chunks_of(fn, data.decode("utf-8"))
    return result


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--refs", default=os.path.join(os.path.dirname(here), "references"))
    ap.add_argument("--out", default=os.path.join(here, "ref_terms.json"))
    a = ap.parse_args()
    res = build(a.refs)
    nb = sum(1 for v in res["files"].values() for c in v if c["k"] == "b")
    npt = sum(1 for v in res["files"].values() for c in v if c["k"] == "p")
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        f.write("\n")
    print("files=%d body excerpts=%d pointer excerpts=%d" % (len(res["files"]), nb, npt))
    print("wrote %s (%d bytes)" % (a.out, os.path.getsize(a.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
