# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS and asymptotic expressions against the cited page(s).

For each citation "(JE p.N[-M][, ...])" in agents/*.md, references/*.md and skills/*/SKILL.md, takes the part of the line
before the citation (since the previous citation) and extracts:
  - terms in italics (*...*) and in backticks (`...`) that look like ENGLISH terms/identifiers (ASCII);
  - O(...), Theta(...), Omega(...) expressions inside $...$ math (normalized: no spaces, no backslash,
    no ^ and braces);
and checks whether they appear on the cited page(s) of the text extracted from the PDF.
Results: OK; NEARBY (only on the neighboring page +-1); ELSEWHERE (exists in the book but far from the citation);
ABSENT (does not exist on any page of the book).
Usage: python -I audit_tokens.py --text erickson.txt --pkg PACKAGE_ROOT [--out report.txt] [--strict]
No network; read-only. Exit 0 if there is no INVALID/ABSENT/ELSEWHERE (NEARBY counts with --strict).
"""
import argparse
import json
import os
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

BS = chr(92)


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"[\s^{}" + re.escape(BS) + "]", "", s)


def load_pages(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def expand(spec):
    """Extracts the pages from "N", "N-M", "N, M", "N, note 3; JE p.M" etc. Returns a list [a, b, ...] or None if invalid.
    Free text after the pages (e.g. ", note 3", ": MomSelect") is ignored; format markers (percent, bracket, backslash) => None."""
    if any(ch in spec for ch in "%[\\"):
        return None
    s = re.sub(r"(?:nota|note)\s*\d+", "", spec)
    s = re.sub(r"JE\s*p\.?", "", s)
    m = re.match(r"^[\s\d,;\-–p.]*", s)
    s = m.group(0) if m else ""
    out = []
    for tok in re.split(r"\s*[,;]\s*", s.strip()):
        tok = re.sub(r"^p\.?\s*", "", tok).strip().rstrip(".")
        if not tok:
            continue
        mm = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if not mm:
            return None
        a = int(mm.group(1))
        b = int(mm.group(2) or a)
        if b < a:
            return None
        out.extend([a, b])
    return out or None


def asym(expr):
    e = expr
    for a, b in ((BS + "Theta", "Θ"), (BS + "Omega", "Ω"), (BS + "log", "log"), (BS + "lg", "lg"),
                 (BS + "cdot", "·"), (BS + "sqrt", "sqrt")):
        e = e.replace(a, b)
    e = e.replace(BS, "")
    return squash(e).lower()


CITE = re.compile(r"\(JE p\.?\s*([^)]+)\)")
ASCII_TERM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 \-+./']*$")
ASYM = re.compile(r"(?:O|" + re.escape(BS) + r"Theta|" + re.escape(BS) + r"Omega)\s*\((?:[^()]|\([^()]*\))*\)")


def terms_in(seg):
    terms = []
    for m in re.finditer(r"(?<![*\w])\*([^*\n]{3,60})\*(?![*\w])", seg):
        t = m.group(1).strip()
        if ASCII_TERM.match(t):
            terms.append(("term", t))
    for m in re.finditer(r"`([^`\n]{3,50})`", seg):
        t = m.group(1).strip()
        if t.startswith("[") or "JE p" in t:
            continue
        if ASCII_TERM.match(t) and not t.startswith(("scripts", "references", "python")) and not t.endswith((".md", ".py", ".json")):
            terms.append(("term", t))
    for m in re.finditer(r"\$([^$\n]+)\$", seg):
        for e in ASYM.finditer(m.group(1)):
            terms.append(("asympt", e.group(0)))
    return terms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--pkg", required=True)
    ap.add_argument("--out")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--allow", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit-tokens-allow.json"),
                    help="list of triaged and accepted items (documented false positives)")
    a = ap.parse_args()
    allowed = set()
    if os.path.exists(a.allow):
        allowed = {i["k"] for i in json.load(open(a.allow, encoding="utf-8"))["itens"]}
    naceito = 0
    pages = load_pages(a.text)
    N = max(pages)
    npg = {k: norm(v) for k, v in pages.items()}
    sqp = {k: squash(norm(v)) for k, v in pages.items()}
    sqall = " ".join(sqp.values())
    allnorm = " ".join(npg.values())
    files = []
    for sub in ("agents", "references", "skills"):
        base = os.path.join(a.pkg, sub)
        for root, _, fs in os.walk(base):
            for f in fs:
                if f.endswith(".md") and f != "INDEX.md":
                    files.append(os.path.join(root, f))
    ncite = ninvalid = ntok = nok = nprox = nabs = nfora = 0
    lines = []
    for fp in sorted(files):
        rel = os.path.relpath(fp, a.pkg)
        for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
            pos = 0
            for m in CITE.finditer(line):
                spec = m.group(1)
                seg = line[pos:m.start()]
                pos = m.end()
                if spec.strip().startswith("N") or any(ch in spec for ch in "%[\\"):
                    continue  # format placeholder
                ends = expand(spec)
                ncite += 1
                pl = []
                if ends:
                    for i in range(0, len(ends), 2):
                        pl.extend(range(ends[i], ends[i + 1] + 1))
                if not pl or any(p < 1 or p > N for p in pl):
                    ninvalid += 1
                    lines.append("INVALID  %s:%d (JE p.%s)" % (rel, ln, spec))
                    continue
                lo, hi = min(pl), max(pl)
                for kind, t in terms_in(seg):
                    ntok += 1
                    if kind == "term":
                        key = norm(t)

                        def fn(p, key=key):
                            return key in npg.get(p, "")
                        anywhere = key in allnorm
                    else:
                        key = asym(t)

                        def fn(p, key=key):
                            return key in sqp.get(p, "")
                        anywhere = key in sqall
                    keyf = rel.replace("\\", "/") + "|" + t
                    if any(fn(p) for p in pl):
                        nok += 1
                    elif keyf in allowed:
                        naceito += 1
                    elif fn(lo - 1) or fn(hi + 1):
                        nprox += 1
                        lines.append("NEARBY   %s:%d [%s] %r cited p.%s" % (rel, ln, kind, t, spec))
                    elif anywhere:
                        nfora += 1
                        lines.append("ELSEWHERE %s:%d [%s] %r cited p.%s (exists on another page)" % (rel, ln, kind, t, spec))
                    else:
                        nabs += 1
                        lines.append("ABSENT   %s:%d [%s] %r cited p.%s (does not exist in the book)" % (rel, ln, kind, t, spec))
    summ = ("Citations: %d (invalid: %d) | tokens checked: %d | OK: %d | accepted (allow-list): %d | NEARBY(+-1): %d | ELSEWHERE: %d | ABSENT: %d"
            % (ncite, ninvalid, ntok, nok, naceito, nprox, nfora, nabs))
    out = "\n".join(lines + [summ])
    print(out)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out + "\n")
    bad = ninvalid + nabs + nfora + (nprox if a.strict else 0)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
