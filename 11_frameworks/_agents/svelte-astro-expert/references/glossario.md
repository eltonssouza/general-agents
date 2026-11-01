# Glossary (only terms the sources use)

Each entry gives the source and page. Terms without a page here = do not appear in the sources.

- **Single file component:** `.svelte` file with `<script>`, markup and `<style>` (SVHB p.9).
- **Prop:** data passed from parent to child, one-way; the child declares it with `export let` (SVHB p.19-20).
- **`$:` (reactive block):** block re-run when variables referenced in it change (SVHB p.17).
- **Store:** shared-state object from `svelte/store`; types writable, readable, derived (SVHB p.23-28).
- **`$store`:** `$` prefix that reads the store reactively; `$` is reserved (SVHB p.25).
- **Context API:** `setContext`/`getContext` from `svelte`; key accessible only in the component and its descendants (SVHB p.22-23).
- **Slot:** composition point `<slot />`; can be named (SVHB p.28-30).
- **Binding (`bind:`):** two-way link between a variable and an element/prop (SVHB p.33-39).
- **Custom event:** dispatched with `createEventDispatcher` and `dispatch` (SVHB p.47-49).
- **Event modifier:** `|preventDefault`, `|stopPropagation`, `capture`, `once`, `self` (SVHB p.47).
- **Lifecycle:** `onMount`, `onDestroy`, `beforeUpdate`, `afterUpdate` (SVHB p.30-31).
- **`context="module"`:** `<script>` attribute where exports beyond the component are written (SVHB p.12-13).
- **Compiled beforehand:** the app is compiled; the framework is not served to the visitor (SVHB p.3).
- **SvelteKit:** framework for web apps that uses Svelte (SKGS p.1).
- **SSR / client-side rendering / prerendering:** SvelteKit's configurable rendering modes (SKGS p.2). Definitions beyond that: NOT COVERED (the page links to a glossary that was not captured).
- **HMR (Hot Module Replacement):** instant update in the browser via Vite and the Svelte plugin (SKGS p.2).
- **Vite:** tool used in the handbook template (SVHB p.4) and by SvelteKit (SKGS p.2).
- **Islands architecture, Astro components, template syntax, content collections, view transitions, integrations (React, Partytown):** only named on the landing page (ASTRO p.2-3); no definition: NOT COVERED.
- **Astro v7:** only the launch/upgrade banner (ASTRO p.1).
- **[DATED]:** relative to the source's date (SVHB Oct 22, 2019; SKGS and ASTRO captures of Aug 18, 2026).
- **NOT COVERED:** the sources do not say; do not infer.
