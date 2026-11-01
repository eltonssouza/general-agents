# -*- coding: utf-8 -*-
"""
agent_checklist.py - design and review checklist for agents and context engineering, anchored in
BAAS (Building Agentic AI Systems, 2025) and CE2 (Context Engineering 2.0, 2025).

Stdlib, no network, read-only. Run with: python -I scripts/agent_checklist.py COMMAND
  areas                          lists the areas and the number of items
  list [--area A] [--fonte F]    lists items (id, source, pages, question)
  markdown [--area A ...]        generates a Markdown checklist to paste into a review
  evaluate FILE.json             evaluates answers {"ID": "yes|no|partial|na", ...}; lists pending items with page
                                 (Portuguese answers sim|nao|parcial|na are also accepted)
Convention: pages = PDF (BAAS: printed = PDF - 25; CE2: PDF = printed).
Labels: the QUESTION is [inference] (checklist form) or [extrapolation] when indicated; the page shows where the text
presents the idea ([from source]). Items with source 'pacote' (also accepted as 'package') have no page in the texts.
This checklist structures a review; it is NOT a security audit and does not replace tests, empirical evaluation, or specialists.
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
VALID = {"yes", "sim", "no", "nao", "não", "partial", "parcial", "na"}
CANON = {"yes": "yes", "sim": "yes", "no": "no", "nao": "no", "não": "no", "partial": "partial", "parcial": "partial", "na": "na"}


def load():
    with io.open(os.path.join(HERE, "agent_checklist_items.json"), encoding="utf-8") as f:
        return json.load(f)


def pick(d, areas, fonte=None):
    if areas:
        bad = [a for a in areas if a not in d["areas"]]
        if bad:
            print("error: invalid area(s): " + ", ".join(bad) + ". Use 'areas'.", file=sys.stderr)
            sys.exit(2)
    out = []
    for i in d["itens"]:
        if areas and i["area"] not in areas:
            continue
        if fonte and i["fonte"] != fonte:
            continue
        out.append(i)
    return out


def cite(i):
    if i["fonte"] == "pacote":
        return "[package, no page]"
    return f"[{i['fonte']} p.{i['paginas']}]"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("areas")
    p = sp.add_parser("list")
    p.add_argument("--area", action="append")
    p.add_argument("--fonte", choices=["BAAS", "CE2", "pacote", "package"])
    p = sp.add_parser("markdown")
    p.add_argument("--area", action="append")
    p = sp.add_parser("evaluate")
    p.add_argument("arquivo")
    a = ap.parse_args()
    d = load()
    if getattr(a, "fonte", None) == "package":
        a.fonte = "pacote"
    if a.cmd == "areas":
        for k, v in d["areas"].items():
            n = sum(1 for i in d["itens"] if i["area"] == k)
            print(f"{k:<6} {n:>3} items  {v}")
        print(f"total: {len(d['itens'])} items")
        return 0
    if a.cmd == "list":
        for i in pick(d, a.area, a.fonte):
            print(f"{i['id']}  {cite(i)}  {i['pergunta']}")
        return 0
    if a.cmd == "markdown":
        items = pick(d, a.area)
        print("# Agent review checklist (BAAS and CE2)")
        print("Questions = [inference] (or [extrapolation] when indicated); pages (PDF) = where the text presents the idea. Does not replace an audit or empirical evaluation.\n")
        cur = None
        for i in items:
            if i["area"] != cur:
                cur = i["area"]
                print(f"\n## {d['areas'][cur]}\n")
            print(f"- [ ] {i['id']}: {i['pergunta']} {cite(i)}")
        return 0
    if a.cmd == "evaluate":
        try:
            with io.open(a.arquivo, encoding="utf-8") as f:
                ans = json.load(f)
        except (OSError, ValueError) as e:
            print(f"error reading {a.arquivo}: {e}", file=sys.stderr)
            return 2
        if not isinstance(ans, dict):
            print("error: the file must be a JSON object {ID: answer}", file=sys.stderr)
            return 2
        byid = {i["id"]: i for i in d["itens"]}
        unknown = [k for k in ans if k not in byid]
        badval = [k for k, v in ans.items() if k in byid and str(v).strip().lower() not in VALID]
        if unknown:
            print("Unknown IDs (ignored): " + ", ".join(sorted(unknown)))
        if badval:
            print("Invalid answers (use yes|no|partial|na): " + ", ".join(sorted(badval)))
        counts = {"yes": 0, "no": 0, "partial": 0, "na": 0, "unanswered": 0}
        gaps = []
        for i in d["itens"]:
            v = CANON.get(str(ans.get(i["id"], "")).strip().lower())
            if v is None:
                counts["unanswered"] += 1
                gaps.append(("unanswered", i))
            else:
                counts[v] += 1
                if v in ("no", "partial"):
                    gaps.append((v, i))
        aplic = counts["yes"] + counts["no"] + counts["partial"]
        print("Summary: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
        if aplic:
            print(f"Adherence = (yes + 0.5*partial) / applicable = {(counts['yes'] + 0.5 * counts['partial']) / aplic:.0%} "
                  f"(over {aplic} applicable answered items; package metric, with no basis in the texts)")
        order = {"no": 0, "partial": 1, "unanswered": 2}
        gaps.sort(key=lambda x: (order[x[0]], x[1]["id"]))
        if gaps:
            print("\nPending items (no, partial, unanswered):")
            for st, i in gaps:
                print(f"- [{st}] {i['id']} {cite(i)} {i['pergunta']}")
        print("\nOrigin: questions are [inference]; pages show where the text presents the idea. Not a security audit.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
