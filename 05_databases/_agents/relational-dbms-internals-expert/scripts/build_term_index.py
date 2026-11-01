# -*- coding: utf-8 -*-
"""
build_term_index.py - generates scripts/source_terms.json, a COMPACT INVERTED INDEX of terms -> PDF pages, from the
text extracted from the sources (the same .txt files, with "=== PAGE N ===" markers, used by tests/verify_citations.py;
use tests/extract_pdfs.py to produce them).

What it is for: relational_lookup.py uses this index to tell three situations apart (COVERED / POINTER ONLY / NOT COVERED)
without depending only on the curated topics of relational_index.json. The absence of a term from the topic index is NOT proof
that the sources do not cover the subject; the term index is the second line of verification.

How the index is built (deterministic, no network, read-only on the sources):
  1. normalize the text (ligatures fi/fl/ff, accents, lowercase);
  2. tokens = sequences [a-z][a-z0-9_]{2,}; identifiers with "_" (pages_per_range) are kept whole AND split into parts;
     the simple plural "-s" is removed (light stem);
  3. per source, terms that appear in more than MAX_DF_RATIO of the pages (and in more than MAX_DF_MIN pages) are "common":
     they keep no pages (they become stopwords of that source);
  4. the pages of each term are written as ranges ("5-7,9").
Usage:
  python -I scripts/build_term_index.py --src <folder with the extracted .txt files> [--out scripts/source_terms.json]
The generated file is versioned with the package (the "generator" and "fingerprint" fields record the origin).
"""
import argparse
import hashlib
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

FILES = {
    "ARCH": "Architecture-of-a-Database-System.txt",
    "PG16": "PostgreSQL-16-Docs.txt",
    "REDBK": "Readings-in-Database-Systems-RedBook-5th.txt",
    "ANTI-INJ": "SQL-Antipatterns-injection-chapter.txt",
    "ANTI-TREE": "SQL-Antipatterns-trees-chapter.txt",
    "ANTI-INT": "SQL-Antipatterns-introduction-chapter.txt",
    "ANTI-TOC": "SQL-Antipatterns-toc-chapter.txt",
}
MAX_DF_RATIO = 0.06   # term in more than 6% of the source pages (and in more than MAX_DF_MIN pages) = "common"
MAX_DF_MIN = 12
VERSION = "1.0"

TOKEN_RE = re.compile(r"[a-z][a-z0-9_]{2,}")
LIGS = (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff"), ("ﬃ", "ffi"), ("ﬄ", "ffl"))


def norm_text(s):
    for a, b in LIGS:
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def stem(t):
    if len(t) > 4 and t.endswith("s") and not t.endswith("ss") and not t.endswith("us") and not t.endswith("is"):
        return t[:-1]
    return t


def tokens_of(text):
    """normalized tokens of a text (also used by relational_lookup.py with the same rule)."""
    out = []
    for m in TOKEN_RE.finditer(norm_text(text)):
        t = m.group(0).strip("_")
        if len(t) < 3:
            continue
        out.append(stem(t))
        if "_" in t:
            for part in t.split("_"):
                if len(part) >= 3:
                    out.append(stem(part))
    return out


def load_pages(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def ranges(pages):
    pages = sorted(pages)
    out, start, prev = [], None, None
    for p in pages:
        if start is None:
            start = prev = p
        elif p == prev + 1:
            prev = p
        else:
            out.append((start, prev))
            start = prev = p
    if start is not None:
        out.append((start, prev))
    return ",".join(str(a) if a == b else "%d-%d" % (a, b) for a, b in out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--out", default=os.path.join(here, "source_terms.json"))
    a = ap.parse_args()
    result = {"_meta": {
        "version": VERSION,
        "generator": "scripts/build_term_index.py",
        "page_convention": "Paginas = paginas do PDF (marcadores === PAGE N ===). ARCH impressa = PDF+140; PG16 impressa = PDF-38.",
        "max_df_ratio": MAX_DF_RATIO,
        "max_df_min": MAX_DF_MIN,
        "note": "Indice de OCORRENCIA de termos (sem semantica). Presenca de um termo numa pagina nao significa que a pagina o explique; "
                "ausencia de um termo aqui significa apenas 'sem ocorrencia textual nas fontes extraidas' (confira sinonimos).",
        "pages_per_source": {},
        "fingerprint": {},
    }, "sources": {}}
    for sig, fn in FILES.items():
        path = os.path.join(a.src, fn)
        pages = load_pages(path)
        n = len(pages)
        result["_meta"]["pages_per_source"][sig] = n
        result["_meta"]["fingerprint"][sig] = hashlib.sha1(open(path, "rb").read()).hexdigest()[:12]
        post = {}
        for pno, text in pages.items():
            for t in set(tokens_of(text)):
                post.setdefault(t, set()).add(pno)
        limit = max(MAX_DF_MIN, int(n * MAX_DF_RATIO))
        common = sorted(t for t, ps in post.items() if len(ps) > limit)
        terms = {t: ranges(ps) for t, ps in sorted(post.items()) if len(ps) <= limit}
        result["sources"][sig] = {"pages": n, "df_limit": limit, "common": common, "terms": terms}
        print("%-10s pages=%5d terms=%7d common=%5d" % (sig, n, len(terms), len(common)))
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    print("wrote %s (%d bytes)" % (a.out, os.path.getsize(a.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
