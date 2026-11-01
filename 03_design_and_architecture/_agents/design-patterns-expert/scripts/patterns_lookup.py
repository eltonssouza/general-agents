# -*- coding: utf-8 -*-
"""
patterns_lookup.py - deterministic topic lookup for design-patterns-expert (read-only, no network).

ORIGIN OF THE RULES: the index (patterns_index.json) was curated by hand from reading the pages of the four PDFs
(RG = capture of the Refactoring.Guru website; GPP = Game Programming Patterns, web capture; CC = Clean Code sample;
PEAA = PoEAA sample). Pages = PDF page. No external knowledge goes into the index.

Each topic has a status:
  texto              - the PDF has the text about the topic
  so_sumario_indice  - the PDF only has the table of contents/index (the chapter is not in the sample)
  referencia_cruzada - the topic only appears cited inside other chapters
  ausente            - the chapter is missing from the PDF (e.g. Subclass Sandbox, GPP p.190 is a 404)
Terms without a topic and terms in the `sem_cobertura` list (not covered) result in "NOT COVERED" (exit code 1).
Search terms may be written in Portuguese or English (the aliases in the index carry both).

Usage:
  python -I patterns_lookup.py "observer"            # search by term
  python -I patterns_lookup.py --list                # list the topics
  python -I patterns_lookup.py --topic game_loop     # exact topic (key)
  python -I patterns_lookup.py --concept game_loop   # v1 compatible
  python -I patterns_lookup.py --query "clean code"  # v1 compatible
  python -I patterns_lookup.py "singleton" --json    # JSON output
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
INDEX_FILE = os.path.join(HERE, "patterns_index.json")
SRC = {
    "RG": "Refactoring.Guru (website capture, 279 pages)",
    "GPP": "Game Programming Patterns (Nystrom, web capture, 338 pages)",
    "CC": "Clean Code (sample: Ch. 1 only, 67 pages)",
    "PEAA": "PoEAA (sample: Introduction and Ch. 3, 78 pages)",
}
STATUS_TXT = {
    "texto": "text present in the PDF",
    "so_sumario_indice": "ALERT: only table of contents/index; the chapter is NOT in the sample",
    "referencia_cruzada": "ALERT: only cross-references; no formal definition in the sample",
    "ausente": "ALERT: chapter ABSENT from the PDF",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    for ch in "-_/'’":
        s = s.replace(ch, " ")
    return " ".join(s.split())


def load():
    if not os.path.exists(INDEX_FILE):
        print("Error: index not found: %s" % INDEX_FILE, file=sys.stderr)
        sys.exit(2)
    with open(INDEX_FILE, encoding="utf-8") as f:
        return json.load(f)


def score(topic, q):
    keys = [norm(topic["key"]), norm(topic["title"])] + [norm(a) for a in topic.get("aliases", [])]
    best = 0
    for k in keys:
        if q == k:
            best = max(best, 100)
        elif q and (q in k or k in q) and len(k) >= 3:
            best = max(best, 60)
    qtok = set(q.split())
    for k in keys:
        ktok = set(k.split())
        common = qtok & ktok
        if common and len(common) / float(min(len(qtok), len(ktok))) >= 0.5:
            best = max(best, 20 + 5 * len(common))
    return best


def show(topic, as_json=False):
    if as_json:
        print(json.dumps(topic, ensure_ascii=False, indent=1))
        return
    print("=== %s [%s] ===" % (topic["title"], topic["key"]))
    print("Status: %s" % STATUS_TXT.get(topic["status"], topic["status"]))
    for e in topic["entries"]:
        print("  %-4s p.%-8s %s" % (e["sigla"], e["pages"], e["note"]))
    if topic.get("note"):
        print("Note: %s" % topic["note"])
    if topic.get("reference"):
        print("Detail in: references/%s" % topic["reference"])
    print("(pages = PDF; see references/INDEX.md)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Topic lookup for design-patterns-expert (no network).")
    ap.add_argument("term", nargs="*", help="term to search for")
    ap.add_argument("--list", action="store_true", help="list all topics")
    ap.add_argument("--topic", help="exact topic key")
    ap.add_argument("--concept", help="(v1) key or part of the key")
    ap.add_argument("--query", help="(v1) search term")
    ap.add_argument("--json", action="store_true", help="JSON output")
    a = ap.parse_args(argv)
    data = load()
    topics = data["topics"]

    if a.list:
        print("=== %d indexed topics (pages = PDF) ===" % len(topics))
        for t in topics:
            print(" - %-26s %-52s [%s]" % (t["key"], t["title"], t["status"]))
        print("Terms NOT COVERED by the sources: " + ", ".join(data["sem_cobertura"]))
        return 0

    term = a.topic or a.concept or a.query or " ".join(a.term)
    if not term.strip():
        ap.print_help()
        return 2
    q = norm(term)

    if a.topic or a.concept:
        for t in topics:
            if t["key"] == a.topic or t["key"] == a.concept:
                show(t, a.json)
                return 0

    nc = [norm(x) for x in data["sem_cobertura"]]
    hits = sorted(((score(t, q), t) for t in topics), key=lambda x: -x[0])
    hits = [(s, t) for s, t in hits if s > 0]
    if q in nc and not hits:
        print("NOT COVERED: '%s' is not addressed by the package sources (RG, GPP, CC sample, PEAA sample)." % term)
        print("If you answer, label it [extrapolation] or refer to another specialist.")
        return 1
    if not hits:
        print("NOT COVERED: no indexed topic for '%s'." % term)
        print("Use --list to see the topics. If you answer, label it [extrapolation].")
        return 1
    top = hits[0][0]
    shown = [t for s, t in hits if s >= max(20, top - 20)][:4]
    for t in shown:
        show(t, a.json)
        print()
    if q in nc:
        print("Note: '%s' is also listed as a NOT COVERED term; do not attribute anything beyond what the pages above say." % term)
    return 0


if __name__ == "__main__":
    sys.exit(main())
