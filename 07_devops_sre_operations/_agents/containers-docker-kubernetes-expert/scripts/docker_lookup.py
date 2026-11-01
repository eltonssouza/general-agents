# -*- coding: utf-8 -*-
"""
Skill: docker-topic-lookup
Looks up topics of the Docker Handbook (DOCKHB, 148 pp.) and Kubernetes Basics (K8SB, 2 pp.).
Read-only: reads docker_index.json from the same directory. No network. Deterministic.
Each topic carries 'rules' (stated in the source, with PDF page), 'not_in_book' (what the
source does NOT say: it may only be said as [inference]/[extrapolation]) and 'datado' (dated) when there is
content that has changed since the edition (2021).
Queries may be in English or Portuguese (the index keeps Portuguese keywords).
No match: prints "NOT COVERED" (the collection does not cover the subject).
"""
import argparse
import json
import os
import sys
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def show_topic(key, info):
    print(f"TOPIC: {info['name']} [{key}]")
    if info["citation"].startswith(("nenhuma", "none")):
        print("CITATION: none (unusable source; everything here is [extrapolation])")
    else:
        print(f"CITATION: [from source] ({info['citation']})")
    print("\nSUMMARY:")
    print(info["summary"])
    print("\nSOURCE RULES/FACTS (with PDF page; items marked [inference]/[extrapolation]/[observation] are not from the book):")
    for rule in info.get("rules", []):
        print(f"  * {rule}")
    for item in info.get("datado", []):
        print(f"\n[DATED] {item}")
    nib = info.get("not_in_book", [])
    if nib:
        print("\nNOT IN THE SOURCE (label as [extrapolation]; never attribute to the book):")
        for item in nib:
            print(f"  ! {item}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Look up topics of the Docker Handbook / Kubernetes Basics")
    ap.add_argument("query", nargs="?", default="", help="Search term or topic key")
    ap.add_argument("--list", action="store_true", help="List all indexed topics")
    ap.add_argument("--json", action="store_true", help="JSON output (for programmatic use)")
    args = ap.parse_args()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker_index.json")
    if not os.path.exists(path):
        print(f"Error: index not found at {path}", file=sys.stderr)
        sys.exit(1)
    data = json.load(open(path, encoding="utf-8"))
    topics = data["topics"]

    if args.list or not args.query:
        print("Available topics (DOCKHB 148 pp.; K8SB 2 pp.):")
        print("=" * 72)
        for key, info in sorted(topics.items()):
            print(f"- {key:30} | {info['name']} ({info['citation']})")
        print("=" * 72)
        print("Page convention: PDF page (the book has no printed number).")
        return

    q = norm(args.query).strip()
    if args.query in topics:
        if args.json:
            print(json.dumps({args.query: topics[args.query]}, ensure_ascii=False, indent=1))
        else:
            show_topic(args.query, topics[args.query])
        return

    words = [w for w in q.replace(",", " ").split() if len(w) > 1]
    matches = []
    for key, info in topics.items():
        score = 0
        neg = 0
        for w in words + ([q] if len(words) > 1 else []):
            if w in norm(key):
                score += 10
            if w in norm(info["name"]):
                score += 8
            if any(w == norm(k) or (len(w) > 3 and (w in norm(k))) for k in info.get("keywords", [])):
                score += 9
            if w in norm(info["summary"]):
                score += 4
            score += sum(3 for r in info.get("rules", []) if w in norm(r))
            neg += sum(2 for r in info.get("not_in_book", []) if w in norm(r))
        if score > 0 or neg > 0:
            matches.append((score, key, info, neg))
    matches.sort(key=lambda x: (-x[0], -x[3], x[1]))
    if matches and all(m[0] == 0 for m in matches):
        print(f"NOT COVERED DIRECTLY: '{args.query}' only appears in 'NOT IN THE SOURCE' lists (the collection does NOT cover it).")
        print("Topics that delimit the gap:")
        for _, key, info, _n in matches[:3]:
            print(f"- [{key}] {info['name']}: " + "; ".join(x for x in info.get("not_in_book", []) if norm(args.query.split()[0]) in norm(x)))
        return

    if not matches:
        print(f"NOT COVERED: no topic for '{args.query}'.")
        print("The collection (the 2021 Docker Handbook and the Kubernetes Basics index page) probably does not cover the subject.")
        print("Answer as a declared [extrapolation], or say it is outside the collection. Use --list to see what is there.")
        return

    top = [(m[0], m[1], m[2]) for m in matches[:3]]
    if args.json:
        print(json.dumps({k: i for _, k, i in top}, ensure_ascii=False, indent=1))
        return
    print(f"Results for '{args.query}': {len(matches)} topic(s) (showing up to 3)")
    print("=" * 72)
    for _, key, info in top:
        show_topic(key, info)
        print("-" * 72)


if __name__ == "__main__":
    main()
