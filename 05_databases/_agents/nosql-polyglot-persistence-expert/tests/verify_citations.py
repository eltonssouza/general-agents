# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the citations of the nosql-polyglot-persistence-expert package against the text extracted from the PDFs.

Preparation (once; PyMuPDF): for each source PDF generate a .txt with "=== PAGE N ===" markers (N = PDF page):
    import fitz
    d = fitz.open("NoSQL-Databases-Strauch.pdf")
    open("NoSQL-Databases-Strauch.txt", "w", encoding="utf-8").write(
        "".join("=== PAGE %d ===\\n%s\\n" % (i, p.get_text()) for i, p in enumerate(d, 1)))
Expected names in --src DIR (see SOURCES below): NoSQL-Databases-Strauch.txt, NoSQL-Redis-The-Little-Redis-Book.txt,
NoSQL-MongoDB-Applied-Design-Patterns.txt, NoSQL-MongoDB-Manual-Home.txt, NoSQL-MongoDB-Manual-Introduction.txt,
NoSQL-Cassandra-Overview.txt, NoSQL-CouchDB-Introduction.txt, NoSQL-Elasticsearch-Guide-Index.txt,
NoSQL-Neo4j-Graph-Databases-2e.txt.

Usage:  python -I verify_citations.py --src DIR_WITH_THE_TXT_FILES [--checks citation-checks.json] [-v]

POSITIVE: all 'terms' must appear (case-insensitive, whitespace-normalized, NFKC) in the set of the cited
'pages' of source 'src' (each term may be on any of the pages). Prefix 're:' = regex.
NEGATIVE: no 'term' may appear on ANY page of any of the sources in 'srcs'.
The 'terms' are verbatim source text (Portuguese or English) and are kept as is; only 'claim' text is translated.
No network; read-only. Exit 0 if everything passed, 1 otherwise (2 if source text is missing).
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

SOURCES = {
    "STRAUCH": "NoSQL-Databases-Strauch.txt",
    "REDIS": "NoSQL-Redis-The-Little-Redis-Book.txt",
    "MONGO-PAT": "NoSQL-MongoDB-Applied-Design-Patterns.txt",
    "MONGO-MAN-H": "NoSQL-MongoDB-Manual-Home.txt",
    "MONGO-MAN-I": "NoSQL-MongoDB-Manual-Introduction.txt",
    "CASS": "NoSQL-Cassandra-Overview.txt",
    "COUCH": "NoSQL-CouchDB-Introduction.txt",
    "ELAST": "NoSQL-Elasticsearch-Guide-Index.txt",
    "NEO4J-GDB": "NoSQL-Neo4j-Graph-Databases-2e.txt",
}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder with the per-page extracted .txt files")
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)

    pages = {}
    for sig, fn in SOURCES.items():
        path = os.path.join(a.src, fn)
        if not os.path.exists(path):
            print("ERROR: source text missing: %s (acronym %s)" % (path, sig), file=sys.stderr)
            return 2
        pages[sig] = load_pages(path)

    fails = []
    for c in checks["positive"]:
        pg = pages[c["src"]]
        bad_pages = [p for p in c["pages"] if p not in pg]
        blob = " ".join(pg.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing and not bad_pages
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], c["src"], "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("nonexistent page: %s" % bad_pages) if bad_pages else "")))
        if not ok:
            fails.append(c["id"])

    for c in checks["negative"]:
        found = []
        for sig in c["srcs"]:
            for n_, txt in pages[sig].items():
                for t in c["terms"]:
                    if has(txt, t):
                        found.append((sig, n_, t))
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "(negative) -", c["claim"],
                  ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])

    npos, nneg = len(checks["positive"]), len(checks["negative"])
    print("Summary: %d positive, %d negative, %d failures" % (npos, nneg, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
