# 05 - Vuex and Vue Router in the handbook (Vue 2, 2018) [DATED]

Source: VUEHB p.110-133. The VUE3G (Vue 3) **does not mention** Vuex or Vue Router; the collection does not say which versions of these packages accompany Vue 3 (NOT COVERED). Handbook code is partially truncated (INDEX §3).

## Vuex (p.110-120)
- [from source] (VUEHB p.110) Vuex is the official state-management library: it shares data between components. Without it, the text's means are props, events and `$root` as a bus. Centralizing state in a **store** is the option when that gets complex.
- [from source] (VUEHB p.110-111) Advantage pointed out: being official and integrated; it follows the Flux pattern popularized by Redux. Components can keep local state even with Vuex. You need Vuex when you spend a lot of work passing state around; it brings extra complexity.
- [from source] (VUEHB p.112) Installation: `npm install vuex` or `yarn add vuex` (or "Add dependency" in CodeSandbox).
- [from source] (VUEHB p.113-114) Store in `src/store/store.js` (suggestion): `Vue.use(Vuex)` and `export const store = new Vuex.Store({})`.
- [from source] (VUEHB p.115-116) Example: two sibling components (`Form` and `Display`); `state: { flavor: '' }`.
- [from source] (VUEHB p.116) **State is only changed by mutations.**
- [from source] (VUEHB p.117) **Getters** expose the state (they receive `state`); the store is registered in `main.js` with `import { store } from './store/store'` and `new Vue({ el, store, ... })`; this way `this.$store` points to the store in every component (p.117-119).
- [from source] (VUEHB p.118-119) Update with `this.$store.commit('change', value)`: mutation name and payload (second parameter of the mutation). Read: `$store.getters.flavor` in the template.
- [from source] (VUEHB p.119) Concepts that the text says are **missing**: actions, modules, helpers, plugins (it points to the official documentation). NOT COVERED in the collection.

## Vue Router (p.120-133)
- [from source] (VUEHB p.120) A router syncs the view with the URL; official, but Vue does not force its use.
- [from source] (VUEHB p.121) Package `vue-router` (`npm install vue-router` or a tag via unpkg); `Vue.use(VueRouter)` after importing Vue.
- [from source] (VUEHB p.122) With the router installed: `this.$router` (object) and `this.$route` (current route). Navigation: `push()` (adds to history), `replace()` (does not add) and `go(n)` (negative goes back) (p.122-123).
- [from source] (VUEHB p.123) `router-link` (attribute `to`) renders an `a` by default and receives the class `router-link-active`; `router-view` is where the route's component goes.
- [from source] (VUEHB p.124-125) `new VueRouter({ routes: [{ path, component }, ...] })`; the instance goes in `new Vue({ router })`; with `name` on the route we have a **named route**.
- [from source] (VUEHB p.126) `push({ name: 'post', params: { post_slug: ... } })` with a named route. On navigation, the new component is instantiated, its guards called and the old one destroyed.
- [from source] (VUEHB p.127-128) Global guards: `beforeEach`, `beforeResolve`, `afterEach`; in `beforeEach` the `next` parameter with `false` blocks navigation and **must always be called**, otherwise execution hangs. Component guards: `beforeRouteEnter`, `beforeRouteUpdate`, `beforeRouteLeave`.
- [from source] (VUEHB p.128-129) Order of checks cited: current `beforeRouteLeave` -> global `beforeEach` -> `beforeRouteUpdate` where there is reuse -> route `beforeEnter` -> new `beforeRouteEnter` -> `beforeResolve` -> navigation confirmed -> `afterEach`. The text suggests using component guards as lifecycle hooks to start data fetching (p.129).
- [from source] (VUEHB p.129-130) Dynamic routes: segment `:post_slug`; value in `$route.params.post_slug`; several segments allowed (`/post/:author/:post_slug`); Vue **reuses** the component instance and calls `beforeRouteUpdate`.
- [from source] (VUEHB p.131) To avoid coupling the component to the router: `props: true` on the route and `props: ['post_slug']` in the component.
- [from source] (VUEHB p.131-133) Nested routes: a second `router-view` inside the parent component (e.g. `Author` containing `Post`), configured in the route definition itself.
- Inconsistency in the capture: in the snippets `Vue.use(Router)` appears with a different name from the `VueRouter` import (p.124, 132). Treat it as a typo in the text, not as a rule.

## NOT COVERED (do not answer as if it were in the collection)
Pinia; Vuex 4; Vue Router 4 / `createRouter` / `useRouter` / `useRoute`; route lazy loading; history modes (hash/history); Nuxt pages <-> router (NUXT p.1 only says "file-based routes in `app/pages/`").
