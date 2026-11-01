# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS in `backticks` against the cited page(s).

For each group of consecutive citations "(SIGLA p.N) (SIGLA p.M)" in references/*.md, takes the terms in backticks
from the text before the group (since the previous group on the same line) and checks whether they appear on ANY of the pages
of the group. Terms with spaces, placeholders (<...>, ...), script paths, or very short ones are ignored.
If the term is not on the cited pages but is on a neighboring one (±1), it warns NEAR; if it is not even close, FAIL.

Usage: python -I tests/audit_tokens.py --src PATH/src [--pkg ROOT] [--strict] [--verbose]
Exit 0 without FAIL (NEAR counts as a failure with --strict).
"""
import argparse
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
CITE = re.compile(r"\((" + SIGLAS + r") p\.([\d,\-–\s]+)\)")


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("�", "'").replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("‐", "-").replace("‑", "-").replace("­", "")
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
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    SQ = {}
    for sig in NPAGES:
        pg = load_pages(os.path.join(a.src, sig + ".txt"))
        SQ[sig] = {k: squash(norm(v)) for k, v in pg.items()}
    refs = os.path.join(a.pkg, "references")
    checked = near = fail = 0
    for fn in sorted(os.listdir(refs)):
        if not fn.endswith(".md") or fn.startswith("INDEX") or fn.startswith("glossario"):
            continue
        for ln, line in enumerate(open(os.path.join(refs, fn), encoding="utf-8"), 1):
            ms = list(CITE.finditer(line))
            if not ms:
                continue
            groups = []
            for m in ms:
                gap = line[groups[-1][-1].end():m.start()] if groups else None
                if groups and re.fullmatch(r"[\s,;]*(\[[^\]]*\]\s*)?", gap or ""):
                    groups[-1].append(m)
                else:
                    groups.append([m])
            prev_end = 0
            for g in groups:
                seg = line[prev_end:g[0].start()]
                prev_end = g[-1].end()
                cites = []
                for m in g:
                    cites.append((m.group(1), expand(m.group(2))))
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if " " in t0 or "<" in t0 or "..." in t0 or t0.endswith((".md", ".py", ".json")) or t0.startswith(("scripts/", "references/", "tests/", "python", "--")):
                        continue
                    if "{" in t0 or "^" in t0 or "(" in t0 and not t0.endswith("()"):
                        continue
                    t = re.sub(r"\(\)$", "", t0).strip(",.;")
                    if len(t) < 4 or re.fullmatch(r"[0-9.%]+", t):
                        continue
                    st = squash(norm(t))
                    checked += 1
                    hit = any(st in SQ[sig].get(p, "") for sig, pl in cites for p in pl)
                    if hit:
                        continue
                    nb = any(st in SQ[sig].get(p, "") for sig, pl in cites for q in pl for p in (q - 1, q + 1))
                    where = ", ".join(f"{s} p.{','.join(map(str, pl))}" for s, pl in cites)
                    if nb:
                        near += 1
                        print(f"NEAR   {fn}:{ln}: `{t}` is not in {where}, but is on a neighboring page")
                    else:
                        fail += 1
                        print(f"FAIL   {fn}:{ln}: `{t}` not found in {where}")
    print(f"Terms checked: {checked}; near: {near}; failures: {fail}")
    sys.exit(1 if (fail or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
