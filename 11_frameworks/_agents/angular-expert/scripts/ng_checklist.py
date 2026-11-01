# -*- coding: utf-8 -*-
"""
ng_checklist.py - checklist of Angular OVERVIEW CONCEPTS, per Overview version (NG18..NG22).

Usage:
  python -I scripts/ng_checklist.py --version 21                       # what the NG21 Overview presents, with pages
  python -I scripts/ng_checklist.py --version 20 --known signals,ssr,router,cli
  python -I scripts/ng_checklist.py --version 22 --check standalone,signals,defer
  python -I scripts/ng_checklist.py --version 19 --group feature --json

This is not a code review checklist: it is a reading/understanding guide to what the "What is Angular?" page
presents. "Not detected" = the capture does not cite it (NOT "does not exist"). Source: scripts/ng_index.json. No network.
Groups: framing, feature, tool, stability, scale, community (the old Portuguese names are also accepted).
"""
import argparse
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ng_lookup  # noqa: E402

CORE_GROUPS = ["framing", "feature", "tool", "stability", "scale", "community"]
GROUP_ALIAS = {"enquadramento": "framing", "recurso": "feature", "ferramenta": "tool", "estabilidade": "stability",
               "escala": "scale", "comunidade": "community"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", type=int, required=True, choices=[18, 19, 20, 21, 22])
    ap.add_argument("--known", help="ids/terms the person already masters (comma-separated)")
    ap.add_argument("--check", help="terms to check against the Overview (coverage)")
    ap.add_argument("--group")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    idx = ng_lookup.load()
    v = str(a.version)
    grp = GROUP_ALIAS.get(a.group, a.group)
    items = [c for c in idx["concepts"] if c["group"] in CORE_GROUPS and (not grp or c["group"] == grp)]
    items.sort(key=lambda c: CORE_GROUPS.index(c["group"]))
    present = [c for c in items if v in c["pages"]]
    absent = [c for c in items if v not in c["pages"]]
    known_ids = set()
    if a.known:
        hits, _ = ng_lookup.find(idx, [t.strip() for t in a.known.split(",") if t.strip()])
        known_ids = {c["id"] for c in hits}
    if a.check:
        terms = [t.strip() for t in a.check.split(",") if t.strip()]
        res = []
        for t in terms:
            hits, gaps = ng_lookup.find(idx, [t])
            if hits:
                for c in hits:
                    pg = c["pages"].get(v)
                    res.append({"term": t, "concept": c["id"], "status": "in the Overview" if pg else "not detected in this capture",
                                "cite": f"NG{v} p.{','.join(map(str, pg))}" if pg else None})
            else:
                res.append({"term": t, "concept": None, "status": "NOT COVERED", "cite": None})
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            for r in res:
                print(f"{r['term']:20s} -> {r['status']}" + (f" ({r['cite']}; {r['concept']})" if r["cite"] else (f" ({r['concept']})" if r["concept"] else "")))
        return
    if a.json:
        print(json.dumps({"version": a.version,
                          "present": [{"id": c["id"], "label": c["label"], "cite": f"NG{v} p.{','.join(map(str, c['pages'][v]))}",
                                         "known": c["id"] in known_ids} for c in present],
                          "not_detected": [c["id"] for c in absent]}, ensure_ascii=False, indent=1))
        return
    print(f"OVERVIEW CHECKLIST — NG{a.version} Overview (doc-capture; PDF pages)")
    cur = None
    for c in present:
        if c["group"] != cur:
            cur = c["group"]
            print(f"\n[{cur}]")
        mark = "[x]" if c["id"] in known_ids else "[ ]"
        print(f"  {mark} {c['label']}  (NG{v} p.{','.join(map(str, c['pages'][v]))})")
    if a.known:
        todo = [c for c in present if c["id"] not in known_ids]
        print(f"\nPending study: {len(todo)} of {len(present)} presented concepts.")
    print(f"\nIndex concepts NOT detected in the NG{a.version} Overview ({len(absent)}): ", ", ".join(c["id"] for c in absent) or "none")
    print("Reminder: 'not detected' does not prove removal; topics outside the index (standalone, zoneless, control flow...) = NOT COVERED (ng_lookup.py --gaps).")


if __name__ == "__main__":
    main()
