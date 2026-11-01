# -*- coding: utf-8 -*-
"""
audit_numbers.py - heuristic audit: numbers (decimals, percentages, integers >= 100) written on a line of
references/*.md must appear in the pages cited ON THE SAME LINE (ISLR p.N / ESL p.N).

Usage: python -I tests/audit_numbers.py --src PATH/scratch/ai [--pkg ROOT]
It is only an alarm for review: numbers computed by the package or general knowledge show up as "not found".
Read-only, no network. Always exit 0 (report); use --strict for exit 1 if there are items.
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

FILES = {"ISLR": "ML-Intro-to-Statistical-Learning-ISLR.txt", "ESL": "ML-Elements-of-Statistical-Learning.txt"}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", s)
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            pages.extend(range(a, int(m.group(2) or a) + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in FILES.items()}
    cite_re = re.compile(r"\b(ISLR|ESL)\s+p{1,2}\.\s*(\d[\d\s,\-–]*)")
    num_re = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+(?![\d])|\d{1,3}(?:\.\d{3})+|\d+,\d+|\d+(?:\.\d+)?)(\s?%)?")
    miss = 0
    checked = 0
    refdir = os.path.join(a.pkg, "references")
    for fn in sorted(os.listdir(refdir)):
        if not fn.endswith(".md"):
            continue
        for ln, line in enumerate(open(os.path.join(refdir, fn), encoding="utf-8"), 1):
            cites = list(cite_re.finditer(line))
            if not cites:
                continue
            blob = {"ISLR": "", "ESL": ""}
            for m in cites:
                for p in expand(m.group(2)):
                    if p in pages[m.group(1)]:
                        blob[m.group(1)] += " " + pages[m.group(1)][p]
            allblob = blob["ISLR"] + " " + blob["ESL"]
            body = cite_re.sub(" ", line)
            body = re.sub(r"\(\d+\.\d+\)|\(\d+\)|\b\d+\.\d+-\d+\.\d+", " ", body)  # equation numbers
            for m in num_re.finditer(body):
                tok = m.group(1)
                pct = m.group(2)
                if re.fullmatch(r"\d{1,2}", tok) or tok in ("2013", "2017", "2009", "1995", "1957"):
                    continue
                cands = {tok.replace(",", ".")}
                if re.fullmatch(r"\d{1,3}(?:,\d{3})+", tok):  # English thousands separator
                    cands = {tok.replace(",", "."), tok.replace(",", ""), tok}
                if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", tok):
                    cands = {tok.replace(".", ","), tok.replace(".", "")}
                    cands |= {c for c in cands}
                if pct:
                    cands |= {tok.replace(",", ".") + "%", tok.replace(",", ".") + " %"}
                checked += 1
                if not any(c in allblob for c in cands):
                    miss += 1
                    print(f"? {fn}:{ln}: '{m.group(0).strip()}' not found in the cited pages -> {line.strip()[:110]}")
    print(f"Numbers checked: {checked}; not found in the pages cited on the same line: {miss} (review: they may be computed or from a neighboring line)")
    sys.exit(1 if (a.strict and miss) else 0)


if __name__ == "__main__":
    main()
