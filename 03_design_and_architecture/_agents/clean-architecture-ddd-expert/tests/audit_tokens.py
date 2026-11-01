# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of the "(ACRONYM p.N[-M])" citations of the clean-architecture-ddd-expert package.

For each citation found in agents/*.md, AGENTS.md, README.md, .github/agents/*.md, references/*.md and
scripts/* (py/json):
  1. checks the page RANGE (1..n of the PDF) and flags a citation to a page that is only the blog sidebar
     (CA11 > 5, CA12 > 7, SRP > 5, OCP > 4, SREL > 5);
  2. (.md only) extracts TERMS from the passage preceding the citation (since the previous citation on the same line):
     terms in backticks and terms in ASCII italics (e.g. *Shotgun Surgery*), ignoring paths, commands, labels and
     placeholders, and checks whether they appear on the cited page(s). If they do not, but appear on a neighboring
     page (+-1), it warns NEAR; if not even close, FAIL.
Citations without an acronym "(p.N)" inherit the acronym of the section (single-source files, or a heading "## ... (`ACRONYM`)").

Usage (from the package root):
  python -I tests/audit_tokens.py --src <dir with DDD.txt, CA11.txt, ...> [--strict] [--verbose]
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

NPAGES = {"DDD": 59, "CA11": 15, "CA12": 15, "SRP": 15, "OCP": 15, "SREL": 15, "TARPIT": 66, "REACT": 2}
CONTENT_MAX = {"CA11": 5, "CA12": 7, "SRP": 5, "OCP": 4, "SREL": 5}
SIGLAS = "|".join(NPAGES)
FILE_DEFAULT = {
    "ddd-estrategico-e-context-maps.md": "DDD", "ddd-tatico-e-agregados.md": "DDD",
    "clean-architecture-e-the-lost-years.md": "CA11",
    "regras-de-dependencia-e-circulos-concentricos.md": "CA12",
    "principios-solid-srp-e-atores.md": "SRP",
    "out-of-the-tar-pit-complexidade-essencial-vs-acidental.md": "TARPIT",
    "programacao-funcional-relacional-frp.md": "TARPIT",
    "o-manifesto-reativo-2.0.md": "REACT",
}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("↵", "ff").replace(" ", " ").replace("­", "-")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("‐", "-").replace("�", "'")
    return re.sub(r"[\s\-]+", "", s.lower())


def load_pages(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for tok in re.split(r"\s*[,;]\s*", spec.strip()):
        tok = re.sub(r"^p\.\s*", "", tok)
        m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, b + 1))
    return pages


def candidate_terms(seg):
    out = []
    seg = re.sub(r"`\[[^\]`]*\]\s*$", "", seg)
    if seg.startswith("`"):
        seg = seg[1:]
    for tok in re.findall(r"`([^`]+)`", seg):
        t = tok.strip()
        if t.startswith("[") or t.startswith(("scripts/", "references/", "tests/", "python", "--")):
            continue
        if re.search(r"[<>{}=|]|\.\.\.|\\|\.py|\.md|\.json|\(\)\.|^\(", t):
            continue
        t = re.sub(r"\(\)$", "", t).strip(".,;:")
        if len(t) < 4 or re.fullmatch(r"[0-9.,%\s]+", t) or re.fullmatch(r"(%s) p\..*" % SIGLAS, t):
            continue
        if re.search(r"[^\x00-\x7f]", t):
            continue
        out.append(t)
    for tok in re.findall(r"(?<![*\w])\*([A-Z][A-Za-z0-9 /\-']{3,60}?)\*(?![*\w])", seg):
        out.append(tok.strip())
    return out


def scan_md(path, fname, default, pages, args, stats):
    cite = re.compile(r"\(\s*(?:(%s)\s+)?p\.\s*([0-9][0-9,;\s\-–]*)\)" % SIGLAS)
    cur_default = default
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.startswith("#"):
            hs = re.findall(r"`(%s)`" % SIGLAS, line)
            if len(hs) == 1:
                cur_default = hs[0]
        pos = 0
        line_sigla = None
        for m in cite.finditer(line):
            sigla = m.group(1) or line_sigla or cur_default
            if m.group(1):
                line_sigla = m.group(1)
            seg = line[pos:m.start()]
            pos = m.end()
            if not sigla:
                continue
            plist = expand(m.group(2))
            if not plist:
                continue
            stats["cit"] += 1
            where = "%s:%d" % (fname, ln)
            if max(plist) > NPAGES[sigla] or min(plist) < 1:
                stats["fail"] += 1
                print("FAIL   %s: (%s p.%s) out of range 1-%d" % (where, sigla, m.group(2).strip(), NPAGES[sigla]))
                continue
            if sigla in CONTENT_MAX and max(plist) > CONTENT_MAX[sigla]:
                stats["fail"] += 1
                print("FAIL   %s: (%s p.%s) cites a sidebar page (content up to p.%d)" % (where, sigla, m.group(2).strip(), CONTENT_MAX[sigla]))
                continue
            for t in candidate_terms(seg):
                st = norm(t).strip(",.;:")
                stats["tok"] += 1
                if any(st in pages[sigla].get(p, "") for p in plist):
                    continue
                nb = set()
                for p in plist:
                    nb.update((p - 1, p + 1))
                nb -= set(plist)
                if any(st in pages[sigla].get(p, "") for p in nb):
                    stats["near"] += 1
                    print("NEAR   %s: `%s` is not in %s p.%s but is on a neighboring page" % (where, t, sigla, m.group(2).strip()))
                else:
                    stats["fail"] += 1
                    print("FAIL   %s: `%s` not found in %s p.%s" % (where, t, sigla, m.group(2).strip()))


def scan_range_only(path, fname, stats):
    cite = re.compile(r"\b(%s)\s+p\.\s*([0-9][0-9,;\s\-–]*)" % SIGLAS)
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        for m in cite.finditer(line):
            plist = expand(m.group(2))
            if not plist:
                continue
            sigla = m.group(1)
            stats["cit"] += 1
            if max(plist) > NPAGES[sigla] or min(plist) < 1 or (sigla in CONTENT_MAX and max(plist) > CONTENT_MAX[sigla]):
                stats["fail"] += 1
                print("FAIL   %s:%d: (%s p.%s) outside the content range" % (fname, ln, sigla, m.group(2).strip()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    pages = {s: load_pages(os.path.join(a.src, s + ".txt")) for s in NPAGES}
    stats = {"cit": 0, "tok": 0, "near": 0, "fail": 0}
    md_files = []
    for sub in ("references", "agents", os.path.join(".github", "agents")):
        d = os.path.join(a.pkg, sub)
        if os.path.isdir(d):
            md_files += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".md")]
    for f in ("AGENTS.md", "README.md"):
        if os.path.exists(os.path.join(a.pkg, f)):
            md_files.append(os.path.join(a.pkg, f))
    for p in md_files:
        fn = os.path.relpath(p, a.pkg)
        scan_md(p, fn, FILE_DEFAULT.get(os.path.basename(p)), pages, a, stats)
    sd = os.path.join(a.pkg, "scripts")
    for f in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
        if f.endswith((".py", ".json")):
            scan_range_only(os.path.join(sd, f), os.path.join("scripts", f), stats)
    print("Citations: %d; terms checked: %d; near: %d; failures: %d" % (stats["cit"], stats["tok"], stats["near"], stats["fail"]))
    return 1 if (stats["fail"] or (a.strict and stats["near"])) else 0


if __name__ == "__main__":
    sys.exit(main())
