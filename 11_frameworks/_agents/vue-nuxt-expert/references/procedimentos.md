# Procedures (each step has a page; extras marked)

## P1 - Identify which Vue the code uses
1. `new Vue({ el, data })`, `Vue.component`, `Vue.use`, `filters`, `slot="x"`, `this.$root.$on` -> VUEHB style (Vue 2, 2018) (VUEHB p.8, 63-65, 104-109).
2. `createApp`, `ref`, `<script setup>` -> VUE3G style (Vue 3) (VUE3G p.1, 5-6).
3. Run `python -I scripts/vue_lint.py FILE` and `python -I scripts/vue_compare.py detect FILE`.
4. Compatibility question between the two: NOT COVERED; consult the Migration Guide cited in VUE3G p.1 (outside the collection).

## P2 - Choose Options API or Composition API
Apply VUE3G p.7: no build tools or low complexity -> Options; full app -> Composition + SFC; learning -> whichever seems easier. `vue_compare.py recommend`.

## P3 - Review a handbook-style Vue 2 component
Check: `data` as a regular function when using `this` (VUEHB p.70-73); computed/methods without arrows if they use `this` (p.92, 106); no `this.data.x` (p.89-90); interpolation with a single expression (p.74); attributes with `v-bind` (p.82); `v-html` only with trusted content ([inference] from p.82); props not mutated (p.107); `next()` called in guards (p.128); Vuex state only via mutation (p.116); CSS with `scoped` when it must be local (p.69).

## P4 - Choose between method, computed and watch
Table in `04-reatividade-methods-computed-watch.md` (VUEHB p.94-95). Non-reactive value (such as `Date.now()`) -> method (p.93-94).

## P5 - Decide how components communicate (Vue 2, handbook)
Parent -> child: props (p.107). Child -> parent: `$emit` + `v-on` (p.107-108). Siblings/distant: event bus on `$root` (p.109); if it grows: Vuex (p.110-111).

## P6 - Choose a rendering mode in Nuxt (v4.5.2)
SSR is the default (NUXT p.1-2). Fully static site: `nuxt generate`; no SSR: `ssr: false`; mixed per route: `routeRules` (p.3). Deploy: Node/Deno, static, serverless/edge (p.3). Configuration details: NOT COVERED. Script: `nuxt_checklist.py`.

## P7 - Review a Nuxt project (static, from a folder)
Run `python -I scripts/nuxt_checklist.py FOLDER`; check routes in `app/pages/` (NUXT p.1), API in `server/api/`, middleware in `server/middleware/` (p.3), `ssr`/`routeRules` options (p.3). Nothing is executed.

## P8 - Answering "NOT COVERED"
Use `scripts/vue_lookup.py TERM`; if it returns NOT COVERED, say what the sources cover that is closest, and only give extra content if the user asks, labeled `[extrapolation]`.
