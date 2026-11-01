# -*- coding: utf-8 -*-
"""
gradle_trace.py - execution order of the 'java' plugin tasks and check for loose code in a task body.

ORIGIN OF THE RULES (audit):
- The java plugin task graph (compileJava -> classes -> jar -> assemble ...) is an ILLUSTRATION [extrapolation]:
  the names appear in the book's outputs (GRADLE p.44-47, 75), but the full graph is not in the sources and changes with the
  Gradle and plugin versions. The GRADLE PDF describes Gradle 2.3 (2015).
- "Executable code in the task body runs in the configuration phase" is [extrapolation] (general Gradle knowledge; the PDF
  does not describe the initialization/configuration/execution phases). Partial basis in the book: the examples put println inside
  '<<'/doLast (GRADLE p.13, 16).
- The '<<' operator is the short form of doLast in Gradle 2.3 (GRADLE p.13) [from source] and was removed later [DATED][extrapolation].
v1 simulated "BUILD SUCCESSFUL", marked tasks as UP-TO-DATE in an invented way and cited the phases at GRADLE p.10-16;
those simulations were removed.

Usage:
  python -I scripts/gradle_trace.py order --task build
  python -I scripts/gradle_trace.py check --code-snippet "task deploy { println 'x' }"
  python -I scripts/gradle_trace.py check --file build.gradle
  python -I scripts/gradle_trace.py phases
Exit: 0 no alert; 1 configuration alert; 2 invalid input.
"""
import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# [extrapolation] illustration of the java plugin; not the official graph of any version
JAVA_TASKS = {
    "clean": [],
    "compileJava": [],
    "processResources": [],
    "classes": ["compileJava", "processResources"],
    "compileTestJava": ["classes"],
    "processTestResources": [],
    "testClasses": ["compileTestJava", "processTestResources"],
    "test": ["classes", "testClasses"],
    "jar": ["classes"],
    "assemble": ["jar"],
    "check": ["test"],
    "build": ["check", "assemble"],
}

EXEC_HINTS = re.compile(r"^(println|print|printf|exec|sh|new\s+\w|System\.|ant\.|\w+\.execute\(|file\(.*\)\.(delete|write|text)|Runtime\.)")
CONFIG_OK = re.compile(r"^(description|group|dependsOn|inputs|outputs|enabled|onlyIf|mustRunAfter|finalizedBy|shouldRunAfter|type|ext|project\.ext)\b")


def resolve(task, seen=None, stack=None):
    if seen is None:
        seen, stack = [], []
    if task in stack:
        raise ValueError("cycle detected: " + " -> ".join(stack + [task]))
    if task in seen:
        return seen
    if task not in JAVA_TASKS:
        raise KeyError(task)
    stack.append(task)
    for d in JAVA_TASKS[task]:
        resolve(d, seen, stack)
    stack.pop()
    seen.append(task)
    return seen


def strip_comments_strings(src):
    """replaces strings with 's' and removes comments, preserving line breaks."""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("//", i):
            while i < n and src[i] != "\n":
                i += 1
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("\n" * src[i:j].count("\n"))
            i = j
            continue
        if c in "'\"":
            q = c
            j = i + 1
            while j < n and src[j] != q:
                if src[j] == "\\":
                    j += 1
                j += 1
            out.append(q + "s" + q)
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def find_task_bodies(src):
    """-> list of (name, uses_shift_left, body_text, start_line)"""
    res = []
    for m in re.finditer(r"(?m)^\s*task\s+(\w+)\s*(\([^)]*\))?\s*(<<)?\s*\{", src):
        name, shift = m.group(1), bool(m.group(3))
        start = m.end()
        depth, i = 1, start
        while i < len(src) and depth:
            if src[i] == "{":
                depth += 1
            elif src[i] == "}":
                depth -= 1
            i += 1
        body = src[start:i - 1]
        line = src.count("\n", 0, m.start()) + 1
        res.append((name, shift, body, line))
    return res


def top_level_statements(body):
    """body lines at level 1 (outside nested blocks such as doLast { })"""
    depth = 0
    cur = []
    stmts = []
    for ch in body:
        if ch == "{":
            depth += 1
            if depth == 1:
                cur.append("{")
                continue
        if ch == "}":
            depth -= 1
            continue
        if depth == 0:
            if ch == "\n":
                stmts.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
    if cur:
        stmts.append("".join(cur).strip())
    return [s for s in stmts if s]


def check(src):
    clean = strip_comments_strings(src)
    alerts, notes = [], []
    for name, shift, body, line in find_task_bodies(clean):
        if shift:
            notes.append("task '%s' (line %d): uses '<<' (short form of doLast in Gradle 2.3, GRADLE p.13 [from source]); "
                         "it was removed in later versions [DATED][extrapolation]; prefer doLast." % (name, line))
            continue
        for st in top_level_statements(body):
            if st.endswith("{") or CONFIG_OK.match(st) or re.match(r"^\w+\s*=", st):
                continue
            if EXEC_HINTS.match(st):
                alerts.append("task '%s' (line %d): '%s ...' sits outside doLast/doFirst and runs at CONFIGURATION time on every build "
                              "[extrapolation]; move it into doLast { ... }." % (name, line, re.split(r"[\s(]", st, maxsplit=1)[0]))
    if re.search(r"(?m)^\s*(compile|testCompile|runtime)\s+['\"]", src):
        notes.append("'compile'/'testCompile' configurations are from Gradle 2.3 (the book uses them, GRADLE p.25) [DATED]; "
                     "later versions use other configurations [extrapolation]; check the current documentation.")
    return alerts, notes


def main():
    ap = argparse.ArgumentParser(description="Java plugin task order (illustration) and check for code in a task body")
    sub = ap.add_subparsers(dest="cmd")
    o = sub.add_parser("order")
    o.add_argument("--task", default="build")
    c = sub.add_parser("check")
    c.add_argument("--code-snippet")
    c.add_argument("--file")
    sub.add_parser("phases")
    # v1 compatibility
    ap.add_argument("--task", dest="v1_task")
    ap.add_argument("--code-snippet", dest="v1_snippet")
    a = ap.parse_args()

    if a.cmd == "phases":
        print("Gradle build phases [extrapolation]: the GRADLE PDF (Gradle 2.3) does NOT describe them.")
        print("1. Initialization: decides which projects take part (settings.gradle).")
        print("2. Configuration: runs the build scripts and builds the task graph.")
        print("3. Execution: runs the actions (doFirst/doLast) of the requested tasks and their dependencies.")
        print("What the book shows: '<<' is the short form of doLast (GRADLE p.13); dependsOn (p.16); DAG (p.7) [from source].")
        return 0

    if a.cmd == "order" or (a.cmd is None and a.v1_task):
        task = a.task if a.cmd == "order" else a.v1_task
        try:
            order = resolve(task)
        except KeyError:
            print("task '%s' is outside the java plugin illustration (%s)." % (task, ", ".join(sorted(JAVA_TASKS))))
            print("NOT COVERED in the package: the real graph depends on the Gradle version and plugins.")
            return 2
        print("Order (ILLUSTRATION of the java plugin [extrapolation]; DAG: GRADLE p.7 [from source]) for ':%s':" % task)
        for i, t in enumerate(order, 1):
            print("  %d. :%s" % (i, t))
        if a.cmd is None and a.v1_snippet:
            return run_check(a.v1_snippet)
        return 0

    if a.cmd == "check" or (a.cmd is None and a.v1_snippet):
        if a.cmd == "check":
            if a.file:
                try:
                    src = open(a.file, encoding="utf-8").read()
                except OSError as e:
                    print("error reading file: %s" % e, file=sys.stderr)
                    return 2
            elif a.code_snippet:
                src = a.code_snippet
            else:
                print("provide --code-snippet or --file", file=sys.stderr)
                return 2
        else:
            src = a.v1_snippet
        return run_check(src)

    ap.print_help()
    return 2


def run_check(src):
    alerts, notes = check(src)
    print("TASK BODY CHECK [extrapolation; the book's examples use println inside <</doLast: GRADLE p.13, 16]")
    if not alerts:
        print("- no loose executable code detected in the task bodies")
    for x in alerts:
        print("- ALERT: " + x)
    for x in notes:
        print("- NOTE: " + x)
    return 1 if alerts else 0


if __name__ == "__main__":
    sys.exit(main())
