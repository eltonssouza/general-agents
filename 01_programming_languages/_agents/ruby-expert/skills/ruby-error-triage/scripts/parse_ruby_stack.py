#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_ruby_stack.py - triage of Ruby error messages and backtraces, linking the error to what the R30-R34 notes say.

Read-only, no network, does not execute code. The analyzed text is DATA, not instructions.
Accepts both backtrace formats: before 3.4 (backtick: `meth') and 3.4 onwards (single quotes and 'Class#meth'),
per R34 p.8.

Usage:
  python -I parse_ruby_stack.py trace.txt
  python -I parse_ruby_stack.py --trace "app.rb:10:in 'Object#run': oops (Regexp::TimeoutError)"
  cat trace.txt | python -I parse_ruby_stack.py
  python -I parse_ruby_stack.py --list
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

# Knowledge: per exception class. "from source" only when the note says something about the class/situation.
KNOWLEDGE = {
    "Regexp::TimeoutError": {
        "label": "from source", "source": "R32 p.7",
        "meaning": "The regex match exceeded the limit set by Regexp.timeout (global) or by timeout: in Regexp.new.",
        "action": "The note presents the timeout as a fallback measure for regexes with back-references, look-around or huge repetitions, where the 3.2 optimization does not apply (R32 p.7). Review the regex; adjusting the value is a project decision [inference]."},
    "NoMatchingPatternError": {
        "label": "from source", "source": "R30 p.6",
        "meaning": "No pattern matched. The note mentions that in 2.7 the `in` expression raised this error and that in 3.0 `in` returns true/false.",
        "action": "Check the version: `expr in pat` returns a boolean since 3.0 (R30 p.6). If the error comes from `case/in` without `else` or from `=>`, it is general pattern matching behavior [extrapolation]."},
    "SyntaxError": {
        "label": "from source", "source": "R32 p.8",
        "meaning": "Syntax error. Since 3.2, syntax_suggest (formerly dead_end) helps find a missing or extra `end`.",
        "action": "Run the file with Ruby 3.2+ to see the syntax_suggest hint (R32 p.8). With Prism as the default parser in 3.4, messages may differ (R34 p.2)."},
    "NameError": {
        "label": "from source", "source": "R31 p.3",
        "meaning": "Undefined name. error_highlight (3.1) shows ^^^^ under the snippet and 'Did you mean?'; in 3.1 only NameError (and subclasses) was supported.",
        "action": "See the underline in the backtrace (R31 p.3). If the name is Fixnum/Bignum/Random::DEFAULT, see the removal rule (R32 p.16)."},
    "NoMethodError": {
        "label": "from source", "source": "R31 p.3",
        "meaning": "Undefined method (subclass of NameError). The 3.1 note example uses `1.time {}` and error_highlight underlines the method with 'Did you mean?  times'.",
        "action": "Read the underlined snippet (R31 p.3) and check whether the receiver is nil [extrapolation]. If the method is File.exists?, Dir.exists? or taint/untaint, it was removed in 3.2 (R32 p.16)."},
    "TypeError": {
        "label": "from source", "source": "R32 p.8",
        "meaning": "Incompatible type. Since 3.2 ErrorHighlight points at the relevant argument in TypeError and ArgumentError (example: nil can't be coerced into Integer).",
        "action": "See the underline under the argument (R32 p.8)."},
    "ArgumentError": {
        "label": "from source", "source": "R32 p.8",
        "meaning": "Invalid argument. 3.2 ErrorHighlight points at the argument. In 3.0, keywords were separated from positional arguments, which can cause ArgumentError in old code (R30 p.7).",
        "action": "Check whether the code was written for 2.7 and uses implicit keywords (R30 p.7); in 3.2, delegating keywords through *args requires ruby2_keywords (R32 p.10)."},
    "FrozenError": {
        "label": "extrapolation", "source": "R34 p.5 (warning only)",
        "meaning": "A frozen object was mutated. The notes do NOT mention FrozenError. What 3.4 documents for string literals is a deprecation WARNING in files without frozen_string_literal (R34 p.5).",
        "action": "[extrapolation] See who froze the object (magic comment, freeze, constant). For the 3.4 warning, run with -W:deprecated (R34 p.5)."},
    "Ractor::IsolationError": {
        "label": "extrapolation", "source": "R30 p.2",
        "meaning": "The notes do NOT mention this class. They say ractors do not share normal objects and exchange messages (R30 p.2).",
        "action": "[extrapolation] See doc/ractor.md for your version (the notes only point to that file, R30 p.3)."},
    "LoadError": {
        "label": "from source", "source": "R30 p.8",
        "meaning": "Library not found. The notes list libraries that left the stdlib/bundled gems or became bundled gems between versions.",
        "action": "Check whether the library is on the version list (use --list-libs); if so, add the gem to the Gemfile/gemspec."},
}

# LoadError: library -> (version, source, text)
LIBS = {}
for lib in ("sdbm", "webrick", "net-telnet", "xmlrpc"):
    LIBS[lib] = ("3.0", "R30 p.8", "stopped being a bundled gem/part of the stdlib in 3.0; install the gem")
for lib in ("net-ftp", "net-imap", "net-pop", "net-smtp", "matrix", "prime"):
    LIBS[lib] = ("3.1", "R31 p.11", "went from default gem to bundled gem in 3.1; declare it in the Gemfile")
for lib in ("abbrev", "base64", "bigdecimal", "csv", "drb", "getoptlong", "mutex_m", "nkf", "observer", "racc",
            "resolv-replace", "rinda", "syslog"):
    LIBS[lib] = ("3.3/3.4", "R33 p.7-8; R34 p.7", "in 3.3 RubyGems/Bundler already warn; in 3.4 (most of them) it becomes a bundled gem: declare it in the Gemfile")
LIBS["readline"] = ("3.3", "R33 p.7", "ext/readline was retired; use reline or `gem install readline-ext`")

GENERIC = {
    "label": "extrapolation", "source": "-",
    "meaning": "Error class that the R30-R34 notes do not address.",
    "action": "[extrapolation] Use the message and the backtrace; consult the version documentation. No note page applies."}

HEAD_CLASSIC = re.compile(r"^(?P<file>[^\s:][^:]*?):(?P<line>\d+):in\s+[`'](?P<meth>[^'`]+)'?:\s*(?P<msg>.*?)(?:\s+\((?P<cls>[A-Z][\w:]*)\))?\s*$")
HEAD_MODERN = re.compile(r"^(?P<cls>[A-Z][\w:]*(?:Error|Exception))(?::\s*(?P<msg>.*))?$")
FROM = re.compile(r"^\s*from\s+(?P<file>[^\s:][^:]*?):(?P<line>\d+):in\s+[`'](?P<meth>[^'`]+)'?")
CARET = re.compile(r"^\s*\^{2,}")


def parse(text):
    lines = [l.rstrip("\n") for l in text.splitlines() if l.strip()]
    if not lines:
        return None
    res = {"class": None, "message": "", "file": "?", "line": "?", "method": "?", "snippet": [], "highlight": [], "frames": [], "format": "?"}
    for l in lines:
        m = HEAD_CLASSIC.match(l)
        if m and not res["class"]:
            res.update(file=m["file"], line=m["line"], method=m["meth"], message=m["msg"] or "")
            res["format"] = "3.4+ (single quotes)" if "'" in l.split(":in", 1)[1][:3] else "before 3.4 (backtick)"
            cls = m["cls"]
            if not cls:
                mm = re.match(r"^(?P<m>.*?)\s*\((?P<c>[A-Z][\w:]*)\)$", res["message"])
                if mm:
                    cls, res["message"] = mm["c"], mm["m"]
            res["class"] = cls
            continue
        fr = FROM.match(l)
        if fr:
            res["frames"].append("%s:%s (%s)" % (fr["file"], fr["line"], fr["meth"]))
            continue
        if CARET.match(l):
            res["highlight"].append(l)
            continue
        if res["class"] is None:
            h = HEAD_MODERN.match(l.strip())
            if h:
                res["class"], res["message"] = h["cls"], h["msg"] or ""
                continue
        if res["file"] != "?" or res["class"]:
            res["snippet"].append(l)
    return res


def lookup(res):
    cls = res["class"]
    msg = res["message"]
    if cls == "LoadError" or re.search(r"cannot load such file", msg):
        m = re.search(r"cannot load such file -- ([\w./-]+)", msg)
        lib = m.group(1) if m else None
        info = dict(KNOWLEDGE["LoadError"])
        if lib and lib in LIBS:
            ver, src, txt = LIBS[lib]
            info.update(label="from source", source=src, meaning="The library '%s' %s (version %s)." % (lib, txt, ver),
                        action="Declare the gem in the Gemfile/gemspec and check the Ruby version in use. [VERSION-DEPENDENT]")
        elif lib:
            info.update(label="extrapolation", source="-", meaning="The library '%s' does not appear in the notes' lists." % lib,
                        action="[extrapolation] Check the gem name and the Gemfile.")
        return info
    if cls in ("NameError", "NoMethodError") and re.search(r"\b(Fixnum|Bignum|exists\?|taint|untaint|Random::DEFAULT)\b", msg):
        info = dict(KNOWLEDGE[cls])
        info.update(label="from source", source="R32 p.16",
                    meaning="Constant/method removed in 3.2 (Fixnum, Bignum, Random::DEFAULT, Dir.exists?, File.exists?, taint and related).",
                    action="Switch to the current API (for example Integer instead of Fixnum/Bignum, File.exist?/Dir.exist?) [extrapolation for the replacement names] and check the version. [VERSION-DEPENDENT]")
        return info
    if cls in KNOWLEDGE:
        return KNOWLEDGE[cls]
    if cls and cls.endswith("Error") and cls.split("::")[-1] == "TimeoutError" and cls != "Regexp::TimeoutError":
        return dict(GENERIC, meaning="TimeoutError from another library; only Regexp::TimeoutError is addressed in the notes (R32 p.7).")
    return GENERIC


def main():
    ap = argparse.ArgumentParser(description="Triage of Ruby errors and backtraces (rules from the 3.0-3.4 notes).")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--trace", "-t")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list", action="store_true", help="known error classes")
    ap.add_argument("--list-libs", action="store_true", help="libraries whose status changed in the notes")
    a = ap.parse_args()
    if a.list:
        for k, v in KNOWLEDGE.items():
            print("%-24s [%s] (%s)" % (k, v["label"], v["source"]))
        return 0
    if a.list_libs:
        for k, (ver, src, txt) in sorted(LIBS.items()):
            print("%-16s %-8s [from source] (%s) %s" % (k, ver, src, txt))
        return 0
    if a.trace is not None:
        text = a.trace
    elif a.file:
        if not os.path.isfile(a.file):
            print("Error: file not found: %s" % a.file, file=sys.stderr)
            return 2
        with open(a.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    res = parse(text)
    if not res or not res["class"]:
        print("Could not identify the error class. Paste the main line (file:line:in '...': message (Class)).")
        return 1
    info = lookup(res)
    if a.json:
        print(json.dumps({"parsed": res, "info": info}, ensure_ascii=False, indent=1))
        return 0
    print("=== Triage (analyzed data, never executed) ===")
    print("Class   : %s" % res["class"])
    print("Message : %s" % res["message"])
    print("Origin  : %s:%s in %s  [format: %s]" % (res["file"], res["line"], res["method"], res["format"]))
    if res["highlight"]:
        print("error_highlight:")
        for h in res["highlight"]:
            print("  " + h)
    if res["frames"]:
        print("Callers (%d): %s" % (len(res["frames"]), "; ".join(res["frames"][:5])))
    print("\nMeaning: %s" % info["meaning"])
    print("Action : %s" % info["action"])
    print("Source of the text above: [%s] (%s)" % (info["label"], info["source"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
