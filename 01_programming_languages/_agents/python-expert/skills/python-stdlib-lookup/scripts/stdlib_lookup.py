#!/usr/bin/env python3
"""Looks up the Python 3.14.0rc3 Standard Library index (PDF bookmarks).

Usage:
    python -I stdlib_lookup.py [--limit N] [--json] TERM [TERM ...]
    python -I stdlib_lookup.py --list-chapters

Searches the terms (case-insensitive) in chapter, module and section titles and returns the
most relevant modules with the PDF PAGES to read. It is only an index: it does NOT contain the
explanation of the modules. Read-only; no network. Source: stdlib_index.json, generated from the
bookmarks of "The Python Library Reference, Release 3.14.0rc3" (release candidate).
Exit code: 0 if it ran (even with no hits); 2 for a usage error.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(HERE, "stdlib_index.json"), encoding="utf-8") as fh:
        return json.load(fh)


def score(mod, chapter, terms):
    title = mod["title"].lower()
    ch = chapter["chapter"].lower()
    secs = [s["t"].lower() for s in mod["sections"]]
    total = 0
    hits = []
    for t in terms:
        s = 0
        if t in title:
            s += 6
            # exact module name (before the dash) is worth more
            if title.split(" — ")[0].strip() == t:
                s += 6
        if t in ch:
            s += 1
        sec_hits = [x for x in secs if t in x]
        if sec_hits:
            s += min(3 * len(sec_hits), 6)
            hits.extend(sec_hits[:3])
        if s == 0:
            return 0, []
        total += s
    return total, hits


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-chapters", action="store_true")
    a = ap.parse_args(argv)
    data = load()
    if a.list_chapters:
        for c in data:
            print(f"- {c['chapter']}: Lib p.{c['page']}-{c['end']} ({len(c['modules'])} modules/topics)")
        return 0
    if not a.terms:
        print("error: provide at least one term (e.g. pathlib, csv, 'json')", file=sys.stderr)
        return 2
    terms = [t.lower() for t in a.terms]
    found = []
    for c in data:
        # chapters without submodules (e.g. Built-in Functions)
        if not c["modules"] and all(t in c["chapter"].lower() for t in terms):
            found.append((10, dict(chapter=c["chapter"], module=c["chapter"], pages=[c["page"], c["end"]], sections=[])))
        for m in c["modules"]:
            sc, hits = score(m, c, terms)
            if sc:
                top_secs = [f"{s['t']} (p.{s['p']})" for s in m["sections"] if s["l"] == 3][:10]
                found.append((sc, dict(chapter=c["chapter"], module=m["title"], pages=[m["page"], m["end"]],
                                       sections=hits, top_sections=top_secs)))
    found.sort(key=lambda x: (-x[0], x[1]["pages"][0]))
    top = found[: a.limit]
    if a.json:
        json.dump([dict(score=s, **r) for s, r in top], sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    if not top:
        print(f"NOT COVERED: no module/section in the bookmarks matched {a.terms}. Try another term (in English) or use --list-chapters; do not invent pages.")
        print("Reminder: the index covers only what is in the PDF bookmarks.")
        return 0
    print(f"# {len(found)} result(s) for {a.terms} (showing {len(top)}) — PDF pages (Lib p.N)")
    for s, r in top:
        extra = f"  [matching sections: {'; '.join(r['sections'])}]" if r["sections"] else ""
        print(f"- {r['module']} — Lib p.{r['pages'][0]}-{r['pages'][1]} ({r['chapter']}){extra}")
        if r.get("top_sections"):
            print(f"    module sections (exact PDF page): {'; '.join(r['top_sections'])}")
    print("\nThe index only locates; read the indicated pages in the PDF to learn how to use the module. "
          "The documentation is from the 3.14.0rc3 release candidate.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
