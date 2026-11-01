#!/usr/bin/env python3
"""Locates ECMA-262 sections (17th edition, ES2026) in the PDF: title, section number and PDF page.

Usage:
    python -I spec_lookup.py TERM [TERM ...]       # all terms must match in the title (case-insensitive)
    python -I spec_lookup.py --section 13.11       # section and direct subsections
    python -I spec_lookup.py --page 310            # sections that start at 310 and the section that covers it
    python -I spec_lookup.py --top                 # level-1 clauses

Read-only (loads spec_toc.json next to the script), no network. The page is the PDF page (not the printed one).
The index comes from the PDF bookmarks: it says WHERE to read, not what the section says. An empty
result means "no title has these terms", not "the feature does not exist": try another term or the
method name. Pages: a section title may appear at the end of the extracted text page.
Exit code: 0 if it ran; 2 for a usage error.
"""
import json
import os
import re
import sys


def load():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_toc.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def num(title):
    m = re.match(r"^(\d+(?:\.\d+)*|[A-F](?:\.\d+)*)\s", title)
    return m.group(1) if m else ""


def show(rows):
    for lvl, title, page in rows:
        print(f"p.{page:<4} {'  ' * (lvl - 1)}{title}")


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    toc = load()
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[0] == "--top":
        show([r for r in toc if r[0] == 1])
        return 0
    if argv[0] == "--section" and len(argv) == 2:
        s = argv[1]
        rows = [r for r in toc if num(r[1]) == s or num(r[1]).startswith(s + ".")]
        rows = [r for r in rows if num(r[1]).count(".") <= s.count(".") + 1]
        if not rows:
            print("Section not found in the index.")
            return 0
        show(rows)
        return 0
    if argv[0] == "--page" and len(argv) == 2 and argv[1].isdigit():
        n = int(argv[1])
        here = [r for r in toc if r[2] == n]
        before = [r for r in toc if r[2] <= n]
        cover = before[-1] if before else None
        if cover:
            print("Section in progress (the last one that started up to this page):")
            show([cover])
        if here:
            print("\nSections that start on this page:")
            show(here)
        return 0
    terms = [t.lower() for t in argv]
    rows = [r for r in toc if all(t in r[1].lower() for t in terms)]
    if not rows:
        print("No title with these terms. This does NOT prove that the feature does not exist in the Spec; try another term.")
        return 0
    print(f"# {len(rows)} section(s) (PDF pages)")
    show(rows[:80])
    if len(rows) > 80:
        print(f"... +{len(rows) - 80} (refine the terms)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
