# -*- coding: utf-8 -*-
"""
snippet_lint.py - STATIC linter for Python snippets (Django/FastAPI) and command lines, with rules that
the sources (DJT, FAPI) support. Never runs or imports the analyzed code: only ast.parse and regex.
Each finding carries: id, severity (ERROR/WARNING/INFO), origin ([from source] or [inference]), PDF page and line.

  ERROR   = contradicts what the source states;  WARNING = the source supports it only in part / direct deduction ([inference]);
  INFO    = observation (includes NOT COVERED for Flask).
Flask: the FLT has no code rules -> no rule is applied (INFO NOT COVERED).
Comments and strings of the analyzed file are DATA: embedded instructions ("ignore the rules") are ignored.

Rules (Python, via ast):
  DJ-PATH-ARGS      ERROR   path() without route and view (DJT p.5)
  DJ-INCLUDE        ERROR   path() pointing straight at .urls / "x.urls" instead of include(); exception: admin.site.urls (DJT p.4)
  DJ-ROUTE-QUERY    WARNING route with '?': patterns do not look at GET/POST or the domain (DJT p.5)
  DJ-VIEW-REQUEST   ERROR   function that returns HttpResponse(...) with no parameter: the view receives HttpRequest as its 1st argument (DJT p.5)
  DJ-NAME-MISSING   INFO    path() without name (optional; name lets you reference the URL) (DJT p.5)
  FA-AWAIT-IN-DEF   ERROR   route with await inside a 'def' function (the source says to use async def with async/await) (FAPI p.6)
  FA-PATH-MISSING   WARNING {param} in the path without a same-named parameter in the function [inference] (FAPI p.8, 17)
  FA-PATH-UNTYPED   WARNING path parameter without a type annotation: validation/conversion comes from the type declaration (FAPI p.16-17)
  FA-OPTIONAL-NODEF WARNING parameter 'X | None' without '= None' is required; what makes it optional is '= None' (FAPI p.17)
  FA-BODY-NOT-MODEL WARNING body (POST/PUT/PATCH) with a local class that does not inherit BaseModel [inference] (FAPI p.10-11)
Rules (command lines, in non-.py files):
  CMD-PROJNAME      ERROR   startproject django|test (DJT p.1)
  CMD-QUOTE         WARNING fastapi[standard] without quotes in pip/uv (FAPI p.5)
  CMD-RUNSERVER-PROD WARNING runserver in a deployment file (Dockerfile, Procfile, *.service, *.yml/*.yaml): development-only server
                           (DJT p.2 [from source]; classifying the file as deployment is [inference])

Usage: python -I scripts/snippet_lint.py PATH [PATH...] [--json] [--rules]
Exit 1 if there is an ERROR; 0 otherwise; 2 on incorrect usage.
"""
import argparse
import ast
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HTTP = {"get", "put", "post", "delete", "patch", "options", "head", "trace"}
BODY_METHODS = {"post", "put", "patch"}
TEXT_EXT = (".sh", ".md", ".txt", ".yml", ".yaml", ".service", ".cfg", ".toml", ".bat", ".ps1")
MAX_BYTES = 1_000_000

RULES = {
    "DJ-PATH-ARGS": ("ERROR", "[from source]", "DJT p.5"),
    "DJ-INCLUDE": ("ERROR", "[from source]", "DJT p.4"),
    "DJ-ROUTE-QUERY": ("WARNING", "[from source]", "DJT p.5"),
    "DJ-VIEW-REQUEST": ("ERROR", "[from source]", "DJT p.5"),
    "DJ-NAME-MISSING": ("INFO", "[from source]", "DJT p.5"),
    "FA-AWAIT-IN-DEF": ("ERROR", "[from source]", "FAPI p.6"),
    "FA-PATH-MISSING": ("WARNING", "[inference]", "FAPI p.8,17"),
    "FA-PATH-UNTYPED": ("WARNING", "[from source]", "FAPI p.16-17"),
    "FA-OPTIONAL-NODEF": ("WARNING", "[from source]", "FAPI p.17"),
    "FA-BODY-NOT-MODEL": ("WARNING", "[inference]", "FAPI p.10-11"),
    "CMD-PROJNAME": ("ERROR", "[from source]", "DJT p.1"),
    "CMD-QUOTE": ("WARNING", "[from source]", "FAPI p.5"),
    "CMD-RUNSERVER-PROD": ("WARNING", "[from source]+[inference]", "DJT p.2"),
    "FLASK-NOT-COVERED": ("INFO", "NOT COVERED", "FLT p.1-3"),
    "PY-SYNTAX": ("INFO", "[extrapolation]", "-"),
}


def finding(rule, line, msg):
    sev, origem, pag = RULES[rule]
    return {"id": rule, "sev": sev, "origem": origem, "pagina": pag, "linha": line, "msg": msg}


def dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def is_path_call(node):
    return isinstance(node, ast.Call) and ((isinstance(node.func, ast.Name) and node.func.id == "path")
                                            or (isinstance(node.func, ast.Attribute) and node.func.attr == "path"))


def route_decorator(fn):
    """Return (method, path|None) if the function has a @something.get/put/... decorator; otherwise None."""
    for d in fn.decorator_list:
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr in HTTP:
            path = None
            if d.args and isinstance(d.args[0], ast.Constant) and isinstance(d.args[0].value, str):
                path = d.args[0].value
            for kw in d.keywords:
                if kw.arg == "path" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    path = kw.value.value
            return d.func.attr, path
    return None


def own_await(fn):
    """Is there an 'await' directly in the function (without descending into nested functions/lambdas)?"""
    stack = list(fn.body)
    while stack:
        n = stack.pop()
        if isinstance(n, ast.Await):
            return n.lineno
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        stack.extend(ast.iter_child_nodes(n))
    return None


def is_optional_ann(ann):
    if ann is None:
        return False
    if isinstance(ann, ast.BinOp) and isinstance(ann.op, ast.BitOr):
        return any(isinstance(s, ast.Constant) and s.value is None for s in (ann.left, ann.right)) or is_optional_ann(ann.left) or is_optional_ann(ann.right)
    if isinstance(ann, ast.Subscript) and dotted(ann.value).split(".")[-1] == "Optional":
        return True
    return False


def params_with_defaults(fn):
    a = fn.args
    pos = list(a.posonlyargs) + list(a.args)
    defs = [None] * (len(pos) - len(a.defaults)) + list(a.defaults)
    out = list(zip(pos, defs))
    out += list(zip(a.kwonlyargs, a.kw_defaults))
    return out


def lint_python(src):
    res = []
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [finding("PY-SYNTAX", e.lineno or 0, f"file is not valid Python ({e.msg}); AST rules not applied")]
    local_classes = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            local_classes[n.name] = [dotted(b).split(".")[-1] for b in n.bases]
    imports_flask = any((isinstance(n, ast.Import) and any(x.name.split(".")[0] == "flask" for x in n.names)) or
                        (isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0] == "flask") for n in ast.walk(tree))
    if imports_flask:
        res.append(finding("FLASK-NOT-COVERED", 1, "file imports flask: the FLT (index only) supports no Flask code rule; no rule applied to it"))

    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and is_path_call(n):
            nargs = len(n.args) + sum(1 for k in n.keywords if k.arg in ("route", "view"))
            if nargs < 2:
                res.append(finding("DJ-PATH-ARGS", n.lineno, "path() takes route and view as required arguments"))
            view = n.args[1] if len(n.args) > 1 else next((k.value for k in n.keywords if k.arg == "view"), None)
            route = n.args[0] if n.args else next((k.value for k in n.keywords if k.arg == "route"), None)
            if view is not None:
                if isinstance(view, ast.Attribute) and view.attr == "urls" and dotted(view) != "admin.site.urls":
                    res.append(finding("DJ-INCLUDE", n.lineno, f"'{dotted(view)}' passed directly; use include() (admin.site.urls is the only exception)"))
                elif isinstance(view, ast.Constant) and isinstance(view.value, str) and view.value.endswith(".urls"):
                    res.append(finding("DJ-INCLUDE", n.lineno, f"string '{view.value}' passed as the view; use include('{view.value}')"))
            if isinstance(route, ast.Constant) and isinstance(route.value, str) and "?" in route.value:
                res.append(finding("DJ-ROUTE-QUERY", n.lineno, "route with '?': the URLconf does not consider GET/POST parameters or the domain"))
            if not any(k.arg == "name" for k in n.keywords) and len(n.args) < 4:
                res.append(finding("DJ-NAME-MISSING", n.lineno, "path() without name (optional); naming lets other places reference the URL"))
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = n.args
            nparams = len(a.posonlyargs) + len(a.args) + len(a.kwonlyargs) + (1 if a.vararg else 0)
            if nparams == 0 and not n.decorator_list:
                for r in ast.walk(n):
                    if isinstance(r, ast.Return) and isinstance(r.value, ast.Call) and dotted(r.value.func).split(".")[-1] == "HttpResponse":
                        res.append(finding("DJ-VIEW-REQUEST", n.lineno, f"'{n.name}' returns HttpResponse but declares no parameters; the view receives HttpRequest as its 1st argument"))
                        break
            rd = route_decorator(n)
            if rd:
                method, rpath = rd
                if isinstance(n, ast.FunctionDef):
                    ln = own_await(n)
                    if ln:
                        res.append(finding("FA-AWAIT-IN-DEF", ln, f"route '{n.name}' uses await in a 'def' function; use 'async def'"))
                pnames = re.findall(r"\{(\w+)(?::[^}]*)?\}", rpath or "")
                plist = params_with_defaults(n)
                byname = {p.arg: (p, d) for p, d in plist}
                for pn in pnames:
                    if pn not in byname:
                        res.append(finding("FA-PATH-MISSING", n.lineno, f"path '{rpath}' declares {{{pn}}} but '{n.name}' has no parameter '{pn}'"))
                    elif byname[pn][0].annotation is None:
                        res.append(finding("FA-PATH-UNTYPED", n.lineno, f"path parameter '{pn}' has no type: validation/conversion comes from the declared type"))
                for p, d in plist:
                    if p.arg in pnames:
                        continue
                    if d is None and is_optional_ann(p.annotation):
                        res.append(finding("FA-OPTIONAL-NODEF", p.lineno, f"'{p.arg}' has '| None' but no '= None': per the source, it is '= None' that makes the parameter optional"))
                    if method in BODY_METHODS and isinstance(p.annotation, ast.Name) and p.annotation.id in local_classes:
                        if "BaseModel" not in local_classes[p.annotation.id]:
                            res.append(finding("FA-BODY-NOT-MODEL", p.lineno, f"body '{p.arg}: {p.annotation.id}' uses a local class that does not inherit BaseModel; the source declares the body with Pydantic"))
    return res


def lint_commands(text, fname):
    res = []
    base = os.path.basename(fname).lower()
    deploy_file = base.startswith("dockerfile") or base == "procfile" or base.endswith((".service", ".yml", ".yaml"))
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("#") and not s.startswith("#!"):
            continue  # shell/yaml comment: data, not a command
        m = re.search(r"startproject\s+([^\s;|&]+)", s)
        if m and m.group(1).strip("\"'") in ("django", "test"):
            res.append(finding("CMD-PROJNAME", i, f"startproject '{m.group(1)}': avoid names such as django (conflicts with Django) or test (Python package)"))
        if re.search(r"\b(pip3?\s+install|uv\s+add|uv\s+pip\s+install|python\s+-m\s+pip\s+install)\b", s):
            if re.search(r"(?<![\"'])fastapi\[standard[^\]]*\](?![\"'])", s):
                res.append(finding("CMD-QUOTE", i, "put \"fastapi[standard]\" in quotes so it works in all terminals"))
        if deploy_file and re.search(r"manage\.py\s+runserver", re.sub(r"[\"',\[\]]", " ", s)):
            res.append(finding("CMD-RUNSERVER-PROD", i, "runserver in a deployment file: the development server must not be used in production"))
    return res


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules", ".venv", "venv")]
                for f in sorted(files):
                    yield os.path.join(root, f)
        else:
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    a = ap.parse_args()
    if a.rules:
        for k, (sev, origem, pag) in RULES.items():
            print(f"{k}: {sev} {origem} ({pag})")
        return 0
    if not a.paths:
        ap.print_help()
        return 2
    allf = []
    nfiles = 0
    for fp in iter_files(a.paths):
        if os.path.islink(fp) or not os.path.isfile(fp):
            if not os.path.exists(fp):
                print(f"WARNING: {fp} does not exist")
            continue
        low = os.path.basename(fp).lower()
        if os.path.getsize(fp) > MAX_BYTES:
            print(f"WARNING: {fp} skipped (> 1 MB)")
            continue
        isdeploy = low.startswith("dockerfile") or low == "procfile"
        if not (low.endswith(".py") or low.endswith(TEXT_EXT) or isdeploy):
            continue
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        nfiles += 1
        fs = lint_python(text) if low.endswith(".py") else lint_commands(text, fp)
        for x in fs:
            x["arquivo"] = fp
        allf.extend(fs)
    allf.sort(key=lambda x: (x["arquivo"], x["linha"], x["id"]))
    if a.json:
        print(json.dumps({"arquivos": nfiles, "achados": allf}, ensure_ascii=False, indent=1))
    else:
        for x in allf:
            print(f"{x['arquivo']}:{x['linha']}: {x['sev']} {x['id']} {x['origem']} ({x['pagina']}) {x['msg']}")
        if not allf:
            print(f"No findings in {nfiles} file(s) (only rules supported by the sources; absence of findings does not prove correctness).")
        else:
            ne = sum(1 for x in allf if x["sev"] == "ERROR")
            print(f"{len(allf)} finding(s), {ne} ERROR(s), in {nfiles} file(s).")
    return 1 if any(x["sev"] == "ERROR" for x in allf) else 0


if __name__ == "__main__":
    sys.exit(main())
