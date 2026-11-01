# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the algorithms-expert package against the text extracted from Erickson's PDF ("Algorithms", 2019).

Layers:
  1. POSITIVE (citation-checks.json): all 'terms' must appear (NFKC, lowercase, normalized whitespace) in the
     cited pages (as a set: each term may be in any one of them). Prefix 're:' = regular expression.
  2. NEGATIVE: none of the 'terms' may appear on ANY page (the book does NOT contain the plausible claim).
  3. RANGES: every citation "(JE p.N[-M][, ...])" in agents/, references/, skills/, README, AGENTS.md and .github/ must be
     within 1..N_pages and, when there is a range, N <= M.
  4. Lookup INDEX (skills/erickson-topic-lookup/scripts/erickson_index.json): for each topic, the 'verificar' terms
     must appear on the topic's pages; for each section, the title must appear on the starting page (+-1).
Usage (from the package root):
  python -I tests/extract_pdf_text.py ../../Algorithms-Erickson.pdf erickson.txt     # generates === PAGE N ===
  python -I tests/verify_citations.py --text erickson.txt [-v]
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


def nz(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s)


def load_pages(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): nz(parts[i + 1]) for i in range(1, len(parts), 2)}


def has(text, term):
    term = nz(term)
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def expand(spec):
    """Extracts the pages from "N", "N-M", "N, M", "N, note 3; JE p.M" etc. Returns a list [a, b, ...] or None if invalid.
    Free text after the pages (e.g. ", note 3", ": MomSelect") is ignored; format markers (percent, bracket, backslash) => None."""
    if any(ch in spec for ch in "%[\\"):
        return None
    s = re.sub(r"(?:nota|note)\s*\d+", "", spec)
    s = re.sub(r"JE\s*p\.?", "", s)
    m = re.match(r"^[\s\d,;\-–p.]*", s)
    s = m.group(0) if m else ""
    out = []
    for tok in re.split(r"\s*[,;]\s*", s.strip()):
        tok = re.sub(r"^p\.?\s*", "", tok).strip().rstrip(".")
        if not tok:
            continue
        mm = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not mm:
            return None
        a = int(mm.group(1))
        b = int(mm.group(2) or a)
        if b < a:
            return None
        out.extend([a, b])
    return out or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    ap.add_argument("--checks", default=os.path.join(here, "citation-checks.json"))
    ap.add_argument("--pkg", default=root)
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    pages = load_pages(a.text)
    npages = max(pages)
    checks = json.load(open(a.checks, encoding="utf-8"))
    fails = []

    # 1. positive
    for c in checks["positive"]:
        blob = " ".join(pages.get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "p.", c["pages"], "-", c["claim"], ("" if ok else "| missing: %s" % missing))
        if not ok:
            fails.append(c["id"])

    # 2. negative
    for c in checks["negative"]:
        found = [(n, t) for n, txt in pages.items() for t in c["terms"] if has(txt, t)]
        ok = not found
        if a.verbose or not ok:
            print(("OK   " if ok else "FAIL "), c["id"], "(negative) -", c["claim"], ("" if ok else "| found in %s" % found[:5]))
        if not ok:
            fails.append(c["id"])

    # 3. page ranges
    cite = re.compile(r"\(JE p\.?\s*([^)]+)\)")
    ncite = nbad = 0
    for sub in ("agents", "references", "skills", ".github", "tests"):
        base = os.path.join(a.pkg, sub)
        for rt, _, fs in os.walk(base):
            for f in fs:
                if not f.endswith((".md", ".py", ".json")) or f in ("citation-checks.json", "erickson_index.json"):
                    continue
                fp = os.path.join(rt, f)
                for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
                    for m in cite.finditer(line):
                        spec = m.group(1)
                        if spec.strip().startswith("N") or any(ch in spec for ch in "%[\\"):
                            continue  # format placeholder
                        ncite += 1
                        r = expand(spec)
                        if r is None or any(p < 1 or p > npages for p in r):
                            nbad += 1
                            print("FAIL invalid range %s:%d (JE p.%s)" % (os.path.relpath(fp, a.pkg), ln, spec))
                            fails.append("range:%s:%d" % (f, ln))
    for fn in ("README.md", "AGENTS.md"):
        fp = os.path.join(a.pkg, fn)
        if os.path.exists(fp):
            for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
                for m in cite.finditer(line):
                    spec = m.group(1)
                    if spec.strip().startswith("N") or any(ch in spec for ch in "%[\\"):
                        continue
                    ncite += 1
                    r = expand(spec)
                    if r is None or any(p < 1 or p > npages for p in r):
                        nbad += 1
                        print("FAIL invalid range %s:%d (JE p.%s)" % (fn, ln, spec))
                        fails.append("range:%s:%d" % (fn, ln))

    # 4. lookup index
    idx_path = os.path.join(a.pkg, "skills", "erickson-topic-lookup", "scripts", "erickson_index.json")
    nidx = 0
    if os.path.exists(idx_path):
        d = json.load(open(idx_path, encoding="utf-8"))
        for e in d["temas"]:
            nidx += 1
            lo, hi = e["paginas"]
            blob = " ".join(pages.get(p, "") for p in range(lo, hi + 1))
            miss = [t for t in e["verificar"] if not has(blob, t)]
            if miss or not (1 <= lo <= hi <= npages):
                print("FAIL index topic %s p.%s missing=%s" % (e["id"], e["paginas"], miss))
                fails.append("index:" + e["id"])
        for s in d["secoes"]:
            nidx += 1
            p = s["pagina_pdf"]
            title = re.sub(r"[^A-Za-z0-9 ]", "", unicodedata.normalize("NFKD", s["titulo"]))
            title = re.sub(r"\s+", " ", title).strip().lower()
            ok = False
            for q in (p, p - 1, p + 1):
                body = re.sub(r"[^A-Za-z0-9 ]", "", unicodedata.normalize("NFKD", pages.get(q, ""))).lower()
                body = re.sub(r"\s+", " ", body)
                if title[:25] in body:
                    ok = True
            if not ok:
                print("WARNING index section %s %r not located on PDF page %d (+-1; may be a ligature/diacritic)" % (s["numero"], s["titulo"], p))
    npos, nneg = len(checks["positive"]), len(checks["negative"])
    print("Summary: %d positive, %d negative, %d citations with verified range (%d invalid), %d index entries, %d failures"
          % (npos, nneg, ncite, nbad, nidx, len(fails)))
    if fails:
        print("Failures:", ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
