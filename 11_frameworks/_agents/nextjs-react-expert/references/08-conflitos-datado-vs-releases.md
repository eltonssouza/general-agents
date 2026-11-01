# Conflicts and evolutions: [DATED] handbooks vs release posts

The two handbooks (NXHB, Next 9.1.2 / November 2019; RCTHB, November 2020) are **[DATED]** relative to the posts NX13 (2022) to NX16 (2025). Each row gives the pages on both sides. Types: *direct conflict* (the release states something incompatible with the handbook), *evolution* (the release shows another mechanism for the same need), *coexistence*, *alternative*, *silence* (the releases say nothing: do NOT infer deprecation) and *gap* (a subject the handbook does not cover).

Lookup: `python -I scripts/nx_lookup.py --conflicts`.

## C01 — next/link with an <a> child  (direct conflict)

- **[DATED] NXHB p.41,42,51,52,53,54:** Link wraps an <a> child (and the custom Link clones the child).
- **[from release] NX13 p.11,14:** Link always renders <a>; an <a> child is no longer allowed (legacyBehavior or remove; new-link codemod).
- **Note:** For Next >= 13 the NXHB pattern breaks; the custom Link with cloneElement (p.54) depends on the child.

## C02 — Static export (next export)  (direct conflict)

- **[DATED] NXHB p.6:** next export generates a fully static site.
- **[from release] NX14 p.9:** next export command removed in favor of output: 'export'.
- **Note:** NXHB mentions the command only as a feature in the list (p.6).

## C03 — Tutorial React/Node/Next versions  (direct conflict)

- **[DATED] NXHB p.14,80:** package.json with next ^9.1.2, react ^16.11.0; tells you to use the latest Node LTS (no number).
- **[from release] NX13 p.14:** Minimum React 18.2.0 (was 17.0.2); minimum Node 14.6.0. Later: Node 18.17 (NX14), 18.18.0 (NX15), 20.9.0 (NX16).
- **Note:** The NXHB project (React 16) does not meet the Next 13+ minimum according to NX13 p.14.

## C04 — How to create the project  (evolution)

- **[DATED] NXHB p.8,9,10,11,15:** npx create-next-app (without @latest); structure with pages/; dev scripts: next, build, start.
- **[from release] NX16 p.2,7:** npx create-next-app@latest; redesigned template with App Router by default, TypeScript, Tailwind and ESLint.
- **Note:** The releases use next dev/next build (NX13 p.8; NX16 p.6); they do not say that bare 'next' without a subcommand was removed (silence).

## C05 — Routing: pages/ vs app/  (coexistence)

- **[DATED] NXHB p.4,12,34,37:** Automatic file-system routing in pages/.
- **[from release] NX13 p.2,3:** app/ in beta (not recommended for production); pages/ stable and supported 'for the foreseeable future'; incremental adoption.
- **Note:** NX15 p.5-6, 18 keeps the Pages Router (with React 18/19); NX16 p.7 makes the App Router the create-next-app default; NX16 does NOT say whether the Pages Router is still supported or deprecated (NO information).

## C06 — Data fetching  (silence)

- **[DATED] NXHB p.56,57,58,59,60,61:** getInitialProps in the page component; runs on the server and on client navigation.
- **[from release] NX13 p.5,6:** Async Server Components + extended fetch (cache force-cache/no-store/revalidate), compared with getStaticProps/getServerSideProps.
- **Note:** No release mentions getInitialProps or declares it deprecated; they are different models (Pages vs app/). Do not claim deprecation.

## C07 — Backend: API Routes  (alternative)

- **[DATED] NXHB p.68,69,70,71,72:** pages/api with export default (req, res); req.method, req.query, cookies, body.
- **[from release] NX14 p.2,3,4:** API Routes (since Next 9) vs Server Actions: a 'use server' function called from the component without creating a manual API Route.
- **Note:** NX14 does not say API Routes were removed. NX15 p.4 covers GET Route Handlers (App Router).

## C08 — Page metadata (<head>)  (silence)

- **[DATED] NXHB p.64,65:** next/head with <title>/<meta> inside the component.
- **[from release] NX14 p.7,8:** metadata API (with viewport/generateViewport); NX15 mentions generateMetadata (p.3).
- **Note:** The releases do not say whether next/head was deprecated.

## C09 — Link prefetch  (evolution)

- **[DATED] NXHB p.5,52,53:** Prefetch when the Link enters the viewport, production only; Save-Data/slow connection; prefetch={false}.
- **[from release] NX16 p.8,9,13:** Rewritten prefetch cache: layout deduplication and incremental prefetch (cancels outside the viewport).
- **Note:** NX13 p.14: no prefetch for bots; NX15 p.12: <Form> with prefetch.

## C10 — Bundler and bundle analysis  (evolution)

- **[DATED] NXHB p.6,80,81:** Next abstracts webpack; @next/bundle-analyzer + cross-env ANALYZE=true next build.
- **[from release] NX16 p.6:** Turbopack is the default (dev and build); webpack via next dev/build --webpack.
- **Note:** The releases say nothing about @next/bundle-analyzer under Turbopack (silence).

## C11 — Styles  (silence)

- **[DATED] NXHB p.61,62,63,64:** styled-jsx; external CSS via @zeit/next-css; Sass via @zeit/next-sass.
- **[from release] NX15 p.18:** Only mentions merging global CSS with CSS Modules (improvement item); NX16 p.7: template with Tailwind CSS.
- **Note:** No release mentions styled-jsx or @zeit/next-*.

## C12 — Deploy platform (Zeit Now vs Vercel)  (silence)

- **[DATED] NXHB p.76,77,78,79:** Next.js created by Zeit; deploy with the now CLI (now.sh).
- **[from release] NX14 p.10:** The releases mention the Vercel core team (NX14 p.10; NX15 p.19) and the footer 'Vercel, Inc.'.
- **Note:** The texts do not relate Zeit and Vercel. [extrapolation] they are the same company renamed; this is not in the collection. Now plan prices/limits (NXHB p.77) are [DATED].

## C13 — Dynamic imports / lazy loading  (evolution)

- **[DATED] NXHB p.5,85,86,87,88,89,90:** Dynamic import() inside getInitialProps to split Moment.js into another bundle.
- **[from release] NX15 p.18:** next/dynamic: suspense prop removed; ssr:false disallowed in Server Components.
- **Note:** NXHB does not use next/dynamic in its examples; only dynamic import().

## C14 — Static/dynamic indicator in dev  (evolution)

- **[DATED] NXHB p.22,23:** 'Prerendered Page' icon (automatic static optimization) when the page has no getInitialProps.
- **[from release] NX15 p.9:** Static Route Indicator in dev and per-route strategy in the next build output.
- **Note:** Close concepts, different mechanisms (Pages vs App Router); NX15 does not mention the NXHB icon.

## C15 — React: creation tool and rendering in RCTHB  (silence)

- **[DATED] RCTHB p.6,7,26:** create-react-app; example with ReactDOM.render.
- **[from release] NX13 p.14:** Minimum React 18.2.0; NX15 p.5-6: React 19 RC in the App Router; NX16 p.11: React 19.2.
- **Note:** The releases do not mention create-react-app or ReactDOM.render. Whether these patterns work in React 18/19 is [extrapolation], outside the collection.

## C16 — Server Components and Client Components  (RCTHB gap)

- **[DATED] RCTHB p.11,12,13,14,24,25,26,31,32,33:** Components with useState, onClick and useEffect (client model), with no server/client distinction.
- **[from release] NX13 p.4:** app/ adopts React Server Components; server-first by default.
- **Note:** RCTHB does not cover Server Components; the collection does not detail the 'use client' boundary beyond mentions (NX14 p.4 uses 'use server').

## C17 — Hooks and hooks lint  (evolution)

- **[DATED] RCTHB p.25,32,33:** useState and useEffect (dependency array).
- **[from release] NX15 p.15:** eslint-plugin-react-hooks 5.0.0 with new rules (the text does not describe them); NX14 p.5 mentions useOptimistic/useFormState/useFormStatus; NX16 p.11 mentions useEffectEvent.
- **Note:** New hooks are only mentioned in the releases; no usage explanation in the collection.
