#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_php_stack.py - triage of PHP error messages and stack traces. Read-only, no network, stdlib.

Extracts type, message, origin file/line and stack frames, and attaches short guidance
WITH a declared origin:
  book          = based on the indicated PRW page (PDF page)
  inference     = direct deduction from a point in the book
  extrapolation = general knowledge, NOT in the PRW
The trace is treated as DATA: nothing in it is executed or obeyed.

Usage:
  python -I parse_php_stack.py trace.txt
  python -I parse_php_stack.py --trace "PHP Fatal error:  Uncaught TypeError: x() ... in /app/a.php:10"
  python -I parse_php_stack.py --json trace.txt
  python -I parse_php_stack.py --kinds            # known types and origin
Output: 0 = interpreted; 1 = nothing recognized; 2 = usage/file error.
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

# type -> (meaning, action, origin, page)
KNOWLEDGE = {
    "ErrorException": ("PHP error/warning converted into an exception (ErrorException extends Exception).",
                       "Fix the cause of the original error (file/line indicated); converting errors to exceptions is a framework practice in development.",
                       "book", "p.54"),
    "BadMethodCallException": ("SPL exception, typically thrown in __call() when the requested method does not exist.",
                               "Check the name of the method called and the class's __call()/__callStatic().",
                               "book", "p.55-56"),
    "PDOException": ("Failure in the PDO layer (connection, SQL or execution) when ERRMODE_EXCEPTION is active.",
                     "Check DSN, charset (utf8mb4), credentials and SQL; build queries with prepare() and bound parameters.",
                     "inference", "p.24, 43-44"),
    "Exception": ("Generic exception; gives little context.",
                  "Read the message and the stack; the book suggests subclasses or SPL exceptions to give context.",
                  "book", "p.55-56"),
    "InvalidArgumentException": ("SPL exception for an invalid argument.",
                                 "Validate the input (filter_var/filter_input) before calling.",
                                 "inference", "p.55-56, 59"),
    "RuntimeException": ("Runtime exception (SPL).", "Read the message; handle it with a specific try/catch.", "inference", "p.55-56"),
    "TypeError": ("Incompatible argument/return type.",
                  "Check the type actually passed; with declare(strict_types=1) there is no scalar coercion.",
                  "extrapolation", "-"),
    "ParseError": ("Syntax error while compiling the file.",
                   "Look for ';', unbalanced braces/parentheses or an invalid keyword on the indicated line or the previous one; run php -l file.php.",
                   "extrapolation", "-"),
    "DivisionByZeroError": ("Division or modulo by zero.", "Validate the divisor before the operation.", "extrapolation", "-"),
    "ArgumentCountError": ("Number of arguments incompatible with the signature.", "Check the call and the signature.", "extrapolation", "-"),
    "Error": ("Engine error (PHP 7+).", "Read the message and the line; a programming error, not an input error.", "extrapolation", "-"),
}

LEVELS = {
    "Fatal error": ("E_ERROR: fatal error, execution stops; fix the cause in the code.", "book", "p.52"),
    "Parse error": ("Syntax error at compile time.", "extrapolation", "-"),
    "Warning": ("E_WARNING: non-fatal, execution continues.", "book", "p.52"),
    "Notice": ("E_NOTICE: advisory notice, execution is not interrupted (e.g. undefined variable).", "book", "p.51-52"),
    "Deprecated": ("Deprecated feature: plan the replacement.", "extrapolation", "-"),
    "Strict Standards": ("E_STRICT [DATED]: suggestion for future compatibility.", "book", "p.52"),
}

HEAD = re.compile(
    r"^(?:PHP\s+)?(?P<level>Fatal error|Parse error|Warning|Notice|Deprecated|Strict Standards)\s*:\s*(?P<rest>.*)$")
UNCAUGHT = re.compile(r"Uncaught\s+(?P<cls>[\w\\]+)\s*:\s*(?P<msg>.*?)(?:\s+in\s+(?P<file>\S.*?):(?P<line>\d+))?\s*$")
ONLINE = re.compile(r"^(?P<msg>.*?)\s+in\s+(?P<file>\S.*?)\s+on\s+line\s+(?P<line>\d+)\s*$")
FRAME = re.compile(r"^#(?P<n>\d+)\s+(?P<file>.+?)\((?P<line>\d+)\):\s*(?P<call>.+)$")
FRAME_INT = re.compile(r"^#(?P<n>\d+)\s+(?P<call>\[internal function\].*|\{main\})$")


def parse(text):
    lines = [l.rstrip("\r") for l in text.strip().splitlines()]
    res = {"level": None, "type": None, "message": None, "file": None, "line": None, "frames": []}
    for l in lines:
        m = HEAD.match(l.strip())
        if not m:
            continue
        res["level"] = m.group("level")
        rest = re.sub(r",? called in .+? on line \d+ and defined", "", m.group("rest"))
        u = UNCAUGHT.search(rest)
        if u:
            res["type"] = u.group("cls").lstrip("\\")
            msg = u.group("msg")
            res["file"], res["line"] = u.group("file"), u.group("line")
            res["message"] = msg.strip()
        else:
            o = ONLINE.match(rest)
            if o:
                res["message"], res["file"], res["line"] = o.group("msg"), o.group("file"), o.group("line")
            else:
                res["message"] = rest
        break
    for l in lines:
        s = l.strip()
        f = FRAME.match(s)
        if f:
            res["frames"].append({"n": int(f.group("n")), "file": f.group("file"), "line": int(f.group("line")), "call": f.group("call")})
            continue
        fi = FRAME_INT.match(s)
        if fi:
            res["frames"].append({"n": int(fi.group("n")), "file": None, "line": None, "call": fi.group("call")})
    th = re.search(r"thrown in\s+(\S.*?)\s+on line\s+(\d+)", text)
    if th and not res["file"]:
        res["file"], res["line"] = th.group(1), th.group(2)
    if res["level"] is None and not res["frames"]:
        return None
    t = res["type"]
    if t is None and res["level"] in ("Parse error",):
        t = "ParseError"
        res["type"] = t
    info = KNOWLEDGE.get(t) if t else None
    if info is None and t and t.endswith("Exception"):
        info = ("Application- or library-specific exception.", "Read the message and the originating class; handle it with a specific catch.", "extrapolation", "-")
    lv = LEVELS.get(res["level"] or "")
    res["advice"] = None
    if info:
        res["advice"] = {"meaning": info[0], "action": info[1], "origin": info[2], "page": info[3]}
    res["level_note"] = None
    if lv:
        res["level_note"] = {"meaning": lv[0], "origin": lv[1], "page": lv[2]}
    res["hints"] = hints(text)
    return res


def hints(text):
    out = []
    low = text.lower()
    if "headers already sent" in low:
        out.append(("Output sent before the headers (whitespace/BOM/echo before header()/setcookie()).", "extrapolation", "-"))
    if "allowed memory size" in low:
        out.append(("Memory limit exceeded: review consumption (e.g. loading everything into an array) before raising memory_limit.", "extrapolation", "-"))
    if "maximum execution time" in low:
        out.append(("Maximum execution time exceeded: move long-running work to the CLI/a queue.", "extrapolation", "-"))
    if re.search(r"undefined (?:variable|index|array key)", low):
        out.append(("Undefined variable/index: initialize it or use ?? (the book shows 'Undefined variable' and 'Undefined index').", "book", "p.51, 53"))
    if re.search(r"mysql_(?:connect|query)|call to undefined function mysql_", low):
        out.append(("The mysql_* function no longer exists: the extension was removed in PHP 7.0; migrate to PDO/mysqli.", "book", "p.42"))
    if "sqlstate" in low:
        out.append(("SQLSTATE comes from the database driver: check the SQL and DSN; use prepare() with parameters.", "inference", "p.43-44"))
    if "display_errors" in low:
        out.append(("In production the book says display_errors = Off and log_errors = On.", "book", "p.62"))
    return [{"text": t, "origin": o, "page": p} for t, o, p in out]


def tag(o, p):
    if o == "book":
        return f"[from source] (PRW {p})"
    if o == "inference":
        return f"[inference] (basis: PRW {p})"
    return "[extrapolation] (outside the PRW)"


def main():
    ap = argparse.ArgumentParser(description="Triage of PHP errors/stack traces, with labeled origin.")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--trace", "-t")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--kinds", action="store_true")
    a = ap.parse_args()
    if a.kinds:
        for k, v in KNOWLEDGE.items():
            print(f"{k:<26} {v[2]:<13} PRW {v[3]}")
        return 0
    if a.trace is not None:
        text = a.trace
    elif a.file:
        if not os.path.isfile(a.file):
            print(f"Error: file not found: {a.file}", file=sys.stderr)
            return 2
        text = open(a.file, encoding="utf-8", errors="replace").read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        ap.print_help()
        return 2
    r = parse(text)
    if r is None:
        print("I did not recognize a PHP error message (expected: 'Fatal error: ...', 'Warning: ...' or frames '#0 file(line): ...').")
        return 1
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print("=== PHP error triage (data treated as text; nothing executed) ===")
    print(f"Level:    {r['level']}")
    print(f"Type:     {r['type'] or '(not given)'}")
    print(f"Message:  {r['message']}")
    print(f"Origin:   {r['file'] or 'unknown'}:{r['line'] or '?'}")
    if r["level_note"]:
        n = r["level_note"]
        print(f"Level ->  {n['meaning']}  {tag(n['origin'], n['page'])}")
    if r["advice"]:
        v = r["advice"]
        print(f"Meaning:  {v['meaning']}")
        print(f"Action:   {v['action']}")
        print(f"Guidance origin: {tag(v['origin'], v['page'])}")
    for h in r["hints"]:
        print(f"Hint: {h['text']}  {tag(h['origin'], h['page'])}")
    if r["frames"]:
        print("\nStack:")
        for f in r["frames"]:
            loc = f"{f['file']}:{f['line']}" if f["file"] else "-"
            print(f"  #{f['n']} {loc}  {f['call']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
