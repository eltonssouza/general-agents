# -*- coding: utf-8 -*-
"""
Skill: a11y-design-topic-lookup
Deterministic lookup (stdlib, no network) in the a11y_design_index.json index, which summarizes the two sources:
  WAI  = W3C WAI, Introduction to Web Accessibility (WAI p.N = PDF page)
  NDDB = Robin Williams, The Non-Designer's Design Book, 4th ed. (SAMPLE; NDDB p.N = printed page)

Usage:
  python a11y_design_lookup.py repeticao
  python a11y_design_lookup.py "tool is not enough" --source WAI
  python a11y_design_lookup.py --page 58 --source NDDB
  python a11y_design_lookup.py --list
  python a11y_design_lookup.py wcag --json

If nothing is found, the script says the topic is OUT OF SCOPE of the sources (it does not invent an answer).
Queries can be in Portuguese (with or without accents) or English.
"""
import argparse
import json
import os
import sys
import unicodedata


def norm(text):
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower().strip()


def load_index(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a11y_design_index.json")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def source_ok(topic, source):
    if not source:
        return True
    return source.upper() in topic.get("source", "").upper().split("+")


STOPWORDS = {"quem", "que", "como", "para", "por", "com", "sem", "uma", "um", "dos", "das", "nos", "nas", "the", "and",
             "of", "ou", "nao", "mais", "sobre", "qual", "quais", "diz", "livro",
             "what", "which", "who", "how", "does", "say", "about", "for", "with", "book", "not", "are", "is"}


def words(text):
    cleaned = "".join(c if c.isalnum() else " " for c in norm(text))
    return set(cleaned.split())


def word_hit(tok, wordset):
    """Match a whole word; for long tokens accept a prefix (plural/derivation)."""
    if tok in wordset:
        return True
    return len(tok) >= 5 and any(w.startswith(tok) or tok.startswith(w) and len(w) >= 5 for w in wordset)


def score_topic(key, topic, query):
    """Deterministic score: key > name > keywords > summary > key points (whole words)."""
    q = norm(query)
    tokens = [t for t in words(q) if len(t) > 2 and t not in STOPWORDS] or [q]
    score = 0
    hay_key, hay_name = norm(key), norm(topic["name"])
    hay_kw = [norm(k) for k in topic.get("keywords", [])]
    kw_words = set().union(*[words(k) for k in hay_kw]) if hay_kw else set()
    name_words, key_words = words(hay_name), words(hay_key.replace("_", " "))
    sum_words, pts_words = words(topic["summary"]), words(" ".join(topic.get("key_points", [])))
    if q in hay_kw:
        score += 12
    elif len(q) > 3 and (q in hay_name or q in hay_key):
        score += 10
    for tok in tokens:
        if word_hit(tok, key_words):
            score += 3
        if word_hit(tok, name_words):
            score += 3
        if word_hit(tok, kw_words):
            score += 3
        if word_hit(tok, sum_words):
            score += 1
        if word_hit(tok, pts_words):
            score += 1
    return score


def search(index, query, source=None):
    results = []
    for key, topic in index["topics"].items():
        if not source_ok(topic, source):
            continue
        s = score_topic(key, topic, query)
        if s > 0:
            results.append((s, key, topic))
    results.sort(key=lambda r: (-r[0], r[1]))
    return results


def by_page(index, page, source=None):
    out = []
    for key, topic in index["topics"].items():
        if not source_ok(topic, source):
            continue
        if page in topic.get("pages", []):
            out.append((0, key, topic))
    out.sort(key=lambda r: r[1])
    return out


def format_topic(key, topic):
    lines = [
        "TOPIC: %s [%s]" % (topic["name"], key),
        "SOURCE: %s | CITATION: (%s) | LABEL: [%s]" % (topic["source"], topic["citation"], topic["label"]),
        "PAGES: %s" % ", ".join(str(p) for p in topic["pages"]),
        "SUMMARY: %s" % topic["summary"],
        "KEY POINTS:",
    ]
    lines += ["  * %s" % kp for kp in topic.get("key_points", [])]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Look up topics in the WAI and NDDB (sample) sources.")
    ap.add_argument("query", nargs="?", default="", help="search term (Portuguese or English; accents optional)")
    ap.add_argument("--list", action="store_true", help="list all topics")
    ap.add_argument("--source", choices=["WAI", "NDDB", "wai", "nddb"], help="filter by source")
    ap.add_argument("--page", type=int, help="topics that cite this page (WAI: PDF page; NDDB: printed page)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--index", help="alternative path to the JSON index")
    args = ap.parse_args(argv)

    try:
        index = load_index(args.index)
    except (OSError, ValueError) as exc:
        print("Error loading the index: %s" % exc, file=sys.stderr)
        return 1

    if args.list or (not args.query and args.page is None):
        for key, topic in sorted(index["topics"].items()):
            if source_ok(topic, args.source):
                print("- %-38s | %-5s | %s (%s)" % (key, topic["source"], topic["name"], topic["citation"]))
        return 0

    if args.page is not None:
        results = by_page(index, args.page, args.source)
        header = "Topics that cite page %d" % args.page
    else:
        results = search(index, args.query, args.source)
        header = "Results for '%s'" % args.query

    if args.json:
        print(json.dumps(
            [{"key": k, "score": s, **t} for s, k, t in results], ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("No topic found for the query.")
        print("OUT OF SCOPE OF THE SOURCES: the index covers only the WAI (introduction to accessibility) and the NDDB sample")
        print("(Repetition principle, table of contents and index). Mark any answer as [extrapolation] or refer elsewhere.")
        return 0

    print("%s: %d found" % (header, len(results)))
    print("=" * 70)
    for _, key, topic in results:
        print(format_topic(key, topic))
        print("-" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
