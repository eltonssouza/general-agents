# -*- coding: utf-8 -*-
"""
audit_numbers.py - heuristic number audit: for each line of references/*.md that cites pages (p.N, p.N-M),
checks that the relevant numbers of the line (>= 2 digits or decimals) appear on the cited pages (or the neighbours +-1).
Lines marked [inference], [extrapolation] (or the Portuguese labels [inferência], [extrapolação]) or containing "script"/"script example" are ignored.

Usage: python -I tests/audit_numbers.py --src PATH/OSTEP-....txt [--pkg PACKAGE] [--verbose]
Output: list of numbers NOT found (for manual review) and counts. Always exit 0 (it is an audit, not a gate);
use --strict to exit 1 if there are unconfirmed numbers outside the exceptions list in tests/numeros-ok.txt.
"""
import argparse
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

LIG = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}


def norm(s):
    for a, b in LIG.items():
        s = s.replace(a, b)
    s = s.replace("−", "-")
    return re.sub(r"\s+", " ", s.lower())


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = set()
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.update(range(a, b + 1))
    return pages


def numbers(line):
    clean = re.sub(r"\bp\.\s*[\d\s,\-–]+", " ", line)  # remove page citations
    clean = re.sub(r"\b(?:cap|ch)\.\s*[\d\-–,]+", " ", clean)
    clean = re.sub(r"`[^`]*`", " ", clean)  # code
    clean = re.sub(r"\(Fig\.[^)]*\)|Eq\.[\d\.]+|Fig\.[\d\.]+", " ", clean)
    clean = re.sub(r"^\s*\d+\.\s", " ", clean)  # list numbering

    def _lista(m):
        partes = m.group(0).split(",")
        if len(partes) >= 3:  # sequences such as 1,2,3,4 or 10,20,30
            return " " + " ".join(partes) + " "
        return m.group(0)

    clean = re.sub(r"(?<![\w.,])\d{1,3}(?:,\d{1,3}){2,}(?![\w.,])", _lista, clean)
    # pairs "10,20" between 2-digit integers without a space: treated as a list
    clean = re.sub(r"(?<![\w.,])(\d{2}),(\d{2})(?![\w.,\d])", r" \1 \2 ", clean)
    out = []
    for m in re.finditer(r"(?<![\w.])(\d{1,3}(?:\.\d{3})+|\d+(?:[.,]\d+)?)(?![\w])", clean):
        tok = m.group(1)
        if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", tok):
            val = tok.replace(".", "")
            alts = {val, tok, tok.replace(".", ",")}
        else:
            val = tok.replace(",", ".")
            alts = {val, tok}
        digits = re.sub(r"\D", "", val)
        if len(digits) < 2:
            continue
        out.append((tok, alts))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    pages = load_pages(a.src)
    okfile = os.path.join(a.pkg, "tests", "numeros-ok.txt")
    allow = set()
    if os.path.exists(okfile):
        allow = {l.strip() for l in open(okfile, encoding="utf-8") if l.strip() and not l.startswith("#")}
    refdir = os.path.join(a.pkg, "references")
    total = confirmed = 0
    missing = []
    for fn in sorted(os.listdir(refdir)):
        if not fn.endswith(".md"):
            continue
        for ln, line in enumerate(open(os.path.join(refdir, fn), encoding="utf-8"), 1):
            if any(lab in line for lab in ("[inference]", "[extrapolation]", "[inferência]", "[extrapolação]")) or "script" in line.lower():
                continue
            cites = re.findall(r"\bp\.\s*(\d[\d\s,\-–]*)", line)
            if not cites:
                continue
            ps = set()
            for c in cites:
                ps |= expand(c)
            ps |= {p - 1 for p in ps} | {p + 1 for p in ps}
            body = " ".join(pages.get(p, "") for p in sorted(ps))
            for tok, alts in numbers(line):
                total += 1
                found = any(re.search(r"(?<![\d.,])" + re.escape(x) + r"(?![\d])", body) or x.replace(".", "") in body.replace(",", "").replace(".", "") if len(x) > 3 else re.search(r"(?<![\d.,])" + re.escape(x) + r"(?![\d])", body) for x in alts)
                key = f"{fn}:{tok}"
                if found or key in allow:
                    confirmed += 1
                else:
                    missing.append((fn, ln, tok, line.strip()[:140]))
    print(f"Numbers audited: {total}; confirmed on the cited pages (+-1): {confirmed}; not confirmed: {len(missing)}")
    for fn, ln, tok, txt in missing:
        print(f"  ? {fn}:{ln} number '{tok}' not found on the cited pages: {txt}")
    if a.strict and missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
