# -*- coding: utf-8 -*-
"""
llm_lookup.py - locates LLMS and PES topics and prints pages (PDF = printed), reference file and labels.

Sources (closed collection):
  LLMS = "A Survey of Large Language Models" (Zhao et al.), arXiv 2303.18223v19, 18 Mar 2026 [DATED]; body p.1-99; p.100-144 = bibliographic references.
  PES  = "A Systematic Survey of Prompt Engineering in LLMs" (Sahoo et al.), arXiv 2402.07927v2, 16 Mar 2025 [DATED]; body p.1-10.

Usage:
  python -I scripts/llm_lookup.py TERMO [--source LLMS|PES] [--top N] [--json]
  python -I scripts/llm_lookup.py --page N --source LLMS|PES
  python -I scripts/llm_lookup.py --sections [--source LLMS|PES]
  python -I scripts/llm_lookup.py --gaps
  python -I scripts/llm_lookup.py --datado
Read-only, stdlib, no network. Missing term -> "NOT COVERED".
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
MAXP = {"LLMS": 144, "PES": 12}
BODY = {"LLMS": (1, 99), "PES": (1, 10)}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9@.+\-' ]+", " ", s.lower()).strip()


def expand(spec):
    out = []
    for tok in spec.split(","):
        m = re.fullmatch(r"\s*(\d+)(?:-(\d+))?\s*", tok)
        if m:
            a = int(m.group(1))
            out.append((a, int(m.group(2) or a)))
    return out


def load():
    with open(os.path.join(HERE, "llm_index.json"), encoding="utf-8") as f:
        idx = json.load(f)
    try:
        with open(os.path.join(HERE, "pes_techniques.json"), encoding="utf-8") as f:
            idx["_tecnicas"] = json.load(f)["tecnicas"]
    except Exception:
        idx["_tecnicas"] = []
    return idx


def score(q, topic):
    qn = norm(q)
    if not qn:
        return 0
    qt = [w for w in qn.split() if len(w) > 1 or w.isdigit()]
    s = 0
    title = norm(topic["title"])
    kws = [norm(k) for k in topic["keywords"]]
    for k in kws:
        if qn == k:
            s += 10
        elif re.search(r"(?<![a-z0-9])" + re.escape(qn) + r"(?![a-z0-9])", k):
            s += 5
    if re.search(r"(?<![a-z0-9])" + re.escape(qn) + r"(?![a-z0-9])", title):
        s += 6
    if s == 0:
        # all tokens present in keywords/title (any order)
        blob = " ".join(kws) + " " + title
        if qt and all(re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", blob) for t in qt):
            s += 2
    return s


def in_gaps(q, idx):
    qn = norm(q)
    hits = []
    for g in idx["nao_coberto"]:
        gt = norm(g["termo"])
        parts = [norm(x) for x in re.split(r"[/;]", g["termo"])] + [gt]
        if any(p and (qn == p or (len(qn) > 3 and qn in p) or (len(p) > 3 and p in qn)) for p in parts):
            hits.append(g)
    return hits


def find_pages_for_technique(idx, q):
    qn = norm(q)
    res = []
    for t in idx["_tecnicas"]:
        if qn and (qn == norm(t["id"]) or qn == norm(t["name"]) or (len(qn) > 3 and qn in norm(t["name"]))):
            res.append(t)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("termo", nargs="*")
    ap.add_argument("--source", choices=["LLMS", "PES"])
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--page", type=int)
    ap.add_argument("--sections", action="store_true")
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--datado", action="store_true")
    a = ap.parse_args()
    idx = load()

    if a.gaps:
        print("NOT COVERED, verified (text search over the body read):")
        for g in idx["nao_coberto"]:
            print(f"  - {g['termo']}: {g['nota']}")
        print("Reading: " + idx["nao_lido"])
        return
    if a.datado:
        print("[DATED] items that age (source PES Mar/2025; LLMS v19 Mar/2026):")
        for d in idx["datado"]:
            print(f"  - {d['item']} ({d['paginas']})")
        return
    if a.sections:
        for src, rows in idx["secoes"].items():
            if a.source and a.source != src:
                continue
            print(f"{src}:")
            for sid, name, pg in rows:
                print(f"  {sid}: {name} -> {src} p.{pg}")
        return
    if a.page is not None:
        src = a.source or "LLMS"
        n = a.page
        if n < 1 or n > MAXP[src]:
            print(f"{src} has {MAXP[src]} pages; p.{n} is out of range.")
            sys.exit(2)
        lo, hi = BODY[src]
        if n > hi and src == "LLMS":
            print(f"{src} p.{n}: BIBLIOGRAPHIC REFERENCES (not used as content). Convention: PDF = printed.")
            return
        if n > hi and src == "PES":
            print(f"{src} p.{n}: bibliographic references (only for authors/titles). Convention: PDF = printed.")
            return
        print(f"{src} p.{n} (PDF = printed):")
        for sid, name, pg in idx["secoes"][src]:
            for lo2, hi2 in expand(pg):
                if lo2 <= n <= hi2 and sid not in ("Fig.2",):
                    print(f"  section {sid}: {name} (p.{pg})")
        found = 0
        for t in idx["topicos"]:
            if t["source"] != src:
                continue
            for lo2, hi2 in expand(t["pages"]):
                if lo2 <= n <= hi2:
                    print(f"  topic: {t['title']} -> references/{idx['refs'][t['ref']]} (p.{t['pages']})")
                    found += 1
                    break
        if src == "PES":
            for t in idx["_tecnicas"]:
                for lo2, hi2 in expand(t["pages"]):
                    if lo2 <= n <= hi2:
                        print(f"  technique: {t['name']} (PES p.{t['pages']})")
                        break
        return
    q = " ".join(a.termo).strip()
    if not q:
        ap.print_help()
        return
    rows = []
    for t in idx["topicos"]:
        if a.source and t["source"] != a.source:
            continue
        s = score(q, t)
        if s:
            rows.append((s, t))
    rows.sort(key=lambda r: (-r[0], r[1]["source"], r[1]["id"]))
    techs = [] if a.source == "LLMS" else find_pages_for_technique(idx, q)
    gap = in_gaps(q, idx)
    if not rows and not techs:
        if gap:
            print(f"NOT COVERED: '{q}' -> {gap[0]['nota']}")
        else:
            print(f"NOT COVERED: '{q}' is not in the LLMS index (p.1-99) or the PES index (p.1-10). It may exist elsewhere, but this package does not cover it: see --gaps.")
        sys.exit(2)
    rows = rows[: a.top]
    if a.json:
        print(json.dumps({"termo": q,
                          "resultados": [{"fonte": t["source"], "titulo": t["title"], "paginas": f"{t['source']} p.{t['pages']}",
                                          "ref": "references/" + idx["refs"][t["ref"]], "score": s} for s, t in rows],
                          "tecnicas_pes": [{"name": t["name"], "paginas": f"PES p.{t['pages']}"} for t in techs],
                          "aviso": "[DATED] sources from Mar/2025 (PES) and Mar/2026 with content mostly up to 2025 (LLMS)"},
                         ensure_ascii=False, indent=1))
        return
    for s, t in rows:
        print(f"[{t['source']}] {t['title']}\n    pages: {t['source']} p.{t['pages']}  |  reference: references/{idx['refs'][t['ref']]}  (score {s})")
    for t in techs:
        print(f"[PES] technique {t['name']} -> PES p.{t['pages']}; Table 1 at PES p.10; prompt acquisition {t['acquisition']}, turns {t['turn']}")
    print("Convention: PDF page = printed page. [DATED]: PES Mar/2025; LLMS v19 Mar/2026 (content mostly up to 2025).")


if __name__ == "__main__":
    main()
