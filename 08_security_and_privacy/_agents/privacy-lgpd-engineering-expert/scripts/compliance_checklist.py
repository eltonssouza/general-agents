# -*- coding: utf-8 -*-
"""
compliance_checklist.py - compliance and privacy-by-design checklist generated from the actual articles of the LGPD
(Lei Geral de Proteção de Dados, Brazil's General Data Protection Law; compiled text) and from NIST IR 8062 concepts.

Each item cites Art./inciso (numbered subitem) and the PDF page. The content comes from the cited text (checked in
tests/citation-checks.json); the WORDING AS A QUESTION is an [inference] by the agent. Items with origin "nist" are
NIST IR 8062 privacy engineering (not an LGPD requirement). This is NOT legal advice:
take the answers to a lawyer/the encarregado (DPO).

Usage (Python 3, stdlib, no network; run with `python -I`):
  python -I scripts/compliance_checklist.py areas
  python -I scripts/compliance_checklist.py list [--area bases]
  python -I scripts/compliance_checklist.py markdown [--areas principios,bases,seguranca] [--out ARQ.md]
  python -I scripts/compliance_checklist.py pbd [--out ARQ.md]          # privacy-by-design roadmap (Art. 6, 46 §2, 49, 50 + NIST)
  python -I scripts/compliance_checklist.py evaluate respostas.json [--areas ...] [--strict]
      respostas.json: {"PRI01": "sim", "BAS02": "nao", "SEG01": "parcial", "TRA01": "na"}
      values: yes | no | partial | na (the Portuguese sim | nao | não | parcial are also accepted). Items not answered
      count as "no answer".
  --strict: exit 1 if there is any "no" or "partial" (use as a review gate).
  Area ids (escopo, principios, bases, ...) are the Portuguese identifiers of the LGPD chapters; `areas` lists them with English descriptions.
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
DATA = os.path.join(HERE, "checklist_items.json")
AVISO = ("Notice: support material generated from two documents; not legal advice or an audit. "
         "Refer to a lawyer/the encarregado (DPO) and check the current version of the law and the regulations of the ANPD (national data protection authority) [extrapolation].")
PBD_AREAS = ["principios", "seguranca", "governanca", "direitos", "incidentes", "nist"]
VALID = {"yes", "no", "partial", "na"}
# accepted answer spellings -> canonical value (Portuguese input stays supported)
ANSWER = {"sim": "yes", "yes": "yes", "nao": "no", "não": "no", "no": "no", "parcial": "partial", "partial": "partial", "na": "na"}


def load():
    with io.open(DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def select(d, areas):
    items = d["items"]
    if areas:
        bad = [a for a in areas if a not in d["areas"]]
        if bad:
            raise SystemExit("unknown area(s): %s. Use `areas` to list them." % ", ".join(bad))
        items = [i for i in items if i["area"] in areas]
    return items


def pg(p):
    return "-".join(str(x) for x in (p if len(p) == 1 else [p[0], p[-1]]))


def render_md(d, items, title):
    out = ["# %s" % title, "",
           "Sources: LGPD (Lei 13.709/2018, compiled text from the PDF, pages = PDF) and NIST IR 8062 (PDF; printed = PDF − 8).",
           "Content of each item: `[from source]` on the cited page. The question form is `[inference]`. NIST items are privacy engineering, not a legal requirement.",
           "For the LGPD, items that mention ANPD deadlines/regulations depend on `[extrapolation]` (current regulation).",
           "", "> " + AVISO, ""]
    cur = None
    for i in items:
        if i["area"] != cur:
            cur = i["area"]
            out.append("")
            out.append("## %s" % d["areas"][cur])
        out.append("- [ ] **%s** %s (%s; p.%s)" % (i["id"], i["text"], i["src"], pg(i["pages"])))
    return "\n".join(out) + "\n"


def cmd_evaluate(d, args):
    items = select(d, args.areas.split(",") if args.areas else None)
    with io.open(args.respostas, "r", encoding="utf-8") as f:
        ans = json.load(f)
    ids = {i["id"] for i in d["items"]}
    unknown = [k for k in ans if k not in ids]
    if unknown:
        print("NOTICE: unknown ids ignored: %s" % ", ".join(unknown))
    counts = {"yes": 0, "no": 0, "partial": 0, "na": 0, "no answer": 0}
    gaps = []
    for i in items:
        v = str(ans.get(i["id"], "no answer")).strip().lower()
        v = ANSWER.get(v, v) if v != "sem resposta" else "no answer"
        if v not in counts:
            raise SystemExit("invalid value for %s: %r (use yes|no|partial|na)" % (i["id"], v))
        counts[v] += 1
        if v in ("no", "partial"):
            gaps.append((i, v))
    total = len(items)
    applicable = total - counts["na"]
    print("Items evaluated: %d (applicable: %d)" % (total, applicable))
    for k, v in counts.items():
        print("  %-13s %d" % (k, v))
    if applicable:
        print("Declared adherence (yes / applicable): %.0f%%  [internal indicator; does not measure legal compliance]" % (100.0 * counts["yes"] / applicable))
    if gaps:
        print("\nGaps (no/partial):")
        for i, v in gaps:
            print("- %s [%s] %s (%s p.%s)" % (i["id"], v, i["text"], i["src"], pg(i["pages"])))
    print("\n" + AVISO)
    return 1 if (args.strict and gaps) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("areas")
    p = sp.add_parser("list"); p.add_argument("--area")
    p = sp.add_parser("markdown"); p.add_argument("--areas"); p.add_argument("--out")
    p = sp.add_parser("pbd"); p.add_argument("--out")
    p = sp.add_parser("evaluate"); p.add_argument("respostas"); p.add_argument("--areas"); p.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    d = load()
    if args.cmd == "areas":
        for k, v in d["areas"].items():
            n = sum(1 for i in d["items"] if i["area"] == k)
            print("%-14s %2d items  %s" % (k, n, v))
        print("Total: %d items" % len(d["items"]))
        return 0
    if args.cmd == "list":
        items = select(d, [args.area] if args.area else None)
        for i in items:
            print("%s  [%s] %s (%s p.%s)" % (i["id"], i["area"], i["text"], i["src"], pg(i["pages"])))
        return 0
    if args.cmd in ("markdown", "pbd"):
        areas = PBD_AREAS if args.cmd == "pbd" else (args.areas.split(",") if args.areas else None)
        items = select(d, areas)
        title = "Privacy-by-design roadmap (reading of Art. 46 §2º, Art. 49, Art. 50 and NIST IR 8062 concepts)" if args.cmd == "pbd" else "LGPD compliance and privacy engineering checklist"
        md = render_md(d, items, title)
        if args.out:
            with io.open(args.out, "w", encoding="utf-8", newline="\n") as f:
                f.write(md)
            print("written: %s" % args.out)
        else:
            sys.stdout.write(md)
        return 0
    if args.cmd == "evaluate":
        return cmd_evaluate(d, args)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
