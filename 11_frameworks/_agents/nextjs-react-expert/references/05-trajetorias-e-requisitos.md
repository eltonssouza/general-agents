# Trajectories by topic and requirements (NX13 → NX16)

Only what the four posts state. "—" cells mean **the text does not say** (not the same as "did not change"). Pages = PDF page of the indicated post. Comparator: `python -I scripts/nx_changes.py topic TERM`.

## 1. Stated requirements

| Item | NX13 (2022) | NX14 (2023) | NX15 (2024) | NX16 (2025) |
|---|---|---|---|---|
| Minimum Node.js | 14.6.0 (was 12.22.0) p.14 | 18.17 p.9 | 18.18.0 p.17 | 20.9.0 (LTS; Node 18 unsupported) p.11 |
| Minimum / used React | 18.2.0 (was 17.0.2) p.14 | — | App Router on React 19 RC; Pages Router accepts 18 and 19 p.5-6, 18 | App Router on React Canary with 19.2 features p.11 |
| Minimum TypeScript | — | — | — | 5.1.0 p.11 |
| Browsers | Chrome 64+, Edge 79+, Firefox 67+, Opera 51+, Safari 12+ (no IE) p.14-15 | — | — | Chrome 111+, Edge 111+, Firefox 111+, Safari 16.4+ p.11 |
| ESLint | — | — | 8 or 9 (compatible) p.15 | plugin with Flat Config by default (aligned with ESLint v10) p.13 |

## 2. Trajectories

**Bundler.** NX13 p.7-8: Turbopack in alpha, only `next dev --turbo`. NX14 p.1-2: 5,000 `next dev` tests pass (90%), not yet stable (becomes stable in a minor once it reaches 100%). NX15 p.8: `next dev --turbo` stable. NX16 p.6: stable for dev **and** build and the default; `--webpack` to opt out; disk cache (beta) in dev, p.6-7.

**Cache.** NX13 p.5-6: extended fetch; `force-cache` is the default; `no-store` and `next.revalidate` options. NX14 p.9: verbose fetch-cache logging (optional); p.5-7 PPR in preview. NX15 p.2, 4-5, 17: fetch, GET Route Handlers and client navigation are no longer cached by default (staleTime 0 on Page segments; `force-dynamic` sets `no-store`). NX16 p.1-3: Cache Components, `'use cache'`, **opt-in** cache; p.9-11: `revalidateTag(tag, profile)`, `updateTag`, `refresh`.

**Middleware → proxy.** NX13 p.13-14: expanded Middleware API (headers, direct response; required `experimental.allowMiddlewareResponseBody`). NX15 p.17: `react-server` condition and vendored React packages in middleware. NX16 p.4, 14: `proxy.ts` (Node.js runtime) replaces `middleware.ts`; the latter is deprecated, still available for Edge. NX14: the text does not say.

**Request APIs.** NX15 p.3-4: `cookies`, `headers`, `draftMode`, `params`, `searchParams` become async (sync tolerated with warnings until the next major). NX16 p.12: synchronous access removed.

**next/image.** NX13 p.8-9, 14: new component; the old one becomes `next/legacy/image`; `next/future/image` becomes `next/image`; `alt` required. NX14 p.9: `onLoadingComplete` and `domains` deprecated. NX15 p.17: `squoosh` → optional `sharp`; `Content-Disposition` attachment; error on spaces in `src`; p.13 automatic `sharp` in self-hosting. NX16 p.12-14: `images.localPatterns` for local src with query; new defaults (`minimumCacheTTL` 4 h, `qualities` [75], `maximumRedirects` 3, `dangerouslyAllowLocalIP`); `next/legacy/image` and `images.domains` deprecated.

**Fonts.** NX13 p.10: `@next/font` (beta). NX14 p.9: abandoned in favor of `next/font` (codemod). NX15 p.17: the external package and the `font-family` hash removed.

**PPR.** NX14 p.5-7: preview, defined by Suspense boundaries, no new APIs. NX16 p.3, 12: `experimental.ppr` and `experimental_ppr` removed; evolves into Cache Components (`cacheComponents: true`; `experimental.dynamicIO` renamed). NX15 does not mention PPR as a feature (only as a motivation for the cache, p.4).

**Server Actions.** NX14 p.4-5: stable. NX15 p.13-14: secure IDs and dead-code elimination; treat as public endpoints. NX16 p.9-11: `updateTag` and `refresh` (only in Server Actions).

**React.** NX13: minimum 18.2.0 and Server Components in app/. NX14: App Router on the canary channel (`useOptimistic`, `useFormState`, `useFormStatus` cited, p.4-5). NX15: React 19 (RC), experimental React Compiler (Babel). NX16: stable React Compiler (not the default), 19.2 features (View Transitions, `useEffectEvent`, Activity).

**Lint.** NX15 p.15: ESLint 9, automatic `ESLINT_USE_FLAT_CONFIG=false`, hooks plugin 5.0.0. NX16 p.12-13: `next lint` removed (use Biome/ESLint; `next build` does not run lint; a codemod exists), plugin with Flat Config.

**Config (renames and removals cited).** NX13: `swcMinify` defaults to `true`; `target` removed. NX15: `serverComponentsExternalPackages` → `serverExternalPackages`; `bundlePagesExternals` → `bundlePagesRouterDependencies`; `experimental.swrDelta` → `expireTime`; `instrumentationHook` no longer needed; `next.config.ts` supported (p.12). NX16 p.12: `experimental.turbopack` → `turbopack`; `dynamicIO` → `cacheComponents`; `serverRuntimeConfig`/`publicRuntimeConfig` removed; `devIndicators` (3 options) removed; `reactCompiler` moved out of experimental (p.7); `--experimental-next-config-strip-types` (p.14).

**Upgrade (literal commands from the posts).** NX13 p.1-2: `npm i next@latest react@latest react-dom@latest eslint-config-next@latest`. NX15 p.1-3: `npx @next/codemod@canary upgrade latest` (`canary` is the codemod version; the text recommends it even when migrating to the latest Next) or `npm install next@latest react@rc react-dom@rc`. NX16 p.2: `npx @next/codemod@canary upgrade latest` or `npm install next@latest react@latest react-dom@latest`. Codemods cited with a command: `new-link` (NX13 p.11), `next-image-to-legacy-image` (NX13 p.9), `next-async-request-api` (NX15 p.4), `next-lint-to-eslint-cli` (NX16 p.12).

## 3. Things the posts do NOT say (do not fill in)
- Whether `viewport`/`colorScheme`/`themeColor` in `metadata` (deprecated in NX14 p.8) have already been removed.
- What happened to `unstable_after` in NX16 (the post does not mention it).
- Whether the Pages Router is still supported in NX16 (NX13 p.2 says "for the foreseeable future"; NX15 p.5-6 keeps it with React 18/19).
- Whether the `--turbo` flag is still valid in NX16.
- Which new rules `eslint-plugin-react-hooks` 5.0.0 brings (NX15 p.15 only says they exist).
