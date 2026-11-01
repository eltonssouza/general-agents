# Cases and antipatterns supported by the texts

| # | Antipattern / pitfall | Why (source) | Fix according to the text |
|---|---|---|---|
| 1 | `data: () => ({ ... })` when `this` is needed | an arrow does not bind `this` to the component; the text says a regular function is mandatory in those cases (VUEHB p.71, 73) | `data() { return {...} }` |
| 2 | computed/method with an arrow using `this` | same reason (VUEHB p.92, 106) | regular function |
| 3 | `this.data.name` | raises an error; use `this.name` (VUEHB p.89-90) | `this.name` |
| 4 | Two expressions in one interpolation | only one is allowed (VUEHB p.74) | move to computed/method |
| 5 | `href="{{ url }}"` | interpolation does not work in attributes (VUEHB p.82) | `:href="url"` |
| 6 | `v-html` with user text | interpolation escapes (XSS protection), `v-html` does not (VUEHB p.82); the restriction is [inference] | normal interpolation or trusted content |
| 7 | Mutating a prop inside the child | props are one-way (VUEHB p.107) | emit an event to the parent |
| 8 | `Date.now()` in computed | only updates with a reactive source; renders once (VUEHB p.93-94) | method |
| 9 | `watch` for several properties | only one property per watcher (VUEHB p.95) | computed (listens to several) |
| 10 | `next` not called in `beforeEach` | execution hangs (VUEHB p.128) | always call `next()` |
| 11 | Changing Vuex state directly | only mutations change the state (VUEHB p.116) | `commit` |
| 12 | `$route.params` scattered across the component | coupling to the router; use `props: true` (VUEHB p.131) | route props |
| 13 | Expecting `beforeRouteEnter` when only the parameter changes | the component is reused and calls `beforeRouteUpdate` (VUEHB p.130) | handle in `beforeRouteUpdate` |
| 14 | Form without `.prevent` | the page reloads (VUEHB p.87) | `@submit.prevent` |
| 15 | `.vue` without a build | handbook: does not work without Webpack (VUEHB p.68); VUE3G: SFC is for projects with a build (p.3-4) | Options API/CDN or set up a build |
| 16 | Using `@change` to react to every keystroke | only fires on losing focus (VUEHB p.118) | `@input` |
| 17 | Forgetting `.value` on a `ref` in the Composition API script | the VUE3G example uses `count.value++` in the script, `count` in the template (VUE3G p.6); the rule is [inference] | use `.value` in the script |
| 18 | Treating Vue 2 and Vue 3 as equivalent without checking | the collection has no migration guide; Vue 2 support ended on 12/31/2023 (VUE3G p.1) | consult the migration guide (outside the collection) |
| 19 | Saying Nuxt 4 does not do SSR by default | SSR is the default (NUXT p.1-2) | `ssr: false` disables it (NUXT p.3) |
| 20 | Stating what `useFetch`/`useAsyncData` do | the page only mentions "data-fetching utilities" (NUXT p.2) | NOT COVERED |
