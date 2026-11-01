#!/usr/bin/env python3
"""Presence of a term in the Python 3.10, 3.11, 3.12, 3.13 and 3.14.0rc3 Tutorials (precomputed index).

Usage:
    python -I tutorial_versions.py TERM [TERM ...]
    python -I tutorial_versions.py --list
    python -I tutorial_versions.py --json TERM

For each term curated in tutorial_index.json it shows, per Tutorial version, the PDF pages (of EACH Tutorial) where
the term appears, split by zone: body (chapters 1-16), glossary (Appendix A) and license (Appendices B-D, which
do NOT indicate a feature). A term outside the index -> "NOT COVERED".

WARNING (read before using the result):
- This is PRESENCE in the Tutorial text, NOT the version in which the feature was born. The Tutorial may mention a
  feature long after it existed (e.g. dataclass appears in the body only from Tutorial 3.12). Saying "was introduced
  in X" from this is [inference]/[extrapolation]; the official version mark exists only where the text says
  "Added/Changed in version" (see references/versoes-e-datado.md).
- Absence from the 5 Tutorials does not prove the feature does not exist; only that the Tutorial does not cover it.
- There is no Tutorial before 3.10 and no "What's New" in the sources.
Read-only, no network, standard library only. Exit code: 0 if it ran; 2 for a usage error.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VERS = ["3.10", "3.11", "3.12", "3.13", "3.14"]


def load():
    with open(os.path.join(HERE, "tutorial_index.json"), encoding="utf-8") as fh:
        return json.load(fh)


def norm(s):
    return " ".join(s.lower().split())


def find(data, q):
    q = norm(q)
    exact, part = [], []
    for t in data["terms"]:
        names = [norm(t["id"])] + [norm(a) for a in t["aliases"]]
        if q in names:
            exact.append(t)
        elif any(q in n or n in q for n in names if len(n) >= 3):
            part.append(t)
    return exact or part


def fmt_pages(z):
    parts = []
    # (zone key in tutorial_index.json, label shown)
    for zone, label in (("corpo", "body"), ("glossario", "glossary"), ("licenca", "license(ignore)")):
        if zone in z:
            ps = ",".join(str(p) for p in z[zone])
            parts.append(f"{label} p.{ps}")
    return "; ".join(parts) if parts else "absent"


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    data = load()
    if "--list" in argv:
        print("# Curated terms (use any id or alias):")
        for t in data["terms"]:
            print(f"- {t['id']}  (aliases: {', '.join(t['aliases'])})")
        print(f"\n# {len(data['terms'])} terms; Tutorials: {', '.join(VERS)}. Anything else: NOT COVERED.")
        return 0
    if not args:
        print("error: provide a term (e.g. match, add_note, dataclass) or --list", file=sys.stderr)
        return 2
    results = []
    for q in args:
        hits = find(data, q)
        results.append({"query": q, "terms": hits})
    if as_json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0
    for r in results:
        print(f"## {r['query']}")
        if not r["terms"]:
            print("NOT COVERED: the term is not in the curated presence index of the 3.10-3.14 Tutorials. "
                  "A version cannot be stated from these sources; use references/versoes-e-datado.md (Ref marks) "
                  "or label it [extrapolation].")
            continue
        for t in r["terms"][:4]:
            print(f"- {t['id']}")
            first = None
            for v in VERS:
                z = t["pages"][v]
                print(f"    Tutorial {v}: {fmt_pages(z)}")
                if first is None and ("corpo" in z or "glossario" in z):
                    first = v
            if first is None:
                print("    => none of the 5 Tutorials has the term in the body/glossary (absence does not prove non-existence).")
            else:
                absent = [v for v in VERS if v < first]
                msg = f"    => first presence in the body/glossary: Tutorial {first}"
                if absent:
                    msg += f" (absent in {', '.join(absent)}). [inference] about the introduction: presence in the Tutorial is not a version mark"
                else:
                    msg += " (already present in the oldest one provided, 3.10: nothing can be concluded about earlier versions)"
                print(msg)
    print("\n# Pages = PDF of each Tutorial (printed = PDF - 6). This is presence in the text, not a version mark.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
