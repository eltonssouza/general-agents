# -*- coding: utf-8 -*-
"""
vue_lint.py - STATIC linter for Vue components/templates, with rules backed by the collection texts
(VUEHB = Vue Handbook, 5 Jul 2018, Vue 2; VUE3G = Vue 3 introduction). Never executes the analyzed code.

Usage:
  python -I scripts/vue_lint.py FILE [FILE...] [--json] [--rules] [--no-info]
  python -I scripts/vue_lint.py - < component.vue       (reads from standard input)

Output: each finding has rule, severity, line, ORIGIN ([from source] | [inference] | [extrapolation]) and page.
Exit code: 1 if there is a finding of severity "error"; 0 otherwise; 2 invalid usage.
It is heuristic (regex + brace counting): not a Vue parser; false positives/negatives are possible.
Rules without support in the text do NOT exist here (e.g. ":key" in v-for is not checked: the collection does not cover it).
[DATED] VUEHB rules apply to the 2018 Vue 2 style; VUE3G is an introduction page (few rules).
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
    "VUE-D01": ("warn", "[from source]", "VUEHB p.71,73", "`data` as an arrow function: the text says a regular function is needed when using `this` (an arrow does not bind `this` to the component)."),
    "VUE-C01": ("warn", "[from source]", "VUEHB p.92,106", "Arrow function in computed/methods/watch using `this`: the text avoids arrows in these cases (use a regular function)."),
    "VUE-M01": ("error", "[from source]", "VUEHB p.89-90", "`this.data.x` raises an error: access the property directly (`this.x`)."),
    "VUE-T01": ("error", "[from source]", "VUEHB p.74", "Interpolation accepts a single JavaScript expression; `;` indicates multiple statements."),
    "VUE-T02": ("error", "[from source]", "VUEHB p.82", "Interpolation `{{ }}` does not work in attributes; use `v-bind`/`:`."),
    "VUE-T03": ("warn", "[inference]", "VUEHB p.82", "`v-html` does not escape HTML (interpolation escapes and protects against XSS); use it only with trusted content."),
    "VUE-T04": ("info", "[from source]", "VUEHB p.87", "Form with submit but no `.prevent`: the page reloads (default behavior); the text shows `v-on:submit.prevent`."),
    "VUE-T05": ("info", "[from source]", "VUEHB p.118", "`@change` on a text field only fires on blur; the text uses `@input` for each keystroke."),
    "VUE-P01": ("error", "[from source]", "VUEHB p.107", "Prop being changed in the child component: props are one-way and must never be mutated."),
    "VUE-W01": ("warn", "[from source]", "VUEHB p.93-94", "`Date.now()` in computed: renders once and does not update (computed only reacts to reactive sources); the text points to a method."),
    "VUE-R01": ("warn", "[from source]", "VUEHB p.128", "Guard `beforeEach` without a call to `next(...)`: the text says `next()` must always be called, otherwise execution hangs."),
    "VUE-V01": ("error", "[from source]", "VUEHB p.116", "Direct assignment to `$store.state`: Vuex state is only changed by mutations (`commit`)."),
    "VUE-RT01": ("info", "[from source]", "VUEHB p.131", "`$route.params` couples the component to the router; the text suggests `props: true` on the route and `props` in the component."),
    "VUE-RT02": ("info", "[from source]", "VUEHB p.130", "Dynamic route: when only the parameter changes, the component is reused and calls `beforeRouteUpdate`."),
    "VUE-S01": ("info", "[from source]", "VUEHB p.69", "`<style>` without `scoped`: the CSS is global; with `scoped` Vue limits it to the component."),
    "VUE2-01": ("info", "[from source]", "VUEHB p.8,12", "Handbook-style construct (Vue 2, 2018): `new Vue(...)`. VUE3G (Vue 3) shows `createApp(...)` (p.1). Compatibility: NOT COVERED (migration guide outside the collection)."),
    "VUE2-02": ("info", "[from source]", "VUEHB p.63-65", "Handbook-style construct (Vue 2): `Vue.component(...)`. VUE3G does not show it. Compatibility: NOT COVERED."),
    "VUE2-03": ("info", "[from source]", "VUEHB p.113,121", "Handbook-style construct (Vue 2): `Vue.use(...)` (Vuex/Vue Router). VUE3G does not show it. Compatibility: NOT COVERED."),
    "VUE2-04": ("info", "[from source]", "VUEHB p.104-106", "Filters (`{{ x | filter }}`) appear in the handbook (Vue 2); VUE3G does not mention them. Do not claim removal: NOT COVERED."),
    "VUE2-05": ("info", "[from source]", "VUEHB p.103-104", "Attribute `slot=\"name\"`: named-slot syntax from the handbook (Vue 2); VUE3G does not cover slots. NOT COVERED."),
    "VUE2-06": ("info", "[from source]", "VUEHB p.109", "Event bus on `$root` (`$root.$on/$emit`): handbook pattern (Vue 2); VUE3G does not cover it. NOT COVERED."),
    "VUE3-01": ("warn", "[inference]", "VUE3G p.6", "Variable created with `ref(...)` used without `.value` in the script (the text example uses `count.value++` in the script and `count` only in the template)."),
    "VUE3-02": ("info", "[inference]", "VUE3G p.6; NUXT p.2", "`ref`/`onMounted` used in `<script setup>` without importing from 'vue' (the text example imports them; Nuxt projects have auto-imports, NUXT p.2)."),
}

SEV = {"error": 0, "warn": 1, "info": 2}


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def block(text, open_idx):
    """text of the {...} block whose '{' is at open_idx (simple brace counting, naive string handling)."""
    depth = 0
    i = open_idx
    n = len(text)
    while i < n:
        c = text[i]
        if c in "'\"`":
            q = c
            i += 1
            while i < n and text[i] != q:
                if text[i] == "\\":
                    i += 1
                i += 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return open_idx, i
        i += 1
    return open_idx, n - 1


def named_blocks(text, name):
    out = []
    for m in re.finditer(r"(?<![\w$.])" + name + r"\s*:\s*\{", text):
        s, e = block(text, m.end() - 1)
        out.append((s, e))
    return out


def split_sfc(text):
    parts = {"template": [], "script": [], "style": []}
    for tag in ("template", "script", "style"):
        for m in re.finditer(r"<" + tag + r"\b([^>]*)>", text):
            if tag == "template":
                end = text.rfind("</template>")
                if m.start() != text.find("<template") or end < m.end():
                    continue
                parts[tag].append((m.group(1), m.end(), end))
            else:
                end = text.find("</" + tag + ">", m.end())
                if end != -1:
                    parts[tag].append((m.group(1), m.end(), end))
    return parts


def lint(text, is_sfc, no_info=False):
    F = []

    def add(rule, pos, extra=""):
        sev, org, cite, msg = RULES[rule]
        if no_info and sev == "info":
            return
        F.append({"regra": rule, "severidade": sev, "linha": line_of(text, pos), "origem": org,
                  "citacao": cite, "mensagem": msg + (" " + extra if extra else "")})

    parts = split_sfc(text) if is_sfc else {"template": [], "script": [], "style": []}
    if is_sfc and parts["template"]:
        tpl_spans = [(s, e) for _, s, e in parts["template"]]
    else:
        tpl_spans = [(0, len(text))]
    script_spans = [(s, e, a) for a, s, e in parts["script"]] if is_sfc and parts["script"] else [(0, len(text), "")]

    # ---- template
    for s, e in tpl_spans:
        t = text[s:e]
        for m in re.finditer(r"\{\{(.*?)\}\}", t, re.S):
            inner = re.sub(r"&\w+;", "", m.group(1))
            inner_ns = re.sub(r"'[^']*'|\"[^\"]*\"|`[^`]*`", "", inner)
            if ";" in inner_ns:
                add("VUE-T01", s + m.start())
            if re.search(r"(?<!\|)\|(?!\|)", inner_ns):
                add("VUE2-04", s + m.start())
        for m in re.finditer(r"\s[:@\w.-]+\s*=\s*\"[^\"]*\{\{[^\"]*\"|\s[:@\w.-]+\s*=\s*'[^']*\{\{[^']*'", t):
            add("VUE-T02", s + m.start())
        for m in re.finditer(r"\bv-html\s*=", t):
            add("VUE-T03", s + m.start())
        for m in re.finditer(r"<form\b[^>]*?(?:@submit|v-on:submit)(?![.\w])[^>]*>", t, re.S):
            add("VUE-T04", s + m.start())
        for m in re.finditer(r"<input\b[^>]*?(?:@change|v-on:change)(?![.\w])[^>]*>", t, re.S):
            if not re.search(r"type\s*=\s*[\"'](?:checkbox|radio|file|range|date)", m.group(0)):
                add("VUE-T05", s + m.start())
        for m in re.finditer(r"\sslot\s*=\s*[\"'][^\"']+[\"']", t):
            add("VUE2-05", s + m.start())
        for m in re.finditer(r"\$route\.params", t):
            add("VUE-RT01", s + m.start())
            break

    # ---- script (or a whole .js file)
    for s, e, attrs in script_spans:
        t = text[s:e]
        is_setup = bool(re.search(r"\bsetup\b", attrs))
        for m in re.finditer(r"(?<![\w$.])data\s*:\s*(?:async\s*)?\(\s*\)\s*=>", t):
            add("VUE-D01", s + m.start())
        for nm in ("computed", "methods", "watch"):
            for bs, be in named_blocks(t, nm):
                seg = t[bs:be + 1]
                for m in re.finditer(r"[\w$]+\s*:\s*(?:async\s*)?(?:\([^)]*\)|[\w$]+)\s*=>", seg):
                    tail = seg[m.end():m.end() + 300]
                    nxt = re.search(r"\n\s*[\w$]+\s*(?::|\()", tail)
                    body = tail[:nxt.start()] if nxt else tail
                    if re.search(r"\bthis\b", body):
                        add("VUE-C01", s + bs + m.start())
                if nm == "computed":
                    for m in re.finditer(r"Date\.now\s*\(", seg):
                        add("VUE-W01", s + bs + m.start())
        for m in re.finditer(r"\bthis\.data\.", t):
            add("VUE-M01", s + m.start())
        # mutated props
        for ps, pe in named_blocks(t, "props"):
            # only level-1 keys
            depth = 0
            names = []
            seg = t[ps:pe + 1]
            i = 0
            while i < len(seg):
                c = seg[i]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                elif depth == 1:
                    mm = re.match(r"([A-Za-z_$][\w$]*)\s*:", seg[i:])
                    if mm and (i == 0 or not re.match(r"[\w$]", seg[i - 1])):
                        names.append(mm.group(1))
                        i += len(mm.group(0))
                        continue
                i += 1
            for nm in names:
                for m in re.finditer(r"\bthis\." + re.escape(nm) + r"\s*(?:\+\+|--|[-+*/]?=(?!=))", t):
                    add("VUE-P01", s + m.start(), f"(prop `{nm}`)")
        for pm in re.finditer(r"\bprops\s*:\s*\[([^\]]*)\]", t):
            for nm in re.findall(r"['\"]([\w$-]+)['\"]", pm.group(1)):
                for m in re.finditer(r"\bthis\." + re.escape(nm) + r"\s*(?:\+\+|--|[-+*/]?=(?!=))", t):
                    add("VUE-P01", s + m.start(), f"(prop `{nm}`)")
        for m in re.finditer(r"\bbeforeEach\s*\(", t):
            i = m.end() - 1
            depth = 0
            j = i
            while j < len(t):
                if t[j] == "(":
                    depth += 1
                elif t[j] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if not re.search(r"\bnext\s*\(", t[i:j + 1]):
                add("VUE-R01", s + m.start())
        for m in re.finditer(r"\$store\.state\.[\w.$]+\s*(?:\+\+|--|[-+*/]?=(?!=))", t):
            add("VUE-V01", s + m.start())
        if re.search(r"\$route\.params", t):
            m = re.search(r"\$route\.params", t)
            add("VUE-RT01", s + m.start())
        for m in re.finditer(r"\bnew\s+Vue\s*\(", t):
            add("VUE2-01", s + m.start())
        for m in re.finditer(r"\bVue\.component\s*\(", t):
            add("VUE2-02", s + m.start())
        for m in re.finditer(r"\bVue\.use\s*\(", t):
            add("VUE2-03", s + m.start())
        for m in re.finditer(r"\$root\.\$(?:on|emit)\s*\(", t):
            add("VUE2-06", s + m.start())
        if re.search(r"\bfilters\s*:\s*\{", t):
            m = re.search(r"\bfilters\s*:\s*\{", t)
            add("VUE2-04", s + m.start())
        # Composition API (<script setup>)
        if is_setup:
            refs = re.findall(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*ref\s*\(", t)
            for nm in refs:
                for lm in re.finditer(r"^.*$", t, re.M):
                    ln = lm.group(0)
                    if re.search(r"\b(?:const|let|var)\s+" + re.escape(nm) + r"\b", ln):
                        continue
                    if re.search(r"(?<![\w$.])" + re.escape(nm) + r"\s*(?:\+\+|--|[-+*/]=|=(?!=))", ln):
                        add("VUE3-01", s + lm.start(), f"(variable `{nm}`)")
            if not re.search(r"from\s+['\"]vue['\"]", t):
                for fn in ("ref", "onMounted"):
                    m = re.search(r"(?<![\w$.])" + fn + r"\s*\(", t)
                    if m:
                        add("VUE3-02", s + m.start(), f"(`{fn}`)")
                        break

    mrt = re.search(r"\$route\.params", text)
    if mrt and not re.search(r"beforeRouteUpdate", text):
        add("VUE-RT02", mrt.start())

    # ---- styles
    for attrs, s, e in parts["style"]:
        if not re.search(r"\bscoped\b", attrs):
            add("VUE-S01", s)

    F.sort(key=lambda f: (f["linha"], SEV[f["severidade"]], f["regra"]))
    # remove identical duplicates
    seen = set()
    out = []
    for f in F:
        k = (f["regra"], f["linha"], f["mensagem"])
        if k not in seen:
            seen.add(k)
            out.append(f)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--no-info", action="store_true")
    a = ap.parse_args()
    if a.rules:
        for k, (sev, org, cite, msg) in RULES.items():
            print(f"{k} [{sev}] {org} ({cite}): {msg}")
        return 0
    if not a.files:
        ap.print_help()
        return 2
    allf = {}
    worst = 0
    for fp in a.files:
        try:
            if fp == "-":
                text = sys.stdin.read()
            else:
                with open(fp, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
        except OSError as ex:
            print(f"Error reading {fp}: {ex}", file=sys.stderr)
            return 2
        is_sfc = fp.endswith(".vue") or bool(re.search(r"<template\b", text) and re.search(r"</template>", text))
        res = lint(text, is_sfc, a.no_info)
        allf[fp] = res
        if any(r["severidade"] == "error" for r in res):
            worst = 1
    if a.json:
        print(json.dumps(allf, ensure_ascii=False, indent=1))
    else:
        for fp, res in allf.items():
            print(f"== {fp}: {len(res)} finding(s)")
            for r in res:
                print(f"  L{r['linha']} [{r['severidade']}] {r['regra']} {r['origem']} ({r['citacao']}): {r['mensagem']}")
            if not res:
                print("  no findings (the rules cover only what the collection supports; this does not prove the component is correct).")
    return worst


if __name__ == "__main__":
    sys.exit(main())
