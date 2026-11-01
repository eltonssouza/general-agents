#!/usr/bin/env python3
"""Queries the list of JEPs from the supplied OpenJDK release notes (JDK 11, 17, 21, 22 and 26).

Usage:
    python -I jdk_lookup.py [--json] TERM [TERM ...]       # search by title or JEP number
    python -I jdk_lookup.py --jdk 21                       # lists the JEPs of a JDK
    python -I jdk_lookup.py --coverage                     # shows which JDKs the sources cover

The data (jdk_features.json) comes ONLY from the "Features" section of each release notes page:
JEP number, title and GA date. There is NO description of any feature in the sources.
The "state" (Preview/Incubator) is what appears in parentheses in the title itself; a title
without a mark does NOT prove the feature is final (that is an inference).
Read-only; no network. Exit code: 0 if it ran; 2 for a usage error.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COVERED = [11, 17, 21, 22, 26]


def load():
    with open(os.path.join(HERE, "jdk_features.json"), encoding="utf-8") as fh:
        return json.load(fh)


def fmt(r):
    st = f" [{r['marker']}]" if r["marker"] else " [no mark in the title]"
    return f"- JDK {r['jdk']} — JEP {r['jep']}: {r['title']}{st}"


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--jdk", type=int)
    ap.add_argument("--coverage", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    data = load()
    feats = data["features"]
    if a.coverage:
        print("# Coverage of the sources (OpenJDK release notes)")
        for v in COVERED:
            rel = data["releases"][str(v)]
            print(f"- JDK {v}: GA {rel['ga']}; LTS: {rel['lts_note']}; {sum(1 for f in feats if f['jdk']==v)} JEPs listed")
        missing = [v for v in range(9, 27) if v not in COVERED]
        print(f"- NO release notes in the sources: JDK {', '.join(map(str, missing))} (and any version above 26)")
        print("- No page describes what a JEP does; only number and title.")
        return 0
    if a.jdk is not None:
        sel = [f for f in feats if f["jdk"] == a.jdk]
        if a.jdk not in COVERED:
            print(f"No release notes for JDK {a.jdk} in the sources (covered: {COVERED}).")
            return 0
        if a.json:
            json.dump(sel, sys.stdout, ensure_ascii=False, indent=2)
            print()
        else:
            rel = data["releases"][str(a.jdk)]
            print(f"# JDK {a.jdk} — GA {rel['ga']} — {len(sel)} JEPs (number and title only)")
            for r in sel:
                print(fmt(r))
        return 0
    if not a.terms:
        print("error: provide terms (e.g. 'virtual threads', 444), --jdk N or --coverage", file=sys.stderr)
        return 2
    terms = [t.lower() for t in a.terms]
    sel = [f for f in feats if all(t in f["title"].lower() or t == str(f["jep"]) for t in terms)]
    sel.sort(key=lambda f: (f["title"].lower(), f["jdk"]))
    if a.json:
        json.dump(sel, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    if not sel:
        print(f"No JEP matched {a.terms} in JDKs {COVERED}.")
        print("This does NOT mean the feature does not exist: the sources only cover these five JDKs and only the listed JEPs.")
        return 0
    print(f"# {len(sel)} result(s) for {a.terms} — JEP number and title only; the sources do not describe the feature")
    for r in sel:
        print(fmt(r))
    print("\nThe state comes from the title (Preview/Incubator). A title without a mark does not prove the feature is final [inference].")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
