# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS in `backticks` against the cited page.

For each citation "(SBR p.N...)" in references/*.md, it takes the terms in backticks from the preceding stretch (since the
previous citation on the same line) and checks whether they appear on the cited page(s) of the extracted text. Terms with spaces,
placeholders (<...>, ...), ellipses or very short ones are ignored. If the term is not on the cited page but is on a
neighboring page (±1), it warns as NEAR; if it is not even close, FAIL.

Usage: python -I tests/audit_tokens.py --src PATH/scratch/frameworks [--pkg ROOT] [--strict]
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


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("�", "'").replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"\s+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    pages = load_pages(os.path.join(a.src, "Spring-Boot-Reference.txt"))
    sq = {k: squash(norm(v)) for k, v in pages.items()}
    refs = os.path.join(a.pkg, "references")
    checked = near = fail = 0
    cite = re.compile(r"\(SBR p\.([^)]+)\)")
    for fn in sorted(os.listdir(refs)):
        if not fn.endswith(".md") or fn.startswith("INDEX") or fn.startswith("glossario"):
            continue
        for ln, line in enumerate(open(os.path.join(refs, fn), encoding="utf-8"), 1):
            pos = 0
            for m in cite.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                plist = []
                for part in re.split(r"[;]", m.group(1)):
                    plist += expand(re.sub(r"^p\.", "", part.strip()))
                if not plist:
                    continue
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if " " in t0 or "<" in t0 or "..." in t0 or "…" in t0 or t0.startswith(("scripts/", "references/", "python")):
                        continue
                    if "{" in t0:
                        continue
                    cands = []
                    # a|b|c -> parts; common prefix (before the 1st '|') only if there is a dot
                    parts = t0.split("|")
                    for i, part in enumerate(parts):
                        part = part.split("=")[0].rstrip("*").rstrip(".").rstrip("/")
                        part = re.sub(r"\(\)$", "", part)
                        if part.startswith("*") or part.startswith("."):
                            part = part.lstrip("*.")
                        if len(part) >= 4 and not re.fullmatch(r"[0-9.]+", part):
                            cands.append(part)
                    for t in cands:
                        st = squash(norm(t)).strip(",.;")
                        checked += 1
                        if any(st in sq.get(p, "") for p in plist):
                            continue
                        nb = set()
                        for p in plist:
                            nb.update((p - 1, p + 1))
                        nb -= set(plist)
                        if any(st in sq.get(p, "") for p in nb if p in sq):
                            near += 1
                            print(f"NEAR {fn}:{ln}: `{t}` is not on p.{m.group(1)} but is on a neighboring page")
                        else:
                            fail += 1
                            print(f"FAIL   {fn}:{ln}: `{t}` not found on p.{m.group(1)}")
    print(f"Terms checked: {checked}; near: {near}; failures: {fail}")
    sys.exit(1 if (fail or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
