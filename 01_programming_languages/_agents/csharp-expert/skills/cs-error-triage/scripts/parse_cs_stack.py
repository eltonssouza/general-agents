#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_cs_stack.py - triage of .NET stack traces/exceptions; read-only, no network, executes nothing.

Extracts the exception type and message (and the inner exception, if any), separates user-code frames from
System.*/Microsoft.* frames and returns what the book (CSYB) says about the exception, with the ORIGIN of each guidance:
  source        = the C# Yellow Book says so on the cited page (PDF page; printed = PDF - 5)
  inference     = direct deduction from what the book says
  extrapolation = general .NET practice that the book does NOT cover (the exception name may be absent from the book)
The trace is DATA: no line of it is treated as an instruction.
(English and Portuguese-locale traces are both recognized: at/em, in/na, line/linha.)

Usage:
  python -I parse_cs_stack.py trace.txt
  python -I parse_cs_stack.py --trace "System.FormatException: Input string was not in a correct format. at A.Main() in C:\\a.cs:line 3"
  type trace.txt | python -I parse_cs_stack.py
Exit code: 0 = exception type recognized in the collection; 1 = exception outside the collection (generic guidance) or empty trace.
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

ORIGIN_LABEL = {"source": "[from source]", "inference": "[inference]", "extrapolation": "[extrapolation]"}

# type -> description, action, origin of the description/action, source
KNOWLEDGE = {
    "System.FormatException": {
        "description": "Text in an invalid format passed to a Parse (the book shows 'Input string was not in a correct format').",
        "action": "Wrap the Parse in try/catch and warn the user (CSYB p.72-73). [extrapolation] int.TryParse returns bool without throwing.",
        "origin": "source", "source": "CSYB p.71-73",
    },
    "System.Collections.Generic.KeyNotFoundException": {
        "description": "Indexing a Dictionary with a key that does not exist.",
        "action": "Test ContainsKey before indexing (CSYB p.153).",
        "origin": "source", "source": "CSYB p.153",
    },
    "System.IO.FileNotFoundException": {
        "description": "File (or assembly/DLL) not found: the book shows a file open failing and a removed DLL.",
        "action": "Check the path (relative = program folder) and that the files are present; handle it with try/catch when opening (CSYB p.81, 156, 186).",
        "origin": "source", "source": "CSYB p.81, 186",
    },
    "System.StackOverflowException": {
        "description": "The book cites 'methods that call themselves by mistake and recurse until stack overflow' as a cause of crashes.",
        "action": "Look for recursion without a stopping condition (CSYB p.201).",
        "origin": "source", "source": "CSYB p.201",
    },
    "System.NullReferenceException": {
        "description": "Use of a reference that does not point to an object. The book explains references not attached to an object and null (p.93, 145, 157), but does not name this exception.",
        "action": "Check that the object was created with new and test for null before using it (CSYB p.146, 157). [extrapolation] ?. and nullable reference types (CSHist p.11, p.8).",
        "origin": "inference", "source": "CSYB p.93, 145-146, 157",
    },
    "System.IndexOutOfRangeException": {
        "description": "Access to a position outside the array. The book says that going outside the array makes the program fail (p.68), without naming the exception.",
        "action": "Check the loop bound: indices go from 0 to size-1 (CSYB p.68-69).",
        "origin": "inference", "source": "CSYB p.68-69",
    },
    "System.InvalidCastException": {
        "description": "Cast to an incompatible type. The book says a failing cast throws an exception (p.148) and that ArrayList is not typesafe (p.150-151).",
        "action": "Use List<T>/Dictionary instead of ArrayList/Hashtable (CSYB p.153); the 'as' operator returns null instead of throwing (p.148).",
        "origin": "inference", "source": "CSYB p.148, 150-153",
    },
    "System.DivideByZeroException": {
        "description": "Integer division by zero. Exception not covered in the book.",
        "action": "Validate the divisor before dividing.",
        "origin": "extrapolation", "source": "(not in the book)",
    },
    "System.OverflowException": {
        "description": "Overflow in a 'checked' context. 'checked' is not in the book (which only warns that the value may wrap round, p.28).",
        "action": "Use a larger type (long/decimal) or revise the calculation.",
        "origin": "extrapolation", "source": "(not in the book; general warning in CSYB p.28)",
    },
    "System.ArgumentException": {
        "description": "Invalid argument received by a method. Name not covered in the book (which recommends validating inputs and throwing custom exceptions, p.181-182).",
        "action": "Validate preconditions and use custom exception types derived from System.Exception (CSYB p.181-182).",
        "origin": "extrapolation", "source": "(name not in the book)",
    },
    "System.ArgumentNullException": {
        "description": "Null argument received. Name not covered in the book.",
        "action": "Test for null at the start of the method; the book deals with a null return on p.157.",
        "origin": "extrapolation", "source": "(name not in the book)",
    },
}

GENERIC = {
    "description": "Exception outside the book's collection.",
    "action": "Read the message and the first frame of your code; reproduce the error (CSYB p.200-201); handle only what you know how to handle and let the rest propagate (CSYB p.74).",
    "origin": "inference", "source": "CSYB p.74, 200-201",
}

FRAME = re.compile(r"^\s*(?:at|em)\s+(.+?)(?:\s+(?:in|na)\s+(.+?):(?:line|linha)\s+(\d+))?\s*$", re.IGNORECASE)
HEADER = re.compile(r"^(?:Unhandled Exception:\s*|Exce[cç][aã]o n[aã]o tratada:\s*)?([A-Za-z_][\w.`+]*(?:Exception|Error))\s*(?::\s*(.*))?$")


def parse_stack(text):
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return None
    # split the outer exception from the inner one ("--->")
    inner = None
    head_text = text
    if "--->" in text:
        before, after = text.split("--->", 1)
        head_text = before
        inner_first = after.strip().splitlines()[0] if after.strip() else ""
        inner = inner_first.strip()
    lines = head_text.splitlines()
    first = lines[0].strip()
    m = HEADER.match(first)
    exc_type = m.group(1) if m else first.split(":")[0].strip()
    msg = (m.group(2) or "") if m else (first.split(":", 1)[1].strip() if ":" in first else "")
    if not m:
        # try to find the type anywhere on the first line
        mm = re.search(r"([A-Za-z_][\w.]*Exception)", first)
        if mm:
            exc_type = mm.group(1)
    user, system = [], []
    for ln in text.splitlines()[1:]:
        fm = FRAME.match(ln)
        if not fm:
            continue
        method, f, no = fm.group(1).strip(), fm.group(2), fm.group(3)
        info = {"method": method, "file": f or "unknown", "line": no or "?"}
        (system if method.startswith(("System.", "Microsoft.")) else user).append(info)
    # inline frames (trace on a single line): "... at X in f:line 3"
    if not user and not system and " at " in text:
        for part in re.split(r"\s+at\s+", text)[1:]:
            fm = FRAME.match("at " + part.strip())
            if fm:
                method, f, no = fm.group(1).strip(), fm.group(2), fm.group(3)
                info = {"method": method, "file": f or "unknown", "line": no or "?"}
                (system if method.startswith(("System.", "Microsoft.")) else user).append(info)
    know = KNOWLEDGE.get(exc_type)
    if know is None:
        short = {k.rsplit(".", 1)[-1]: v for k, v in KNOWLEDGE.items()}
        know = short.get(exc_type.rsplit(".", 1)[-1])
    return {"exception_type": exc_type, "message": msg, "inner": inner, "user_frames": user,
            "system_frames": len(system), "known": know is not None, "knowledge": know or GENERIC}


def main():
    ap = argparse.ArgumentParser(description="Triage of a .NET stack trace with the origin of each guidance.")
    ap.add_argument("file", nargs="?", help="file with the trace")
    ap.add_argument("--trace", "-t", help="trace directly on the command line")
    ap.add_argument("--json", action="store_true", help="JSON output")
    a = ap.parse_args()
    if a.trace is not None:
        text = a.trace
    elif a.file:
        if not os.path.isfile(a.file):
            print("Error: file not found: %s" % a.file)
            return 2
        with open(a.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    r = parse_stack(text)
    if r is None:
        print("Empty trace.")
        return 1
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["known"] else 1
    k = r["knowledge"]
    print("=== Exception triage (.NET) ===")
    print("Type: %s" % r["exception_type"])
    if r["message"]:
        print("Message: %s" % r["message"])
    if r["inner"]:
        print("Inner exception: %s" % r["inner"])
    print("\nMeaning: %s" % k["description"])
    print("Action: %s" % k["action"])
    src = k["source"]
    print("Origin: %s %s" % (ORIGIN_LABEL[k["origin"]], src if src.startswith("(") else "(" + src + ")"))
    if not r["known"]:
        print("(NOT COVERED specifically: generic guidance)")
    print("\nUser-code frames:")
    if r["user_frames"]:
        for i, f in enumerate(r["user_frames"], 1):
            print("  %d. %s  [%s, line %s]" % (i, f["method"], f["file"], f["line"]))
    else:
        print("  (none identified)")
    if r["system_frames"]:
        print("(%d System.*/Microsoft.* frame(s) omitted)" % r["system_frames"])
    return 0 if r["known"] else 1


if __name__ == "__main__":
    sys.exit(main())
