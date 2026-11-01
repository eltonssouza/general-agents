# -*- coding: utf-8 -*-
"""
go_checklist.py - prints a review checklist by area, each item with its ORIGIN and PAGE (no network, read-only).

The rules come from scripts/go_checklists.json. Each item carries its origin:
  [from source]    the cited page says so (checked by tests/verify_citations.py);
  [inference]      conclusion of the package from the sources (or a claim of absence);
  [extrapolation]  knowledge outside the sources (when used, it must be labeled in the answer).
Pages = PDF pages (Little: printed = N - 1). [DATED] items come from Eff (2009) or Little (go1.3.3).
This is NOT a code linter: for code scanning use skills/go-code-review/scripts/scan_go_smells.py.
Area names are the Portuguese keys of the JSON (see --list); English aliases are accepted too.

Usage:
  python -I scripts/go_checklist.py --list
  python -I scripts/go_checklist.py concorrencia
  python -I scripts/go_checklist.py erros --json
  python -I scripts/go_checklist.py all
Exit code: 0 ok; 2 unknown area.
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
LABEL = {"from source": "[from source]", "inference": "[inference]", "extrapolation": "[extrapolation]"}
# English aliases for the area keys (the Portuguese keys remain the canonical names)
ALIAS = {"formatting": "formatacao", "names": "nomes", "naming": "nomes", "errors": "erros", "pointers": "ponteiros-receivers",
         "receivers": "ponteiros-receivers", "pointers-receivers": "ponteiros-receivers", "slices-and-maps": "slices-maps",
         "defer-panic-recover": "defer-panic", "concurrency": "concorrencia", "version-migration": "versao-migracao",
         "migration": "versao-migracao"}


def fmt(it):
    src = ""
    if it.get("doc"):
        src = " (%s %s)" % (it["doc"], ", ".join("p.%d" % p for p in it["paginas"]))
    return "- [ ] %s %s%s" % (LABEL[it["origem"]], it["texto"], src)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("area", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--file", default=os.path.join(HERE, "go_checklists.json"))
    a = ap.parse_args()
    with open(a.file, encoding="utf-8") as f:
        data = json.load(f)["areas"]
    if a.list or not a.area:
        for k, v in data.items():
            print("- %-20s %s (%d items)" % (k, v["titulo"], len(v["itens"])))
        return 0
    areas = list(data) if a.area == "all" else [ALIAS.get(a.area, a.area)]
    for k in areas:
        if k not in data:
            print("unknown area: %s (use --list)" % k, file=sys.stderr)
            return 2
    if a.json:
        json.dump({k: data[k] for k in areas}, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    print("Page convention: PDF (Little: printed = N - 1). Labels: [from source] / [inference] / [extrapolation].")
    for k in areas:
        print("\n## %s" % data[k]["titulo"])
        for it in data[k]["itens"]:
            print(fmt(it))
    return 0


if __name__ == "__main__":
    sys.exit(main())
