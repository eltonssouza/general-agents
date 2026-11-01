# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS between `backticks` against the cited page (data-structures-expert package).

For each citation "(ODS p.N[-M][, ...])" in agents/*.md, references/*.md, skills/*/SKILL.md, README.md, AGENTS.md and
.github/agents/*.md, it takes the backticked terms in the preceding text (since the previous citation on the same line) and
checks that they appear on the cited page(s) of the text extracted from the PDF ("=== PAGE N ===" markers, N = PDF page).
- Terms with spaces, placeholders (<...>, ...), with '$' (math), with 'ODS p.' or very short are ignored.
- Underscores and spaces are ignored in the comparison (the PDF loses '_' and uses ligatures: NFKC handles that).
- Term absent from the cited page(s) but present on a neighboring page (+-1): NEAR; otherwise: FAIL.
- It also checks that the page range is between 1 and the total number of pages and that begin <= end.

Usage: python -I tests/audit_tokens.py --text PATH/Open-Data-Structures.txt [--pkg ROOT] [--strict] [-v]
Exit 0 without FAIL (NEAR counts as a failure with --strict). No network; read-only.
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
    s = unicodedata.normalize("NFKC", s).replace("\xa0", " ")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return s.lower()


def squash(s):
    return re.sub(r"[\s_]+", "", norm(s))


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    bad = []
    for tok in re.split(r"\s*,\s*", spec.strip()):
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            if b < a:
                bad.append(tok)
                continue
            pages.extend(range(a, b + 1))
        else:
            bad.append(tok)
    return pages, bad


def files(pkg):
    out = []
    for sub in ("agents", "references", ".github/agents"):
        d = os.path.join(pkg, *sub.split("/"))
        if os.path.isdir(d):
            out += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".md")]
    sk = os.path.join(pkg, "skills")
    if os.path.isdir(sk):
        for s in sorted(os.listdir(sk)):
            p = os.path.join(sk, s, "SKILL.md")
            if os.path.isfile(p):
                out.append(p)
    for f in ("README.md", "AGENTS.md"):
        if os.path.isfile(os.path.join(pkg, f)):
            out.append(os.path.join(pkg, f))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pages = load_pages(a.text)
    total = max(pages)
    sq = {k: squash(v) for k, v in pages.items()}
    cite = re.compile(r"\(ODS p\.([^)]+)\)")
    ncites = nterms = near = fail = badrange = 0
    for path in files(a.pkg):
        rel = os.path.relpath(path, a.pkg)
        for ln, line in enumerate(open(path, encoding="utf-8"), 1):
            pos = 0
            for m in cite.finditer(line):
                seg = line[pos:m.start()]
                if seg.endswith("`"):
                    seg = seg[:-1]
                pos = m.end()
                if line[pos:pos + 1] == "`":
                    pos += 1
                if m.group(1).strip() in ("N", "N-M", "N[-M]"):
                    continue  # format placeholder, not a citation
                ncites += 1
                plist, bad = expand(m.group(1))
                if bad or any(p < 1 or p > total for p in plist):
                    badrange += 1
                    print("RANGE   %s:%d: (ODS p.%s) outside the range 1-%d or malformed" % (rel, ln, m.group(1), total))
                    continue
                if not plist:
                    continue
                for tok in re.findall(r"`([^`]+)`", seg):
                    t0 = tok.strip()
                    if (" " in t0 or "<" in t0 or "..." in t0 or "…" in t0 or "$" in t0 or "ODS p." in t0
                            or t0.startswith(("scripts/", "references/", "python", "skills/", "tests/", "["))
                            or "{" in t0 or "/" in t0 or "\\" in t0 or t0.endswith((".md", ".py", ".json", ".pdf", ".txt"))):
                        continue
                    cands = []
                    for part in t0.split("|"):
                        part = part.split("=")[0].rstrip("*").rstrip(".").rstrip("/")
                        part = re.sub(r"\(.*\)$", "", part)
                        if len(part) >= 3 and not re.fullmatch(r"[0-9.]+", part):
                            cands.append(part)
                    for t in cands:
                        st = squash(t).strip(",.;")
                        nterms += 1
                        if any(st in sq.get(p, "") for p in plist):
                            continue
                        nb = set()
                        for p in plist:
                            nb.update((p - 1, p + 1))
                        nb -= set(plist)
                        if any(st in sq.get(p, "") for p in nb if p in sq):
                            near += 1
                            print("NEAR    %s:%d: `%s` is not on p.%s but is on a neighboring page" % (rel, ln, t, m.group(1)))
                        else:
                            fail += 1
                            print("FAIL    %s:%d: `%s` not found on p.%s" % (rel, ln, t, m.group(1)))
    print("Citations: %d; terms checked: %d; invalid ranges: %d; near: %d; failures: %d"
          % (ncites, nterms, badrange, near, fail))
    sys.exit(1 if (fail or badrange or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
