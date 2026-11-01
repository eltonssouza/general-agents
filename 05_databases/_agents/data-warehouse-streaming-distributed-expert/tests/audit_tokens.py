# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of `backticked` TERMS against the cited page (adapted from the Spring Boot package).

For each citation "(KIMBALL p.N...)" or "(STREAM p.N...)" in references/*.md, takes the backticked terms of the stretch
that precedes it (since the previous citation on the same line) and checks that they appear in the cited pages of the extracted text.
Ignores: terms with spaces, with '_' or '(', numeric, too short, and stretches labeled [extrapolation]/[inference]
(those may deliberately mention terms the source does not have; the Portuguese labels [extrapolação]/[inferência]
of the still-untranslated references are also recognized). If the term is not on the cited page but is on a
neighboring one (+-1), it warns NEAR; if it is not nearby, FAIL.

Usage: python -I tests/audit_tokens.py --kimball KIMBALL.txt --stream STREAM.txt [--pkg ROOT] [--strict]
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
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"[\s\-]+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): squash(norm(parts[i + 1])) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        tok = re.sub(r"^p\.", "", tok.strip())
        m = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kimball", required=True)
    ap.add_argument("--stream", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    srcs = {"KIMBALL": load_pages(a.kimball), "STREAM": load_pages(a.stream)}
    refs = os.path.join(a.pkg, "references")
    checked = near = fail = 0
    cite = re.compile(r"\((KIMBALL|STREAM) p\.([^)]+)\)")
    for fn in sorted(os.listdir(refs)):
        if not fn.endswith(".md") or fn.startswith("INDEX") or fn.startswith("pat-helland"):
            continue
        for ln, line in enumerate(open(os.path.join(refs, fn), encoding="utf-8"), 1):
            pos = 0
            for m in cite.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                if any(lbl in seg for lbl in ("[extrapolation]", "[inference]", "[extrapolação]", "[inferência]")):
                    continue
                sig = m.group(1)
                plist = []
                for part in m.group(2).split(";"):
                    plist += expand(part)
                if not plist:
                    continue
                sq = srcs[sig]
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if " " in t0 or "_" in t0 or "(" in t0 or "..." in t0 or len(t0) < 4 or re.fullmatch(r"[0-9.,\-]+", t0):
                        continue
                    st = squash(norm(t0)).strip(",.;")
                    checked += 1
                    if any(st in sq.get(p, "") for p in plist):
                        continue
                    nb = set()
                    for p in plist:
                        nb.update((p - 1, p + 1))
                    nb -= set(plist)
                    if any(st in sq.get(p, "") for p in nb if p in sq):
                        near += 1
                        print("NEAR %s:%d: `%s` is not in %s p.%s but is on a neighboring page" % (fn, ln, t0, sig, m.group(2)))
                    else:
                        fail += 1
                        print("FAIL %s:%d: `%s` not found in %s p.%s" % (fn, ln, t0, sig, m.group(2)))
    print("Terms checked: %d; near: %d; failures: %d" % (checked, near, fail))
    return 1 if (fail or (a.strict and near)) else 0


if __name__ == "__main__":
    sys.exit(main())
