# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the citations of the relational-dbms-internals-expert package against the text extracted from the PDFs.

Input: --src folder with the 7 extracted texts (one per PDF; use tests/extract_pdfs.py), with markers
"=== PAGE N ===" (N = PDF page). Expected names:
  Architecture-of-a-Database-System.txt, PostgreSQL-16-Docs.txt, Readings-in-Database-Systems-RedBook-5th.txt,
  SQL-Antipatterns-injection-chapter.txt, SQL-Antipatterns-trees-chapter.txt,
  SQL-Antipatterns-introduction-chapter.txt, SQL-Antipatterns-toc-chapter.txt

Modes (can be combined):
  (default)        curated checks from tests/citation-checks.json:
                   POSITIVE: all 'terms' must appear on the cited pages ('src' + 'pages');
                   NEGATIVE: no 'term' may appear on ANY page of the source (or, if the check carries 'pages', on none of those pages).
  --audit-index    (round 9) checks the page ranges of ALL topics and aliases of scripts/relational_index.json against the size of each
                   source, and that every COVERED topic with at most 4 pages has an existing, non-empty page in the extracted text
  --audit-ranges   extracts ALL the citations "SIGLA p.N[-M][, p.X]" from the package files (md/py/json) and checks
                   range (1..number of pages), order and width (ranges > 12 pages become a WARNING).
Terms: case-insensitive comparison, with normalized whitespace/quotes, tolerant of end-of-line hyphenation
(also compares without spaces and hyphens). Prefix 're:' = regular expression. No network; read-only.
Exit code 0 if there was no failure (warnings do not count).
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

FILES = {
    "ARCH": "Architecture-of-a-Database-System.txt",
    "PG16": "PostgreSQL-16-Docs.txt",
    "REDBK": "Readings-in-Database-Systems-RedBook-5th.txt",
    "ANTI-INJ": "SQL-Antipatterns-injection-chapter.txt",
    "ANTI-TREE": "SQL-Antipatterns-trees-chapter.txt",
    "ANTI-INT": "SQL-Antipatterns-introduction-chapter.txt",
    "ANTI-TOC": "SQL-Antipatterns-toc-chapter.txt",
}
SIGLAS = "|".join(sorted(FILES, key=len, reverse=True))
CITE_RE = re.compile(r"\b(" + SIGLAS + r")\s+p\.(\d+)(?:\s*[-–]\s*(\d+))?((?:\s*[,;]\s*p\.\d+(?:\s*[-–]\s*\d+)?)*)")
EXTRA_RE = re.compile(r"p\.(\d+)(?:\s*[-–]\s*(\d+))?")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"),
                 (" ", " "), ("�", "'")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


def squash(s):
    return re.sub(r"[\s\-]+", "", s)


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    pages = {}
    for i in range(1, len(parts), 2):
        pages[int(parts[i])] = parts[i + 1]
    return pages


class Corpus:
    def __init__(self, src):
        self.src = src
        self.raw = {}
        self.n = {}
        self.sq = {}

    def get(self, sigla):
        if sigla not in self.raw:
            pages = load_pages(os.path.join(self.src, FILES[sigla]))
            self.raw[sigla] = pages
            self.n[sigla] = {k: norm(v) for k, v in pages.items()}
            self.sq[sigla] = {k: squash(v) for k, v in self.n[sigla].items()}
        return self.raw[sigla]

    def has(self, sigla, page, term):
        self.get(sigla)
        if page not in self.n[sigla]:
            return False
        return term_in(self.n[sigla][page], self.sq[sigla][page], term)


def term_in(text_n, text_sq, term):
    if term.startswith("re:"):
        return re.search(term[3:], text_n, re.IGNORECASE) is not None
    t = norm(term)
    if t in text_n:
        return True
    # tolerance for end-of-line hyphenation only for long terms (avoids false positives on short terms)
    return len(t) >= 12 and squash(t) in text_sq


def expand(a, b):
    a = int(a)
    b = int(b) if b else a
    return list(range(a, b + 1))


def run_checks(corp, checks_path, verbose):
    with open(checks_path, encoding="utf-8") as f:
        checks = json.load(f)
    fails = []
    for c in checks["positive"]:
        sig = c["src"]
        corp.get(sig)
        missing = []
        bad_pages = [p for p in c["pages"] if p not in corp.n[sig]]
        for t in c["terms"]:
            if not any(corp.has(sig, p, t) for p in c["pages"]):
                missing.append(t)
        ok = not missing and not bad_pages
        if verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], sig, "p.", c["pages"], "-", c["claim"],
                  ("" if ok else "| missing: %s %s" % (missing, ("| nonexistent pages: %s" % bad_pages) if bad_pages else "")))
        if not ok:
            fails.append(c["id"])
    for c in checks["negative"]:
        sigs = c["src"] if isinstance(c["src"], list) else [c["src"]]
        found = []
        for sig in sigs:
            corp.get(sig)
            for p in corp.n[sig]:
                if c.get("pages") and p not in c["pages"]:
                    continue        # negative with "pages": the term must not appear on THESE pages (e.g., citation overreach)
                for t in c["terms"]:
                    if term_in(corp.n[sig][p], corp.sq[sig][p], t):
                        found.append((sig, p, t))
        ok = not found
        if verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "(negative)", sigs, "-", c["claim"],
                  ("" if ok else "| found on %s" % found[:4]))
        if not ok:
            fails.append(c["id"])
    print("Curated checks: %d positive, %d negative, %d failures" % (len(checks["positive"]), len(checks["negative"]), len(fails)))
    return fails


def audit_ranges(corp, pkg, verbose):
    totals = {}
    errors = []
    warns = []
    n_cites = 0
    for dp, dn, fn in os.walk(pkg):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
        for name in fn:
            if not name.endswith((".md", ".py", ".json")):
                continue
            # the report and the test cases cite WRONG v1 pages on purpose; audit only the current content
            if name in ("relatorio-de-fidelidade.md",):
                continue
            path = os.path.join(dp, name)
            try:
                text = open(path, encoding="utf-8").read()
            except Exception:
                continue
            for ln, line in enumerate(text.splitlines(), 1):
                for m in CITE_RE.finditer(line):
                    sig = m.group(1)
                    specs = [(m.group(2), m.group(3))] + EXTRA_RE.findall(m.group(4) or "")
                    npg = len(corp.get(sig))
                    for a, b in specs:
                        n_cites += 1
                        ia, ib = int(a), int(b) if b else int(a)
                        totals[sig] = totals.get(sig, 0) + 1
                        rel = os.path.relpath(path, pkg)
                        if ia < 1 or ib < ia or ib > npg:
                            errors.append("%s:%d %s p.%s%s out of range 1..%d" % (rel, ln, sig, a, ("-" + b) if b else "", npg))
                        elif ib - ia > 12:
                            warns.append("%s:%d %s p.%s-%s wide range (%d pages)" % (rel, ln, sig, a, b, ib - ia + 1))
    print("Citations extracted: %d (per source: %s)" % (n_cites, ", ".join("%s=%d" % kv for kv in sorted(totals.items()))))
    for w in warns:
        print("WARN  ", w)
    for e in errors:
        print("FAIL  ", e)
    print("Range audit: %d failures, %d warnings" % (len(errors), len(warns)))
    return errors


def audit_index(corp, pkg):
    """page ranges of the page map (topics/aliases of relational_index.json) within 1..number of pages of the source, and short ranges non-empty."""
    with open(os.path.join(pkg, "scripts", "relational_index.json"), encoding="utf-8") as f:
        idx = json.load(f)
    errors = []
    n = 0
    for kind in ("topics", "aliases"):
        for t in idx.get(kind, []):
            for sig, spec in (t.get("pages") or {}).items():
                if sig not in FILES:
                    errors.append("%s %s: unknown sigla %s" % (kind, t["id"], sig))
                    continue
                pages = corp.get(sig)
                for m in EXTRA_RE.finditer(spec):
                    a = int(m.group(1))
                    b = int(m.group(2) or a)
                    n += 1
                    if a < 1 or b < a or b > len(pages):
                        errors.append("%s %s: %s p.%d-%d out of range 1..%d" % (kind, t["id"], sig, a, b, len(pages)))
                    elif b - a <= 3 and any(len(pages[p].strip()) < 40 for p in range(a, b + 1)):
                        errors.append("%s %s: %s p.%d-%d has a practically empty page in the extracted text" % (kind, t["id"], sig, a, b))
    for e in errors:
        print("FAIL  ", e)
    print("Curated index audit: %d ranges checked, %d failures" % (n, len(errors)))
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder with the texts extracted from the PDFs")
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("--pkg", default=os.path.dirname(here))
    ap.add_argument("--audit-ranges", action="store_true")
    ap.add_argument("--audit-index", action="store_true")
    ap.add_argument("--no-checks", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    corp = Corpus(a.src)
    fails = []
    if not a.no_checks:
        fails += run_checks(corp, a.checks, a.verbose)
    if a.audit_ranges:
        fails += audit_ranges(corp, a.pkg, a.verbose)
    if a.audit_index:
        fails += audit_index(corp, a.pkg)
    if fails:
        print("Failures:", len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
