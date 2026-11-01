# Procedures (only what the sources support)

The commands below are **collection data**: the agent does not run them and they are [DATED] (check the current documentation).

## P1. Create and run a Svelte project (SVHB p.3-6)
1. Have Node.js (p.3).
2. `npm create vite@latest helloworld -- --template svelte` (p.4).
3. `cd helloworld`, `npm install`, `npm run dev`; open localhost:5173 (p.4-5).
4. Open in the editor; install Svelte for VS Code (p.6-7).
5. Read `src/main.js` and `src/App.svelte` (p.8).

## P2. Create a component that receives data (SVHB p.10-12, 19-20)
1. `.svelte` file; `<script>` with `export let name` (p.11, 20).
2. Import in the parent (`import X from './X.svelte'`) and use `<X name={value} />` (p.19-20).
3. If two-way is needed, `bind:prop={variable}` (p.38-39).

## P3. Change array state (SVHB p.15-16)
Prefer `list = [...list, item]`; if using `push/pop/shift/splice`, reassign afterwards (`list = list`).

## P4. Share state (SVHB p.21-28), from shortest to longest distance
1. Props, lifting the state to the common ancestor (p.21-22).
2. Context (`setContext`/`getContext`) for descendants (p.22-23).
3. Store (`writable` etc.) in a shared `.js`, read with `$name` (p.23-25).

## P5. Clean up a timer (SVHB p.31-32)
In `onMount`, create the `setInterval` and **return** a function with `clearInterval` (or use `onDestroy`).

## P6. Form (SVHB p.33-37, 47)
`bind:value` on a `let` variable; `on:submit|preventDefault={...}` when you need to prevent the default submit.

## P7. Review a component with the linter
1. `python -I scripts/svelte_lint.py Component.svelte` (each finding carries rule, origin and page).
2. For a project: `python -I scripts/svelte_checklist.py scan FOLDER` and `list`.
3. If `SVL-X01` (runes) or `SVL-X02` (`+page`/`.astro`) appears: report NOT COVERED; the linter is switched off for those parts.

## P8. Compare frameworks (SVHB, SKGS, ASTRO)
`python -I scripts/framework_compare.py table`; for one criterion, `show CRITERION`. Decision between them: NOT COVERED.

## P9. Install Astro (ASTRO p.2)
`npm create astro@latest` (the landing page says the guide details CLI, existing repository and manual; those steps are **not** in the collection).

## P10. Create a SvelteKit project
NOT COVERED: the "Creating a project" page was not captured (SKGS p.2).
