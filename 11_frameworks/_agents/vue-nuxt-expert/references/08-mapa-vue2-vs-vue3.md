# 08 - Vue 2 (VUEHB, 2018) vs Vue 3 (VUE3G) map - only with what the texts say [DATED]

The VUEHB is Vue 2 by inference (INDEX §2); the VUE3G is Vue 3. The collection **does not contain** the official migration guide, so this map only compares what each text **shows**; "does not appear" does **not** mean "was removed".

| Topic | VUEHB (Vue 2, Jul/2018) | VUE3G (Vue 3, 2026 capture) | Safe reading |
|---|---|---|---|
| Creating the app | `new Vue({ el: '#example', data })` (p.8, 12) | `createApp({ setup() { ... } }).mount('#app')` (p.1-2) | different ways to initialize; the newer text uses `createApp` |
| Importing Vue | `import Vue from 'vue'` (p.12) | `import { createApp, ref } from 'vue'` (p.1) | named import in Vue 3 (example) |
| State | `data` (object or function) (p.8, 70-73) | `data()` (Options, p.5) or `ref()` (Composition, p.6) | Options is still documented in Vue 3 |
| API styles | options only (p.66-67) | Options **and** Composition (p.4-7) | Composition API is what the newer text adds |
| SFC | `.vue` requires Webpack (p.68) | `.vue` + `<script setup>` + `<style scoped>` (p.4-6); "Vue takes care of the build setup" (p.4) | `<script setup>` does not appear in the VUEHB |
| CSS scoping | `<style scoped>` (p.14, 69) | `<style scoped>` (p.4) | same |
| Template/directives | `{{ }}`, `v-bind`/`:`, `v-on`/`@`, `v-if`... (p.71-87) | `{{ }}`, `@click` (p.2, 4) | same basic syntax in the snippets shown; the VUE3G does not list directives |
| Events | `$emit`, `v-on`, event bus on `$root` (p.107-109) | does not appear | NOT COVERED in Vue 3 |
| Props | `props` array/object with types (p.95-99) | does not appear | NOT COVERED in Vue 3 |
| Slots | `<slot>`, `slot="name"` (p.102-104) | does not appear | NOT COVERED in Vue 3 |
| Filters | `{{ x \| filter }}` (p.104-106) | does not appear | NOT COVERED (do not claim removal) |
| computed/watch | sections p.90-95 | does not appear | NOT COVERED in Vue 3 |
| Lifecycle | `mounted` cited (p.109) | `mounted` (Options) and `onMounted` (Composition) (p.5-6) | an equivalent is shown in both VUE3G styles |
| Global state | Vuex (p.110-120) | does not appear | NOT COVERED |
| Routing | Vue Router, `Vue.use(VueRouter)` (p.120-133) | does not appear | NOT COVERED |
| Project tooling | Vue CLI 3, `vue create`, Webpack (p.10, 18-33) | does not appear (only "Vue takes care of the build", p.4) | NOT COVERED about the current tool |
| DevTools / editor | Vue DevTools, Vetur (p.34-62) | does not appear | NOT COVERED |
| Support | "IE9+" (p.80) | Vue 2 support ended on 12/31/2023 (p.1) | [DATED] browsers and support |
| Size | ~24KB (p.2) | does not appear | [DATED] |

## How to answer "does my Vue 2 code run on Vue 3?"
Honest answer: **NOT COVERED** in the collection (there is no migration guide). Give: (a) what the VUEHB shows for Vue 2; (b) what the VUE3G shows for Vue 3; (c) the Migration Guide link cited in VUE3G p.1 as a pointer (content absent); (d) any additional judgment as `[extrapolation]`. The `vue_lint.py` script flags handbook-style constructs (`new Vue`, `Vue.component`, filters, `slot=`, `Vue.use`) with the label "VUEHB construct (Vue 2); VUE3G does not show it".
