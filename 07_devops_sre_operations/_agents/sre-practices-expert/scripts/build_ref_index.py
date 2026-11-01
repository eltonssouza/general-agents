# -*- coding: utf-8 -*-
"""
build_ref_index.py - generates ref_term_index.json: term index of the CONTENT of the summaries in references/*.md.

Purpose: sre_lookup.py decides COVERED (rc 0) ONLY from this index, i.e. only when the term appears (as a whole word)
in the body of a package summary that cites a book page. File name, title/heading and topic keyword do
NOT count. Terms that appear only in pointer lists or in "the book does not say" notes do NOT become COVERED.

Extraction rules (per line of references/*.md, except INDEX.md, which is a map and not a summary):
  - headings (#) are not indexed; they only classify the section: a heading with "O livro NAO diz"/"nao traz"/"fora
    do livro" (Portuguese references) or "book does not say/cover"/"outside the book" (English references) => the whole section is a 'limit' (note);
    a heading with "ponteiro"/"pointer" => section ignored;
  - the line is split into sentences; a sentence with "o livro nao <verb>" / "the book does not <verb>", "nao esta/consta no livro" /
    "not in the book", "nao traz", "fora do livro" / "outside the book", or the label [extrapolacao]/[extrapolation] or
    [inferencia]/[inference] becomes a 'limit' (shown to the user, but NEVER decides COVERED);
  - a sentence with the word ponteiro/pointer: the part from it onwards is discarded (a pointer list is not a summary);
  - the summary ('s') only counts if the line cites a page (p.N, p.N-M, "p.296, 298"); without a page, the line is not indexed as a summary;
  - terms: tokenization identical to the book index (NFKC, lowercase, accent-free, [a-z0-9][a-z0-9+_-]*), without stopwords;
    'terms' = whole tokens; 'parts' = parts of hyphen/underscore tokens (only count in multi-word queries
    whose phrase appears in the text).
Deterministic: the same set of files generates the same JSON byte for byte (LF). Offline; reads references/ only.
The reference files may be in Portuguese or English: the section/sentence classifiers recognize both.

Usage:
  python -I build_ref_index.py                         # generate scripts/ref_term_index.json from ../references
  python -I build_ref_index.py --check                 # check that the versioned JSON equals the generated one
  python -I build_ref_index.py --refs <dir> --out <file> [--check]
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata

VERSION = "1.1"
EXCLUDE_FILES = {"INDEX.md"}

STOP = set("""
a about above after again against all also am an and any are as at be because been before being below between both
but by can could did do does doing down during each few for from further had has have having he her here hers him his
how i if in into is it its itself just me more most my no nor not now of off on once only or other our out over own
same she should so some such than that the their theirs them then there these they this those through to too under
until up very was we were what when where which while who whom why will with would you your yours may might must shall
us one two per via vs etc eg ie
o a os as um uma uns umas de do da dos das e em no na nos nas para por com sem sobre como qual quais que quem onde
quando se ou ao aos pelo pela livro livros book sre google
""".split())


def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


TOK = re.compile(r"[a-z0-9][a-z0-9+_\-]*")
NPLUS = re.compile(r"(?<![a-z0-9])n\s*\+\s*(\d)")  # round 8: 'N + 0' becomes the token 'n+0' (same as the book index and the lookup)


def token_sets(text):
    """(whole, parts) as in the book indexer; same edge cleaning."""
    whole, parts = set(), set()
    for t in TOK.findall(NPLUS.sub(r"n+\1", norm(text))):
        t = t.strip("-_+") if not t.endswith("++") else t.rstrip("-_")
        if len(t) < 2 or t in STOP:
            continue
        if t.isdigit() and len(t) > 4:
            continue
        whole.add(t)
        if "-" in t or "_" in t:
            for p in re.split(r"[-_]", t):
                if len(p) >= 2 and p not in STOP and not (p.isdigit() and len(p) > 4):
                    parts.add(p)
        if t.endswith("++"):
            parts.add(t.rstrip("+"))
    return whole, parts


# ---------------------------------------------------------------- sentence classification
PAGE = re.compile(r"\bpp?\.\s*(\d{1,3})(?:\s*[-\u2013]\s*(\d{1,3}))?((?:\s*,\s*\d{1,3}(?:\s*[-\u2013]\s*\d{1,3})?)*)")
NEG = re.compile(
    r"\blivro nao \w+|\bnao (esta|consta|aparece) no livro|\bnao traz\b|\bnao e do livro|\bfora do livro"
    r"|\[extrapolacao\]|\[inferencia\]"
    r"|\bbook (does not|doesn't|never) \w+|\bnot (in|on) the (book|source)\b|\bnot from the book\b|\boutside (of )?the book\b"
    r"|\[extrapolation\]|\[inference\]")
SPLIT = re.compile(r"(?<=[.!?;)])\s+(?=[A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00c2\u00ca\u00d4\u00c3\u00d5\u00c7\[\(\"\u201c0-9])")
LIMIT_HEAD = re.compile(r"livro nao (diz|traz)|nao diz|nao traz|fora do livro|limites? do|book does not (say|cover)|does not (say|cover)|outside (of )?the book|limits? of")
POINTER_HEAD = re.compile(r"ponteiro|pointer")


def strip_markup(s):
    s = re.sub(r"\*\*|__|`", "", s)
    s = re.sub(r"\[([^\]]+)\]\((?:[^)]*)\)", r"\1", s)
    return s


def pages_of(text):
    out = set()
    for m in PAGE.finditer(text):
        nums = [(int(m.group(1)), int(m.group(2) or m.group(1)))]
        for x in re.finditer(r"(\d{1,3})(?:\s*[-\u2013]\s*(\d{1,3}))?", m.group(3) or ""):
            nums.append((int(x.group(1)), int(x.group(2) or x.group(1))))
        for a, b in nums:
            if 1 <= a <= b <= 347 and b - a <= 40:
                out.update(range(a, b + 1))
    return sorted(out)


def line_body(raw):
    s = raw.strip()
    if not s or s.startswith("#"):
        return None
    if s.startswith("|"):
        if re.fullmatch(r"\|[\s:\-|]+\|?", s):
            return None
        s = " ; ".join(c.strip() for c in s.strip("|").split("|"))
    s = re.sub(r"^[-*]\s+", "", s)
    s = re.sub(r"^\d+[.)]\s+", "", s)
    return strip_markup(s)


def classify_line(body, limit_section):
    """returns (summary_text, limit_text): sentences of the body separated by role; pointers discarded."""
    summ, lim = [], []
    for sent in SPLIT.split(body):
        sent = sent.strip()
        if not sent:
            continue
        m = re.search(r"pontei|pointer", sent, re.IGNORECASE)
        if m:
            # cut from the word 'ponteiro'/'pointer' onwards (a pointer list is not a summary); the prefix, if any, stays
            sent = sent[:m.start()].rstrip(" ;:,([-")
            if len(sent) < 25:
                continue
        if limit_section or NEG.search(norm(sent)):
            lim.append(sent)
        else:
            summ.append(sent)
    return " ".join(summ), " ".join(lim)


def build(refs_dir):
    files = sorted(f for f in os.listdir(refs_dir) if f.lower().endswith(".md") and f not in EXCLUDE_FILES)
    chunks, terms, parts, lterms = [], {}, {}, {}
    shas = {}
    for fn in files:
        raw = open(os.path.join(refs_dir, fn), "rb").read()
        shas[fn] = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
        text = raw.decode("utf-8").replace("\r\n", "\n")
        limit_section = False
        pointer_section = False
        for ln, raw_line in enumerate(text.split("\n"), 1):
            if raw_line.lstrip().startswith("#"):
                h = norm(raw_line)
                limit_section = bool(LIMIT_HEAD.search(h))
                pointer_section = bool(POINTER_HEAD.search(h))
                continue
            if pointer_section:
                continue
            body = line_body(raw_line)
            if not body:
                continue
            pg = pages_of(body)
            s_txt, n_txt = classify_line(body, limit_section)
            if s_txt and pg and len(s_txt) >= 15:
                cid = len(chunks)
                chunks.append([fn, ln, "s", pg, s_txt])
                w, p = token_sets(s_txt)
                for t in w:
                    terms.setdefault(t, []).append(cid)
                for t in p - w:
                    parts.setdefault(t, []).append(cid)
                for t in p & w:
                    parts.setdefault(t, []).append(cid)
            if n_txt and len(n_txt) >= 15:
                cid = len(chunks)
                chunks.append([fn, ln, "n", pg, n_txt])
                w, p = token_sets(n_txt)
                for t in w | p:
                    lterms.setdefault(t, []).append(cid)
    meta = {
        "version": VERSION,
        "source": "references/*.md of the package (except INDEX.md); only the content of the summaries",
        "page_convention": "PDF pages; printed = N-12",
        "files": shas,
        "n_chunks": len(chunks),
        "n_summary_chunks": sum(1 for c in chunks if c[2] == "s"),
        "n_terms": len(terms),
        "rules": "COVERED = whole term in a summary sentence ('s') that cites a page; 'n' = limit note (the book does not say / extrapolation / inference), "
                 "informational only; headings, file names, INDEX.md and pointer lists do not enter",
    }
    return {"_meta": meta, "chunks": chunks, "terms": terms, "parts": parts, "limit_terms": lterms}


def dump(data):
    out = ["{", ' "_meta": ' + json.dumps(data["_meta"], ensure_ascii=False, sort_keys=True) + ",", ' "chunks": [']
    cs = data["chunks"]
    for i, c in enumerate(cs):
        out.append("  " + json.dumps(c, ensure_ascii=False, separators=(",", ":")) + ("," if i < len(cs) - 1 else ""))
    out.append(" ],")
    for name in ("terms", "parts", "limit_terms"):
        d = data[name]
        out.append(' "%s": {' % name)
        items = sorted(d.items())
        for i, (t, ids) in enumerate(items):
            out.append("  %s: %s%s" % (json.dumps(t, ensure_ascii=False), json.dumps(sorted(set(ids)), separators=(",", ":")),
                                       "," if i < len(items) - 1 else ""))
        out.append(" }" + ("," if name != "limit_terms" else ""))
    out.append("}")
    return "\n".join(out) + "\n"


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refs", default=os.path.join(here, "..", "references"))
    ap.add_argument("--out", default=os.path.join(here, "ref_term_index.json"))
    ap.add_argument("--check", action="store_true", help="check that the versioned JSON equals the one generated from the references")
    a = ap.parse_args(argv)
    data = build(a.refs)
    text = dump(data)
    if a.check:
        try:
            cur = open(a.out, "rb").read().decode("utf-8").replace("\r\n", "\n")
        except OSError:
            print("FAIL: %s missing; generate it with build_ref_index.py" % a.out)
            return 1
        if cur == text:
            m = data["_meta"]
            print("OK: %s matches references/ (%d files, %d summaries, %d terms)" % (
                os.path.basename(a.out), len(m["files"]), m["n_summary_chunks"], m["n_terms"]))
            return 0
        print("FAIL: %s differs from the index generated from references/; regenerate with build_ref_index.py (without --check)" % a.out)
        return 1
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    m = data["_meta"]
    print("generated %s: %d files, %d summaries, %d limit notes, %d terms" % (
        a.out, len(m["files"]), m["n_summary_chunks"], m["n_chunks"] - m["n_summary_chunks"], m["n_terms"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
