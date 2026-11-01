#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic lookup of JavaScript TOPICS in the package references, with pages per source.

Usage:
    python -I scripts/js_topic_lookup.py TERM [TERM ...]     # all terms must match (accent- and case-insensitive)
    python -I scripts/js_topic_lookup.py --exact Promise.any
    python -I scripts/js_topic_lookup.py --rebuild           # regenerates js_topic_index.json from references/*.md
    python -I scripts/js_topic_lookup.py --check             # checks whether the index is up to date with references/*.md (exit 1 if not)
    python -I scripts/js_topic_lookup.py --missing           # lists what the sources do NOT cover (verified in tests/)

The index (js_topic_index.json) is DERIVED from the references: each entry is a glossary term, a built-ins table
row or a section title, with the citations `(Spec p.N)`, `(EJpt p.N)`, `(EJ1 p.N)` that appear in THAT row or
section (PDF pages; Spec: printed = PDF - 24; EJpt and EJ1 have no printed numbering). Nothing is invented here: if the
index does not have the term, the answer is NOT COVERED, which does NOT prove that the source does not address the subject
(confirm with Grep in references/ and with js-spec-lookup). Read-only (except --rebuild, which rewrites the JSON), no network.
Exit codes: 0 found; 1 NOT COVERED; 2 usage error.
"""
import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
INDEX = os.path.join(HERE, "js_topic_index.json")
DASH = "[–—-]"
CITE = re.compile(r"\b(Spec|EJpt|EJ1) pp?\.\s*(\d+(?:%s\d+)?(?:\s*[,;]\s*p\.\s*\d+(?:%s\d+)?)*)" % (DASH, DASH))
SKIP = {"INDEX.md"}

# What the sources do NOT cover: each item was checked by searching the text of the PDFs (see tests/citation-checks.json, negatives).
NOT_IN_BOOKS = [
    {"termo": "structuredClone, queueMicrotask, AbortController", "fontes": "EJpt, EJ1 e Spec",
     "nota": "Environment APIs: they do not appear in any of the three sources (negatives N001-N003, N016, N022)."},
    {"termo": "Temporal (API), Intl (API detalhada)", "fontes": "Spec, EJpt, EJ1",
     "nota": "The Spec only refers to ECMA-402 (Spec p.25-26) and only uses 'Temporal' in date grammar names (TemporalDecimalFraction); EJpt and EJ1 do not cover it."},
    {"termo": "TypeScript, React, Vue, Angular, Express, Next.js, Jest", "fontes": "Spec, EJpt, EJ1",
     "nota": "Out of scope; EJpt makes only a passing mention of static types (EJpt p.171)."},
    {"termo": "Array.isArray, localeCompare, Number.EPSILON, replaceAll, response.ok, eval, focusin", "fontes": "EJpt",
     "nota": "They do not appear in EJpt (negatives N004-N010); the Spec defines most of them (use js-spec-lookup)."},
    {"termo": "Promise, JSON.parse, Object.create, querySelector, Symbol, strict mode, arrow, class, const", "fontes": "EJ1",
     "nota": "EJ1 (1st edition) does not include them (negatives N013-N015)."},
    {"termo": "browser/engine support tables, release dates of editions ES2016-ES2026", "fontes": "Spec, EJpt, EJ1",
     "nota": "They do not appear; see references/versoes-e-datado.md (Gaps)."},
]


# Portuguese query words still accepted (the index terms are now English): Portuguese word -> English equivalent.
PT_ALIASES = {
    "fechamento": "closure", "heranca": "inheritance", "prototipo": "prototype", "promessa": "promise",
    "escopo": "scope", "laco": "loop", "excecao": "exception", "matriz": "array", "objeto": "object",
    "funcao": "function", "cadeia": "string", "verbete": "term", "iteracao": "iteration", "erro": "error",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.casefold()).strip()


def expand(spec):
    out = []
    for m in re.finditer(r"(\d+)(?:%s(\d+))?" % DASH, spec):
        a = int(m.group(1))
        b = int(m.group(2) or a)
        out.extend(range(a, b + 1) if b >= a else [a])
    return out


def ranges(pages):
    pages = sorted(set(pages))
    out = []
    for p in pages:
        if out and p == out[-1][1] + 1:
            out[-1][1] = p
        else:
            out.append([p, p])
    return ["%d" % a if a == b else "%d-%d" % (a, b) for a, b in out]


def cites(text):
    res = {"Spec": set(), "EJpt": set(), "EJ1": set()}
    for m in CITE.finditer(text):
        res[m.group(1)].update(expand(m.group(2)))
    return res


def pack(c):
    return {k: ranges(v) for k, v in c.items() if v}


def clean(t):
    return re.sub(r"[`*]", "", t).strip()


def build(write=True):
    entries = []
    for f in sorted(glob.glob(os.path.join(PKG, "references", "*.md"))):
        base = os.path.basename(f)
        if base in SKIP:
            continue
        with open(f, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        heads = []  # (nivel, linha, titulo)
        for i, ln in enumerate(lines, 1):
            m = re.match(r"^(#{2,4})\s+(.*)$", ln)
            if m:
                heads.append((len(m.group(1)), i, m.group(2).strip()))
        # section entries (citations aggregated up to the next heading of equal or lower level)
        for idx, (lvl, i, title) in enumerate(heads):
            end = len(lines)
            for lvl2, j, _ in heads[idx + 1:]:
                if lvl2 <= lvl:
                    end = j - 1
                    break
            c = cites("\n".join(lines[i:end]))
            if any(c.values()):
                entries.append({"termo": clean(title), "tipo": "secao", "arquivo": base, "linha": i, "paginas": pack(c)})
        # glossary terms and table rows
        for i, ln in enumerate(lines, 1):
            term = None
            m = re.match(r"^\s*[-*]\s+\*\*(.+?)\*\*\s*[—:-]", ln)
            if m:
                term, tipo = clean(m.group(1)), "verbete"
            else:
                m = re.match(r"^\|\s*(`[^|]+?`(?:\s*,\s*`[^|]+?`)*)\s*\|", ln)
                if m and not ln.startswith("|---"):
                    term, tipo = clean(m.group(1)), "linha"
            if not term:
                continue
            c = cites(ln)
            if any(c.values()):
                entries.append({"termo": term, "tipo": tipo, "arquivo": base, "linha": i, "paginas": pack(c)})
    data = {
        "aviso": "Index derived from references/*.md by js_topic_lookup.py --rebuild; pages = PDF pages.",
        "entradas": entries,
        "sem_cobertura": NOT_IN_BOOKS,
    }
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if write:
        with open(INDEX, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    return text, len(entries)


KIND_LABEL = {"verbete": "term", "linha": "row", "secao": "section"}


def show(e):
    extra = "  (union of the section citations, not just of the topic)" if e["tipo"] == "secao" else ""
    print("- [%s] %s  (references/%s:%d)%s" % (KIND_LABEL.get(e["tipo"], e["tipo"]), e["termo"], e["arquivo"], e["linha"], extra))
    for sig in ("Spec", "EJpt", "EJ1"):
        if sig in e["paginas"]:
            lst = e["paginas"][sig]
            more = ""
            if len(lst) > 14:
                more = " ... (+%d ranges; open the reference)" % (len(lst) - 14)
                lst = lst[:14]
            print("    %-4s p.%s%s" % (sig, ", ".join(lst), more))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[0] == "--rebuild":
        _, n = build()
        print("index regenerated: %d entries" % n)
        return 0
    if argv[0] == "--check":
        text, n = build(write=False)
        with open(INDEX, encoding="utf-8") as fh:
            same = fh.read() == text
        print("index %s the references (%d entries)" % ("MATCHES" if same else "DIVERGES from", n))
        return 0 if same else 1
    with open(INDEX, encoding="utf-8") as fh:
        data = json.load(fh)
    if argv[0] == "--missing":
        for it in data["sem_cobertura"]:
            print("- %s [%s]: %s" % (it["termo"], it["fontes"], it["nota"]))
        return 0
    exact = False
    if argv[0] == "--exact":
        exact = True
        argv = argv[1:]
    if not argv:
        print(__doc__)
        return 2
    q = [norm(t) for t in argv]
    q = [(t, PT_ALIASES[t]) if t in PT_ALIASES else (t,) for t in q]
    hits = []
    for e in data["entradas"]:
        key = norm(e["termo"])
        if exact:
            if norm(" ".join(argv)) in [norm(x) for x in re.split(r"\s*,\s*", e["termo"])] or key == norm(" ".join(argv)):
                hits.append(e)
        elif all(any(a in key for a in alts) for alts in q):
            hits.append(e)
    order = {"verbete": 0, "linha": 1, "secao": 2}
    hits.sort(key=lambda e: (order[e["tipo"]], len(e["termo"]), e["arquivo"], e["linha"]))
    if not hits:
        print("NOT COVERED in the index for: %s" % " ".join(argv))
        print("This does NOT prove that the sources do not address the subject: run Grep in references/ and use js-spec-lookup (Spec).")
        miss = [it for it in data["sem_cobertura"] if any(a in norm(it["termo"]) for alts in q for a in alts)]
        for it in miss:
            print("Verified as absent: %s [%s]: %s" % (it["termo"], it["fontes"], it["nota"]))
        return 1
    print("# %d entry(ies); PDF pages (Spec: printed = PDF - 24). Check the term on the page before citing." % len(hits))
    for e in hits[:15]:
        show(e)
    if len(hits) > 15:
        print("... +%d entries (refine the terms)" % (len(hits) - 15))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
