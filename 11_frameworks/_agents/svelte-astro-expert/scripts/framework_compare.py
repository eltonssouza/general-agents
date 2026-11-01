# -*- coding: utf-8 -*-
"""
framework_compare.py - Svelte x SvelteKit x Astro comparator ONLY with criteria that the 3 sources of the collection provide.
Each cell carries a citation (SVHB / SKGS / ASTRO p.N) or "NOT COVERED". Nothing is executed; stdlib, no network, deterministic.

Sources (page = PDF page):
  SVHB  The Svelte Handbook (Flavio Copes; header 22 Oct 2019; Svelte version not declared; 49 pages)
  SKGS  SvelteKit Docs, "Introduction" (captured 18 Aug 2026; 3 pages, useful 1-2)
  ASTRO Astro Docs, landing (banner "Astro v7 is here"; captured 18 Aug 2026; 3 pages)
[DATED] each column is relative to the date of its source; the columns are NOT from the same era nor the same depth
(SVHB is a book; SKGS and ASTRO are entry pages). "NOT COVERED" never means "the framework does not have it".

Subcommands:
  criteria                 list the criteria
  table                    summary table (status per criterion and framework)
  show CRITERION           detail of one criterion (id, part of the title or keyword; Portuguese ids/keywords still work)
  compare A B              two frameworks (svelte | sveltekit | astro), criterion by criterion
  coverage                 how many criteria each framework covers
  which TEXT               maps a need (keywords, Portuguese or English) to criteria and says what the sources answer
  commands                 creation commands the sources cite (only printed; never executed)
"""
import argparse
import re
import sys
import unicodedata

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

FW = ["svelte", "sveltekit", "astro"]
LAB = {"svelte": "Svelte (SVHB, 2019)", "sveltekit": "SvelteKit (SKGS, 2026)", "astro": "Astro (ASTRO, 2026)"}
N = None  # NOT COVERED

# criterion: (id, title, keywords, svelte, sveltekit, astro); cell = (status, text, citation) or None
# status "source" = stated in the source; "parcial" = only cited/named (internal value, kept for compatibility)
C = [
    ("definicao", "What it is", "definicao o que e what is concept definition",
     ("source", "front-end framework to build web applications; the app is compiled beforehand, the framework is not served to the visitor", "SVHB p.2-3"),
     ("source", "framework for robust, performant web applications using Svelte; analogous to Next (for those coming from React) and Nuxt (for those coming from Vue)", "SKGS p.1"),
     ("parcial", "the landing only presents itself as 'Astro Docs: guides, resources and references'; it does NOT define what Astro is", "ASTRO p.1")),
    ("componente", "Component model", "componente component file sfc format .svelte .astro template",
     ("source", ".svelte file (single file component) with <script>, markup and <style>", "SVHB p.8-11"),
     ("source", "uses Svelte components ('a way of writing UI components')", "SKGS p.1"),
     ("parcial", "only names 'Astro components' and 'Astro template syntax' as features; the file format is NOT described", "ASTRO p.2")),
    ("estado", "Local state and reactivity", "estado state reatividade reactivity reactive let $: assignment",
     ("source", "variable with let + assignment; arrays require reassignment; `$:` blocks", "SVHB p.14-19"), N, N),
    ("compartilhado", "State between components", "compartilhado props context stores store shared global state between components",
     ("source", "props (lifting state up), context API (setContext/getContext) and stores (writable/readable/derived)", "SVHB p.19-28"), N, N),
    ("estilo", "CSS styling and scope", "estilo style css scope scoped",
     ("source", "CSS in <style> is scoped to the component and does not leak", "SVHB p.11"), N, N),
    ("roteamento", "Routing", "roteamento routing router rota rotas route routes navegacao navigation pagina paginas page pages",
     ("parcial", "the handbook does not cover a router; at the end it points to SvelteKit for server-rendered apps", "SVHB p.49"),
     ("source", "includes a router that updates the UI when a link is clicked (details, such as file-based routes, NOT covered)", "SKGS p.2"),
     N),
    ("renderizacao", "Rendering modes (SSR, CSR, prerender)", "renderizacao rendering ssr csr prerender prerendering servidor server client-side estatico static hidratacao hydration islands",
     ("parcial", "ahead-of-time compilation to JavaScript; SSR is not covered", "SVHB p.3"),
     ("source", "configurable rendering: SSR on the server, client-side rendering in the browser or prerendering at build time, per part of the app", "SKGS p.2"),
     ("parcial", "only names 'Islands architecture' (unexplained); SSG/SSR/static do NOT appear", "ASTRO p.2")),
    ("build", "Build/dev tooling", "build vite hmr bundler ferramenta tool tooling dev servidor server",
     ("source", "project created by the Vite template; `npm run dev` starts the site in development on port 5173", "SVHB p.4-5"),
     ("source", "uses Vite with the Svelte plugin and Hot Module Replacement; build optimizations to load only the necessary code", "SKGS p.2"),
     N),
    ("criacao", "Create a project (cited command)", "criacao criar create novo new projeto project comando command scaffold instalar install npm",
     ("source", "`npm create vite@latest helloworld -- --template svelte`, then `npm install` and `npm run dev`", "SVHB p.4"),
     ("parcial", "the next page, 'Creating a project', is NOT in the capture (only the navigation link)", "SKGS p.2"),
     ("source", "`npm create astro@latest` (installation from an existing repository and manual installation also exist, only described in one line)", "ASTRO p.2")),
    ("otimizacoes", "Preload, offline and images", "otimizacoes optimizations preload preloading offline imagem imagens image images otimizacao optimization performance",
     N, ("source", "lists offline support, preloading of pages before navigation and image optimization (only named)", "SKGS p.2"), N),
    ("integracoes", "Integration with other libraries/frameworks", "integracao integracoes integration integrations react partytown plugin",
     N, N, ("source", "'add integrations like React and Partytown' (only named; how to install is NOT covered)", "ASTRO p.2")),
    ("conteudo", "Data/content", "conteudo content dados data collections cms fetch promise",
     ("source", "promises in the template with {#await} (example fetch)", "SVHB p.44-45"), N,
     ("parcial", "typed content collections (p.2) and headless CMS (p.3) only appear as items/links", "ASTRO p.2-3")),
    ("transicoes", "Navigation transitions", "view transitions transicoes transition navegacao navigation",
     N, N, ("parcial", "'view transitions' only as an item/link", "ASTRO p.3")),
    ("aprendizado", "Where to learn", "aprendizado aprender learn learning tutorial curso course comunidade community discord documentacao documentation docs",
     ("source", "the handbook itself; playground at svelte.dev/repl; official site and SvelteKit as next steps", "SVHB p.3,49"),
     ("source", "interactive Svelte tutorial and Discord chat", "SKGS p.1"),
     ("source", "Build a Blog tutorial, starter themes, Discord and video course (external promotion)", "ASTRO p.2-3")),
    ("versao", "Version/date declared in the source", "versao version data date 2019 2026 v7",
     ("parcial", "Svelte version NOT declared; header of 22 Oct 2019; pre-runes syntax [inference]", "SVHB p.1"),
     ("parcial", "version NOT declared; captured 18 Aug 2026 (PDF metadata)", "SKGS p.1"),
     ("parcial", "banner 'Astro v7 is here' with an upgrade link; the upgrade content is NOT in the capture", "ASTRO p.1")),
    ("desempenho", "Performance (numbers)", "desempenho performance fast rapido leve lightweight bundle size tamanho benchmark",
     ("parcial", "qualitative claims (less bandwidth, lighter); no numbers", "SVHB p.3"),
     ("parcial", "qualitative claims (fast dev, optimized build); no numbers", "SKGS p.2"), N),
    ("typescript", "TypeScript", "typescript ts tipos types", N, N, ("parcial", "only 'type safe content collections' as an item; TypeScript itself is NOT covered", "ASTRO p.2")),
    ("testes", "Tests", "teste testes test tests testing", N, N, N),
    ("deploy", "Deploy/hosting", "deploy hospedagem hosting producao production adapter", N, N, N),
    ("seo", "SEO / accessibility / i18n", "seo acessibilidade accessibility i18n", N, N, N),
]

IDX = {c[0]: c for c in C}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def cell(c, fw):
    v = c[3 + FW.index(fw)]
    if v is None:
        return "NOT COVERED"
    st, txt, cite = v
    tag = "[from source]" if st == "source" else "[partial]"
    return f"{tag} {txt} ({cite})"


def short(c, fw):
    v = c[3 + FW.index(fw)]
    if v is None:
        return "NOT COVERED"
    return ("ok " if v[0] == "source" else "partial ") + v[2]


def find(q):
    q = norm(q).strip()
    if q in IDX:
        return [IDX[q]]
    return [c for c in C if q in norm(c[0]) or q in norm(c[1]) or q in norm(c[2]).split()]


def cmd_criteria():
    for c in C:
        print(f"{c[0]:14} {c[1]}")


def cmd_table():
    print(f"{'criterion':34} | {'Svelte (SVHB)':24} | {'SvelteKit (SKGS)':22} | Astro (ASTRO)")
    for c in C:
        print(f"{c[1][:34]:34} | {short(c, 'svelte')[:24]:24} | {short(c, 'sveltekit')[:22]:22} | {short(c, 'astro')[:22]}")
    print("Legend: ok = [from source] on the page; partial = only cited/named; NOT COVERED = the source does not say.")
    print("[DATED] SVHB 2019 (book); SKGS/ASTRO captures of 18 Aug 2026 (entry pages). Columns of different depths.")


def cmd_show(q):
    hits = find(q)
    if not hits:
        print("NOT COVERED: criterion does not exist in the comparator (the sources do not give this criterion). Use `criteria`.")
        return 0
    for c in hits:
        print(f"== {c[1]} ({c[0]})")
        for fw in FW:
            print(f"  {LAB[fw]}: {cell(c, fw)}")
    return 0


def cmd_compare(a, b):
    for x in (a, b):
        if x not in FW:
            print("Valid frameworks: svelte | sveltekit | astro")
            return 2
    for c in C:
        print(f"- {c[1]}")
        print(f"    {LAB[a]}: {cell(c, a)}")
        print(f"    {LAB[b]}: {cell(c, b)}")
    print("Documented relationship: SvelteKit is built on Svelte (SKGS p.1-2). Astro and Svelte/SvelteKit: no relation in the sources (NOT COVERED).")
    return 0


def cmd_coverage():
    for fw in FW:
        ok = sum(1 for c in C if c[3 + FW.index(fw)] and c[3 + FW.index(fw)][0] == "source")
        par = sum(1 for c in C if c[3 + FW.index(fw)] and c[3 + FW.index(fw)][0] != "source")
        sem = sum(1 for c in C if c[3 + FW.index(fw)] is None)
        print(f"{LAB[fw]}: {ok} covered, {par} partial, {sem} NOT COVERED (of {len(C)})")
    print("Criteria not covered in ANY framework:", ", ".join(c[0] for c in C if all(c[3 + i] is None for i in range(3))))


def cmd_which(text):
    q = norm(text)
    toks = set(re.findall(r"[a-z0-9$:@._-]+", q))
    hits = []
    for c in C:
        kws = set(norm(c[2]).split())
        if toks & kws:
            hits.append(c)
    if not hits:
        print("NOT COVERED: no criterion of the sources matches this need.")
    for c in hits:
        print(f"== {c[1]}")
        for fw in FW:
            print(f"  {LAB[fw]}: {cell(c, fw)}")
    if re.search(r"\b(qual|escolh|melhor|vs|ou|decidir|recomend|which|choos|best|decid|recommend|or\b)", q):
        print("DECISION: the sources do NOT give a criterion for choosing between Svelte, SvelteKit and Astro (NOT COVERED).")
        print("What they say: 'you need more than Svelte to write a whole app' and SvelteKit covers that (SKGS p.2); "
              "Astro only appears as a docs landing (ASTRO p.1-3). Any recommendation beyond that would be [extrapolation].")
    return 0


def cmd_commands():
    print("Commands cited by the sources (are NOT executed by this script; collection data):")
    print("  SVHB p.4: npm create vite@latest helloworld -- --template svelte")
    print("  SVHB p.4: cd helloworld ; npm install ; npm run dev   (site em localhost:5173)")
    print("  ASTRO p.2: npm create astro@latest")
    print("  SKGS: no command in the capture (the 'Creating a project' page was not captured) -> NOT COVERED")
    print("[DATED] SVHB: the text cites commands from an era other than the capture; check the current documentation before using them.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("criteria")
    sub.add_parser("table")
    p = sub.add_parser("show")
    p.add_argument("q")
    p = sub.add_parser("compare")
    p.add_argument("a")
    p.add_argument("b")
    sub.add_parser("coverage")
    p = sub.add_parser("which")
    p.add_argument("text", nargs="+")
    sub.add_parser("commands")
    a = ap.parse_args()
    if a.cmd == "criteria":
        cmd_criteria()
    elif a.cmd == "table":
        cmd_table()
    elif a.cmd == "show":
        return cmd_show(a.q)
    elif a.cmd == "compare":
        return cmd_compare(a.a.lower(), a.b.lower())
    elif a.cmd == "coverage":
        cmd_coverage()
    elif a.cmd == "which":
        return cmd_which(" ".join(a.text))
    elif a.cmd == "commands":
        cmd_commands()
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
