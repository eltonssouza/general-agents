# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of `backticked` TERMS against the pages cited on the same line.

For each line of references/*.md and agents/*.md that carries citations "(SICP|TAUP|CI p.N[-M][, p.K])", takes the
backticked terms of the line and checks whether they appear on ANY of the pages cited on the line (union, per book). Ignores labels
(`[from source]`, `[inference]`...), terms with spaces, placeholders, paths/files, commands and short terms (< 4
characters). If the term is not on the cited pages but is on a neighboring page (+-1), it warns as NEAR; if it is not even
close, FAIL. Function names with arguments (`f(x)`) are ignored.

Usage: python -I tests/audit_tokens.py --src FOLDER_WITH_sicp.txt_taup.txt_ci.txt [--pkg PACKAGE_ROOT] [--strict] [-v]
Exit 0 without FAIL (NEAR counts as a failure with --strict). Read-only, no network.
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

BOOKS = {"SICP": "sicp.txt", "TAUP": "taup.txt", "CI": "ci.txt"}
CITE = re.compile(
    r"(SICP|TAUP|CI)\s+p\.\s*(\d+)(?:\s*[-\u2013]\s*(\d+))?((?:\s*,\s*p\.\s*\d+(?:\s*[-\u2013]\s*\d+)?)*)")
EXTRA = re.compile(r"p\.\s*(\d+)(?:\s*[-\u2013]\s*(\d+))?")
# lines that declare inference/extrapolation/absence may carry terms that are NOT on the page (that is the point of the line)
DECLARA = re.compile(r"\[extrapola|\[infer|\*\*não\*\*|NÃO|não está|não aparece|não consta|não traz|não usa|não diz|"
                     r"\[extrapolation|\[inference|\*\*not\*\*|NOT|not in the|does not appear|is not in|"
                     r"does not (?:contain|use|say|bring|define|cover|mention)")


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\ufffd", "'").replace("\xa0", " ")
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"\s+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def line_cites(line):
    """{livro: set(paginas)} citadas na linha."""
    out = {}
    for m in CITE.finditer(line):
        b = m.group(1)
        a = int(m.group(2))
        z = int(m.group(3)) if m.group(3) else a
        s = out.setdefault(b, set())
        s.update(range(a, z + 1))
        for e in EXTRA.finditer(m.group(4) or ""):
            ea = int(e.group(1))
            ez = int(e.group(2)) if e.group(2) else ea
            s.update(range(ea, ez + 1))
    return out


def candidates(tok):
    t0 = tok.strip()
    if t0.startswith("["):  # epistemic labels
        return []
    if " " in t0 or "<" in t0 or "..." in t0 or "…" in t0 or "{" in t0:
        return []
    if t0.startswith(("scripts/", "references/", "python", "tests/", "http")) or t0.endswith((".py", ".md", ".json")):
        return []
    if "(" in t0 and not t0.endswith("()"):
        return []
    cands = []
    for part in t0.split("|"):
        part = part.split("=")[0].rstrip("*").rstrip(".").rstrip("/")
        part = re.sub(r"\(\)$", "", part).lstrip("*.")
        if len(part) >= 4 and not re.fullmatch(r"[0-9.]+", part):
            cands.append(part)
    return cands


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--dirs", default="references,agents")
    a = ap.parse_args()
    sq = {b: {k: squash(norm(v)) for k, v in load_pages(os.path.join(a.src, fn)).items()} for b, fn in BOOKS.items()}
    checked = near = fail = nlines = declared = 0
    for d in a.dirs.split(","):
        base = os.path.join(a.pkg, d)
        if not os.path.isdir(base):
            continue
        for fn in sorted(os.listdir(base)):
            if not fn.endswith(".md") or fn.startswith("INDEX"):
                continue
            for ln, line in enumerate(open(os.path.join(base, fn), encoding="utf-8"), 1):
                cites = line_cites(line)
                if not cites:
                    continue
                nlines += 1
                for tk in re.findall(r"`([^`]+)`", line):
                    for t in candidates(tk):
                        st = squash(norm(t)).strip(",.;")
                        checked += 1
                        ok = nb = False
                        for b, pset in cites.items():
                            if any(st in sq[b].get(p, "") for p in pset):
                                ok = True
                                break
                            around = {q for p in pset for q in (p - 1, p + 1)} - pset
                            if any(st in sq[b].get(p, "") for p in around):
                                nb = True
                        if ok:
                            if a.verbose:
                                print(f"OK      {d}/{fn}:{ln}: `{t}`")
                        elif DECLARA.search(line):
                            declared += 1
                            if a.verbose:
                                print(f"ABSENCE-DECLARED {d}/{fn}:{ln}: `{t}` (line labeled [inference]/[extrapolation]/NOT)")
                        elif nb:
                            near += 1
                            print(f"NEAR    {d}/{fn}:{ln}: `{t}` is not on the pages cited on the line, but is on a neighboring one")
                        else:
                            fail += 1
                            print(f"FAIL    {d}/{fn}:{ln}: `{t}` not found on the pages cited on the line {sorted(cites)}")
    print(f"Lines with citation: {nlines}; terms checked: {checked}; absences declared: {declared}; near: {near}; failures: {fail}")
    sys.exit(1 if (fail or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
