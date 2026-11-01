# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the citations of the web-performance-networking-expert package against the text extracted from the PDF.

NOTE: this script belongs to a suite that targets an older layout of the package (see run_script_tests.py); it is kept for reference.

Usage (read-only, no network):
  python -I tests/verify_citations.py --src PATH/HPBN.txt [--pkg PACKAGE_PATH]

The source text has "=== PAGE N ===" markers (N = PDF page, 1-401; printed = N - 18).

Checks:
 1) Range: every citation "HPBN p.N[-M][, ...]" in the package's .md/.py/.json files (outside tests/) must be within 1-401.
 2) Content (positives): each item of tests/citation-checks.json["positivas"] requires the indicated PDF page to
    contain all the terms (normalization: lowercase, alphanumeric only, NFKC) and printed = PDF - 18 (when >= 22).
 3) Negatives: each term of ["negativas"] must be ABSENT from the whole PDF (whole word, case-insensitive) (modern content
    must not become [from source]).
 3b) Negatives per page (round 2): each item of ["negativas_por_pagina"] requires the term to be ABSENT from the indicated PDF pages
     (e.g. p.89-90 do not contain "privacy": the book does not credit OCSP stapling with eliminating the privacy leak).
 4) Token audit: a line carrying the label [from source] (or the Portuguese [do livro]) that contains a forbidden modern token (HPACK, Huffman, TLS 1.3,
    0-RTT, QUIC, HTTP/3, BBR, Core Web Vitals, preconnect, preload, permessage-deflate, WebTransport, OFDMA, WPA3...)
    must also carry a caveat mark on the same line ([extrapolation], [DATED], "not", "NOT", "absent",
    "outside the book", "name", "not covered"...).
Exit 0 if everything passes, 1 otherwise.
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

MAXP = 401
FORBIDDEN = ["HPACK", "Huffman", "TLS 1.3", "0-RTT", "QUIC", "HTTP/3", "BBR", "Core Web Vitals", "preconnect",
             "preload", "permessage-deflate", "WebTransport", "OFDMA", "WPA3", "Lighthouse", "Service Worker",
             "Early Hints", "RFC 7540", "RFC 7541", "RFC 8446", "RFC 7413", "RFC 7692"]
# The reference files are still in Portuguese, so the Portuguese caveat marks stay; the English equivalents are added.
LABELS = ["[do livro]", "[from source]"]
HEDGES = ["[extrapolação]", "[DATADO]", "[inferência]", "não ", "Não ", "NÃO", "ausente", "fora do livro", "nome",
          "sem cobertura", "SEM COBERTURA", "nunca", "Nunca", "não aparece",
          "[extrapolation]", "[DATED]", "[inference]", "not ", "Not ", "NOT", "absent", "outside the book", "name",
          "not covered", "NOT COVERED", "never", "Never", "does not appear"]


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[^a-z0-9]", "", s)


def load_pages(path):
    if os.path.isdir(path):
        path = os.path.join(path, "HPBN.txt")
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = set()
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.update(range(a, b + 1))
    return pages


def default_src(pkg):
    root = os.path.abspath(os.path.join(pkg, "..", "..", ".."))
    return os.path.join(root, "scratch", "blind", "cases", "web-performance-networking-expert", "src", "HPBN.txt")


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", help="HPBN.txt (or the folder containing it); default: scratch/blind/cases/.../src/HPBN.txt")
    ap.add_argument("--pkg", default=here)
    a = ap.parse_args()
    src = a.src or default_src(a.pkg)
    pages = load_pages(src)
    if len(pages) != MAXP:
        print(f"WARNING: the text has {len(pages)} pages (expected {MAXP})")
    fulltext_words = unicodedata.normalize("NFKC", " ".join(pages.values())).lower()
    fails = 0

    # 1) range
    cite_re = re.compile(r"\bHPBN\s+p\.\s*(\d[\d\s,\-–]*)")
    total, distinct = 0, set()
    files = []
    for root, _, fs in os.walk(a.pkg):
        for fn in fs:
            if not fn.endswith((".md", ".json", ".py")):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, a.pkg)
            if rel.startswith("tests" + os.sep) and fn.endswith(".json"):
                continue
            if fn in ("verify_citations.py", "run_script_tests.py"):
                continue
            files.append((fp, rel))
    for fp, rel in files:
        text = open(fp, "r", encoding="utf-8", errors="replace").read()
        for m in cite_re.finditer(text):
            for p in expand(m.group(1)):
                total += 1
                distinct.add(p)
                if p < 1 or p > MAXP:
                    fails += 1
                    print(f"FAIL range: HPBN p.{p} outside 1-{MAXP} in {rel}")
    print(f"Range: {total} page numbers checked in {len(files)} files; {len(distinct)} distinct pages cited")

    # 2) positives and 3) negatives
    checks = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))
    ok = 0
    pos = checks["positivas"]
    for c in pos:
        p = c["pagina_pdf"]
        body = norm(pages.get(p, ""))
        miss = [t for t in c["termos"] if norm(t) not in body]
        imp = c.get("pagina_impressa")
        bad_imp = imp is not None and p >= 22 and imp != p - 18
        if miss or bad_imp:
            fails += 1
            print(f"FAIL content: PDF {p} ({c.get('descricao', '')}) does not contain {miss}" + (" / printed page inconsistent" if bad_imp else ""))
        else:
            ok += 1
    print(f"Positives: {ok}/{len(pos)} OK")
    neg = checks["negativas"]
    nok = 0
    for n in neg:
        pat = r"(?<![a-z0-9])" + re.escape(n["termo"].lower()).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
        if re.search(pat, fulltext_words):
            fails += 1
            print(f"FAIL negative: '{n['termo']}' APPEARS in the PDF (it cannot be declared absent)")
        else:
            nok += 1
    print(f"Negatives: {nok}/{len(neg)} absent from the PDF, as declared")
    npg = checks.get("negativas_por_pagina", [])
    npok = 0
    for n in npg:
        txt = unicodedata.normalize("NFKC", " ".join(pages.get(q, "") for q in n["paginas"])).lower()
        pat = r"(?<![a-z0-9])" + re.escape(n["termo"].lower()).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
        if re.search(pat, txt):
            fails += 1
            print(f"FAIL negative per page: '{n['termo']}' APPEARS on pages {n['paginas']} ({n.get('descricao', '')})")
        else:
            npok += 1
    print(f"Negatives per page: {npok}/{len(npg)} absent from the indicated pages")

    # 4) token audit
    flagged = 0
    checked = 0
    for fp, rel in files:
        if not fp.endswith(".md"):
            continue
        for i, line in enumerate(open(fp, "r", encoding="utf-8", errors="replace").read().splitlines(), 1):
            if not any(lb in line for lb in LABELS):
                continue
            for tok in FORBIDDEN:
                extra = r"(?!\s+scanner)" if tok == "preload" else ""
                if re.search(r"(?<![A-Za-z0-9])" + re.escape(tok) + r"(?![A-Za-z0-9])" + extra, line, re.I):
                    checked += 1
                    if not any(h in line for h in HEDGES):
                        flagged += 1
                        fails += 1
                        print(f"FAIL token: '{tok}' next to [from source] without a caveat in {rel}:{i}")
    print(f"Tokens: {checked} occurrences of modern tokens next to [from source] examined; {flagged} without a caveat")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
