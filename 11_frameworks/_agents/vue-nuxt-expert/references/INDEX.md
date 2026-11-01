# INDEX - vue-nuxt-expert

Agent for an **overview based on three short sources** (an old handbook, an introduction page of Vue 3 and an introduction page of Nuxt). It is not a complete Vue/Nuxt reference agent: what the sources do not say is **NOT COVERED** or, if the user asks, a labeled `[extrapolation]`.

## 1. Sources, versions and dates (recorded from the texts themselves)

| Abbrev. | PDF file | Pages | What it really is | Version / date that appears in the text |
|---|---|---|---|---|
| **VUEHB** | Vue-Handbook-freeCodeCamp.pdf | 133 (~88 thousand characters) | Long article "The Vue Handbook" (Flavio Copes) on freeCodeCamp. Running text + many screenshots + **truncated** code boxes (see §3) | Date printed on p.1: **July 5, 2018**; popularity numbers "as of June 2018" (p.4). **It is Vue 2** (see §2). [DATED] 2018 |
| **VUE3G** | Vue3-Guide-Introduction.pdf | 8 | "Introduction" page of the official **Vue 3** documentation (vuejs.org), captured from the site | p.1: "You are reading the documentation for Vue 3"; "Vue 2 support has ended on Dec 31, 2023". Minor version does not appear. Capture date: see the PDF metadata (August 2026), **not** printed in the text |
| **NUXT** | Nuxt-Getting-Started.pdf | 6 (useful: 1-4; p.5-6 are footer/newsletter) | "Introduction" page of the "Get Started with Nuxt v4" guide (nuxt.com) | Version selector **v4.5.2** (p.1); footer "Copyright 2016-2026" (p.6) |

"Current" state of any version: **the model's prior knowledge does not count**; only the text above. [DATED] is relative to the date of each PDF.

## 2. Is the handbook Vue 2? How it was identified
The handbook **never writes "Vue 2"**. The identification is an **[inference]** from the set of evidence read: instance with `new Vue({ el, data })` (VUEHB p.8, 12), `Vue.component(...)` (p.63-64), `Vue.use(Vuex)` and `Vue.use(VueRouter)` (p.113, 121), filters `{{ name | fallback }}` (p.104-106), `slot="sidebar"` attribute (p.104), event bus on `this.$root` (p.109), `vue create` with Vue CLI on Webpack (p.10, 18-33, 68), "IE9+" (p.80) and a note that Vue CLI was moving from version 2 to 3, not yet stable (p.18). The VUE3G guide, in contrast, shows `createApp({ setup() ... }).mount('#app')` (VUE3G p.1-2). Map in `08-mapa-vue2-vs-vue3.md`.

## 3. Capture quality (for those who cite)
- **Page convention:** PDF page ("=== PAGE N ===" marker). The handbook has no printed numbering; the VUE3G and the NUXT do not either. Therefore, **PDF = the only numbering**; no offset.
- **Truncated code in the VUEHB:** the code boxes were captured with horizontal scrolling; many lines are cut off (checked by rendering p.116 and p.126). The agent only states what appears legibly; it does not complete snippets from memory as if they were from the book.
- **Pages without useful textual content (image/screen only):** VUEHB p.20-25 (CLI wizard), 36-49 (DevTools installation/use), 51-54 (Vetur); p.61 empty. The surrounding text describes what the screens show.
- **VUE3G:** p.1-2 bring the minimal example (code broken across columns); p.8 only has "learning path" links.
- **NUXT:** p.5-6 are footer (Community, Explore, newsletter, copyright). No technical content.
- No page is 404 or "Page not found". All three sources have useful content.

## 4. Map topic -> pages -> file

| Topic | Source and pages | File |
|---|---|---|
| Overview, popularity, positioning vs React/Angular (2018) | VUEHB p.2-7 | 01-vue2-handbook-fundamentos.md |
| First app (CDN), Vue CLI app, file structure | VUEHB p.8-17 | 01 |
| Vue CLI 3 (create, presets, serve/build, inspect), DevTools, VS Code/Vetur | VUEHB p.18-62 | 09-ferramentas-cli-devtools-vetur.md |
| Components (4 ways, global/local registration, SFC, scoped) | VUEHB p.62-71 | 02-componentes-props-eventos-slots.md |
| Templates, interpolation, styles/classes | VUEHB p.71-80 | 03-templates-diretivas-estilos.md |
| Directives (v-text, v-once, v-html, v-bind, v-model, v-if/else, v-for, v-on, v-show, modifiers) | VUEHB p.80-87 | 03 |
| methods / watch / computed and when to use each | VUEHB p.88-95 | 04-reatividade-methods-computed-watch.md |
| Props, events, slots, filters, communication, event bus | VUEHB p.95-110 | 02 |
| Vuex | VUEHB p.110-120 | 05-vuex-e-vue-router-vue2.md |
| Vue Router (guards, dynamic routes, nested) | VUEHB p.120-133 | 05 |
| Vue 3: what it is, declarative rendering, reactivity, SFC, API styles | VUE3G p.1-8 | 06-vue3-guia-introducao.md |
| Options API vs Composition API (according to the texts) | VUE3G p.4-7; VUEHB p.66-67, 88-95 | 07-options-vs-composition.md |
| Nuxt v4: conventions, SSR, Nitro, modules, packages | NUXT p.1-4 | 10-nuxt-v4.md |
| Differences VUEHB (Vue 2) vs VUE3G (Vue 3) | VUEHB + VUE3G | 08-mapa-vue2-vs-vue3.md |
| Terms, procedures, cases, dated items | all | glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md |

## 5. Triggers -> file
| Question | Open |
|---|---|
| "what is Vue / progressive framework / SFC?" | 06 and 01 |
| "how do I declare a component, pass props, emit an event, use a slot?" | 02 |
| "difference between computed, method and watch?" | 04 |
| "v-if, v-for, v-model, @click?" | 03 |
| "Vuex / Vue Router?" | 05 |
| "Options API or Composition API?" | 07 |
| "does my Vue 2 code work on Vue 3?" | 08 (the collection does **not** have the migration guide: NOT COVERED) |
| "Nuxt: SSR, structure, deploy?" | 10 |
| "Pinia, Vue Router 4, Vuex 4, Nuxt 3, `defineProps`, `emit` in the Composition API, `v-for` with `:key`, testing, Vite?" | **NOT COVERED** (see `datado.md`) |

## 6. Reading coverage (honest)
- **Read in full:** all 133 pages of the VUEHB, the 8 of the VUE3G and the 6 of the NUXT (text extracted by me with PyMuPDF; the files did not exist in `scratch/frameworks/` and were generated).
- **Checked visually (render):** VUEHB p.116 and p.126 (truncated code); NUXT p.1 and p.5.
- **Not verified on image:** CLI and DevTools screenshots (VUEHB p.20-25, 36-49, 51-54) and the "Result" demo of VUE3G p.2; the claims come from the surrounding text.
- Intermediate notes: `scratch/frameworks/vue-nuxt-expert/notes/`.
