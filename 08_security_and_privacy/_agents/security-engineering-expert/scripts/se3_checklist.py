# -*- coding: utf-8 -*-
"""
se3_checklist.py - security engineering review checklist anchored in "Security Engineering" (Ross Anderson, 3rd ed., SE3).

Stdlib, no network, read-only. Run with: python -I scripts/se3_checklist.py COMMAND
  areas                         lists the areas and the number of items
  list [--area A]               lists items (id, question, PDF pages)
  markdown [--area A ...]       generates a Markdown checklist to paste into a review document
  evaluate FILE.json            evaluates answers {"ID": "yes|no|partial|na", ...}; lists pending items with page
                                (Portuguese answers sim|nao|parcial are also accepted)
Area names: the Portuguese keys (oponentes, senhas, protocolos, cripto, acesso, economia, politicas, bancos, selos,
biometria, rede, devsec, assurance, ml) or the English aliases (see 'areas').
Convention: pages = PDF (printed = PDF - chapter offset; see references/INDEX.md).
Labels: the QUESTION is [inference] (checklist form); the PAGE indicates where the book presents the principle ([from source]).
This checklist helps structure the review; it is NOT a formal security review and does not replace specialists, penetration testing or audit.
"""
import argparse
import io
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))

# English aliases for the area keys (the Portuguese keys remain valid).
AREA_ALIASES = {"opponents": "oponentes", "passwords": "senhas", "protocols": "protocolos", "crypto": "cripto",
                "access": "acesso", "economics": "economia", "policies": "politicas", "banking": "bancos",
                "seals": "selos", "biometrics": "biometria", "network": "rede"}
# Answer normalization: English and Portuguese accepted; canonical form is English.
ANSWER_ALIASES = {"yes": "yes", "sim": "yes", "no": "no", "nao": "no", "não": "no", "partial": "partial",
                  "parcial": "partial", "na": "na", "n/a": "na"}


def load():
    with io.open(os.path.join(HERE, "se3_checklist_items.json"), encoding="utf-8") as f:
        return json.load(f)


def pick(d, areas):
    if not areas:
        return d["itens"]
    areas = [AREA_ALIASES.get(a.strip().lower(), a) for a in areas]
    bad = [a for a in areas if a not in d["areas"]]
    if bad:
        print("error: invalid area(s): " + ", ".join(bad) + ". Use 'areas'.", file=sys.stderr)
        sys.exit(2)
    return [i for i in d["itens"] if i["area"] in areas]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("areas")
    p = sp.add_parser("list")
    p.add_argument("--area", action="append")
    p = sp.add_parser("markdown")
    p.add_argument("--area", action="append")
    p = sp.add_parser("evaluate")
    p.add_argument("arquivo", metavar="FILE")
    a = ap.parse_args()
    d = load()
    if a.cmd == "areas":
        for k, v in d["areas"].items():
            n = sum(1 for i in d["itens"] if i["area"] == k)
            alias = next((e for e, pt in AREA_ALIASES.items() if pt == k), k)
            print(f"{k:<10} {alias:<10} {n:>3} items  {v}")
        return 0
    if a.cmd == "list":
        for i in pick(d, a.area):
            print(f"{i['id']}  [SE3 p.{i['paginas']}]  {i['pergunta']}")
        return 0
    if a.cmd == "markdown":
        items = pick(d, a.area)
        print("# Review checklist (SE3, Ross Anderson, 3rd ed.)")
        print("Questions = [inference]; pages (PDF) = where the book presents the principle [from source]. Does not replace a formal security review.\n")
        cur = None
        for i in items:
            if i["area"] != cur:
                cur = i["area"]
                print(f"\n## {d['areas'][cur]}\n")
            print(f"- [ ] {i['id']}: {i['pergunta']} (SE3 p.{i['paginas']})")
        return 0
    if a.cmd == "evaluate":
        try:
            with io.open(a.arquivo, encoding="utf-8") as f:
                ans = json.load(f)
        except (OSError, ValueError) as e:
            print(f"error reading {a.arquivo}: {e}", file=sys.stderr)
            return 2
        by = {i["id"]: i for i in d["itens"]}
        unk = [k for k in ans if k not in by]
        if unk:
            print("Unknown IDs (ignored): " + ", ".join(unk))
        cnt = {"yes": 0, "no": 0, "partial": 0, "na": 0, "no answer": 0}
        pend = []
        for i in d["itens"]:
            if ans and i["id"] not in ans:
                continue
            v = ANSWER_ALIASES.get(str(ans.get(i["id"], "")).strip().lower(), "")
            if v in cnt:
                cnt[v] += 1
            else:
                cnt["no answer"] += 1
                v = "no answer"
            if v in ("no", "partial", "no answer"):
                pend.append((v, i))
        print("Summary: " + ", ".join(f"{k}={n}" for k, n in cnt.items()))
        order = {"no": 0, "partial": 1, "no answer": 2}
        for v, i in sorted(pend, key=lambda x: (order[x[0]], x[1]["id"])):
            print(f"[{v.upper()}] {i['id']} (SE3 p.{i['paginas']}): {i['pergunta']}")
        print("Warning: the result is [inference] over self-reported answers; it does not replace a formal security review.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
