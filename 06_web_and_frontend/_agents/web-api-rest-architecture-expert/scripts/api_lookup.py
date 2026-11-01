# -*- coding: utf-8 -*-
"""
Skill: api-topic-lookup
Looks up topics of *Web API Design: The Missing Link* (Apigee/Google, 2018) indexed in
api_index.json: PDF pages, summary and rules. Standard library only, no network, read-only.
The index is a shortcut: check the page in the reference before citing [from source].
Queries are matched in English and in Portuguese (the "keywords" field of each topic).
"""

import os
import sys
import json
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Look up RESTful API design topics (Apigee)")
    parser.add_argument("query", nargs="?", default="", help="Search term or topic identifier")
    parser.add_argument("--list", action="store_true", help="List all indexed topics")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(script_dir, "api_index.json")

    if not os.path.exists(index_path):
        print(f"Error: index file not found at {index_path}", file=sys.stderr)
        sys.exit(1)

    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = data.get("topics", {})

    if args.list or not args.query:
        print("Topics available in the API Design index (Apigee):")
        print("=" * 65)
        for key, info in sorted(topics.items()):
            print(f"- {key:30} | {info['name']} ({info['citation']})")
        print("=" * 65)
        print("Usage: python api_lookup.py <term_or_topic>")
        return

    q = args.query.lower().strip()

    if q in topics:
        show_topic(q, topics[q])
        return

    matches = []
    for key, info in topics.items():
        score = 0
        if q in key.lower():
            score += 10
        if q in info["name"].lower():
            score += 8
        if any(q in kw.lower() for kw in info.get("keywords", [])):
            score += 8
        if q in info["summary"].lower():
            score += 4
        for r in info.get("rules", []):
            if q in r.lower():
                score += 3
        if score > 0:
            matches.append((score, key, info))

    matches.sort(key=lambda x: x[0], reverse=True)

    if not matches:
        print(f"No topic found for the query: '{args.query}'")
        print("Try: links, urls, flat, query, pagination, status, actions, versioning, oauth")
        sys.exit(0)

    print(f"Results for '{args.query}': {len(matches)} found")
    print("=" * 65)
    for score, key, info in matches:
        show_topic(key, info)
        print("-" * 65)

def show_topic(key, info):
    print(f"TOPIC: {info['name']} [{key}]")
    print(f"CITATION: [from source] ({info['citation']})")
    print(f"PDF PAGES: {info['pages']}")
    print("\nSUMMARY:")
    print(info['summary'])
    print("\nDESIGN RULES AND GUIDELINES:")
    for rule in info.get("rules", []):
        print(f"  * {rule}")

if __name__ == "__main__":
    main()
