#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sysdesign_lookup.py - deterministic topic lookup in the curated index `sysdesign_index.json`.

Origin of the index: built by manually reading the 11 source PDFs (SAP, SDH, MS-MIC, MS-CLD, MS-WEB, EDS, SBC, SOA, APIGW,
JMG, REST). Each entry carries a PDF page (package convention; see references/INDEX.md), its own note (paraphrase,
no copied passages), and `terms` that `tests/verify_citations.py` checks against the page text.
Concepts the corpus does NOT cover appear with coverage = "NOT COVERED" (e.g., Little's Law, Half-Open, Two-Pizza).
Queries are accent- and case-insensitive; Portuguese keywords (e.g., "escalabilidade", "disjuntor") keep working.

Usage:
  python -I scripts/sysdesign_lookup.py --list
  python -I scripts/sysdesign_lookup.py --concept circuit-breaker
  python -I scripts/sysdesign_lookup.py --query "backoff"
  python -I scripts/sysdesign_lookup.py --concept saga --json
Exit codes: 0 = concept/query found (including a declared 'NOT COVERED'); 1 = nothing in the index
(prints NOT COVERED); 2 = incorrect usage/missing index.
Read-only, no network.
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

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(HERE, "sysdesign_index.json")


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def load_index():
    if not os.path.exists(INDEX_FILE):
        print(f"Error: index not found: {INDEX_FILE}", file=sys.stderr)
        sys.exit(2)
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def show(entry, as_json=False):
    if as_json:
        print(json.dumps(entry, ensure_ascii=False, indent=1))
        return
    print(f"=== {entry['title']} [key: {entry['key']}] coverage: {entry['coverage']} ===")
    if entry["coverage"] == "NOT COVERED":
        print("NOT COVERED: the corpus does not present this concept as its own definition.")
    for e in entry.get("entries", []):
        sig, pg = e["cite"].split(" p.")
        print(f"  [from source] ({sig} p.{pg}): {e['note']}")
    if entry.get("nota"):
        print(f"  Note: {entry['nota']}")


def cmd_list(idx):
    print(f"=== {len(idx)} concepts indexed ===")
    for c in idx:
        print(f" - {c['key']:30} {c['coverage']:14} {c['title']} ({len(c.get('entries', []))} citations)")
    return 0


def cmd_concept(idx, key, as_json):
    k = fold(key).strip()
    for c in idx:
        if fold(c["key"]) == k:
            show(c, as_json)
            return 0
    cand = [c for c in idx if k in fold(c["key"])]
    if len(cand) == 1:
        show(cand[0], as_json)
        return 0
    if len(cand) > 1:
        print(f"Ambiguous key '{key}': " + ", ".join(c["key"] for c in cand))
        return 1
    print(f"NOT COVERED: concept '{key}' is not in the index. Use --list or --query.")
    return 1


def cmd_query(idx, q, as_json):
    qf = fold(q).strip()
    hits = []
    for c in idx:
        score = 0
        if qf in fold(c["key"]):
            score += 4
        if qf in fold(c["title"]):
            score += 3
        if any(qf in fold(k) for k in c.get("keywords", [])):
            score += 2
        if qf in fold(c.get("nota", "")):
            score += 1
        if any(qf in fold(e["note"]) for e in c.get("entries", [])):
            score += 1
        if score:
            hits.append((score, c))
    if not hits:
        print(f"NOT COVERED: no indexed concept for '{q}'.")
        return 1
    hits.sort(key=lambda x: (-x[0], x[1]["key"]))
    if as_json:
        print(json.dumps([c for _, c in hits], ensure_ascii=False, indent=1))
        return 0
    print(f"=== {len(hits)} concept(s) for '{q}' ===")
    for _, c in hits[:8]:
        show(c)
        print()
    return 0


def main():
    ap = argparse.ArgumentParser(description="Topic lookup in the curated index (System Design & Microservices).")
    ap.add_argument("--list", action="store_true", help="list the concepts")
    ap.add_argument("--concept", help="concept key (e.g., saga, circuit-breaker)")
    ap.add_argument("--query", help="keyword search (accent- and case-insensitive)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    a = ap.parse_args()
    idx = load_index()
    if a.list:
        return cmd_list(idx)
    if a.concept:
        return cmd_concept(idx, a.concept, a.json)
    if a.query:
        return cmd_query(idx, a.query, a.json)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
