# -*- coding: utf-8 -*-
"""
dpe_checklist.py - DPE maturity checklist (items derived from the practices of the Developer Productivity Engineering Handbook, 2022).
Stdlib, no network. Pages = PDF (printed = PDF - 5).

IMPORTANT: the book has NO checklist or maturity model. Each item is an [inference] question whose practice
comes from the cited pages. The score bands (low/medium/high) are an [extrapolation] of the package, not of the book.

Usage:
  python -I scripts/dpe_checklist.py areas
  python -I scripts/dpe_checklist.py list [--area ORG]
  python -I scripts/dpe_checklist.py markdown [--area ORG]
  python -I scripts/dpe_checklist.py evaluate ANSWERS.json     # {"ORG-01": "yes|partial|no|na", ...} ; "-" reads stdin
                                                               # Portuguese values sim|parcial|nao|na are also accepted
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
DATA = json.load(open(os.path.join(HERE, "dpe_checklist_items.json"), encoding="utf-8"))
ITEMS = DATA["items"]
AREAS = DATA["areas"]
# English values plus the Portuguese aliases (user input may still be in Portuguese)
VAL = {"yes": 1.0, "partial": 0.5, "no": 0.0, "sim": 1.0, "parcial": 0.5, "nao": 0.0, "não": 0.0}


def band(p):
    # [extrapolation]
    return "low" if p < 0.4 else ("medium" if p < 0.75 else "high")


def sel(area):
    return [i for i in ITEMS if (not area or i["area"] == area.upper())]


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("areas")
    for n in ("list", "markdown"):
        p = sp.add_parser(n)
        p.add_argument("--area")
    p = sp.add_parser("evaluate")
    p.add_argument("file")
    a = ap.parse_args()

    if a.cmd == "areas":
        for k, v in AREAS.items():
            print(f"{k}: {v} ({len(sel(k))} items)")
        print(f"Total: {len(ITEMS)} items. {DATA['origem']}")
        return 0
    if a.cmd == "list":
        for i in sel(a.area):
            print(f"{i['id']} (DPE p.{i['pages']}) {i['text']}")
        return 0
    if a.cmd == "markdown":
        cur = None
        for i in sel(a.area):
            if i["area"] != cur:
                cur = i["area"]
                print(f"\n## {cur}: {AREAS[cur]}")
            print(f"- [ ] **{i['id']}** {i['text']} (DPE p.{i['pages']}) [inference]")
        return 0
    if a.cmd == "evaluate":
        raw = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
        ans = json.loads(raw)
        ids = {i["id"] for i in ITEMS}
        unknown = [k for k in ans if k not in ids]
        if unknown:
            print("Unknown IDs (ignored): " + ", ".join(unknown))
        per = {}
        gaps = []
        for i in ITEMS:
            v = str(ans.get(i["id"], "")).strip().lower()
            if v in ("", "na", "n/a"):
                continue
            if v not in VAL:
                print(f"Invalid value for {i['id']}: {v!r} (use yes|partial|no|na)")
                continue
            d = per.setdefault(i["area"], [0.0, 0])
            d[0] += VAL[v]
            d[1] += 1
            if VAL[v] < 1.0:
                gaps.append((VAL[v], i))
        tot = sum(d[0] for d in per.values())
        n = sum(d[1] for d in per.values())
        print("DPE maturity by area (answered items; na excluded):")
        for k in AREAS:
            if k in per:
                s, c = per[k]
                print(f"- {k} {AREAS[k]}: {s:.1f}/{c} = {s / c:.0%} (band {band(s / c)} [extrapolation])")
        if n:
            print(f"Overall: {tot:.1f}/{n} = {tot / n:.0%} (band {band(tot / n)} [extrapolation]; the book defines no levels)")
        else:
            print("No items answered.")
        print("Gaps (partial/no), with the page of the practice:")
        for v, i in sorted(gaps, key=lambda x: (x[0], x[1]["id"])):
            print(f"- {i['id']} ({'partial' if v else 'no'}) {i['text']} (DPE p.{i['pages']})")
        print("Warning: items are [inference]; the book is vendor material (Gradle), with a pro-instrumentation and pro-acceleration bias.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
