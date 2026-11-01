# -*- coding: utf-8 -*-
"""
build_term_index.py - generates scripts/sbr_terms.json, the TERM INDEX of the Reference text (Spring Boot 2.7.18).

Purpose: sbr_lookup.py can only say "the Reference does not cover X" if X has no occurrence in this index
(or if it is in the curated out-of-scope list, scripts/sbr_curated.json). The index keeps ONLY words/word pairs and
the PDF pages where they occur (no prose from the book, no sentences).

Input  : the text extracted per page (marker "=== PAGE N ===") Spring-Boot-Reference.txt (not shipped in the package).
Output : scripts/sbr_terms.json
  {"fonte":..., "paginas":882, "unigramas":{palavra:"p1,p3-5"}, "bigramas":{"par de palavras":"p1,p3-5"}}
Normalization: lowercase; "@Foo" -> "foo"; tokens with . - _ are indexed whole and also split into parts
("circuit-breaker" -> "circuit-breaker", "circuit", "breaker"); pairs (bigrams) over the sequence of parts;
pairs on more than 40 pages and pairs made only of stop words (of the, in a...) are discarded (noise).

Usage: python -I scripts/build_term_index.py --src PATH/scratch/frameworks [--out scripts/sbr_terms.json]
Stdlib only, no network. Rerun if the source text changes; run_script_tests.py checks the count hash.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_FILE = "Spring-Boot-Reference.txt"
STOP = set("a an the of in on to for and or is are be by as at it its this that with from can you your if not "
           "do does we has have will may also any all one more other such these those which when what how than "
           "then so but only use used using see here there their they them should must would could into out up "
           "no yes".split())
MAX_PAGES_BIGRAM = 40
TOKEN = re.compile(r"[a-z0-9]+(?:[._\-][a-z0-9]+)*")


def norm_text(s):
    s = s.lower()
    for a in ("‘", "’", "�", "“", "”"):
        s = s.replace(a, "'")
    for a in ("‐", "‑", "–", "—", "−"):
        s = s.replace(a, "-")
    return s.replace("\xa0", " ").replace("​", "")


def tokens(text):
    """returns (list of whole tokens, list of parts in text order)."""
    whole = []
    parts = []
    for t in TOKEN.findall(norm_text(text)):
        whole.append(t)
        ps = re.split(r"[._\-]", t)
        parts.extend(p for p in ps if p)
        if len(ps) > 1:
            whole.extend(p for p in ps if p)
    return whole, parts


def pack(pages):
    """compacts a page list into 'a,b-c,d'."""
    ps = sorted(pages)
    out = []
    i = 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[j] + 1:
            j += 1
        out.append(str(ps[i]) if i == j else "%d-%d" % (ps[i], ps[j]))
        i = j + 1
    return ",".join(out)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder with Spring-Boot-Reference.txt")
    ap.add_argument("--out", default=os.path.join(HERE, "sbr_terms.json"))
    a = ap.parse_args()
    pages = load_pages(os.path.join(a.src, SRC_FILE))
    uni, bi = {}, {}
    for n, s in pages.items():
        whole, parts = tokens(s)
        for w in whole:
            uni.setdefault(w, set()).add(n)
        for x, y in zip(parts, parts[1:]):
            if x in STOP and y in STOP:
                continue
            bi.setdefault(x + " " + y, set()).add(n)
    bi = {k: v for k, v in bi.items() if len(v) <= MAX_PAGES_BIGRAM}
    data = {
        "fonte": "Spring Boot Reference Documentation 2.7.18 (SBR); pages = PDF pages",
        "paginas": len(pages),
        "unigramas": {k: pack(v) for k, v in sorted(uni.items())},
        "bigramas": {k: pack(v) for k, v in sorted(bi.items())},
    }
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print("pages=%d unigrams=%d bigrams=%d -> %s (%d bytes)" % (
        len(pages), len(uni), len(bi), a.out, os.path.getsize(a.out)))


if __name__ == "__main__":
    main()
