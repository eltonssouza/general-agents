# -*- coding: utf-8 -*-
"""
slr_lookup.py - locates topics of ISLR (1st ed.) and ESL (2nd ed.) by theme, page or chapter.

Read-only, stdlib, no network, deterministic. Run with: python -I scripts/slr_lookup.py TERM
Page convention: PDF (marker "=== PAGE N ==="). Printed ISLR = PDF - 15; printed ESL = PDF - 19.
Origin of the findings: [from source] = the index points to the page where the topic was read; the topic classification is [inference].
Queries work in English and Portuguese (accents ignored).

Options:
  TERM [TERM...]        search by theme (accents ignored); --top N (default 6); --json
  --page BOOK N         chapter, printed page, whether the page was read and the topics that cover it (BOOK = ISLR or ESL)
  --printed BOOK N      PDF page corresponding to printed page N
  --chapters [BOOK]     chapter table with PDF range and reading status
  --map [THEME]         ISLR <-> ESL map (where the ESL goes deeper than the ISLR), with pages of both
  --gaps                NOT COVERED terms (with occurrence counts in the extracted text) and unread ranges
  --coverage            reading coverage summary
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


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "slr_index.json"), encoding="utf-8") as f:
        return json.load(f)


def ranges(spec):
    out = []
    for tok in (spec or "").split(","):
        tok = tok.strip()
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", tok)
        if m:
            a = int(m.group(1))
            out.append((a, int(m.group(2) or a)))
    return out


def in_ranges(p, spec):
    return any(a <= p <= b for a, b in ranges(spec))


def tokens(q):
    return [t for t in re.split(r"[^a-z0-9+#.\-/]+", norm(q)) if t]


def score(e, qn, qt):
    best = 0
    cand = list(e["terms"]) + [e["topic"]]
    for term in cand:
        tn = norm(term)
        if qn == tn:
            best = max(best, 100)
        elif len(qn) >= 2 and re.search(r"(?<![a-z0-9])" + re.escape(qn) + r"(?![a-z0-9])", tn):
            best = max(best, 60 if tn in [norm(x) for x in e["terms"]] else 40)
        elif len(tn) >= 3 and re.search(r"(?<![a-z0-9])" + re.escape(tn) + r"(?![a-z0-9])", qn):
            best = max(best, 50)
    tt = set()
    for term in cand:
        tt.update(tokens(term))
    hits = [t for t in qt if len(t) >= 3 and t in tt]
    if hits:
        best = max(best, 10 * len(hits))
    return best


def gap_for(idx, qn):
    for g in idx["gaps"]:
        keys = [norm(k) for k in g["keys"]] + [norm(g["term"])]
        for k in keys:
            if k and (qn == k or re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", qn)):
                return g
    return None


def cmd_search(idx, a):
    q = " ".join(a.term)
    qn, qt = norm(q), tokens(q)
    res = []
    for e in idx["entries"]:
        s = score(e, qn, qt)
        if s > 0:
            res.append((s, e))
    res.sort(key=lambda x: -x[0])
    res = res[: a.top]
    gap = gap_for(idx, qn)
    if a.json:
        print(json.dumps({"query": q, "results": [dict(score=s, **e) for s, e in res], "not_covered": gap}, ensure_ascii=False, indent=1))
        return 0
    if gap:
        o = gap["occurrences"]
        print(f"NOT COVERED (or partial coverage): '{gap['term']}' - {gap['note']}.")
        print(f"  Occurrences in the extracted text: ISLR {sum(o['ISLR'].values())} | ESL {sum(o['ESL'].values())}  ({', '.join(gap['keys'])})")
    if not res:
        if not gap:
            print(f"NOT COVERED: no indexed topic matches '{q}'. See --chapters/--gaps; any answer is [extrapolation].")
        return 0
    for s, e in res:
        print(f"- {e['topic']}")
        parts = []
        if e["islr"]:
            parts.append(f"ISLR p.{e['islr']}")
        if e["esl"]:
            parts.append(f"ESL p.{e['esl']}")
        print(f"    {' | '.join(parts) if parts else '(no book pages; supporting file)'} (PDF) | ref: references/{e['ref']}")
    print("Origin: [inference] on the index; confirm the text in the reference before citing. Pages = PDF (printed ISLR = PDF - 15; ESL = PDF - 19).")
    return 0


def book(idx, name):
    n = name.upper()
    if n not in idx["books"]:
        print("BOOK must be ISLR or ESL")
        return None
    return n, idx["books"][n]


def chapter_of(b, p):
    for c in b["chapters"]:
        if c["pdf_start"] <= p <= c["pdf_end"]:
            return c
    return None


def cmd_page(idx, name, p):
    r = book(idx, name)
    if not r:
        return 2
    n, b = r
    if p < 1 or p > b["pdf_pages"]:
        print(f"{n} has {b['pdf_pages']} PDF pages; p.{p} is out of range.")
        return 2
    c = chapter_of(b, p)
    lo, hi = b["body"]
    if not c:
        print(f"{n} PDF p.{p}: outside the mapped body (body = {lo}-{hi}; covers, preface, table of contents, references and index not used).")
        return 0
    was_read = any(a0 <= p <= b0 for a0, b0 in c["read"])
    print(f"{n} PDF p.{p} | printed {p - b['offset']} | Ch.{c['ch']} {c['title']} | chapter reading: {c['reading']}")
    print("  page READ by this package" if was_read else "  page NOT READ by this package (NOT COVERED directly)")
    key = "islr" if n == "ISLR" else "esl"
    for e in idx["entries"]:
        if in_ranges(p, e[key]):
            print(f"  - {e['topic']} (p.{e[key]}) -> references/{e['ref']}")
    return 0


def cmd_printed(idx, name, k):
    r = book(idx, name)
    if not r:
        return 2
    n, b = r
    p = k + b["offset"]
    print(f"{n} printed {k} -> PDF p.{p}  (uniform offset {b['offset']})")
    c = chapter_of(b, p)
    if c:
        print(f"  Ch.{c['ch']} {c['title']}")
    return 0


def cmd_chapters(idx, name):
    names = [name.upper()] if name else ["ISLR", "ESL"]
    for n in names:
        if n not in idx["books"]:
            print("BOOK must be ISLR or ESL")
            return 2
        b = idx["books"][n]
        print(f"{n}: {b['title']} | {b['pdf_pages']} PDF pages | printed = PDF - {b['offset']}")
        for c in b["chapters"]:
            print(f"  Ch.{c['ch']:>2} {c['title']} | PDF {c['pdf_start']}-{c['pdf_end']} | {c['reading']}")
    return 0


def cmd_map(idx, theme):
    qn = norm(theme) if theme else ""
    k = 0
    for m in idx["map"]:
        if qn and qn not in norm(m["theme"]) and qn not in norm(m["esl_adds"]) and not any(qn in norm(x) for x in m.get("aliases", [])):
            continue
        k += 1
        unread = "" if m["esl_read"] else "  [NOT READ in the ESL]"
        print(f"- {m['theme']}: ISLR p.{m['islr'] or '(none)'} | ESL p.{m['esl']}{unread}")
        print(f"    ESL adds: {m['esl_adds']}")
    if not k:
        print(f"NOT COVERED in the map for '{theme}'. Run without an argument to list everything.")
    return 0


def cmd_gaps(idx):
    print("NOT COVERED / partial coverage (occurrence counts in the extracted text of both books):")
    for g in idx["gaps"]:
        o = g["occurrences"]
        print(f"- {g['term']}: {g['note']}. ISLR {sum(o['ISLR'].values())} | ESL {sum(o['ESL'].values())}")
    print("\nUNREAD RANGES in this package (may exist in the books; do not use as [from source]):")
    for n, lst in idx["unread"].items():
        for g in lst:
            print(f"- {n} PDF p.{g['pages']}: {g['theme']}")
    return 0


def cmd_coverage(idx):
    for n, b in idx["books"].items():
        print(f"{n}: {b['pdf_pages']} PDF pages; body {b['body'][0]}-{b['body'][1]}; printed = PDF - {b['offset']}")
        for c in b["chapters"]:
            tot = c["pdf_end"] - c["pdf_start"] + 1
            read = sum(min(b2, c["pdf_end"]) - max(a2, c["pdf_start"]) + 1 for a2, b2 in c["read"] if b2 >= c["pdf_start"] and a2 <= c["pdf_end"])
            print(f"  Ch.{c['ch']:>2}: {read}/{tot} pages of the range read")
    print("Neither book was read in full; the ISLR labs and exercises were not read.")
    return 0


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("term", nargs="*")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", nargs=2, metavar=("BOOK", "N"))
    ap.add_argument("--printed", nargs=2, metavar=("BOOK", "N"))
    ap.add_argument("--chapters", nargs="?", const="")
    ap.add_argument("--map", nargs="?", const="")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--coverage", action="store_true")
    a = ap.parse_args()
    idx = load()
    if a.page:
        return cmd_page(idx, a.page[0], int(a.page[1]))
    if a.printed:
        return cmd_printed(idx, a.printed[0], int(a.printed[1]))
    if a.chapters is not None:
        return cmd_chapters(idx, a.chapters)
    if a.map is not None:
        return cmd_map(idx, a.map)
    if a.gaps:
        return cmd_gaps(idx)
    if a.coverage:
        return cmd_coverage(idx)
    if not a.term:
        ap.print_help()
        return 1
    return cmd_search(idx, a)


if __name__ == "__main__":
    sys.exit(main())
