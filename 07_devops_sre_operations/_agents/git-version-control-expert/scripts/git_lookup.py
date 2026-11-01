# -*- coding: utf-8 -*-
"""
git_lookup.py - deterministic lookup in the git_index.json index (read-only, no network).

Usage:
  python -I git_lookup.py rebase                # topic by key, alias or text search
  python -I git_lookup.py "reset --hard"        # command/option term
  python -I git_lookup.py --list                # list all topics
  python -I git_lookup.py bisect --json         # JSON output

Terms may be given in English or Portuguese (aliases are bilingual; accents are ignored).

Each answer carries pages (PGEN = Pro Git EN; PGBR = Pro Git PT-BR; PDF page), a summary,
risks, what is [DATED] and what the book does NOT say. If nothing is found, it prints "NOT COVERED"
(it does not invent a page). Terms the book provably does NOT contain (checked against the extracted
text in tests/verify_citations.py) are listed as NOT IN THE SOURCE.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Terms checked as ABSENT from PGEN (and PGBR when indicated) by tests/citation-checks.json
ABSENT = {
    "force-with-lease": "PGEN and PGBR: only --force/-f (PGEN p.107, PGBR p.98); --force-with-lease is [extrapolation]",
    "sha-256": "PGEN: only SHA-1; 'SHA256' appears once, in a note (PGEN p.226: Git is moving to SHA256); PGBR: no mention [DATED]",
    "sha256": "PGEN: only SHA-1; 'SHA256' appears once, in a note (PGEN p.226: Git is moving to SHA256); PGBR: no mention [DATED]",
    "object-format": "PGEN: does not appear (SHA-256 repos are not taught)",
    "autosquash": "PGEN: rebase --autosquash does not appear",
    "--fixup": "PGEN: commit --fixup does not appear",
    "git flow": "PGEN: git-flow is not covered",
    "gitflow": "PGEN: git-flow is not covered",
    "conventional commits": "PGEN: does not appear",
    "github actions": "PGEN: does not appear",
    "git lfs": "PGEN: Git LFS does not appear",
    "lfs": "PGEN: Git LFS does not appear",
    "partial clone": "PGEN: does not appear",
    "--depth": "PGEN: shallow clone (--depth) does not appear",
    "shallow": "PGEN: shallow clone is not taught (only 'shallow' in the git-p4 context)",
    "reflog expire": "PGEN: does not appear",
    "--no-ff": "PGEN: merge --no-ff does not appear",
    "--ff-only": "PGEN: merge --ff-only does not appear",
    "reset --keep": "PGEN: does not appear",
    "restore --source": "PGEN: does not appear",
    "orig_head": "PGEN: ORIG_HEAD does not appear",
    "git maintenance": "PGEN: does not appear",
    "commit-graph": "PGEN: does not appear",
    "codeowners": "PGEN: does not appear",
    "branch protection": "PGEN: branch protection does not appear",
    "protected branch": "PGEN: branch protection does not appear",
    "gerrit": "PGEN: does not appear",
    "bisect skip": "PGEN: does not appear",
    "dependabot": "PGEN: does not appear",
    "git absorb": "PGEN: does not appear",
    "trunk-based": "PGEN: 'trunk' only appears in the Subversion context (git svn)",
    "git worktree": "PGEN: the git worktree command does not appear (only GIT_WORK_TREE/--work-tree in environment variables, PGEN p.453)",
    "gitops": "outside the collection (not a topic of the book)",
}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def load_index():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "git_index.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def score(term, key, t):
    q = norm(term)
    if not q:
        return 0
    if q == norm(key):
        return 100
    best = 0
    for a in t.get("aliases", []):
        na = norm(a)
        if q == na:
            best = max(best, 90)
        elif q in na or (len(na) > 3 and re.search(r"(?<![a-z0-9])" + re.escape(na) + r"(?![a-z0-9])", q)):
            best = max(best, 60)
    if q in norm(t["name"]):
        best = max(best, 50)
    if q in norm(t.get("summary", "")):
        best = max(best, 30)
    toks = [x for x in q.replace("-", " ").split() if len(x) > 2]
    if toks and best == 0:
        hit = sum(1 for x in toks if x in norm(" ".join(t.get("aliases", [])) + " " + t["name"] + " " + t.get("summary", "")))
        if hit == len(toks):
            best = 20
    return best


def show(key, t):
    print(f"TOPIC: {t['name']} [{key}]")
    print(f"CITATION: [from source] (PGEN p.{t['pgen']})  |  PT-BR: (PGBR p.{t['pgbr']})")
    print(f"REFERENCE: references/{t['ref']}")
    print("\nSUMMARY:\n  " + t["summary"])
    if t.get("mechanisms"):
        print("\nMECHANISMS/POINTS:")
        for m in t["mechanisms"]:
            print("  * " + m)
    if t.get("risks"):
        print("\nRISKS (from the source):")
        for m in t["risks"]:
            print("  ! " + m)
    if t.get("dated"):
        print("\n[DATED]:")
        for m in t["dated"]:
            print("  - " + m)
    if t.get("gaps"):
        print("\nTHE BOOK DOES NOT SAY (treat as [extrapolation] if asked):")
        for m in t["gaps"]:
            print("  - " + m)


def main():
    ap = argparse.ArgumentParser(description="Lookup in the Pro Git index (PGEN/PGBR).")
    ap.add_argument("term", nargs="*", help="term, command or topic (English or Portuguese)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    idx = load_index()
    topics = idx["topics"]
    if a.list:
        for k, t in topics.items():
            print(f"{k:34s} PGEN p.{t['pgen']:<18s} {t['name']}")
        return 0
    term = " ".join(a.term).strip()
    if not term:
        ap.print_help()
        return 2
    nt = norm(term)
    absent = [(k, v) for k, v in ABSENT.items() if k == nt or (len(k) > 4 and k in nt)]
    ranked = sorted(((score(term, k, t), k) for k, t in topics.items()), reverse=True)
    ranked = [(s, k) for s, k in ranked if s > 0][:3]
    if a.json:
        print(json.dumps({"term": term, "absent": [{"term": k, "note": v} for k, v in absent],
                          "matches": [{"key": k, "score": s, **topics[k]} for s, k in ranked]}, ensure_ascii=False, indent=2))
        return 0 if (ranked or absent) else 1
    if absent:
        for k, v in absent:
            print(f"NOT IN THE SOURCE: '{k}' -> {v}")
        print()
    if not ranked:
        if not absent:
            print(f"NOT COVERED: '{term}' is not in the collection index (Pro Git). Do not cite a page; "
                  "if you answer, mark it [extrapolation] and recommend checking the current Git documentation.")
            return 1
        return 0
    for i, (s, k) in enumerate(ranked):
        if i:
            print("\n" + "-" * 60 + "\n")
        show(k, topics[k])
    return 0


if __name__ == "__main__":
    sys.exit(main())
