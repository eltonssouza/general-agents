# -*- coding: utf-8 -*-
"""
css_lookup.py - deterministic lookup in the css_index.json index (read-only, no network).

Usage:
  python css_lookup.py flexbox            # topic by key or text search
  python css_lookup.py flex-grow          # property/value/at-rule -> pages
  python css_lookup.py --list             # list topics
  python css_lookup.py --props            # list indexed properties
  python css_lookup.py grid --json        # JSON output

Each answer carries the citation in the (CSSHB p.N) format, the known gaps and the dated content.
If nothing is found, the script says there is NO coverage (it does not invent a page).
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
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def fmt_pages(pages):
    pages = sorted(set(pages))
    out, start, prev = [], None, None
    for p in pages:
        if start is None:
            start = prev = p
        elif p == prev + 1:
            prev = p
        else:
            out.append((start, prev))
            start = prev = p
    if start is not None:
        out.append((start, prev))
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)


def show_topic(key, t):
    print(f"TOPIC: {t['name']} [{key}]")
    print(f"SOURCE: {t['source']}  |  CITATION: [from source] ({t['citation']})")
    print(f"PAGES: {fmt_pages(t['pages'])}")
    print(f"REFERENCE: references/{t['reference_file']}")
    print("\nSUMMARY:\n  " + t["summary"])
    print("\nMECHANISMS:")
    for m in t["key_mechanisms"]:
        print("  * " + m)
    if t.get("gaps"):
        print("\nGAPS (treat as [extrapolation] if the user asks):")
        for g in t["gaps"]:
            print("  - " + g)
    if t.get("dated"):
        print("\nDATED:")
        for d in t["dated"]:
            print("  - [DATED] " + d)


def show_prop(name, p, topics):
    t = topics.get(p["topic"], {})
    print(f"ITEM: {name}")
    print(f"CITATION: [from source] (CSSHB p.{fmt_pages(p['pages'])})")
    print(f"TOPIC: {p['topic']} -> references/{t.get('reference_file', '?')}")
    print(f"NOTE: {p['note']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Looks up the index of the modern-css-layout-expert agent")
    ap.add_argument("query", nargs="?", default="", help="topic, property or term")
    ap.add_argument("--list", action="store_true", help="list topics")
    ap.add_argument("--props", action="store_true", help="list indexed properties")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--index", default=None, help="alternative path to css_index.json")
    a = ap.parse_args(argv)

    path = a.index or os.path.join(os.path.dirname(os.path.abspath(__file__)), "css_index.json")
    if not os.path.exists(path):
        print(f"Error: index not found at {path}", file=sys.stderr)
        return 1
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    topics, props = data["topics"], data["properties"]

    if a.list or (not a.query and not a.props):
        print("Indexed topics:")
        for k, t in sorted(topics.items()):
            print(f"- {k:20} | {t['name']} ({t['citation']})")
        return 0
    if a.props:
        print("Indexed properties/items:")
        for k in sorted(props):
            print(f"- {k:28} CSSHB p.{fmt_pages(props[k]['pages'])}")
        return 0

    q = norm(a.query)
    results = {"query": a.query, "topics": [], "properties": []}

    # 1) exact property (with or without '--', ':' etc.)
    exact = [k for k in props if norm(k) == q or norm(k).lstrip("-:@") == q.lstrip("-:@")]
    # 2) exact topic
    if q in topics:
        results["topics"].append(q)
    # 3) text search
    scored = []
    for k, t in topics.items():
        s = 0
        if q in norm(k):
            s += 10
        if q in norm(t["name"]):
            s += 8
        if q in norm(t.get("name_pt", "")):  # Portuguese queries still match
            s += 8
        if q in norm(t["summary"]):
            s += 4
        s += sum(3 for m in t["key_mechanisms"] if q in norm(m))
        if s:
            scored.append((s, k))
    scored.sort(reverse=True)
    for _, k in scored:
        if k not in results["topics"]:
            results["topics"].append(k)
    results["properties"] = exact or [k for k in props if q in norm(k)][:12]

    if a.json:
        out = {
            "query": a.query,
            "properties": {k: props[k] for k in results["properties"]},
            "topics": {k: topics[k] for k in results["topics"][:3]},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if not results["topics"] and not results["properties"]:
        print(f"NOT COVERED: '{a.query}' is not in the collection index (CSSHB, MDNFS, MDNL).")
        print("If you answer, label it [extrapolation] and do not attribute a page to the book.")
        return 0

    for k in results["properties"]:
        show_prop(k, props[k], topics)
        print("-" * 60)
    for k in results["topics"][:3]:
        show_topic(k, topics[k])
        print("-" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
