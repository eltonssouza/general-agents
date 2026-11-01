# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the citations of the software-foundations-expert package against the text extracted from the PDFs.

Inputs: a --src folder with sicp.txt, taup.txt and ci.txt (text extracted with "=== PAGE N ===" markers, N = PDF page;
extraction with PyMuPDF, e.g. page.get_text()). The PDFs live in 03_design_and_architecture/ and are NOT shipped in the package.

Layers:
 1. RANGE: every citation "(SICP|TAUP|CI p.N[-M][, p.K][; CI p.X])" found in agents/, references/, scripts/, tests/*.md,
    README.md and AGENTS.md must have an existing page (SICP 1-634, TAUP 1-549, CI 1-630) and an ordered range.
 2. POSITIVE (tests/citation-checks.json, >=60): all 'terms' must appear, within the set of listed pages
    (case-insensitive, whitespace normalized, NFKC). 'a|b' = any alternative; prefix 're:' = regular expression.
 3. NEGATIVE (>=15): plausible claims that the books do NOT contain; none of the terms may appear on ANY page of the
    listed books.
 4. INDEX: each entry of scripts/foundations_index.json has 'verify' terms that must appear on the cited pages.

Usage: python -I tests/verify_citations.py --src <folder> [-v]       Exit 0 if everything passed, 1 otherwise. No network.
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
ROOT = os.path.dirname(HERE)
FILES = {"SICP": "sicp.txt", "TAUP": "taup.txt", "CI": "ci.txt"}
NPAGES = {"SICP": 634, "TAUP": 549, "CI": 630}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\ufffd", "'")
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", s)


def load_pages(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def has(text, term):
    if term.startswith("re:"):
        return re.search(term[3:], text, re.IGNORECASE) is not None
    t = norm(term).lower()
    low = text.lower()
    return any(alt.strip() in low for alt in t.split("|")) if "|" in t else t in low


CITE = re.compile(
    r"(SICP|TAUP|CI)\s+p\.\s*(\d+)(?:\s*[-\u2013]\s*(\d+))?((?:\s*,\s*p\.\s*\d+(?:\s*[-\u2013]\s*\d+)?)*)")
EXTRA = re.compile(r"p\.\s*(\d+)(?:\s*[-\u2013]\s*(\d+))?")


def citations(text):
    out = []
    for m in CITE.finditer(text):
        b = m.group(1)
        a = int(m.group(2))
        z = int(m.group(3)) if m.group(3) else a
        out.append((b, a, z))
        for e in EXTRA.finditer(m.group(4) or ""):
            ea = int(e.group(1))
            ez = int(e.group(2)) if e.group(2) else ea
            out.append((b, ea, ez))
    return out


def scan_files():
    paths = []
    for d in ("agents", "references", "scripts", "tests"):
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for fn in sorted(os.listdir(base)):
            if fn.endswith((".md", ".py", ".json")) and fn != "citation-checks.json":
                paths.append(os.path.join(base, fn))
    for fn in ("README.md", "AGENTS.md"):
        p = os.path.join(ROOT, fn)
        if os.path.isfile(p):
            paths.append(p)
    gh = os.path.join(ROOT, ".github", "agents")
    if os.path.isdir(gh):
        paths += [os.path.join(gh, f) for f in sorted(os.listdir(gh)) if f.endswith(".md")]
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--checks", default=os.path.join(HERE, "citation-checks.json"))
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    pages = {b: load_pages(os.path.join(a.src, fn)) for b, fn in FILES.items()}
    for b, n in NPAGES.items():
        if len(pages[b]) != n:
            print("WARNING: %s has %d pages in the text (expected %d)" % (b, len(pages[b]), n))

    fails = []

    # 1) range
    total = bad = 0
    per_file = {}
    for p in scan_files():
        with open(p, encoding="utf-8") as f:
            txt = f.read()
        cs = citations(txt)
        per_file[os.path.relpath(p, ROOT)] = len(cs)
        for b, x, z in cs:
            total += 1
            if x < 1 or z > NPAGES[b] or x > z:
                bad += 1
                print("FAIL    range %s p.%d-%d invalid in %s" % (b, x, z, os.path.relpath(p, ROOT)))
                fails.append("range:" + os.path.relpath(p, ROOT))
    print("[1] range: %d citations read, %d out of range" % (total, bad))

    # 2) positive
    with open(a.checks, encoding="utf-8") as f:
        checks = json.load(f)
    npos = 0
    for c in checks["positive"]:
        npos += 1
        blob = " ".join(pages[c["book"]].get(p, "") for p in c["pages"])
        missing = [t for t in c["terms"] if not has(blob, t)]
        ok = not missing
        if a.verbose or not ok:
            print("%s %s %s p.%s - %s%s" % ("OK    " if ok else "FAIL  ", c["id"], c["book"], c["pages"], c["claim"],
                                            "" if ok else " | missing: %s" % missing))
        if not ok:
            fails.append(c["id"])
    print("[2] positive: %d checks" % npos)

    # 3) negative
    nneg = 0
    for c in checks["negative"]:
        nneg += 1
        found = []
        for b in c["books"]:
            for n, txt in pages[b].items():
                for t in c["terms"]:
                    if has(txt, t):
                        found.append((b, n, t))
        ok = not found
        if a.verbose or not ok:
            print("%s %s (negative) %s - %s%s" % ("OK    " if ok else "FAIL  ", c["id"], "/".join(c["books"]), c["claim"],
                                                  "" if ok else " | found in %s" % found[:4]))
        if not ok:
            fails.append(c["id"])
    print("[3] negative: %d checks" % nneg)

    # 4) index
    nidx = 0
    ip = os.path.join(ROOT, "scripts", "foundations_index.json")
    if os.path.isfile(ip):
        with open(ip, encoding="utf-8") as f:
            idx = json.load(f)
        for e in idx["entries"]:
            nidx += 1
            x, _, z = e["pages"].partition("-")
            x, z = int(x), int(z or x)
            blob = " ".join(pages[e["book"]].get(p, "") for p in range(x, z + 1))
            missing = [t for t in e["verify"] if not has(blob, t)]
            if missing or a.verbose:
                print("%s index %s %s p.%s%s" % ("OK    " if not missing else "FAIL  ", e["id"], e["book"], e["pages"],
                                                  "" if not missing else " | missing: %s" % missing))
            if missing:
                fails.append("index:" + e["id"])
    print("[4] index: %d entries checked" % nidx)

    print("Summary: %d positive, %d negative, %d index entries, %d citations in range, %d failures"
          % (npos, nneg, nidx, total, len(fails)))
    if fails:
        print("Failures:", ", ".join(sorted(set(fails))))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
