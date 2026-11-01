# -*- coding: utf-8 -*-
"""
Skill: run-topic-lookup
Looks up topics of the RUN book (Building Serverless Applications with Google Cloud Run, 2020)
with PDF pages and what the book does NOT say. Read-only: reads run_index.json from the same
directory. No network. Deterministic. Accepts queries in English or Portuguese.
Usage: python -I run_lookup.py <term> | --list
Prints "NOT COVERED" when no topic matches or the term is known to be outside the book.
"""
import argparse
import json
import os
import re
import sys
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# Terms known to be ABSENT from the book (confirmed by searching the text: see tests/citation-checks.json)
OUT = ["jobs", "job", "secret manager", "set-secrets", "min-instances", "gen2", "segunda geracao",
       "2nd gen", "second generation", "cpu boost", "startup cpu", "always allocated", "always-allocated", "no-cpu-throttling",
       "probe", "health check", "eventarc", "cloud deploy", "binary authorization", "websocket", "grpc",
       "direct vpc", "serverless neg", "cloud armor", "workload identity", "no-traffic", "gcloud run deploy --source",
       "lambda", "opentelemetry", "iap", "identity platform"]


NOTES = {"lambda": "AWS Lambda is only mentioned in passing as an example of FaaS (RUN p.33); for Lambda, hand off to aws-lambda-serverless-expert.",
         "opentelemetry": "the book uses OpenCensus (RUN p.169); for OpenTelemetry, hand off to observability-opentelemetry-expert."}


def show(key, info):
    print(f"TOPIC: {info['name']} [{key}]")
    print(f"CITATION: [from source] ({info['citation']})  (PDF page = printed + 28)")
    print("SUMMARY:", info["summary"])
    print("BOOK RULES (with page):")
    for r in info.get("rules", []):
        print("  *", r)
    nib = info.get("not_in_book", [])
    if nib:
        print("NOT IN THE SOURCE (label as [inference]/[extrapolation]/[DATED] or NOT COVERED):")
        for n in nib:
            print("  !", n)
    print()


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Look up the RUN book (Cloud Run, 2020)")
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_index.json")
    with open(path, encoding="utf-8") as f:
        topics = json.load(f)["topics"]
    if a.list or not a.query:
        for k, v in sorted(topics.items()):
            print(f"- {k:28} | {v['name']} ({v['citation']})")
        return 0
    q = norm(a.query)
    out = [w for w in OUT if re.search(r"(?<![a-z0-9-])" + re.escape(norm(w)) + r"(?![a-z0-9-])", q)]
    if out:
        print(f"WARNING NOT COVERED: {', '.join(out)} is not covered by the book (2020); what follows may be only a partial match on another word of the query.")
        for w in out:
            if w in NOTES:
                print("NOTE:", NOTES[w])
        print()
    if q in topics:
        show(q, topics[q])
        return 0
    q_rest = q
    for w in out:
        q_rest = re.sub(r"(?<![a-z0-9-])" + re.escape(norm(w)) + r"(?![a-z0-9-])", " ", q_rest)
    words = [w for w in re.split(r"[\s,;/]+", q_rest) if len(w) > 1]
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
    strong = [k for k, v in topics.items()
              if any(w == norm(kw) for w in words for kw in v["keywords"])
              or any(len(norm(kw)) > 3 and norm(kw) in q_rest for kw in v["keywords"])]
    if out and not strong:
        print("NOT COVERED: the book does not cover the term(s) above. Answer only as [extrapolation] [DATED], if asked.")
        return 0
    if not scored:
        print(f"NOT COVERED: no topic of the RUN book matches '{a.query}'.")
        print("Answer only as [extrapolation] (if asked) and state that the book does not cover the subject.")
        return 0
    scored.sort(key=lambda t: (-t[0], t[1]))
    if out:
        scored = [(s, k) for s, k in scored if k in strong]
    for _, k in scored[:3]:
        show(k, topics[k])
    return 0


if __name__ == "__main__":
    sys.exit(main())
