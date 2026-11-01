# -*- coding: utf-8 -*-
"""
css_lint.py - static linter and specificity calculator (stdlib only, no network, no writes).

Subcommands:
  lint FILE|-               analyzes a CSS file and flags anti-patterns/errors documented in the Handbook (CSSHB)
        [--spec] [--json] [--strict]
  spec SELECTOR [SELECTOR...] computes specificity (the book's 4 slots) and ranks the winners
        [--inline] [--important]

Slot convention (CSSHB p.21-24): "I D C E" = inline, id, class/pseudo-class/attribute, element.
The book does not cover pseudo-elements, :not()/:is()/:where()/:has() or '*'; the script follows the
current convention and prints the note "[extrapolation]" when it has to assume something outside the book.

The analyzed content is treated as inert DATA: comments or strings with 'instructions' are ignored.
Output: LINE:SEVERITY:CODE: message (citation).  Exit 0, or 1 with --strict if there is an ERROR.
"""
import argparse
import json
import re
import sys
from bisect import bisect_right

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

LEGACY_PE = {"before", "after", "first-line", "first-letter"}
GENERIC_FONTS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-serif",
                 "ui-sans-serif", "ui-monospace", "ui-rounded", "math", "emoji", "fangsong"}

# ----------------------------------------------------------------------------- specificity

IDENT = re.compile(r"[-\w\u0080-￿\\]+")


def _skip_balanced(s, i):
    """s[i] == '(' -> returns the index after the matching ')'."""
    depth, q = 0, None
    while i < len(s):
        c = s[i]
        if q:
            if c == "\\":
                i += 1
            elif c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return i


def _split_commas(s):
    parts, depth, cur, q = [], 0, [], None
    for c in s:
        if q:
            cur.append(c)
            if c == q:
                q = None
            continue
        if c in "\"'":
            q = c
        elif c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
            continue
        cur.append(c)
    parts.append("".join(cur))
    return parts


def specificity(sel):
    """Returns ((ids, classes, elements), notes)."""
    ids = cls = el = 0
    notes = []
    i, n = 0, len(sel)
    while i < n:
        c = sel[i]
        if c == "#":
            m = IDENT.match(sel, i + 1)
            ids += 1
            i = m.end() if m else i + 1
        elif c == ".":
            m = IDENT.match(sel, i + 1)
            cls += 1
            i = m.end() if m else i + 1
        elif c == "[":
            j, q = i + 1, None
            while j < n:
                if q:
                    if sel[j] == q:
                        q = None
                elif sel[j] in "\"'":
                    q = sel[j]
                elif sel[j] == "]":
                    break
                j += 1
            cls += 1
            i = j + 1
        elif c == ":":
            double = i + 1 < n and sel[i + 1] == ":"
            m = IDENT.match(sel, i + (2 if double else 1))
            name = (m.group(0) if m else "").lower()
            i = m.end() if m else i + 1
            args = None
            if i < n and sel[i] == "(":
                end = _skip_balanced(sel, i)
                args = sel[i + 1:end - 1]
                i = end
            if double or name in LEGACY_PE:
                el += 1
                notes.append(f"pseudo-element ::{name} counted as an element [extrapolation]")
            elif name == "where":
                notes.append(":where() contributes 0 [extrapolation]")
            elif name in ("not", "is", "has", "matches") and args is not None:
                best = (0, 0, 0)
                for part in _split_commas(args):
                    sp, _ = specificity(part.strip())
                    best = max(best, sp)
                ids, cls, el = ids + best[0], cls + best[1], el + best[2]
                notes.append(f":{name}() counted by its most specific argument [extrapolation]")
            else:
                cls += 1
        elif c == "*" or c in " \t\r\n>+~,&|":
            i += 1
        else:
            m = IDENT.match(sel, i)
            if m:
                el += 1
                i = m.end()
            else:
                i += 1
    return (ids, cls, el), sorted(set(notes))


def fmt_spec(sp, inline=0, important=False):
    s = f"{inline} {sp[0]} {sp[1]} {sp[2]}"
    return s + ("  +!important" if important else "")


def cmd_spec(args):
    rows = []
    for idx, raw in enumerate(args.selectors):
        for part in _split_commas(raw):
            part = part.strip()
            if not part:
                continue
            sp, notes = specificity(part)
            rows.append((idx, part, sp, notes))
    if not rows:
        print("No selector provided.")
        return 1
    print("Slots (CSSHB p.21-24): inline | id | class/pseudo-class/attribute | element")
    for idx, part, sp, notes in rows:
        print(f"  [{idx + 1}] {part:40} -> {fmt_spec(sp, 1 if args.inline else 0, args.important)}")
        for nt in notes:
            print(f"        note: {nt}")
    if len(rows) > 1:
        key = lambda r: ((1 if args.inline else 0), r[2][0], r[2][1], r[2][2], r[0])
        win = max(rows, key=key)
        top = [r for r in rows if key(r)[:4] == key(win)[:4]]
        if len(top) > 1:
            print(f"Specificity tie: the rule that appears last wins (CSSHB p.21) -> [{win[0] + 1}] {win[1]}")
        else:
            print(f"The most specific wins (CSSHB p.21) -> [{win[0] + 1}] {win[1]}")
    return 0


# ----------------------------------------------------------------------------- simple CSS parser


class Node:
    def __init__(self, kind, prelude, line):
        self.kind, self.prelude, self.line = kind, prelude, line
        self.decls, self.children = [], []  # decls: (prop, value, line, raw)


class Parser:
    def __init__(self, text):
        self.t = text
        self.n = len(text)
        self.starts = [0] + [m.end() for m in re.finditer(r"\n", text)]
        self.problems = []  # (line, sev, code, msg)

    def line(self, pos):
        return bisect_right(self.starts, pos)

    def first_nonws(self, a, b):
        while a < b and self.t[a].isspace():
            a += 1
        return a

    def parse(self):
        _, nodes, _ = self.block(0, True)
        return nodes

    def block(self, i, top):
        t, n = self.t, self.n
        nodes, decls = [], []
        start, paren, quote = i, 0, None
        while i < n:
            c = t[i]
            if quote:
                if c == "\\":
                    i += 2
                    continue
                if c == quote:
                    quote = None
            elif c in "\"'":
                quote = c
            elif c == "(":
                paren += 1
            elif c == ")":
                paren = max(0, paren - 1)
            elif paren == 0 and c == "{":
                s = self.first_nonws(start, i)
                prelude = " ".join(t[start:i].split())
                node = Node("at" if prelude.startswith("@") else "rule", prelude, self.line(s))
                i, node.children, node.decls = self.block(i + 1, False)
                nodes.append(node)
                start = i
                continue
            elif paren == 0 and c == ";":
                self.chunk(start, i, top, nodes, decls)
                start = i + 1
            elif paren == 0 and c == "}":
                if not top:
                    self.chunk(start, i, top, nodes, decls)
                    return i + 1, nodes, decls
                self.problems.append((self.line(i), "ERROR", "stray-brace", "'}' without a matching '{'"))
                start = i + 1
            i += 1
        if not top:
            self.problems.append((self.line(max(0, start)), "ERROR", "unclosed-block", "block '{' without a closing '}'"))
        return i, nodes, decls

    def chunk(self, a, b, top, nodes, decls):
        raw = self.t[a:b]
        if not raw.strip():
            return
        s = self.first_nonws(a, b)
        ln = self.line(s)
        if top:
            if raw.strip().startswith("@"):
                node = Node("stmt", " ".join(raw.split()), ln)
                nodes.append(node)
            else:
                self.problems.append((ln, "ERROR", "stray-text", "text outside a rule (the browser would discard it)"))
            return
        clean = re.sub(r"\"[^\"]*\"|'[^']*'", '""', raw)
        clean = re.sub(r"url\([^)]*\)", "url()", clean)
        m = re.match(r"\s*([-\w]+)\s*:(.*)$", clean, re.S)
        if not m:
            self.problems.append((ln, "WARN", "decl-without-colon",
                                  f"declaration without 'property: value' ('{' '.join(raw.split())[:40]}'); it will be ignored (CSSHB p.205)"))
            return
        if re.search(r"\n[ \t]*[-\w]+[ \t]*:[ \t]*[^\s:]", m.group(2)) and not m.group(1).startswith("--"):
            self.problems.append((ln, "ERROR", "missing-semicolon",
                                  "possible missing ';': two declarations stuck together; the browser discards both (CSSHB p.205-206)"))
        prop = m.group(1).lower() if not m.group(1).startswith("--") else m.group(1)
        value = raw.split(":", 1)[1].strip()
        decls.append((prop, value, ln, raw))


def strip_comments(text):
    out, i, n, q = [], 0, len(text), None
    while i < n:
        c = text[i]
        if q:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == q:
                q = None
            i += 1
            continue
        if c in "\"'":
            q = c
            out.append(c)
            i += 1
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join(ch if ch == "\n" else " " for ch in text[i:j]))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


# ----------------------------------------------------------------------------- lint rules


def lint(text, show_spec=False):
    original_has_unclosed = text.count("/*") > text.count("*/")
    clean = strip_comments(text)
    P = Parser(clean)
    nodes = P.parse()
    issues = list(P.problems)
    if original_has_unclosed:
        issues.append((1, "ERROR", "unclosed-comment", "comment '/*' without '*/' (CSSHB p.54)"))

    for ln, line in enumerate(clean.splitlines(), 1):
        if re.match(r"\s*//", line):
            issues.append((ln, "ERROR", "comment-double-slash",
                           "'//' is not a comment in CSS; the next line may be discarded because of a syntax error; use /* */ (CSSHB p.54-55)"))
        if re.search(r"\$[A-Za-z_][\w-]*", line) and ":" in line and "url(" not in line:
            issues.append((ln, "WARN", "preprocessor-var",
                           "preprocessor variable ($name) in plain CSS is invalid [inference] (cf. CSSHB p.55-56, 210)"))

    defined, used = {}, []
    spec_rows = []
    seen_other = False

    def walk(ns, top):
        nonlocal seen_other
        for nd in ns:
            if top:
                if nd.kind == "stmt" and nd.prelude.lower().startswith("@import"):
                    if seen_other:
                        issues.append((nd.line, "ERROR", "import-not-at-top",
                                       "@import after other rules is ignored (CSSHB p.29)"))
                elif not (nd.kind == "stmt" and nd.prelude.lower().startswith(("@charset",))):
                    seen_other = True
            if nd.kind == "stmt":
                continue
            pre = nd.prelude
            low = pre.lower()
            if nd.kind == "at":
                if low.startswith("@media"):
                    if re.search(r"device-(width|height|aspect-ratio)", low):
                        issues.append((nd.line, "INFO", "media-device-width",
                                       "[DATED] device-width/height/aspect-ratio appear in the book (CSSHB p.169-170), but were superseded by width/height [extrapolation]"))
                if low.startswith("@-"):
                    issues.append((nd.line, "INFO", "vendor-prefix",
                                   "at-rule with a vendor prefix; prefer Autoprefixer (CSSHB p.206-208)"))
                decl_checks(nd, is_rule=False)
                if low.startswith(("@keyframes", "@-webkit-keyframes", "@font-face", "@page")):
                    continue
                walk(nd.children, False)
                continue
            # style rule
            if pre.startswith("//"):
                issues.append((nd.line, "WARN", "rule-invalidated-by-double-slash",
                               "the selector starts with '//' (fake comment); the browser discards this whole rule (CSSHB p.54-55)"))
                decl_checks(nd, is_rule=False)
                walk(nd.children, False)
                continue
            sels = [s.strip() for s in _split_commas(pre) if s.strip()]
            for s in sels:
                sp, notes = specificity(s)
                spec_rows.append((nd.line, s, sp))
                if sp[0] > 0:
                    issues.append((nd.line, "INFO", "id-selector",
                                   f"'{s}' uses an id (high specificity); the book recommends classes (CSSHB p.25)"))
                if re.search(r"(?<!:):(before|after|first-line|first-letter)\b", s):
                    issues.append((nd.line, "INFO", "pseudo-element-single-colon",
                                   f"'{s}': use '::' for pseudo-elements; a single colon exists only for compatibility (CSSHB p.34)"))
            decl_checks(nd, is_rule=True)
            walk(nd.children, False)

    def decl_checks(nd, is_rule):
        props = {}
        for prop, value, ln, _ in nd.decls:
            props.setdefault(prop, []).append((value, ln))
            v = value
            if prop.startswith("--"):
                defined[prop] = ln
            for m in re.finditer(r"var\(\s*(--[^\s,)]+)\s*(,)?", v):
                used.append((m.group(1), bool(m.group(2)), ln))
            if re.search(r"!\s*important", v, re.I):
                issues.append((ln, "WARN", "important",
                               f"'{prop}' uses !important; the book recommends avoiding it and controlling specificity (CSSHB p.24-25)"))
            if prop.startswith(("-webkit-", "-moz-", "-ms-", "-o-")):
                issues.append((ln, "INFO", "vendor-prefix",
                               f"'{prop}' is a vendor prefix; a declining practice, use Autoprefixer (CSSHB p.206-208)"))
            if prop in ("grid-gap", "grid-column-gap", "grid-row-gap"):
                issues.append((ln, "INFO", "grid-gap-dated",
                               f"[DATED] '{prop}' appears in the book (CSSHB p.129-131); today gap/column-gap/row-gap [extrapolation]"))
            if prop.startswith("page-break-"):
                issues.append((ln, "INFO", "page-break-dated",
                               f"[DATED] '{prop}' in the book (CSSHB p.211-212); replaced by break-* [extrapolation]"))
            if prop == "font-family":
                items = [x.strip().strip("'\"").lower() for x in _split_commas(re.sub(r"!\s*important", "", v, flags=re.I))]
                if items and not any(x in GENERIC_FONTS for x in items) and not re.match(r"(var\(|inherit|initial|unset|revert)", items[0]):
                    issues.append((ln, "INFO", "font-no-generic",
                                   "font-family without a generic family at the end (serif/sans-serif/monospace...) (CSSHB p.66-67)"))
            for m in re.finditer(r"calc\(", v):
                end = _skip_balanced(v, m.end() - 1)
                inner = v[m.end():end - 1]
                inner = re.sub(r"var\([^)]*\)", "V", inner)
                inner = re.sub(r"[a-z]+(?:-[a-z]+)+", "ID", inner, flags=re.I)
                if re.search(r"[0-9a-zA-Z%)][+-](?=[0-9a-zA-Z(.])", inner) or re.search(r"[0-9a-zA-Z%)]\s[+-](?=[0-9a-zA-Z(.])", inner):
                    issues.append((ln, "ERROR", "calc-spaces",
                                   f"calc({inner.strip()}): the spaces around the + and - operators are mandatory (CSSHB p.49)"))
            if re.search(r"\b(blur|brightness|contrast|grayscale|hue-rotate|invert|sepia|saturate|drop-shadow)\(\s*\)", v):
                issues.append((ln, "WARN", "filter-no-argument",
                               "filter function without an argument (like the book's example on p.182) (CSSHB p.180-182)"))
        if not is_rule:
            return
        pnames = set(props)
        if "z-index" in pnames and "position" not in pnames:
            ln = props["z-index"][0][1]
            issues.append((ln, "WARN", "z-index-without-position",
                           "z-index without position in the same rule: in the book it only works with relative/absolute/fixed (CSSHB p.122); "
                           "flex/grid items also honor z-index [extrapolation]"))
        border_parts = [p for p in pnames if re.fullmatch(r"border(-(top|right|bottom|left))?-(width|color)", p)]
        if border_parts and not any(p in pnames for p in ("border", "border-style", "border-top", "border-right", "border-bottom",
                                                           "border-left", "border-top-style", "border-right-style",
                                                           "border-bottom-style", "border-left-style")):
            issues.append((props[border_parts[0]][0][1], "WARN", "border-without-style",
                           "border-width/color without border-style: the default style is none and the border does not show (CSSHB p.87); "
                           "check whether another rule sets the style"))
        mg = props.get("margin")
        auto_h = False
        if mg:
            vals = mg[-1][0].split()
            auto_h = (len(vals) == 2 and vals[1] == "auto") or (len(vals) in (3, 4) and vals[1] == "auto" and (len(vals) == 3 or vals[3] == "auto"))
        if "margin-left" in props and "margin-right" in props and props["margin-left"][-1][0] == "auto" and props["margin-right"][-1][0] == "auto":
            auto_h = True
        if auto_h and not any(p in pnames for p in ("width", "max-width", "min-width")) and \
                not any(p in pnames for p in ("display",)):
            ln = (mg or props.get("margin-left"))[-1][1]
            issues.append((ln, "INFO", "margin-auto-without-width",
                           "horizontal margin auto only centers with a defined width (and display:block if inline) (CSSHB p.164)"))
        pe = [s for s in _split_commas(nd.prelude) if re.search(r"::?(before|after)\b", s)]
        if pe and "content" not in pnames:
            issues.append((nd.line, "WARN", "pseudo-without-content",
                           "::before/::after without a content property generate nothing (CSSHB p.34-36) [inference: the rule may be in another block]"))

    walk(nodes, True)

    for name, has_fb, ln in used:
        if name not in defined:
            ci = [d for d in defined if d.lower() == name.lower()]
            if ci:
                issues.append((ln, "ERROR", "var-case",
                               f"var({name}) does not match {ci[0]}: custom properties are case sensitive (CSSHB p.62)"))
            elif not has_fb:
                issues.append((ln, "INFO", "var-undefined",
                               f"var({name}) has no definition in this file and no fallback value (CSSHB p.56-63); it may come from another file or from JS"))

    all_decls = []

    def collect(ns):
        for nd in ns:
            all_decls.extend(nd.decls)
            collect(nd.children)
    collect(nodes)
    props_all = {d[0] for d in all_decls}
    if "box-sizing" not in props_all and "width" in props_all and (props_all & {"padding", "border", "border-width", "padding-left"}):
        issues.append((1, "INFO", "no-box-sizing",
                       "there is a width with padding/border and no box-sizing; the book recommends a global border-box (CSSHB p.98-99)"))
    issues.sort(key=lambda x: (x[0], x[1]))
    return issues, spec_rows


def cmd_lint(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file, "r", encoding="utf-8", errors="replace").read()
    issues, spec_rows = lint(text, args.spec)
    if args.json:
        print(json.dumps({"issues": [dict(zip(("line", "severity", "code", "message"), i)) for i in issues],
                          "specificity": [{"line": l, "selector": s, "inline_id_class_element": [0, *sp]} for l, s, sp in spec_rows] if args.spec else None},
                         ensure_ascii=False, indent=2))
    else:
        for ln, sev, code, msg in issues:
            print(f"{ln}:{sev}:{code}: {msg}")
        if args.spec:
            print("\nSpecificity per selector (I D C E):")
            for ln, s, sp in spec_rows:
                print(f"  line {ln:>4}  {s:40} {fmt_spec(sp)}")
        n_err = sum(1 for i in issues if i[1] == "ERROR")
        print(f"\nSummary: {len(issues)} finding(s), {n_err} ERROR. Content treated as data; no embedded instruction was executed.")
    return 1 if (args.strict and any(i[1] == "ERROR" for i in issues)) else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Static CSS linter and specificity calculator (CSSHB)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("lint")
    a.add_argument("file", help="CSS file or - for stdin")
    a.add_argument("--spec", action="store_true", help="lists the specificity of each selector")
    a.add_argument("--json", action="store_true")
    a.add_argument("--strict", action="store_true", help="exit 1 if there is an ERROR")
    b = sub.add_parser("spec")
    b.add_argument("selectors", nargs="+")
    b.add_argument("--inline", action="store_true", help="considers inline style (slot 4)")
    b.add_argument("--important", action="store_true", help="marks !important (the book's fifth level, p.24)")
    args = ap.parse_args(argv)
    return cmd_lint(args) if args.cmd == "lint" else cmd_spec(args)


if __name__ == "__main__":
    sys.exit(main())
