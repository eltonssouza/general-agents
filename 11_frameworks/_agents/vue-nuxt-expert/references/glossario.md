# Glossary (terms as they appear in the sources)

| Term | Meaning according to the sources | Where |
|---|---|---|
| Progressive framework | framework that adapts and grows with needs (script tag up to a full application) | VUEHB p.4-5; VUE3G p.3 |
| SFC (Single-File Component) | `.vue` file with logic, template and styles together | VUEHB p.12, 68; VUE3G p.3-4 |
| Interpolation | `{{ }}` in the template content; one expression; escapes HTML | VUEHB p.72-75 |
| Directive | `v-...` attribute in the template | VUEHB p.81 |
| `scoped` | `<style>` attribute that limits the CSS to the component | VUEHB p.14, 69; VUE3G p.4 |
| Prop | attribute for passing data from parent to child; one-way | VUEHB p.64, 95, 107 |
| Slot / named slot | injection point for parent content; named by `slot="x"` (handbook) | VUEHB p.102-104 |
| Filter | function applied with `\|` in the interpolation (Vue 2, handbook) | VUEHB p.104-106 |
| Computed | derived, cached property | VUEHB p.91-94 |
| Watcher | function fired when a property changes | VUEHB p.90-91 |
| Event bus | emit/listen to events on a common component (`$root`) | VUEHB p.109 |
| Vuex / store / mutation / getter | official state management (2018); only mutations change the state | VUEHB p.110-119 |
| Vue Router / `$router` / `$route` | official router; navigation object and current route | VUEHB p.120-122 |
| Route guard | function called at moments of navigation (`beforeEach`...) | VUEHB p.126-129 |
| Options API | logic as an options object, `this` = instance | VUE3G p.5 |
| Composition API | logic as imported functions; `<script setup>` | VUE3G p.5-6 |
| `<script setup>` | hint for compile-time transformation for the Composition API with less boilerplate | VUE3G p.5-6 |
| `ref` | creates reactive state; `.value` in the script | VUE3G p.1, 6 |
| `createApp` | app creation entry point in the Vue 3 example | VUE3G p.1 |
| Vue CLI | command-line utility for scaffolding (2018) | VUEHB p.10, 18-33 |
| Nuxt | full-stack framework on top of Vue.js | NUXT p.1 |
| Nitro | Nuxt's server engine | NUXT p.3 |
| SSR | server-side rendering; default in Nuxt; can be turned off with `ssr: false` | NUXT p.1-3 |
| Hybrid rendering | combination via `routeRules` | NUXT p.3 |
| `nuxt generate` | static rendering of the whole application | NUXT p.3 |
| Auto-imports | composables and components without explicit import | NUXT p.2 |
| `.output` | Nitro's universal output directory in production | NUXT p.3 |
| Module (Nuxt) | extension of features/integrations | NUXT p.4 |
