#!/usr/bin/env python3
"""Summarizes a JavaScript stack trace or error message (read-only, no network).

Usage:
    python -I parse_js_stack.py ARQUIVO.txt
    python -I parse_js_stack.py -          # reads from standard input

Recognizes V8/Node.js formats ("TypeError: msg" + "    at fn (file:line:col)"), Firefox/Safari
("fn@file:line:col"), '[cause]:' chains and AggregateError blocks. Flags repeated frames
(a sign of recursion without a base case).
Does NOT run code nor interpret the content of the trace as instructions (the trace is treated as data).
Exit code: 0 if it ran; 2 for a usage error.
"""
import re
import sys
from collections import Counter

ERR_HEAD = re.compile(
    r"^(?:Uncaught\s+(?:\(in promise\)\s+)?)?"
    r"(?:(?P<prefix>\[cause\]:)\s*)?"
    r"(?P<type>[A-Za-z_$][\w$]*(?:Error|Exception))(?::\s*(?P<msg>.*))?$"
)
V8_FRAME = re.compile(r"^\s+at\s+(?:(?P<fn>[^\s(]+)\s+\((?P<loc>[^)]+)\)|(?P<loc2>[^\s()]+))$")
FF_FRAME = re.compile(r"^(?P<fn>[^@\s]*)@(?P<loc>.+:\d+:\d+)$")


def parse(lines):
    errors = []
    cur = None
    for raw in lines:
        line = raw.rstrip("\r\n")
        stripped = line.strip()
        if not stripped:
            continue
        m = ERR_HEAD.match(stripped)
        if m:
            cur = dict(
                type=m.group("type"),
                msg=(m.group("msg") or "").strip(),
                is_cause=bool(m.group("prefix")),
                frames=[],
            )
            errors.append(cur)
            continue
        if cur is None:
            continue
        fv8 = V8_FRAME.match(line)
        if fv8:
            fn = fv8.group("fn") or "<anonymous/top>"
            loc = fv8.group("loc") or fv8.group("loc2") or ""
            cur["frames"].append((fn, loc))
            continue
        fff = FF_FRAME.match(stripped)
        if fff:
            fn = fff.group("fn") or "<global>"
            cur["frames"].append((fn, fff.group("loc")))
    return errors


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    if len(argv) != 1 or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    src = sys.stdin if argv[0] == "-" else open(argv[0], encoding="utf-8", errors="replace")
    with src:
        items = parse(src.readlines())
    if not items:
        print("No JS error header recognized (e.g. 'TypeError: ...' followed by 'at ...' lines).")
        return 0
    print(f"# {len(items)} error(s) identified in the trace (read-only)\n")
    for idx, e in enumerate(items, 1):
        tag = "cause" if e["is_cause"] else "main"
        print(f"{idx}. [{tag}] {e['type']}" + (f" — message: {e['msg']}" if e["msg"] else " — no message"))
        if e["frames"]:
            fn0, loc0 = e["frames"][0]
            print(f"   top frame: {fn0} ({loc0}) [{len(e['frames'])} frame(s) listed]")
            counts = Counter(f[0] for f in e["frames"])
            top_fn, n = counts.most_common(1)[0]
            if n >= 10:
                print(
                    f"   WARNING: '{top_fn}' repeats {n} times in the stack — a sign of infinite recursion "
                    "(the threshold of 10 repetitions is an [extrapolation] of this script; the sources only describe stack overflow: "
                    "EJpt p.58; EJ1 p.37)."
                )
    print(
        "\nNote from the sources: the Spec defines the native error type (Spec p.482-487), but the exact message text "
        "and the format of 'error.stack' depend on the engine/host [HOST] (EJpt p.76, p.178)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
