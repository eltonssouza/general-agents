# -*- coding: utf-8 -*-
"""
audit_tokens.py - audits TERMS between `backticks` against the cited page(s).

For each citation (Tut|Ref|Notes|Lib p.N[-M][, p.K ...]) in references/*.md and skills/*/SKILL.md, takes the terms
between backticks in the preceding stretch (since the previous citation on the same line) and checks whether they
appear in the extracted text of the cited page. If the term appears only on a neighboring page (+-1) -> NEAR; if it
does not appear nearby -> FAIL. Terms with <...>, ellipses, package paths, or very short ones are ignored.

Page convention: N = PDF page (marker "=== PAGE N ===" of the extracted text).

Usage: python -I tests/audit_tokens.py --src FOLDER_WITH_THE_TXT_FILES [--pkg ROOT] [--strict] [--verbose]
  FOLDER_WITH_THE_TXT_FILES must contain Python-3.14-Tutorial.txt, Python-3.14-Language-Reference.txt,
  Python-Notes-for-Professionals.txt and Python-3.14-Standard-Library.txt (see the verifiers section of the README).
Exit 0 without FAIL (NEAR counts as a failure with --strict). Read-only, no network.
"""
import argparse, os, re, sys, unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SOURCES = {
    "Tut": ("Python-3.14-Tutorial.txt", 167),
    "Ref": ("Python-3.14-Language-Reference.txt", 225),
    "Notes": ("Python-Notes-for-Professionals.txt", 813),
    "Lib": ("Python-3.14-Standard-Library.txt", 2488),
}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\ufffd", "'").replace("\xa0", " ")
    for a, b in (("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'),
                 ("\u2013", "-"), ("\u2014", "-"), ("\u2212", "-"), ("\u200b", ""), ("\u00ad", "")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s.lower()).strip()


def squash(s):
    return re.sub(r"\s+", "", s)


def load_pages(path):
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


SIGLA_RE = re.compile(r"\b(Tut|Ref|Notes|Lib)\s+pp?\.\s*")
NUM_RE = re.compile(r"\s*(?:p{1,2}\.\s*)?(\d+)(?:\s*[-\u2013]\s*(\d+))?")


def parse_citations(line):
    """Returns [(start, end, abbreviation, [pages])]. Accepts 'Tut p.19, p.30, p.31-32; Ref p.5, 7'."""
    out = []
    for m in SIGLA_RE.finditer(line):
        pos = m.end()
        pages = []
        while True:
            n = NUM_RE.match(line, pos)
            if not n:
                break
            a = int(n.group(1))
            b = int(n.group(2) or a)
            if b < a or b - a > 60:
                b = a
            pages.extend(range(a, b + 1))
            pos = n.end()
            sep = re.match(r"\s*,\s*(?=(?:p{1,2}\.\s*)?\d)", line[pos:])
            if sep:
                pos += sep.end()
            else:
                break
        if pages:
            out.append((m.start(), pos, m.group(1), pages))
    return out


def candidates(tok):
    t0 = tok.strip()
    if "<" in t0 or "..." in t0 or "\u2026" in t0 or "{" in t0:
        return []
    if t0.startswith(("scripts/", "references/", "skills/", "python ", "python-", "tests/")) or "/" in t0 and t0.endswith((".py", ".md", ".json")):
        return []
    if re.search(r"[^\x00-\x7f]", t0):
        return []
    out = []
    for part in t0.split("|"):
        part = part.strip().rstrip(".,;:")
        part = re.sub(r"\(\)$", "", part)
        if len(part) >= 4 and not re.fullmatch(r"[0-9.\s]+", part):
            out.append(part)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--pkg", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--baseline", default=None,
                    help="file with ALREADY TRIAGED failures (default: tests/audit_tokens_baseline.txt); only a new failure fails")
    ap.add_argument("--write-baseline", action="store_true", help="writes the current failures as the triaged baseline")
    a = ap.parse_args()
    sq = {}
    for sg, (fn, n) in SOURCES.items():
        pg = load_pages(os.path.join(a.src, fn))
        if len(pg) != n:
            print(f"WARNING: {fn} has {len(pg)} pages (expected {n})")
        sq[sg] = {k: squash(norm(v)) for k, v in pg.items()}
    targets = []
    refs = os.path.join(a.pkg, "references")
    for fn in sorted(os.listdir(refs)):
        if fn.endswith(".md") and not fn.startswith("INDEX"):
            targets.append(os.path.join(refs, fn))
    sk = os.path.join(a.pkg, "skills")
    for d in sorted(os.listdir(sk)):
        p = os.path.join(sk, d, "SKILL.md")
        if os.path.exists(p):
            targets.append(p)
    ag = os.path.join(a.pkg, "agents", "python-expert.md")
    checked = near = fail = ncite = skipped = known = 0
    base_path = a.baseline or os.path.join(a.pkg, "tests", "audit_tokens_baseline.txt")
    baseline = set()
    if os.path.exists(base_path) and not a.write_baseline:
        baseline = {l.rstrip() for l in open(base_path, encoding="utf-8") if l.strip() and not l.startswith("#")}
    seen_fail = []
    for fp in targets:
        rel = os.path.relpath(fp, a.pkg)
        for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
            prev = 0
            prev0 = 0
            for (s, e, sg, pages) in parse_citations(line):
                ncite += 1
                seg = line[prev:s]
                prev = e
                if re.search(r"\[(?:infer|extrapol|a confirmar|to confirm|sem fonte|no source)", seg, re.I):
                    skipped += 1  # stretch labeled as not-from-the-book: nothing to check on the page
                    continue
                for p in pages:
                    if p not in sq[sg]:
                        fail += 1
                        print(f"FAIL range {rel}:{ln}: {sg} p.{p} does not exist")
                if line.lstrip().startswith("|"):
                    # table: only the first 2 cells (symptom/cause); the fix column mixes
                    # package recommendations and is not checked against the page
                    cells = seg.split("|")
                    seg = "|".join(cells[:3]) if prev0 == 0 else seg
                prev0 = 1
                for tok in re.findall(r"`([^`]+)`", seg):
                    for t in candidates(tok):
                        st = squash(norm(t)).strip(",.;")
                        checked += 1
                        if any(st in sq[sg].get(p, "") for p in pages):
                            continue
                        nb = set()
                        for p in pages:
                            nb.update((p - 1, p + 1))
                        nb -= set(pages)
                        if any(st in sq[sg].get(p, "") for p in nb):
                            near += 1
                            print(f"NEAR {rel}:{ln}: `{t}` is not in {sg} p.{pages[0]}..{pages[-1]} but is on a neighboring one")
                        else:
                            key = f"{rel.replace(os.sep, '/')}|{t}|{sg} p.{','.join(map(str, pages))}"
                            seen_fail.append(key)
                            if key in baseline:
                                known += 1
                                continue
                            fail += 1
                            other = [p for p in sorted(sq[sg]) if st in sq[sg][p]]
                            where = ("other pages: " + ",".join(map(str, other[:6])) + ("..." if len(other) > 6 else "")) if other else "absent from the source"
                            print(f"FAIL    {rel}:{ln}: `{t}` not found in {sg} p.{','.join(map(str, pages))} ({where})")
    if a.write_baseline:
        with open(base_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# audit_tokens failures ALREADY TRIAGED in the audit (see tests/relatorio-de-fidelidade.md): backticked term absent from the\n"
                     "# cited page because it is a package form (suggestion/identifier/spelling) or because of a line with several citations.\n"
                     "# format: file|term|source p.pages\n")
            for k in sorted(set(seen_fail)):
                fh.write(k + "\n")
        print(f"baseline written: {len(set(seen_fail))} entries in {base_path}")
        sys.exit(0)
    print(f"Already triaged failures (baseline): {known}")
    print(f"Citations read: {ncite} ({skipped} with an [inference]/[extrapolation] stretch ignored); terms checked: {checked}; near: {near}; failures: {fail}")
    sys.exit(1 if (fail or (a.strict and near)) else 0)


if __name__ == "__main__":
    main()
