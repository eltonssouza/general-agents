# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the design-patterns-expert package's citations against the text extracted from the 4 PDFs.

Input: a directory (--src) with RG.txt, GPP.txt, CC.txt and PEAA.txt, each with "=== PAGE N ===" markers (N = PDF
page), for example extracted with PyMuPDF (fitz): page.get_text(). No network; read-only.

POSITIVE checks (citation-checks.json, "positive"): all the "terms" must appear, case-insensitively, in the set of
cited pages ("pages") of the text of the "sigla" (source code). Terms with the "re:" prefix are regular expressions.
NEGATIVE checks ("negative"): none of the "terms" may appear in the text of the "sigla" (all pages, or only the given
"pages"); they prove that the PDF does NOT contain something that could be attributed to the book. Without "sigla": all sources.

Usage:
  python -I verify_citations.py --src PATH/src [--checks citation-checks.json] [-v]
Exit code 0 if everything passed; 1 otherwise.
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

SIGLAS = ("RG", "GPP", "CC", "PEAA")


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
    t = norm(term)
    if t.startswith("re:"):
        return re.search(t[3:], text, re.IGNORECASE) is not None
    low = text.lower()
    tl = t.lower()
    if tl in low:
        return True
    # tolerates line breaks/hyphenation from the extraction
    return re.sub(r"[\s\-]+", "", tl) in re.sub(r"[\s\-]+", "", low)


def expand(pages):
    out = []
    for p in pages:
        if isinstance(p, str) and "-" in p:
            a, b = p.split("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(p))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="directory with RG.txt, GPP.txt, CC.txt, PEAA.txt")
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    books = {}
    for s in SIGLAS:
        p = os.path.join(a.src, s + ".txt")
        if not os.path.exists(p):
            print("ERROR: missing %s" % p)
            return 2
        books[s] = load_pages(p)
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)

    fails = []
    for c in checks["positive"]:
        pages = books[c["sigla"]]
        want = expand(c["pages"])
        bad = [p for p in want if p not in pages]
        blob = " ".join(pages.get(p, "") for p in want)
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing and not bad
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["sigla"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("nonexistent page: %s" % bad) if bad else "")))
        if not ok:
            fails.append(c["id"])

    for c in checks["negative"]:
        found = []
        siglas = [c["sigla"]] if c.get("sigla") else list(SIGLAS)
        for s in siglas:
            pages = books[s]
            rng = expand(c["pages"]) if c.get("pages") else sorted(pages)
            for n in rng:
                txt = pages.get(n, "")
                for t in c["terms"]:
                    if has(txt, t):
                        found.append((s, n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:4]))
        if not ok:
            fails.append(c["id"])

    npos, nneg = len(checks["positive"]), len(checks["negative"])
    print("Summary: %d positive, %d negative, %d failures" % (npos, nneg, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
