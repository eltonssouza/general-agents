# 06. SvelteKit: introduction page (SKGS p.1-2)

Source: the *Introduction* page of the SvelteKit documentation, captured from the browser. **It only introduces**: there are no commands, code, configuration or examples. [DATED] capture of Aug 18, 2026 (PDF metadata); the page states neither version nor date. The "Svelte Summit Nov 18-19" banner carries no year.

## What the text says
- **[from source] (SKGS p.1)** SvelteKit is a framework for developing robust, performant web applications **using Svelte**. For those coming from React, "it is similar to Next"; for those coming from Vue, "it is similar to Nuxt". There is a page about project types (link only).
- **[from source] (SKGS p.1)** before starting: an interactive tutorial for those new to Svelte/SvelteKit and a Discord chat for help.
- **[from source] (SKGS p.1-2)** Svelte is a way of writing **UI components** (navigation bar, comments section, contact form); the **compiler converts the components into JavaScript** that renders the page's HTML and into CSS for styling. You do not need to know Svelte to follow the guide, but it helps. (The text extraction of the p.1-2 passage loses parts tied to links; the reading was checked against the page images.)
- **[from source] (SKGS p.2)** **SvelteKit vs Svelte:** Svelte renders components; you can compose a whole page with Svelte alone, but a complete app needs more. SvelteKit offers solutions to common challenges following "modern best practices". The list of named features: a **router** that updates the UI when a link is clicked; **build optimizations** to load only the necessary code; **offline support**; **preloading** of pages before navigation; **configurable rendering** to handle parts of the app on the server (SSR), in the browser (client-side rendering) or at build time (**prerendering**); **image optimization**.
- **[from source] (SKGS p.2)** development experience: reflects changes in the browser instantly using **Vite** with the **Svelte plugin** for **Hot Module Replacement (HMR)**.
- **[from source] (SKGS p.2)** navigation: the next page is "Creating a project" (**not** in the capture; only the footer link).
- SKGS p.3: no technical content (banner and footer).

## What the text does NOT say (NOT COVERED)
How to create a SvelteKit project (command); file-based routing (`+page.svelte`, `+layout`); `load`, form actions, hooks, endpoints; adapters/deploy; how to configure SSR/CSR/prerender; folder structure; current version; relationship with Svelte 5/runes; TypeScript; testing. The agent answers "NOT COVERED" and, if the user insists, `[extrapolation]` without stating a version.

## Use in the agent
For "what is SvelteKit and when does it come in", answer with these paragraphs and cite SKGS p.1-2. For the comparison with plain Svelte and Astro, see `08-comparador-e-sem-cobertura.md`.
