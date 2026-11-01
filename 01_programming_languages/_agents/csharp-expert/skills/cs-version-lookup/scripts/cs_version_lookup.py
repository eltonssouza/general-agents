#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cs_version_lookup.py - lookup of C# versions and features according to CSHist, CS12 and CS13; read-only, no network.

Usage:
  python -I cs_version_lookup.py --version 12
  python -I cs_version_lookup.py --query "records"       # in which version the source lists the feature
  python -I cs_version_lookup.py --all
Pages = PDF pages. A feature that is not in the sources: "NOT COVERED: version not stated in the sources" (exit 1).
The script does NOT know Visual Studio/.NET versions beyond those the sources cite ('platform' field).
Queries match the English feature names and the original Portuguese names (features_pt).
"""
import argparse
import json
import os
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def load():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cs_version_data.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def show(entry):
    print("=== %s ===" % entry["name"])
    print("Release: %s" % entry["release_date"])
    print("Platform/IDE cited in the source: %s" % (entry["platform"] or "not stated in the sources"))
    print("Source: [from source] (%s)" % entry["source"])
    for f in entry["features"]:
        print("  - %s" % f)
    if entry.get("note"):
        print("Note: %s" % entry["note"])


def main():
    ap = argparse.ArgumentParser(description="C# versions and features (CSHist, CS12, CS13).")
    ap.add_argument("--version", "-v", help="version (e.g. 12, 13, 8.0, 7.3, 2.0; accepts 'C# 12')")
    ap.add_argument("--query", "-q", help="search term (e.g. records, lock, primary, params)")
    ap.add_argument("--all", "-a", action="store_true", help="list all cataloged versions")
    a = ap.parse_args()
    data = load()
    versions = data["versions"]

    if a.version:
        def canon(x):
            x = norm(x).replace("c#", "").strip()
            return x[:-2] if x.endswith(".0") and x != "1.0" else x
        v = canon(a.version)
        found = [e for e in versions if canon(e["version"]) == v]
        if not found:
            print("NOT COVERED: version '%s' is not in the sources (CSHist covers C# 1.0 to 14)." % a.version)
            return 1
        for e in found:
            show(e)
        return 0

    if a.query:
        q = norm(a.query).strip()
        hits = []
        for e in versions:
            qs = {q, q[:-1]} if len(q) > 4 and q.endswith("s") else {q}
            feats = [f for f in e["features"] if any(x in norm(f) for x in qs)]
            for i, fpt in enumerate(e.get("features_pt", [])):
                if any(x in norm(fpt) for x in qs) and e["features"][i] not in feats:
                    feats.append(e["features"][i])
            if feats:
                hits.append((e, feats))
        if not hits:
            print("NOT COVERED: '%s' is not listed as a feature in the sources: version not stated in the sources." % a.query)
            print("If you add to it, label it [extrapolation].")
            return 1
        for e, feats in hits:
            print("--- %s (%s) | [from source] (%s) ---" % (e["name"], e["release_date"], e["source"]))
            print("Platform cited: %s" % (e["platform"] or "not stated in the sources"))
            for f in feats:
                print("  * %s" % f)
        return 0

    if a.all:
        for e in versions:
            print("%-7s %-18s %-60s [from source] (%s)" % (e["name"], e["release_date"], (e["platform"] or "platform not stated")[:60], e["source"]))
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
