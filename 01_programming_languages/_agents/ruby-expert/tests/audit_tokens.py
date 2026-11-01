# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of `backtick` TERMS against the cited page.

For each citation "(R3x p.N[-M]; R3y p.K)" in agents/*.md and references/*.md, takes the backticked terms from the text
preceding the citation (since the previous citation on the same line) and checks whether they appear on the cited page(s).
If they are not there but are on a neighboring page (+-1), it warns NEARBY; if not even close, FAIL.
Lines containing the [extrapolation] label (or the Portuguese [extrapolação]) are not checked (they declare precisely what is NOT in the notes).
Terms with spaces, placeholders, ellipses, 1 to 3 characters, or that are just numbers/file names are ignored.

Usage: python -I tests/audit_tokens.py --src FOLDER_WITH_TXT_FILES [--strict] [-v]
Exit 0 without FAIL (NEARBY counts as failure with --strict).
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = {"R30": "Ruby-3.0-Release-Notes", "R31": "Ruby-3.1-Release-Notes", "R32": "Ruby-3.2-Release-Notes",
       "R33": "Ruby-3.3-Release-Notes", "R34": "Ruby-3.4-Release-Notes"}


def squash(s):
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"').replace("\xa0", " ")
    return re.sub(r"\s+", "", s.lower())


def load(src):
    books = {}
    for sig, name in REL.items():
        raw = open(os.path.join(src, name + ".txt"), encoding="utf-8").read()
        parts = re.split(r"=== PAGE (\d+) ===", raw)
        books[sig] = {int(parts[i]): squash(parts[i + 1]) for i in range(1, len(parts), 2)}
    return books


def expand(spec):
    out = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", tok)
        if m:
            out += list(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1))
    return out


CITE = re.compile(r"\((R3[0-4] p\.[\d,\s\-]+(?:;\s*R3[0-4] p\.[\d,\s\-]+)*)\)")
SKIP_PREFIX = ("scripts/", "references/", "skills/", "python", "tests/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    books = load(a.src)
    checked = near = fail = 0
    files = [os.path.join(ROOT, "agents", f) for f in os.listdir(os.path.join(ROOT, "agents"))]
    files += [os.path.join(ROOT, "references", f) for f in os.listdir(os.path.join(ROOT, "references"))
              if not f.startswith("INDEX")]
    for fp in sorted(files):
        if not fp.endswith(".md"):
            continue
        for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
            if any(x in line for x in ("[extrapolação]", "extrapolação]`", "[extrapolation]", "extrapolation]`")):
                continue
            pos = 0
            for m in CITE.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                spans = []
                for part in m.group(1).split(";"):
                    mm = re.match(r"\s*(R3[0-4]) p\.(.*)", part)
                    if mm:
                        spans.append((mm.group(1), expand(mm.group(2))))
                if not spans:
                    continue
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if (" " in t0 or "<" in t0 or "..." in t0 or t0.startswith(SKIP_PREFIX) or len(t0) <= 3
                            or t0.endswith((".md", ".py", ".json", ".rb", ".pdf")) or re.fullmatch(r"[\d.,%\-x ]+", t0)
                            or t0.startswith("[") or t0.startswith("(R")):
                        continue
                    cands = [p.strip() for p in t0.split("|")]
                    for t in cands:
                        t = re.sub(r"\(\)$", "", t.rstrip(",.;:"))
                        st = squash(t)
                        if len(st) <= 3:
                            continue
                        checked += 1
                        if any(st in books[r].get(p, "") for r, pl in spans for p in pl):
                            continue
                        nb = set()
                        for r, pl in spans:
                            for p in pl:
                                nb.update((r, q) for q in (p - 1, p + 1))
                        nb -= {(r, p) for r, pl in spans for p in pl}
                        if any(st in books[r].get(p, "") for r, p in nb):
                            near += 1
                            print("NEARBY %s:%d: `%s` is not in %s but is on a neighboring page" % (os.path.basename(fp), ln, t, m.group(1)))
                        else:
                            fail += 1
                            print("FAIL   %s:%d: `%s` not found in %s" % (os.path.basename(fp), ln, t, m.group(1)))
    print("Terms checked: %d; nearby: %d; failures: %d" % (checked, near, fail))
    return 1 if (fail or (a.strict and near)) else 0


if __name__ == "__main__":
    sys.exit(main())
