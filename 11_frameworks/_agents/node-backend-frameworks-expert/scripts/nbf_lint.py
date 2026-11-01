# -*- coding: utf-8 -*-
"""
nbf_lint.py - STATIC linter for Node/Express/Fastify/Nest snippets/files, using only rules supported by the text of the sources.

Sources (acronyms; page = PDF page): NODEHB (Node Handbook, 2018-09-06), EXPHB (Express Handbook, 2022-11-18),
FSTF (Fastify Getting Started, v5.12.x), NEST (NestJS First steps).

- Heuristic (regular expressions + brace counting); does NOT execute or import the target code; no network; stdlib.
- Each finding carries: file:line, rule, severity, origin ([from source] | [inference] | [extrapolation] | [DATED]) and page.
- [from source] rule = statement made on the cited page; [inference] = deduction from the text; [extrapolation] = outside the collection.
- It is not a security audit nor a full quality audit; no findings does not mean correct code.

Usage:
  python -I scripts/nbf_lint.py FILE [FILE ...] [--json] [--strict] [--rules]
  python -I scripts/nbf_lint.py --stdin [--name app.js]
Exit: 1 if there is an ERROR (or a WARNING with --strict); 0 otherwise.
Handled types: .js .mjs .cjs .ts (code); package.json; .gitignore; .html/.ejs (forms); other texts (npx URL, ws://).
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

RULES = {
    "EXP-MW-NEXT": ("WARNING", "[from source]", "EXPHB p.17", "Middleware (req, res, next) that neither calls next() nor ends the response: the request may hang."),
    "EXP-BODY-PARSER": ("WARNING", "[inference]", "EXPHB p.6, p.24, p.34", "req.body used without a visible parsing middleware (express.json/urlencoded/formidable)."),
    "EXP-MW-ORDER": ("INFO", "[inference]", "EXPHB p.17-18", "Middleware registered with app.use after a route: the order defines the execution stack; check whether the earlier route needs it (the handbook's own example on p.18 does this with cookie-parser)."),
    "EXP-SESSION-SECRET": ("ERROR", "[from source]", "EXPHB p.21-22", "express-session without 'secret' (the only required parameter according to the text)."),
    "EXP-SESSION-MEMORY": ("INFO", "[from source]", "EXPHB p.23", "express-session without an explicit store: in-memory default, for development only according to the author."),
    "EXP-COOKIE-SESSION": ("INFO", "[from source]", "EXPHB p.23", "cookie-session stores data on the client (limit ~4 KB); the author does not recommend it."),
    "EXP-VIEW-ENGINE": ("WARNING", "[inference]", "EXPHB p.15-16", "res.render without a visible app.set('view engine', ...)."),
    "EXP-JADE": ("INFO", "[from source]", "EXPHB p.15", "Jade is the default for compatibility, but the author recommends Pug (or another engine) in new projects."),
    "EXP-VALIDATION": ("INFO", "[inference]", "EXPHB p.24, p.30", "req.body data used without visible validation; the handbook uses express-validator and says never to trust the input."),
    "EXP-VALIDATION-RESULT": ("WARNING", "[from source]", "EXPHB p.25", "check() used without validationResult(): validation errors are not read."),
    "EXP-FORM-ENCTYPE": ("WARNING", "[from source]", "EXPHB p.35", "Form with a file input without enctype=\"multipart/form-data\": files are not uploaded."),
    "EXP-REQ-LOCALS": ("INFO", "[extrapolation]", "EXPHB p.18", "The handbook mentions Request.locals for data shared between middleware; check the current Express documentation (the locals field is usually res.locals). Not stated by the sources."),
    "NODE-CONFIGURE": ("WARNING", "[DATED]", "NODEHB p.199", "app.configure/express.errorHandler appear in the 2018 text; [extrapolation]: they do not exist in current Express versions. Check the current documentation."),
    "NODE-ERR-FIRST": ("WARNING", "[from source]", "NODEHB p.109", "Error-first callback that ignores its first parameter (err)."),
    "NODE-SYNC-HANDLER": ("WARNING", "[inference]", "NODEHB p.86-87, p.148, p.162", "Synchronous call (...Sync) inside an HTTP handler: blocks the event loop's single thread."),
    "NODE-READFILE-RESPONSE": ("INFO", "[from source]", "NODEHB p.153, p.186-187", "readFile loads the whole file into memory before responding; the text suggests streams (createReadStream().pipe(res))."),
    "NODE-EXIT": ("INFO", "[from source]", "NODEHB p.17-18", "process.exit() ends abruptly (pending requests are aborted); the text prefers handling SIGTERM and closing the server."),
    "NODE-SIGTERM": ("INFO", "[inference]", "NODEHB p.18-19", "http/Express server started without visible SIGTERM handling."),
    "NODE-PROMISE-NEW": ("ERROR", "[from source]", "NODEHB p.118", "Promise(...) without new: error described in the text ('undefined is not a promise')."),
    "NODE-FS-NOCB": ("ERROR", "[from source]", "NODEHB p.148, p.160-162", "Asynchronous fs method without a callback and without await/then: in fs the methods are asynchronous by default and the synchronous version has the Sync suffix."),
    "NODE-MYSQL-CONCAT": ("WARNING", "[inference]", "NODEHB p.195", "SQL built by concatenation/template; the text uses '?' placeholders whose values are escaped automatically."),
    "NODE-MYSQL-RESULTID": ("ERROR", "[from source]", "NODEHB p.196-197", "results.resultId: the text says the generated id comes in results.insertId (the p.197 snippet has this error)."),
    "NODE-SETINTERVAL-ASYNC": ("INFO", "[from source]", "NODEHB p.104", "setInterval with asynchronous work may overlap executions; the text suggests recursive setTimeout."),
    "NODE-NPX-URL": ("WARNING", "[from source]", "NODEHB p.85", "npx running code from a URL: only run code you control."),
    "NODE-WS-INSECURE": ("WARNING", "[from source]", "NODEHB p.143", "ws:// URL (unencrypted); the text says to use wss://."),
    "NODE-PKG-NAME": ("ERROR", "[from source]", "NODEHB p.54", "package.json name outside the text's rules (fewer than 214 characters, no spaces, lowercase, hyphens or underscores)."),
    "NODE-PKG-VERSION": ("WARNING", "[from source]", "NODEHB p.57", "version is not in semver x.y.z format."),
    "NODE-PKG-RANGE": ("WARNING", "[inference]", "NODEHB p.64-66", "Dependency with '*' or 'latest' accepts any version (including major); the text shows why the lockfile exists."),
    "NODE-PKG-PRIVATE": ("INFO", "[inference]", "NODEHB p.53, p.60", "Application (has scripts.start) without \"private\": true; the field prevents accidental publishing to npm."),
    "NODE-GITIGNORE-ENV": ("WARNING", "[from source]", "NODEHB p.21", ".gitignore without .env: the text says to ignore the .env file."),
    "NODE-GITIGNORE-MODULES": ("INFO", "[from source]", "NODEHB p.65", ".gitignore without node_modules: the text says the folder is not committed."),
    "FST-LISTEN-HOST": ("INFO", "[from source]", "FSTF p.3-4", "listen without host: listens only on 127.0.0.1; in a container the text suggests 0.0.0.0 or ::."),
    "FST-PLUGIN-ENCAP": ("INFO", "[from source]", "FSTF p.7, p.10", "decorate/addHook inside a plugin without fastify-plugin: they stay in the encapsulated scope; fastify-plugin exposes them to the parent scope."),
    "FST-NO-SCHEMA": ("INFO", "[inference]", "FSTF p.11-12", "request.body used without a visible 'schema'; the text treats JSON Schema validation as a core concept."),
    "NEST-NODE-VERSION": ("WARNING", "[from source]", "NEST p.2", "Nest project with engines.node below 20; the text requires Node >= 20 (capture version; [DATED] if it changes)."),
}

SEV_ORDER = {"ERROR": 0, "WARNING": 1, "INFO": 2}
CODE_EXT = {".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx"}
FS_ASYNC = "stat|readFile|writeFile|mkdir|readdir|rename|rmdir|appendFile|access|unlink|copyFile|open|chmod|chown|truncate|readlink|realpath|lstat"
SYNC_CALLS = r"\b(?:readFileSync|writeFileSync|readdirSync|statSync|lstatSync|existsSync|mkdirSync|appendFileSync|renameSync|unlinkSync|rmdirSync|copyFileSync|execSync|spawnSync)\s*\("


def strip_comments(t):
    """Replaces comments with spaces (preserves length and line breaks), respecting strings."""
    out = []
    i, n = 0, len(t)
    q = None
    while i < n:
        c = t[i]
        if q:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(t[i + 1])
                i += 2
                continue
            if c == q:
                q = None
            i += 1
            continue
        if c in "'\"`":
            q = c
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and t[i + 1] == "/" and (i == 0 or t[i - 1] != ":"):
            while i < n and t[i] != "\n":
                out.append(" ")
                i += 1
            continue
        if c == "/" and i + 1 < n and t[i + 1] == "*":
            while i < n and not (t[i] == "*" and i + 1 < n and t[i + 1] == "/"):
                out.append("\n" if t[i] == "\n" else " ")
                i += 1
            if i < n:
                out.append("  ")
                i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def match_brace(t, i):
    """t[i] == '{'; returns the index of the matching '}' (or len(t))."""
    depth = 0
    q = None
    n = len(t)
    while i < n:
        c = t[i]
        if q:
            if c == "\\":
                i += 2
                continue
            if c == q:
                q = None
        elif c in "'\"`":
            q = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return n


def match_paren(t, i):
    depth = 0
    q = None
    n = len(t)
    while i < n:
        c = t[i]
        if q:
            if c == "\\":
                i += 2
                continue
            if c == q:
                q = None
        elif c in "'\"`":
            q = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return n


def lineof(t, i):
    return t.count("\n", 0, i) + 1


class Lint:
    def __init__(self, name):
        self.name = name
        self.f = []

    def add(self, rule, idx_or_line, text, extra=""):
        sev, lab, pg, msg = RULES[rule]
        line = lineof(text, idx_or_line) if isinstance(idx_or_line, int) and idx_or_line >= 0 else 1
        if isinstance(idx_or_line, tuple):
            line = idx_or_line[0]
        self.f.append({"file": self.name, "line": line, "rule": rule, "severity": sev, "origin": lab,
                       "cite": pg, "message": msg + (" " + extra if extra else "")})


def lint_code(name, raw):
    L = Lint(name)
    t = strip_comments(raw)
    uses_express = bool(re.search(r"require\(\s*['\"]express['\"]\s*\)|from\s+['\"]express['\"]", t))
    uses_fastify = bool(re.search(r"require\(\s*['\"]fastify['\"]\s*\)|from\s+['\"]fastify['\"]", t))
    # --- middleware without next
    mw_re = re.compile(r"\(\s*(?:_?req|request)\s*,\s*(?:_?res|response)\s*,\s*next\s*\)\s*(?:=>\s*)?\{")
    term = re.compile(r"\bres\.(?:send|json|end|redirect|render|sendStatus|download|sendFile)\s*\(|\bres\.status\s*\([^)]*\)\s*\.\s*(?:send|json|end)\s*\(|\bres\.status\s*\([^)]*\)\s*\.\s*\w+\s*\(")
    for m in mw_re.finditer(t):
        b = m.end() - 1
        e = match_brace(t, b)
        body = t[b:e]
        if not re.search(r"\bnext\s*\(", body) and not term.search(body) and not re.search(r"\bnext\b(?!\s*\))", body[1:]):
            L.add("EXP-MW-NEXT", m.start(), t)
    # --- req.body without a parser
    if re.search(r"\breq\.body\b", t) and not re.search(r"express\.json\s*\(|express\.urlencoded\s*\(|bodyParser|body-parser|formidable|multer|busboy", t):
        L.add("EXP-BODY-PARSER", re.search(r"\breq\.body\b", t).start(), t)
    # --- order: app.use(mw) after a route
    route_re = re.compile(r"\b(?:app|router)\.(?:get|post|put|delete|patch)\s*\(")
    first_route = route_re.search(t)
    if first_route:
        for m in re.finditer(r"\bapp\.use\s*\(\s*(cookieParser\s*\(|session\s*\(|express\.json\s*\(|express\.urlencoded\s*\()", t):
            if m.start() > first_route.start():
                L.add("EXP-MW-ORDER", m.start(), t, f"(route on line {lineof(t, first_route.start())}).")
    # --- sessions
    for m in re.finditer(r"\bsession\s*\(", t):
        if not re.search(r"require\(\s*['\"]express-session['\"]\s*\)|from\s+['\"]express-session['\"]", t):
            break
        e = match_paren(t, m.end() - 1)
        args = t[m.end():e]
        if not re.search(r"""['"]?secret['"]?\s*:""", args):
            L.add("EXP-SESSION-SECRET", m.start(), t)
        if not re.search(r"""['"]?store['"]?\s*:""", args):
            L.add("EXP-SESSION-MEMORY", m.start(), t)
    m = re.search(r"require\(\s*['\"]cookie-session['\"]\s*\)|from\s+['\"]cookie-session['\"]", t)
    if m:
        L.add("EXP-COOKIE-SESSION", m.start(), t)
    # --- views
    m = re.search(r"\bres\.render\s*\(", t)
    if m and not re.search(r"app\.set\s*\(\s*['\"]view engine['\"]|app\.engine\s*\(|\.set\(\s*['\"]view engine", t):
        L.add("EXP-VIEW-ENGINE", m.start(), t)
    m = re.search(r"""['"]view engine['"]\s*,\s*['"]jade['"]""", t)
    if m:
        L.add("EXP-JADE", m.start(), t)
    # --- validation
    if uses_express or re.search(r"\bapp\.(?:post|put|patch)\s*\(", t):
        for m in re.finditer(r"\breq\.body\.\w+", t):
            if not re.search(r"express-validator|validationResult|\bcheck\s*\(|body\s*\(\s*['\"]|\bjoi\b|\bzod\b|\bajv\b|\byup\b", t, re.I):
                L.add("EXP-VALIDATION", m.start(), t)
            break
    if re.search(r"\bcheck\s*\(\s*['\"]", t) and not re.search(r"validationResult", t):
        L.add("EXP-VALIDATION-RESULT", re.search(r"\bcheck\s*\(", t).start(), t)
    m = re.search(r"\breq\.locals\b", t)
    if m:
        L.add("EXP-REQ-LOCALS", m.start(), t)
    m = re.search(r"\bapp\.configure\s*\(|express\.errorHandler\s*\(", t)
    if m:
        L.add("NODE-CONFIGURE", m.start(), t)
    # --- callbacks error-first
    cb_re = re.compile(r"\(\s*(err|error)\s*,\s*[\w, ]+\)\s*=>\s*\{|function\s*\w*\s*\(\s*(err|error)\s*,\s*[\w, ]+\)\s*\{")
    for m in cb_re.finditer(t):
        name_ = m.group(1) or m.group(2)
        b = m.end() - 1
        e = match_brace(t, b)
        body = t[b + 1:e]
        if not re.search(r"\b" + name_ + r"\b", body):
            L.add("NODE-ERR-FIRST", m.start(), t)
    # --- sync call in handler
    h_re = re.compile(r"\(\s*(?:_?req|request)\s*,\s*(?:_?res|response|reply)\s*(?:,\s*next\s*)?\)\s*(?:=>\s*)?\{")
    seen = set()
    for m in h_re.finditer(t):
        b = m.end() - 1
        e = match_brace(t, b)
        body = t[b:e]
        for s in re.finditer(SYNC_CALLS, body):
            pos = b + s.start()
            if pos not in seen:
                seen.add(pos)
                L.add("NODE-SYNC-HANDLER", pos, t)
        if re.search(r"\breadFile\s*\(", body) and re.search(r"\bres\.(?:end|send)\s*\(", body):
            L.add("NODE-READFILE-RESPONSE", m.start(), t)
    # --- exit
    for m in re.finditer(r"\bprocess\.exit\s*\(", t):
        ctx = t[max(0, m.start() - 160):m.start()]
        if re.search(r"\bif\s*\(\s*err|\bcatch\b|\.on\(\s*['\"]error", ctx):
            continue
        L.add("NODE-EXIT", m.start(), t)
    # --- SIGTERM
    if (uses_express or re.search(r"http\.createServer|createServer\s*\(", t)) and re.search(r"\.listen\s*\(", t) and "SIGTERM" not in t:
        L.add("NODE-SIGTERM", re.search(r"\.listen\s*\(", t).start(), t)
    # --- Promise without new
    for m in re.finditer(r"(?<![\w.])Promise\s*\(", t):
        pre = t[max(0, m.start() - 4):m.start()]
        if pre.endswith("new "):
            continue
        L.add("NODE-PROMISE-NEW", m.start(), t)
    # --- fs without callback
    if not re.search(r"fs-extra|fs/promises|fs\.promises|require\(\s*['\"]fs['\"]\s*\)\.promises", t):
        for m in re.finditer(r"\bfs\.(" + FS_ASYNC + r")\s*\(", t):
            e = match_paren(t, m.end() - 1)
            args = t[m.end():e]
            pre = t[max(0, m.start() - 12):m.start()]
            post = t[e + 1:e + 12]
            if "=>" in args or re.search(r"\bfunction\b", args) or re.search(r"await\s*$", pre) or post.lstrip().startswith(".then"):
                continue
            # callback passed by name (last argument is an identifier)? only accepted if there are >=2 args and the last is an identifier
            parts = [p.strip() for p in re.split(r",(?![^()]*\))", args) if p.strip()]
            if len(parts) >= 2 and re.fullmatch(r"[A-Za-z_$][\w$]*", parts[-1]) and parts[-1] not in ("utf8", "null"):
                continue
            L.add("NODE-FS-NOCB", m.start(), t)
    # --- mysql
    for m in re.finditer(r"\.query\s*\(", t):
        e = match_paren(t, m.end() - 1)
        args = t[m.end():e]
        first = args.split(",")[0] if args else ""
        if re.search(r"\b(SELECT|INSERT|UPDATE|DELETE)\b", args, re.I) and (re.search(r"['\"]\s*\+|\+\s*['\"]|\$\{", first) or ("`" in first and "${" in first)):
            L.add("NODE-MYSQL-CONCAT", m.start(), t)
    m = re.search(r"\.resultId\b", t)
    if m:
        L.add("NODE-MYSQL-RESULTID", m.start(), t)
    # --- setInterval async
    for m in re.finditer(r"\bsetInterval\s*\(\s*(async\b|[^)]*\b(?:fetch|await|axios|query|readFile)\b)", t):
        L.add("NODE-SETINTERVAL-ASYNC", m.start(), t)
    # --- Fastify
    if uses_fastify or re.search(r"\bfastify\.(?:get|post|register|listen|decorate|addHook)\s*\(", t):
        for m in re.finditer(r"\.listen\s*\(\s*\{([^}]*)\}", t):
            if "host" not in m.group(1):
                L.add("FST-LISTEN-HOST", m.start(), t)
        if re.search(r"\bfastify\.(?:decorate|addHook)\s*\(", t) and not re.search(r"fastify-plugin|\bfp\s*\(|fastifyPlugin", t) \
                and re.search(r"async\s+function\s+\w+\s*\(\s*fastify|module\.exports\s*=\s*async|export\s+default\s+async", t):
            L.add("FST-PLUGIN-ENCAP", re.search(r"\bfastify\.(?:decorate|addHook)\s*\(", t).start(), t)
        if re.search(r"\brequest\.body\b", t) and not re.search(r"\bschema\b", t):
            L.add("FST-NO-SCHEMA", re.search(r"\brequest\.body\b", t).start(), t)
    L.f.extend(lint_text(name, raw))
    return L.f


def lint_text(name, raw):
    """Rules that apply to any text (scripts, md, js)."""
    L = Lint(name)
    for m in re.finditer(r"\bnpx\s+(?:-\w+\s+)*https?://\S+", raw):
        L.add("NODE-NPX-URL", m.start(), raw)
    for m in re.finditer(r"\bws://(?!localhost|127\.0\.0\.1)", raw):
        L.add("NODE-WS-INSECURE", m.start(), raw)
    return L.f


def lint_html(name, raw):
    L = Lint(name)
    for m in re.finditer(r"<form\b[^>]*>(.*?)</form>", raw, re.S | re.I):
        tag = raw[m.start():raw.find(">", m.start()) + 1]
        if re.search(r"type\s*=\s*['\"]file['\"]", m.group(1), re.I) and not re.search(r"enctype\s*=\s*['\"]multipart/form-data['\"]", tag, re.I):
            L.add("EXP-FORM-ENCTYPE", m.start(), raw)
    return L.f


def first_int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group(0)) if m else None


def lint_package(name, raw):
    L = Lint(name)
    try:
        d = json.loads(raw)
    except Exception as ex:
        return [{"file": name, "line": 1, "rule": "NODE-PKG-NAME", "severity": "ERROR", "origin": "[from source]", "cite": "NODEHB p.50",
                 "message": f"Invalid JSON ({ex}); the text requires package.json to follow the JSON format."}]
    if not isinstance(d, dict):
        return []

    def ln(key):
        m = re.search(r'"' + re.escape(key) + r'"', raw)
        return lineof(raw, m.start()) if m else 1
    nm = d.get("name")
    if isinstance(nm, str) and (len(nm) >= 214 or re.search(r"\s", nm) or re.search(r"[A-Z]", nm)):
        L.add("NODE-PKG-NAME", (ln("name"),), raw)
    v = d.get("version")
    if isinstance(v, str) and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.\-+]+)?", v):
        L.add("NODE-PKG-VERSION", (ln("version"),), raw)
    for sect in ("dependencies", "devDependencies"):
        for k, val in (d.get(sect) or {}).items():
            if isinstance(val, str) and val.strip() in ("*", "latest", ""):
                L.add("NODE-PKG-RANGE", (ln(k),), raw, f"({sect}.{k} = '{val}')")
    if (d.get("scripts") or {}).get("start") and "private" not in d:
        L.add("NODE-PKG-PRIVATE", (ln("scripts"),), raw)
    deps = {}
    deps.update(d.get("dependencies") or {})
    deps.update(d.get("devDependencies") or {})
    if any(k.startswith("@nestjs/") for k in deps):
        eng = (d.get("engines") or {}).get("node")
        n = first_int(eng) if isinstance(eng, str) else None
        if n is not None and n < 20:
            L.add("NEST-NODE-VERSION", (ln("engines"),), raw)
    return L.f


def lint_gitignore(name, raw):
    L = Lint(name)
    lines = [x.strip() for x in raw.splitlines()]
    if not any(x in (".env", "/.env", ".env*", "*.env") for x in lines):
        L.add("NODE-GITIGNORE-ENV", (1,), raw)
    if not any(x.strip("/") in ("node_modules", "node_modules/*") for x in lines):
        L.add("NODE-GITIGNORE-MODULES", (1,), raw)
    return L.f


def lint_file(name, raw):
    base = os.path.basename(name).lower()
    ext = os.path.splitext(base)[1]
    if base == "package.json" or (base.startswith("package") and base.endswith(".json") and "lock" not in base):
        return lint_package(name, raw)
    if base == ".gitignore" or base.endswith(".gitignore"):
        return lint_gitignore(name, raw)
    if ext in CODE_EXT:
        res = lint_code(name, raw)
        if "<form" in raw.lower():
            res += lint_html(name, raw)
        return res
    if ext in (".html", ".htm", ".ejs", ".pug"):
        return lint_html(name, raw) + lint_text(name, raw)
    return lint_text(name, raw)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--name", default="stdin.js")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--rules", action="store_true")
    a = ap.parse_args(argv)
    if a.rules:
        for k, (sev, lab, pg, msg) in RULES.items():
            print(f"{k}\t{sev}\t{lab}\t{pg}\t{msg}")
        return 0
    res = []
    if a.stdin:
        res += lint_file(a.name, sys.stdin.read())
    for f in a.files:
        try:
            raw = open(f, "r", encoding="utf-8", errors="replace").read()
        except OSError as ex:
            print(f"Could not read {f}: {ex}")
            return 2
        res += lint_file(f, raw)
    if not a.files and not a.stdin:
        ap.print_help()
        return 2
    res.sort(key=lambda r: (r["file"], r["line"], SEV_ORDER[r["severity"]], r["rule"]))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for r in res:
            print(f"{r['file']}:{r['line']}: {r['severity']} {r['rule']} {r['origin']} ({r['cite']}) {r['message']}")
        c = {k: sum(1 for r in res if r["severity"] == k) for k in SEV_ORDER}
        print(f"-- {len(res)} finding(s): {c['ERROR']} ERROR, {c['WARNING']} WARNING, {c['INFO']} INFO. Heuristic; no findings does not prove correctness.")
    bad = any(r["severity"] == "ERROR" for r in res) or (a.strict and any(r["severity"] == "WARNING" for r in res))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
