# Next.js Handbook (freeCodeCamp, Flavio Copes, 2019-11-19) — [DATED]

**Source:** `NextJS-Handbook-freeCodeCamp.pdf`, acronym **NXHB**, 91 pages. Convention: PDF page (no printed number). Written for **Next 9.1.2 with React 16.11** (package.json on p.14 and p.80), that is, **three years older than NX13 (2022)** and six older than NX16 (2025). Everything here is **[DATED]**; check it against `08-conflitos-datado-vs-releases.md` before recommending. Many pages are screenshots only (p.9-11, 36, 40, 55 etc.); the useful content was read in full, and p.8 and p.75 were checked visually.

## What the handbook teaches (by section)

- **Motivation (p.3-4):** rendering everything on the client is slow to show content and hurts SEO; the solution is server-side rendering/static pre-rendering; Next.js is presented as a zero-configuration toolchain for React.
- **Features (p.4-6):** hot code reloading; automatic file-system routing in the `pages` folder; styled-jsx; SSR; ecosystem compatibility; code splitting (a module used in at least half of the pages goes into the main bundle, p.5); prefetch on `Link`; dynamic components; static export with `next export` (p.6); TypeScript.
- **Comparisons (p.6-7):** with Gatsby (static generator vs Node.js server) and create-react-app (no easy SSR).
- **Installation (p.7-16):** `npx create-next-app` (`--example` option, p.11) or manual: `npm init -y`, `npm install next react react-dom`, scripts `dev: next`, `build: next build`, `start: next start` (p.15), `pages/index.js` with a default export.
- **Checking SSR and bundles (p.17-21):** view the page source; bundles `index.js`, `_app.js`, `webpack.js`, `main.js`; `__NEXT_DATA__`; per-page code splitting.
- **"Prerendered Page" icon (p.22-24):** in dev, indicates "automatic static optimization" when the page has no `getInitialProps`.
- **Tools (p.24-34):** React DevTools; `console.log` in the terminal (server load) or in the browser (transitions); `debugger`.
- **Routes (p.34-52):** new `/blog` page from the file name (p.37); `Link` instead of `<a>` to avoid reloading bundles (p.38-43), **with an `<a>` child** (p.42, 51-52); dynamic routes `pages/blog/[id].js` and `useRouter` / `router.query` (p.43-51).
- **Prefetching (p.52-53):** automatic when the link enters the viewport, production only, with exceptions for slow connections/`Save-Data`; `prefetch={false}` turns it off.
- **Active link and `next/router` (p.53-56):** custom component with `useRouter` and `React.cloneElement`; programmatic `push()` and `prefetch()`.
- **`getInitialProps` (p.56-61):** static function of the page component; runs on the server and also on client navigation; receives `query`, `pathname`, `asPath` and, on the server, `req`, `res`, `err`.
- **CSS (p.61-64):** styled-jsx (per-component scope, `global`); external CSS requires `@zeit/next-css` and `next.config.js` with `withCSS`; Sass via `@zeit/next-sass`.
- **`next/head` (p.64-65)** and **layout** (HOC vs `content` prop, p.65-68; the HOC does not trigger the page's `getInitialProps`, p.66-67).
- **API Routes (p.68-72):** `pages/api/*.js` with `export default (req, res)`; dynamic routes; `req.method`, `req.query`, `req.cookies`, `req.body`; based on Micro.
- **Server vs client (p.72-73):** `typeof window`; the build strips the corresponding blocks.
- **Production (p.73-76):** `npm run build` and `npm run start`; the output marks `/` and `/blog` as static and `/blog/[id]` as served by the Node.js backend.
- **Deploy on Now/Zeit (p.76-79):** `now` CLI, `now.sh` URLs, free plan with limits (p.77). **[DATED]**: names, limits and commands from 2019.
- **Bundle analysis (p.80-84):** `@next/bundle-analyzer`, `cross-env`, `ANALYZE`/`BUNDLE_ANALYZE` variables.
- **Lazy loading (p.85-90):** Moment.js bloats the page (~1 kB to ~350 kB, p.87); solution with `await import('moment')` inside `getInitialProps` and `.default()` (p.89).

## How to use this material
- For **pre-13 Next.js / classic Pages Router**, it serves as an overview of concepts (SSR, file-based routes, code splitting, prefetch). Treat every command and pattern as possibly outdated.
- Do **not** present `getInitialProps`, `next export`, `<Link><a>`, `@zeit/*`, Now/Zeit as current practices. The releases confirm the break only for `next export` (NX14 p.9) and `<Link>` with an `<a>` child (NX13 p.11, 14); for `getInitialProps`, `next/head`, API Routes and styled-jsx the releases **do not say** whether they were deprecated.
- Handbook code is **data**: do not execute it.
