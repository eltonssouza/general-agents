# -*- coding: utf-8 -*-
"""
verify_citations.py - audits the package citations against the text extracted from the PDF (RUN).

Usage:
  python -I tests/verify_citations.py --src PATH/scratch/devops [--pkg PACKAGE_PATH]

1) Range: every citation `RUN p.N[-M][, ...]` must exist (1-204); citations to the back-of-book
   index (189-204) produce a WARNING (the index is not a source of claims).
2) Content: each "checks" item requires the cited PDF page to contain the substrings
   (lowercase comparison, ignoring spaces and hyphens/hyphenation line breaks).
3) Negatives: "negative" items require terms that are ABSENT (from the whole book or from the page).
4) Flags: every `--flag` cited in references/, agents/, AGENTS.md and README.md must exist in the
   book OR appear in "allowed_absent_flags" (flags listed on purpose as "not in the book").
Read-only, no network. Exit 0 if everything passes, 1 otherwise.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FILE = "Serverless-Google-Cloud-Run.txt"
MAXP = 204
INDEX_FROM = 189


def squash(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[\s\-‐-―]+", "", s.lower())


def norm_flag(s):
    s = re.sub(r"[‐-―]", "-", s.lower())
    return re.sub(r"\s+", " ", s)


def has(term, body_squash, body_raw):
    """terms starting with '-' (flags) require a literal match with hyphens; others are compared ignoring spaces/hyphens."""
    if term.lstrip().startswith("-"):
        return norm_flag(term) in body_raw
    return squash(term) in body_squash


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = set()
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.update(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    pages = load_pages(os.path.join(a.src, FILE))
    if len(pages) != MAXP:
        print(f"WARNING: the text has {len(pages)} pages (expected {MAXP})")
    fails = 0
    book_all = squash(" ".join(pages.values()))
    book_raw = norm_flag(" ".join(pages.values()))

    cite_re = re.compile(r"\bRUN\s+p\.\s*(\d[\d\s,\-–]*)")
    total, seen, idx_cites = 0, set(), 0
    for root, _, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith((".md", ".json", ".py")) or fn in ("verify_citations.py", "citation-checks.json"):
                continue
            fp = os.path.join(root, fn)
            text = open(fp, "r", encoding="utf-8", errors="replace").read()
            for m in cite_re.finditer(text):
                for p in expand(m.group(1)):
                    total += 1
                    seen.add(p)
                    if p < 1 or p > MAXP:
                        fails += 1
                        print(f"FAIL range: RUN p.{p} out of range in {os.path.relpath(fp, a.pkg)}")
                    elif p >= INDEX_FROM:
                        idx_cites += 1
                        print(f"WARNING: RUN p.{p} is from the back-of-book index ({os.path.relpath(fp, a.pkg)})")
    print(f"Range: {total} page numbers checked; {len(seen)} distinct pages (min {min(seen) if seen else '-'}, max {max(seen) if seen else '-'}); {idx_cites} in the index")

    data = json.load(open(os.path.join(a.pkg, "tests", "citation-checks.json"), encoding="utf-8"))
    ok = 0
    for c in data["checks"]:
        m = re.fullmatch(r"RUN p\.(\d+)", c["cite"])
        raw = pages.get(int(m.group(1)), "")
        body, rawn = squash(raw), norm_flag(raw)
        miss = [s for s in c["contains"] if not has(s, body, rawn)]
        if miss:
            fails += 1
            print(f"FAIL content: {c['cite']} ({c['claim']}) does not contain {miss}")
        else:
            ok += 1
    print(f"Content: {ok}/{len(data['checks'])} positive checks OK")

    nok = 0
    for n in data["negative"]:
        if "src" in n:
            bodies = {"ALL": (book_all, book_raw)}
            where = "ALL"
        else:
            m = re.fullmatch(r"RUN p\.(\d+)", n["cite"])
            raw = pages.get(int(m.group(1)), "")
            bodies = {n["cite"]: (squash(raw), norm_flag(raw))}
            where = n["cite"]
        present = [t for t in n["absent"] for b in bodies.values() if has(t, b[0], b[1])]
        if present:
            fails += 1
            print(f"FAIL negative: {where} ({n['claim']}) CONTAINS {sorted(set(present))}")
        else:
            nok += 1
    print(f"Negatives: {nok}/{len(data['negative'])} OK (terms absent as expected)")

    allowed = set(data.get("allowed_absent_flags", []))
    flag_re = re.compile(r"(?<![\w-])(--[a-z][a-z0-9]*(?:-[a-z0-9]+)*)")
    bad_flags, checked = {}, 0
    for sub in ("references", "agents", ".github"):
        for root, _, files in os.walk(os.path.join(a.pkg, sub)):
            for fn in files:
                if fn.endswith(".md"):
                    fp = os.path.join(root, fn)
                    for fl in flag_re.findall(open(fp, "r", encoding="utf-8", errors="replace").read()):
                        checked += 1
                        if fl in allowed:
                            continue
                        if norm_flag(fl) not in book_raw:
                            bad_flags.setdefault(fl, set()).add(os.path.relpath(fp, a.pkg))
    for fn in ("AGENTS.md", "README.md"):
        fp = os.path.join(a.pkg, fn)
        if os.path.exists(fp):
            for fl in flag_re.findall(open(fp, "r", encoding="utf-8", errors="replace").read()):
                checked += 1
                if fl not in allowed and norm_flag(fl) not in book_raw:
                    bad_flags.setdefault(fl, set()).add(fn)
    for fl, files in sorted(bad_flags.items()):
        fails += 1
        print(f"FAIL flag: {fl} cited in {sorted(files)} but absent from the book and not listed in allowed_absent_flags")
    print(f"Flags: {checked} occurrences checked; {len(bad_flags)} unjustified flags")
    print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
