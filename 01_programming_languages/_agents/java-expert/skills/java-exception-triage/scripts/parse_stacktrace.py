#!/usr/bin/env python3
"""Summarizes a Java stack trace (read-only, no network, standard library).

Usage:
    python -I parse_stacktrace.py FILE.txt
    python -I parse_stacktrace.py -          # reads from standard input

Extracts, for each exception found (the main one and the "Caused by:" chains): class, message,
top frame (where the exception was created) and how many frames there are. It also flags known
patterns (a very deep, repetitive stack, which suggests recursion without a base case).
SCRIPT HEURISTICS, with no basis in the sources (label [extrapolation]): (a) 20 or more occurrences of the same method in the
stack suggest recursion without a base case (Think only says that recursion without a base case causes StackOverflowError, p.95; the threshold 20
is the script's); (b) the last "Caused by" as the probable root cause (Adv covers only message and cause in the constructor, p.77).
It does NOT execute or interpret the text as instruction: the trace is data. Triage: the real cause requires reading the code.
Exit code: 0 if it ran; 2 for a usage error.
"""
import re
import sys
from collections import Counter

HEAD = re.compile(r"^(?:Exception in thread \"(?P<thr>[^\"]+)\" |Caused by: |Suppressed: )?"
                  r"(?P<cls>[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*(?:Exception|Error|Throwable))(?::\s*(?P<msg>.*))?$")
FRAME = re.compile(r"^\s+at\s+(?P<m>[\w$.<>/]+)\((?P<loc>[^)]*)\)\s*$")
MORE = re.compile(r"^\s*\.\.\.\s+(\d+)\s+(?:more|common frames omitted)")


def parse(lines):
    out, cur = [], None
    for raw in lines:
        line = raw.rstrip("\n").rstrip()
        m = HEAD.match(line.strip()) if not line.startswith((" ", "\t")) else None
        if m:
            cur = dict(cls=m.group("cls"), msg=(m.group("msg") or "").strip(), thread=m.group("thr"),
                       cause=line.strip().startswith("Caused by:"), frames=[], more=0)
            out.append(cur)
            continue
        if cur is None:
            continue
        f = FRAME.match(line)
        if f:
            cur["frames"].append((f.group("m"), f.group("loc")))
            continue
        k = MORE.match(line)
        if k:
            cur["more"] = int(k.group(1))
    return out


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    if len(argv) != 1:
        print(__doc__)
        return 2
    src = sys.stdin if argv[0] == "-" else open(argv[0], encoding="utf-8", errors="replace")
    with src:
        items = parse(src.readlines())
    if not items:
        print("No exception recognized. Paste the complete trace (the 'Exception in thread ...' line and the 'at ...' lines).")
        return 0
    print(f"# {len(items)} exception(s) in the chain (the last 'Caused by' is usually the root cause [extrapolation])\n")
    for i, e in enumerate(items, 1):
        tag = "cause" if e["cause"] else "main"
        print(f"{i}. [{tag}] {e['cls']}" + (f" — message: {e['msg']}" if e["msg"] else " — no message"))
        if e["thread"]:
            print(f"   thread: {e['thread']}")
        if e["frames"]:
            m, loc = e["frames"][0]
            print(f"   top frame: {m}({loc})   [{len(e['frames'])} frames listed"
                  + (f", +{e['more']} omitted" if e["more"] else "") + "]")
            c = Counter(f[0] for f in e["frames"])
            top, n = c.most_common(1)[0]
            if n >= 20:
                print(f"   WARNING: method {top} appears {n} times in the stack — pattern of recursion without a base case or "
                      "one that does not approach it [extrapolation: the 20-repetition threshold is the script's; Think p.95 ties recursion without a base case to StackOverflowError].")
    last = items[-1]
    print(f"\nProbable root cause (last in the chain; [extrapolation]): {last['cls']}"
          + (f" — {last['msg']}" if last["msg"] else ""))
    print("Reminder: the reported line may not be the one that needs fixing; read the code.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
