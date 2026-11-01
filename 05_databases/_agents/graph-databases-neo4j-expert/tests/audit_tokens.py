# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS in `backticks` against the cited page(s).

For each "(NEO4J p.N...)" citation in the package files, it takes the backtick terms in the preceding text (since the previous
citation on the same line) and checks whether they appear on the cited page(s) of the extracted text. Terms with spaces, placeholders
({...}, <...>, ...), file/script names and short terms are ignored. If the term is not on the cited page but is on a
neighboring page (+-1), it reports NEARBY; if it is not even close, FAIL.

Usage (from the package root):
  python -I tests/audit_tokens.py --text NEO4J.txt [--pkg ROOT] [--strict]
Exit 0 if there is no FAIL (NEARBY counts as a failure with --strict). Read-only, no network.
"""
import argparse
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‐ ", "").replace("‐\n", "").replace("‐", "-").replace("‑", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", "", s.lower())


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*[,;]\s*", spec.strip()):
        m = re.search(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


SKIP_PREFIX = ("scripts/", "references/", "tests/", "python", "agents/", ".github")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    sq = load_pages(a.text)
    files = []
    refs = os.path.join(a.pkg, "references")
    for fn in sorted(os.listdir(refs)):
        if fn.endswith(".md") and not fn.startswith("INDEX"):
            files.append(os.path.join(refs, fn))
    for sub in (os.path.join("agents"), ):
        d = os.path.join(a.pkg, sub)
        if os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".md")]
    files.append(os.path.join(a.pkg, "AGENTS.md"))
    cite = re.compile(r"\(NEO4J p\.([^)]+)\)")
    checked = near = fail = 0
    for path in files:
        if not os.path.exists(path):
            continue
        fn = os.path.relpath(path, a.pkg)
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            pos = 0
            for m in cite.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                plist = expand(m.group(1))
                if not plist:
                    continue
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if " " in t0 or "<" in t0 or "{" in t0 or "..." in t0 or t0.startswith(SKIP_PREFIX):
                        continue
                    if t0.endswith((".md", ".py", ".json")) or t0.startswith(("NEO4J", "NEO_START", "[")):
                        continue
                    cands = []
                    for part in t0.split("|"):
                        part = part.split("=")[0].rstrip("*").rstrip(".").rstrip("/")
                        part = re.sub(r"\(\)$", "", part)
                        if len(part) >= 4 and not re.fullmatch(r"[0-9.]+", part):
                            cands.append(part)
                    for t in cands:
                        st = norm(t).strip(",.;")
                        checked += 1
                        if any(st in sq.get(p, "") for p in plist):
                            continue
                        nb = set()
                        for p in plist:
                            nb.update((p - 1, p + 1))
                        nb -= set(plist)
                        if any(st in sq.get(p, "") for p in nb if p in sq):
                            near += 1
                            print("NEARBY %s:%d: `%s` is not on p.%s but is on a neighboring page" % (fn, ln, t, m.group(1)))
                        else:
                            fail += 1
                            print("FAIL   %s:%d: `%s` not found on p.%s" % (fn, ln, t, m.group(1)))
    print("Terms checked: %d; nearby: %d; failures: %d" % (checked, near, fail))
    return 1 if (fail or (a.strict and near)) else 0


if __name__ == "__main__":
    sys.exit(main())
