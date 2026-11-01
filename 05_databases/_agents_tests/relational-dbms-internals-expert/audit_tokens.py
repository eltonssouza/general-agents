# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS between `backticks` against the cited page (adapted from audit_tokens.py
of the spring-boot-reference-expert package).

For each citation "SIGLA p.N[-M][, p.X]" in references/*.md (except INDEX and glossario), it takes the terms between backticks from the
preceding excerpt (since the previous citation on the same line; adjacent citations separated by ';' or ',' form a group and the terms
are searched on the pages of ALL the siglas of the group) and checks that they appear on the cited page(s). If the term is not
on the cited page but is on a neighboring page (+-1), it warns NEARBY (recorded, informational tolerance only); if it is not
even close, FAIL. Terms with spaces, placeholders, file/script names and very short ones are ignored.

Usage: python -I tests/audit_tokens.py --src <folder with the extracted .txt files> [--pkg ROOT] [--strict] [-v]
Exit 0 without FAIL (with --strict, NEARBY also fails). No network; read-only.
"""
import argparse
import os
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_citations import FILES, CITE_RE, EXTRA_RE, load_pages  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), (" ", " ")):
        s = s.replace(a, b)
    return s.lower()


def squash(s):
    return re.sub(r"[\s\-]+", "", s)


def pages_of(m):
    specs = [(m.group(2), m.group(3))] + EXTRA_RE.findall(m.group(4) or "")
    out = []
    for a, b in specs:
        out.extend(range(int(a), int(b or a) + 1))
    return m.group(1), out


def candidates(tok):
    t0 = tok.strip()
    if (" " in t0 or "<" in t0 or "..." in t0 or t0.startswith(("scripts/", "references/", "python", "tests/", "--"))
            or "{" in t0 or "[" in t0 or t0.endswith((".md", ".py", ".json", ".txt"))):
        return []
    out = []
    for part in t0.split("|"):
        part = part.split("=")[0].rstrip(".*/")
        part = re.sub(r"\(\)$", "", part)
        part = part.lstrip("*.")
        if len(part) >= 4 and not re.fullmatch(r"[0-9.,%/:-]+", part):
            out.append(part)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    sq = {}
    for sig, fn in FILES.items():
        pg = load_pages(os.path.join(a.src, fn))
        sq[sig] = {k: squash(norm(v)) for k, v in pg.items()}
    refs = os.path.join(a.pkg, "references")
    checked = near = fail = 0
    for fn in sorted(os.listdir(refs)):
        if not fn.endswith(".md") or fn.startswith(("INDEX", "glossario")):
            continue
        for ln, line in enumerate(open(os.path.join(refs, fn), encoding="utf-8"), 1):
            ms = list(CITE_RE.finditer(line))
            groups = []
            for m in ms:
                if groups and re.fullmatch(r"[\s;,)(]*", line[groups[-1][-1].end():m.start()]):
                    groups[-1].append(m)
                else:
                    groups.append([m])
            prev_end = 0
            for g in groups:
                seg = line[prev_end:g[0].start()]
                prev_end = g[-1].end()
                cites = [pages_of(m) for m in g]
                label = "; ".join("%s p.%s" % (s, ",".join(map(str, p[:3])) + ("..." if len(p) > 3 else "")) for s, p in cites)
                for tok in re.findall(r"`([^`]+)`", seg):
                    for t in candidates(tok):
                        st = squash(norm(t)).strip(",.;")
                        checked += 1
                        if any(st in sq[s].get(p, "") for s, ps in cites for p in ps):
                            if a.verbose:
                                print("OK      %s:%d `%s` in %s" % (fn, ln, t, label))
                            continue
                        nb = set()
                        for s, ps in cites:
                            for p in ps:
                                for d in (-1, 1):
                                    if (p + d) in sq[s] and (p + d) not in ps:
                                        nb.add((s, p + d))
                        if any(st in sq[s].get(p, "") for s, p in nb):
                            near += 1
                            print("NEARBY  %s:%d `%s` is not in %s but is on a neighboring page" % (fn, ln, t, label))
                        else:
                            fail += 1
                            print("FAIL    %s:%d `%s` not found in %s" % (fn, ln, t, label))
    print("Terms checked: %d; nearby: %d; failures: %d" % (checked, near, fail))
    return 1 if (fail or (a.strict and near)) else 0


if __name__ == "__main__":
    sys.exit(main())
