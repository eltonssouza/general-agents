#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_php_smells.py - simple (heuristic, line-by-line) checklist/linter for PHP code.
Read-only, no network, stdlib. NOT a full static analysis: it produces false positives and negatives.

Each rule declares its ORIGIN:
  book          = the recommendation is in the PRW (PDF page given)
  inference     = direct deduction from a point in the book (page given)
  extrapolation = common practice NOT present in the PRW (do not cite as [from source])

Usage:
  python -I scan_php_smells.py file.php [more.php ...]
  python -I scan_php_smells.py --code '<?php echo $_GET["x"];'
  python -I scan_php_smells.py --rules            # list the rules and their origin
  python -I scan_php_smells.py --only-livro f.php # only rules with origin book/inference (alias: --only-book)
  python -I scan_php_smells.py --json f.php
Output: 0 = nothing found; 1 = findings; 2 = usage/file error.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ESC = r"(?:htmlspecialchars|htmlentities|strip_tags|filter_var|filter_input|intval|\(int\)|escapeshellarg|->escape)"

# (id, name, regex, level, origin, page, description, 'sem' = regex that, if present on the SAME line, cancels the finding)
RULES = [
    ("PHP-MYSQL", "mysql_* extension (removed in PHP 7.0)",
     r"\bmysql_(?:connect|pconnect|query|select_db|fetch_\w+|real_escape_string|num_rows|close)\s*\(",
     "HIGH", "book", "p.42",
     "Migrate to PDO or mysqli; do not just find-and-replace mysql_*->mysqli_* (you lose parameter binding).", None),
    ("PHP-SQLI", "SQL built with a variable (SQL Injection risk)",
     r"(?:->|::)\s*(?:query|exec|prepare)\s*\(\s*(?:\"[^\"]*\$\w+|'[^']*'\s*\.\s*\$|\"[^\"]*\"\s*\.\s*\$)"
     r"|(?:SELECT\s.+\sFROM|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM)[^;]*(?:\.\s*\$|\{?\$\w+)",
     "HIGH", "book", "p.43-44",
     "Use prepare() with placeholders and bound parameters (bindParam/execute) and filter the input first.", None),
    ("PHP-XSS", "external input printed without escaping (XSS risk)",
     r"(?:\becho\b|\bprint\b|<\?=)[^;?]*\$_(?:GET|POST|REQUEST|COOKIE)\b",
     "HIGH", "book", "p.59",
     "Sanitize before output: htmlspecialchars($x, ENT_QUOTES, 'UTF-8') (example p.25), htmlentities or strip_tags.", ESC),
    ("PHP-PASSHASH", "fast general-purpose hash for a password (md5/sha1/sha256...)",
     r"\b(?:md5|sha1|crc32)\s*\([^)]*(?:pass|senha|pwd)|\bhash\s*\(\s*['\"]sha\w*['\"]\s*,[^)]*(?:pass|senha|pwd)",
     "HIGH", "inference", "p.57",
     "The book says to use a specialized password algorithm, not a fast general-purpose hash (it cites SHA256); use password_hash()/password_verify() (p.58). md5/sha1 are not named in the book: the conclusion is an inference.", None),
    ("PHP-UNSERIALIZE", "unserialize() of possibly external data",
     r"\bunserialize\s*\(\s*\$_(?:GET|POST|REQUEST|COOKIE)|\bunserialize\s*\(\s*\$(?:data|input|payload|body)\b",
     "HIGH", "book", "p.60",
     "Untrusted data can instantiate objects with destructors; prefer JSON (json_decode/json_encode).", None),
    ("PHP-SHELL", "shell command with a variable and no escapeshellarg",
     r"\b(?:exec|shell_exec|system|passthru|popen|proc_open)\s*\([^)]*\$",
     "HIGH", "book", "p.59",
     "Command arguments coming from input must go through escapeshellarg() (and the book says this is 'usually a bad idea').", r"escapeshellarg"),
    ("PHP-INCLUDE", "include/require with a path coming from external input",
     r"\b(?:include|require)(?:_once)?\s*\(?\s*[^;]*\$_(?:GET|POST|REQUEST|COOKIE)\b",
     "HIGH", "book", "p.59",
     "A file path derived from input can be manipulated (../, null bytes): validate it and strip dangerous characters.", None),
    ("PHP-ERRDISPLAY", "display_errors turned on in code",
     r"ini_set\s*\(\s*['\"]display_errors['\"]\s*,\s*(?:1|true|['\"](?:1|on|true)['\"])",
     "MEDIUM", "book", "p.61-62",
     "In production the book says display_errors = Off and log_errors = On; on only in development.", None),
    ("PHP-SUPPRESS", "@ suppression operator",
     r"(?<![\w\"'@.\-])@\s*(?:\$|[A-Za-z_\\]\w*\s*\()",
     "MEDIUM", "book", "p.52-53",
     "The @ swallows the error (no screen, no log), costs performance and cannot be turned off in production; avoid it (e.g. $a['k'] ?? '').", None),
    ("PHP-UTF8-DSN", "DSN with charset utf8 (not utf8mb4)",
     r"charset\s*=\s*utf8(?![mM][bB]4)",
     "MEDIUM", "book", "p.23",
     "For full UTF-8 in MySQL use utf8mb4 in the database, tables and PDO DSN.", None),
    ("PHP-REGGLOBALS", "extract() over a superglobal (register_globals effect)",
     r"\bextract\s*\(\s*\$_(?:GET|POST|REQUEST|COOKIE)",
     "HIGH", "inference", "p.60-61",
     "The book describes the register_globals risk ($_GET['foo'] becoming $foo and overwriting variables); extract() of a superglobal reproduces the effect.", None),
    ("PHP-MB", "non-multibyte string function (informational)",
     r"\b(?:strlen|substr|strpos|strtolower|strtoupper)\s*\(",
     "INFO", "book", "p.22",
     "If the string can be UTF-8, use the mb_* counterparts (mb_strlen, mb_substr, ...). Ignore if it is ASCII/binary text.", None),
    ("PHP-STRICT", "file without declare(strict_types=1)",
     "__FILE__", "INFO", "extrapolation", "-",
     "NOT in the PRW. Common PHP 7+ practice: declare(strict_types=1) at the top avoids silent coercion of scalar types.", None),
    ("PHP-CLOSETAG", "closing tag ?> at the end of a PHP-only file",
     "__EOF__", "INFO", "extrapolation", "-",
     "NOT in the PRW. PSR-1/PSR-12 omit the final ?> to avoid accidental output; see php-fig.org.", None),
    ("PHP-DATETIME", "new DateTime( (mutable)",
     r"\bnew\s+DateTime\s*\(",
     "INFO", "extrapolation", "-",
     "NOT in the PRW (the book uses DateTime, p.20-21). In new code many prefer DateTimeImmutable to avoid shared mutation.", None),
]


def is_comment(line):
    s = line.strip()
    return s.startswith(("//", "#", "*", "/*"))


def scan(code, name="<buffer>", only_book=False):
    out = []
    lines = code.splitlines()
    for rid, title, rx, level, origin, page, desc, anul in RULES:
        if only_book and origin == "extrapolation":
            continue
        if rx == "__FILE__":
            if "<?php" in code and not re.search(r"declare\s*\(\s*strict_types\s*=\s*1\s*\)", code):
                out.append(dict(file=name, line=1, id=rid, title=title, level=level, origin=origin,
                                page=page, text="<?php", detail=desc))
            continue
        if rx == "__EOF__":
            body = code.rstrip("\n\r ")
            if "<?php" in code and body.endswith("?>"):
                out.append(dict(file=name, line=len(lines), id=rid, title=title, level=level, origin=origin,
                                page=page, text="?>", detail=desc))
            continue
        cre = re.compile(rx, re.IGNORECASE)
        for i, line in enumerate(lines, 1):
            if is_comment(line):
                continue
            m = cre.search(line)
            if not m:
                continue
            if anul and re.search(anul, line, re.IGNORECASE):
                continue
            out.append(dict(file=name, line=i, id=rid, title=title, level=level, origin=origin,
                            page=page, text=line.strip()[:120], detail=desc))
    out.sort(key=lambda f: (f["file"], f["line"], f["id"]))
    return out


def label(f):
    if f["origin"] == "book":
        return f"[from source] (PRW {f['page']})"
    if f["origin"] == "inference":
        return f"[inference] (basis: PRW {f['page']})"
    return "[extrapolation] (outside the PRW)"


def main():
    ap = argparse.ArgumentParser(description="Heuristic checklist/linter for PHP with the origin of each rule.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--code", "-c")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--only-livro", "--only-book", dest="only_book", action="store_true", help="omit rules with extrapolation origin")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.rules:
        for rid, title, _rx, level, origin, page, _d, _a in RULES:
            print(f"{rid:<16} {level:<6} {origin:<13} PRW {page:<7} {title}")
        return 0

    sources = []
    if a.code is not None:
        sources.append(("<inline>", a.code))
    for p in a.files:
        if not os.path.isfile(p):
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 2
        with open(p, encoding="utf-8", errors="replace") as f:
            sources.append((p, f.read()))
    if not sources:
        if sys.stdin.isatty():
            ap.print_help()
            return 2
        sources.append(("<stdin>", sys.stdin.read()))

    findings = []
    for name, code in sources:
        findings += scan(code, name, a.only_book)
    if a.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return 1 if findings else 0
    if not findings:
        print("No findings by the heuristic rules (this does NOT prove the code is safe).")
        return 0
    print(f"{len(findings)} finding(s) (heuristic; confirm in the code):\n")
    for f in findings:
        print(f"[{f['level']}] {f['id']} {f['title']}  ({f['file']}:{f['line']})")
        print(f"   snippet: {f['text']}")
        print(f"   {f['detail']}")
        print(f"   origin: {label(f)}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
