# -*- coding: utf-8 -*-
"""
verify_citations.py - checks the package citations against the texts extracted from the two PDFs.

Checks:
  1. tests/citation-checks.json: positive claims (all terms must appear on the cited PDF page) and
     NEGATIVE claims (plausible statements the sources do NOT contain: terms absent from the WHOLE text or from the page).
  2. scripts/checklist_items.json: each item has its terms on the indicated pages.
  3. scripts/lgpd_nist_mapping.json: LGPD terms on the LGPD pages and NIST terms on the NIST pages of each row.
  4. scripts/privacy_index.json: each LGPD entry cites pages where the article really appears; absent terms (gaps)
     really absent from the sources.
  5. references/*.md and agents/*.md: every citation of the form "(LGPD Art. N ... p.M)" is checked (article N appears on
     PDF page M); "NIST8062 p.N" citations are checked for range (1-49).

Usage (Python 3, stdlib, no network):
  python -I tests/verify_citations.py --src <folder with LGPD-Lei-13709-ptBR.txt and NIST-IR-8062-Privacy-Engineering.txt>
Exit codes: 0 all good; 1 there are failures. Normalization: lowercase, no accents, collapsed spaces, straight quotes,
line-break hyphenation removed.
"""
import argparse
import glob
import io
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
PKG = os.path.dirname(HERE)
FILES = {"LGPD": "LGPD-Lei-13709-ptBR.txt", "NIST8062": "NIST-IR-8062-Privacy-Engineering.txt"}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"-\s*\n\s*(?=[a-z])", "", s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("­", "").replace("‑", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def load_pages(path):
    with io.open(path, "r", encoding="utf-8") as f:
        t = f.read()
    parts = re.split(r"\n?=== PAGE (\d+) ===\n", t)
    pages = {}
    for i in range(1, len(parts), 2):
        pages[int(parts[i])] = parts[i + 1]
    return pages


def has(pages_norm, page, term, whole=False):
    txt = pages_norm.get(page, "")
    t = norm(term)
    if whole:
        return re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", txt) is not None
    return t in txt


def article_pages(raw_pages):
    """art id -> set of pages (from the starting line to the start of the next article)."""
    arts = {}
    cur = None
    for p in sorted(raw_pages):
        for line in raw_pages[p].split("\n"):
            m = re.match(r"^Art\. ?(\d+)(?:\s?-\s?([A-Z]))?[º°]?\.?\s", line)
            if m:
                cur = m.group(1) + ("-" + m.group(2) if m.group(2) else "")
                arts.setdefault(cur, set())
            if cur:
                arts[cur].add(p)
    return arts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    raw = {}
    for k, fn in FILES.items():
        path = os.path.join(a.src, fn)
        if not os.path.exists(path):
            print("ERROR: could not find %s" % path)
            return 2
        raw[k] = load_pages(path)
    pn = {k: {p: norm(t) for p, t in v.items()} for k, v in raw.items()}
    whole = {k: norm("\n".join(raw[k][p] for p in sorted(raw[k]))) for k in raw}
    arts = article_pages(raw["LGPD"])
    fails = []
    npos = nneg = 0

    # 1. citation-checks.json
    with io.open(os.path.join(HERE, "citation-checks.json"), "r", encoding="utf-8") as f:
        cc = json.load(f)
    for c in cc["checks"]:
        npos += 1
        src = c["src"]
        for term in c["contains"]:
            if not has(pn[src], c["page"], term):
                fails.append("POS %s p.%s: term missing %r  (%s)" % (src, c["page"], term, c["claim"]))
    for c in cc["negatives"]:
        nneg += 1
        src = c["src"]
        for term in c["terms"]:
            if c.get("page"):
                present = has(pn[src], c["page"], term, whole=True)
            else:
                t = norm(term)
                present = re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", whole[src]) is not None
            if present:
                fails.append("NEG %s: the term %r EXISTS in the text, but the claim says it is absent  (%s)" % (src, term, c["claim"]))

    # 2. checklist
    with io.open(os.path.join(PKG, "scripts", "checklist_items.json"), "r", encoding="utf-8") as f:
        ck = json.load(f)
    nck = 0
    for it in ck["items"]:
        src = "NIST8062" if it["origem"] == "nist" else "LGPD"
        for term in it["terms"]:
            nck += 1
            if not any(has(pn[src], p, term) for p in it["pages"]):
                fails.append("CHECKLIST %s: term %r missing from pages %s" % (it["id"], term, it["pages"]))
    # 3. mapping
    with io.open(os.path.join(PKG, "scripts", "lgpd_nist_mapping.json"), "r", encoding="utf-8") as f:
        mp = json.load(f)
    nmp = 0
    for r in mp["rows"]:
        for term in r["lgpd_termos"]:
            nmp += 1
            if not any(has(pn["LGPD"], p, term) for p in r["lgpd_paginas"]):
                fails.append("MAP %s: LGPD term %r missing from pages %s" % (r["id"], term, r["lgpd_paginas"]))
        for term in r["nist_termos"]:
            nmp += 1
            if not any(has(pn["NIST8062"], p, term) for p in r["nist_paginas"]):
                fails.append("MAP %s: NIST term %r missing from pages %s" % (r["id"], term, r["nist_paginas"]))
    # 4. index
    with io.open(os.path.join(PKG, "scripts", "privacy_index.json"), "r", encoding="utf-8") as f:
        ix = json.load(f)
    nix = 0
    for e in ix["entries"]:
        if e["src"] != "LGPD":
            for p in e["pages"]:
                if p not in raw["NIST8062"]:
                    fails.append("INDEX %s: page %s does not exist" % (e["id"], p))
            continue
        for art in e["arts"]:
            nix += 1
            ap_ = arts.get(art)
            if not ap_:
                fails.append("INDEX %s: Art. %s not found in the text" % (e["id"], art))
            elif not (set(e["pages"]) & ap_):
                fails.append("INDEX %s: pages %s do not match those of Art. %s (%s)" % (e["id"], e["pages"], art, sorted(ap_)))
    for src, terms in ix["gaps"].items():
        for t in terms:
            nneg += 1
            tn = norm(t)
            if re.search(r"(?<![a-z0-9])" + re.escape(tn) + r"(?![a-z0-9])", whole[src]):
                fails.append("GAP %s: term %r appears in the text, but is listed as absent" % (src, t))
    for am in ix["amendments"]:
        nix += 1
        if am["page"] not in raw["LGPD"]:
            fails.append("AMENDMENT invalid page: %s" % am)
        elif am["lei"]:
            tag = "lei n %s" % am["lei"]
            tag2 = "lei nº %s" % am["lei"]
            if norm("Lei nº %s, de %s" % (am["lei"], am["ano"])) not in whole["LGPD"] and norm("Lei nº %s" % am["lei"]) not in whole["LGPD"]:
                fails.append("AMENDMENT law not found in the text: %s" % am)

    # 5. refs
    nref = 0
    cite_art = re.compile(r"Art\. ?(\d+(?:-[A-Z])?)º?[^()\n;]{0,70}?\bp\.(\d+)(?:-(\d+))?")
    cite_nist = re.compile(r"NIST8062 ?(?:[^()\n]{0,40}?)p\.(\d+)(?:-(\d+))?")
    mdfiles = glob.glob(os.path.join(PKG, "references", "*.md")) + glob.glob(os.path.join(PKG, "agents", "*.md")) + [os.path.join(PKG, "README.md"), os.path.join(PKG, "AGENTS.md")]
    for fp in [x for x in mdfiles if os.path.exists(x)]:
        with io.open(fp, "r", encoding="utf-8") as f:
            txt = f.read()
        for lineno, line in enumerate(txt.split("\n"), 1):
            if "LGPD" not in line and "Art." not in line:
                continue
            for m in cite_art.finditer(line):
                # only checks citations inside parentheses/brackets such as [from source] (LGPD Art. ..., p.N)
                art = m.group(1)
                p1 = int(m.group(2)); p2 = int(m.group(3)) if m.group(3) else p1
                nref += 1
                ap_ = arts.get(art)
                if not ap_:
                    fails.append("REF %s:%d Art. %s does not exist" % (os.path.basename(fp), lineno, art))
                    continue
                if not (set(range(p1, p2 + 1)) & ap_):
                    fails.append("REF %s:%d Art. %s cited at p.%s-%s, but appears at %s" % (os.path.basename(fp), lineno, art, p1, p2, sorted(ap_)))
        for lineno, line in enumerate(txt.split("\n"), 1):
            for m in cite_nist.finditer(line):
                p1 = int(m.group(1)); p2 = int(m.group(2)) if m.group(2) else p1
                nref += 1
                if p1 < 1 or p2 > 49 or p2 < p1:
                    fails.append("REF %s:%d NIST8062 page out of range: %s" % (os.path.basename(fp), lineno, m.group(0)))
    print("Positive checks (citation-checks): %d | negatives+gaps: %d | checklist (terms): %d | map (terms): %d | index: %d | citations in .md: %d"
          % (npos, nneg, nck, nmp, nix, nref))
    if fails:
        print("FAILURES (%d):" % len(fails))
        for x in fails:
            print(" - " + x)
        return 1
    print("OK: all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
