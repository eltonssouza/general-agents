# -*- coding: utf-8 -*-
"""
verify_citations.py - audits "BAAS p.N" and "CE2 p.N" citations against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/ai [--pkg PACKAGE_ROOT] [--checks file1.json ...]

Page convention: N = PDF page ("=== PAGE N ===" marker of the extracted text).
  BAAS: printed = PDF - 25 in the body; CE2: PDF = printed.
1) Range: every citation "BAAS p.N[-M][, ...]" / "CE2 p.N[-M]" in the package's .md/.json/.py files must be within 1..289 (BAAS) or 1..28 (CE2);
   in the references, BAAS within 20..282 (body + index) and CE2 within 1..28. It also checks the page ranges of the data files (ctx_index.json,
   agent_checklist_items.json).
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings (normalized: lowercase,
   collapsed whitespace, line-break hyphenation removed, straight quotes).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears (as a whole word) on the cited pages
   (plausible claims that the texts do NOT contain).
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

SRC = {"BAAS": "Building-Agentic-AI-System.txt", "CE2": "Context-Engineering-2.0-arxiv.txt"}
MAXP = {"BAAS": 289, "CE2": 28}
REF_RANGE = {"BAAS": (20, 282), "CE2": (1, 28)}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()
    pages = {}
    npages = {}
    for k, fn in SRC.items():
        pages[k] = load_pages(os.path.join(a.src, fn))
        npages[k] = {p: norm(v) for p, v in pages[k].items()}
        if len(pages[k]) != MAXP[k]:
            print(f"WARNING: {k} has {len(pages[k])} pages (expected {MAXP[k]})")
    fails = 0

    cite_re = re.compile(r"\b(BAAS|CE2)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            in_refs = os.sep + "references" + os.sep in fp and fn != "INDEX.md"  # INDEX cites front/back matter (cover, p.24, p.287)
            for m in cite_re.finditer(text):
                src = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    lo, hi = REF_RANGE[src] if in_refs else (1, MAXP[src])
                    if p < lo or p > hi:
                        fails += 1
                        print(f"FAIL range: {src} p.{p} outside {lo}-{hi} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} pages cited in package text.")

    # data files: page ranges of the indexes
    sdir = os.path.join(a.pkg, "scripts")
    idx_fp = os.path.join(sdir, "ctx_index.json")
    if os.path.exists(idx_fp):
        idx = json.load(open(idx_fp, encoding="utf-8"))
        for e in idx["topicos"]:
            for rng in expand(e["paginas"]):
                if rng < 1 or rng > MAXP[e["fonte"]]:
                    fails += 1
                    print(f"FAIL index: {e['fonte']} p.{rng} outside the PDF in topic '{e['topico']}'")
        for c in idx["capitulos"]:
            if c["pdf_fim"] > MAXP[c["fonte"]] or c["pdf_ini"] < 1:
                fails += 1
                print(f"FAIL chapter outside the PDF: {c}")
    ck_fp = os.path.join(sdir, "agent_checklist_items.json")
    if os.path.exists(ck_fp):
        ck = json.load(open(ck_fp, encoding="utf-8"))
        for i in ck["itens"]:
            if i["fonte"] in MAXP:
                for p in expand(i["paginas"]):
                    if p < 1 or p > MAXP[i["fonte"]]:
                        fails += 1
                        print(f"FAIL checklist {i['id']}: {i['fonte']} p.{p} outside the PDF")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.match(r"(BAAS|CE2)\s+p{1,2}\.\s*(\S.*)$", cite)
            if not m:
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            src = m.group(1)
            plist = expand(m.group(2))
            if not plist or any(p not in npages[src] for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite} ({os.path.basename(f)})")
                continue
            blob = " ".join(npages[src][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", blob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' ({os.path.basename(f)}) -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
