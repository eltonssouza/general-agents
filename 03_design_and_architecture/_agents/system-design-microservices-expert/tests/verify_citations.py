# -*- coding: utf-8 -*-
"""
verify_citations.py - audits "(SIGLA p.N[-M])" citations against the text extracted from the source PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/src [--pkg PACKAGE_ROOT] [--checks file.json ...]

--src must contain one SIGLA.txt file per work (SAP.txt, SDH.txt, MS-MIC.txt, MS-CLD.txt, MS-WEB.txt, EDS.txt, SBC.txt,
SOA.txt, APIGW.txt, JMG.txt, REST.txt), generated with "=== PAGE N ===" markers (N = PDF page, the package convention).
The extractor used in the audit is `tests/extract_sources.py` (PyMuPDF).

Layers:
1) Range: every "SIGLA p.N[-M][, ...]" citation in the package .md/.py/.json files must be within 1..number of pages of the work.
2) Positive content: item {"cite","contains":[...]} -> the cited page(s) contain ALL the substrings
   (normalized: lowercase, collapsed whitespace; also compares the version without spaces/hyphens, to tolerate line breaks).
3) Negative content: item {"cite","absent":[...]} -> NONE of the terms appears on the cited pages
   (plausible claims that the source does NOT make in that passage).
4) Index: each entry in scripts/sysdesign_index.json has "cite" and "terms"; the terms must be on the page.
Read-only, no network. Exit 0 if everything passes; 1 otherwise.
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

NPAGES = {"SAP": 54, "SDH": 75, "MS-MIC": 350, "MS-CLD": 193, "MS-WEB": 118, "EDS": 166, "SBC": 4,
          "SOA": 55, "APIGW": 50, "JMG": 160, "REST": 118}
SIGLAS = "|".join(sorted(NPAGES, key=len, reverse=True))
CITE_RE = re.compile(r"\b(" + SIGLAS + r")\s+pp?\.\s*(\d[\d\s,\-–]*)")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("�", "'").replace("\xa0", " ")
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("​", "").replace("­", "")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"[\s\-]+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok.strip())
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.extend(range(a, b + 1))
    return pages


def parse_cite(cite):
    m = CITE_RE.search(cite)
    if not m:
        return None, []
    return m.group(1), expand(m.group(2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--checks", nargs="*", default=None)
    a = ap.parse_args()

    N, S = {}, {}
    for sig in NPAGES:
        p = os.path.join(a.src, sig + ".txt")
        if not os.path.exists(p):
            print(f"ERROR: missing {p}")
            sys.exit(2)
        pages = load_pages(p)
        if len(pages) != NPAGES[sig]:
            print(f"WARNING: {sig} has {len(pages)} pages (expected {NPAGES[sig]})")
        N[sig] = {k: norm(v) for k, v in pages.items()}
        S[sig] = {k: squash(v) for k, v in N[sig].items()}
    fails = 0

    # 1) range
    total = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json", "audit_tokens.py"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in CITE_RE.finditer(text):
                sig = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    if p < 1 or p > NPAGES[sig]:
                        fails += 1
                        print(f"FAIL range: {sig} p.{p} outside 1-{NPAGES[sig]} in {os.path.relpath(fp, a.pkg)}")
    print(f"Range: {total} cited pages checked.")

    # 2) and 3) curated checks
    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            sig, plist = parse_cite(cite)
            if not sig or not plist or any(p not in N[sig] for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite}")
                continue
            blob = " ".join(N[sig][p] for p in plist)
            sblob = "".join(S[sig][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    nt = norm(t)
                    if nt not in blob and squash(nt) not in sblob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    nt = norm(t)
                    if re.search(r"(?<![a-z0-9])" + re.escape(nt) + r"(?![a-z0-9])", blob) or (len(squash(nt)) >= 6 and squash(nt) in sblob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' -- {it.get('claim', '')}")
    print(f"Curated checks: {pos} positive, {neg} negative.")

    # 4) terms of the concept index
    idx_path = os.path.join(a.pkg, "scripts", "sysdesign_index.json")
    nterms = 0
    if os.path.exists(idx_path):
        for c in json.load(open(idx_path, "r", encoding="utf-8")):
            for e in c.get("entries", []):
                sig, plist = parse_cite(e["cite"])
                if not sig or not plist or any(p not in N[sig] for p in plist):
                    fails += 1
                    print(f"FAIL index: invalid cite {e['cite']} ({c['key']})")
                    continue
                blob = " ".join(N[sig][p] for p in plist)
                sblob = "".join(S[sig][p] for p in plist)
                for t in e.get("terms", []):
                    nterms += 1
                    nt = norm(t)
                    if nt not in blob and squash(nt) not in sblob:
                        fails += 1
                        print(f"FAIL index: {e['cite']} does not contain '{t}' ({c['key']})")
    print(f"Index: {nterms} terms checked.")
    print(f"Total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
