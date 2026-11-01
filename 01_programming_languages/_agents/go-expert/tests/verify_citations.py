# -*- coding: utf-8 -*-
"""
verify_citations.py - checks go-expert claims against the text extracted from the source PDFs.

POSITIVE checks (citation-checks.json, "positive"): all the 'terms' must appear (case-insensitive, whitespace
normalized) in the cited pages of the 'doc' (each term may be on any of the listed pages).
NEGATIVE checks ("negative"): plausible claims that the PDF does NOT contain; none of the 'terms' may appear on
any page of the listed 'docs' (a term prefixed with 're:' is a regular expression). 'docs' may be "all".
It also checks the index scripts/go_index.json (--index): page ranges and 'terms' of each source labeled "from source".
Doc acronyms: Eff, Spec, Little, RN1.20 ... RN1.24. Pages = PDF pages (Little: printed = N - 1).

Usage:  python -I tests/verify_citations.py --src FOLDER_WITH_THE_TXT_FILES [--checks tests/citation-checks.json] [-v]
The .txt files come from tests/extract_pdf_text.py. No network, read-only. Exit 0 if everything passed, 1 otherwise.
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

DOCS = {
    "Eff": "Go-Effective-Go", "Spec": "Go-Language-Specification", "Little": "Go-The-Little-Go-Book",
    "RN1.20": "Go-1.20-Release-Notes", "RN1.21": "Go-1.21-Release-Notes", "RN1.22": "Go-1.22-Release-Notes",
    "RN1.23": "Go-1.23-Release-Notes", "RN1.24": "Go-1.24-Release-Notes",
}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"),
                 ("­", ""), ("\xa0", " ")):
        s = s.replace(a, b)
    return s


def load(src):
    pages = {}
    for sig, stem in DOCS.items():
        with open(os.path.join(src, stem + ".txt"), encoding="utf-8") as f:
            raw = f.read()
        parts = re.split(r"=== PAGE (\d+) ===", raw)
        pages[sig] = {int(parts[i]): re.sub(r"\s+", " ", norm(parts[i + 1])) for i in range(1, len(parts), 2)}
    return pages


def has(text, term):
    term = norm(term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    # compare ignoring all whitespace (the extracted text breaks lines in the middle of expressions)
    return re.sub(r"\s+", "", term.lower()) in re.sub(r"\s+", "", text.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder with the extracted .txt files (=== PAGE N ===)")
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("--index", default=os.path.join(os.path.dirname(here), "scripts", "go_index.json"))
    ap.add_argument("--checklists", default=os.path.join(os.path.dirname(here), "scripts", "go_checklists.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    P = load(a.src)
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    fails = []

    for c in checks["positive"]:
        pages = P[c["doc"]]
        out_of_range = [p for p in c["pages"] if p not in pages]
        blob = " ".join(pages.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing and not out_of_range
        if a.verbose or not ok:
            print("OK   " if ok else "FAIL", c["id"], c["doc"], "p.", c["pages"], "-", c["claim"],
                  "" if ok else "| missing: %s %s" % (missing, ("| out of range: %s" % out_of_range) if out_of_range else ""))
        if not ok:
            fails.append(c["id"])

    for c in checks["negative"]:
        docs = list(DOCS) if c["docs"] == "all" else c["docs"]
        found = [(d, n, t) for d in docs for n, txt in P[d].items() for t in c["terms"] if has(txt, t)]
        ok = not found
        if a.verbose or not ok:
            print("OK   " if ok else "FAIL", c["id"], "(negative)", docs, "-", c["claim"],
                  "" if ok else "| found in %s" % found[:5])
        if not ok:
            fails.append(c["id"])

    nidx = 0
    if os.path.exists(a.index):
        with open(a.index, encoding="utf-8") as f:
            idx = json.load(f)
        for t in idx["topicos"]:
            for s in t["fontes"]:
                if s["label"] != "from source":
                    continue
                nidx += 1
                pages = P[s["sigla"]]
                bad = [p for p in s["paginas"] if p not in pages]
                blob = " ".join(pages.get(p, "") for p in s["paginas"])
                missing = [x for x in s.get("terms", []) if not has(blob, x)]
                ok = not bad and not missing and s.get("terms")
                if a.verbose or not ok:
                    print("OK   " if ok else "FAIL", "IDX", t["id"], s["sigla"], s["paginas"],
                          "" if ok else "| missing: %s out of range: %s" % (missing, bad))
                if not ok:
                    fails.append("IDX:%s:%s" % (t["id"], s["sigla"]))

    nchk = 0
    if os.path.exists(a.checklists):
        with open(a.checklists, encoding="utf-8") as f:
            cl = json.load(f)
        for area, v in cl["areas"].items():
            for i, it in enumerate(v["itens"], 1):
                if it["origem"] != "from source":
                    continue
                nchk += 1
                pages = P[it["doc"]]
                bad = [p for p in it["paginas"] if p not in pages]
                blob = " ".join(pages.get(p, "") for p in it["paginas"])
                missing = [x for x in it.get("terms", []) if not has(blob, x)]
                ok = not bad and not missing and it.get("terms")
                if a.verbose or not ok:
                    print("OK   " if ok else "FAIL", "CHK", area, i, it["doc"], it["paginas"],
                          "" if ok else "| missing: %s out of range: %s" % (missing, bad))
                if not ok:
                    fails.append("CHK:%s:%d" % (area, i))

    npos, nneg = len(checks["positive"]), len(checks["negative"])
    print("Summary: %d positive, %d negative, %d index sources, %d checklist items, %d failures" % (npos, nneg, nidx, nchk, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
