# 08. Svelte x SvelteKit x Astro comparator and NOT COVERED list

Generated from `scripts/framework_compare.py` (criteria the sources provide; each cell has a citation or NOT COVERED). **[DATED]** SVHB = 2019 book; SKGS and ASTRO = entry pages captured in 2026; different depths. "NOT COVERED" does not mean the framework lacks the feature.

| Criterion | Svelte (SVHB) | SvelteKit (SKGS) | Astro (ASTRO) |
|---|---|---|---|
| What it is | front-end framework, compiled ahead of time, "disappears" on deploy (p.2-3) | framework for web apps using Svelte; analogous to Next/Nuxt (p.1) | partial: only "Astro Docs" (p.1) |
| Component | `.svelte` with script/markup/style (p.8-11) | uses Svelte components (p.1) | partial: names "Astro components" and "template syntax" (p.2) |
| Local state | `let` + assignment, `$:` (p.14-19) | NOT COVERED | NOT COVERED |
| Shared state | props, context, stores (p.19-28) | NOT COVERED | NOT COVERED |
| Scoped CSS | yes (p.11) | NOT COVERED | NOT COVERED |
| Routing | partial: points to SvelteKit (p.49) | router (p.2; details NOT COVERED) | NOT COVERED |
| Rendering | partial: compiled (p.3) | configurable SSR, CSR, prerender (p.2) | partial: names islands (p.2) |
| Build/dev | Vite, `npm run dev`, 5173 (p.4-5) | Vite + Svelte plugin + HMR (p.2) | NOT COVERED |
| Create project | `npm create vite@latest ... --template svelte` (p.4) | partial: next page outside the capture (p.2) | `npm create astro@latest` (p.2) |
| Preload/offline/images | NOT COVERED | named (p.2) | NOT COVERED |
| Integrations | NOT COVERED | NOT COVERED | React and Partytown, named (p.2) |
| Data/content | `{#await}` (p.44-45) | NOT COVERED | partial: content collections, CMS (p.2-3) |
| TypeScript, testing, deploy, SEO | NOT COVERED | NOT COVERED | NOT COVERED (TypeScript: only "type safe content collections") |

Use `python -I scripts/framework_compare.py table|show CRITERION|compare A B|which TEXT|coverage|commands`.

## Relationships the collection establishes
- **[from source] (SKGS p.1-2)** SvelteKit **uses** Svelte and adds what is missing for a whole app.
- **[from source] (SVHB p.49; SVHB p.8)** the handbook points to SvelteKit as the next step and as the official app framework.
- **Svelte/SvelteKit x Astro:** no relationship in the collection (NOT COVERED). Whether Astro uses Svelte, whether it competes with SvelteKit, when to choose each: nothing in the sources.

## Choosing between them
**NOT COVERED.** No source gives a decision criterion. Only what the text says about each one exists (table above). Any further recommendation is `[extrapolation]` and only if the user asks, without stating a version ("Astro v7 does X" never).

## NOT COVERED (summary; full list in `svelte_lookup.py --gaps`)
Runes and Svelte 5; differences 3/4/5 and migration; file-based routing, `load`, actions, adapters, SvelteKit's create command; `.astro` syntax, hydration, use of integrations/collections/view transitions, content of the v7 upgrade; TypeScript; testing; transitions, `use:` actions, `{@html}`, `<svelte:head>`, `class:`; benchmarks; SEO/i18n; React/Next, Vue/Nuxt, Angular (other agents).
