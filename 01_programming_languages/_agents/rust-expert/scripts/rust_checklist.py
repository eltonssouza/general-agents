# -*- coding: utf-8 -*-
"""
rust_checklist.py - review checklists of the rust-expert package, with the ORIGIN and page of each item.

The rules come from scripts/rust_checklists.json; each item carries a label:
  [from source]    the cited page supports the item (terms checked by tests/verify_citations.py);
  [inference]      follows from the pages, which do not state it;
  [extrapolation]  convention external to the sources (no page).

Usage:
  python -I scripts/rust_checklist.py --list
  python -I scripts/rust_checklist.py review            # areas: review, errors, ownership, unsafe, concurrency, edition
  python -I scripts/rust_checklist.py unsafe --markdown   # Markdown output with [ ] boxes
  python -I scripts/rust_checklist.py all --json

The Portuguese area names (revisao, erros, concorrencia, todas) are still accepted as aliases.
Exit 0; exit 2 for an unknown area. Pages are PDF pages. No network; read-only.
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
# Portuguese aliases for the area names (user input), mapped to the canonical English names
ALIASES = {"revisao": "review", "erros": "errors", "concorrencia": "concurrency", "todas": "all"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("area", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--data", default=os.path.join(HERE, "rust_checklists.json"))
    a = ap.parse_args()
    with open(a.data, encoding="utf-8") as f:
        d = json.load(f)
    areas = d["areas"]
    if a.list or not a.area:
        for k, v in areas.items():
            print("%-13s %s (%d items)" % (k, v["titulo"], len(v["itens"])))
        return 0
    area = ALIASES.get(a.area, a.area)
    sel = list(areas) if area == "all" else [area]
    for k in sel:
        if k not in areas:
            print("unknown area: %s (use --list)" % k, file=sys.stderr)
            return 2
    if a.json:
        json.dump({k: areas[k] for k in sel}, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0
    for k in sel:
        v = areas[k]
        print(("## " if a.markdown else "# ") + v["titulo"])
        for it in v["itens"]:
            src = "; ".join(it["fontes"]) if it["fontes"] else "no page"
            box = "- [ ] " if a.markdown else "[ ] "
            print("%s%s — %s %s" % (box, it["texto"], it["rotulo"], src))
        print()
    print("Convention: PDF pages. Labels: [from source] / [inference] / [extrapolation]. "
          "[from source] items have their terms checked against the page (tests/verify_citations.py).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
