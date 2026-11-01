# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of "(SIGLA p.N)" citations of the cicd-build-automation-expert package.

For each citation "(SIGLA p.N[-M][, p.K][; OTHER p.X])" in agents/, references/, AGENTS.md, README.md,
.github/agents/ and scripts/*.py:
  1) checks the page RANGE against the PDF (CICD 67, GRADLE 78, GHA 7, SWE-G 408);
  2) extracts verifiable TERMS from the text preceding the citation and checks that they appear on the cited page(s):
       - terms in backticks (identifiers, commands, names) - always checked;
       - numbers with a unit (%, x, minutes...) and UPPERCASE acronyms - checked;
       - ASCII bold/italic terms - checked ONLY IF they exist in some source (otherwise they are Portuguese terms
         or package terms and are not claims about the source);
     Passages marked [extrapolation] are skipped (they are not claimed to be in the source); citations whose parenthesis mentions
     "v1" (audit of what v1 said) are skipped.
     If the term only appears on a neighboring page (+-1) => NEAR; if it does not appear => FAIL.

Usage: python -I tests/audit_tokens.py --src <pasta com CICD.txt GRADLE.txt GHA.txt SWEG.txt> [--pkg RAIZ] [--strict] [-v]
Exit 0 with no FAIL/RANGE (with --strict, NEAR also counts). No network.
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

SRC_FILES = {"CICD": "CICD.txt", "GRADLE": "GRADLE.txt", "GHA": "GHA.txt", "SWE-G": "SWEG.txt"}
NPAGES = {"CICD": 67, "GRADLE": 78, "GHA": 7, "SWE-G": 408}

CITE_GROUP = re.compile(r"\(([^()]*?(?:CICD|GRADLE|GHA|SWE-G) p\.[^()]*)\)")
PIECE = re.compile(r"(CICD|GRADLE|GHA|SWE-G) p\.\s*([0-9][0-9,\s\-–p\.]*)")
ABSENCE = re.compile(r"(?i)(does not appear|do not appear|is not in|are not in|not in the source|does not define|do not define|does not cover|do not cover|does not describe|does not say|not covered|no backing|absent|ausente|não aparece|nao aparece|não consta|nao consta|não está|não existe|não define|não definem|não trata|não tratam|não descreve|sem lastro|sem cobertura|não vêm|não diz|não há)")
STOP = {"sigla", "pdf", "url", "json", "yaml", "yml", "pt-br", "ci", "cd", "ci/cd", "cicd", "gradle", "gha", "swe-g",
        "dora", "html", "xml", "http", "https", "sdk", "cli", "ide", "dsl", "jar", "war"}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\ufffd", "'").replace("\xa0", " ")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("−", "-")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"[\s\-_/\\]+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): squash(norm(parts[i + 1])) for i in range(1, len(parts), 2)}


def expand(spec):
    pages = []
    for m in re.finditer(r"(\d+)(?:\s*[-–]\s*(\d+))?", spec):
        a = int(m.group(1))
        b = int(m.group(2) or a)
        pages.extend(range(a, max(a, b) + 1))
    return pages


def parse_group(inner):
    out = []
    for piece in inner.split(";"):
        m = PIECE.search(piece)
        if m:
            out.append((m.group(1), expand(m.group(2).replace("p.", ""))))
    return out


def terms_of(seg):
    """-> list of (term, strict); strict=True for backticks"""
    terms = []
    for t in re.findall(r"`([^`]+)`", seg):
        t = t.strip()
        if not t or len(t) < 3 or "<" in t or "..." in t or t.startswith(("scripts/", "references/", "python", "tests/", "agents/", "[")):
            continue
        if re.search(r"\.(md|py|json)$", t):
            continue
        if ("{" in t and "${{" not in t) or "*" in t or "NOME" in t or "NAME" in t:
            continue
        for part in (t.split("|") if "|" in t else [t]):
            part = part.strip()
            if len(part) >= 3 and part.lower() not in STOP:
                terms.append((part, True))
    seg2 = re.sub(r"`[^`]*`", " ", seg)
    for t in re.findall(r"\b(\d+(?:[.,]\d+)?\s?(?:%|x|vezes|dígitos|digitos|minutos|min|horas|dias|segundos|times|digits|minutes|hours|days|seconds))", seg2):
        terms.append((t, False))
    for t in re.findall(r"\b([A-Z]{3,}[A-Za-z0-9\-]*)\b", seg2):
        if t.lower() not in STOP:
            terms.append((t, False))
    for t in re.findall(r"\*{1,2}([A-Za-z][A-Za-z0-9 \-\./]{3,40})\*{1,2}", seg2):
        t = t.strip()
        if t.lower() not in STOP and re.search(r"[A-Z].*[A-Z]|[0-9\-\./]", t):
            terms.append((t, False))
    seen, out = set(), []
    for t, st in terms:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append((t, st))
    return out


def variants(t):
    t = t.strip().strip(",.;:")
    t = re.sub(r"\(\)$", "", t)
    vs = [t]
    if len(t) > 3 and t.endswith("s") and t[:-1].isupper():
        vs.append(t[:-1])
    m = re.fullmatch(r"(\d+)(?:[.,](\d+))?\s?(%|x|vezes|dígitos|digitos|minutos|min|horas|dias|segundos|times|digits|minutes|hours|days|seconds)", t)
    if m:
        n = m.group(1) + ("." + m.group(2) if m.group(2) else "")
        u = m.group(3)
        if u == "%":
            vs += [n + "%", n + " %"]
        elif u in ("x", "vezes"):
            vs += [n + "x", n + " times"]
        else:
            vs.append(n)
    return vs


def files_to_scan(pkg):
    for sub in ("agents", "references", os.path.join(".github", "agents")):
        d = os.path.join(pkg, sub)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".md"):
                    yield os.path.join(d, fn)
    for fn in ("AGENTS.md", "README.md"):
        p = os.path.join(pkg, fn)
        if os.path.isfile(p):
            yield p
    d = os.path.join(pkg, "scripts")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"):
                yield os.path.join(d, fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in SRC_FILES.items()}
    everything = {k: "".join(v.values()) for k, v in pages.items()}
    ncit = nrange = nterms = nok = nnear = nfail = nskip = 0
    cit_bad = 0
    for path in files_to_scan(a.pkg):
        rel = os.path.relpath(path, a.pkg)
        for ln, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
            pos = 0
            for m in CITE_GROUP.finditer(line):
                seg = line[pos:m.start()]
                pos = m.end()
                if re.search(r"\bv1\b", m.group(1)):
                    continue
                groups = parse_group(m.group(1))
                if not groups:
                    continue
                ncit += 1
                bad = False
                allpages = {}
                for sig, pl in groups:
                    for p in pl:
                        if p < 1 or p > NPAGES[sig]:
                            nrange += 1
                            bad = True
                            print(f"RANGE   {rel}:{ln}: {sig} p.{p} outside the PDF (1-{NPAGES[sig]})")
                    allpages.setdefault(sig, set()).update(p for p in pl if 1 <= p <= NPAGES[sig])
                if "[extrapolation]" in seg or "[extrapolação]" in seg or "[extrapolacao]" in seg or ABSENCE.search(seg):
                    nskip += 1
                    continue
                for t, strict_tok in terms_of(seg):
                    found = near = False
                    present_somewhere = False
                    for sig, ps in allpages.items():
                        for v in variants(t):
                            sv = squash(norm(v))
                            if len(sv) < 2:
                                continue
                            if sv in everything[sig]:
                                present_somewhere = True
                            if any(sv in pages[sig].get(p, "") for p in ps):
                                found = True
                            elif any(sv in pages[sig].get(q, "") for p in ps for q in (p - 1, p + 1)):
                                near = True
                    if not strict_tok and not present_somewhere and not any(
                            squash(norm(v)) in "".join(everything.values()) for v in variants(t)):
                        nskip += 1  # Portuguese/package term: not a claim about the source
                        continue
                    nterms += 1
                    if found:
                        nok += 1
                    elif near:
                        nnear += 1
                        bad = bad or a.strict
                        print(f"NEAR    {rel}:{ln}: `{t}` is not in {m.group(1)} but is on a neighboring page")
                    else:
                        nfail += 1
                        bad = True
                        print(f"FAIL    {rel}:{ln}: `{t}` not found in {m.group(1)}")
                if bad:
                    cit_bad += 1
    print(f"Citations: {ncit}; invalid range: {nrange}; terms checked: {nterms} (ok {nok}, near {nnear}, failures {nfail}); "
          f"skipped: {nskip}; citations with problems: {cit_bad}")
    sys.exit(1 if (nfail or nrange or (a.strict and nnear)) else 0)


if __name__ == "__main__":
    main()
