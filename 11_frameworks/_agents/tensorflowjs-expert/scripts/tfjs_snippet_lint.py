# -*- coding: utf-8 -*-
"""
tfjs_snippet_lint.py - static linter for TF.js snippets/configs. Only rules backed by the captures
(TFJS = Tutorial-Setup, TFJI = Getting started). Does not run the file, no network.

Usage: python -I scripts/tfjs_snippet_lint.py FILE [FILE...] [--json] [--strict]
Accepts .html, .js, .mjs, .cjs, .ts and .json (package.json, tsconfig.json).
Output: ID, severity (WARN/INFO), origin label ([from source]/[inference]/[extrapolation]), page, message.
Exit 1 if there is a WARN (or INFO with --strict).

Rules:
  L01 WARN  [inference] `tf.` used without a tfjs script tag, import or require (the global `tf` comes from the tag) - TFJS p.2
  L02 WARN  [inference] `tf` loaded after the first script that uses it (HTML) - TFJI p.2
  L03 WARN  [inference] tfjs-node and tfjs-node-gpu in the same file/package.json: the text presents them as alternative options - TFJS p.4
  L04 WARN  [inference] @tensorflow/tfjs together with tfjs-node(-gpu): the text says tfjs is imported indirectly - TFJS p.4-5
  L05 WARN  [inference] tf.sequential + fit without compile in the file (the text: compile prepares the model with loss and optimizer) - TFJI p.3
  L06 INFO  [from source] tfjs-node-gpu: Linux only with NVIDIA GPU/CUDA - TFJS p.5
  L07 INFO  [from source] require('@tensorflow/tfjs') on Node: slowest option - TFJS p.6
  L08 INFO  [from source] tsconfig with strict null checking and without skipLibCheck: true: "perhaps" needed - TFJS p.6
  L09 INFO  [extrapolation] CDN with @latest and no pinned version (the source uses @latest; pinning a version is not addressed)
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

TAG_RE = re.compile(r"<script[^>]+src=[\"'][^\"']*@tensorflow/tfjs[^\"']*[\"']", re.I)
IMPORT_RE = re.compile(r"(import\s+[^;]*from\s+['\"]@tensorflow/tfjs[^'\"]*['\"]|require\(\s*['\"]@tensorflow/tfjs[^'\"]*['\"]\s*\))")
USE_TF_RE = re.compile(r"(?<![\w.$])tf\.[A-Za-z_]")


def strip_comments(js):
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    return re.sub(r"(?m)(?<![:\"'])//.*$", "", js)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def lint_json(path, text):
    out = []
    try:
        d = json.loads(text)
    except Exception as e:
        return [("L00", "INFO", "[extrapolation]", "-", 1, f"invalid JSON: {e}")]
    base = os.path.basename(path).lower()
    if base.startswith("tsconfig"):
        co = d.get("compilerOptions", {}) if isinstance(d, dict) else {}
        strict = co.get("strict") is True or co.get("strictNullChecks") is True
        if strict and co.get("strictNullChecks") is not False and co.get("skipLibCheck") is not True:
            out.append(("L08", "INFO", "[from source]", "TFJS p.6", 1,
                        "strict null checking without skipLibCheck: true; the text says it may be needed to avoid compilation errors"))
    else:
        deps = {}
        for k in ("dependencies", "devDependencies"):
            if isinstance(d, dict) and isinstance(d.get(k), dict):
                deps.update(d[k])
        node, gpu, pure = "@tensorflow/tfjs-node" in deps, "@tensorflow/tfjs-node-gpu" in deps, "@tensorflow/tfjs" in deps
        if node and gpu:
            out.append(("L03", "WARN", "[inference]", "TFJS p.4", 1, "tfjs-node and tfjs-node-gpu together; the text presents the options as alternatives (pick one of them)"))
        if pure and (node or gpu):
            out.append(("L04", "WARN", "[inference]", "TFJS p.4-5", 1, "@tensorflow/tfjs together with tfjs-node(-gpu); the text says tfjs is imported indirectly by them"))
        if gpu:
            out.append(("L06", "INFO", "[from source]", "TFJS p.5", 1, "tfjs-node-gpu: Linux only, NVIDIA GPU with CUDA support"))
    return out


def lint_code(path, text, is_html):
    out = []
    code = text
    scripts_pos = []
    if is_html:
        tag_m = TAG_RE.search(text)
        for m in TAG_RE.finditer(text):
            if "@latest" in m.group(0) and not re.search(r"@tensorflow/tfjs@\d", m.group(0)):
                out.append(("L09", "INFO", "[extrapolation]", "-", line_of(text, m.start()), "CDN with @latest (the source does it this way); version pinning is not addressed in the captures"))
                break
        # inline script blocks
        inline = [(m.start(1), m.group(1)) for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", text, flags=re.S | re.I)]
        code = "\n".join(b for _, b in inline)
        first_use = next((p for p, b in inline if USE_TF_RE.search(strip_comments(b))), None)
        has_tag = tag_m is not None
        has_import = bool(IMPORT_RE.search(code))
        if first_use is not None and not has_tag and not has_import:
            out.append(("L01", "WARN", "[inference]", "TFJS p.2", line_of(text, first_use), "tf.* used without a tfjs script tag or import/require"))
        elif first_use is not None and has_tag and tag_m.start() > first_use:
            out.append(("L02", "WARN", "[inference]", "TFJI p.2", line_of(text, tag_m.start()), "tfjs script appears after the first script that uses tf"))
    else:
        code = strip_comments(text)
        if USE_TF_RE.search(code) and not IMPORT_RE.search(code):
            out.append(("L01", "WARN", "[inference]", "TFJS p.2", line_of(text, USE_TF_RE.search(code).start()),
                        "tf.* used without a tfjs import/require (the global tf only comes from the script tag)"))
    c = strip_comments(code)
    mods = set(re.findall(r"['\"](@tensorflow/tfjs(?:-node-gpu|-node)?)['\"]", c))
    node, gpu, pure = "@tensorflow/tfjs-node" in mods, "@tensorflow/tfjs-node-gpu" in mods, "@tensorflow/tfjs" in mods
    if node and gpu:
        out.append(("L03", "WARN", "[inference]", "TFJS p.4", 1, "tfjs-node and tfjs-node-gpu in the same file; they are alternative options"))
    if pure and (node or gpu):
        out.append(("L04", "WARN", "[inference]", "TFJS p.4-5", 1, "@tensorflow/tfjs together with tfjs-node(-gpu); tfjs is already imported indirectly"))
    if gpu:
        out.append(("L06", "INFO", "[from source]", "TFJS p.5", 1, "tfjs-node-gpu: Linux only, NVIDIA GPU with CUDA support"))
    if re.search(r"require\(\s*['\"]@tensorflow/tfjs['\"]\s*\)", c):
        out.append(("L07", "INFO", "[from source]", "TFJS p.6", 1, "require('@tensorflow/tfjs') on Node is the slowest option in performance"))
    if "tf.sequential" in c and re.search(r"\.fit\(", c) and not re.search(r"\.compile\(", c):
        out.append(("L05", "WARN", "[inference]", "TFJI p.3", 1, "model.fit without model.compile in the file (the text prepares the model with compile: loss and optimizer)"))
    return out


def lint(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        return lint_json(path, text)
    return lint_code(path, text, ext in (".html", ".htm"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    allr, bad = [], False
    for p in a.files:
        for rid, sev, org, pg, ln, msg in lint(p):
            allr.append({"arquivo": p, "id": rid, "sev": sev, "origem": org, "pagina": pg, "linha": ln, "msg": msg})
            if sev == "WARN" or (a.strict and sev == "INFO"):
                bad = True
    if a.json:
        print(json.dumps(allr, ensure_ascii=False, indent=1))
    else:
        for r in allr:
            print(f"{r['arquivo']}:{r['linha']} {r['id']} {r['sev']} {r['origem']} ({r['pagina']}) {r['msg']}")
        if not allr:
            print("No findings under the rules backed by the captures (this does not guarantee the code is correct).")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
