# Next.js 14 — change map (only what the NX14 post states)

**Source:** `NextJS-14-Release.pdf` (acronym **NX14**), post of 2023-10-26. Convention: PDF page (no printed number). Everything below is a paraphrase of the post; nothing was completed with outside knowledge.

## Notes on the capture

- Blog post of Oct 26, 2023 (Thursday), 13 pages; useful content p.1-9; p.10-13 are contributors and footer.
- The command npx create-next-app@latest appears at the top of p.2 in the extraction (introduced on p.1).
- NX14 gives no upgrade command besides create-next-app; it mentions codemods by link, with no command text.

To query from the command line: `python -I scripts/nx_changes.py changes --only 14`.

## Upgrade / commands

### Commands quoted in 14  [from release: NX14 p.1,2,9]

The post says 'Upgrade today or get started with' and shows npx create-next-app@latest. It mentions codemods (links) for @next/font and ImageResponse, without command text.

- command quoted in the post (data, do not execute): `npx create-next-app@latest`

## Requirements

### Minimum Node.js 18.17  [from release: NX14 p.9]

The minimum Node.js version becomes 18.17.

## Breaking changes

### @next/font dropped in favor of next/font  [from release: NX14 p.9]

Support for @next/font was dropped in favor of next/font; there is a codemod.

### ImageResponse comes from next/og  [from release: NX14 p.9]

The ImageResponse import changes from next/server to next/og; there is a codemod.

### next export command removed  [from release: NX14 p.9]

The next export command was removed in favor of the config option output: 'export'.

## Removals

### next-swc WASM target removed  [from release: NX14 p.9]

The WASM target of the next-swc build was removed.

## Deprecations

### viewport, colorScheme and themeColor leave metadata  [from release: NX14 p.7,8]

The metadata options viewport, colorScheme and themeColor are deprecated and will be removed in a future major; viewport and generateViewport appear as replacements. The old options keep working; the other metadata options do not change.

### onLoadingComplete of next/image  [from release: NX14 p.9]

The onLoadingComplete prop of next/image is deprecated in favor of onLoad.

### images.domains  [from release: NX14 p.9]

The domains option of next/image is deprecated in favor of remotePatterns.

## New features

### Turbopack in development (not yet stable) _[preview]_  [from release: NX14 p.1,2]

5,000 next dev integration tests pass with Turbopack (90% of the next dev tests); on vercel.com: up to 53.3% faster local server startup and up to 94.7% faster Fast Refresh. It becomes stable in a minor release once it reaches 100% of the tests; webpack remains supported for custom configs and plugins. Usage: next dev --turbo.

- command quoted in the post (data, do not execute): `next dev --turbo`

### Server Actions (stable) _[stable]_  [from release: NX14 p.1,2,3,4,5]

Functions that run on the server, called directly from React components ('use server' directive), instead of manual API Routes; they work with <form action> and also as a function call. Built on the React canary channel. They integrate with revalidatePath/revalidateTag, redirect, cookies, useOptimistic, useFormState and useFormStatus.

### Partial Prerendering (preview) _[preview]_  [from release: NX14 p.5,6,7]

Preview of a compiler optimization: a static shell is served immediately and dynamic content is streamed, defined by <Suspense> boundaries (prerendered fallback); no new APIs. loading.js is already an implicit boundary. Under active development; more news promised for a minor release.

### Next.js Learn course  [from release: NX14 p.1,8,9]

New free course (App Router, Tailwind, fonts and images, Postgres, Server Components, streaming, optional PPR, mutations, errors, accessibility, authentication, metadata).

## Improvements and minor items

### Other improvements in 14  [from release: NX14 p.9]

More verbose fetch cache logging (optional); 80% smaller function in a basic create-next-app; better edge runtime memory management in development.
