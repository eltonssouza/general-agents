# -*- coding: utf-8 -*-
"""
compare_frameworks.py - side-by-side comparator of Django (DJT), Flask (FLT) and FastAPI (FAPI) ONLY on criteria
that the sources provide. Each cell carries what the source says with the PDF page, or "NOT COVERED". Nothing comes from memory.
Note: the FLT is only an index/introduction; most Flask cells will be NOT COVERED or "only a section title".

Read-only, stdlib, no network, deterministic.

Usage:
  python -I scripts/compare_frameworks.py list
  python -I scripts/compare_frameworks.py compare [ID ...] [--only DJT,FAPI] [--json]   (no ID = all criteria)
  python -I scripts/compare_frameworks.py find TERM [TERM...]
  python -I scripts/compare_frameworks.py coverage     (how many cells have content per framework)
Criterion IDs are the (Portuguese-derived) ids printed by `list`; English aliases are also accepted
(e.g. installation, dev-server, routing, database, testing, performance, license).
"""
import argparse
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
ORDER = ["DJT", "FLT", "FAPI"]

# English aliases -> criterion ids (the ids themselves stay unchanged)
ALIASES = {
    "nature": "natureza", "python-version": "versao-python", "installation": "instalacao",
    "project-structure": "estrutura-projeto", "dev-server": "servidor-dev", "reload": "recarga",
    "routing": "roteamento", "validation-conversion": "validacao-conversao", "auto-docs": "docs-automaticas",
    "database": "banco-dados", "testing": "testes", "tests": "testes", "security-auth": "seguranca-auth",
    "packaging": "empacotamento", "dependencies": "dependencias", "performance": "desempenho", "license": "licenca",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "compare_data.json"), encoding="utf-8") as f:
        return json.load(f)


def pg(p):
    return ",".join(str(x) for x in p)


def cell_text(cell):
    if cell is None:
        return "NOT COVERED"
    texto, fonte, pags = cell
    return f"{texto}  [from source: {fonte} p.{pg(pags)}]"


def show(crit, only):
    print(f"## {crit['titulo']}  (id: {crit['id']})")
    for k in ORDER:
        if only and k not in only:
            continue
        print(f"- {k}: {cell_text(crit['celulas'].get(k))}")
    print()


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list")
    c = sub.add_parser("compare")
    c.add_argument("ids", nargs="*")
    c.add_argument("--only", help="comma-separated list of source codes (DJT,FLT,FAPI)")
    c.add_argument("--json", action="store_true")
    f = sub.add_parser("find")
    f.add_argument("terms", nargs="+")
    sub.add_parser("coverage")
    a = ap.parse_args()
    data = load()
    crits = data["criterios"]

    if a.cmd == "list":
        for c_ in crits:
            print(f"{c_['id']}: {c_['titulo']}")
        return 0
    if a.cmd == "coverage":
        for k in ORDER:
            n = sum(1 for c_ in crits if c_["celulas"].get(k))
            print(f"{k}: {n}/{len(crits)} criteria with some content; {len(crits) - n} NOT COVERED")
        print("Note: FLT cells with content are mostly just tutorial index section titles.")
        return 0
    if a.cmd == "compare":
        only = None
        if a.only:
            only = [x.strip().upper() for x in a.only.split(",") if x.strip()]
            bad = [x for x in only if x not in ORDER]
            if bad:
                print(f"Unknown source codes: {','.join(bad)}. Use DJT, FLT, FAPI.")
                return 2
        sel = crits
        if a.ids:
            byid = {c_["id"]: c_ for c_ in crits}
            ids = [ALIASES.get(i.lower(), i) for i in a.ids]
            miss = [i for i in ids if i not in byid]
            if miss:
                print(f"Nonexistent criterion(s): {', '.join(miss)}. NOT COVERED: the package only compares criteria the sources address (use 'list').")
                return 1
            sel = [byid[i] for i in ids]
        if a.json:
            out = []
            for c_ in sel:
                out.append({"id": c_["id"], "titulo": c_["titulo"],
                            "celulas": {k: ({"texto": c_["celulas"][k][0], "fonte": c_["celulas"][k][1], "paginas": c_["celulas"][k][2]}
                                            if c_["celulas"].get(k) else "NOT COVERED")
                                        for k in ORDER if not only or k in only}})
            print(json.dumps(out, ensure_ascii=False, indent=1))
            return 0
        for k, v in data["fontes"].items():
            if not only or k in only:
                print(f"{k} = {v}")
        print()
        for c_ in sel:
            show(c_, only)
        print("Outside the cells: " + "; ".join(data["nao_comparavel"]))
        return 0
    if a.cmd == "find":
        toks = [norm(t) for t in a.terms]
        hits = []
        for c_ in crits:
            hay = norm(c_["id"] + " " + c_["titulo"] + " " + " ".join(x[0] for x in c_["celulas"].values() if x))
            sc = sum(1 for t in toks if t in hay)
            if sc:
                hits.append((sc, c_))
        hits.sort(key=lambda x: -x[0])
        if not hits:
            print("NOT COVERED: no comparator criterion matches the term; the sources may not address the subject.")
            return 0
        for _, c_ in hits:
            print(f"{c_['id']}: {c_['titulo']}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
