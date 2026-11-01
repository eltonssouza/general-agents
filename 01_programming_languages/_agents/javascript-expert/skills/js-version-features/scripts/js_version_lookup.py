#!/usr/bin/env python3
"""Queries the catalog of versions, epochs, Annex B and the [HOST] boundary of JavaScript in the sources.

Uso:
    python -I js_version_lookup.py TERMO [TERMO ...]
    python -I js_version_lookup.py --category {dated,unversioned,annex-b,host,missing}
    python -I js_version_lookup.py --summary
    python -I js_version_lookup.py --json TERMO

Read-only (reads js_version_data.json next to the script), no network.
Reminder: being in the 2026 Spec only proves that the feature exists in ES2026 (Spec p.25). When the
category is 'unversioned', answer 'version not stated in the sources'.
Exit code: 0 if it ran; 2 for a usage error.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(HERE, "js_version_data.json"), encoding="utf-8") as fh:
        return json.load(fh)


def fmt_item(r):
    return (
        f"- [{r['category']}] {r['name']} — version in the sources: {r['version']} | "
        f"label: {r['label']}\n  detail: {r['detail']} ({r['citations']})"
    )


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--category", choices=["dated", "unversioned", "annex-b", "host", "missing"])
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    data = load()
    items = data["items"]

    if a.summary:
        print("# Summary of versions and epochs in the JavaScript sources")
        for k, v in data["sources_overview"].items():
            print(f"- {k}: {v}")
        counts = {}
        for it in items:
            counts[it["category"]] = counts.get(it["category"], 0) + 1
        print("\n## Count by category in the catalog")
        for c, n in counts.items():
            print(f"- {c}: {n} entry(ies)")
        return 0

    if a.category:
        sel = [it for it in items if it["category"] == a.category]
        if a.json:
            json.dump(sel, sys.stdout, ensure_ascii=False, indent=2)
            print()
            return 0
        print(f"# Category '{a.category}' — {len(sel)} entry(ies)\n")
        for r in sel:
            print(fmt_item(r))
        return 0

    if not a.terms:
        print(__doc__)
        return 2

    terms = [t.lower() for t in a.terms]
    sel = [
        it
        for it in items
        if all(
            t in it["name"].lower()
            or t in it["detail"].lower()
            or any(t in kw.lower() for kw in it.get("keywords", []))
            for t in terms
        )
    ]
    if a.json:
        json.dump(sel, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    if not sel:
        print(f"No entry in the version catalog matched {a.terms}.")
        print(
            "Tip: use spec_lookup.py to locate the section in ECMA-262 and versoes-e-datado.md. "
            "If the feature is in the Spec with no note in Annexes E/F and no date in EJpt, the answer is "
            "'version not stated in the sources'."
        )
        return 0
    print(f"# {len(sel)} result(s) for {a.terms}\n")
    for r in sel:
        print(fmt_item(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
