# 01. Svelte Handbook: fundamentals, setup and components (SVHB p.1-14, 49)

Convention: PDF page. [DATED] article of Oct 22, 2019 (SVHB p.1); Svelte version not stated (see INDEX section 2).

## Audience and purpose (p.1-3)
- **[from source] (SVHB p.1)** author Flavio Copes; ideal reader has no Svelte knowledge, perhaps some Vue or React.
- **[from source] (SVHB p.2-3)** presents Svelte as a front-end framework for web applications, a good first choice.
- **[from source] (SVHB p.3)** core difference: the app is **compiled ahead of time**, so the whole framework does not need to be served to every visitor; less bandwidth, a feeling of lightness; **on deploy "Svelte disappears"** and only plain JavaScript remains. (No numbers: qualitative claim.)
- **[from source] (SVHB p.3)** requires Node.js; the official site has a "playground" at svelte.dev/repl.

## Creating and running the first project (p.4-7)
- **[from source] (SVHB p.4)** command: `npm create vite@latest helloworld -- --template svelte`; enter the folder, `npm install`, then `npm run dev`, which starts the development site on localhost, **port 5173**. [DATED] (command and port are from the time of the text; check the current documentation). These commands are collection data: the agent does not run them.
- **[from source] (SVHB p.5)** the browser shows the sample project (p.5 is just a screenshot).
- **[from source] (SVHB p.6-7)** open in VS Code (`code .`), which suggests the **Svelte for VS Code** extension (highlighting and other features).

## Project structure (p.8-9)
- **[from source] (SVHB p.8)** in `src`, the main file is `main.js` (entry point that initializes the `App` component), and `App.svelte` defines the root component; it imports `Counter` from `./lib/Counter.svelte` and a logo. The sample text still mentions SvelteKit as "the official app framework for Svelte, with Vite".
- **[from source] (SVHB p.8-9)** three sections: `<script>`, markup (`<main>`...) and `<style>`: this is the **single file component** (markup, behavior and style in the same file). The basis of all components.

## Components (p.10-14)
- **[from source] (SVHB p.10)** a component = an atomic, self-contained part of the application that can reference others; a form, an input or the whole application can be components. Each lives in a `.svelte` file.
- **[from source] (SVHB p.11)** sample `Dog.svelte`: `export let name` in `<script>`, `<style>` and `<h1>The dog name is {name}!</h1>`. JavaScript goes in `<script>`; the CSS in `<style>` is **scoped** to the component and does not leak (useful when reusing components or third-party libraries, such as a date picker).
- **[from source] (SVHB p.11-12)** importing: `import Dog from './Dog.svelte'` and using it like an HTML tag (`<Dog />`). The component is the file's **default export**.
- **[from source] (SVHB p.12-14)** to export something else (functions), use `<script context="module">` with `export function ...`; another component imports `Button, { changeColor } from './Button.svelte'`; the component can still have a regular `<script>`. The text itself says that, for the example case (changing the button color), **props are the better solution** (p.13).

## Where to go next (p.49)
- **[from source] (SVHB p.49)** points to the official Svelte site and to **SvelteKit**, "built on top of Svelte", for server-rendered apps with Node.js.

## What SVHB does NOT cover (NOT COVERED)
TypeScript, testing, transitions/animations, actions (`use:`), `{@html}`, `<svelte:head>`, the `class:` directive, global CSS, SSR, routing, deploy, runes. Run `python -I scripts/svelte_lookup.py --gaps`.
