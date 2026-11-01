# 10 - Nuxt v4 (NUXT, 6 pages; useful p.1-4) [DATED]

Source: the "Introduction" page of "Get Started with Nuxt v4" (nuxt.com). Version shown: **v4.5.2** (p.1); footer "2016-2026" (p.6). It is a **marketing/concepts overview**: it has no step-by-step installation, no CLI commands (except `nuxt generate`), no code examples and no complete directory structure. Any detail beyond that is `[extrapolation]` or NOT COVERED.

## What it is (p.1)
- [from source] (NUXT p.1) Free, open-source framework for **full-stack** applications and sites with Vue.js, typed, performant and "production-grade". You start by writing `.vue` files, with HMR in development and **SSR by default** in production. No vendor lock-in: you can deploy "anywhere, even on the edge".
- [from source] (NUXT p.1) Uses **conventions** and an opinionated directory structure; the configuration file can customize/override the defaults.

## Features cited (p.1-2)
- [from source] (NUXT p.1-2) **File-based routing:** routes defined by the structure of the `app/pages/` directory.
- [from source] (NUXT p.2) Automatic **code splitting**; **built-in SSR** without configuring a server; **auto-imports** (composables and components in their "respective directories" without importing, with tree-shaking); **data-fetching utilities** compatible with SSR and with distinct strategies; **zero-config TypeScript** (types and `tsconfig.json` generated); **Vite by default** (HMR and bundling).
- [extrapolation] The exact names of the composables/components directories and of the data-fetching functions do **not** appear on the page.

## SSR (p.2-3)
- [from source] (NUXT p.2) Benefits listed: faster initial load (HTML ready), better SEO, better performance on weak devices, better accessibility (content available on load; p.3), easier caching on the server (p.3).
- [from source] (NUXT p.3) Alternatives: render the whole application statically with **`nuxt generate`**; **disable SSR globally** with the `ssr: false` option; **hybrid rendering** with the `routeRules` option. Points to "Nuxt rendering modes" (not included).

## Server: Nitro (p.3)
- [from source] (NUXT p.3) The **Nitro** server engine enables full-stack capabilities. In development it uses Rollup and Node.js workers (context isolation) and generates the API by reading `server/api/` and server middleware in `server/middleware/`.
- [from source] (NUXT p.3) In production, Nitro bundles app and server into a universal **`.output`** directory (minified, no Node.js modules except polyfills), deployable on any system with JavaScript: Node.js, serverless, Workers, edge or static.
- [from source] (NUXT p.3) A Nuxt app can be deployed on a Node or Deno server, pre-rendered for static hosting or on serverless/edge providers. Points to the Deployment section (not included).

## Modularity and packages (p.4)
- [from source] (NUXT p.4) A **module** system to extend Nuxt (features and integrations with third-party services).
- [from source] (NUXT p.4) Core packages: `nuxt` (core), bundlers `@nuxt/vite-builder`, `@nuxt/rspack-builder`, `@nuxt/webpack-builder`, CLI `@nuxt/cli`, server `nitro`, development kit `@nuxt/kit`.

## Pages 5-6
Site footer (Community, Explore, Enterprise, newsletter, copyright). No technical content.

## NOT COVERED (do not invent)
Project creation command; full directory tree (`components/`, `composables/`, `layouts/`, `plugins/`, `public/` etc. are not named); `nuxt.config` beyond `ssr` and `routeRules`; `useFetch`/`useAsyncData`; Pinia/state; route middleware; specific modules; per-provider deploy configuration; Nuxt 2/3 -> 4 migration; Nuxt 4 vs Vue versions relationship (the page only says "with Vue.js").
