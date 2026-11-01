# Next.js 13 — change map (only what the NX13 post states)

**Source:** `NextJS-13-Release.pdf` (acronym **NX13**), post of 2022-10-25. Convention: PDF page (no printed number). Everything below is a paraphrase of the post; nothing was completed with outside knowledge.

## Notes on the capture

- Blog post of Oct 25, 2022 (Tuesday), 16 pages; useful content p.1-15; p.16 is only footer and contributors.
- In the extraction, the terminal block with the update command appears at the top of p.2, although the post introduces it on p.1.
- The text states: Next.js 13 and the pages directory are stable; app/ is in beta and not recommended in production (p.2).

To query from the command line: `python -I scripts/nx_changes.py changes --only 13`.

## Upgrade / commands

### Upgrade command  [from release: NX13 p.1,2,15]

Upgrade: npm i next@latest react@latest react-dom@latest eslint-config-next@latest. The text points to the upgrade guide for details.

- command quoted in the post (data, do not execute): `npm i next@latest react@latest react-dom@latest eslint-config-next@latest`

## Requirements

### Minimum React 18.2.0  [from release: NX13 p.14]

The minimum React version rises from 17.0.2 to 18.2.0.

### Minimum Node.js 14.6.0  [from release: NX13 p.14]

The minimum Node.js version rises from 12.22.0 to 14.6.0 (12.x reached end of life).

### Supported browsers  [from release: NX13 p.14,15]

Drops Internet Explorer and targets modern browsers: Chrome 64+, Edge 79+, Firefox 67+, Opera 51+, Safari 12+; Browserslist can still change the target.

## Breaking changes

### swcMinify becomes true  [from release: NX13 p.14]

The swcMinify configuration property changed from false to true.

### next/image rename  [from release: NX13 p.9,14]

The next/image import was renamed to next/legacy/image and next/future/image was renamed to next/image. There is a codemod: npx @next/codemod next-image-to-legacy-image ./pages.

- command quoted in the post (data, do not execute): `npx @next/codemod next-image-to-legacy-image ./pages`

### <a> child not allowed in next/link  [from release: NX13 p.14,11]

The child of next/link can no longer be an <a>; use the legacyBehavior prop for the old behavior or remove the <a>. There is a codemod.

### No prefetch for bots  [from release: NX13 p.14]

Routes are no longer prefetched when the User-Agent is a bot.

## Removals

### target option removed  [from release: NX13 p.14]

The obsolete target option of next.config.js was removed.

## New features

### app directory (beta) _[beta]_  [from release: NX13 p.1,2,3]

Introduces the app/ directory in beta: the text says it is NOT yet recommended for production; the pages/ directory remains stable and supported for the foreseeable future; adopting app/ can be incremental from pages/. Routes in app/ require a page.js file.

### Layouts  [from release: NX13 p.1,3,4,5]

Layouts share UI across routes and, on navigation, preserve state, stay interactive and do not re-render; they are defined by the file system (e.g. app/blog/layout.js). Code (components, tests, styles) can live next to the routes.

### React Server Components in app/  [from release: NX13 p.1,4]

app/ adopts the React Server Components architecture: server-first by default, less JavaScript sent to the client; the Next/React runtime is cacheable and does not grow with the application.

### Streaming and loading.js  [from release: NX13 p.4,5,7]

Progressive rendering with streaming of UI units; the special file loading.js creates an Instant Loading UI with Suspense boundaries. On Vercel, apps using app/ stream by default on the Node.js and Edge runtimes.

### Data fetching: async Server Components and extended fetch  [from release: NX13 p.2,5,6]

Server components can be async and use fetch; the native fetch is extended (automatic dedupe) and offers an API for caching/revalidation: cache 'force-cache' (the text says it is the default), 'no-store', and next: { revalidate: N }. The text compares this with getStaticProps / getServerSideProps. Data mutations would be simplified in a future version.

### Turbopack (alpha) _[alpha]_  [from release: NX13 p.1,7,8]

Successor to Webpack written in Rust, in alpha. It only supports next dev (the text says they are working on supporting next build); enabled with next dev --turbo. Figures from the text: 700x faster than Webpack on updates, 10x faster than Vite, 4x on cold start; a 3,000-module app starts in 1.8 s (Vite 11.4 s, Webpack 16.5 s). Many features are still unsupported.

- command quoted in the post (data, do not execute): `next dev --turbo`

### New next/image  [from release: NX13 p.1,8,9]

New image component: less client JS, simpler styling, alt required by default, native lazy loading without hydration. The old component was renamed to next/legacy/image.

### @next/font (beta) _[beta]_  [from release: NX13 p.1,10]

Font system with automatic self-hosting, no external requests (Google Fonts downloaded at build time) and zero layout shift via CSS size-adjust; imported from @next/font/google and @next/font/local.

### Simplified next/link  [from release: NX13 p.1,11]

<Link> always renders an <a>; nesting an <a> is no longer needed (experimental option since 12.2, now the default). Codemod: npx @next/codemod new-link ./pages.

- command quoted in the post (data, do not execute): `npx @next/codemod new-link ./pages`

### OG image generation (@vercel/og)  [from release: NX13 p.11,12]

The @vercel/og library for dynamic social cards (ImageResponse), based on Vercel Edge Functions and WebAssembly; the example uses the 'experimental-edge' runtime in pages/api/og.jsx.

### Middleware API updates _[experimental]_  [from release: NX13 p.13,14]

Middleware can set request/response headers and respond directly (e.g. NextResponse.json with 401) without a rewrite/redirect; responding from Middleware requires the experimental.allowMiddlewareResponseBody option in next.config.js.
