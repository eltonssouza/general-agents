# -*- coding: utf-8 -*-
"""
foundations_lookup.py - deterministic lookup in the package index (SICP, TAUP, CI).

ORIGIN OF THE RULES: the index (foundations_index.json) was built by hand from reading the PDF pages and is
checked by tests/verify_citations.py (each entry has 'verify' terms that must appear on the cited pages).
The search itself (normalization, keyword scoring) is [extrapolation]: it is our heuristic, with no basis in the books.
Pages = PDF page (see references/INDEX.md); in TAUP, printed page = PDF - 2.

Usage:
  python -I scripts/foundations_lookup.py "substitution model"
  python -I scripts/foundations_lookup.py --book CI "tricolor"
  python -I scripts/foundations_lookup.py --list [--book TAUP]
  python -I scripts/foundations_lookup.py --not-in-book
Output: 0 if coverage was found; 1 with "NOT COVERED" when the index does not cover the term (label [extrapolation]).
No network; read-only.
"""
import argparse
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
STOP = {"de", "da", "do", "das", "dos", "e", "o", "a", "os", "as", "em", "no", "na", "um", "uma", "the", "of", "and", "for",
        "to", "in", "is", "what", "how", "como", "que", "qual", "sobre", "livro", "regra", "regras", "rule", "rules",
        "chapter", "capitulo"}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def tokens(q):
    return [t for t in re.findall(r"[a-z0-9!\-\+/\.]+", norm(q)) if len(t) >= 2 and t not in STOP]


def load():
    with open(os.path.join(HERE, "foundations_index.json"), encoding="utf-8") as f:
        return json.load(f)


def cite(e):
    a, _, b = e["pages"].partition("-")
    pg = a if (not b or a == b) else "%s-%s" % (a, b)
    return "[%s p.%s]" % (e["book"], pg)


def stem(t):
    for suf in ("ing", "es", "ed", "s"):
        if t.endswith(suf) and len(t) - len(suf) >= 4:
            return t[: -len(suf)]
    return t


def has(t, text):
    """token present in the text: whole word (short tokens), substring (>= 4 letters) or same stem (scoping ~ scope)."""
    if len(t) < 4:
        return re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", text) is not None
    if t in text:
        return True
    st = stem(t)
    return len(st) >= 4 and any(w.startswith(st) for w in re.findall(r"[a-z0-9]+", text))


def score(e, q, toks):
    """returns (points, tokens_in_keywords_or_title, tokens_in_any_field)."""
    kws = [norm(k) for k in e["keywords"]]
    title = norm(e["title"])
    summ = norm(e["summary"])
    kwtext = " ".join(kws)
    s = 0
    nq = norm(q)
    if nq and any(nq == k for k in kws):
        s += 8
    elif nq and any(nq in k or k in nq for k in kws if len(k) >= 4):
        s += 4
    hit_kw = hit_any = 0
    for t in toks:
        if has(t, kwtext):
            s += 3
            hit_kw += 1
            hit_any += 1
        elif has(t, title):
            s += 2
            hit_kw += 1
            hit_any += 1
        elif has(t, summ):
            s += 1
            hit_any += 1
    return s, hit_kw, hit_any


def main():
    ap = argparse.ArgumentParser(description="Looks up the foundations index (SICP, TAUP, CI).")
    ap.add_argument("query", nargs="*", help="term (e.g. 'substitution model', 'rule of silence', 'pratt parsing')")
    ap.add_argument("--book", choices=["SICP", "TAUP", "CI"], help="filter by book")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--list", action="store_true", help="list all entries (with pages)")
    ap.add_argument("--not-in-book", action="store_true", help="list what the books do NOT contain")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    data = load()
    entries = [e for e in data["entries"] if not a.book or e["book"] == a.book]

    if a.list:
        for e in entries:
            print("%-34s %-5s %-12s %s" % (e["id"], e["book"], cite(e), e["title"]))
        return 0
    if a.not_in_book:
        for n in data["not_in_book"]:
            print("- [%s] (termos: %s) %s" % ("/".join(n["books"]), ", ".join(n["terms"]), n["note"]))
        return 0
    if not a.query:
        ap.error("give a term, --list or --not-in-book")
    q = " ".join(a.query)
    toks = tokens(q)
    nq = norm(q)

    # 1) boundary: is the term something the book does NOT contain?
    warn = []
    for n in data["not_in_book"]:
        if any(norm(t) == nq or norm(t) in nq for t in n["terms"]) and (not a.book or a.book in n["books"]):
            warn.append(n)

    strict, partial = [], []
    for e in entries:
        s, kw, anyc = score(e, q, toks)
        if kw > 0:
            (strict if (toks and anyc == len(toks)) else partial).append((s, e))
    strict.sort(key=lambda x: (-x[0], x[1]["page"]))
    partial.sort(key=lambda x: (-x[0], x[1]["page"]))
    res = strict if strict else partial
    is_partial = not strict
    # the boundary applies: the term is something the book does not contain and there is no complete match
    if warn and is_partial:
        res_related = res
        res = []
    if a.json:
        print(json.dumps({"query": q, "not_in_book": warn, "partial": is_partial,
                          "results": [dict(e, score=s) for s, e in res[: a.limit]]}, ensure_ascii=False, indent=1))
        return 0 if res else 1

    for n in warn:
        print("ALERT (boundary): %s" % n["note"])
    if not res:
        print("NOT COVERED: no record for '%s'%s. The collection covers SICP, TAUP and CI; label [extrapolation] "
              "or say that the book does not address it." % (q, (" in " + a.book) if a.book else ""))
        return 1
    print("Found %d record(s) for '%s' (PDF page; TAUP printed = PDF - 2):\n" % (len(res), q))
    for i, (s, e) in enumerate(res[: a.limit], 1):
        print("[%d] %s - %s (section %s)" % (i, e["book"], e["title"], e["section"]))
        print("    Citation: %s   Read: references/%s" % (cite(e), e["ref"]))
        print("    Keywords: %s" % ", ".join(e["keywords"][:6]))
        print("    Summary: %s\n" % e["summary"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
