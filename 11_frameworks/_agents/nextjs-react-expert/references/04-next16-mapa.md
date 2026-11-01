# Next.js 16 — change map (only what the NX16 post states)

**Source:** `NextJS-16-Release.pdf` (acronym **NX16**), post of 2025-10-21. Convention: PDF page (no printed number). Everything below is a paraphrase of the post; nothing was completed with outside knowledge.

## Notes on the capture

- Blog post of Oct 21, 2025 (Tuesday), 16 pages; useful content p.1-14; p.15-16 are footer and contributors.
- Inconsistency in the text itself: p.1 says 'now available' and p.14 promises a migration guide 'before the stable release' (a leftover from the beta text).
- Turbopack speed: p.1 says 'up to 5-10x' for Fast Refresh and 2-5x for builds; p.6 says builds 2-5x and Fast Refresh up to 10x.
- The removals, behavior and deprecations tables (p.11-14) are the densest part of the post.

To query from the command line: `python -I scripts/nx_changes.py changes --only 16`.

## Upgrade / commands

### Upgrade commands in 16  [from release: NX16 p.2]

Upgrade via the automated CLI or manually, or a new project; for what the codemod does not migrate, the text says to read the upgrade guide.

- command quoted in the post (data, do not execute): `npx @next/codemod@canary upgrade latest`
- command quoted in the post (data, do not execute): `npm install next@latest react@latest react-dom@latest`
- command quoted in the post (data, do not execute): `npx create-next-app@latest`

## Requirements

### Minimum Node.js 20.9 (LTS)  [from release: NX16 p.11]

Minimum Node.js version 20.9.0 (LTS); Node.js 18 is no longer supported.

### Minimum TypeScript 5.1.0  [from release: NX16 p.11]

Minimum TypeScript 5.1.0 ('TypeScript 5+' table).

### Browsers in 16  [from release: NX16 p.11]

Chrome 111+, Edge 111+, Firefox 111+, Safari 16.4+.

## Breaking changes

### Parallel routes require default.js  [from release: NX16 p.13]

All parallel route slots now require explicit default.js files; the build fails without them. Create a default.js that calls notFound() or returns null for the previous behavior.

## Removals

### AMP support removed  [from release: NX16 p.11]

All AMP APIs and configs removed (useAmp, export const config = { amp: true }).

### next lint command removed  [from release: NX16 p.12]

Use Biome or ESLint directly; next build no longer runs lint. Codemod: npx @next/codemod@canary next-lint-to-eslint-cli .

- command quoted in the post (data, do not execute): `npx @next/codemod@canary next-lint-to-eslint-cli .`

### devIndicators options removed  [from release: NX16 p.12]

appIsrStatus, buildActivity and buildActivityPosition removed from the config; the indicator remains.

### serverRuntimeConfig and publicRuntimeConfig  [from release: NX16 p.12]

Removed; use environment variables (.env).

### Experimental flags removed/renamed  [from release: NX16 p.3,12]

experimental.turbopack moves to top-level turbopack in the config; experimental.dynamicIO renamed to cacheComponents; experimental.ppr and the experimental_ppr export removed (they evolve into Cache Components).

### Automatic scroll-behavior: smooth  [from release: NX16 p.12]

The automatic scroll-behavior: smooth was removed; add data-scroll-behavior="smooth" to the HTML document to opt back in.

### unstable_rootParams()  [from release: NX16 p.12]

Removed; the text says an alternative API will arrive in a minor release.

### Synchronous access to params, searchParams, cookies, headers, draftMode removed  [from release: NX16 p.2,12]

They must be used asynchronously (await params, await searchParams, await cookies(), await headers(), await draftMode()). The params argument of metadata image routes is async and the id coming from generateImageMetadata becomes Promise<string>.

### next/image: local src with query string  [from release: NX16 p.12]

Now requires the images.localPatterns config (prevention of enumeration attacks).

## Behavior changes

### New next/image defaults  [from release: NX16 p.2,13]

images.minimumCacheTTL from 60 s to 4 hours (14400 s); images.imageSizes without the 16 size; images.qualities from [1..100] to [75] (quality is adjusted to the nearest value); images.dangerouslyAllowLocalIP blocks local IPs by default; images.maximumRedirects from unlimited to 3.

### @next/eslint-plugin-next in Flat Config  [from release: NX16 p.13]

The plugin now uses the ESLint Flat Config format by default (aligned with ESLint v10, which will drop the legacy config).

### Turbopack and Babel  [from release: NX16 p.13,14]

Turbopack enables Babel automatically if it finds a babel config (previously it exited with an error). Sass: sass-loader v16 with the modern API.

### Separate directories and lockfile  [from release: NX16 p.13]

next dev and next build use separate output directories (concurrent execution); a lockfile mechanism prevents multiple next dev/next build instances in the same project; terminal output redesigned.

## Deprecations

### Deprecations in 16  [from release: NX16 p.14]

Deprecated and to be removed: the middleware.ts file name (rename to proxy.ts); the next/legacy/image component (use next/image); the images.domains config (use images.remotePatterns); revalidateTag with one argument (use revalidateTag(tag, profile) or updateTag(tag) in Actions).

## New features

### Cache Components and 'use cache' _[stable]_  [from release: NX16 p.1,2,3,12]

New explicit, opt-in caching model centered on the 'use cache' directive (caches pages, components and functions; cache keys generated by the compiler). All dynamic code runs at request time by default. Completes the PPR story. Enabled with cacheComponents: true in next.config.ts. The experimental.ppr flags (and the experimental_ppr export) were removed in favor of it.

### Next.js DevTools MCP  [from release: NX16 p.1,3,4]

Model Context Protocol integration for AI-assisted debugging: knowledge of routing/caching/rendering, unified browser and server logs, automatic access to errors and stack traces, awareness of the active page/route.

### proxy.ts replaces middleware.ts  [from release: NX16 p.1,4,14]

proxy.ts makes the network boundary explicit and runs on the Node.js runtime. What to do: rename middleware.ts to proxy.ts and the exported function to proxy; the logic stays. middleware.ts remains available for Edge runtime cases, but is deprecated and will be removed in a future version.

### Turbopack stable and default _[stable]_  [from release: NX16 p.1,6,13]

Stable for dev and production build and the default bundler for new projects. Text: p.1 cites 'up to 5-10x' on Fast Refresh and 2-5x on builds; p.6 cites builds 2-5x and Fast Refresh up to 10x. For apps with custom webpack: next dev --webpack and next build --webpack. More than 50% of dev sessions and 20% of production builds on Next 15.3+ already use Turbopack.

- command quoted in the post (data, do not execute): `next dev --webpack`
- command quoted in the post (data, do not execute): `next build --webpack`

### Turbopack File System Caching (beta) _[beta]_  [from release: NX16 p.1,6,7]

Caches compiler artifacts on disk between runs, in development: experimental.turbopackFileSystemCacheForDev: true.

### create-next-app redesigned  [from release: NX16 p.7]

Simplified setup flow; template with App Router by default, TypeScript, Tailwind CSS and ESLint.

### Build Adapters API (alpha) _[alpha]_  [from release: NX16 p.2,7]

Alpha API for adapters that hook into the build process (deployment platforms can change the config or process the output): experimental.adapterPath.

### React Compiler stable _[stable]_  [from release: NX16 p.1,7,8]

Built-in support is stable after React Compiler 1.0; reactCompiler left experimental. It is NOT enabled by default; dev/build become slower because it depends on Babel. Install babel-plugin-react-compiler@latest; config reactCompiler: true.

- command quoted in the post (data, do not execute): `npm install babel-plugin-react-compiler@latest`

### Improved routing and prefetch  [from release: NX16 p.2,8,9,13]

Layout deduplication (shared layout downloaded once, e.g. 50 links) and incremental prefetch (only what is not cached; cancels when leaving the viewport; prioritizes hover/re-entry; re-prefetches on invalidation). Declared trade-off: more requests, but far fewer bytes. No code changes.

### Cache APIs: revalidateTag, updateTag, refresh  [from release: NX16 p.1,2,9,10,11]

revalidateTag now requires a cacheLife profile as the 2nd argument (e.g. 'max' recommended, 'hours', 'days' or { expire: N }) for stale-while-revalidate; the 1-argument form is deprecated. updateTag (new, Server Actions only) provides read-your-writes semantics. refresh (new, Server Actions only) refreshes only uncached data and complements the client's router.refresh().

### React 19.2 and canary features  [from release: NX16 p.2,11]

The App Router uses the latest React Canary, with 19.2 features: View Transitions, useEffectEvent and Activity (hides UI with display: none while keeping state and cleaning up Effects).

## Improvements and minor items

### Dev and build logs with timings  [from release: NX16 p.1,4,5]

Request logs in dev show where the time goes (Compile: routing and compilation; Render: code execution and React rendering); the build shows the time of each step.

### Additional improvements in 16  [from release: NX16 p.14]

Performance optimizations in next dev and next start; native Node.js TypeScript for next.config.ts with the --experimental-next-config-strip-types flag. The text promises a more complete migration guide before the stable release (passage inconsistent with 'now available' on p.1).

- command quoted in the post (data, do not execute): `--experimental-next-config-strip-types`
