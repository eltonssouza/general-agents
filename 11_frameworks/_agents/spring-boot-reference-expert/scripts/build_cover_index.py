# -*- coding: utf-8 -*-
"""
build_cover_index.py - generates scripts/sbr_cover.json, the package SUMMARY INDEX.

Purpose: sbr_lookup.py only answers LEVEL: COVERED when the queried term appears, as a WHOLE TERM or CONTIGUOUS PHRASE,
in the BODY of the summaries in references/*.md (never in the Reference source text, never by part of a word).
This index is generated only from the content of the references (it does not read the PDF or extracted text).

Indexed lines (those that can "cover"): headings (#) and summary lines that cite a page ("p.N"), plus fenced code blocks
that inherit the citation of the previous paragraph. INDEX.md is left out (it is a map, not a summary).
For each line it stores:
  i = "file:line"   p = cited pages ("87-88,100")   t = all tokens of the line   d = tokens of the DELIMITED fragments
Delimited fragment = `backticks`, **bold**, *italic*, "quotes" or heading. A plain common word loose in prose (e.g. "record" in
the middle of a sentence) stays only in t and does NOT cover on its own; an identifier (with . - _ # @ = :, digit or camelCase) and a phrase of 2+
words cover in t; a plain common word covers only in d.
Tokens: lowercase; whole token = [a-z0-9]+ with internal separators . _ - (e.g. git.commit.time is ONE token).

Usage: python -I scripts/build_cover_index.py [--check]   (--check only verifies the file is up to date; exit 1 if not)
Stdlib only.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.join(os.path.dirname(HERE), "references")
OUT = os.path.join(HERE, "sbr_cover.json")
TOKEN = re.compile(r"[a-z0-9]+(?:[._\-][a-z0-9]+)*")
LABEL = re.compile(r"\[(?:do livro[^\]]*|from source[^\]]*|infer[êe]ncia|inference|extrapola[çc][ãa]o|extrapolation|DATADO|DATED)\]", re.I)  # Portuguese labels (older references) and English ones
PAGE = re.compile(r"p\.\s?(\d+(?:\s?[-–]\s?\d+)?(?:\s*,\s*\d+(?:\s?[-–]\s?\d+)?)*)")
SPANS = [
    re.compile(r"`([^`]+)`"),
    re.compile(r"\*\*(.+?)\*\*"),
    re.compile(r"(?<![*\w])\*(?!\*)([^*\n]+?)(?<!\*)\*(?![*\w])"),
    re.compile(r'"([^"\n]+)"'),
    re.compile(r"“([^”\n]+)”"),
]


def norm_text(s):
    s = s.lower()
    for a in ("‘", "’", "“", "”"):
        s = s.replace(a, "'")
    for a in ("‐", "‑", "–", "—", "−"):
        s = s.replace(a, "-")
    return s.replace("\xa0", " ")


def tokenize(s):
    """whole tokens (shared with sbr_lookup.py)."""
    return TOKEN.findall(norm_text(s))


def cited_pages(line):
    out = []
    for m in PAGE.finditer(line):
        for part in re.split(r"\s*,\s*", m.group(1)):
            out.append(re.sub(r"\s", "", part.replace("–", "-")))
    seen = []
    for p in out:
        if p not in seen:
            seen.append(p)
    return ",".join(seen)


def delimited_text(line):
    parts = []
    for rx in SPANS:
        for m in rx.finditer(line):
            g = m.group(1)
            if g.lstrip().startswith("["):  # labels **[from source]**
                g = LABEL.sub(" ", g)
            parts.append(g)
    return " ".join(parts)


def build():
    lines = []
    h = hashlib.sha256()
    for fp in sorted(glob.glob(os.path.join(REFS, "*.md"))):
        name = os.path.basename(fp)
        if name.upper().startswith("INDEX"):
            continue
        raw = open(fp, "rb").read()
        h.update(name.encode("utf-8") + b"\0" + raw)
        src = raw.decode("utf-8").splitlines()
        infence = False
        last_cited = False
        last_pages = ""
        for n, ln in enumerate(src, 1):
            if ln.strip().startswith("```"):
                infence = not infence
                continue
            if infence:
                if last_cited:
                    lines.append([name + ":%d" % n, last_pages, " ".join(tokenize(ln)), ""])
                continue
            heading = ln.startswith("#")
            pages = cited_pages(ln)
            last_cited = bool(pages)
            last_pages = pages
            if not (heading or pages):
                continue
            body = LABEL.sub(" ", ln)
            t = " ".join(tokenize(body))
            d = " ".join(tokenize(body.lstrip("# "))) if heading else " ".join(tokenize(delimited_text(ln)))
            lines.append([name + ":%d" % n, pages, t, d])
    return {"fonte": "references/*.md (except INDEX.md); only the content of the package summaries", "sha": h.hexdigest(), "linhas": lines}


def refs_sha():
    h = hashlib.sha256()
    for fp in sorted(glob.glob(os.path.join(REFS, "*.md"))):
        name = os.path.basename(fp)
        if name.upper().startswith("INDEX"):
            continue
        h.update(name.encode("utf-8") + b"\0" + open(fp, "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    data = build()
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if a.check:
        try:
            cur = open(OUT, "r", encoding="utf-8").read()
        except OSError:
            cur = ""
        ok = cur == text
        print("sbr_cover.json %s" % ("up to date" if ok else "OUT OF DATE: run scripts/build_cover_index.py"))
        return 0 if ok else 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("lines=%d -> %s (%d bytes)" % (len(data["linhas"]), OUT, os.path.getsize(OUT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
