# -*- coding: utf-8 -*-
"""
vue_compare.py - Options API vs Composition API comparator using ONLY what the collection texts say.
  VUE3G p.4-7 (Vue 3: Options and Composition, same counter examples) and VUEHB p.66-67, 88-95 (Vue 2: options only).
Never executes code; only reads a file/text. stdlib, no network, deterministic.

Subcommands:
  table                          table of equivalences that BOTH VUE3G examples show (p.5-6)
  map TERM                       equivalent of a construct (e.g. data, methods, mounted, this.count, ref); NOT COVERED if the text does not show it
  detect FILE|-                  identifies the code style (options | composition | mixed | Vue 2 instance) and lists constructs
                                 with no documented equivalent in the texts
  recommend --build-tools yes|no --complexity low|high --goal learn|production
                                 applies the VUE3G p.7 recommendation
[DATED] VUEHB = Vue 2 (Jul 2018); VUE3G = 2026 capture with no printed date.
Labels: [from source] is on the cited page; [inference] direct deduction; [extrapolation] outside the collection.
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

TABLE = [
    ("component declaration", "export default { ... } in <script>", "<script setup> with imports and top-level variables/functions", "VUE3G p.5-6"),
    ("reactive state", "data() { return { count: 0 } }", "const count = ref(0)", "VUE3G p.5-6"),
    ("read/change in the script", "this.count++", "count.value++", "VUE3G p.5-6"),
    ("function that changes the state", "methods: { increment() { ... } }", "function increment() { ... }", "VUE3G p.5-6"),
    ("hook on mount", "mounted() { ... }", "onMounted(() => { ... }) imported from 'vue'", "VUE3G p.5-6"),
    ("template", "<button @click=\"increment\">Count is: {{ count }}</button>", "the same template", "VUE3G p.5-6"),
]

MAP = {
    "data": 1, "this.count": 2, "count": 2, "ref": 1, "ref(": 1, "value": 2, ".value": 2, "methods": 3, "method": 3, "function": 3,
    "mounted": 4, "onmounted": 4, "export default": 0, "script setup": 0, "<script setup>": 0, "template": 5,
}
NOCOV = {
    "computed": "VUEHB p.91-94 (Options, Vue 2): computed is cached; the collection does NOT show the Composition API equivalent.",
    "watch": "VUEHB p.90-91 (Options, Vue 2): watch observes one property; the collection does NOT show the Composition API equivalent.",
    "props": "VUEHB p.95-99 (Options, Vue 2): props; the collection does NOT show props in Vue 3 (nor in the Composition API).",
    "emit": "VUEHB p.107-109 ($emit, Vue 2); the collection does NOT show event emission in Vue 3.",
    "$emit": "VUEHB p.107-109 ($emit, Vue 2); the collection does NOT show event emission in Vue 3.",
    "slot": "VUEHB p.102-104 (Vue 2); VUE3G does not cover slots.",
    "slots": "VUEHB p.102-104 (Vue 2); VUE3G does not cover slots.",
    "filters": "VUEHB p.104-106 (Vue 2); VUE3G does not mention filters; do not claim removal.",
    "filter": "VUEHB p.104-106 (Vue 2); VUE3G does not mention filters; do not claim removal.",
    "created": "the collection only shows the `mounted` hook (VUEHB p.109; VUE3G p.5); other hooks: NOT COVERED.",
    "beforemount": "the collection only shows the `mounted` hook; other hooks: NOT COVERED.",
    "reactive": "NOT COVERED: VUE3G only shows `ref` (p.1, 6).",
    "provide": "NOT COVERED.", "inject": "NOT COVERED.", "watcheffect": "NOT COVERED.",
}


def cmd_table():
    print("Equivalences shown in the VUE3G examples (p.5-6) [from source]:")
    for a, b, c, p in TABLE:
        print(f"- {a}: Options `{b}`  <->  Composition `{c}`  ({p})")
    print("Not shown in the texts (NOT COVERED for the Composition API): " + ", ".join(sorted({k for k in NOCOV if k.isalpha()})) + ".")
    print("Note: VUE3G p.6 says both styles are interfaces over the same system and that the Options API is implemented on top of the Composition API.")


def cmd_map(term):
    k = term.strip().lower()
    if k in MAP:
        a, b, c, p = TABLE[MAP[k]]
        print(f"[from source] ({p}) {a}: Options `{b}` <-> Composition `{c}`")
        return 0
    if k in NOCOV:
        print("NOT COVERED (equivalent): " + NOCOV[k])
        return 0
    print("NOT COVERED: the construct does not appear in the VUE3G examples and has no comparison in the collection. Any answer is [extrapolation].")
    return 0


def detect(text):
    sig = {
        "options": [r"export\s+default\s*\{", r"(?<![\w$.])data\s*\(", r"(?<![\w$.])methods\s*:", r"(?<![\w$.])mounted\s*\(", r"(?<![\w$.])computed\s*:", r"(?<![\w$.])watch\s*:", r"(?<![\w$.])props\s*:"],
        "composition": [r"<script\s+setup", r"(?<![\w$.])ref\s*\(", r"(?<![\w$.])onMounted\s*\(", r"(?<![\w$.])setup\s*\(", r"\bcreateApp\s*\("],
        "vue2_instancia": [r"\bnew\s+Vue\s*\(", r"\bVue\.component\s*\(", r"\bVue\.use\s*\(", r"\bfilters\s*:"],
    }
    found = {k: [p for p in v if re.search(p, text)] for k, v in sig.items()}
    return found


def cmd_detect(path):
    text = sys.stdin.read() if path == "-" else open(path, "r", encoding="utf-8", errors="replace").read()
    f = detect(text)
    has_o = bool(f["options"]) and any(re.search(p, text) for p in (r"export\s+default\s*\{",))
    has_c = bool(f["composition"])
    has_2 = bool(f["vue2_instancia"])
    if has_2 and not has_c:
        style = "Vue 2 instance/style from the handbook (VUEHB p.8, 63-65)"
    elif has_c and has_o and not re.search(r"<script\s+setup", text):
        style = "mixed (Options + setup())"
    elif has_c and re.search(r"<script\s+setup", text) and has_o:
        style = "mixed (<script setup> + export default with options)"
    elif has_c:
        style = "Composition API (VUE3G p.5-6)"
    elif has_o:
        style = "Options API (VUE3G p.5; VUEHB p.66-67)"
    else:
        style = "undetermined (no recognized construct)"
    print("Detected style: " + style + "  [inference from text patterns]")
    for k, v in f.items():
        if v:
            print(f"  {k} constructs: {len(v)} pattern(s)")
    nocov = []
    for name, rx in (("computed", r"(?<![\w$.])computed\s*:"), ("watch", r"(?<![\w$.])watch\s*:"), ("props", r"(?<![\w$.])props\s*:"),
                     ("$emit", r"\$emit\s*\("), ("filters", r"\bfilters\s*:|\{\{[^}|]*(?<!\|)\|(?!\|)[^}]*\}\}"), ("slot", r"<slot\b|\sslot\s*="),
                     ("created", r"(?<![\w$.])created\s*\(")):
        if re.search(rx, text):
            nocov.append(name)
    if nocov:
        print("Constructs present with NO documented equivalent in the texts for the Composition API: " + ", ".join(nocov))
        for n in nocov:
            print("  - " + n + ": " + NOCOV.get(n, NOCOV.get(n.lstrip("$"), "NOT COVERED.")))
    if has_2:
        print("Warning: the collection does not include the Vue 2 -> Vue 3 migration guide; compatibility = NOT COVERED (VUE3G p.1 mentions a Migration Guide outside the collection).")
    return 0


def cmd_recommend(a):
    bt = a.build_tools == "yes"
    low = a.complexity == "low"
    print("Applying VUE3G p.7 [from source]:")
    if a.goal == "learn":
        print("- Learning: the style that seems easier; core concepts are shared; you can switch later (VUE3G p.7).")
    if not bt or low:
        print("- Production: Options API if there are no build tools OR usage is low complexity (e.g. progressive enhancement) (VUE3G p.7).")
    if bt and not low:
        print("- Production: Composition API + Single-File Components for full applications (VUE3G p.7).")
    if bt and low:
        print("- Note [inference]: build tools + low complexity -> the text accepts Options (low complexity); SFC is recommended when there is a build (VUE3G p.3-4).")
    print("Limit: the recommendation comes from the introduction guide; team/legacy/TypeScript criteria: NOT COVERED.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("table")
    m = sp.add_parser("map")
    m.add_argument("term")
    d = sp.add_parser("detect")
    d.add_argument("file")
    r = sp.add_parser("recommend")
    r.add_argument("--build-tools", choices=["yes", "no"], required=True)
    r.add_argument("--complexity", choices=["low", "high"], required=True)
    r.add_argument("--goal", choices=["learn", "production"], default="production")
    a = ap.parse_args()
    if a.cmd == "table":
        cmd_table()
    elif a.cmd == "map":
        return cmd_map(a.term)
    elif a.cmd == "detect":
        try:
            return cmd_detect(a.file)
        except OSError as ex:
            print(f"Error reading: {ex}", file=sys.stderr)
            return 2
    elif a.cmd == "recommend":
        return cmd_recommend(a)
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
