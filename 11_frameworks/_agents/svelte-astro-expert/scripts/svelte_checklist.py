# -*- coding: utf-8 -*-
"""
svelte_checklist.py - review checklist for Svelte projects/components (SVHB), with SvelteKit (SKGS) and Astro (ASTRO) notes.
Static: only reads local files; nothing is executed; no network; stdlib; deterministic.

Subcommands:
  list [svelte|sveltekit|astro]   checklist items, each with a citation (SIGLA p.N) and origin
  scan FOLDER [--json]            scans the folder (ignores node_modules/.git/dist/build/.svelte-kit): package.json,
                                  .svelte/.astro files, SvelteKit conventions, the Vite template structure of SVHB p.8,
                                  and a svelte_lint.py summary per rule
Sources: SVHB (handbook, header 22 Oct 2019), SKGS (SvelteKit intro, captured 18 Aug 2026), ASTRO (landing, captured 18 Aug 2026).
[DATED] what the scan says about versions is only what is declared in the user's package.json; the collection does NOT teach how to interpret versions
(NOT COVERED). The collection does not cover SvelteKit file-based routing or .astro files: the scan only counts them.
Exit code: 0 normal; 1 if the lint summary has any `error`; 2 invalid usage.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import svelte_lint  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SKIP = {"node_modules", ".git", "dist", "build", ".svelte-kit", ".astro", "__pycache__"}

ITEMS = [
    ("svelte", "CK01", "[from source]", "SVHB p.3", "Node.js installed (all the handbook tooling is Node-based)."),
    ("svelte", "CK02", "[from source]", "SVHB p.4", "Project created with the Svelte Vite template (handbook command) and served with `npm run dev` (port 5173 in the text)."),
    ("svelte", "CK03", "[from source]", "SVHB p.6-7", "Editor with the Svelte for VS Code extension (syntax highlighting and other features)."),
    ("svelte", "CK04", "[from source]", "SVHB p.8-9", "Each component in .svelte with script / markup / style sections (single file component)."),
    ("svelte", "CK05", "[from source]", "SVHB p.15-16", "State changed? There is an assignment: arrays changed by push/pop/shift/splice require reassignment or spread."),
    ("svelte", "CK06", "[from source]", "SVHB p.33", "Variables bound with `bind:value` are `let`/`var`, never `const`."),
    ("svelte", "CK07", "[from source]", "SVHB p.43", "Dynamically changing lists have a key in `{#each}` (item id)."),
    ("svelte", "CK08", "[from source]", "SVHB p.31-32", "Timers/intervals created in the component are cleared in onDestroy or in the function returned by onMount."),
    ("svelte", "CK09", "[from source]", "SVHB p.19-20", "Parent data arrives through `export let` (props, one-way); for two-way, `bind:` on the prop (p.38-39)."),
    ("svelte", "CK10", "[from source]", "SVHB p.23-26", "Stores: imported from 'svelte/store'; `$name` only for stores; readable does not receive set/update."),
    ("svelte", "CK11", "[from source]", "SVHB p.28-30", "Several slots in the same component have names; only one unnamed slot (the default)."),
    ("svelte", "CK12", "[from source]", "SVHB p.44-45", "`{#await}` has `{:catch}` when the promise can fail."),
    ("svelte", "CK13", "[from source]", "SVHB p.47", "Form events use modifiers (`|preventDefault`) when needed."),
    ("svelte", "CK14", "[from source]", "SVHB p.47-48", "Custom events via `createEventDispatcher` imported from 'svelte'."),
    ("sveltekit", "CK15", "[from source]", "SKGS p.2", "Decide how each part of the app is rendered: SSR, client-side or prerendering (the page only says it is configurable; HOW to configure is NOT COVERED)."),
    ("sveltekit", "CK16", "[from source]", "SKGS p.1", "If coming from React/Vue, the text compares SvelteKit to Next/Nuxt; file-based routing, load and actions: NOT COVERED."),
    ("astro", "CK17", "[from source]", "ASTRO p.2", "Installation documented as `npm create astro@latest` (also from an existing repository or manually; steps are NOT in the capture)."),
    ("astro", "CK18", "[from source]", "ASTRO p.1", "There is an upgrade guide for Astro v7 (only the banner/link); upgrade review: NOT COVERED."),
]


def cmd_list(which):
    for g, cid, org, cite, txt in ITEMS:
        if which and g != which:
            continue
        print(f"[ ] {cid} ({g}) {org} ({cite}) {txt}")
    if not which or which == "astro":
        print("NOT COVERED: checklist for .astro components, islands, content collections (the collection only names these items: ASTRO p.2).")


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP)
        for f in sorted(files):
            yield os.path.join(d, f)


def cmd_scan(root, as_json):
    if not os.path.isdir(root):
        print(f"Folder does not exist: {root}", file=sys.stderr)
        return 2
    rep = {"pasta": root, "package_json": None, "svelte_files": [], "astro_files": [], "convencoes_sveltekit": [],
           "estrutura_template_vite": {}, "lint": {}, "notas": []}
    rels = []
    for fp in walk(root):
        rel = os.path.relpath(fp, root).replace("\\", "/")
        rels.append(rel)
        base = os.path.basename(fp)
        if base == "package.json" and rep["package_json"] is None and "/" not in rel:
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                    pj = json.load(fh)
                deps = {}
                for k in ("dependencies", "devDependencies"):
                    deps.update(pj.get(k, {}))
                rep["package_json"] = {k: deps[k] for k in ("svelte", "@sveltejs/kit", "astro", "vite", "@sveltejs/vite-plugin-svelte") if k in deps}
            except (OSError, ValueError):
                rep["package_json"] = {"erro": "package.json unreadable"}
        if fp.endswith(".svelte"):
            rep["svelte_files"].append(rel)
            if base.startswith("+"):
                rep["convencoes_sveltekit"].append(rel)
        if fp.endswith(".astro"):
            rep["astro_files"].append(rel)
    s = set(rels)
    rep["estrutura_template_vite"] = {
        "src/main.js": "src/main.js" in s or "src/main.ts" in s,
        "src/App.svelte": "src/App.svelte" in s,
        "src/lib/Counter.svelte": "src/lib/Counter.svelte" in s,
    }
    counts, errs = {}, 0
    for rel in rep["svelte_files"]:
        with open(os.path.join(root, rel), "r", encoding="utf-8", errors="replace") as fh:
            res = svelte_lint.lint(fh.read(), rel)
        for r in res:
            counts[r["regra"]] = counts.get(r["regra"], 0) + 1
            if r["severidade"] == "error":
                errs += 1
    rep["lint"] = dict(sorted(counts.items()))
    pj = rep["package_json"]
    if pj is None:
        rep["notas"].append("No package.json at the folder root: project type not identified.")
    elif "astro" in pj:
        rep["notas"].append("Astro project (`astro` dependency): the collection only has the Astro landing (ASTRO p.1-3); review of .astro code: NOT COVERED.")
    if pj and "@sveltejs/kit" in pj:
        rep["notas"].append("SvelteKit project (`@sveltejs/kit` dependency): SKGS p.1-2 only introduces; file-based routing, load, actions, adapters: NOT COVERED.")
    if pj and "svelte" in pj:
        rep["notas"].append(f"Svelte version declared by the user: {pj['svelte']}. The SVHB does not declare a version (pre-runes syntax, [inference]); how to interpret versions: NOT COVERED [DATED].")
    if rep["convencoes_sveltekit"]:
        rep["notas"].append(f"{len(rep['convencoes_sveltekit'])} +*.svelte file(s) (SvelteKit convention): content and routing NOT COVERED.")
    if as_json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        print(f"Folder: {root}")
        print(f"package.json (relevant deps): {rep['package_json']}")
        print(f".svelte: {len(rep['svelte_files'])}; .astro: {len(rep['astro_files'])}; +*.svelte conventions: {len(rep['convencoes_sveltekit'])}")
        print("Vite template structure of SVHB p.8 (informative):", rep["estrutura_template_vite"])
        print("Lint summary per rule (use svelte_lint.py for details):", rep["lint"] or "no findings")
        for n in rep["notas"]:
            print("NOTE:", n)
        print("Manual items: run `svelte_checklist.py list`.")
    return 1 if errs else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("list")
    p.add_argument("which", nargs="?", choices=["svelte", "sveltekit", "astro"])
    p = sub.add_parser("scan")
    p.add_argument("pasta")
    p.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.cmd == "list":
        cmd_list(a.which)
        return 0
    if a.cmd == "scan":
        return cmd_scan(a.pasta, a.json)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
