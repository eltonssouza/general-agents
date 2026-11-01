#!/usr/bin/env python3
"""AST scan for points of attention in Python 3 code (read-only, no network).

Usage:
    python -I scan_python_smells.py [--json] PATH [PATH ...]

PATH may be a .py file or a directory (recursive; skips .git, __pycache__, venv, .venv,
node_modules, site-packages, build, dist). Uses the standard library `ast` module; it does NOT run
or import the analyzed code. If a file is not valid Python 3 for the interpreter running this
script, it is reported with a textual scan for Python 2 constructs.

This is triage: it points to WHERE to look and has false positives/negatives. "No findings" is NOT approval.
Exit code: 0 if it ran; 2 for a usage error.
"""
import argparse
import ast
import json
import os
import re
import sys

# Origin of each rule (the audit requires every coded rule to have backing or to be labeled).
# label: official = Tut/Ref; community = Notes; inference = conclusion of the package; extrapolation = outside the sources.
# Pages = PDF page (printed: Tut -6, Ref -8, Notes -25). Checked in tests/verify_citations.py.
RULES = {
    "mutable-default": ("official + community", "Ref p.103; Tut p.31-32; Notes p.207-208, 788-789"),
    "compare-none": ("community", "Notes p.39, 105, 107"),
    "compare-bool": ("community", "Notes p.786-787"),
    "is-literal": ("official", "Ref p.31-32"),
    "bare-except": ("community", "Notes p.448-449, 783"),
    "except-pass": ("inference", "basis Notes p.448-449 (they advise against catching everything); the severity and the pass part are inference"),
    "shadowed-except": ("official", "Tut p.68-69"),
    "finally-flow": ("official", "Tut p.73; Ref p.129"),
    "eq-without-hash": ("official", "Ref p.52-53, 109"),
    "mutate-while-iterating": ("official + community", "Tut p.23-24; Notes p.143, 643"),
    "eval-exec": ("community", "Notes p.505-506"),
    "pickle-load": ("official + community", "Tut p.66; Notes p.535"),
    "shell-true": ("community", "Notes p.434"),
    "weak-hash": ("extrapolation", "Notes p.694 lists MD5/SHA1 without a warning; their unsuitability for security is outside knowledge"),
    "syntax-error": ("inference", "the file is not valid Python 3 for this interpreter"),
    "py2-print": ("community [DATED]", "Notes p.626"),
    "py2-raw-input": ("community [DATED]", "Notes p.631"),
    "py2-xrange": ("community [DATED]", "Notes p.627"),
    "py2-iter-dict": ("community [DATED]", "Notes p.627, 642-643"),
    "py2-has-key": ("community [DATED]", "Notes p.642"),
    "py2-except-comma": ("official + community [DATED]", "Notes p.628; Ref p.127 (3.14 accepts except A, B without as)"),
    "py2-types": ("community [DATED]", "Notes p.37, 48, 624"),
    "py2-long-literal": ("community [DATED]", "Notes p.37, 57"),
    "py2-ne": ("community [DATED]", "Notes p.634"),
    "py2-exec": ("community [DATED]", "Notes p.641"),
    "py2-misc": ("community [DATED]", "Notes p.48, 632, 706"),
    "py2-module-names": ("community [DATED]", "Notes p.464, 534, 702"),
}

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", "site-packages", "build", "dist", ".tox"}

MUTABLE_CALLS = {"list", "dict", "set", "bytearray", "deque", "defaultdict", "OrderedDict", "Counter"}
MUTATORS = {"append", "extend", "insert", "remove", "pop", "clear", "sort", "reverse", "add", "discard", "update", "popitem"}

# typical Python 2 constructs (regex) -> (rule, message with source)
PY2 = [
    (re.compile(r"^\s*print\s+[^\s(=].*|^\s*print\s*$|^\s*print\s*>>"), "py2-print",
     "print as a statement (Python 2): in Python 3 it is a function; the old form is a SyntaxError (Notes p.626)"),
    (re.compile(r"\braw_input\s*\("), "py2-raw-input", "raw_input: in Python 3 use input() (Notes p.631)"),
    (re.compile(r"\bxrange\s*\("), "py2-xrange", "xrange: in Python 3 use range (Notes p.627)"),
    (re.compile(r"\.(iteritems|iterkeys|itervalues)\s*\("), "py2-iter-dict",
     "iteritems/iterkeys/itervalues: in Python 3 use items()/keys()/values() (Notes p.627, 642-643)"),
    (re.compile(r"\.has_key\s*\("), "py2-has-key", "has_key: in Python 3 use 'in' (Notes p.627)"),
    (re.compile(r"^\s*except\s+[\w.]+\s*,\s*\w+\s*:"), "py2-except-comma",
     "except Type, name: was Python 2 syntax (binding the name is 'except Type as name:'); note: in Python 3.14 "
     "'except A, B:' WITHOUT 'as' is valid and means a tuple of types (Ref p.127) — confirm what was intended"),
    (re.compile(r"\bunicode\s*\(|\bbasestring\b|\blong\s*\("), "py2-types", "unicode/basestring/long: Python 2 types"),
    (re.compile(r"\b\d+[lL]\b"), "py2-long-literal", "integer literal with an L suffix (Python 2)"),
    (re.compile(r"<>"), "py2-ne", "<> operator (Python 2); use !="),
    (re.compile(r"^\s*exec\s+[\"'\w]"), "py2-exec", "exec as a statement (Python 2); in Python 3 it is a function"),
    (re.compile(r"\bexecfile\s*\(|\.next\s*\(\s*\)"), "py2-misc", "execfile/.next(): Python 2 (in Python 3 use next(it))"),
    (re.compile(r"^\s*from\s+(Queue|ConfigParser|urllib2|StringIO|cPickle)\s+import|^\s*import\s+(Queue|ConfigParser|urllib2|StringIO|cPickle)\b"),
     "py2-module-names", "module with a Python 2 name (Queue, ConfigParser, urllib2, StringIO, cPickle…)"),
]


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(".py"):
                yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in sorted(files):
                    if f.endswith(".py"):
                        yield os.path.join(root, f)
        else:
            print(f"warning: path does not exist: {p}", file=sys.stderr)


def call_name(node):
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        base = f.value.id if isinstance(f.value, ast.Name) else ""
        return f"{base}.{f.attr}" if base else f.attr
    return ""


def _escapes_finally(stmts, in_loop=False):
    """return/break/continue that LEAVE the finally block (ignores nested functions and break/continue of inner loops)."""
    for st in stmts:
        if isinstance(st, ast.Return):
            yield st
        elif isinstance(st, (ast.Break, ast.Continue)) and not in_loop:
            yield st
        elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        else:
            loop = isinstance(st, (ast.For, ast.AsyncFor, ast.While))
            for fld in ("body", "orelse", "finalbody"):
                sub = getattr(st, fld, None)
                if isinstance(sub, list):
                    yield from _escapes_finally(sub, in_loop or (loop and fld == "body"))
            for h in getattr(st, "handlers", []) or []:
                yield from _escapes_finally(h.body, in_loop)
            for c in getattr(st, "cases", []) or []:
                yield from _escapes_finally(c.body, in_loop)


class Visitor(ast.NodeVisitor):
    def __init__(self, path, lines):
        self.path, self.lines, self.findings = path, lines, []

    def add(self, node, rule, sev, msg):
        ln = getattr(node, "lineno", 1)
        txt = self.lines[ln - 1].strip()[:140] if 0 < ln <= len(self.lines) else ""
        lab, src = RULES.get(rule, ("extrapolation", ""))
        self.findings.append(dict(file=self.path, line=ln, rule=rule, severity=sev, message=msg, text=txt,
                                  origin=lab, source=src))

    # --- functions: mutable default (Ref p.103; Notes p.207-208, 788-789) ---
    def _check_defaults(self, node):
        a = node.args
        for d in list(a.defaults) + [x for x in a.kw_defaults if x is not None]:
            bad = isinstance(d, (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp))
            if isinstance(d, ast.Call) and call_name(d).split(".")[-1] in MUTABLE_CALLS:
                bad = True
            if bad:
                self.add(d, "mutable-default", "high",
                         "mutable default value: it is computed ONCE at definition time and shared between calls; "
                         "use None and create the object inside the function (Ref p.103; Notes p.207-208, 788-789)")

    def visit_FunctionDef(self, node):
        self._check_defaults(node)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Lambda(self, node):
        self._check_defaults(node)
        self.generic_visit(node)

    # --- comparisons ---
    def visit_Compare(self, node):
        for op, right in zip(node.ops, node.comparators):
            if isinstance(op, (ast.Eq, ast.NotEq)) and isinstance(right, ast.Constant):
                if right.value is None:
                    self.add(node, "compare-none", "medium",
                             "== None / != None: use 'is None' / 'is not None' (Notes p.39, 105, 107)")
                elif right.value is True or right.value is False:
                    self.add(node, "compare-bool", "low",
                             "== True/False also matches 1 and 0; prefer implicit truthiness or 'is True/False' "
                             "if the singleton is the goal (Notes p.786-787)")
            if isinstance(op, (ast.Is, ast.IsNot)) and isinstance(right, ast.Constant) \
                    and isinstance(right.value, (str, bytes, int, float)) and not isinstance(right.value, bool):
                self.add(node, "is-literal", "medium",
                         "'is' with a literal: 'is' compares IDENTITY, '==' compares equality; the result depends on the "
                         "implementation (Ref p.31-32)")
        self.generic_visit(node)

    # --- exceptions ---
    def visit_ExceptHandler(self, node):
        broad = node.type is None or (isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"})
        if node.type is None:
            self.add(node, "bare-except", "high",
                     "bare except: catches everything (including KeyboardInterrupt/SystemExit) and hides the origin of the error; "
                     "catch specific types (Notes p.448-449, 783)")
        if broad and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.add(node, "except-pass", "high",
                     "broad exception swallowed with 'pass': masks bugs (Notes p.448-449)")
        self.generic_visit(node)

    @staticmethod
    def _handler_types(h):
        """List of the handler's class names (None = bare except:)."""
        if h.type is None:
            return None
        elts = h.type.elts if isinstance(h.type, ast.Tuple) else [h.type]
        return [e.id for e in elts if isinstance(e, ast.Name)]

    def _check_shadowed_handlers(self, node):
        import builtins
        seen = []  # previous handlers: (list of names | None)
        for h in node.handlers:
            names = self._handler_types(h)
            for prev in seen:
                shadow = prev is None
                if not shadow and names:
                    for earlier in prev:
                        ce = getattr(builtins, earlier, None)
                        if not (isinstance(ce, type) and issubclass(ce, BaseException)):
                            continue
                        for later in names:
                            cl = getattr(builtins, later, None)
                            if isinstance(cl, type) and issubclass(cl, BaseException) and issubclass(cl, ce):
                                shadow = True
                if shadow:
                    self.add(h, "shadowed-except", "high",
                             "unreachable except clause: the first matching clause wins, so a derived type "
                             "after a base class (or after 'except:'/'except Exception') is never executed; "
                             "put the derived classes before the bases (Tut p.68-69)")
                    break
            seen.append(names)

    def visit_Try(self, node):
        self._check_shadowed_handlers(node)
        for sub in _escapes_finally(node.finalbody):
            self.add(sub, "finally-flow", "medium",
                     "return/break/continue that leaves the 'finally': the Tutorial (p.73) says the pending exception is not "
                     "re-raised and that, since 3.14, the compiler emits a SyntaxWarning (PEP 765)")
        self.generic_visit(node)

    visit_TryStar = visit_Try

    # --- classes: __eq__ without __hash__ (Ref p.52-53, 109) ---
    def visit_ClassDef(self, node):
        names = {n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        assigned = {t.id for n in node.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
        if "__eq__" in names and "__hash__" not in names and "__hash__" not in assigned:
            self.add(node, "eq-without-hash", "medium",
                     "class defines __eq__ without __hash__: instances stop being hashable and cannot be used as a "
                     "dict key/set member (Ref p.52-53, 109)")
        self.generic_visit(node)

    # --- mutating the collection during iteration (Notes p.143, 643; Tut p.23-24) ---
    def visit_For(self, node):
        if isinstance(node.iter, ast.Name):
            target = node.iter.id
            for sub in ast.walk(ast.Module(body=node.body, type_ignores=[])):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute) \
                        and isinstance(sub.func.value, ast.Name) and sub.func.value.id == target \
                        and sub.func.attr in MUTATORS:
                    self.add(sub, "mutate-while-iterating", "high",
                             f"'{target}.{sub.func.attr}()' inside 'for ... in {target}': changing the collection during "
                             "iteration skips items or raises RuntimeError on dict/set; iterate over a copy or build "
                             "a new collection (Notes p.143, 643; Tut p.23-24)")
                if isinstance(sub, ast.Delete):
                    for t in sub.targets:
                        if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == target:
                            self.add(sub, "mutate-while-iterating", "high",
                                     f"'del {target}[...]' inside 'for ... in {target}' (Notes p.143, 643; Tut p.23-24)")
        self.generic_visit(node)

    # --- calls ---
    def visit_Call(self, node):
        name = call_name(node)
        last = name.split(".")[-1]
        if name in {"eval", "exec"}:
            self.add(node, "eval-exec", "medium",
                     f"{name}(): confirm where the string comes from; the Notes (p.505) state that it is not possible to use eval/exec "
                     "securely with untrusted user code (see references/fontes-comunitarias.md)")
        if name in {"pickle.load", "pickle.loads", "cPickle.load", "cPickle.loads"}:
            self.add(node, "pickle-load", "medium",
                     "pickle.load(s): only with trusted data: the Tutorial (p.66) says pickle is insecure by default and that "
                     "unpickling untrusted data can execute arbitrary code; the Notes (p.535) give the same warning")
        if last in {"run", "call", "check_call", "check_output", "Popen"} and name.startswith("subprocess"):
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.add(node, "shell-true", "medium",
                             "subprocess with shell=True: the Notes (p.434) say it raises security problems; "
                             "prefer an argument list (the list recommendation is the package's, [inference])")
        if name in {"hashlib.md5", "hashlib.sha1"}:
            self.add(node, "weak-hash", "low",
                     f"{name}: the Notes (p.694) list MD5/SHA1 without a warning; for security purposes, suitability should be "
                     "checked in the official documentation [to confirm]")
        self.generic_visit(node)


def scan_py2_text(path, lines):
    out = []
    for i, line in enumerate(lines, 1):
        code = line.split("#", 1)[0]
        for rx, rule, msg in PY2:
            if rx.search(code):
                out.append(dict(file=path, line=i, rule=rule, severity="high", message=msg, text=line.strip()[:140],
                                origin=RULES.get(rule, ("extrapolation", ""))[0], source=RULES.get(rule, ("", ""))[1]))
    return out


def scan_file(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            src = fh.read()
    except OSError as e:
        print(f"warning: could not read {path}: {e}", file=sys.stderr)
        return []
    lines = src.splitlines()
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        found = [dict(file=path, line=e.lineno or 1, rule="syntax-error", severity="high",
                      message=f"not valid Python 3 for this interpreter ({sys.version.split()[0]}): {e.msg}. "
                              "It may be Python 2 or syntax newer than this interpreter",
                      text=(e.text or "").strip()[:140], origin=RULES["syntax-error"][0], source=RULES["syntax-error"][1])]
        return found + scan_py2_text(path, lines)
    v = Visitor(path, lines)
    v.visit(tree)
    return v.findings


def main(argv):
    try:  # the Windows console uses cp1252 by default; force UTF-8
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    allf, n = [], 0
    for f in iter_files(a.paths):
        n += 1
        allf.extend(scan_file(f))
    order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    allf.sort(key=lambda d: (order[d["severity"]], d["file"], d["line"]))
    if a.json:
        json.dump(dict(files_scanned=n, python=sys.version.split()[0], findings=allf), sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0
    print(f"# Python scan (AST) — {n} .py file(s) — interpreter {sys.version.split()[0]} — {len(allf)} finding(s)")
    print("# Triage: it points to where to look; confirm each item by reading the code.\n")
    counts = {}
    for d in allf:
        counts[d["rule"]] = counts.get(d["rule"], 0) + 1
        print(f"[{d['severity']}] {d['file']}:{d['line']} {d['rule']}: {d['message']}")
        print(f"      rule origin: {d['origin']} | {d['source']}")
        if d["text"]:
            print(f"      {d['text']}")
    print("\n## Count by rule")
    for r, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"- {r}: {c}")
    print("\n## Warning: no findings is NOT approval")
    print("The scan does not cover: scope/closures in loops, logic, types, performance, concurrency, SQL built by string")
    print("formatting, or library misuse. Read the code.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
