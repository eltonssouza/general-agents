# 07 - Options API vs Composition API (according to the texts) [DATED]

Main source: VUE3G p.4-7 (Vue 3). The VUEHB (2018, Vue 2) only shows the options style (`data`, `methods`, `computed`, `watch`) and **does not know** the Composition API.

## What the VUE3G says
- [from source] (VUE3G p.4-5) Components can be written in two styles: **Options API** and **Composition API**.
- [from source] (VUE3G p.5) **Options API:** the logic is an object with options (`data`, `methods`, `mounted`...); the properties are exposed on `this`, the component instance. `data()` returns the reactive state; `methods` are functions that change state and can be bound in the template; lifecycle hooks (`mounted`) run at stages of the component.
- [from source] (VUE3G p.5-6) **Composition API:** the logic is defined by imported functions (`ref`, `onMounted`). In an SFC, `<script setup>` is usually used, a hint that makes Vue apply compile-time transforms with less boilerplate: imports and top-level variables/functions are directly usable in the template.
- [from source] (VUE3G p.6) Both cover the common cases; they are interfaces over **the same system**; "the Options API is implemented on top of the Composition API". Fundamental concepts are shared.
- [from source] (VUE3G p.6-7) Options: centered on the "component instance" (`this`), aligns with a class/OOP mental model, is friendlier to beginners by abstracting reactivity and imposing organization by option groups. Composition: state declared in function scope and composed from several functions; freer and requires understanding reactivity; in return, it allows more powerful patterns of organization and logic reuse.
- [from source] (VUE3G p.7) Recommendations: for learning, the style that seems easier; **production:** Options API if there are **no** build tools or the use is low complexity (e.g. progressive enhancement); **Composition API + SFC** for full applications. You do not need to commit to just one while learning; the documentation offers an "API Preference" switch.

## Construct map (only what the two VUE3G examples show)
| Idea | Options API (VUE3G p.5) | Composition API with `<script setup>` (VUE3G p.6) |
|---|---|---|
| component declaration | `export default { ... }` in `<script>` | `<script setup>` with imports and top-level variables |
| reactive state | `data() { return { count: 0 } }` | `const count = ref(0)` |
| read/change in the script | `this.count++` | `count.value++` |
| function that changes state | `methods: { increment() { ... } }` | `function increment() { ... }` |
| hook on mount | `mounted() { ... }` | `onMounted(() => { ... })` (imported from `'vue'`) |
| template | `<button @click="increment">Count is: {{ count }}</button>` | the **same** template |

Everything else (props, emits, computed, watch, slots, provide/inject, composables) **does not appear** in the texts for the Composition API: **NOT COVERED**. For the Vue 2 Options API, `computed`/`watch`/`props` exist in the VUEHB (04, 02), but the handbook does not say they apply unchanged to Vue 3.

## Decision rules for the agent
1. Question "which one to use?" -> apply the VUE3G p.7 recommendation (build tools + complexity + learning or production goal).
2. Question about `computed`/`watch`/`props` in the Composition API -> NOT COVERED; give the Options equivalent from the VUEHB (Vue 2) and label `[extrapolation]` if you state anything about Vue 3.
3. Never say that one of the styles is "obsolete": the VUE3G says the opposite (p.6: both capable).
4. Script: `python -I scripts/vue_compare.py` (table, detection of a file's style, recommendation).
