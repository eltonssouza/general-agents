# -*- coding: utf-8 -*-
"""
design_review_checklist.py - secure and reliable design review checklist with items the BSRS provides.

Each item cites the PDF pages of the book (BSRS p.N). The question wording is the agent's [inference];
the content of each item comes from the cited pages and was checked against the text (tests/citation-checks.json).

Usage (Python 3, stdlib, no network; run with `python -I`):
  python -I scripts/design_review_checklist.py areas
  python -I scripts/design_review_checklist.py list [--area privilegio]
  python -I scripts/design_review_checklist.py markdown [--areas requisitos,privilegio,resiliencia] [--out ARQ.md]
  python -I scripts/design_review_checklist.py evaluate respostas.json [--areas ...] [--strict]
      respostas.json: {"REQ01": "sim", "PRI02": "nao", "RES03": "parcial", "DOS01": "na"}
      values: sim | nao | parcial | na (not applicable); English aliases yes | no | partial | n/a are also accepted.
      Missing items count as "unanswered".
  --strict: exit 1 if there is any "nao" (no) or "parcial" (partial) (for use as a review gate).
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


def render_md(d, items):
    out = ["# Secure and reliable design review checklist (BSRS)", "",
           "Source: *Building Secure and Reliable Systems* (Google, 2020). Pages = PDF (`BSRS p.N`; printed = N − 36).",
           "Items derived from recommendations in the book `[from source]`; the question form is `[inference]`. Mark `na` when not applicable and justify.",
           "Boundary: SLO, error budget and on-call belong to sre-practices-expert.", ""]
    cur = None
    for i in items:
        if i["area"] != cur:
            cur = i["area"]
            out.append("## %s" % d["areas"][cur])
        out.append("- [ ] **%s** %s (BSRS p.%s)" % (i["id"], i["text"], i["pages"]))
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Secure/reliable design review checklist (BSRS)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("areas")
    p = sub.add_parser("list")
    p.add_argument("--area")
    p = sub.add_parser("markdown")
    p.add_argument("--areas", default="")
    p.add_argument("--out")
    p = sub.add_parser("evaluate")
    p.add_argument("answers")
    p.add_argument("--areas", default="")
    p.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    d = load()
    if a.cmd == "areas" or not a.cmd:
        for k, v in d["areas"].items():
            n = sum(1 for i in d["items"] if i["area"] == k)
            print("%-20s %s (%d items)" % (k, v, n))
        print("Total: %d items" % len(d["items"]))
        return
    if a.cmd == "list":
        for i in select(d, [a.area] if a.area else []):
            print("%s [%s] %s (BSRS p.%s)" % (i["id"], i["area"], i["text"], i["pages"]))
        return
    areas = [x.strip() for x in getattr(a, "areas", "").split(",") if x.strip()]
    if a.cmd == "markdown":
        md = render_md(d, select(d, areas))
        if a.out:
            with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
                f.write(md)
            print("written: %s" % a.out)
        else:
            sys.stdout.write(md)
        return
    if a.cmd == "evaluate":
        with io.open(a.answers, "r", encoding="utf-8") as f:
            ans = json.load(f)
        valid = {"sim", "nao", "parcial", "na"}
        alias = {"yes": "sim", "y": "sim", "no": "nao", "não": "nao", "n": "nao", "partial": "parcial", "n/a": "na", "not applicable": "na"}
        items = select(d, areas)
        ids = {i["id"] for i in items}
        unknown = [k for k in ans if k not in {i["id"] for i in d["items"]}]
        if unknown:
            print("WARNING: unknown ids ignored: %s" % ", ".join(unknown))
        per = {}
        gaps = []
        for i in items:
            v = str(ans.get(i["id"], "")).strip().lower()
            v = alias.get(v, v)
            if v and v not in valid:
                print("WARNING: invalid value '%s' in %s (use sim|nao|parcial|na or yes|no|partial|n/a); treated as unanswered" % (v, i["id"]))
                v = ""
            c = per.setdefault(i["area"], {"sim": 0, "nao": 0, "parcial": 0, "na": 0, "": 0})
            c[v] += 1
            if v in ("nao", "parcial", ""):
                gaps.append((i, v))
        print("# Evaluation (%d items evaluated)" % len(items))
        for k, c in per.items():
            aplic = c["sim"] + c["nao"] + c["parcial"] + c[""]
            pct = (100.0 * c["sim"] / aplic) if aplic else 100.0
            print("- %s: yes=%d partial=%d no=%d unanswered=%d na=%d | compliance %.0f%%" % (d["areas"][k], c["sim"], c["parcial"], c["nao"], c[""], c["na"], pct))
        print("\n# Gaps (no / partial / unanswered)")
        for i, v in gaps:
            print("- %s [%s] %s: %s (BSRS p.%s)" % (i["id"], {"nao": "no", "parcial": "partial"}.get(v, v) or "unanswered", i["area"], i["text"], i["pages"]))
        bad = [1 for i, v in gaps if v in ("nao", "parcial")]
        if a.strict and bad:
            sys.exit(1)
        return


if __name__ == "__main__":
    main()
