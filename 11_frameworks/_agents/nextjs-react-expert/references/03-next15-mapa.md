# Next.js 15 — change map (only what the NX15 post states)

**Source:** `NextJS-15-Release.pdf` (acronym **NX15**), post of 2024-10-21. Convention: PDF page (no printed number). Everything below is a paraphrase of the post; nothing was completed with outside knowledge.

## Notes on the capture

- Blog post of Oct 21, 2024 (Monday), 22 pages; useful content p.1-19; p.20-22 are contributors and footer.
- The post calls the release stable, based on RC1 and RC2, and says React 19 is still in RC (p.1, 5-6).
- The summary (p.2) says fetch is no longer cached by default, but the detail (p.4-5) covers GET Route Handlers and the Client Router Cache; force-dynamic/no-store appears on p.17.

To query from the command line: `python -I scripts/nx_changes.py changes --only 15`.

## Upgrade / commands

### @next/codemod CLI for upgrading  [from release: NX15 p.1,2,3]

A CLI that updates dependencies, shows the available codemods and guides their application. The canary tag uses the latest codemod version and latest sets the Next.js version; the text recommends the canary codemod even when migrating to the latest Next. Manual alternative: npm install next@latest react@rc react-dom@rc.

- command quoted in the post (data, do not execute): `npx @next/codemod@canary upgrade latest`
- command quoted in the post (data, do not execute): `npm install next@latest react@rc react-dom@rc`

## Requirements

### Minimum Node.js 18.18.0  [from release: NX15 p.17]

The minimum Node.js version is updated to 18.18.0.

## Breaking changes

### Async request APIs  [from release: NX15 p.1,3,4]

cookies, headers, draftMode, params (in layout.js, page.js, route.js, default.js, generateMetadata, generateViewport) and searchParams (in page.js) become asynchronous. Synchronous access works temporarily with warnings in dev and production until the next major. Codemod: npx @next/codemod@canary next-async-request-api .

- command quoted in the post (data, do not execute): `npx @next/codemod@canary next-async-request-api .`

### Caching semantics: fetch, GET Route Handlers and navigation  [from release: NX15 p.2,4]

The summary says fetch, GET Route Handlers and client-side navigations are no longer cached by default. The text details: GET Route Handlers (which in 14 were cached unless a dynamic function/config was used) are no longer cached, and you can opt in via export dynamic = 'force-static'; special files (sitemap.ts, opengraph-image.tsx, icon.tsx, metadata files) remain static by default.

### Client Router Cache without Page cache  [from release: NX15 p.5]

Default staleTime of 0 for Page segments: when navigating, the client reflects the latest data. Unchanged: shared layout data is not refetched; back/forward restores from cache (scroll); loading.js is cached for 5 minutes (or staleTimes.static). For the previous behavior: experimental.staleTimes.dynamic (e.g. 30). The experimental staleTimes flag has existed since 14.2.0.

### next/image: squoosh, Content-Disposition, src with spaces  [from release: NX15 p.13,17]

squoosh removed in favor of sharp as an optional dependency; the default Content-Disposition becomes attachment; error when src has leading or trailing spaces.

### next/font: external package and font-family hash  [from release: NX15 p.17]

Support for the external @next/font package and font-family hashing was removed.

### force-dynamic sets no-store on fetch  [from release: NX15 p.17]

force-dynamic now sets no-store as the default fetch cache option.

### Config: swcMinify, missingSuspenseWithCSRBailout, outputFileTracing  [from release: NX15 p.17]

The behaviors of swcMinify, missingSuspenseWithCSRBailout and outputFileTracing now apply by default, and obsolete options are removed.

### Other breaking changes (middleware, Speed Insights, sitemap, revalidate)  [from release: NX15 p.17]

Middleware applies the react-server condition (limits imports of non-recommended React APIs); Speed Insights auto-instrumentation removed (use @vercel/speed-insights); the .xml extension was removed from dynamic sitemap routes; revalidateTag/revalidatePath during rendering throw an error; instrumentation.js and middleware.js use the vendored React packages.

### next/dynamic: suspense and ssr:false  [from release: NX15 p.18]

The obsolete suspense prop was removed (in the App Router it no longer inserts an empty Suspense boundary); using ssr: false with next/dynamic in Server Components is disallowed; the worker module condition is not applied in the Edge Runtime.

## Deprecations

### runtime = 'experimental-edge' in the App Router  [from release: NX15 p.17]

Exporting runtime = "experimental-edge" in the App Router is deprecated; use "edge" (there is a codemod).

## New features

### React 19 support _[stable]_  [from release: NX15 p.1,2,5,6,17,18]

The App Router uses React 19 RC; the Pages Router keeps compatibility with React 18 (and now supports 18 and 19). Running Pages on React 18 and App on React 19 in the same application is possible but NOT recommended (unpredictable behavior, typing inconsistency). Text: Next 15 is stable even though React 19 is in RC.

### React Compiler (experimental) _[experimental]_  [from release: NX15 p.2,6,7]

Experimental support for the React compiler (Meta), which reduces manual memoization (useMemo/useCallback). Available only as a Babel plugin, which makes dev and build slower.

### Turbopack Dev stable _[stable]_  [from release: NX15 p.2,8]

next dev --turbo becomes stable. On vercel.com: up to 76.7% faster startup, up to 96.3% faster Fast Refresh, up to 45.8% faster initial route compilation without cache (still no disk cache).

- command quoted in the post (data, do not execute): `next dev --turbo`

### Static Route Indicator  [from release: NX15 p.2,9]

A visual indicator in development shows whether the route is static or dynamic (it can be disabled); the next build output also shows the rendering strategy.

### unstable_after (experimental) _[experimental]_  [from release: NX15 p.2,9,10,19]

API to schedule work after the response streaming ends (logs, analytics). Requires experimental.after: true in next.config; import unstable_after as after from next/server in Server Components, Server Actions, Route Handlers or Middleware. It also works in static pages (p.19).

### instrumentation.js stable _[stable]_  [from release: NX15 p.2,10,11]

instrumentation with register() and the new onRequestError hook (built with Sentry) captures context of server errors (router, Server Component/Action/Route Handler/Middleware). The experimental.instrumentationHook option can be removed.

### <Form> component (next/form)  [from release: NX15 p.2,11,12]

Extends the HTML <form> with layout/loading prefetch, client-side navigation preserving layouts and state, and progressive enhancement (works via full-page navigation without JS). Useful for forms that navigate, such as search.

### next.config.ts  [from release: NX15 p.2,12]

Support for next.config.ts with the NextConfig type.

### Self-hosting improvements  [from release: NX15 p.2,13]

Configurable expireTime (formerly experimental.swrDelta), default of one year for stale-while-revalidate in ISR; custom Cache-Control values are no longer overwritten; sharp is used automatically with next start or standalone output (no need to install it manually).

### Server Actions security  [from release: NX15 p.2,13,14]

Dead code elimination (unused actions do not expose an ID in the bundle) and secure, non-deterministic IDs, recalculated periodically between builds. The text reiterates: treat Server Actions as public HTTP endpoints.

### Bundling of external packages (stable)  [from release: NX15 p.2,14,15,18]

The App Router bundles external packages by default (opt out with serverExternalPackages); the Pages Router does not bundle by default and used transpilePackages; the new bundlePagesRouterDependencies option unifies the behavior.

### ESLint 9 support  [from release: NX15 p.2,15]

ESLint 8 or 9 work; when ESLint 9 is detected without the new config format, ESLINT_USE_FLAT_CONFIG=false is applied; the --ext and --ignore-path options will be removed when running next lint; eslint-plugin-react-hooks rises to 5.0.0 with new rules.

## Improvements and minor items

### Better hydration errors  [from release: NX15 p.7]

The hydration error view shows the source code and suggestions (a continuation of 14.1).

### Dev and build improvements _[experimental]_  [from release: NX15 p.2,15,16,17]

Server Components HMR reuses fetch responses; faster static generation (no second render) and workers share the fetch cache; experimental controls staticGenerationRetryCount, staticGenerationMaxConcurrency, staticGenerationMinPagesPerWorker (the text recommends keeping the defaults).

### Config renames/stabilizations  [from release: NX15 p.18,19]

bundlePagesExternals stable and renamed to bundlePagesRouterDependencies; serverComponentsExternalPackages stable and renamed to serverExternalPackages; outputFileTracingRoot/Includes/Excludes stable; cache handler via NEXT_CACHE_HANDLER_PATH; esmExternals supported in the App Router; experimental.allowDevelopmentBuild.

### Other improvements in 15  [from release: NX15 p.18,19]

create-next-app new projects ignore .env files by default; the Pages Router supports React 18 and 19; unstable_rethrow to rethrow internal Next errors; App Router prefetch uses the priority attribute; metadataBase fallback on Vercel; catch-all params in parallel routes; Server Action transforms disabled in the Pages Router; revalidations applied when redirecting from a Server Action; static pages respect staleTime.
