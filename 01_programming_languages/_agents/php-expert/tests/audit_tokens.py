# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS in `backticks` against the cited page (PRW).

For each citation "(PRW p.N[-M][, ...])" in the package .md files (references/, agents/, tests/ optional via --also),
it takes the backtick terms from the preceding segment (since the previous citation on the same line) and checks that they appear
in the cited page(s) of the extracted text. Terms with spaces, placeholders, ellipses or very short ones are ignored.
If the term is not on the cited page but is on a neighboring page (+-1): NEAR; otherwise: FAIL.
Citations whose label is [inference]/[extrapolation] are not this auditor's concern (only literal "(PRW p." count).

Usage: python -I tests/audit_tokens.py --src PATH/prw.txt [--pkg ROOT] [--strict] [--verbose]
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
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
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


CITE = re.compile(r"\(PRW p\.([^)]+)\)")


def candidates(tok):
    t0 = tok.strip()
    if t0.startswith("[") or " " in t0 or "<" in t0 or "..." in t0 or "…" in t0 or "{" in t0:
        return []
    if t0.startswith(("scripts/", "references/", "python", "skills/", "tests/")) or t0.endswith((".py", ".md", ".json")):
        return []
    out = []
    for part in t0.split("|"):
        part = part.split("=")[0].rstrip("*").rstrip(".").rstrip("/")
        part = re.sub(r"\(\)$", "", part)
        part = part.lstrip("*.")
        if len(part) >= 4 and not re.fullmatch(r"[0-9.]+", part):
            out.append(part)
    return out


def audit(pkg, pages, files=None, verbose=False, strict=False):
    sq = {k: squash(norm(v)) for k, v in pages.items()}
    refs = os.path.join(pkg, "references")
    todo = []
    for fn in sorted(os.listdir(refs)):
        if fn.endswith(".md") and not fn.startswith("INDEX"):
            todo.append(os.path.join(refs, fn))
    for extra in (files or []):
        todo.append(os.path.join(pkg, extra))
    checked = near = fail = ncite = 0
    for path in todo:
        if not os.path.exists(path):
            continue
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            pos = 0
            for m in CITE.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                if line[pos:pos + 1] == "`":
                    pos += 1
                seg = re.sub(r"`\[[^\]`]*\]`", "", seg)
                plist = []
                for part in re.split(r";", m.group(1)):
                    plist += expand(re.sub(r"^p\.", "", part.strip()))
                if not plist:
                    continue
                ncite += 1
                for tok in re.findall(r"`([^`]+)`", seg):
                    for t in candidates(tok):
                        st = squash(norm(t)).strip(",.;")
                        checked += 1
                        if any(st in sq.get(p, "") for p in plist):
                            continue
                        nb = set()
                        for p in plist:
                            nb.update((p - 1, p + 1))
                        nb -= set(plist)
                        fn = os.path.basename(path)
                        if any(st in sq.get(p, "") for p in nb if p in sq):
                            near += 1
                            print(f"NEAR    {fn}:{ln}: `{t}` is not in p.{m.group(1)} but is on a neighboring page")
                        else:
                            fail += 1
                            print(f"FAIL    {fn}:{ln}: `{t}` not found in p.{m.group(1)}")
    print(f"Citations: {ncite}; terms checked: {checked}; near: {near}; failures: {fail}")
    return fail, near


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--also", nargs="*", default=["agents/php-expert.md"])
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    fail, near = audit(a.pkg, load_pages(a.src), a.also, a.verbose, a.strict)
    sys.exit(1 if (fail or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
