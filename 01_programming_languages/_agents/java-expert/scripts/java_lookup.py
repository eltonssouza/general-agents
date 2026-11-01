#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Looks up a topic in the java-expert package collection (read-only, no network, standard library).

Usage:
    python -I scripts/java_lookup.py TERM [TERM ...]       # topics whose alias contains all the terms
    python -I scripts/java_lookup.py --list                # lists the index topics
    python -I scripts/java_lookup.py --json TERM           # JSON output

For each topic it shows: which references to open (references/*.md, with the section), which PDF pages the sources
devote to the subject (Think, Adv, JVM; PDF page, not the printed one) and the era of the source.
If the topic is on the "not covered" list or matches nothing, the output starts with "NOT COVERED": the collection
does not cover the subject (this does NOT prove the subject does not exist in Java; only that the package's sources do not treat it).

The index (scripts/java_index.json) is curated by the package: each topic has anchors (term + page) checked by
tests/verify_citations.py. The aliases in Portuguese and English are the package's own [extrapolation]: they serve to find
the topic and are not the books' vocabulary (Portuguese aliases are kept so that Portuguese queries keep working).
To find out in which JDK a JEP shipped use skills/java-jdk-features/scripts/jdk_lookup.py.
Exit code: 0 if it ran; 2 for a usage error.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
NOMES = {"Think": "Think Java 6.1.3", "Adv": "Advanced Java", "JVM": "JVM Troubleshooting Handbook", "RN": "OpenJDK release notes"}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def load():
    with open(os.path.join(HERE, "java_index.json"), encoding="utf-8") as fh:
        return json.load(fh)


def palavra(t, campo):
    """True if the term (one or more words) appears in the field as a whole word (avoids 'record' in 'recorder')."""
    return re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", campo) is not None


def casa(termos, aliases, titulo=""):
    campos = [norm(a) for a in aliases] + [norm(titulo)]
    frase = " ".join(termos)
    if any(palavra(frase, c) for c in campos):
        return True
    return all(any(palavra(t, c) for c in campos) for t in termos)


def fmt_pages(pgs):
    out = []
    for p in pgs:
        if p["sig"] == "RN":
            out.append("(RN %s)" % p["pages"])
        else:
            out.append("(%s p.%s)" % (p["sig"], p["pages"].replace("-", "–")))
    return "; ".join(out)


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    data = load()
    if a.list:
        print("# Index topics (%d) and topics declared NOT COVERED (%d)" % (len(data["entries"]), len(data["no_coverage"])))
        for e in data["entries"]:
            print("- %s: %s %s" % (e["id"], e["titulo"], fmt_pages(e["pages"])))
        print("## NOT COVERED (declared)")
        for n in data["no_coverage"]:
            print("- %s: %s" % (n["id"], ", ".join(n["aliases"][:4])))
        return 0
    if not a.terms:
        print("error: provide a topic (e.g. 'deadlock', 'equals', 'scanner'), --list or --json", file=sys.stderr)
        return 2
    termos = [norm(t) for t in a.terms]
    # a declared 'not covered' entry takes priority: the term may be in an alias of a topic covered only in part
    nc = [n for n in data["no_coverage"] if casa(termos, n["aliases"])]
    hits = [e for e in data["entries"] if casa(termos, e["aliases"], e["titulo"])]
    if a.json:
        json.dump(dict(termos=a.terms, sem_cobertura=nc, temas=hits, cobertura=bool(hits)), sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    if nc:
        for n in nc:
            print("NOT COVERED (declared): %s" % ", ".join(a.terms))
            print("  reason: %s" % n["motivo"])
            if n["ver"]:
                print("  see also: %s (JEP number and title only)" % n["ver"])
    if hits:
        if nc:
            print("\nThe collection treats this only partially or tangentially; related topics:")
        print("# %d topic(s) for %s" % (len(hits), a.terms))
        for e in hits:
            print("- %s %s" % (e["titulo"], e["rotulo"]))
            print("    PDF pages: %s" % fmt_pages(e["pages"]))
            print("    open: %s" % "; ".join(e["refs"]))
            if e["nota"]:
                print("    note: %s" % e["nota"])
        print("\nPages = PDF numbering (convention in references/INDEX.md). Era marks: [introductory]=Think (Java SE 8),")
        print("[advanced]=Adv (Java 7/8), [DATED]=tied to Java 8 or to PermGen. Check the page in the PDF before citing.")
    elif not nc:
        print("NOT COVERED in the package index for %s." % a.terms)
        print("This does NOT prove the subject does not exist in Java; only that the sources (Think, Adv, JVM Handbook, JEP titles) do not")
        print("treat it or that the index does not map it. Before saying 'the book does not say', search references/ and check the source.")
        print("Knowledge from outside the sources must be labeled [extrapolation].")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
