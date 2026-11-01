# -*- coding: utf-8 -*-
"""
compare_approaches.py - approach comparator ACCORDING TO THE TEXT of the package's three sources
(SB3G = Mastering Spring Boot 3.0; QRK = Quarkus Serverless Refcard; MPS = MapStruct 1.6.3 Reference Guide).

Each approach lists only what the source says (with the PDF page) and, at the end, "What the text does NOT say". Nothing comes from memory.
Read-only, stdlib, no network, deterministic.

Usage:
  python -I scripts/compare_approaches.py list
  python -I scripts/compare_approaches.py compare ID [--json]
  python -I scripts/compare_approaches.py find TERM [TERM...]
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

# Portuguese query words still accepted by "find" (mapped to the English words used in the data)
PT_ALIASES = {
    "injecao": "injection", "colecao": "collection", "colecoes": "collection", "teste": "test", "testes": "test",
    "reativo": "reactive", "bloqueante": "blocking", "imagem": "image", "esquema": "schema",
    "configuracao": "configuration", "perfis": "profiles", "autenticacao": "authentication",
    "cliente": "client", "clientes": "clients", "construtor": "constructor", "padroes": "patterns",
    "obter": "obtaining", "abordagens": "approach", "arquitetura": "architectural", "cache": "cache",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load():
    with io.open(os.path.join(HERE, "compare_data.json"), encoding="utf-8") as f:
        return json.load(f)["comparacoes"]


def pg(p):
    return ",".join(str(x) for x in p)


def show(c):
    print(f"## {c['titulo']}  (id: {c['id']})")
    for nome, pts in c["abordagens"].items():
        print(f"\n### {nome}")
        for texto, fonte, pags in pts:
            print(f"- {texto}  [from source: {fonte} p.{pg(pags)}]")
    print("\n### What the text does NOT say (NOT COVERED / [extrapolation] only if requested)")
    for t in c["texto_nao_diz"]:
        print(f"- {t}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list")
    pc = sub.add_parser("compare")
    pc.add_argument("id")
    pc.add_argument("--json", action="store_true")
    pf = sub.add_parser("find")
    pf.add_argument("terms", nargs="+")
    a = ap.parse_args()
    data = load()
    if a.cmd == "list":
        for c in data:
            print(f"{c['id']}: {c['titulo']}")
        return 0
    if a.cmd == "compare":
        for c in data:
            if c["id"] == a.id:
                if a.json:
                    print(json.dumps(c, ensure_ascii=False, indent=1))
                else:
                    show(c)
                return 0
        print(f"Comparison '{a.id}' does not exist. NOT COVERED: the package only compares what the sources address (use 'list').")
        return 1
    if a.cmd == "find":
        toks = [PT_ALIASES.get(norm(t), norm(t)) for t in a.terms]
        hits = []
        for c in data:
            hay = norm(c["id"] + " " + c["titulo"] + " " + " ".join(c["abordagens"].keys()))
            sc = sum(1 for t in toks if t in hay)
            if sc:
                hits.append((sc, c))
        hits.sort(key=lambda x: -x[0])
        if not hits:
            print("NOT COVERED: no comparison in the package matches the term; the sources may not address the topic.")
            return 1
        for _, c in hits:
            print(f"{c['id']}: {c['titulo']}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
