#!/usr/bin/env python3
"""verify_citations.py - checks the page citations of graphql-expert against the extracted source text.

Usage: python -I verify_citations.py [--txt PATH.txt] [--checks citation-checks.json]
  positive: all terms in "all" must appear on the cited pages (union of the "pages").
  negative: no term in "absent" may appear on ANY page (plausible claims that the PDF does not bring).
Default text: ROOT/scratch/frameworks/GraphQL-Learn-Official.txt (ROOT = 4 levels above 14_frameworks/_agents/graphql-expert/tests).
Exit 0 if everything passes (or SKIP when the source text is missing); 1 if any check fails.
"""
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def squash(s):
    return re.sub(r"\s+", " ", s).lower()


def load_pages(txt):
    with open(txt, encoding="utf-8") as f:
        raw = f.read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    pages = {}
    for i in range(1, len(parts), 2):
        pages[int(parts[i])] = squash(parts[i + 1])
    return pages


def main(argv):
    txt = os.path.join(ROOT, "scratch", "frameworks", "GraphQL-Learn-Official.txt")
    checks = os.path.join(HERE, "citation-checks.json")
    if "--txt" in argv:
        txt = argv[argv.index("--txt") + 1]
    if "--checks" in argv:
        checks = argv[argv.index("--checks") + 1]
    if not os.path.isfile(txt):
        print(f"SKIP: source text not found ({txt}); use --txt PATH")
        return 0
    pages = load_pages(txt)
    if len(pages) != 6:
        print(f"WARNING: expected 6 pages, read {len(pages)}")
    with open(checks, encoding="utf-8") as f:
        data = json.load(f)
    fails = 0
    for c in data["positive"]:
        blob = " ".join(pages.get(p, "") for p in c["pages"])
        miss = [t for t in c["all"] if squash(t) not in blob]
        if miss:
            fails += 1
            print(f"FAIL {c['id']} p.{c['pages']}: missing {miss} :: {c['claim']}")
    alltext = " ".join(pages.values())
    for c in data["negative"]:
        found = [t for t in c["absent"] if squash(t) in alltext]
        if found:
            fails += 1
            print(f"FAIL {c['id']}: terms PRESENT in the source {found} :: {c['claim']}")
    np_, nn = len(data["positive"]), len(data["negative"])
    print(f"positive: {np_}, negative: {nn}, failures: {fails}")
    print("OK" if not fails else "WITH FAILURES")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
