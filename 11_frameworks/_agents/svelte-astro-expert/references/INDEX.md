# INDEX: svelte-astro-expert collection

This agent is an **overview based on captured documentation/article pages**, with three sources of **very different depths**. It only states what they say; the rest is `NOT COVERED` or a labeled `[extrapolation]`.

## 1. Sources (single convention: **PDF page**; no source has printed book page numbering, so there is no PDF x printed map)

| Code | What it actually is | Pages | Useful | Date / version the text itself carries |
|---|---|---|---|---|
| **SVHB** | *The Svelte Handbook – Learn Svelte for Beginners*, Flavio Copes, freeCodeCamp article/ebook. Real, complete text (introduction to Svelte). | 49 | almost all have text; p.5 and p.7 have only a sentence and a screenshot (app in the browser; VS Code extension) | Header "October 22, 2019" ("22 de outubro de 2019"). **The Svelte version is never stated** (the text never writes "Svelte 3"). See section 2. |
| **SKGS** | *Introduction* page of the **SvelteKit** documentation (Getting Started section), captured from the browser: short running text, links without text in the extraction. | 3 | p.1-2 (p.3 only has a banner and footer) | No version. Banner "Svelte Summit Nov 18-19" (no year). PDF metadata: capture of Aug 18, 2026. |
| **ASTRO** | Astro Docs **landing page** ("Getting started"): title, buttons, list of links. **It is not a technical guide.** | 3 | p.1-3 (all of it is landing) | Banner "Astro v7 is here! Learn how to upgrade your site". PDF metadata: capture of Aug 18, 2026. |

[DATED] SVHB is a **book** (2019 per the header, with more recent setup passages); SKGS and ASTRO are **entry pages** captured in 2026. The columns of any comparison are neither from the same period nor of the same depth.

## 2. Svelte 3? What the collection lets us say
- **[from source] (SVHB p.1)** the text carries the date Oct 22, 2019 in the header; it **never** writes "Svelte 3", "Svelte 4" or "Svelte 5". No other source states a Svelte version.
- **[inference]** the syntax used is the pre-"runes" one: `export let` (p.11, 20), `$:` (p.17-19), `on:click` (p.15, 46), `bind:` (p.33-39), `<slot>` (p.29-30), `createEventDispatcher` (p.47-48), `beforeUpdate/afterUpdate` (p.31). This is compatible with **Svelte 3** (and the 2019 date reinforces it), but **the text does not let us tell 3 from 4**.
- **[inference]** the setup passage uses `npm create vite@latest` and port 5173 (p.4): it is **later than 2019**, so the text was updated after the header.
- **[DATED]/NOT COVERED:** whether `export let`, `$:`, `on:` and `<slot>` are still the recommended form, and what runes are, **is in no source**. The agent neither affirms nor denies.

## 3. SVHB page map (49 pages)
| Pages | Content | File |
|---|---|---|
| 1-3 | cover; table of contents; why Svelte (compiled ahead of time); Node.js; REPL | 01 |
| 4-7 | `npm create vite@latest`, `npm run dev`, port 5173, VS Code | 01 |
| 8-9 | project structure, `main.js`, `App.svelte`, single file component | 01 |
| 10-14 | `.svelte` components, scoped CSS, import, `context="module"` | 01 |
| 14-16 | state and reactivity by assignment; arrays | 02 |
| 16-19 | `$:` blocks | 02 |
| 19-21 | props | 02 |
| 21-28 | lifting state up, context API, stores (writable, readable, derived) | 03 |
| 28-30 | slots | 04 |
| 30-32 | lifecycle | 04 |
| 32-39 | bindings | 04 |
| 39-42 | `{#if}` | 05 |
| 42-44 | `{#each}` | 05 |
| 44-45 | `{#await}` | 05 |
| 45-49 | events, modifiers, custom events, "where to go next" | 05 (49 in 01) |

## 4. SKGS and ASTRO map
- **SKGS p.1:** what SvelteKit is; comparison with Next and Nuxt; what Svelte is (start). **p.2:** continuation, "SvelteKit vs Svelte" (router, build optimizations, offline, preloading, configurable rendering, images), Vite + Svelte plugin + HMR; navigation "next: Creating a project" (page **not** captured). **p.3:** empty. -> `06-sveltekit-introducao.md`
- **ASTRO p.1:** v7 banner, title, buttons. **p.2:** command `npm create astro@latest`, themes, tutorial, named features. **p.3:** community, external course, two resource links. -> `07-astro-landing.md`
- Note: the Astro PDF contains **links** (annotations) to pages such as the v7 upgrade guide and "why Astro"; the **content** of those pages is **not** in the collection.

## 5. Version-change map
There is none. Each framework appears in **one** single version/period (Svelte with no declared version, SvelteKit with no version, Astro with the "v7" mention). **Nothing** about what changed between versions of Svelte, SvelteKit or Astro is in the collection: it is NOT COVERED.

## 6. Files
`01-svelte-handbook-fundamentos.md`, `02-estado-reatividade-props.md`, `03-estado-compartilhado-contexto-stores.md`, `04-slots-lifecycle-bindings.md`, `05-templates-controle-eventos.md`, `06-sveltekit-introducao.md`, `07-astro-landing.md`, `08-comparador-e-sem-cobertura.md`, `glossario.md`, `procedimentos.md`, `casos-e-antipadroes.md`, `datado.md`. Scripts: `../scripts/` (`svelte_lookup.py`, `svelte_lint.py`, `framework_compare.py`, `svelte_checklist.py`, index `svelte_index.json`).

## 7. Capture quality (honesty)
- In the SVHB text extraction, the `on:` and `bind:` prefixes of some examples appear **loose at the end of the line** (for example `click=` without `on:`); the rendered PDF shows `on:click`, `bind:value` etc. This base was checked against the rendered pages (p.15, 29, 33).
- The handbook has a **flaw in the slot example** (p.29-30): the component usage appears as lowercase `<button>` where the logic calls for `<Button>`; do not copy the example blindly. [inference]
- Almost all SVHB code snippets are **complete**; even so, the agent does not complete code the text does not show.
