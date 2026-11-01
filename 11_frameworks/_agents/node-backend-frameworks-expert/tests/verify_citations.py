# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (ACRONYM p.N) against the text extracted from the PDFs.

Sources (acronym -> file in --src): NODEHB (Node-Handbook-freeCodeCamp.txt, 200 págs), EXPHB (Express-Handbook-freeCodeCamp.txt, 38),
FSTF (Fastify-Getting-Started.txt, 14), NEST (NestJS-First-Steps.txt, 10).
Page convention: N = PDF page (marker "=== PAGE N ==="); the PDFs have no printed page numbers.

Usage:
  python -I tests/verify_citations.py [--src PATH/scratch/frameworks] [--pkg PACKAGE_ROOT] [--checks file.json ...]

1) Range: every citation "ACRONYM p.N[-M][, p.K ...]" in the package's .md/.json/.py files (except tests/citation-checks.json and this file)
   must be within 1..N pages of the source.
2) Positive: {"cite","contains":[...]} -> the union of the cited pages contains ALL substrings (normalized:
   lowercase, collapsed whitespace, line-break hyphenation removed, straight quotes).
3) Negative: {"cite","absent":[...]} -> NONE of the expressions appears (whole word) in the cited pages
   (plausible claims that the text does NOT make).
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
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
    "NODEHB": ("Node-Handbook-freeCodeCamp.txt", 200),
    "EXPHB": ("Express-Handbook-freeCodeCamp.txt", 38),
    "FSTF": ("Fastify-Getting-Started.txt", 14),
    "NEST": ("NestJS-First-Steps.txt", 10),
}
SKIP_FILES = {"citation-checks.json", "verify_citations.py"}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[‐‑­]\s*\n\s*", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("​", "")
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


NUM = r"\d+(?:\s*[-–]\s*\d+)?"
CITE_RE = re.compile(r"\b(NODEHB|EXPHB|FSTF|NEST)\s+pp?\.\s*(" + NUM + r"(?:\s*,\s*(?:pp?\.\s*)?" + NUM + r")*)")


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        tok = re.sub(r"^pp?\.\s*", "", tok)
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.extend(range(a, b + 1))
    return pages


def parse_cite(c):
    m = CITE_RE.search(c)
    if not m:
        return None, []
    return m.group(1), expand(m.group(2))


def has_word(text, term):
    t = norm(term)
    return re.search(r"(?<![a-z0-9_@])" + re.escape(t) + r"(?![a-z0-9_])", text) is not None


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_default = os.path.dirname(here)
    root_default = os.path.abspath(os.path.join(pkg_default, "..", "..", ".."))
    ap.add_argument("--src", default=os.path.join(root_default, "scratch", "frameworks"))
    ap.add_argument("--pkg", default=pkg_default)
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    pages = {}
    for sig, (fn, n) in SOURCES.items():
        p = os.path.join(a.src, fn)
        if not os.path.exists(p):
            print(f"ERROR: missing source {p}")
            return 2
        pages[sig] = {k: norm(v) for k, v in load_pages(p).items()}
        if len(pages[sig]) != n:
            print(f"WARNING: {sig} has {len(pages[sig])} pages (expected {n})")
    fails = 0
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if fn in SKIP_FILES or not fn.endswith((".md", ".json", ".py")):
                continue
            path = os.path.join(root, fn)
            try:
                txt = open(path, "r", encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            for m in CITE_RE.finditer(txt):
                sig = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    if not (1 <= p <= SOURCES[sig][1]):
                        fails += 1
                        print(f"FAIL range: {os.path.relpath(path, a.pkg)}: '{m.group(0)}' -> {sig} p.{p} outside 1..{SOURCES[sig][1]}")
    print(f"Range: {total} page numbers checked")

    check_files = a.checks or [os.path.join(here, "citation-checks.json")]
    pos = neg = 0
    for cf in check_files:
        data = json.load(open(cf, "r", encoding="utf-8"))
        for it in data["checks"]:
            sig, pgs = parse_cite(it["cite"])
            if not sig or not pgs:
                fails += 1
                print(f"FAIL invalid cite: {it['cite']}")
                continue
            bad = [p for p in pgs if p not in pages[sig]]
            if bad:
                fails += 1
                print(f"FAIL nonexistent page: {it['cite']} {bad}")
                continue
            union = " ".join(pages[sig][p] for p in pgs)
            if "contains" in it:
                pos += 1
                miss = [t for t in it["contains"] if norm(t) not in union]
                if miss:
                    fails += 1
                    print(f"FAIL positive: {it['cite']} missing {miss} | {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                found = [t for t in it["absent"] if has_word(union, t)]
                if found:
                    fails += 1
                    print(f"FAIL negative: {it['cite']} contains {found} | {it.get('claim', '')}")
    print(f"Positives: {pos} | Negatives: {neg}")
    print("RESULT:", "OK" if fails == 0 else f"{fails} failure(s)")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
