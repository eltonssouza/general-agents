# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of `backticked` TERMS against the cited page.

For each line of references/*.md (except INDEX) that contains the label [do livro] (or [from source]), take each
citation "(SIGLA p.N ...)" (SIGLA in JUNIT, MOCK, TDM, JMETER, SWE-G) and the backticked terms in the preceding
stretch (since the previous citation on the same line). Check that each term appears on the cited page(s) of the extracted text.
Terms with spaces, brackets, placeholders (<...>, ...), ellipses or that are too short are ignored. If the term
is not on the cited page but is on a neighboring page (+-1), it warns NEAR; otherwise, it FAILS.
Lines without [do livro]/[from source] (e.g. "no basis in v1" tables, [extrapolation]) are not audited by this script.
The references/ files may still carry the Portuguese label [do livro]; both spellings are accepted.

Usage: python -I tests/audit_tokens.py --src PATH/src [--pkg ROOT] [--strict] [-v]
  --src: directory with JUNIT.txt, MOCK.txt, TDM.txt, JMETER.txt, SWEG.txt (=== PAGE N === markers, N = PDF page)
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

FILES = {"JUNIT": "JUNIT.txt", "MOCK": "MOCK.txt", "TDM": "TDM.txt", "JMETER": "JMETER.txt", "SWE-G": "SWEG.txt"}
SOURCE_LABELS = ("[do livro]", "[from source]")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("\xa0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", "", s.lower())


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def parse_pages(group):
    pages = []
    for part in re.split(r"[;,]", group):
        m = re.match(r"\s*(?:p\.)?\s*(\d+)(?:\s*-\s*(\d+))?", part)
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
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in FILES.items()}
    refs = os.path.join(a.pkg, "references")
    cite = re.compile(r"\((JUNIT|MOCK|TDM|JMETER|SWE-G) p\.([^)]+)\)")
    checked = near = fail = ncites = 0
    for fn in sorted(os.listdir(refs)):
        if not fn.endswith(".md") or fn.startswith("INDEX"):
            continue
        for ln, line in enumerate(open(os.path.join(refs, fn), encoding="utf-8"), 1):
            if not any(lbl in line for lbl in SOURCE_LABELS):
                continue
            pos = 0
            for m in cite.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                src = m.group(1)
                plist = parse_pages(m.group(2))
                if not plist:
                    continue
                ncites += 1
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if (" " in t0 or "<" in t0 or "..." in t0 or "…" in t0 or "[" in t0
                            or t0.startswith(("scripts/", "references/", "python", "tests/"))
                            or "{" in t0):
                        continue
                    t = re.sub(r"\(\)$", "", t0.rstrip(".,;"))
                    if len(t) < 4 or re.fullmatch(r"[0-9.%/\-]+", t):
                        continue
                    st = norm(t)
                    checked += 1
                    if any(st in pages[src].get(p, "") for p in plist):
                        if a.verbose:
                            print(f"OK      {fn}:{ln}: `{t}` in {src} p.{m.group(2)}")
                        continue
                    nb = set()
                    for p in plist:
                        nb.update((p - 1, p + 1))
                    nb -= set(plist)
                    if any(st in pages[src].get(p, "") for p in nb):
                        near += 1
                        print(f"NEAR    {fn}:{ln}: `{t}` is not in {src} p.{m.group(2)} but is on a neighboring page")
                    else:
                        fail += 1
                        print(f"FAIL    {fn}:{ln}: `{t}` not found in {src} p.{m.group(2)}")
    print(f"Citations audited: {ncites}; terms checked: {checked}; near: {near}; failures: {fail}")
    sys.exit(1 if (fail or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
