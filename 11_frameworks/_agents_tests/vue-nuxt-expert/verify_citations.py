# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (VUEHB|VUE3G|NUXT p.N) against the text extracted from the PDFs.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/frameworks [--pkg PACKAGE_ROOT] [--checks file.json ...]

--src must contain: Vue-Handbook-freeCodeCamp.txt, Vue3-Guide-Introduction.txt, Nuxt-Getting-Started.txt
(text per page with the marker "=== PAGE N ===", N = PDF page; the sources have no printed page numbers).

1) Range: every citation "ABBR p.N[-M][, ...]" in the package .md/.json/.py files must be within 1..number of pages of the ABBR
   (VUEHB 133, VUE3G 8, NUXT 6). In references/, bare "p.N" are checked against the last abbreviation on the same line
   or, failing that, the file's default abbreviation (01-05,09 VUEHB; 06 VUE3G; 10 NUXT) or 1..133.
2) Positive: {"cite","contains":[...]} -> the cited pages contain ALL the substrings (normalized).
3) Negative: {"cite","absent":[...]} -> NO term appears (whole word) in the cited pages.
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

SRC = {"VUEHB": ("Vue-Handbook-freeCodeCamp.txt", 133), "VUE3G": ("Vue3-Guide-Introduction.txt", 8), "NUXT": ("Nuxt-Getting-Started.txt", 6)}
FILE_DEFAULT = {"01": "VUEHB", "02": "VUEHB", "03": "VUEHB", "04": "VUEHB", "05": "VUEHB", "06": "VUE3G", "09": "VUEHB", "10": "NUXT"}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("​", "")
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
    for sig, (fn, npg) in SRC.items():
        pages[sig] = {k: norm(v) for k, v in load_pages(os.path.join(a.src, fn)).items()}
        if len(pages[sig]) != npg:
            print(f"WARNING: {sig} has {len(pages[sig])} pages (expected {npg})")
    fails = 0
    cite_re = re.compile(r"\b(VUEHB|VUE3G|NUXT)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    bare_re = re.compile(r"(?<![A-Za-z])p{1,2}\.\s*(\d[\d\s,\-–]*)")
    total = bare = 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".py", ".json")) or fn in ("verify_citations.py", "citation-checks.json", "vue_index.json"):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, a.pkg)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                sig = m.group(1)
                for p in expand(m.group(2)):
                    total += 1
                    if p < 1 or p > SRC[sig][1]:
                        fails += 1
                        print(f"FAIL range: {sig} p.{p} outside 1-{SRC[sig][1]} in {rel}")
            if os.sep + "references" + os.sep in fp and not fn.startswith("INDEX"):
                dflt = FILE_DEFAULT.get(fn[:2])
                for line in text.splitlines():
                    for m in bare_re.finditer(line):
                        before = line[:m.start()]
                        sigs = re.findall(r"\b(VUEHB|VUE3G|NUXT)\b[^|]*$", before)
                        # abbreviation immediately before on the line; if the citation itself already has one, ignore (checked above)
                        if re.search(r"\b(VUEHB|VUE3G|NUXT)\s*$", before):
                            continue
                        sig = sigs[-1] if sigs else dflt
                        mx = SRC[sig][1] if sig else 133
                        for p in expand(m.group(1)):
                            bare += 1
                            if p < 1 or p > mx:
                                fails += 1
                                print(f"FAIL range: p.{p} outside 1-{mx} (abbreviation {sig}) in {rel}: {line.strip()[:90]}")
    print(f"Range: {total} pages in 'ABBR p.N' citations; {bare} in bare 'p.N' in the references.")

    files = a.checks or [os.path.join(a.pkg, "tests", "citation-checks.json")]
    pos = neg = 0
    for f in files:
        data = json.load(open(f, "r", encoding="utf-8"))
        for it in data.get("checks", []):
            cite = it["cite"]
            m = re.match(r"(VUEHB|VUE3G|NUXT)\s+p{1,2}\.\s*(\S.*)$", cite)
            plist = expand(m.group(2)) if m else []
            sig = m.group(1) if m else None
            if not plist or any(p not in pages[sig] for p in plist):
                fails += 1
                print(f"FAIL invalid cite: {cite}")
                continue
            blob = " ".join(pages[sig][p] for p in plist)
            if "contains" in it:
                pos += 1
                for t in it["contains"]:
                    if norm(t) not in blob:
                        fails += 1
                        print(f"FAIL positive: {cite} does not contain '{t}' -- {it.get('claim', '')}")
            if "absent" in it:
                neg += 1
                for t in it["absent"]:
                    if re.search(r"(?<![a-z0-9])" + re.escape(norm(t)) + r"(?![a-z0-9])", blob):
                        fails += 1
                        print(f"FAIL negative: {cite} CONTAINS '{t}' -- {it.get('claim', '')}")
    print(f"Checks: {pos} positive, {neg} negative; total failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
