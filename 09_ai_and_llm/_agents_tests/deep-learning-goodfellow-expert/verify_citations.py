# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (DLB p.N) against the text extracted from the PDF.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/ai [--pkg PACKAGE_ROOT] [--checks file1.json ...]

Page convention: N = PDF page (marker "=== PAGE N ===" of the extracted text). Printed page = N - 15 (constant in the body p.16-735).

1) Range: every citation "DLB p.N[-M][, ...]" in the package .md/.json/.py files must be in 1..800 and, for the references, in the body that was read (16..735).
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings
   (normalized: lowercase, NFKC [fi/fl ligatures], collapsed whitespace, line-break hyphenation removed, straight quotes and dashes).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (as a whole word) on the cited pages
   (plausible claims that the book does NOT make in that passage; covers the 2016 boundary).
4) Gaps: each term of "lacunas" in scripts/dlb_index.json must have 0 occurrences in the body (p.16-735).
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

SRC_FILE = "DL-Deep-Learning-Goodfellow.txt"
MAXP = 800
BODY_MIN, BODY_MAX = 16, 735


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[‐‑­]\s*\n\s*", "", s)
    s = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s.lower()).strip()


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


def word_in(term, blob):
    return re.search(r"(?<![a-z0-9])" + re.escape(norm(term)) + r"(?![a-z0-9])", blob) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    pages = load_pages(os.path.join(a.src, SRC_FILE))
    npages = {k: norm(v) for k, v in pages.items()}
    if len(pages) != MAXP:
        print(f"WARNING: text has {len(pages)} pages (expected {MAXP})")
    fails = 0

    cite_re = re.compile(r"\bDLB\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            in_refs = os.sep + "references" + os.sep in fp
            for m in cite_re.finditer(text):
                for p in expand(m.group(1)):
                    total += 1
                    lo, hi = (BODY_MIN, BODY_MAX) if in_refs else (1, MAXP)
                    if p < lo or p > hi:
                        fails += 1
                        print(f"FAIL range: DLB p.{p} outside {lo}-{hi} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages cited in package text.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.search(r"p{1,2}\.\s*(\S.*)$", cite)
            plist = expand(m.group(1)) if m else []
            if not plist or any(p not in npages for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            blob = " ".join(npages[p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    if word_in(t, blob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")

    # index gaps: 0 occurrences in the body
    idxp = os.path.join(a.pkg, "scripts", "dlb_index.json")
    if os.path.exists(idxp):
        idx = json.load(open(idxp, "r", encoding="utf-8"))
        body = " ".join(npages[p] for p in range(BODY_MIN, BODY_MAX + 1) if p in npages)
        nl = 0
        for g in idx.get("lacunas", []):
            for t in g["busca"]:
                nl += 1
                if len(t) <= 3 and t.lower() in ("nas", "gnn", "gpt", "llm", "jax", "tpu", "bpe", "bf16", "fp16"):
                    # short acronyms: search as a whole word
                    pass
                if word_in(t, body):
                    # legitimate occurrences in another sense are handled in the note; here we flag them
                    fails += 1
                    print(f"FAIL gap: term '{t}' (gap '{g['termo']}') occurs in the body p.{BODY_MIN}-{BODY_MAX}")
        print(f"Gaps: {nl} terms verified as absent from the body.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
