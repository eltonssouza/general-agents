# -*- coding: utf-8 -*-
"""
nh_map.py - map of what each documentation covers and per-item coverage checklist.

Usage (package root; always python -I):
  python -I scripts/nh_map.py map [--fonte N8N|HERMES] [--json]
      page-by-page map: topics, depth (described | command | title-only)
  python -I scripts/nh_map.py checklist --items "instalação; preço; webhooks; MCP" [--json]
  python -I scripts/nh_map.py checklist --file itens.txt        # one item per line
  python -I scripts/nh_map.py checklist --preset geral          # default list of common questions
Each item gets, per source: COVERED | PARTIAL (title/link name only) | NOT COVERED.
Reuses the nh_index.json index (read-only, no network, deterministic).
Items may be in Portuguese or English (the index keeps both sets of keywords).
Exit: 0 whenever the run is valid; 2 for invalid usage.
"""
import argparse
import importlib.util
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("nh_lookup", os.path.join(HERE, "nh_lookup.py"))
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

PRESET_GERAL = [
    "what is it", "installation", "docker", "price", "license", "version", "webhook", "credentials",
    "MCP", "scheduling", "cron", "memory", "security", "messaging platforms",
    "models and providers", "n8n hermes integration", "benchmark", "usage examples",
]


def status_for(idx, item, fonte):
    hits, gaps = L.search(idx, [item], fonte)
    own_gaps = [(g, m) for g, m in gaps if g["fonte"] in (fonte, "AMBAS")]
    if own_gaps:
        nota = own_gaps[0][0]["nota"]
        if hits and all(g.get("parcial") for g, _ in own_gaps):
            return "PARTIAL", "title/mention only, no detail: " + nota, [t["id"] for _, t, _ in hits[:3]]
        return "NOT COVERED", nota, [t["id"] for _, t, _ in hits[:3]]
    if not hits:
        return "NOT COVERED", "no topic matches the item", []
    deep = [t for _, t, _ in hits if t["profundidade"] in ("described", "command")]
    if deep:
        t = deep[0]
        return "COVERED", f"{t['id']} ({L.cite(t)}): {t['titulo']}", [x["id"] for _, x, _ in hits[:3]]
    t = hits[0][1]
    return "PARTIAL", f"{t['id']} ({L.cite(t)}): only the link title/name '{t['titulo']}'", [x["id"] for _, x, _ in hits[:3]]


def cmd_map(idx, fonte, as_json):
    out = {}
    for f, meta in idx["fontes"].items():
        if fonte and f != fonte:
            continue
        pages = {}
        for n in range(1, meta["paginas"] + 1):
            pages[n] = [{"id": t["id"], "profundidade": t["profundidade"], "titulo": t["titulo"]}
                        for t in idx["topicos"] if t["fonte"] == f and n in t["paginas"]]
        out[f] = {"arquivo": meta["arquivo"], "descricao": meta["descricao"], "util": meta["util"], "paginas": pages}
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    for f, v in out.items():
        print(f"== {f}: {v['arquivo']} ==\n{v['descricao']}\nUsefulness: {v['util']}")
        for n, ts in v["paginas"].items():
            print(f"  p.{n}:")
            for t in ts:
                print(f"    - [{t['profundidade']}] {t['id']} {t['titulo']}")
    print("\nLegend: described = the source gives explanatory text; command = gives a literal command; "
          "title-only = only the link/section name.")


def cmd_check(idx, items, as_json):
    rows = []
    for it in items:
        row = {"item": it}
        for f in idx["fontes"]:
            s, why, ids = status_for(idx, it, f)
            row[f] = {"status": s, "detalhe": why, "topicos": ids}
        rows.append(row)
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    w = max(len(r["item"]) for r in rows)
    print(f"{'ITEM'.ljust(w)} | {'N8N'.ljust(13)} | {'HERMES'.ljust(13)}")
    print("-" * (w + 32))
    for r in rows:
        print(f"{r['item'].ljust(w)} | {r['N8N']['status'].ljust(13)} | {r['HERMES']['status'].ljust(13)}")
    print("\nDetails:")
    for r in rows:
        for f in ("N8N", "HERMES"):
            print(f"  {r['item']} / {f}: {r[f]['status']} - {r[f]['detalhe']}")
    n = sum(1 for r in rows for f in ("N8N", "HERMES") if r[f]["status"] == "NOT COVERED")
    print(f"\nSummary: {n} of {len(rows) * 2} cells NOT COVERED. Do not fill those cells with prior knowledge.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("map")
    m.add_argument("--fonte", choices=["N8N", "HERMES"])
    m.add_argument("--json", action="store_true")
    c = sub.add_parser("checklist")
    c.add_argument("--items")
    c.add_argument("--file")
    c.add_argument("--preset", choices=["geral"])
    c.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        return 2
    idx = L.load()
    if a.cmd == "map":
        cmd_map(idx, a.fonte, a.json)
        return 0
    items = []
    if a.items:
        items += [x.strip() for x in a.items.split(";") if x.strip()]
    if a.file:
        with open(a.file, "r", encoding="utf-8") as fh:
            items += [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    if a.preset == "geral":
        items += PRESET_GERAL
    if not items:
        print("Provide --items, --file or --preset geral.", file=sys.stderr)
        return 2
    cmd_check(idx, items, a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
