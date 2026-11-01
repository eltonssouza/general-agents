# 09 - Handbook tools: Vue CLI 3, DevTools and Vetur (2018) [DATED]

Source: VUEHB p.18-62. **Everything [DATED]**: 2018 tools (Vue CLI on Webpack, Vetur extension, old DevTools). The VUE3G and the NUXT mention none of them; do not claim that they are or are not the current tools (NOT COVERED). Pages 20-25, 36-49 and 51-54 are almost only screenshots.

## Vue CLI (p.18-33)
- [from source] (VUEHB p.18) The author warns that the CLI was moving from version 2 to 3 (not yet stable) and describes 3.
- [from source] (VUEHB p.19) Global installation: `npm install -g @vue/cli` or `yarn global add @vue/cli`; command `vue`.
- [from source] (VUEHB p.19-20) Goal: make the tools work together and hide the configuration; it allows tweaking without "ejecting" (the text's contrast with `create-react-app`); at runtime it is a tool built on Webpack.
- [from source] (VUEHB p.20-25) `vue create example` opens an interactive wizard: default preset with Babel and ESLint, or manual choice (Linter/Formatter, ESLint + Prettier, lint on save, tests with Mocha + Chai or Jest, configuration in `package.json` or dedicated files, save preset, Yarn or NPM).
- [from source] (VUEHB p.26-27) In `example`, `yarn serve` starts development mode; `yarn build` (production build), `yarn lint`, `yarn test:unit` (scripts from `package.json`).
- [from source] (VUEHB p.28) The CLI creates a git repository and makes the first commit.
- [from source] (VUEHB p.28-29) `vue create -p favourite example-2` uses a preset; presets live in `.vuejs` in the user's directory; a preset is a collection of plugins with optional configuration (example with `@vue/cli-plugin-babel`, `@vue/cli-plugin-eslint`, `@vue/cli-plugin-unit-jest`, `router: true`, `vuex: true`).
- [from source] (VUEHB p.29-30) `vue add @vue/cli-plugin-babel` adds plugins; a version can be pinned with `"version": "^3.0.0"`; remote presets via a repository with `preset.json` (`vue create --preset flaviocopes/vue-cli-preset example3`).
- [from source] (VUEHB p.31-33) Prototyping: `npm install -g @vue/cli-service-global`, then `vue serve app.vue`; `vue build` generates `dist/`; `vue inspect` shows the hidden Webpack configuration. The author notes that global dependencies are not suitable beyond a demo (p.32).

## Vue DevTools (p.34-49)
- [from source] (VUEHB p.34-35) The console shows a message suggesting installing the extension. DevTools only inspects apps in **development mode**, so as not to allow interacting with production (and Vue gets faster).
- [from source] (VUEHB p.35-44) Three ways to install: Chrome, Firefox or standalone app (`npm install -g @vue/devtools`, command `vue-devtools`, pasting the tag `<script src="http://localhost:8098"></script>` in `index.html`).
- [from source] (VUEHB p.45-50) Usage: "Vue" panel or "Inspect Vue component"; component tree with props and data; buttons Components, Vuex, Events, Refresh; `$vm0` in the console; filter, select on the page, name format, Inspect DOM, open in editor.

## VS Code and Vetur (p.50-62)
- [from source] (VUEHB p.50-51) Vetur: extension for VS Code (more than 3 million downloads in 2018).
- [from source] (VUEHB p.53-60) Offers syntax highlighting for SFC blocks (HTML, CSS, JS, Pug, Haml, SCSS, PostCSS, Sass, Stylus, TypeScript), snippets, IntelliSense, scaffolding (`scaffold` generates template/script/style), Emmet, lint integration with ESLint and formatting (tied to `editor.formatOnSave`, Prettier for most languages) (p.62).
- [DATED] Do not claim that Vetur is the current recommendation; the collection only records 2018.
