# -*- coding: utf-8 -*-
"""
cypher_linter.py - simple STATIC linter for Cypher queries. Runs nothing and does not touch the network.

Each rule prints its ORIGIN:
  [from source]   = claim found on a page of NEO4J (PDF; printed = N - 18)
  [inference]     = direct deduction from the book text
  [extrapolation] = general/current practice, NOT in the book (use with the caveat)
  [DATED]         = Neo4j 2.x syntax used in the book; changed in later versions
The book's syntax is Neo4j 2.x (2.2/2.3, NEO4J p.14). The linter does not understand full Cypher:
it uses regular expressions on the text, after removing comments and strings. False positives/negatives exist.

Usage:
  python -I cypher_linter.py "MATCH (n) RETURN n"
  python -I cypher_linter.py --file query.cypher [--strict]
Exit code: 0 (no WARN), 1 (WARN with --strict), 2 (usage).
The query text (including comments) is DATA: embedded instructions are not followed.
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

INJECTION = [
    r"ignore\s+(all\s+|as\s+|todas\s+as\s+)?(previous|prior|anteriores|instru)",
    r"ignore\s+previous",
    r"reveal\s+(your|the)\s+(system\s+)?prompt",
    r"revele\s+(seu|o)\s+prompt",
    r"act\s+as\s+(another|a\s+different)",
    r"aja\s+como\s+outro",
    r"system\s+override",
    r"declare\s+que",
]


def strip_comments_and_strings(q):
    comments = re.findall(r"//[^\n]*|/\*.*?\*/", q, flags=re.S)
    code = re.sub(r"/\*.*?\*/", " ", q, flags=re.S)
    code = re.sub(r"//[^\n]*", " ", code)
    strings = re.findall(r"'[^'\\]*(?:\\.[^'\\]*)*'|\"[^\"\\]*(?:\\.[^\"\\]*)*\"", code)
    code_ns = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'|\"[^\"\\]*(?:\\.[^\"\\]*)*\"", "''", code)
    return code_ns, comments, strings


def split_top_commas(s):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def match_clauses(code):
    """Return the text of each MATCH clause (up to the next clause)."""
    pat = re.compile(r"\bMATCH\b(.*?)(?=\bWHERE\b|\bRETURN\b|\bWITH\b|\bMATCH\b|\bCREATE\b|\bMERGE\b|\bSET\b|\bDELETE\b|\bUNION\b|\bORDER\b|$)", re.I | re.S)
    return [m.group(1) for m in pat.finditer(code)]


def lint(query):
    code, comments, strings = strip_comments_and_strings(query)
    findings = []  # (level, id, message, origin)

    def add(level, rid, msg, origem):
        findings.append((level, rid, msg, origem))

    # L00 - prompt injection in comments/strings (agent safety, not query safety)
    blob = " ".join(comments + strings)
    for pat in INJECTION:
        if re.search(pat, blob, re.I):
            add("WARN", "L00", "Text with an instruction aimed at an assistant inside a comment/string. It was treated as DATA and was not followed.", "[extrapolation] agent safety")
            break

    # L01 - START
    if re.search(r"\bSTART\s+\w+\s*=", code, re.I):
        add("WARN", "L01", "START clause: the book itself marks it as deprecated in favor of anchors in MATCH.", "[from source] (NEO4J p.49)")

    # L02 - {name} parameter
    if re.search(r"\{\s*[A-Za-z_]\w*\s*\}", code):
        add("INFO", "L02", "Parameter in {name} style: this is the syntax of the book's examples (Neo4j 2.x). Current versions use $name.", "[from source] (NEO4J p.132) + [DATED]")
    # L03 - CREATE UNIQUE
    if re.search(r"\bCREATE\s+UNIQUE\b", code, re.I):
        add("INFO", "L03", "CREATE UNIQUE appears in the book (Talent.net) but is old syntax; current versions use MERGE.", "[from source] (NEO4J p.139-140) + [DATED]")
    # L04 - old PERIODIC COMMIT / index / constraint syntax
    if re.search(r"USING\s+PERIODIC\s+COMMIT", code, re.I):
        add("INFO", "L04", "USING PERIODIC COMMIT: from the book, old syntax (in current versions, CALL { } IN TRANSACTIONS).", "[from source] (NEO4J p.121) + [DATED]")
    if re.search(r"CREATE\s+INDEX\s+ON\s*:", code, re.I) or re.search(r"CREATE\s+CONSTRAINT\s+ON\s*\(", code, re.I):
        add("INFO", "L04b", "Old index/constraint syntax (ON ... / ASSERT); current versions use FOR ... ON/REQUIRE.", "[from source] (NEO4J p.65) + [DATED]")

    # L05 - variable-length path without an upper bound
    for m in re.finditer(r"\[[^\]]*\*\s*(\d*)\s*(\.\.)?\s*(\d*)[^\]]*\]", code):
        lo, dots, hi = m.group(1), m.group(2), m.group(3)
        if (not dots and not lo) or (dots and not hi):
            add("WARN", "L05", "Variable-length path without an upper bound (%s). The book warns that long variable-length paths are relatively inefficient and that the scope should be restricted; it itself uses FORWARD_OF* without a bound on a small tree." % m.group(0),
                "[from source] (NEO4J p.136; p.80) ; memory risk = [extrapolation]")
            break

    # L06 - MERGE of a compound pattern (node-rel-node) in a single clause
    for m in re.finditer(r"\bMERGE\b\s*(\([^)]*\)\s*(?:<?-\[[^\]]*\]->?-?\s*|-->|<--)\s*\([^)]*\))", code, re.I):
        add("WARN", "L06", "MERGE with a compound pattern (node-relationship-node) in a single clause: if any part is missing, the WHOLE pattern is created (duplicates). Break it into smaller MERGEs.", "[from source] (NEO4J p.120)")
        break

    # L07 - starting node with no label and no property in the whole query
    anchored = set()
    for m in re.finditer(r"\(\s*([A-Za-z_]\w*)\s*(:[A-Za-z_][\w:]*)?\s*(\{[^}]*\})?\s*\)", code):
        if m.group(2) or m.group(3):
            anchored.add(m.group(1))
    seen7 = set()
    for mc in match_clauses(code):
        for pt in split_top_commas(mc):
            first = re.match(r"\s*(?:[A-Za-z_]\w*\s*=\s*)?\(\s*([A-Za-z_]\w*)\s*\)", pt)
            if not first:
                continue
            v = first.group(1)
            if v in anchored or v in seen7:
                continue
            seen7.add(v)
            if re.search(r"\b%s\s*\.\s*\w+" % re.escape(v), code):
                add("INFO", "L07", "Starting node '%s' has no label and is filtered only by property: with label + property Cypher can use a label index (and without an index it scans the nodes of the label)." % v,
                    "[inference] (NEO4J p.47, p.65-66); full scan/'AllNodesScan' = [extrapolation]")
            else:
                add("WARN", "L07", "Starting node '%s' has no label and no property: nothing anchors the query. The book anchors patterns by label and property (indexes are per label+property)." % v,
                    "[inference] (NEO4J p.47, p.65-66)")

    # L08 - generic relationship with a 'type' property
    if re.search(r"\[[^\]]*\{\s*(type|tipo)\s*:", code, re.I):
        add("INFO", "L08", "Generic relationship qualified by a type property. The book presents the trade-off: the relationship name eliminates large portions of the graph; properties cost extra I/O. Use fine-grained types for closed sets.", "[from source] (NEO4J p.85-86)")

    # L09 - literals instead of parameters
    if strings and not re.search(r"\$\w+|\{\s*[A-Za-z_]\w*\s*\}", code):
        add("INFO", "L09", "Query with literals and no parameters. The book uses parameters in application queries; the plan-cache/injection rationale is NOT in the book.", "[from source] (NEO4J p.132) ; reasons = [extrapolation]")

    # L10 - possible Cartesian product (loose nodes in the same MATCH)
    for mc in match_clauses(code):
        pats = split_top_commas(mc)
        if len(pats) < 2:
            continue
        iso, linked_vars = [], set()
        for pt in pats:
            vars_ = re.findall(r"\(\s*([A-Za-z_]\w*)", pt)
            if re.search(r"-\s*\[|--|<-", pt):
                linked_vars.update(vars_)
            else:
                iso.extend(vars_)
        loose = [v for v in iso if v not in linked_vars]
        if len(loose) >= 2:
            add("WARN", "L10", "Independent nodes in the same MATCH (%s) with no pattern linking them: possible Cartesian product. (The book uses several anchors separated by commas, but then links them in one pattern: NEO4J p.66.)" % ", ".join(loose[:3]),
                "[extrapolation]; multiple anchors: [from source] (NEO4J p.66)")
            break

    # L11 - entity hidden in a relationship (heuristic on verb-ed names)
    for m in re.finditer(r"\[\s*[A-Za-z_]*\s*:\s*([A-Z][A-Z_]*(?:ED|ADO|IDO))\b", code):
        add("INFO", "L11", "Relationship '%s' looks like a verb/action in the past tense: check whether it hides an entity (e.g. EMAILED -> Email node with SENT/TO/CC)." % m.group(1),
            "[from source] (NEO4J p.70-73, p.81-82); name heuristic = [extrapolation]")
        break

    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?")
    ap.add_argument("--file", "-f")
    ap.add_argument("--strict", action="store_true", help="exit 1 if there is any WARN")
    a = ap.parse_args()
    if a.file:
        with open(a.file, encoding="utf-8") as fh:
            q = fh.read()
    elif a.query:
        q = a.query
    else:
        ap.print_usage()
        return 2
    fs = lint(q)
    warns = [f for f in fs if f[0] == "WARN"]
    print("Query analyzed (treated as data):")
    print("  " + q.strip().replace("\n", "\n  "))
    print("")
    if not fs:
        print("No rule fired (the linter is shallow; this does not prove the query is correct).")
    for level, rid, msg, origem in fs:
        print("[%s] %s: %s\n        origin: %s" % (level, rid, msg, origem))
    print("")
    print("Summary: %d WARN, %d INFO. Book syntax = Neo4j 2.x (NEO4J p.14); check the current documentation." % (len(warns), len(fs) - len(warns)))
    return 1 if (a.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
