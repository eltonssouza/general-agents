# -*- coding: utf-8 -*-
"""
verify_citations.py - audits citations (ACRONYM p.N) against the text extracted from the 6 PDFs of the collection.

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/frameworks [--pkg PACKAGE_ROOT] [--checks file.json ...]

Acronyms and files (in --src):
  NX13 NextJS-13-Release.txt (16 pages)   NX14 NextJS-14-Release.txt (13)   NX15 NextJS-15-Release.txt (22)
  NX16 NextJS-16-Release.txt (16)         NXHB NextJS-Handbook-freeCodeCamp.txt (91)   RCTHB React-Handbook-freeCodeCamp.txt (35)
Page convention: N = PDF page ("=== PAGE N ===" marker of the extracted text); the PDFs have no printed number.

1) Range: every citation "ACRONYM p.N[-M][, ...]" in the package's .md/.json/.py files must exist (1..page count of the source).
2) Data: every entry of scripts/nx_changes.json and nx_index.json has valid pages; every command (cmds) appears in the
   text of the cited pages (compared ignoring spaces/line breaks).
3) Positive: item {"cite","contains":[...]} -> ALL substrings appear in the cited pages (normalized:
   lowercase, collapsed whitespace, straight quotes).
4) Negative: item {"cite","absent":[...]} -> NONE of the terms (whole word) appears in the cited pages
   (plausible claims that the source does NOT make).
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

FILES = {
    "NX13": ("NextJS-13-Release.txt", 16), "NX14": ("NextJS-14-Release.txt", 13),
    "NX15": ("NextJS-15-Release.txt", 22), "NX16": ("NextJS-16-Release.txt", 16),
    "NXHB": ("NextJS-Handbook-freeCodeCamp.txt", 91), "RCTHB": ("React-Handbook-freeCodeCamp.txt", 35),
}
CITE_RE = re.compile(r"\b(NX13|NX14|NX15|NX16|NXHB|RCTHB)\s+p\.\s*(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("​", "")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for part in re.split(r"\s*,\s*", spec.strip()):
        m = re.match(r"(\d+)\s*[-–]\s*(\d+)$", part)
        if m:
            pages += list(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            pages.append(int(part))
    return pages


def parse_cite(c):
    m = CITE_RE.search(c)
    if not m:
        return None, []
    return m.group(1), expand(m.group(2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    ap.add_argument("--checks", nargs="*")
    a = ap.parse_args()
    pkg = os.path.abspath(a.pkg)
    docs = {}
    for sig, (fn, n) in FILES.items():
        p = os.path.join(a.src, fn)
        if not os.path.exists(p):
            print(f"FAIL: text not found: {p}")
            sys.exit(2)
        docs[sig] = load_pages(p)
        if len(docs[sig]) != n:
            print(f"FAIL: {sig} has {len(docs[sig])} pages in the text, expected {n}")
            sys.exit(2)
    fails = []
    stats = {"range": 0, "data": 0, "pos": 0, "neg": 0, "cmd": 0}

    # 1) range
    for root, dirs, fs in os.walk(pkg):
        for f in fs:
            if not f.endswith((".md", ".json", ".py")) or f == "verify_citations.py":
                continue
            fp = os.path.join(root, f)
            txt = open(fp, encoding="utf-8", errors="replace").read()
            for m in CITE_RE.finditer(txt):
                sig = m.group(1)
                for p in expand(m.group(2)):
                    stats["range"] += 1
                    if not 1 <= p <= FILES[sig][1]:
                        fails.append(f"range: {os.path.relpath(fp, pkg)}: '{sig} p.{p}' outside 1..{FILES[sig][1]}")

    # 2) data
    for fn in ("scripts/nx_changes.json", "scripts/nx_index.json"):
        d = json.load(open(os.path.join(pkg, fn), encoding="utf-8"))
        if "entries" in d:
            for e in d["entries"]:
                sig = f"NX{e['v']}"
                stats["data"] += 1
                for p in e["pages"]:
                    if p not in docs[sig]:
                        fails.append(f"data: {e['id']} page {p} does not exist in {sig}")
                blob = " ".join(squash(docs[sig].get(p, "")) for p in e["pages"])
                for c in e.get("cmds", []):
                    stats["cmd"] += 1
                    if squash(c) not in blob:
                        fails.append(f"data: {e['id']} command '{c}' is not on pages {e['pages']} of {sig}")
        for sec in ("topicos", "conflitos"):
            for t in d.get(sec, []):
                if sec == "topicos":
                    ref = [(t["fonte"], t["paginas"])]
                else:
                    ref = [(t["datado"]["fonte"], t["datado"]["paginas"]), (t["release"]["fonte"], t["release"]["paginas"])]
                for sig, pgs in ref:
                    stats["data"] += 1
                    for p in pgs:
                        if p not in docs[sig]:
                            fails.append(f"data: {sec} {t.get('id', t.get('tema'))} page {p} does not exist in {sig}")

    # 3/4) checks
    cks = a.checks or [os.path.join(pkg, "tests", "citation-checks.json")]
    for ck in cks:
        data = json.load(open(ck, encoding="utf-8"))
        for it in data["checks"]:
            sig, pgs = parse_cite(it["cite"])
            if not sig:
                fails.append(f"check without a valid citation: {it['cite']}")
                continue
            blob = " ".join(norm(docs[sig].get(p, "")) for p in pgs)
            for term in it.get("contains", []):
                stats["pos"] += 1
                if norm(term) not in blob:
                    fails.append(f"POSITIVE failed: {it['cite']} does not contain '{term}' ({it.get('claim', '')})")
            for term in it.get("absent", []):
                stats["neg"] += 1
                if re.search(r"(?<![\w])" + re.escape(norm(term)) + r"(?![\w])", blob):
                    fails.append(f"NEGATIVE failed: {it['cite']} CONTAINS '{term}' ({it.get('claim', '')})")

    print(f"citations checked in range: {stats['range']}; data entries: {stats['data']}; commands checked: {stats['cmd']}; "
          f"positive terms: {stats['pos']}; negative terms: {stats['neg']}")
    if fails:
        for f in fails:
            print("FAIL:", f)
        print(f"{len(fails)} failure(s)")
        sys.exit(1)
    print("OK: all checks passed")


if __name__ == "__main__":
    main()
