# -*- coding: utf-8 -*-
"""
audit_tokens.py - automatic audit of TERMS and NUMBERS against the cited page.

For each citation "(ABBREV p.N[-M][; p.K])" in references/*.md, agents/*.md, AGENTS.md, .github/agents/*.md and
README.md, takes the span of the same line since the previous citation and extracts:
  - terms between `backticks` (without spaces, without placeholders);
  - numbers with 2+ digits or with % (thousands separators and decimal comma normalized);
  - proper names from a curated list (Piper, Rosie, Tricorder, ...).
Each item must appear in one of the cited pages of the ABBREV. If it appears only on a neighboring page (+-1):
NEAR (fails with --strict). If it appears nowhere nearby: FAIL.
Citations whose span is marked [extrapolation]/[inference] or "NOT"/"does not appear" are ignored
(they do not assert book text). Both the English labels and the Portuguese ones of the untranslated
references/ are recognized.

Usage: python -I tests/audit_tokens.py [--src DIR_WITH_TXT] [--strict] [-v]
Text: DIR/<name>.txt (=== PAGE N ===) or extracted from the PDFs at ../../*.pdf with PyMuPDF.
Exit 0 without FAIL.
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

PDFS = {
    "SWE-G": "Software-Engineering-at-Google-completo",
    "SWE-PREV": "Software-Engineering-at-Google",
    "CC2": "Code-Complete-SampleChapter-Pearson",
    "97TH": "97-Things-Every-Programmer-Should-Know",
}
PROPER = ["Piper", "Rosie", "Tricorder", "Critique", "Kythe", "Blaze", "Bazel", "Forge", "ObjFS", "Gerrit", "Mockito",
          "Guice", "Dagger", "Error Prone", "clang-tidy", "clang-format", "gofmt", "buildifier", "Takeout", "Beyonc",
          "Silverstein", "Mediratta", "Parnas", "Brooks", "Dijkstra", "Fusco", "Marquardt", "Kua", "Jevons", "Abseil",
          "Googley", "Buganizer", "Refaster", "ClangMR", "JavacFlume", "Cider", "Zapfhahn", "GwsQ", "WebDriver"]


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("�", "'").replace("\xa0", " ")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-")):
        s = s.replace(a, b)
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)  # 50,000 -> 50000
    return re.sub(r"\s+", " ", s).lower()


def squash(s):
    return re.sub(r"\s+", "", s)


def load_txt(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    parts = re.split(r"=== PAGE (\d+) ===", raw)
    return {int(parts[i]): squash(norm(parts[i + 1])) for i in range(1, len(parts), 2)}


def load_pdf(path):
    import fitz
    return {i: squash(norm(pg.get_text())) for i, pg in enumerate(fitz.open(path), 1)}


def load_source(sig, src):
    name = PDFS[sig]
    if src and os.path.exists(os.path.join(src, name + ".txt")):
        return load_txt(os.path.join(src, name + ".txt"))
    here = os.path.dirname(os.path.abspath(__file__))
    pdf = os.path.normpath(os.path.join(here, "..", "..", "..", name + ".pdf"))
    if os.path.exists(pdf):
        return load_pdf(pdf)
    sys.exit("source missing for %s" % sig)


def expand(spec):
    pages = []
    for tok in re.split(r"\s*[,;]\s*", spec.strip()):
        tok = re.sub(r"^p\.", "", tok.strip())
        m = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", tok)
        if m:
            a = int(m.group(1))
            b = int(m.group(2) or a)
            pages.extend(range(a, min(b, a + 40) + 1))
    return pages


CITE = re.compile(r"\((SWE-G|SWE-PREV|CC2|97TH) (p\.[^)]+)\)")
BARE = re.compile(r"\((p\.[^)]+)\)")
LABEL = re.compile(r"\[(?:from source|do livro|inference|infer[eê]ncia|extrapolation|extrapola[cç][aã]o|DATED|DATADO)\]")
SOURCE_LABELS = ("[from source]", "[do livro]")
PAGEREF = re.compile(r"p\.\s?\d+(?:\s?[-,;]\s?(?:p\.\s?)?\d+)*")
CUT = re.compile(r"N[AÃ]O\b|NOT\b|\bv1\b|Nota de fidelidade|Fidelity note|n[aã]o consta|is not in the (?:book|source|sample)|n[aã]o aparece|does not appear|n[aã]o usa|does not use|n[aã]o traz|does not (?:carry|bring|contain)|n[aã]o diz|does not say|n[aã]o est[aá]|is not in|era ilustra|was illustrative")


QUOTE = re.compile(r"\"([A-Za-z][A-Za-z0-9 '/,.:;?!()+_-]{3,90})\"")
EN_WORDS = re.compile(r"\b(the|of|to|is|are|you|your|it|we|if|not|be|and|or|for|in|on|that|this|should|can|will|have|their|only|never|always|own|every|what|how)\b", re.I)


def items(seg):
    out = []
    for tok in re.findall(r"`([^`]+)`", seg):
        t = tok.strip()
        if " " in t or "<" in t or "..." in t or t.startswith(("scripts/", "references/", "python", "tests/")):
            continue
        t = t.rstrip("()").rstrip(".")
        if len(t) >= 4 and not re.fullmatch(r"[0-9.,%]+", t) and not t.endswith((".md", ".py", ".json")):
            out.append(("term", t))
    seg2 = re.sub(r"\((?:SWE-G|SWE-PREV|CC2|97TH) p\.[^)]*\)", " ", seg)
    seg2 = re.sub(r"`[^`]*`", " ", seg2)
    seg2 = PAGEREF.sub(" ", seg2)
    seg2 = re.sub(r"97TH", " ", seg2)
    for m in re.finditer(r"(?<![\w.])(\d{1,3}(?:\.\d{3})+|\d{2,})(?:,(\d+))?\s?(%)?", seg2):
        whole = m.group(1).replace(".", "")
        if m.group(2):
            whole += "," + m.group(2)
        txt = whole.replace(",", ".") + (m.group(3) or "")
        # ignore years and page numbers without a suffix
        if re.fullmatch(r"(19|20)\d\d", whole) and not m.group(3):
            continue
        out.append(("number", txt))
    for q in re.findall(QUOTE, seg2):
        q = q.strip(' ,.;:?!')
        if len(q) >= 4 and EN_WORDS.search(q) and ' ' in q:
            out.append(('quote', q))
    for pn in PROPER:
        if re.search(r"\b" + re.escape(pn), seg2):
            out.append(("name", pn))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--pkg", default=None, help="root of the package to audit (default: this package)")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    pkg = a.pkg or os.path.dirname(here)
    files = []
    for d in ("references", "agents", ".github/agents"):
        dd = os.path.join(pkg, d)
        if os.path.isdir(dd):
            files += [os.path.join(dd, f) for f in sorted(os.listdir(dd)) if f.endswith(".md")]
    for f in ("README.md", "AGENTS.md"):
        if os.path.exists(os.path.join(pkg, f)):
            files.append(os.path.join(pkg, f))

    cache = {}
    checked = near = fail = ncites = 0
    per = {}
    for fp in files:
        rel = os.path.relpath(fp, pkg)
        for ln, line in enumerate(open(fp, encoding="utf-8"), 1):
            units = []
            labels = list(LABEL.finditer(line))
            if labels:
                for i, lm in enumerate(labels):
                    if lm.group(0) not in SOURCE_LABELS:
                        continue
                    end_i = labels[i + 1].start() if i + 1 < len(labels) else len(line)
                    units.append(line[lm.start():end_i])
            else:
                pos = 0
                for m in CITE.finditer(line):
                    units.append(line[pos:m.end()])
                    pos = m.end()
            for unit in units:
                cm = CITE.search(unit)
                if not cm:
                    continue
                ncites += 1
                sig = cm.group(1)
                per.setdefault(sig, [0, 0, 0, 0])[0] += 1
                pl = []
                for c in CITE.finditer(unit):
                    if c.group(1) == sig:
                        pl += expand(c.group(2))
                for b2 in BARE.finditer(unit):
                    pl += expand(b2.group(1))
                pl = sorted(set(pl))
                if not pl:
                    continue
                if sig not in cache:
                    cache[sig] = load_source(sig, a.src)
                pages = cache[sig]
                bad = [p for p in pl if p not in pages]
                if bad:
                    fail += 1
                    print("FAIL    %s:%d: page outside the PDF range (%s p.%s)" % (rel, ln, sig, bad[:3]))
                    continue
                cut = CUT.search(unit)
                text = unit[:cut.start()] if cut else unit
                for kind, val in items(text):
                    st = squash(norm(val))
                    checked += 1
                    per[sig][1] += 1
                    if any(st in pages[p] for p in pl):
                        if a.verbose:
                            print("OK      %s:%d: %s `%s` in %s p.%s" % (rel, ln, kind, val, sig, pl))
                        continue
                    nb = set()
                    for p in pl:
                        nb.update((p - 1, p + 1))
                    nb -= set(pl)
                    if any(st in pages.get(p, "") for p in nb):
                        near += 1
                        per[sig][2] += 1
                        print("NEAR    %s:%d: %s `%s` is not in %s p.%s but is on a neighboring page" % (rel, ln, kind, val, sig, pl))
                    else:
                        fail += 1
                        per[sig][3] += 1
                        print("FAIL    %s:%d: %s `%s` not found in %s p.%s" % (rel, ln, kind, val, sig, pl))
    for k, v in sorted(per.items()):
        print("  %s: citations=%d items=%d near=%d failures=%d" % (k, v[0], v[1], v[2], v[3]))
    print("Citations: %d; items checked: %d; near: %d; failures: %d" % (ncites, checked, near, fail))
    return 1 if (fail or (a.strict and near)) else 0


if __name__ == "__main__":
    sys.exit(main())
