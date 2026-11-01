# -*- coding: utf-8 -*-
"""
lambda_lookup.py - deterministic lookup in the lambda_index.json index and the references (read-only, no network).

Usage:
  python -I lambda_lookup.py snapstart          # topic by key/keyword
  python -I lambda_lookup.py "visibility timeout"
  python -I lambda_lookup.py --list             # list topics
  python -I lambda_lookup.py provisioned --text # besides the index, shows reference lines that contain the term
  python -I lambda_lookup.py kinesis --json

Queries may be in English or Portuguese (the index keeps Portuguese keywords).
Each answer carries pages (LAMBDA p.N, PDF page; printed = N-22), reference file, [DATED] items and gaps.
If nothing is found it says "NOT COVERED" (it does not invent a page). Coverage: 2022 edition of the guide.
"""
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
IDX = json.load(open(os.path.join(HERE, "lambda_index.json"), encoding="utf-8"))


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def wb(a, b):
    """a appears in b as a whole word/sequence (prevents 'stream' from matching 'streaming')."""
    return re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", b) is not None


def score(q, t):
    nq = norm(q)
    s = 0
    if nq == norm(t["key"]):
        s += 100
    for k in t["keywords"]:
        nk = norm(k)
        if nq == nk:
            s += 60
        elif wb(nq, nk) or wb(nk, nq):
            s += 25
    if wb(nq, norm(t["name"])):
        s += 20
    if wb(nq, norm(t["summary"])):
        s += 8
    return s


def text_hits(q, limit=12):
    nq = norm(q)
    out = []
    refdir = os.path.join(PKG, "references")
    for fn in sorted(os.listdir(refdir)):
        if not fn.endswith(".md"):
            continue
        for i, line in enumerate(open(os.path.join(refdir, fn), encoding="utf-8"), 1):
            if wb(nq, norm(line)) and line.startswith("- "):
                out.append((fn, i, line.strip()[:260]))
    return out[:limit], len(out)


def show(t):
    print(f"TOPIC: {t['name']} [{t['key']}]")
    print(f"PAGES: LAMBDA p.{t['pages']}  (PDF page; printed = N-22)")
    print(f"REFERENCE: {t['reference_file']}")
    print("SUMMARY: " + t["summary"])
    if t.get("datado"):
        print("[DATED]: " + t["datado"])
    if t.get("gaps"):
        print("GAPS: " + t["gaps"])
    print()


def main(argv):
    as_json = "--json" in argv
    with_text = "--text" in argv
    args = [a for a in argv if not a.startswith("--")]
    if "--list" in argv:
        for t in IDX["topics"]:
            print(f"{t['key']:22} p.{t['pages']:28} {t['name']}")
        return 0
    if not args:
        print(__doc__)
        return 2
    q = " ".join(args)
    ranked = sorted(((score(q, t), t) for t in IDX["topics"]), key=lambda x: -x[0])
    ranked = [(s, t) for s, t in ranked if s > 0][:4]
    hits, total = text_hits(q) if (with_text or not ranked) else ([], 0)
    if as_json:
        print(json.dumps({"query": q, "topics": [t for _, t in ranked], "text_hits": hits, "coverage": bool(ranked or hits)}, ensure_ascii=False, indent=1))
        return 0
    # Portuguese alternates stay: the references are still written in Portuguese
    gap_re = re.compile(r"(?i)(nao cobre|nao constam|nao consta|nao traz|nao e coberto|fora do acervo|extrapola|not covered|does not cover|not included|outside the collection)")
    real = [h for h in hits if h[0] != "lacunas-e-fronteiras.md" and not gap_re.search(norm(h[2]))]
    if not ranked and not real:
        if hits:
            print("Note: the collection only mentions the ABSENCE of the term:")
            for fn, i, l in hits[:3]:
                print(f"  references/{fn}:{i}: {l[:200]}")
        print(f"NOT COVERED: the collection (AWS Lambda Developer Guide, 2022 edition) does not contain '{q}'. Do not cite a page; treat as [extrapolation] and recommend checking the current documentation.")
        return 1
    for s, t in ranked:
        show(t)
    if hits:
        print(f"EXCERPTS IN THE REFERENCES ({len(hits)} of {total}):")
        for fn, i, l in hits:
            print(f"  references/{fn}:{i}: {l}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
