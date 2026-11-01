# -*- coding: utf-8 -*-
"""
swift_lint.py - STATIC, heuristic linter for Swift snippets, backed by "A Swift Tour" (SWT; Swift version
NOT stated; 2026 capture). It never compiles or runs the code; it only reads the file (or stdin with "-"). stdlib, no network.

Each finding carries its origin:
  [from source]    the tour says so on the cited page (SWT p.N);
  [inference]      direct deduction from the tour (e.g. the "remove the default" experiment); the page is given;
  [extrapolation]  NOT in the tour (outside knowledge); rule marked as such, severity only "info"/"warning".
It is regex plus brace counting, NOT a parser: false positives and negatives are possible. No findings does not prove
that the code compiles. To really validate, use the compiler (out of scope and outside the collection).

Usage:
  python -I scripts/swift_lint.py FILE.swift [FILE2 ...] [--json] [--no-info]
  python -I scripts/swift_lint.py --rules
  cat x.swift | python -I scripts/swift_lint.py -
Output: exit 0 with no findings (or only info), exit 1 if there is an error/warning, 2 for incorrect usage.
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

RULES = {
    "SWF-01": ("error", "from source", "SWT p.1", "constant (let) assigned more than once: it must receive a value exactly once"),
    "SWF-02": ("error", "from source", "SWT p.3", "if/while condition that is not Boolean (e.g. `if score {`) is an error, not an implicit comparison with zero"),
    "SWF-03": ("error", "from source", "SWT p.3", "braces around the body of if/for/while are required"),
    "SWF-04": ("warning", "inference", "SWT p.5", "switch without default (the tour proposes removing the default and seeing the error; enum exhaustiveness may make it unnecessary)"),
    "SWF-05": ("info", "from source", "SWT p.5", "break at the end of a case is not needed (execution does not fall into the next case)"),
    "SWF-06": ("error", "from source", "SWT p.3", "empty array/dictionary in a new variable without a type: the type must be specified"),
    "SWF-07": ("error", "from source", "SWT p.2", "implicit conversion between types (String + number, Int with Double): convert explicitly"),
    "SWF-08": ("error", "from source", "SWT p.9", "method that overrides the superclass without `override`"),
    "SWF-09": ("error", "from source", "SWT p.9", "`override` on a method that does not exist in the superclass"),
    "SWF-10": ("warning", "from source", "SWT p.9", "stored property without a value and without init in the class: every property needs a value"),
    "SWF-11": ("warning", "from source+inference", "SWT p.16", "struct/enum/extension method that modifies its own value without `mutating`"),
    "SWF-12": ("error", "from source", "SWT p.17", "call to a function that `throws` without `try`"),
    "SWF-13": ("error", "from source", "SWT p.14", "call to an `async` function without `await`"),
    "SWF-14": ("error", "from source+inference", "SWT p.15-16", "type declares conformance to a local protocol but does not implement a requirement"),
    "SWF-15": ("info", "from source", "SWT p.1", "semicolon at the end of the statement is not needed"),
    "SWF-16": ("info", "from source", "SWT p.1", "`func main()` is not needed: code in the global scope is the entry point"),
    "SWF-17": ("warning", "from source", "SWT p.15", "access to an actor instance method/property without `await`"),
    "SWF-18": ("info", "extrapolation", "SWT p.3", "parentheses around the condition: optional in the tour; removing them is a matter of style"),
    "SWF-19": ("warning", "inference", "SWT p.4, 11", "member accessed directly on an optional variable (the tour uses if let, ?? or ?.)"),
    "SWF-X1": ("info", "extrapolation", "outside the tour", "forced unwrapping `!` or `try!`: not covered by the tour; risk of a runtime failure"),
    "SWF-X2": ("warning", "extrapolation", "outside the tour (the tour uses += on SWT p.3 and 6)", "`++`/`--`: the tour only shows `+=`/`-=`; increment operators are not covered"),
    "SWF-X3": ("warning", "extrapolation", "outside the tour (the tour uses for-in and ranges on SWT p.3-6)", "C-style for loop `for (i = 0; ...; ...)`: the tour only shows for-in, while and repeat-while"),
}
KW = {"let", "var", "case", "true", "false", "nil", "self", "in"}
INTT = {"Int"}
FLT = {"Double", "Float"}


def sanitize(text):
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
        elif text.startswith("/*", i):
            while i < n and not text.startswith("*/", i):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            out.append("  ")
            i += 2
        elif text.startswith('"""', i):
            out.append('"""')
            i += 3
            while i < n and not text.startswith('"""', i):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            out.append('"""')
            i += 3
        elif c == '"':
            out.append('"')
            i += 1
            while i < n and text[i] != '"' and text[i] != "\n":
                if text[i] == "\\" and i + 1 < n:
                    out.append("  ")
                    i += 2
                    continue
                out.append(" ")
                i += 1
            if i < n and text[i] == '"':
                out.append('"')
                i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def match_brace(s, i, o="{", c="}"):
    d = 0
    for j in range(i, len(s)):
        if s[j] == o:
            d += 1
        elif s[j] == c:
            d -= 1
            if d == 0:
                return j
    return len(s) - 1


def line_of(s, pos):
    return s.count("\n", 0, pos) + 1


class Lint:
    def __init__(self, text, name):
        self.name = name
        self.raw = text
        self.s = sanitize(text)
        self.lines = self.s.split("\n")
        self.f = []
        self.types = []
        self.parse_types()

    def add(self, rule, line, msg, sev=None):
        sev0, orig, page, _ = RULES[rule]
        sev = sev or sev0
        self.f.append({"arquivo": self.name, "linha": line, "regra": rule, "severidade": sev, "origem": orig, "pagina": page, "mensagem": msg})

    # ---- structure
    def parse_types(self):
        s = self.s
        pat = re.compile(r"(?m)^[ \t]*(?:(?:public|private|internal|fileprivate|final|open)\s+)*(class|struct|enum|actor|protocol|extension)\s+([A-Za-z_]\w*)([^{\n]*)\{")
        for m in pat.finditer(s):
            kind, name, rest = m.group(1), m.group(2), m.group(3)
            ob = m.end() - 1
            cb = match_brace(s, ob)
            body = s[ob + 1:cb]
            rest = re.sub(r"<[^>]*>", "", rest)
            rest = rest.split(" where ")[0]
            supers = []
            if ":" in rest:
                supers = [x.strip() for x in rest.split(":", 1)[1].split(",") if x.strip()]
            t = {"kind": kind, "name": name, "supers": supers, "ob": ob, "cb": cb, "body": body, "line": line_of(s, m.start()),
                 "props": [], "funcs": [], "has_init": False, "cases": set()}
            if kind == "enum":
                for cm in re.finditer(r"(?m)^\s*case\s+([^\n]+)", body):
                    for part in re.sub(r"\([^)]*\)", "", cm.group(1)).split(","):
                        nm = re.match(r"\s*(\w+)", part)
                        if nm:
                            t["cases"].add(nm.group(1))
            self.members(t)
            self.types.append(t)

    def members(self, t):
        s, body = self.s, t["body"]
        base = t["ob"] + 1
        depth = 0
        pos = 0
        for ln in body.split("\n"):
            if depth == 0:
                mp = re.match(r"\s*(?:(?:private|public|internal|fileprivate|static|lazy|weak|final|override)\s+)*(var|let)\s+(\w+)\s*(?::\s*([^={\n]+?))?\s*(=|\{|$)", ln)
                if mp:
                    t["props"].append({"kw": mp.group(1), "name": mp.group(2), "type": (mp.group(3) or "").strip(), "default": mp.group(4) == "=", "computed": mp.group(4) == "{", "line": line_of(s, base + pos)})
                mf = re.match(r"\s*((?:(?:private|public|internal|fileprivate|override|mutating|static|final|nonisolated|class)\s+)*)func\s+(\w+)", ln)
                if mf:
                    off = base + pos + mf.end()
                    ob = s.find("{", off)
                    nl = s.find("\n", off)
                    body_f = ""
                    if ob != -1:
                        # header may continue on next lines; accept the first brace after name
                        cb = match_brace(s, ob)
                        body_f = s[ob + 1:cb]
                    t["funcs"].append({"name": mf.group(2), "mods": set(mf.group(1).split()), "line": line_of(s, base + pos), "body": body_f})
                if re.match(r"\s*(?:(?:public|private|internal|override|required|convenience)\s+)*init\b", ln):
                    t["has_init"] = True
            depth += ln.count("{") - ln.count("}")
            pos += len(ln) + 1

    def tget(self, name, kinds=None):
        return [t for t in self.types if t["name"] == name and (not kinds or t["kind"] in kinds)]

    # ---- rules
    def run(self):
        self.r_let_reassign()
        self.r_if_bool()
        self.r_braces()
        self.r_switch()
        self.r_empty_collection()
        self.r_implicit_conv()
        self.r_override()
        self.r_init_props()
        self.r_mutating()
        self.r_try_await()
        self.r_protocol()
        self.r_actor()
        self.r_optional_member()
        self.r_style()
        self.f.sort(key=lambda x: (x["linha"], x["regra"]))
        return self.f

    def r_let_reassign(self):
        decl = {}
        for i, ln in enumerate(self.lines, 1):
            for m in re.finditer(r"\b(let|var)\s+(\w+)", ln):
                decl.setdefault(m.group(2), []).append((m.group(1), i, bool(re.match(r"\s*(?:let|var)\s+\w+\s*(?::[^=]+)?=", ln[m.start():]) and ln.strip().startswith(m.group(1)))))
        member_lines = set()
        for t in self.types:
            for p in t["props"]:
                member_lines.add(p["line"])
        params = set()
        for m in re.finditer(r"\bfunc\s+\w+\s*(?:<[^>]*>)?\s*\(([^)]*)\)", self.s):
            for pm in re.finditer(r"(?:(\w+)\s+)?(\w+)\s*:", m.group(1)):
                params.add(pm.group(2))
        for name, ds in decl.items():
            if len(ds) != 1 or ds[0][0] != "let" or not ds[0][2] or ds[0][1] in member_lines or name in params:
                continue
            dl = ds[0][1]
            for i, ln in enumerate(self.lines, 1):
                if i > dl and re.match(r"\s*" + re.escape(name) + r"\s*(?:[+\-*/%]|\?\?)?=(?!=)", ln):
                    self.add("SWF-01", i, f"`{name}` was declared with let on line {dl} and receives a new value here")
                    break

    def r_if_bool(self):
        boolnames = set(re.findall(r"\b(\w+)\s*:\s*Bool\b", self.s)) | set(re.findall(r"\b(?:let|var)\s+(\w+)\s*=\s*(?:true|false)\b", self.s))
        boolnames |= set(re.findall(r"\b(?:let|var)\s+(\w+)\s*=[^=\n]*(?:==|!=|<=|>=|&&|\|\|)", self.s))
        for i, ln in enumerate(self.lines, 1):
            m = re.match(r"\s*(?:\}\s*else\s+)?(?:if|while)\s*\(?\s*(!?)\s*([A-Za-z_]\w*|\d+)\s*\)?\s*\{", ln)
            if not m or m.group(2) in KW:
                continue
            if m.group(2).isdigit():
                self.add("SWF-02", i, f"condition `{m.group(2)}` is not Boolean (error)")
            elif m.group(2) not in boolnames and not m.group(1):
                self.add("SWF-02", i, f"condition `{m.group(2)}` is an identifier with no known Bool type in the file; if it is not a Bool, it is an error (there is no implicit comparison with zero)", "warning")

    def r_braces(self):
        L = self.lines
        for i, ln in enumerate(L):
            st = ln.strip()
            if st.startswith("}"):
                if "while" in st and "else" not in st:
                    continue
                st = re.sub(r"^\}\s*else\s+", "", st)
            m = re.match(r"(if|while|for)\b", st)
            if not m or "{" in st:
                continue
            if re.search(r"(&&|\|\||,|\(|\+|\?|:|=)\s*$", st):
                continue
            nxt = next((x.strip() for x in L[i + 1:] if x.strip()), "")
            if nxt.startswith(("{", "&&", "||", ".", "?", ":", ",")):
                continue
            self.add("SWF-03", i + 1, f"`{st[:50]}` without braces around the body")

    def r_switch(self):
        s = self.s
        for m in re.finditer(r"\bswitch\b[^{\n]*\{", s):
            ob = m.end() - 1
            cb = match_brace(s, ob)
            body = s[ob + 1:cb]
            if not re.search(r"\bdefault\s*:", body):
                covered = set(re.findall(r"\bcase\s+(?:let\s+)?\.(\w+)", body)) | set(re.findall(r",\s*\.(\w+)", body))
                full = any(t["kind"] == "enum" and t["cases"] and t["cases"] <= covered for t in self.types)
                if not full:
                    self.add("SWF-04", line_of(s, m.start()), "switch without `default` (and without covering all the cases of an enum in the file)")
        L = self.lines
        for i, ln in enumerate(L):
            if ln.strip() == "break":
                prev = next((x.strip() for x in reversed(L[:i]) if x.strip()), "")
                nxt = next((x.strip() for x in L[i + 1:] if x.strip()), "")
                if (nxt.startswith("case ") or nxt.startswith("default")) and not (prev.startswith("case ") or prev.startswith("default")):
                    self.add("SWF-05", i + 1, "`break` at the end of the case is unnecessary")

    def r_empty_collection(self):
        for i, ln in enumerate(self.lines, 1):
            if re.match(r"\s*(?:let|var)\s+\w+\s*=\s*(\[\s*\]|\[\s*:\s*\])\s*$", ln):
                self.add("SWF-06", i, "empty collection without a type: write the type (e.g. `[String]`, `[String: Float]`)")

    def r_implicit_conv(self):
        types = {}
        counts = {}
        for ln in self.lines:
            for m in re.finditer(r"\b(?:let|var)\s+(\w+)", ln):
                counts[m.group(1)] = counts.get(m.group(1), 0) + 1
        for m in re.finditer(r"\bfunc\s+\w+\s*(?:<[^>]*>)?\s*\(([^)]*)\)", self.s):
            for pm in re.finditer(r"(\w+)\s*:", m.group(1)):
                counts[pm.group(1)] = counts.get(pm.group(1), 0) + 1
        for i, ln in enumerate(self.lines, 1):
            m = re.match(r"\s*(?:let|var)\s+(\w+)\s*(?::\s*(\w+))?\s*=\s*(-?\d+(?:\.\d+)?)?(\"|\w+)?", ln)
            if not m:
                continue
            nm, ex, lit, other = m.group(1), m.group(2), m.group(3), m.group(4)
            if counts.get(nm, 0) != 1:
                continue
            if ex in INTT | FLT | {"String"}:
                types[nm] = ex
            elif lit is not None and not ex:
                rest = ln[m.end(3):].strip() if m.group(3) else ""
                if re.match(r"^[+\-*/]", rest):
                    continue
                types[nm] = "Double" if "." in lit else "Int"
            elif other == '"' and not ex:
                types[nm] = "String"
        num = {k: v for k, v in types.items() if v in INTT | FLT}
        for i, ln in enumerate(self.lines, 1):
            for m in re.finditer(r'"\s*\+\s*(\w+)\b(?!\s*\()|\b(\w+)\s*\+\s*"', ln):
                nm = m.group(1) or m.group(2)
                if nm in num and not re.search(r'"\s*\+\s*\w+\s*\(', ln[m.start():m.end() + 1]):
                    self.add("SWF-07", i, f"String + `{nm}` ({num[nm]}): convert with String({nm}) or use \\({nm})")
                    break
            for m in re.finditer(r"\b(\w+)\s*([+\-*/])\s*(\w+)\b", ln):
                a, b = m.group(1), m.group(3)
                if a in num and b in num and ((num[a] in INTT) != (num[b] in INTT) or num[a] != num[b]):
                    self.add("SWF-07", i, f"`{a}` ({num[a]}) {m.group(2)} `{b}` ({num[b]}): convert one of the sides explicitly")
                    break
            m = re.match(r"\s*(?:let|var)\s+\w+\s*:\s*(\w+)\s*=\s*(\w+)\s*$", ln)
            if m and m.group(2) in types and types[m.group(2)] != m.group(1) and m.group(1) in INTT | FLT | {"String"}:
                self.add("SWF-07", i, f"value `{m.group(2)}` ({types[m.group(2)]}) assigned to {m.group(1)} without conversion")

    def r_override(self):
        for t in self.types:
            if t["kind"] != "class" or not t["supers"]:
                continue
            sup = self.tget(t["supers"][0], ["class"])
            if not sup:
                continue
            chain, cur, seen, complete = [], t, {t["name"]}, True
            while cur["supers"]:
                sp = self.tget(cur["supers"][0], ["class"])
                if not sp:
                    complete = bool(self.tget(cur["supers"][0], ["protocol"]))
                    break
                if sp[0]["name"] in seen:
                    break
                chain.append(sp[0])
                seen.add(sp[0]["name"])
                cur = sp[0]
            anc = {f["name"] for a in chain for f in a["funcs"]}
            for f in t["funcs"]:
                if f["name"] in anc and "override" not in f["mods"]:
                    self.add("SWF-08", f["line"], f"`{f['name']}` already exists in the superclass: mark it with `override`")
                if "override" in f["mods"] and f["name"] not in anc and complete:
                    self.add("SWF-09", f["line"], f"`override func {f['name']}` does not override any method of the superclasses in the file")

    def r_init_props(self):
        for t in self.types:
            if t["kind"] != "class" or t["has_init"]:
                continue
            for p in t["props"]:
                if p["kw"] == "var" or p["kw"] == "let":
                    if not p["default"] and not p["computed"] and p["type"] and not p["type"].endswith(("?", "!")):
                        self.add("SWF-10", p["line"], f"`{p['name']}: {p['type']}` in class `{t['name']}` without an initial value and without init")

    def r_mutating(self):
        valuekinds = {"struct", "enum"}
        builtin = {"Int", "Double", "Float", "String", "Bool", "Array", "Dictionary"}
        for t in self.types:
            is_value = t["kind"] in valuekinds or (t["kind"] == "extension" and (t["name"] in builtin or any(x["kind"] in valuekinds for x in self.tget(t["name"]))))
            if not is_value:
                continue
            names = {p["name"] for tt in self.tget(t["name"]) for p in tt["props"] if p["kw"] == "var" and not p["computed"]}
            for f in t["funcs"]:
                if "mutating" in f["mods"] or "static" in f["mods"]:
                    continue
                body = f["body"]
                hit = re.search(r"(?m)^\s*self\s*(?:[+\-*/%]|\?\?)?=(?!=)", body)
                what = "self"
                if not hit:
                    for nm in names:
                        h = re.search(r"(?m)^\s*(?:self\.)?" + re.escape(nm) + r"\s*(?:[+\-*/%]|\?\?)?=(?!=)", body)
                        if h:
                            hit, what = h, nm
                            break
                if hit:
                    self.add("SWF-11", f["line"], f"`{f['name']}` modifies `{what}` in {t['kind']} `{t['name']}` without `mutating`")

    def r_try_await(self):
        thr, asy = set(), set()
        s = self.s
        for m in re.finditer(r"\bfunc\s+(\w+)\s*(?:<[^>]*>)?\s*\(", s):
            op = m.end() - 1
            cp = match_brace(s, op, "(", ")")
            tail = s[cp + 1:cp + 80].split("{")[0].split("\n")[0]
            hd = tail.split("->")[0]
            if re.search(r"\bthrows\b", hd):
                thr.add(m.group(1))
            if re.search(r"\basync\b", hd):
                asy.add(m.group(1))
        for i, ln in enumerate(self.lines, 1):
            if re.match(r"\s*(?:[\w\s]*\s)?func\s", ln):
                continue
            for nm in thr:
                for m in re.finditer(r"\b" + re.escape(nm) + r"\s*\(", ln):
                    if not re.search(r"\btry[?!]?\s", ln[:m.start()]):
                        self.add("SWF-12", i, f"`{nm}(...)` can throw: write `try` before the call")
                        break
            for nm in asy:
                for m in re.finditer(r"\b" + re.escape(nm) + r"\s*\(", ln):
                    if not re.search(r"\bawait\b", ln[:m.start()]) and not re.search(r"\basync\s+let\b", ln[:m.start()]):
                        self.add("SWF-13", i, f"`{nm}(...)` is asynchronous: write `await` before the call (or `async let`)")
                        break

    def r_protocol(self):
        for p in [t for t in self.types if t["kind"] == "protocol"]:
            reqs = [("var", x["name"]) for x in p["props"]] + [("func", f["name"]) for f in p["funcs"]]
            if not reqs:
                continue
            seen_types = set()
            for t in self.types:
                if t["kind"] == "protocol" or p["name"] not in t["supers"]:
                    continue
                if (t["name"], t["kind"] == "extension") in seen_types:
                    continue
                seen_types.add((t["name"], t["kind"] == "extension"))
                props, funcs = set(), set()
                for tt in self.tget(t["name"]):
                    props |= {x["name"] for x in tt["props"]}
                    funcs |= {f["name"] for f in tt["funcs"]}
                    if tt["kind"] == "class" and tt["supers"]:
                        for a in self.tget(tt["supers"][0], ["class"]):
                            props |= {x["name"] for x in a["props"]}
                            funcs |= {f["name"] for f in a["funcs"]}
                miss = [f"{k} {n}" for k, n in reqs if (k == "var" and n not in props) or (k == "func" and n not in funcs)]
                if miss:
                    self.add("SWF-14", t["line"], f"`{t['name']}` declares conformance to `{p['name']}` but does not implement: {', '.join(miss)}")

    def r_actor(self):
        actors = {t["name"] for t in self.types if t["kind"] == "actor"}
        for a in actors:
            for m in re.finditer(r"\b(?:let|var)\s+(\w+)\s*(?::\s*\w+)?\s*=\s*" + re.escape(a) + r"\s*\(", self.s):
                inst = m.group(1)
                dl = line_of(self.s, m.start())
                for i, ln in enumerate(self.lines, 1):
                    if i == dl:
                        continue
                    for mm in re.finditer(r"\b" + re.escape(inst) + r"\.\w+", ln):
                        if not re.search(r"\bawait\b", ln[:mm.start()]):
                            self.add("SWF-17", i, f"`{mm.group(0)}` accesses the actor `{a}`: use `await`")
                            break

    def r_optional_member(self):
        opt = set()
        for m in re.finditer(r"\b(?:let|var)\s+(\w+)\s*:\s*[^=\n{]*?\?\s*(?:=|$)", self.s, re.M):
            opt.add(m.group(1))
        for i, ln in enumerate(self.lines, 1):
            if re.match(r"\s*(?:let|var)\s", ln):
                continue
            for nm in opt:
                if re.search(r"(?<![\w.?])" + re.escape(nm) + r"\.\w", ln):
                    self.add("SWF-19", i, f"`{nm}` is an optional: use `if let`, `??` or `{nm}?.` before accessing members")
                    break

    def r_style(self):
        for i, ln in enumerate(self.lines, 1):
            st = ln.rstrip()
            if st.endswith(";") and not st.lstrip().startswith("for"):
                self.add("SWF-15", i, "semicolon at the end of the statement is unnecessary")
            if re.match(r"\s*func\s+main\s*\(", ln):
                self.add("SWF-16", i, "`func main()` is unnecessary in global-scope code")
            m = re.match(r"\s*(?:\}\s*else\s+)?(if|while|switch)\s*\(", ln)
            if m:
                op = ln.index("(")
                cp = match_brace(ln, op, "(", ")")
                if ln[cp + 1:].strip().startswith("{") and cp > op:
                    self.add("SWF-18", i, "parentheses around the condition are optional")
            if re.search(r"[\w)\]]!(?!=)", ln) or re.search(r"\btry!", ln):
                self.add("SWF-X1", i, "forced unwrapping `!` or `try!`: outside the tour")
            if re.search(r"\b\w+(\+\+|--)(?!\w)", ln):
                self.add("SWF-X2", i, "`++`/`--` operator: use `+= 1`/`-= 1` as in the tour")
            if re.match(r"\s*for\s*\(?[^\n]*;[^\n]*;", ln):
                self.add("SWF-X3", i, "C-style for: use `for i in 0..<n`")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-info", action="store_true")
    ap.add_argument("--rules", action="store_true")
    a = ap.parse_args()
    if a.rules:
        for k, (sev, orig, page, desc) in RULES.items():
            print(f"{k}  [{sev}] [{orig}] ({page}): {desc}")
        return 0
    if not a.files:
        ap.print_help()
        return 2
    allf = []
    for fn in a.files:
        try:
            text = sys.stdin.read() if fn == "-" else open(fn, "r", encoding="utf-8", errors="replace").read()
        except OSError as e:
            print(f"Error reading {fn}: {e}", file=sys.stderr)
            return 2
        allf += Lint(text, "<stdin>" if fn == "-" else fn).run()
    if a.no_info:
        allf = [x for x in allf if x["severidade"] != "info"]
    if a.json:
        print(json.dumps(allf, ensure_ascii=False, indent=1))
    else:
        for x in allf:
            print(f"{x['arquivo']}:{x['linha']}: [{x['severidade']}] {x['regra']} {x['mensagem']} [{x['origem']}] ({x['pagina']})")
        if not allf:
            print("No findings. This does NOT prove that the code compiles (heuristic linter, backed only by A Swift Tour).")
        else:
            c = {}
            for x in allf:
                c[x["severidade"]] = c.get(x["severidade"], 0) + 1
            print("Summary: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())) + ". [DATED] Swift version not stated by the source.")
    return 1 if any(x["severidade"] != "info" for x in allf) else 0


if __name__ == "__main__":
    sys.exit(main())
