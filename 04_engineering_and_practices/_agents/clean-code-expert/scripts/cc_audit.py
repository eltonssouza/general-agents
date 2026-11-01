# -*- coding: utf-8 -*-
"""
cc_audit.py - heuristic code auditor based on "Código Limpo" (Clean Code, Robert C. Martin). Flags
CANDIDATE smells that simple syntactic analysis can see and links each finding to the heuristic (ch. 17)
or to the book topic, with the PDF page. It is not a full linter nor a verdict: the reviewer decides.

Reads the code as TEXT (never executes it). Read-only, no network. Languages: Java, C#, JavaScript,
TypeScript (brace blocks) and Python (indentation blocks).

Usage:
  python -I cc_audit.py File.java [other.py ...]
  python -I cc_audit.py - --lang java < snippet.txt     reads from standard input
  python -I cc_audit.py file.ts --min MEDIUM             only MEDIUM and HIGH findings
                                                         (ALTO/MEDIO/BAIXO are accepted too)
Output: SEVERITY file:line CODE title (CL p.N) - detail.
Exit: 0 no findings, 1 findings, 2 usage/read error.
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

HERE = os.path.dirname(os.path.abspath(__file__))
SEV = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
SEV_ALIAS = {"BAIXO": "LOW", "MEDIO": "MEDIUM", "ALTO": "HIGH"}  # Portuguese spellings accepted by --min
EXT = {".java": "java", ".cs": "csharp", ".js": "js", ".jsx": "js", ".mjs": "js", ".ts": "ts", ".tsx": "ts", ".py": "python"}

# Limits taken from the book; "ref" points to cc_smells.json (code) or cc_index.json (topic).
LIMITS = {
    "args_avoid": 3,          # three arguments: avoid whenever possible
    "func_lines": 20,         # functions: rarely more than 20 lines
    "nesting": 2,             # indentation level of a function: at most one or two
    "line_width": 120,        # the author's line width limit
    "file_lines": 500,        # files of ~200 lines, limit ~500 (the book says it is not a fixed rule)
}

# (rule, reference)
RULES = {
    "args": ("smell", "F1"),
    "flag": ("smell", "F3"),
    "long_func": ("topic", "tamanho-de-funcoes"),
    "nesting": ("topic", "tamanho-de-funcoes"),
    "commented_code": ("smell", "C5"),
    "magic": ("smell", "G25"),
    "negative_cond": ("smell", "G29"),
    "switch": ("smell", "G23"),
    "transitive": ("smell", "G36"),
    "return_null": ("topic", "nao-retornar-null"),
    "encoding": ("smell", "N6"),
    "brace_comment": ("topic", "comentarios-ruins"),
    "line_width": ("topic", "formatacao-horizontal"),
    "file_size": ("topic", "formatacao-vertical"),
    "duplication": ("smell", "G5"),
}

CTRL = {"if", "for", "while", "switch", "catch", "return", "new", "else", "do", "try", "synchronized",
        "using", "lock", "foreach", "throw", "function", "await", "typeof", "sizeof", "with"}
SIG_BRACE = re.compile(
    r"^\s*(?:@\w+(?:\([^)]*\))?\s+)*(?:(?:public|private|protected|internal|static|final|abstract|synchronized|"
    r"async|override|virtual|export|default|readonly|sealed|extern|unsafe|partial)\s+)*"
    r"(?:function\s*\*?\s*)?(?:[\w<>\[\],.?]+\s+)?(\w+)\s*(?:<[^>]*>)?\s*\(([^()]*)\)\s*"
    r"(?::\s*[\w<>\[\],.?| ]+)?\s*(?:throws\s+[\w.,\s]+)?\s*\{")
SIG_ARROW = re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^()]*)\)\s*(?::\s*[\w<>\[\]|]+)?\s*=>\s*\{")
SIG_PY = re.compile(r"^(\s*)(?:async\s+)?def\s+(\w+)\s*\((.*)\)\s*(?:->\s*[^:]+)?:\s*(?:#.*)?$")
CODEISH = re.compile("|".join([
    r";\s*$",                                                       # ends with ;
    r"^\s*[{}]\s*$",                                                # lone brace
    r"^\s*(if|for|while|return|else|int|long|double|float|String|var|let|const|def|import|print|"
    r"System\.out|console\.log|public|private|try|catch)\b.*[(=;:{]",  # starts with a keyword
    r"^\s*[\w.\[\]]+\s*[-+*/]?=\s*[\w.\[\]]+\s*\(.*\)\s*$",         # assignment with a call
    r"^\s*[\w.]+\([^()]*\)\s*$",                                    # bare call
]))
NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?[fFdDlL]?(?![\w.])")
CONST_DECL = re.compile(r"\b(static\s+final|const|final|readonly|enum)\b|^\s*[A-Z][A-Z0-9_]+\s*=")
TRANSITIVE = re.compile(r"\w+\s*\([^()]*\)\s*\.\s*\w+\s*\([^()]*\)\s*\.\s*\w+\s*\(")
HUNGARIAN = re.compile(r"\b(m_\w+|(?:str|int|lng|dbl|bln|arr|obj|sz)[A-Z]\w*)\b")
IFACE_I = re.compile(r"\binterface\s+(I[A-Z]\w*)")
BRACE_COMMENT = re.compile(r"\}\s*//\s*(end|fim|if|else|while|for|try|switch|class|method)\b", re.I)


def load_refs():
    def j(name):
        try:
            with open(os.path.join(HERE, name), encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}
    smells = {s["code"]: s for s in j("cc_smells.json").get("smells", [])}
    topics = j("cc_index.json").get("topics", {})
    return smells, topics


def ref_label(rule, smells, topics):
    kind, key = RULES[rule]
    if kind == "smell" and key in smells:
        return "%s %s (CL p.%s)" % (key, smells[key].get("title_en") or smells[key]["title"], smells[key]["page"])
    if kind == "topic" and key in topics:
        return "%s (CL %s)" % (topics[key]["name"], topics[key]["citation"].replace("CL ", ""))
    return "%s (page not indexed)" % key


def strip_strings(line):
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`[^`]*`', '""', line)


def split_params(params):
    p = re.sub(r"<[^<>]*>", "", params)
    p = re.sub(r"\[[^\[\]]*\]", "", p)
    out = [x.strip() for x in p.split(",") if x.strip()]
    return [x for x in out if x not in ("self", "cls", "*", "/") and not x.startswith("**") and x != "this"]


def is_flag(param, lang):
    if lang == "python":
        return bool(re.search(r":\s*bool\b|=\s*(True|False)\b", param))
    if lang == "ts":
        return bool(re.search(r":\s*boolean\b", param))
    return bool(re.match(r"(final\s+)?(boolean|bool|Boolean)\s+\w+", param))


def comment_of(line, lang):
    if lang == "python":
        m = re.match(r"^\s*#\s?(.*)$", line)
    else:
        m = re.match(r"^\s*//\s?(.*)$", line)
    return m.group(1) if m else None


def functions(lines, lang):
    """Return (name, start_line, params, body_lines, max_depth)."""
    found = []
    if lang == "python":
        for i, l in enumerate(lines):
            m = SIG_PY.match(l)
            if not m:
                continue
            base = len(m.group(1))
            body, depth_levels = [], []
            for k in range(i + 1, len(lines)):
                t = lines[k]
                if not t.strip() or t.strip().startswith("#"):
                    continue
                ind = len(t) - len(t.lstrip())
                if ind <= base:
                    break
                body.append(k)
                depth_levels.append(ind)
            depth = 0
            if depth_levels:
                b = min(depth_levels)
                steps = sorted({d - b for d in depth_levels if d > b})
                unit = steps[0] if steps else 4
                depth = max((d - b) // unit for d in depth_levels)
            found.append((m.group(2), i + 1, m.group(3), len(body), depth))
        return found
    for i, l in enumerate(lines):
        s = strip_strings(l)
        m = SIG_BRACE.match(s) or SIG_ARROW.match(s)
        if not m or m.group(1) in CTRL:
            continue
        depth, maxd, count, end = 0, 0, 0, None
        for k in range(i, len(lines)):
            t = strip_strings(lines[k]).split("//")[0]
            for ch in t:
                if ch == "{":
                    depth += 1
                    maxd = max(maxd, depth)
                elif ch == "}":
                    depth -= 1
            if k > i and t.strip() and t.strip() != "}":
                count += 1
            if depth <= 0 and k >= i and "{" in strip_strings(lines[i]):
                end = k
                break
        if end is None:
            continue
        found.append((m.group(1), i + 1, m.group(2), count, max(0, maxd - 1)))
    return found


def audit(path, text, lang, smells, topics):
    lines = text.splitlines()
    out = []

    def add(sev, ln, rule, detail):
        out.append((SEV[sev], sev, ln, ref_label(rule, smells, topics), detail))

    for name, ln, params, size, depth in functions(lines, lang):
        ps = split_params(params)
        if len(ps) > LIMITS["args_avoid"]:
            add("HIGH", ln, "args", "'%s' has %d arguments (book: ideal 0; 1-2 ok; 3 avoid; more than 3 needs very special justification)" % (name, len(ps)))
        elif len(ps) == LIMITS["args_avoid"]:
            add("MEDIUM", ln, "args", "'%s' has 3 arguments (triad: avoid when possible)" % name)
        flags = [p for p in ps if is_flag(p, lang)]
        if flags:
            add("MEDIUM", ln, "flag", "'%s' takes a boolean argument (%s): a sign it does more than one thing" % (name, ", ".join(flags)))
        if size > LIMITS["func_lines"]:
            add("MEDIUM", ln, "long_func", "'%s' has %d body lines (book: rarely more than %d)" % (name, size, LIMITS["func_lines"]))
        if depth > LIMITS["nesting"]:
            add("MEDIUM", ln, "nesting", "'%s' reaches %d levels of nesting (book: at most one or two)" % (name, depth))

    run = []
    for i, l in enumerate(lines + [""]):
        c = comment_of(l, lang) if i < len(lines) else None
        if c is not None and CODEISH.search(c):
            run.append(i + 1)
            continue
        if run:
            add("MEDIUM", run[0], "commented_code", "%d line(s) of commented-out code: delete it (version control keeps the history)" % len(run))
            run = []

    seen = {}
    for i, l in enumerate(lines, 1):
        s = strip_strings(l)
        code = s.split("#")[0] if lang == "python" else s.split("//")[0]
        if not code.strip() or comment_of(l, lang) is not None:
            continue
        if len(l.rstrip("\n")) > LIMITS["line_width"]:
            add("LOW", i, "line_width", "line with %d characters (author's limit: %d)" % (len(l), LIMITS["line_width"]))
        if not CONST_DECL.search(code) and not re.match(r"^\s*(import|package|using|from|#)", code):
            nums = [n for n in NUM.findall(code) if n.lstrip("-").rstrip("fFdDlL") not in ("0", "1", "2", "0.0", "1.0")]
            if nums:
                add("LOW", i, "magic", "literal number(s) %s: consider a named constant" % ", ".join(sorted(set(nums))))
        if re.search(r"\bif\s*\(\s*!\s*\w|\bif\s+not\s+\w", code):
            add("LOW", i, "negative_cond", "negative conditional: prefer the positive form when possible")
        if re.search(r"\bswitch\s*\(|^\s*match\s+\w+.*:\s*$", code):
            add("LOW", i, "switch", "switch/match: check whether polymorphism would be better (one switch per type, hidden in a factory)")
        if TRANSITIVE.search(code):
            add("MEDIUM", i, "transitive", "call chain (train wreck): possible Law of Demeter violation")
        if lang != "python" and re.search(r"\breturn\s+null\s*;", code):
            add("MEDIUM", i, "return_null", "returns null: consider an exception or a special case object")
        if HUNGARIAN.search(code) or IFACE_I.search(code):
            m = HUNGARIAN.search(code) or IFACE_I.search(code)
            add("LOW", i, "encoding", "name with encoding/prefix ('%s')" % m.group(1))
        if BRACE_COMMENT.search(l):
            add("LOW", i, "brace_comment", "closing brace comment: a sign of a function that is too long")
        key = re.sub(r"\s+", " ", code.strip())
        if len(key) >= 25 and not re.match(r"^(import|package|using|from|return;|\}|@)", key):
            seen.setdefault(key, []).append(i)
    for key, where in seen.items():
        if len(where) >= 3:
            add("LOW", where[0], "duplication", "line repeated %d times (lines %s): candidate for extraction" % (len(where), ", ".join(map(str, where[:6]))))
    if len(lines) > LIMITS["file_lines"]:
        add("LOW", 1, "file_size", "file with %d lines (book: large systems can be built with files of ~200 lines and a limit of ~%d; not a fixed rule)" % (len(lines), LIMITS["file_lines"]))
    return sorted(out, key=lambda x: (x[2], -x[0]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="code files, or - for standard input")
    ap.add_argument("--lang", choices=sorted(set(EXT.values())), help="required with -; otherwise taken from the extension")
    ap.add_argument("--min", choices=list(SEV) + list(SEV_ALIAS), default="LOW", type=lambda v: v.upper(),
                    help="minimum severity shown (LOW, MEDIUM, HIGH; ALTO/MEDIO/BAIXO also accepted)")
    a = ap.parse_args(argv)
    smells, topics = load_refs()
    total = 0
    for path in a.files:
        if path == "-":
            if not a.lang:
                print("Error: use --lang with standard input.")
                return 2
            # Explicit UTF-8: on Windows, with -I, standard input would be read as cp1252
            text, lang, label = sys.stdin.buffer.read().decode("utf-8", errors="replace"), a.lang, "<stdin>"
        else:
            lang = a.lang or EXT.get(os.path.splitext(path)[1].lower())
            if not lang:
                print("Error: unsupported language for %s (use --lang)." % path)
                return 2
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError as e:
                print("Error reading %s: %s" % (path, e))
                return 2
            label = path
        minsev = SEV_ALIAS.get(a.min, a.min)
        found = [f for f in audit(label, text, lang, smells, topics) if f[0] >= SEV[minsev]]
        for _, sev, ln, ref, detail in found:
            print("%-6s %s:%d %s - %s" % (sev, label, ln, ref, detail))
        total += len(found)
    print("\n%d candidate(s). Syntactic heuristic [inference] over [from source] rules: confirm each finding by reading the code;"
          " what the script cannot see (bad names, a function that does more than one thing, mixed levels of abstraction) requires judgment." % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
