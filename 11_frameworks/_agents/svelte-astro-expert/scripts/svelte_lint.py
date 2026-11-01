# -*- coding: utf-8 -*-
"""
svelte_lint.py - STATIC linter for .svelte components, with rules backed by The Svelte Handbook
(SVHB = Flavio Copes, freeCodeCamp, header 22 Oct 2019; Svelte version not declared; pre-runes syntax:
`export let`, `$:`, `on:event`, `bind:`, `<slot>`, `createEventDispatcher`). It never executes the analyzed code.

Usage:
  python -I scripts/svelte_lint.py FILE [FILE...] [--json] [--rules] [--no-info]
  python -I scripts/svelte_lint.py - < Component.svelte        (reads from standard input)

Output: each finding carries rule, severity, line, ORIGIN ([from source] | [inference] | [extrapolation]) and page.
Exit code: 1 if there is an "error" finding; 0 otherwise; 2 on invalid usage.
It is heuristic (regex; not a Svelte parser): false positives/negatives are possible.
Boundary: the collection does NOT cover runes ($state, $props...), snippets, SvelteKit (+page.svelte, load) or Astro (.astro);
in those cases the linter only warns NOT COVERED (SVL-X01/X02) and does not invent rules.
[DATED] all rules apply to the handbook syntax (2019); how current Svelte versions treat these patterns is NOT COVERED.
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
    "SVL-A01": ("warn", "[from source]", "SVHB p.15-16",
                "Array-mutating method (push/pop/shift/splice) without reassignment: the text says Svelte does not detect the change; reassign (`list = list`) or use spread (`list = [...list, x]`)."),
    "SVL-A02": ("info", "[inference]", "SVHB p.15-16",
                "Array-mutating method not listed by the text (unshift/sort/reverse...) without reassignment: the text cites the 4 methods and an ellipsis; treated by analogy."),
    "SVL-B01": ("error", "[from source]", "SVHB p.33",
                "`bind:value` on a `const` variable: the text requires `let`/`var`, since `const` cannot be reassigned by Svelte."),
    "SVL-B02": ("warn", "[inference]", "SVHB p.33",
                "`bind:` on a `const` variable: the text states the rule for `bind:value`; extended by analogy to other bindings."),
    "SVL-E01": ("info", "[from source]", "SVHB p.43",
                "`{#each}` without a key `(id)`: when adding/removing items dynamically the text recommends always passing an identifier."),
    "SVL-L01": ("warn", "[from source]", "SVHB p.31-32",
                "`setInterval` without `clearInterval`: the text shows clearing timers in `onDestroy` or in the function returned by `onMount`."),
    "SVL-L02": ("warn", "[from source]", "SVHB p.31",
                "Lifecycle function used without importing from 'svelte': the text says there is no access by default (`import { onMount, ... } from 'svelte'`)."),
    "SVL-L03": ("info", "[extrapolation]", "NO page in the collection",
                "`onMount(async ...)` returning a cleanup function: SVHB p.32 shows exactly this, but other Svelte documentation may treat async `onMount` differently; the collection does not discuss it (NOT COVERED)."),
    "SVL-S01": ("error", "[from source]", "SVHB p.25",
                "User-declared identifier starting with `$`: the text says Svelte reserves `$` for store values and prevents using it for anything else (do not prefix DOM references with `$`)."),
    "SVL-S02": ("warn", "[inference]", "SVHB p.25",
                "`$name` without `name` declared/imported in the component: `$x` only makes sense for a store `x` (the text shows `$username` from `username`)."),
    "SVL-ST01": ("error", "[from source]", "SVHB p.26",
                 "Store created with `readable()` receiving `.set()`/`.update()`: the text says readable has no such methods (it is not changed from outside)."),
    "SVL-ST02": ("warn", "[from source]", "SVHB p.23,26-27",
                 "`writable`/`readable`/`derived` used without importing from 'svelte/store'."),
    "SVL-M01": ("warn", "[from source]", "SVHB p.12-13",
                "`export function/const/class` in the regular `<script>`: the text says to write exports beyond the component in `<script context=\"module\">` (props use `export let`)."),
    "SVL-P01": ("info", "[inference]", "SVHB p.19-20,38-39",
                "Assignment to a prop (`export let`) inside the component: props are one-way parent->child communication (p.19); `bind:` on the prop is the two-way path (p.38-39)."),
    "SVL-D01": ("warn", "[from source]", "SVHB p.47-48",
                "`dispatch(...)` without `createEventDispatcher`: the text imports the function from 'svelte' and calls it to obtain the dispatcher."),
    "SVL-AW01": ("info", "[from source]", "SVHB p.45",
                 "`{#await}` without `{:catch}`: the text shows the `{:catch}` block to detect promise rejection."),
    "SVL-EV01": ("info", "[from source]", "SVHB p.47",
                 "`on:submit` without the `|preventDefault` modifier (nor `preventDefault(` in the code): the text cites the modifiers to avoid the default submit."),
    "SVL-EV02": ("info", "[inference]", "SVHB p.45",
                 "Event attribute in the `onclick={...}` style: the handbook only uses `on:event` (p.45-46). Whether this syntax is valid in current versions is NOT COVERED ([DATED])."),
    "SVL-SL01": ("warn", "[inference]", "SVHB p.29",
                 "More than one `<slot>` without `name`: the text says the only unnamed slot is the default one."),
    "SVL-R01": ("info", "[inference]", "SVHB p.38",
                "`bind:this` variable used at the top of the script: the element only exists after being mounted; the text associates `bind:this` with use in `onMount()`."),
    "SVL-X01": ("info", "[extrapolation]", "NOT COVERED",
                "Runes/snippets ($state, $props, $derived, $effect, $bindable, {#snippet}, {@render}) appear in NO source of the collection; this linter's state/props rules follow the handbook syntax (2019) and were turned off for this file."),
    "SVL-X02": ("info", "[extrapolation]", "NOT COVERED",
                "SvelteKit convention file (+page/+layout/+server) or .astro: the collection does not cover file-based routing, load, actions or Astro syntax (SKGS p.2 only mentions the router in general; ASTRO p.2 only mentions 'Astro components')."),
}
SEV = {"error": 0, "warn": 1, "info": 2}
LIFE = ("onMount", "onDestroy", "beforeUpdate", "afterUpdate")
RUNE_NAMES = {"state", "props", "derived", "effect", "bindable", "inspect", "host"}
KW = {"if", "else", "each", "await", "then", "catch", "key", "html", "debug", "const"}


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def strip_comments(text):
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    text = re.sub(r"(?<![:\"'\w])//[^\n]*", blank, text)
    return text


def blank_strings(code):
    def rep(m):
        s = m.group(0)
        return s[0] + re.sub(r"[^\n]", " ", s[1:-1]) + s[-1]
    return re.sub(r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"", rep, code)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def lint(text, filename=""):
    F = []
    code = strip_comments(text)
    scripts = []
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", code, flags=re.S):
        scripts.append((m.group(1), m.start(2), m.end(2)))
    styles = [(m.start(), m.end()) for m in re.finditer(r"<style\b[^>]*>.*?</style>", code, flags=re.S)]
    mask = list(code)
    for _, s, e in scripts:
        for i in range(s, e):
            if mask[i] != "\n":
                mask[i] = " "
    for s, e in styles:
        for i in range(s, e):
            if mask[i] != "\n":
                mask[i] = " "
    markup = "".join(mask)
    inst = [(s, e) for a, s, e in scripts if "context" not in a]
    mod = [(s, e) for a, s, e in scripts if "context" in a]
    script_all = "\n".join(code[s:e] for _, s, e in scripts)

    def add(rule, pos, extra=""):
        sev, org, cite, msg = RULES[rule]
        F.append({"regra": rule, "severidade": sev, "linha": line_of(text, pos), "origem": org,
                  "citacao": cite, "mensagem": msg + (" " + extra if extra else "")})

    base = filename.replace("\\", "/").split("/")[-1]
    if base.startswith("+") or base.endswith(".astro"):
        add("SVL-X02", 0, f"File: {base}.")
        if base.endswith(".astro"):
            return F
    runes = re.search(r"\$(state|props|derived|effect|bindable)\b|\{#snippet\b|\{@render\b", code)
    if runes:
        add("SVL-X01", runes.start())

    # declarations
    declared = set()
    for sm in re.finditer(r"\b(?:let|const|var|function|class)\s+([A-Za-z_$][\w$]*)", script_all):
        declared.add(sm.group(1))
    for sm in re.finditer(r"import\s+([^;\n]*?)\s+from\s+['\"][^'\"]+['\"]", script_all):
        for nm in re.findall(r"[A-Za-z_$][\w$]*", sm.group(1)):
            declared.add(nm)
    for sm in re.finditer(r"\blet\s*\{([^}]*)\}", script_all):
        for nm in re.findall(r"[A-Za-z_$][\w$]*", sm.group(1)):
            declared.add(nm)
    consts = set(re.findall(r"\bconst\s+([A-Za-z_$][\w$]*)", script_all))
    lets = set(re.findall(r"\blet\s+([A-Za-z_$][\w$]*)", script_all))
    off = {}
    for s, e in inst:
        for mm in re.finditer(r"\bexport\s+let\s+([A-Za-z_$][\w$]*)", code[s:e]):
            off.setdefault(mm.group(1), s + mm.start())

    # SVL-A01/A02: array mutation without reassignment
    if not runes:
        for s, e in inst:
            body = code[s:e]
            for mm in re.finditer(r"(?<![\w$.])(?P<n>[A-Za-z_$][\w$]*)\.(?P<m>push|pop|shift|splice|unshift|sort|reverse)\(", body):
                name, meth = mm.group("n"), mm.group("m")
                if name not in lets:
                    continue
                if not re.search(r"\{[^}]*\b" + re.escape(name) + r"\b|#each\s+" + re.escape(name) + r"\b", markup):
                    continue
                rest = body[mm.end():]
                nxt = "\n".join(rest.splitlines()[:3])
                if re.search(r"(?m)^\s*(?:[^\n]*;\s*)?" + re.escape(name) + r"\s*=[^=]", nxt) or re.search(r"\)\s*;?\s*" + re.escape(name) + r"\s*=[^=]", nxt):
                    continue
                add("SVL-A01" if meth in ("push", "pop", "shift", "splice") else "SVL-A02", s + mm.start("n"),
                    f"Variable `{name}`, method `{meth}`.")

    # SVL-B01/B02
    for mm in re.finditer(r"\bbind:(\w+)\s*=\s*\{\s*([A-Za-z_$][\w$]*)\s*\}", markup):
        kind, var = mm.group(1), mm.group(2)
        if var in consts and var not in lets:
            add("SVL-B01" if kind == "value" else "SVL-B02", mm.start(), f"`bind:{kind}={{{var}}}`, `{var}` is const.")

    # SVL-E01
    for mm in re.finditer(r"\{#each\s+([^}]*)\}", markup):
        hdr = mm.group(1).strip()
        if " as " in hdr and not hdr.endswith(")"):
            add("SVL-E01", mm.start(), f"`{{#each {hdr[:60]}}}`.")

    # SVL-L01/L02/L03
    if re.search(r"\bsetInterval\s*\(", script_all) and not re.search(r"\bclearInterval\s*\(", script_all):
        m0 = re.search(r"\bsetInterval\s*\(", code)
        add("SVL-L01", m0.start() if m0 else 0)
    imported = set()
    for sm in re.finditer(r"import\s*\{([^}]*)\}\s*from\s*['\"]svelte['\"]", script_all):
        imported.update(x.strip().split(" as ")[0].strip() for x in sm.group(1).split(","))
    for fn in LIFE:
        mm = re.search(r"(?<![\w.$])" + fn + r"\s*\(", script_all)
        if mm and fn not in imported and fn not in declared:
            pos = code.find(mm.group(0))
            add("SVL-L02", pos if pos >= 0 else 0, f"`{fn}`.")
    mm = re.search(r"onMount\s*\(\s*async\b", script_all)
    if mm:
        add("SVL-L03", code.find(mm.group(0)))

    # SVL-S01 / S02
    sn = blank_strings(script_all)
    for mm in re.finditer(r"\b(?:let|const|var|function)\s+(\$[A-Za-z_][\w$]*)", sn):
        pos = code.find(mm.group(0))
        add("SVL-S01", pos if pos >= 0 else 0, f"Identifier `{mm.group(1)}`.")
    if not runes:
        seen = set(re.findall(r"\b(?:let|const|var|function)\s+\$([A-Za-z_][\w$]*)", sn))
        scan = [(m_.start(), m_.group(0)) for m_ in re.finditer(r"[^\n]*", markup)]
        cand = []
        for ln_pos, ln in scan:
            if not ln.strip():
                continue
            for mm in re.finditer(r"(?<![\w$])\$([A-Za-z_]\w*)", ln):
                cand.append((ln_pos + mm.start(), mm.group(1)))
        for mm in re.finditer(r"(?<![\w$])\$([A-Za-z_]\w*)", sn):
            cand.append((None, mm.group(1)))
        for pos, nm in cand:
            if nm in declared or nm in RUNE_NAMES or nm in KW or nm in seen:
                continue
            # `$:` does not match (colon is not a letter); `$$props` is discarded by the lookbehind
            seen.add(nm)
            add("SVL-S02", pos if pos is not None else code.find("$" + nm), f"`${nm}` without `{nm}` declared.")

    # SVL-ST01 / ST02
    for nm in re.findall(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*readable\s*\(", script_all):
        mm = re.search(r"(?<![\w$.])" + re.escape(nm) + r"\.(set|update)\s*\(", code)
        if mm:
            add("SVL-ST01", mm.start(), f"`{nm}.{mm.group(1)}()`.")
    imp_store = set()
    for sm in re.finditer(r"import\s*\{([^}]*)\}\s*from\s*['\"]svelte/store['\"]", script_all):
        imp_store.update(x.strip().split(" as ")[0].strip() for x in sm.group(1).split(","))
    for fn in ("writable", "readable", "derived"):
        mm = re.search(r"(?<![\w$.])" + fn + r"\s*\(", sn)
        if mm and fn not in imp_store and fn not in declared:
            add("SVL-ST02", code.find(mm.group(0)), f"`{fn}`.")

    # SVL-M01
    for s, e in inst:
        for mm in re.finditer(r"\bexport\s+(function|const|class|async\s+function)\b", code[s:e]):
            add("SVL-M01", s + mm.start(), f"`export {mm.group(1)}`.")

    # SVL-P01
    if not runes:
        for name, pos in off.items():
            for mm in re.finditer(r"(?<![\w$.])" + re.escape(name) + r"\s*(\+\+|--|[-+*/]?=(?!=))", code):
                if abs(mm.start() - pos) < len("export let " + name) + 1:
                    continue
                if code[max(0, mm.start() - 12):mm.start()].rstrip().endswith("let"):
                    continue
                add("SVL-P01", mm.start(), f"Prop `{name}`.")
                break

    # SVL-D01
    if re.search(r"(?<![\w$.])dispatch\s*\(", script_all) and "createEventDispatcher" not in script_all:
        add("SVL-D01", code.find("dispatch("))

    # SVL-AW01
    for mm in re.finditer(r"\{#await\b", markup):
        end = markup.find("{/await}", mm.end())
        blk = markup[mm.end():end if end != -1 else len(markup)]
        if "{:catch" not in blk:
            add("SVL-AW01", mm.start())

    # SVL-EV01 / EV02
    if re.search(r"\bon:submit(?!\|[\w|]*preventDefault)\b", markup) and not re.search(r"preventDefault", code):
        mm = re.search(r"\bon:submit\b", markup)
        add("SVL-EV01", mm.start())
    for mm in re.finditer(r"<[A-Za-z][^>]*?\s(on[A-Za-z]+)\s*=\s*\{", markup):
        add("SVL-EV02", mm.start(1), f"`{mm.group(1)}=`.")
        break

    # SVL-SL01
    unnamed = [m_.start() for m_ in re.finditer(r"<slot\b(?![^>]*\bname\s*=)[^>]*>", markup)]
    if len(unnamed) > 1:
        add("SVL-SL01", unnamed[1])

    # SVL-R01
    for mm in re.finditer(r"\bbind:this\s*=\s*\{\s*([A-Za-z_$][\w$]*)\s*\}", markup):
        v = mm.group(1)
        for s, e in inst:
            body = code[s:e]
            for um in re.finditer(r"(?m)^(\S[^\n]*?)(?<![\w$])" + re.escape(v) + r"\.\w+", body):
                line = um.group(0)
                if line.lstrip().startswith(("let ", "const ", "var ", "//", "import ")):
                    continue
                add("SVL-R01", s + um.start(), f"Variable `{v}`.")
                break
    F.sort(key=lambda x: (x["linha"], SEV[x["severidade"]], x["regra"]))
    return F


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--no-info", action="store_true")
    a = ap.parse_args()
    if a.rules:
        for k, (sev, org, cite, msg) in RULES.items():
            print(f"{k}  {sev:5} {org} ({cite})  {msg}")
        return 0
    if not a.files:
        ap.print_usage(sys.stderr)
        return 2
    out, worst = [], 0
    for f in a.files:
        try:
            if f == "-":
                text = sys.stdin.read()
            else:
                with open(f, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
        except OSError as ex:
            print(f"error reading {f}: {ex}", file=sys.stderr)
            return 2
        res = lint(text, f if f != "-" else "")
        if a.no_info:
            res = [r for r in res if r["severidade"] != "info"]
        for r in res:
            r["arquivo"] = f
            if r["severidade"] == "error":
                worst = 1
        out.extend(res)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        if not out:
            print("No findings (SVHB rules). This does not prove correctness: the linter is heuristic and the sources are short.")
        for r in out:
            print(f"{r['arquivo']}:{r['linha']} [{r['severidade']}] {r['regra']} {r['origem']} ({r['citacao']}) {r['mensagem']}")
    return worst


if __name__ == "__main__":
    sys.exit(main())
