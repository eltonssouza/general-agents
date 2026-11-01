# -*- coding: utf-8 -*-
"""
map_lgpd_nist.py - maps LGPD (Lei Geral de Proteção de Dados, Brazil's General Data Protection Law) concepts/articles to the
NIST IR 8062 privacy engineering objectives (predictability, manageability, disassociability) ONLY where there is
textual support; the rest is [inference] or NO SUPPORT.

Levels (see scripts/lgpd_nist_mapping.json):
  TEXTUAL     NIST links the concept/objective (Fig. 8, 3.1.1.x, glossary) AND both texts use equivalent terms
              verifiable on the cited pages. Neither source cites the other: the LGPD<->NIST correspondence is
              made by the agent and must be presented as a comparison, not as a legal rule.
  INFERENCE   conceptual link without direct textual support: label it [inference].
  NO_SUPPORT  LGPD topic with no equivalent in NIST IR 8062.

Usage (Python 3, stdlib, no network; run with `python -I`):
  python -I scripts/map_lgpd_nist.py table [--level TEXTUAL|INFERENCE|NO_SUPPORT] [--objective predictability]
  python -I scripts/map_lgpd_nist.py by-objective            # groups by NIST objective
  python -I scripts/map_lgpd_nist.py art 6                   # rows that cite the article
  python -I scripts/map_lgpd_nist.py nist-only               # NIST concepts with no LGPD counterpart
  python -I scripts/map_lgpd_nist.py markdown [--out ARQ.md]
Pages = PDF. This is not legal advice.
"""
import argparse
import io
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "lgpd_nist_mapping.json")
LABEL = {"TEXTUAL": "[from source + agent comparison]", "INFERENCE": "[inference]", "NO_SUPPORT": "NO SUPPORT"}
LEVELS = ["TEXTUAL", "INFERENCE", "NO_SUPPORT"]
AVISO = "Notice: the sources do not cite each other; the mapping is an engineering tool, not a legal interpretation. Consult a lawyer/the encarregado (DPO)."


def load():
    with io.open(DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def pg(p):
    return ",".join(str(x) for x in p) if p else "-"


def fmt(r):
    s = "%s %s %s\n   LGPD: %s (p.%s)\n   NIST: %s (p.%s)\n   Objective: %s\n   Why: %s" % (
        r["id"], r["nivel"], LABEL[r["nivel"]], r["lgpd"], pg(r["lgpd_paginas"]), r["nist"], pg(r["nist_paginas"]),
        r["objetivo"] or "-", r["justificativa"])
    return s


def arts_of(txt):
    """Articles cited in the LGPD column (includes ranges such as 'Art. 33-36'); 55-A etc. count as '55-A'."""
    out = set()
    for m in re.finditer(r"Art\.? ?(\d+)(?:º)?(?:-([A-Z]))?(?:-(\d+))?", txt):
        a1 = m.group(1)
        if m.group(2):
            out.add("%s-%s" % (a1, m.group(2)))
            out.add(a1)
        elif m.group(3):
            for x in range(int(a1), int(m.group(3)) + 1):
                out.add(str(x))
        else:
            out.add(a1)
    for m in re.finditer(r"Art\. ?(\d+)º?, [IVX]+(?:, [a-z])?(?: e | a |, )?(?:Art\. )?", txt):
        out.add(m.group(1))
    return out


def select(d, a):
    rows = d["rows"]
    if getattr(a, "level", None):
        rows = [r for r in rows if r["nivel"] == a.level]
    if getattr(a, "objective", None):
        rows = [r for r in rows if a.objective.lower() in r["objetivo"].lower()]
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd")
    p = sp.add_parser("table"); p.add_argument("--level", "--nivel", dest="level", choices=LEVELS); p.add_argument("--objective", "--objetivo", dest="objective")
    sp.add_parser("by-objective")
    p = sp.add_parser("art"); p.add_argument("numero")
    sp.add_parser("nist-only")
    p = sp.add_parser("markdown"); p.add_argument("--out")
    a = ap.parse_args()
    d = load()
    if a.cmd == "table":
        for r in select(d, a):
            print(fmt(r)); print()
        print(AVISO)
        return 0
    if a.cmd == "by-objective":
        for obj in ("predictability", "manageability", "disassociability"):
            print("== %s ==" % obj)
            for r in d["rows"]:
                if obj in r["objetivo"].lower():
                    print("  %s %-10s %s (LGPD p.%s) <-> %s" % (r["id"], r["nivel"], r["lgpd"], pg(r["lgpd_paginas"]), r["nist"].split(";")[0]))
        print("\nOthers (not tied to one of the three objectives): security (CIA), privacy problems, risk model, PIA, life cycle.")
        print(AVISO)
        return 0
    if a.cmd == "art":
        n = a.numero.strip().lstrip("0")
        rows = [r for r in d["rows"] if n in arts_of(r["lgpd"])]
        if not rows:
            print("NO MAPPING for Art. %s (the mapper only covers articles with a conceptual counterpart in NIST or listed as NO SUPPORT)." % n)
            return 0
        for r in rows:
            print(fmt(r)); print()
        print(AVISO)
        return 0
    if a.cmd == "nist-only":
        for x in d["nist_sem_lgpd"]:
            print("- %s (NIST p.%s)\n  %s" % (x["conceito"], pg(x["paginas"]), x["obs"]))
        return 0
    if a.cmd == "markdown":
        out = ["# LGPD <-> NIST IR 8062 map (privacy engineering objectives)", "",
               "Levels: " + "; ".join("**%s** = %s" % (k, v) for k, v in d["niveis"].items()), "",
               "> " + AVISO, "",
               "| Id | Level | LGPD (PDF pages) | NIST IR 8062 (PDF pages) | Objective |", "|---|---|---|---|---|"]
        for r in d["rows"]:
            out.append("| %s | %s | %s (p.%s) | %s (p.%s) | %s |" % (r["id"], r["nivel"], r["lgpd"], pg(r["lgpd_paginas"]), r["nist"], pg(r["nist_paginas"]), r["objetivo"] or "-"))
        out += ["", "## NIST concepts with no LGPD counterpart", ""]
        for x in d["nist_sem_lgpd"]:
            out.append("- %s (NIST p.%s): %s" % (x["conceito"], pg(x["paginas"]), x["obs"]))
        md = "\n".join(out) + "\n"
        if a.out:
            with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
                f.write(md)
            print("written: %s" % a.out)
        else:
            sys.stdout.write(md)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
