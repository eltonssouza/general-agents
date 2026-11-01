# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the citations of the software-testing-qa-expert package against the text extracted from the PDFs.

Requires a directory (--src) with the per-page extracted texts, one file per source, with markers
"=== PAGE N ===" (N = PDF page): JUNIT.txt, MOCK.txt, TDM.txt, JMETER.txt, SWEG.txt
(SWEG = Software-Engineering-at-Google-completo.pdf, 408 pages; ch. 11-14 = p.149-221).
Extraction (PyMuPDF): python -I -c "import fitz; d=fitz.open(PDF); open(TXT,'w',encoding='utf-8').write(''.join('=== PAGE %d ===\\n%s\\n' % (i, p.get_text()) for i,p in enumerate(d,1)))"

POSITIVE checks: all 'terms' must appear (case-insensitive, whitespace and ligatures normalized) in the
set of cited pages. NEGATIVE checks: no 'term' may appear on any page of the source
(or in the 'page_range'); terms prefixed with 're:' are regular expressions.
No network; read-only. Exit 0 if everything passed, 1 otherwise.

Usage: python -I tests/verify_citations.py --src PATH/src [--checks tests/citation-checks.json] [-v]
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


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("\xa0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def has(text, term):
    term = norm(term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    cache = {}

    def pages_of(src):
        if src not in cache:
            cache[src] = load_pages(os.path.join(a.src, src + ".txt"))
        return cache[src]

    fails = []
    for c in checks["positive"]:
        pg = pages_of(c["src"])
        missing_pages = [p for p in c["pages"] if p not in pg]
        blob = " ".join(pg.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing and not missing_pages
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("| nonexistent pages: %s" % missing_pages) if missing_pages else "")))
        if not ok:
            fails.append(c["id"])
    for c in checks["negative"]:
        pg = pages_of(c["src"])
        lo, hi = c.get("page_range", [min(pg), max(pg)])
        found = [(n, t) for n, txt in pg.items() if lo <= n <= hi for t in c["terms"] if has(txt, t)]
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])
    print("Summary: %d positive, %d negative, %d failures" % (len(checks["positive"]), len(checks["negative"]), len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
