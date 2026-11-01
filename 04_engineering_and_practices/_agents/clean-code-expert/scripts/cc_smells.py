# -*- coding: utf-8 -*-
"""
cc_smells.py - catalog of "Odores e Heurísticas" (Smells and Heuristics; Código Limpo, ch. 17) searchable
by code, family or keyword, with the PDF page of each heuristic.

Reads cc_smells.json (same directory). Read-only, no network.
Each heuristic is printed with its English title first and the Portuguese title printed in the
Brazilian edition in parentheses. Keywords work in Portuguese and in English.

Usage:
  python -I cc_smells.py G5                 one heuristic by code (accepts g5, G05)
  python -I cc_smells.py G5 F3 N1           several
  python -I cc_smells.py "duplication"      keyword search ("duplicação" works too)
  python -I cc_smells.py --family F         list one family (C, E, F, G, J, N, T)
  python -I cc_smells.py --list             list all
A code that does not exist in the book (e.g. G37) or a search with no result: "NOT COVERED" (exit 1).
Usage error: exit 2.
"""
import argparse
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

CODE_RE = re.compile(r"^([A-Za-z])0*(\d{1,2})$")


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def load():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "cc_smells.json"), encoding="utf-8") as f:
        return json.load(f)


def canon(code):
    m = CODE_RE.match(code.strip())
    return (m.group(1).upper() + m.group(2)) if m else None


def title_of(s):
    """English title first, the edition's printed Portuguese title in parentheses."""
    en = s.get("title_en")
    return "%s (%s)" % (en, s["title"]) if en else s["title"]


def show(s, families):
    print("%s - %s [%s] (CL p.%s)" % (s["code"], title_of(s), families.get(s["code"][0], "?"), s["page"]))
    print("  %s" % s["summary"])
    det = "candidates by script (cc_audit.py)" if s.get("detectable") == "script" else "requires reviewer judgment"
    print("  Detection: %s" % det)
    if s.get("related"):
        print("  Related: %s" % ", ".join(s["related"]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*", help="code(s) such as G5, or a keyword")
    ap.add_argument("--family", help="C, E, F, G, J, N or T")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--max", type=int, default=5)
    a = ap.parse_args(argv)
    data = load()
    fam, smells = data["families"], data["smells"]
    by_code = {s["code"]: s for s in smells}
    print("[from source] Código Limpo, ch. 17 (PDF pages).")
    if a.list or a.family:
        f = (a.family or "").upper()
        if a.family and f not in fam:
            print("Unknown family: %s. Use one of: %s" % (a.family, ", ".join(fam)))
            return 2
        for s in smells:
            if not a.family or s["code"][0] == f:
                print("%-4s %s (CL p.%s)" % (s["code"], title_of(s), s["page"]))
        return 0
    if not a.query:
        ap.print_help()
        return 2
    codes = [canon(q) for q in a.query]
    if all(codes):
        missing = [c for c in codes if c not in by_code]
        for i, c in enumerate(c for c in codes if c in by_code):
            if i:
                print()
            show(by_code[c], fam)
        for c in missing:
            print("NOT COVERED: the book has no heuristic %s (families: %s)." % (
                c, ", ".join("%s1-%s%d" % (k, k, max(int(s["code"][1:]) for s in smells if s["code"][0] == k)) for k in fam)))
        return 1 if missing else 0
    q = norm(" ".join(a.query))
    scored = []
    for s in smells:
        sc = 0
        if q in norm(s["title"]) or q in norm(s.get("title_en", "")):
            sc += 40
        for k in s.get("keywords", []):
            kn = norm(k)
            if q == kn:
                sc += 50
            elif len(q) >= 3 and (q in kn or kn in q):
                sc += 20
        if len(q) >= 4 and q in norm(s["summary"]):
            sc += 10
        if sc:
            scored.append((sc, s["code"]))
    scored.sort(key=lambda x: (-x[0], x[1]))
    if not scored:
        print("NOT COVERED: no heuristic in ch. 17 matches '%s'. Try cc_lookup.py." % " ".join(a.query))
        return 1
    for i, (_, c) in enumerate(scored[: a.max]):
        if i:
            print()
        show(by_code[c], fam)
    return 0


if __name__ == "__main__":
    sys.exit(main())
