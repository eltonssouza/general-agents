# -*- coding: utf-8 -*-
"""
Skill: perf-topic-lookup
Shortcut for looking up the topic index of *High Performance Browser Networking* (Grigorik, O'Reilly, 2013).

- The index pages are PDF pages (printed = PDF - 18).
- The index is only a shortcut: it points to the topic, the pages and the reference in references/.
  Check the reference (and, if needed, the PDF) before citing.
- Terms the book does not use (HPACK, TLS 1.3, QUIC, defer/async, preload etc.) are
  answered by the index's "not_in_book" section, with the [extrapolation] warning.
- Queries match in English and in Portuguese (keywords of both languages are indexed).

Usage:
  python -I perf_lookup.py --list
  python -I perf_lookup.py sse
  python -I perf_lookup.py "tls 1.3"
Read-only, no network.
"""

import os
import re
import sys
import json
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _has(q, text):
    """Whole-word search for short queries (e.g. 'sse'); substring for the others."""
    text = text.lower()
    if len(q) <= 3:
        return re.search(r"(?<![a-z0-9])" + re.escape(q) + r"(?![a-z0-9])", text) is not None
    return q in text


def main():
    parser = argparse.ArgumentParser(description="Look up the HPBN topic index (Grigorik, 2013)")
    parser.add_argument("query", nargs="?", default="", help="Search term or topic key")
    parser.add_argument("--list", action="store_true", help="List all indexed topics")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, "perf_index.json")

    if not os.path.exists(index_path):
        print(f"Error: index file not found at {index_path}", file=sys.stderr)
        sys.exit(1)

    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", {})
    absent = data.get("not_in_book", {})

    if args.list or not args.query:
        print("HPBN index topics (PDF pages; printed = PDF - 18):")
        print("=" * 72)
        for key, info in sorted(topics.items()):
            print(f"- {key:36} | {info['name']}")
        print("=" * 72)
        print("Usage: python -I perf_lookup.py <term_or_key>")
        print("The index is a shortcut: check the indicated reference before citing.")
        return

    q = args.query.lower().strip()

    if q in absent:
        print(f"WARNING: '{args.query}' is not in the book as such.")
        print(absent[q])
        print("-" * 60)

    if q in topics:
        show_topic(q, topics[q])
        return

    matches = []
    for key, info in topics.items():
        score = 0
        if _has(q, key.replace("_", " ")):
            score += 10
        if _has(q, info["name"]):
            score += 8
        if any(_has(q, k) for k in info.get("keywords", [])):
            score += 6
        if _has(q, info["summary"]):
            score += 4
        for m in info.get("key_mechanisms", []):
            if _has(q, m):
                score += 3
        if score > 0:
            matches.append((score, key, info))

    matches.sort(key=lambda x: x[0], reverse=True)

    if not matches:
        if q not in absent:
            print(f"No topic found for: '{args.query}'")
            print("Try: tcp, tls, alpn, mobile, rrc, http2, xhr, sse, websocket, webrtc, polling, cache.")
        sys.exit(0)

    print(f"Results for '{args.query}': {len(matches)} found")
    print("=" * 60)
    for score, key, info in matches:
        show_topic(key, info)
        print("-" * 60)


def show_topic(key, info):
    print(f"TOPIC: {info['name']} [{key}]")
    print(f"CITATION: [from source] ({info['citation']})")
    print(f"PDF PAGES: {', '.join(str(p) for p in info['pages'])}")
    if info.get("ref"):
        print(f"REFERENCE: references/{info['ref']}")
    print("\nSUMMARY:")
    print(info["summary"])
    print("\nKEY POINTS (with page):")
    for mech in info.get("key_mechanisms", []):
        print(f"  * {mech}")


if __name__ == "__main__":
    main()
