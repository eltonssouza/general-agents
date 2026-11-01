# -*- coding: utf-8 -*-
"""
nuxt_checklist.py - STATIC Nuxt project checklist, using only what NUXT (Nuxt v4 introduction, v4.5.2) says.
Never executes the project, Nuxt or npm; only reads local files (package.json, config file, folder existence).

Subcommands:
  scan FOLDER [--json]   checks structure and configuration (NUXT p.1-4) and summarizes the rendering mode
  questions              architecture review questions (rendering mode, deployment, modules) with page
  modes                  rendering modes and commands/options the text cites (only `nuxt generate`, `ssr: false`, `routeRules`)
Labels: [from source] = is in NUXT p.N; [inference]; [extrapolation] = file/folder name the text does NOT cite.
[DATED] the text is for v4.5.2 (footer 2016-2026). For other versions: NOT COVERED.
Exit code of scan: 1 if there is a "warn" finding; 0 otherwise; 2 invalid usage.
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

CONFIG_NAMES = ["nuxt.config.ts", "nuxt.config.js", "nuxt.config.mjs", "nuxt.config.mts"]
BUILDERS = ["@nuxt/vite-builder", "@nuxt/rspack-builder", "@nuxt/webpack-builder"]


def strip_comments(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$|(?<=[;,{}\s])//[^\n]*$", "", s)


def scan(root):
    R = []

    def add(sev, cod, org, cite, msg):
        R.append({"severidade": sev, "codigo": cod, "origem": org, "citacao": cite, "mensagem": msg})

    if not os.path.isdir(root):
        raise SystemExit("Folder does not exist: " + root)
    pkg = None
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        try:
            pkg = json.load(open(pj, "r", encoding="utf-8"))
        except Exception:
            add("warn", "N00", "[inference]", "-", "package.json unreadable (invalid JSON).")
    else:
        add("warn", "N00", "[inference]", "NUXT p.4", "package.json not found in the folder.")
    deps = {}
    scripts = {}
    if isinstance(pkg, dict):
        for k in ("dependencies", "devDependencies"):
            deps.update(pkg.get(k) or {})
        scripts = pkg.get("scripts") or {}
    if "nuxt" in deps:
        v = str(deps["nuxt"])
        add("ok", "N01", "[inference]", "NUXT p.4", f"Core package `nuxt` declared ({v}). The package is cited as 'Core engine' (p.4).")
        m = re.search(r"(\d+)\.", v)
        if m and m.group(1) != "4":
            add("warn", "N01b", "[from source]", "NUXT p.1", f"The collection covers Nuxt v4 (v4.5.2); the declared version is {v}: the rest of this check may not apply (NOT COVERED for other versions).")
        elif not m:
            add("info", "N01c", "[inference]", "NUXT p.1", f"Version `{v}` is not numeric; confirm it is v4 (the collection covers v4.5.2).")
    elif pkg is not None:
        add("warn", "N01", "[inference]", "NUXT p.4", "Dependency `nuxt` not found in package.json.")
    for b in BUILDERS:
        if b in deps:
            add("info", "N02", "[from source]", "NUXT p.4", f"Explicit bundler `{b}` (the text lists vite/rspack/webpack builders; the default is Vite, p.2).")

    cfg_path = None
    for n in CONFIG_NAMES:
        if os.path.isfile(os.path.join(root, n)):
            cfg_path = os.path.join(root, n)
            break
    cfg = ""
    if cfg_path:
        cfg = strip_comments(open(cfg_path, "r", encoding="utf-8", errors="replace").read())
        add("ok", "N03", "[from source]", "NUXT p.1", f"Configuration file present ({os.path.basename(cfg_path)}): the text says configuration customizes/overrides the defaults. [extrapolation] the file name does not appear in the text.")
    else:
        add("info", "N03", "[from source]", "NUXT p.1", "No configuration file: the text says there are conventional defaults; config only customizes (file name: [extrapolation]).")

    app_pages = os.path.isdir(os.path.join(root, "app", "pages"))
    root_pages = os.path.isdir(os.path.join(root, "pages"))
    if app_pages:
        add("ok", "N04", "[from source]", "NUXT p.1", "`app/pages/` exists: routes defined by the directory structure (file-based routing).")
    elif root_pages:
        add("info", "N04", "[from source]", "NUXT p.1", "`pages/` exists at the root, but the text (v4.5.2) cites `app/pages/`. If the project is another version: NOT COVERED.")
    else:
        add("info", "N04", "[from source]", "NUXT p.1", "No `app/pages/`: no file-based routing (acceptable if the app has a single page; the text does not define the minimum).")
    for d, cite, what in (("api", "NUXT p.3", "server API read from `server/api/`"), ("middleware", "NUXT p.3", "server middleware read from `server/middleware/`")):
        if os.path.isdir(os.path.join(root, "server", d)):
            add("ok", "N05", "[from source]", cite, f"`server/{d}/` exists: {what} by Nitro.")

    ssr_false = bool(re.search(r"\bssr\s*:\s*false\b", cfg))
    rr = bool(re.search(r"\brouteRules\b", cfg))
    gen = any("nuxt generate" in str(v) for v in scripts.values())
    if ssr_false:
        add("info", "N06", "[from source]", "NUXT p.3", "`ssr: false` in the config: SSR disabled globally (the default is SSR, p.1-2; the SSR benefits listed on p.2-3 are lost).")
    else:
        add("info", "N06", "[from source]", "NUXT p.1-2", "SSR active (built-in default, no server configuration).")
    if rr:
        add("info", "N07", "[from source]", "NUXT p.3", "`routeRules` present: hybrid rendering per route. Content of the rules: NOT COVERED.")
    if gen:
        add("info", "N08", "[from source]", "NUXT p.3", "Script with `nuxt generate`: static rendering of the whole application for static hosting.")
    if ssr_false and gen:
        add("warn", "N09", "[inference]", "NUXT p.3", "`ssr: false` together with `nuxt generate`: the text cites both options as alternatives to the default SSR but does not explain the combination; review the intent (NOT COVERED).")
    if re.search(r"\bmodules\s*:", cfg):
        add("info", "N10", "[from source]", "NUXT p.4", "Modules configured: the text describes the module system (extensions/integrations). [extrapolation] the name of the `modules` option does not appear in the text.")
    if os.path.isdir(os.path.join(root, ".output")):
        add("info", "N11", "[from source]", "NUXT p.3", "`.output` exists: Nitro universal production output (minified, no Node.js modules except polyfills).")
    if os.path.isfile(os.path.join(root, "tsconfig.json")):
        add("info", "N12", "[from source]", "NUXT p.2", "`tsconfig.json` present; the text says types and `tsconfig.json` are generated automatically (zero-config TypeScript).")
    return R


def cmd_questions():
    Q = [
        ("Which rendering mode does the project need: SSR (default), static (`nuxt generate`), no SSR (`ssr: false`) or hybrid (`routeRules`)?", "NUXT p.1-3"),
        ("Do the SSR benefits (initial load, SEO, low-end devices, accessibility, caching) matter for this product?", "NUXT p.2-3"),
        ("Where will it be deployed: Node/Deno, static hosting, serverless/edge?", "NUXT p.3"),
        ("Do the routes follow the `app/pages/` structure or are there manual routes? (the text only cites the convention)", "NUXT p.1-2"),
        ("Is there a server-side API/middleware of its own (`server/api/`, `server/middleware/`)?", "NUXT p.3"),
        ("Which third-party modules/integrations are needed? (the text only describes the module system)", "NUXT p.4"),
        ("Which bundler: Vite (default), rspack or webpack?", "NUXT p.2, 4"),
        ("Is the project version v4? (the collection only covers v4.5.2; other versions: NOT COVERED)", "NUXT p.1"),
    ]
    for i, (q, c) in enumerate(Q, 1):
        print(f"{i}. {q}  [{c}]")
    print("Beyond what the text answers (NOT COVERED): installation commands, full directory structure, data fetching, state, per-provider deployment.")


def cmd_modes():
    print("Rendering modes cited in NUXT p.3 [from source]:")
    print("- SSR by default, no server configuration (p.1-2).")
    print("- Static rendering of the whole application: `nuxt generate` (p.3).")
    print("- SSR disabled globally: option `ssr: false` (p.3).")
    print("- Hybrid rendering: option `routeRules` (p.3).")
    print("Deployment targets (p.3): Node or Deno server, pre-rendered on static hosting, serverless and edge.")
    print("Commands the text cites: only `nuxt generate`. Creating a project, running dev/build: NOT COVERED.")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd")
    s = sp.add_parser("scan")
    s.add_argument("root")
    s.add_argument("--json", action="store_true")
    sp.add_parser("questions")
    sp.add_parser("modes")
    a = ap.parse_args()
    if a.cmd == "scan":
        R = scan(a.root)
        if a.json:
            print(json.dumps(R, ensure_ascii=False, indent=1))
        else:
            for r in R:
                print(f"[{r['severidade']}] {r['codigo']} {r['origem']} ({r['citacao']}): {r['mensagem']}")
        return 1 if any(r["severidade"] == "warn" for r in R) else 0
    if a.cmd == "questions":
        cmd_questions()
        return 0
    if a.cmd == "modes":
        cmd_modes()
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
