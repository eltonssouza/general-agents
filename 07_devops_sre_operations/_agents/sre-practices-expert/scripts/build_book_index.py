# -*- coding: utf-8 -*-
"""
build_book_index.py - builds the inverted index (term -> PDF pages) from the TEXT of the Google SRE Book (2016)
extracted per page (markers '=== PAGE N ==='). Generates/checks book_term_index.json.

Purpose: sre_lookup.py uses this index to AVOID saying 'the book does not cover this topic' when the term exists
in the book. Lookup output levels: COVERED (summary+pages in the package), POINTER ONLY (the book has the term on
pages X, the package does not summarize it) and NOT COVERED (curated list of things outside the book OR 'not found in the index', which does not prove absence).

Usage:
  python -I build_book_index.py --text <Google-SRE-Book.txt> [--out book_term_index.json]   # generate
  python -I build_book_index.py --text <Google-SRE-Book.txt> --check                         # check the versioned JSON
Round 4: the lookup now requires the topic summary to address the term (COVERED); this index remains the source of POINTER ONLY and
of real absence (NOT COVERED). Deterministic (no date/time in the JSON): the same text generates the same file byte for byte.
Reads the text only; offline. The JSON stores only terms and page numbers (no book excerpts).

Tokenization: NFKC (resolves ligatures such as 'ff'), lowercase, accent-free; tokens [a-z0-9][a-z0-9+_-]*;
discarded: 1-letter tokens, digit-only tokens longer than 4 digits, and English stopwords; words that occur on
more than MAXPAGES pages become 'common' (count only, no page list). Pages are PDF pages (printed = N-12).
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata

VERSION = "1.2"  # round 8: token n+0 (note 25, p.62); round 4: regenerated after the new topics (p.55, 189, 193, 236, 268, 296-297...); tokenization unchanged
MAXPAGES = 90
STOP = set("""
a about above after again against all also am an and any are as at be because been before being below between both
but by can could did do does doing down during each few for from further had has have having he her here hers him his
how i if in into is it its itself just me more most my no nor not now of off on once only or other our out over own
same she should so some such than that the their theirs them then there these they this those through to too under
until up very was we were what when where which while who whom why will with would you your yours may might must shall
us one two per via vs etc eg ie
""".split())


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


TOK = re.compile(r"[a-z0-9][a-z0-9+_\-]*")
NPLUS = re.compile(r"(?<![a-z0-9])n\s*\+\s*(\d)")  # round 8: 'N + 0' (zero redundancy) becomes the token 'n+0'


def tokens(text):
    for t in TOK.findall(NPLUS.sub(r"n+\1", norm(text))):
        t = t.strip("-_+") if not t.endswith("++") else t.rstrip("-_")
        if len(t) < 2:
            continue
        if t.isdigit() and len(t) > 4:
            continue
        if t in STOP:
            continue
        yield t
        # alphabetic parts of hyphen/underscore tokens (least-loaded -> least, loaded)
        if "-" in t or "_" in t:
            for p in re.split(r"[-_]", t):
                if len(p) >= 2 and p not in STOP and not (p.isdigit() and len(p) > 4):
                    yield p
        # 'sonnet++' also indexes 'sonnet'
        if t.endswith("++"):
            yield t.rstrip("+")


def load_pages(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}, raw


def build(path):
    pages, raw = load_pages(path)
    inv = {}
    for n in sorted(pages):
        for t in set(tokens(pages[n])):
            inv.setdefault(t, set()).add(n)
    terms = {}
    common = {}
    for t in sorted(inv):
        ps = sorted(inv[t])
        if len(ps) > MAXPAGES:
            common[t] = len(ps)
        else:
            terms[t] = ps
    meta = {
        "version": VERSION,
        "source": "Site Reliability Engineering (Google/O'Reilly, 2016), text extracted per page",
        "page_convention": "PDF pages; printed = N-12",
        "source_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "pages": len(pages),
        "max_pages_per_term": MAXPAGES,
        "tokenization": "NFKC, lowercase, no accents, tokens [a-z0-9][a-z0-9+_-]*; hyphen/underscore also index the parts; "
                        "no English stopwords; digit-only tokens of more than 4 digits dropped",
        "n_terms": len(terms),
        "n_common_terms": len(common),
        "note": "term index of the book text; absence here = no occurrence in the extracted text (figures/images are not included)",
    }
    return {"_meta": meta, "common": common, "terms": terms}


def dump(data):
    # pages as a compact list, one line per term (readable diff)
    lines = ["{", ' "_meta": ' + json.dumps(data["_meta"], ensure_ascii=False, sort_keys=True) + ",",
             ' "common": ' + json.dumps(data["common"], ensure_ascii=False, sort_keys=True) + ",", ' "terms": {']
    items = sorted(data["terms"].items())
    for i, (t, ps) in enumerate(items):
        lines.append("  %s: %s%s" % (json.dumps(t, ensure_ascii=False), json.dumps(ps, separators=(",", ":")),
                                     "," if i < len(items) - 1 else ""))
    lines.append(" }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--text", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--out", default=os.path.join(here, "book_term_index.json"))
    ap.add_argument("--check", action="store_true", help="check that the versioned JSON equals the one generated from the text")
    a = ap.parse_args(argv)
    data = build(a.text)
    text = dump(data)
    if a.check:
        with open(a.out, encoding="utf-8") as f:
            cur = f.read()
        if cur == text:
            print("OK: %s matches the text (%d terms, %d common, %d pages, sha256 %s...)" % (
                os.path.basename(a.out), data["_meta"]["n_terms"], data["_meta"]["n_common_terms"],
                data["_meta"]["pages"], data["_meta"]["source_sha256"][:12]))
            return 0
        print("FAIL: %s differs from the index generated from the text; regenerate with --text (without --check)" % a.out)
        return 1
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("generated %s: %d terms, %d common, %d pages" % (a.out, data["_meta"]["n_terms"],
                                                         data["_meta"]["n_common_terms"], data["_meta"]["pages"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
