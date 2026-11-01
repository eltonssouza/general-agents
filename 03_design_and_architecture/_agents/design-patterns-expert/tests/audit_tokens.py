# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of `backticked` TERMS against the cited page.

For each citation "(SIGLA p.N[-M][, K][; SIGLA2 p.X])" in references/*.md, takes the backticked terms from the preceding
stretch (since the previous citation on the same line) and checks whether they appear on the cited page(s) of the text extracted
from the corresponding source. Terms with labels ([...]), paths, commands, placeholders or very short ones are ignored. If the
term is not on the cited page but is on a neighboring page (+-1), it is reported as NEAR; if it is not even close, FAIL.

Usage: python -I tests/audit_tokens.py --src PATH/src [--pkg PACKAGE_ROOT] [--strict] [-v]
  --src: directory with RG.txt, GPP.txt, CC.txt, PEAA.txt (=== PAGE N === markers)
Exit 0 without FAIL (NEAR counts as a failure with --strict).
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

SIGLAS = ("RG", "GPP", "CC", "PEAA")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("\xa0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).lower().strip()


def squash(s):
    return re.sub(r"[\s\-]+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): squash(norm(parts[i + 1])) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


CITE = re.compile(r"\(((?:RG|GPP|CC|PEAA) p\.[^)]*)\)")
PART = re.compile(r"(RG|GPP|CC|PEAA) p\.\s*([0-9,\s\-–]+)")


def candidates(tok):
    t = tok.strip()
    if not t or t.startswith(("[", "scripts/", "references/", "python", "--", "tests/", "agents/")):
        return []
    if "<" in t or "..." in t or "…" in t or "/" in t or "=" in t or "|" in t or "{" in t:
        return []
    t = re.sub(r"\(\)$", "", t).rstrip(".,;:*")
    t = re.sub(r"^\*+", "", t)
    if t.lower().endswith((".md", ".pdf", ".py", ".json", ".txt")):
        return []
    if len(t) < 4 or re.fullmatch(r"[0-9.,%x\s]+", t):
        return []
    if len(t.split()) > 4:
        return []
    return [t]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    books = {s: load_pages(os.path.join(a.src, s + ".txt")) for s in SIGLAS}
    refs = os.path.join(a.pkg, "references")
    checked = near = fail = 0
    for fn in sorted(os.listdir(refs)):
        if not fn.endswith(".md") or fn.startswith("INDEX"):
            continue
        for ln, line in enumerate(open(os.path.join(refs, fn), encoding="utf-8"), 1):
            pos = 0
            for m in CITE.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                # the citation is inside a code span `[from source] (SIGLA p.N)`: strip the closing backtick of the previous
                # stretch and the opening label of the current one, so the backtick pairs stay aligned
                seg = re.sub(r"^\s*`", "", seg)
                seg = re.sub(r"`\[[^`\]]*\]\s*$", "", seg)
                targets = []  # (sigla, [pages])
                for pm in PART.finditer(m.group(1)):
                    targets.append((pm.group(1), expand(pm.group(2))))
                if not targets:
                    continue
                for tok in re.findall(r"`([^`]+)`", seg):
                    for t in candidates(tok):
                        st = squash(norm(t)).strip(",.;")
                        checked += 1
                        found = any(st in books[s].get(p, "") for s, pl in targets for p in pl)
                        if found:
                            continue
                        nb = [(s, p) for s, pl in targets for p in pl for p in (p - 1, p + 1)]
                        if any(st in books[s].get(p, "") for s, p in nb):
                            near += 1
                            print("NEAR    %s:%d: `%s` is not on %s but is on a neighboring page" % (fn, ln, t, m.group(1)))
                        else:
                            fail += 1
                            print("FAIL    %s:%d: `%s` not found in %s" % (fn, ln, t, m.group(1)))
    print("Terms checked: %d; near: %d; failures: %d" % (checked, near, fail))
    # page range: all citations in all the package's .md files
    ncite = nbad = 0
    for root, _dirs, files in os.walk(a.pkg):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            for ln, line in enumerate(open(path, encoding="utf-8"), 1):
                for m in CITE.finditer(line):
                    for pm in PART.finditer(m.group(1)):
                        sg = pm.group(1)
                        for tok in re.split(r"\s*,\s*", pm.group(2).strip()):
                            mm = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
                            if not mm:
                                continue
                            lo, hi = int(mm.group(1)), int(mm.group(2) or mm.group(1))
                            ncite += 1
                            if lo < 1 or hi < lo or hi > max(books[sg]):
                                nbad += 1
                                print("RANGE   %s:%d: (%s p.%s) outside the range 1-%d" % (os.path.relpath(path, a.pkg), ln, sg, tok, max(books[sg])))
    print("Page citations checked (range): %d; out of range: %d" % (ncite, nbad))
    sys.exit(1 if (fail or nbad or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
