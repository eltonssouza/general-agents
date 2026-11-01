# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the data-warehouse-streaming-distributed-expert package against the text extracted from the PDFs.

Usage (from any folder):
  python -I tests/verify_citations.py --kimball KIMBALL.txt --stream STREAM.txt --helland HELLAND.txt [-v]

The .txt files have "=== PAGE N ===" markers (N = PDF page; KIMBALL printed = N-3; STREAM printed = N).
To extract: see README.md, section "Audit" (PyMuPDF: page.get_text() per page).

Layers:
 1. POSITIVE (citation-checks.json): all 'terms' must appear (case-insensitive, whitespace normalized)
    in the cited pages (the set of pages).
 2. NEGATIVE: no 'term' may appear in ANY page of the source ('re:' = regex).
 3. PACKAGE SWEEP: every citation "(KIMBALL p.N[-M])", "(STREAM p.N[-M])" in the package's .md/.py/.json files must fall
    inside the source page range (KIMBALL 1-24, STREAM 1-30); a HELLAND citation with a page is an error.
No network; read-only. Exit 0 if everything passed, 1 otherwise.
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

RANGES = {"KIMBALL": 24, "STREAM": 30}


def load_pages(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    pages = {}
    for i in range(1, len(parts), 2):
        t = unicodedata.normalize("NFKC", parts[i + 1])
        pages[int(parts[i])] = re.sub(r"\s+", " ", t)
    return pages


def has(text, term):
    term = unicodedata.normalize("NFKC", term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def scan_package(root):
    """Validates the page ranges of all citations (SIGLA p.N[-M][, p.X])."""
    bad = []
    total = 0
    pat = re.compile(r"\((KIMBALL|STREAM|HELLAND) p\.([0-9][0-9,\-\sp.;]*)\)")
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or "__pycache__" in dp:
            continue
        for f in fn:
            if not f.endswith((".md", ".py", ".json")):
                continue
            p = os.path.join(dp, f)
            if f in ("citation-checks.json", "verify_citations.py", "audit_tokens.py", "run_script_tests.py"):
                continue
            try:
                txt = open(p, encoding="utf-8").read()
            except Exception:
                continue
            if f in ("casos-de-teste.md", "relatorio-de-fidelidade.md") and False:
                continue
            for m in pat.finditer(txt):
                sigla = m.group(1)
                nums = [int(x) for x in re.findall(r"\d+", m.group(2))]
                total += 1
                if sigla == "HELLAND":
                    bad.append((os.path.relpath(p, root), m.group(0), "HELLAND has no citable pages"))
                    continue
                for n in nums:
                    if n < 1 or n > RANGES[sigla]:
                        bad.append((os.path.relpath(p, root), m.group(0), "outside 1-%d" % RANGES[sigla]))
                        break
    return total, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kimball", required=True)
    ap.add_argument("--stream", required=True)
    ap.add_argument("--helland", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("--pkg", default=os.path.dirname(here))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    srcs = {"KIMBALL": load_pages(a.kimball), "STREAM": load_pages(a.stream), "HELLAND": load_pages(a.helland)}
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)

    fails = []
    for c in checks["positive"]:
        pages = srcs[c["src"]]
        blob = " ".join(pages.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s" % missing))
        if not ok:
            fails.append(c["id"])

    for c in checks["negative"]:
        found = []
        for n, txt in srcs[c["src"]].items():
            for t in c["terms"]:
                if has(txt, t):
                    found.append((n, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])

    total, bad = scan_package(a.pkg)
    for b in bad:
        print("FAIL range:", b)
        fails.append("range:%s" % b[0])
    print("Citations swept in the package: %d; out of range: %d" % (total, len(bad)))
    npos, nneg = len(checks["positive"]), len(checks["negative"])
    print("Summary: %d positive, %d negative, %d failures" % (npos, nneg, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
