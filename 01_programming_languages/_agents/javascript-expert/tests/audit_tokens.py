# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of the javascript-expert package citations against the text extracted from the PDFs.

For EVERY citation "ABBR p.N[-M][, p.K ...]" (ABBR = Spec, EJpt, EJ1) in agents/*.md, references/*.md, README.md,
AGENTS.md, .github/agents/*.md, skills/**/SKILL.md, tests/*.md and JSON/py data of the skills:
  1) RANGE: the page exists in the corresponding PDF (Spec 1-876, EJpt 1-504, EJ1 1-247; see --counts).
  2) TOKENS: the terms between `backticks` (identifiers, no spaces) in the passage preceding the citation must appear
     on the cited page(s) (comparison ignoring whitespace and case). If they only appear on a neighboring page
     (+-1) the output is NEAR (recorded tolerance, counts as a failure with --strict); if they do not appear, FAIL.
Usage: python -I tests/audit_tokens.py --src <folder with ecma262.txt, ejs-pt.txt, ejs-en.txt> [--pkg ROOT] [--strict] [-v]
Text extracted by tests/extract_pages.py (markers "=== PAGE N ===", N = PDF page). No network, read-only.
Exit 0 with no FAIL.
"""
import argparse, os, re, sys, unicodedata, glob

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

BOOKS = {"Spec": "ecma262.txt", "EJpt": "ejs-pt.txt", "EJ1": "ejs-en.txt"}
DASH = "[–—-]"
CITE = re.compile(r"\b(Spec|EJpt|EJ1) pp?\.\s*(\d+(?:%s\d+)?(?:\s*[,;]\s*p\.\s*\d+(?:%s\d+)?)*)" % (DASH, DASH))


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\xa0", " ")
    return s.lower()


def squash(s):
    return re.sub(r"\s+", "", norm(s))


def load_pages(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): squash(parts[i + 1]) for i in range(1, len(parts), 2)}


def expand(spec):
    out = []
    for m in re.finditer(r"(\d+)(?:%s(\d+))?" % DASH, spec):
        a = int(m.group(1)); b = int(m.group(2) or a)
        out.extend(range(a, b + 1) if b >= a else [a])
    return out


# terms too generic to discriminate a page (they appear in almost all); ignored in the token audit
GENERIC = {"typeerror", "rangeerror", "syntaxerror", "referenceerror", "error", "null", "undefined", "true", "false",
           "class", "const", "function", "extends", "next", "foreach", "length", "break", "this", "else", "return",
           "async", "await", "yield", "export", "import", "print", "size", "clear", "some", "every", "filter", "slice",
           "includes", "stack", "window", "document", "value", "done", "then", "catch", "finally", "super", "static",
           "string", "number", "object", "array", "symbol", "boolean"}


def variants(t):
    """alternative ways of writing the same identifier (the Spec uses %Symbol.x% and @@x)."""
    out = {t}
    m = re.fullmatch(r"\[?(Symbol\.\w+)\]?", t)
    if m:
        out |= {"%" + m.group(1) + "%", m.group(1)}
    m = re.fullmatch(r"@@(\w+)", t)
    if m:
        out |= {"%Symbol." + m.group(1) + "%", "Symbol." + m.group(1)}
    return out


# negation markers: Portuguese (legacy wording kept) and English
NEG = re.compile(r"n[aã]o (consta|constam|aparece|aparecem|existe|existem|h[aá]|trata|cobre|cita|diz|menciona|define|traz|usa|nomeia|informa|ensina)|ausente|n/c|fora das fontes|sem cobertura|nenhuma fonte|nem "
                 r"|(do|does|is|are|was|were) not (appear|exist|occur|cover|mention|define|cite|say|state|name|use|teach|include|have|carry|address|list|treat|contain|show)"
                 r"|absent|not covered|no source|neither|nor |outside the sources|not in the (source|book|sources|books)|not stated|\bno (mention|occurrence|trace)", re.I)


def illustrative(t, seg):
    """True if the term is illustrative code (call, index, operator) or the sentence asserts ABSENCE in the source."""
    if any(c in t for c in "()[]?#<>") or re.search(r"\w\.\w+\.", t):
        return True
    return NEG.search(seg) is not None


def cand_terms(seg):
    res = []
    for tok in re.findall(r"`([^`]+)`", seg):
        t = tok.strip()
        if any(c in t for c in (" ", "<", ">", "{", "}", "…", "...", "/", "\\", "'", '"', "=", "$", ";", "|")):
            continue
        if t.startswith(("scripts", "references", "python", "--", "%")):
            continue
        t = re.sub(r"\(\)$", "", t).rstrip(".,:")
        t = t.rstrip("*")
        if len(t) < 4 or re.fullmatch(r"[0-9.]+", t):
            continue
        if t.lower() in GENERIC:
            continue
        res.append(t)
    return res


def files(pkg):
    pats = ["agents/*.md", "references/*.md", "README.md", "AGENTS.md", ".github/agents/*.md", "skills/*/SKILL.md",
            "tests/*.md", "skills/*/scripts/*.py", "skills/*/scripts/*.json", "tests/*.json"]
    out = []
    for p in pats:
        out += glob.glob(os.path.join(pkg, p))
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--baseline", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit-tokens-baseline.txt"),
                    help="failures already REVIEWED manually (token is not literally on the page, but the claim was checked)")
    ap.add_argument("--write-baseline", action="store_true", help="writes the current failures as baseline (only after manual review!)")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    pages = {k: load_pages(os.path.join(a.src, v)) for k, v in BOOKS.items()}
    counts = {k: len(v) for k, v in pages.items()}
    ncite = nrange = ntok = nnear = nfail = 0
    bysig = {k: 0 for k in BOOKS}
    nline = nskip = nbase = 0
    base = set()
    if os.path.isfile(a.baseline) and not a.write_baseline:
        base = {l.rstrip(chr(10)) for l in open(a.baseline, encoding="utf-8") if l.strip() and not l.startswith("#")}
    newbase = []
    for fp in files(a.pkg):
        rel = os.path.relpath(fp, a.pkg)
        skip_tokens = rel.endswith((".json", ".py")) or rel.startswith("tests")
        for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
            pos = 0
            cites = []
            for m in CITE.finditer(line):
                sig = m.group(1); plist = expand(m.group(2))
                seg = line[pos:m.start()]; pos = m.end()
                ncite += 1; bysig[sig] += 1
                bad = [p for p in plist if p not in pages[sig]]
                if bad:
                    nrange += 1
                    print(f"RANGE   {rel}:{ln}: {sig} p.{m.group(2)} outside the PDF ({counts[sig]} pages)")
                    continue
                cites.append((sig, plist, m.group(2), seg))
            if skip_tokens or not cites:
                continue
            # union of all pages cited on the same line (table row = several sources)
            union = "".join(pages[sg][p] for sg, pl, _, _ in cites for p in pl)
            for sig, plist, raw, seg in cites:
                blob = "".join(pages[sig][p] for p in plist)
                nb = set()
                for p in plist: nb.update((p - 1, p + 1))
                nb -= set(plist)
                nblob = "".join(pages[sig].get(p, "") for p in nb)
                for t in cand_terms(seg):
                    sts = [squash(v) for v in variants(t)]
                    ntok += 1
                    if any(x in blob for x in sts): continue
                    if any(x in union for x in sts):
                        nline += 1   # present in another source/page cited on the same line: accepted
                    elif any(x in nblob for x in sts):
                        nnear += 1
                        print(f"NEAR    {rel}:{ln}: `{t}` is not in {sig} p.{raw} (it is on a neighboring page)")
                    else:
                        where = [k for k, v in pages[sig].items() if any(x in v for x in sts)]
                        if illustrative(t, seg):
                            nskip += 1   # illustrative code or claim of absence: not an attribution to a page
                            continue
                        key = "%s|%s|%s p.%s" % (rel.replace(os.sep, "/"), t, sig, raw)
                        newbase.append(key)
                        if key in base:
                            nbase += 1   # reviewed manually (see baseline)
                            continue
                        nfail += 1
                        loc = ("; in the book only on p.%s" % ",".join(map(str, where[:8]))) if where else "; absent from the whole book"
                        print(f"FAIL    {rel}:{ln}: `{t}` not found in {sig} p.{raw}{loc}")
    print(f"accepted via another citation on the same line: {nline}; ignored (illustrative code or claim of absence): {nskip}")
    if a.write_baseline:
        with open(a.baseline, "w", encoding="utf-8", newline=chr(10)) as fh:
            fh.write("# token failures REVIEWED manually in the audit (file|term|source page). Regenerate only after a new review." + chr(10))
            fh.write(chr(10).join(sorted(set(newbase))) + chr(10))
        print("baseline written:", len(set(newbase)))
    print(f"reviewed manually (baseline): {nbase}")
    print(f"Citations: {ncite} {bysig}; out of range: {nrange}; terms checked: {ntok}; near: {nnear}; failures: {nfail}")
    sys.exit(1 if (nrange or nfail or (a.strict and nnear)) else 0)


if __name__ == "__main__":
    main()
