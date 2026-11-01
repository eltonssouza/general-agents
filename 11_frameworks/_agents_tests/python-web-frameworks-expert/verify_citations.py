# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the python-web-frameworks-expert package citations against the text extracted from the PDFs (three sources).

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/frameworks [--pkg PACKAGE_ROOT] [--checks file.json ...]

Sources and files (in --src): DJT = Django-Tutorial01-Docs.txt (8 pp.), FLT = Flask-Tutorial-Docs.txt (3),
FAPI = FastAPI-Docs-Overview.txt (21). Convention: N = PDF page (marker "=== PAGE N ===").

1) Range: every citation "CODE p.N[-M][, ...]" in the package .md/.json/.py files must be within 1..max of the source. (Pages with no
   technical content - DJT 6-8 and FAPI 3 - may be cited, since the package declares them as such; the positive
   checks are what guarantee the technical content.)
2) Positive: {"cite","contains":[...]} -> the cited pages contain ALL the terms (normalized).
3) Negative: {"cite","absent":[...]} -> NO term appears (whole word) in the cited pages.
Normalization: lowercase, collapsed whitespace, straight quotes; the extracted text breaks lines in the middle of tokens, so
each page is tested in 4 variants (spaces; line-break hyphen removed; break after hyphen joined with hyphen;
line breaks removed). A positive passes if ANY variant contains the term; a negative requires absence in ALL.
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

FILES = {"DJT": "Django-Tutorial01-Docs.txt", "FLT": "Flask-Tutorial-Docs.txt", "FAPI": "FastAPI-Docs-Overview.txt"}
MAXP = {"DJT": 8, "FLT": 3, "FAPI": 21}
BLANK = {"DJT": set(), "FLT": set(), "FAPI": set()}

NUM = r"\d+(?:\s*[-–]\s*\d+)?"
CITE_RE = re.compile(r"\b(DJT|FLT|FAPI)\s+pp?\.\s*(" + NUM + r"(?:\s*,\s*" + NUM + r")*)")


def base_norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("​", "").replace("­", "")
    return s.lower()


def variants(raw):
    s = base_norm(raw)
    v1 = re.sub(r"\s+", " ", s).strip()
    v2 = re.sub(r"\s+", " ", re.sub(r"-[ \t]*\n[ \t]*", "", s)).strip()
    v3 = re.sub(r"\s+", " ", re.sub(r"-[ \t]*\n[ \t]*", "-", s)).strip()
    v4 = re.sub(r"\s+", " ", re.sub(r"[ \t]*\n[ \t]*", "", s)).strip()
    return [v1, v2, v3, v4]


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.extend(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    raw = {}
    var = {}
    for k, fn in FILES.items():
        raw[k] = load_pages(os.path.join(a.src, fn))
        var[k] = {p: None for p in raw[k]}
        if len(raw[k]) != MAXP[k]:
            print(f"WARNING: {k} has {len(raw[k])} pages (expected {MAXP[k]})")
    fails = 0
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in CITE_RE.finditer(text):
                src = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    if p < 1 or p > MAXP[src]:
                        fails += 1
                        print(f"FAILURE range: {src} p.{p} outside 1-{MAXP[src]} in {os.path.relpath(fp, a.pkg)}")
                    elif p in BLANK[src]:
                        fails += 1
                        print(f"FAILURE blank/ad page: {src} p.{p} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages in 'CODE p.N' citations verified.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = CITE_RE.search(cite)
            if not m:
                fails += 1
                print(f"FAILURE invalid cite: {cite}")
                continue
            src = m.group(1)
            plist = expand(m.group(2))
            if not plist or any(p not in var[src] for p in plist):
                fails += 1
                print(f"FAILURE invalid cite (nonexistent page): {cite}")
                continue
            blobs = variants(chr(10).join(raw[src][p] for p in plist))
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    tn = re.sub(r"\s+", " ", base_norm(t)).strip()
                    if not any(tn in b for b in blobs):
                        fails += 1
                        print(f"FAILURE positive: {cite} does not contain '{t}' -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    tn = re.sub(r"\s+", " ", base_norm(t)).strip()
                    rx = re.compile(r"(?<![a-z0-9])" + re.escape(tn) + r"(?![a-z0-9])")
                    if any(rx.search(b) for b in blobs):
                        fails += 1
                        print(f"FAILURE negative: {cite} CONTAINS '{t}' -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
