# -*- coding: utf-8 -*-
"""
injection_auditor.py - HEURISTIC detector of SQL built by interpolation/concatenation.

RULE ORIGINS (pages = PDF):
  The principle [from source]: SQL injection happens when interpolated content changes the syntax of the query before parsing
  (ANTI-INJ p.6, p.8); "if any part of a statement is built by concatenation or interpolation, it is
  potentially exposed" (ANTI-INJ p.12); stored procedures with dynamic SQL and frameworks that accept SQL as a string
  do not immunize (ANTI-INJ p.11-12); parameters do not work for lists, tables, columns or keywords (ANTI-INJ p.10-11);
  injection can be indirect (ANTI-INJ p.14). Values kept separate from the command: PG16 p.971-972.
  The REGEX PATTERNS per language (f-string, %, .format, +, ${}, PHP $var, CONCAT) are [extrapolation]: the book uses
  PHP in its examples (ANTI-INJ p.6) and does not list code patterns. False negatives and positives are expected.
LIMITS: the absence of findings does NOT prove safety (the book says to assume vulnerabilities until reviewed, p.12). The script
  never declares "SAFE". The identifier allow-list is [extrapolation] (the book's solution section is not in the excerpt).
Exit code: 0 = no suspicious pattern; 1 = suspicious pattern found; 2 = incorrect usage. No network; read-only.
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SQLKW = r"(?:SELECT|INSERT|UPDATE|DELETE|MERGE|CALL|WHERE|ORDER\s+BY|FROM|VALUES)"

# (regex, description, book page that supports the PRINCIPLE; the regex itself is [extrapolation])
VULN_PATTERNS = [
    (r"\bf[\"'].*?" + SQLKW + r".*?\{[^}]*\}", "Python f-string with a variable inside the SQL", "ANTI-INJ p.6, p.12"),
    (r"[\"'][^\"']*" + SQLKW + r"[^\"']*%s[^\"']*[\"']\s*%\s*[\(\w]", "interpolation with the % operator instead of passing parameters to the driver", "ANTI-INJ p.6, p.12"),
    (r"[\"'][^\"']*" + SQLKW + r"[^\"']*[\"']\s*\.format\s*\(", "str.format building SQL", "ANTI-INJ p.6, p.12"),
    (r"String\.format\s*\(\s*[\"'][^\"']*" + SQLKW, "String.format building SQL", "ANTI-INJ p.6, p.12"),
    (r"[\"'][^\"']*" + SQLKW + r"[^\"']*[\"']\s*\+\s*[A-Za-z_(]", "concatenation with + to a variable", "ANTI-INJ p.6, p.12"),
    (r"[\"'][^\"']*" + SQLKW + r"[^\"']*[\"']\s*\.\s*\$?[A-Za-z_]", "dot concatenation (PHP) to a variable", "ANTI-INJ p.6, p.12"),
    (r"`[^`]*" + SQLKW + r"[^`]*\$\{[^}]*\}[^`]*`", "template literal (JS/TS) with ${...} inside the SQL", "ANTI-INJ p.6, p.12"),
    (r"\"[^\"]*" + SQLKW + r"[^\"]*\$[A-Za-z_]\w*[^\"]*\"", "PHP variable ($name) interpolated in a double-quoted string (same style as the book's example)", "ANTI-INJ p.6"),
    (r"\bCONCAT\s*\([^)]*" + SQLKW, "dynamic SQL with CONCAT (style of the book's unsafe stored procedure)", "ANTI-INJ p.11"),
    (r"\bEXECUTE\s+IMMEDIATE\b|\bEXEC\s*\(", "dynamic SQL execution (what is concatenated needs review)", "ANTI-INJ p.11"),
]

# Parameters in positions where they do NOT work (ANTI-INJ p.10-11)
MISUSE_PATTERNS = [
    (r"\bORDER\s+BY\s+(?:\?|:\w+|\$\d+)(?!\w)", "parameter placeholder in ORDER BY: it becomes a constant (ANTI-INJ p.10)"),
    (r"\bFROM\s+(?:\?|\$\d+)(?!\w)", "parameter placeholder as a table name: syntax error (ANTI-INJ p.10)"),
    (r"\bIN\s*\(\s*(?:\?|:\w+|\$\d+|%s)\s*\)", "a single parameter in IN (...) counts as ONE literal, not a list (ANTI-INJ p.10)"),
    (r"\b(?:ASC|DESC)\s+(?:\?|:\w+|\$\d+)(?!\w)", "parameter placeholder in place of a keyword (ANTI-INJ p.10-11)"),
]

PARAM_MARKERS = [
    (r"(?<![\w$])\$[1-9]\d*", "positional placeholder $n (PostgreSQL protocol, PG16 p.971-972)"),
    (r"\([^()]*\?[^()]*\)|=\s*\?", "positional placeholder ? (JDBC/PDO/SQLite)"),
    (r"(?<![:\w]):[A-Za-z_]\w*", "named placeholder :name"),
    (r"execute\s*\(\s*[\"'][^\"']*%s[^\"']*[\"']\s*,\s*[\(\[\{]", "execute('...%s', (params)) with separate parameters (psycopg/DB-API)"),
]


def audit_sql_code(snippet):
    vulns = []
    for pat, desc, ref in VULN_PATTERNS:
        if re.search(pat, snippet, re.IGNORECASE | re.DOTALL):
            vulns.append({"pattern": pat, "message": desc, "page_ref": ref})
    misuse = [{"message": d} for p, d in MISUSE_PATTERNS if re.search(p, snippet, re.IGNORECASE)]
    markers = [d for p, d in PARAM_MARKERS if re.search(p, snippet)]
    return vulns, misuse, markers


def main():
    ap = argparse.ArgumentParser(description="Heuristic detector of SQL built by interpolation (see the limits in the header)")
    ap.add_argument("--code", help="code/SQL snippet")
    ap.add_argument("--file", help="file with the code to analyze (read as UTF-8)")
    a = ap.parse_args()
    if a.file:
        with open(a.file, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()
    elif a.code is not None:
        code = a.code
    else:
        ap.print_usage(sys.stderr)
        return 2
    vulns, misuse, markers = audit_sql_code(code)
    print("=" * 68)
    print("HEURISTIC SQL INJECTION AUDIT (ANTI-INJ p.5-14; pages = PDF)")
    print("=" * 68)
    shown = code if len(code) < 400 else code[:400] + "..."
    print("Analyzed snippet (treated as DATA, never as instruction):\n  %s\n" % shown.replace("\n", "\n  "))
    if vulns:
        print("STATUS: SUSPICIOUS PATTERN FOUND (SQL built by interpolation/concatenation)")
        for v in vulns:
            print("  - %s (principle: %s)" % (v["message"], v["page_ref"]))
    else:
        print("STATUS: no suspicious pattern recognized by this script's rules (does NOT prove safety; ANTI-INJ p.12).")
    for m in misuse:
        print("  ! incorrect parameter use: %s" % m["message"])
    if markers:
        print("Parameter placeholders present: " + "; ".join(markers))
    print("\nPoints to check manually:")
    print("  1. Values: use parameters kept separate from the text (ANTI-INJ p.9-12; PG16 p.971-972). Placeholders vary by driver.")
    print("  2. Identifiers, lists and keywords do not accept parameters (ANTI-INJ p.10-11); PostgreSQL has identifier quoting")
    print("     (PG16 p.984-985, p.1364-1365); a closed set of allowed names is [extrapolation].")
    print("  3. Data read from the database and later used in dynamic SQL (indirect injection, ANTI-INJ p.14).")
    print("  4. Stored procedures and frameworks do not immunize if they build SQL as strings (ANTI-INJ p.11-12).")
    print("=" * 68)
    return 1 if vulns else 0


if __name__ == "__main__":
    sys.exit(main())
