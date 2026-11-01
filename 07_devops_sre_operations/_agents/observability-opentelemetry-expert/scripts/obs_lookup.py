# -*- coding: utf-8 -*-
"""
Skill: obs-topic-lookup
Looks up topics from the two Refcards (DOW and OTW) with pages and what is NOT in them.
Read-only: reads obs_index.json from the same directory. No network. Deterministic.
Usage: python -I obs_lookup.py <term> | --list   (Portuguese or English terms)
Prints "NOT COVERED" when no topic matches: the collection does not cover the term.
"""
import argparse
import json
import os
import sys
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


OUT = ["java", "golang", "node", "dotnet", ".net", "grafana", "loki", "tempo", "slo", "sli", "ebpf",
       "traceparent", "baggage", "cardinalidade", "cardinality", "exemplar"]


def show(key, info):
    print(f"TOPIC: {info['name']} [{key}]")
    print(f"CITATION: [from source] ({info['citation']})")
    print("SUMMARY:", info["summary"])
    print("SOURCE RULES (with page):")
    for r in info.get("rules", []):
        print("  *", r)
    nib = info.get("not_in_book", [])
    if nib:
        print("NOT IN THE SOURCE (label [inference]/[extrapolation]/[DATED]):")
        for n in nib:
            print("  !", n)
    print()


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="DOW/OTW lookup")
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "obs_index.json")
    with open(path, encoding="utf-8") as f:
        topics = json.load(f)["topics"]
    if a.list or not a.query:
        for k, v in sorted(topics.items()):
            print(f"- {k:28} | {v['name']} ({v['citation']})")
        return 0
    q = norm(a.query)
    import re
    out = [w for w in OUT if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", q)]
    if out:
        print(f"NOT COVERED WARNING: {', '.join(out)} is not addressed by the Refcards; what follows may be only a partial match on another word of the query.")
        print()
    if q in topics:
        show(q, topics[q])
        return 0
    words = [w for w in q.replace(",", " ").split() if len(w) > 1]
    scored = []
    for k, v in topics.items():
        score = 0
        hay = norm(v["name"] + " " + v["summary"])
        for w in words:
            if any(w == norm(kw) for kw in v["keywords"]):
                score += 3
            elif any(w in norm(kw) or norm(kw) in w for kw in v["keywords"] if len(norm(kw)) > 3):
                score += 2
            elif w in hay:
                score += 1
        if score:
            scored.append((score, k))
    if not scored:
        print(f"NOT COVERED: no topic in the DOW/OTW Refcards matches '{a.query}'.")
        print("Answer only as [extrapolation] (if asked) and state that the sources do not address the subject.")
        return 0
    scored.sort(key=lambda t: (-t[0], t[1]))
    for _, k in scored[:3]:
        show(k, topics[k])
    return 0


if __name__ == "__main__":
    sys.exit(main())
