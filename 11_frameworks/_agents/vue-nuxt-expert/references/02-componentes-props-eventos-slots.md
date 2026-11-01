# 02 - Components, props, events, slots, filters and communication (Vue 2, 2018) [DATED]

Source: VUEHB p.62-71 and 95-110. Vue 2 syntax (`Vue.component`, `new Vue`, `slot=`, filters). For what Vue 3 shows, see 06 and 08.

## Ways to define components (p.62-67)
- [from source] (VUEHB p.62-63) Four ways: `new Vue({ ... })`, `Vue.component('name', { ... })`, **local** components and `.vue` files (SFC).
- [from source] (VUEHB p.63) `new Vue` / `Vue.component` are the default way when Vue is used in parts of pages (form, cart) or with a server-rendered layout; in an SPA the SFC is more common.
- [from source] (VUEHB p.63) `new Vue({ el: '#app' })` mounts on the DOM; a component created this way has no tag name and is usually the main container.
- [from source] (VUEHB p.64) `Vue.component('user-name', { props: ['name'], template: ... })` defines a reusable tag; `props` is the attribute for passing data to children.
- [from source] (VUEHB p.64-65) The name can be kebab-case or PascalCase; Vue creates the alias in both directions. The text recommends PascalCase in JavaScript, kebab-case in the template.
- [from source] (VUEHB p.65-66) `Vue.component()` registers **globally**. For local registration: an object assigned to a variable and declared in `components: { Sidebar }`; JS modules (`import Sidebar from './Sidebar'`) are the suggested way.
- [from source] (VUEHB p.66) Each instance of a reused component is independent.
- [from source] (VUEHB p.66-67) Options cited: `el` (root only via `new Vue`), `props`, `template`, `data` (local state), `methods`, `computed`, `watch`.

## Single File Components (p.67-71)
- [from source] (VUEHB p.68) `.vue` groups JS logic, HTML template and CSS in one file. The text states that this depends on Webpack and that `.vue` **cannot be used without a Webpack configuration**, so it does not suit those who use Vue on a single page that is not an SPA. [DATED] holds for the 2018 ecosystem; the VUE3G only says that SFC is used "in projects with build tools" (VUE3G p.4).
- [from source] (VUEHB p.69) Preprocessors cited: TypeScript, SCSS, Sass, Less, PostCSS, Pug. Babel allows ES6-8 and modules; CSS Modules for scoping.
- [from source] (VUEHB p.69) Without `scoped` the CSS is global; with `<style scoped>` Vue adds a unique class and the CSS does not leak.
- [from source] (VUEHB p.70) The `src` attribute externalizes the script (`<script src="./hello.js">`) and also the CSS (according to the text).
- [from source] (VUEHB p.70-71) `data()` can be written as a method, `data: function()` or `data: () => ...`. The text says the arrow function is a problem when `this` is needed and that **a regular function is mandatory** in those cases; it also prefers ES Modules to `module.exports`.

## Props (p.95-99)
- [from source] (VUEHB p.95-96) Props are how the parent passes data to the child; the component declares them in `props` (array of names or object).
- [from source] (VUEHB p.96-97) Valid types listed: String, Number, Boolean, Array, Object, Date, Function, Symbol. A type mismatch raises a console warning **in development mode**. Multiple types: `[String, Number]`.
- [from source] (VUEHB p.97-98) `required: true`; `default` (value or function that returns the value); custom `validator`.
- [from source] (VUEHB p.98-99) Passing: `<ComponentName color="white" />` for a static value; `:color="color"` for a data property; a ternary is allowed inside the value.
- [from source] (VUEHB p.107) Props are one-way (parent -> child) and **a prop must never be mutated in the child**.

## Child -> parent events (p.99-102, 107-109)
- [from source] (VUEHB p.99-100) `v-on:click` or `@click`; with or without parentheses they are equivalent (`@click="handleClick"` = `@click="handleClick()"`); parameters can be passed in the template.
- [from source] (VUEHB p.101) `$event` gives access to the original event object, including combined with other arguments.
- [from source] (VUEHB p.101-102) Modifiers: `.prevent` (preventDefault), `.stop`, `.passive`, `.capture`, `.self`, `.once`; they can be chained in sequence.
- [from source] (VUEHB p.107-108) The child emits with `this.$emit(...)` and the parent listens with `v-on:eventName="handler"` on the child's tag; extra parameters reach the parent's handler.
- [from source] (VUEHB p.109) **Event bus:** emit on an accessible component, such as `this.$root`, and listen in `mounted`; a dedicated component is also possible. The text says to look at Vuex or third-party libraries when that is not enough (p.110). [DATED] Vue 2 pattern; the VUE3G does not cover it (NOT COVERED).

## Slots (p.102-104)
- [from source] (VUEHB p.102-103) `<slot></slot>` in the component's template receives the content placed between the component's tags; content inside the `<slot>` is the default if nothing is passed.
- [from source] (VUEHB p.103-104) Named slots: the content is targeted with the `slot="sidebar"` attribute on any tag; whatever is outside goes to the main slot. [DATED] Vue 2 syntax; the VUE3G does not show slots (NOT COVERED).

## Filters (p.104-106)
- [from source] (VUEHB p.104-105) Filters format the output without changing data: `{{ name | fallback }}`, defined in `filters: {}` (functions that receive a value and return another); they can be chained (`| fallback | capitalize`) and receive parameters (the first argument is always the interpolated value).
- [from source] (VUEHB p.106) Here the author uses an arrow function because the filter does not need `this`. He cites a package of ready-made filters (capitalize, uppercase, currency, pluralize etc.) without giving its name. [DATED]
- [extrapolation] The collection **does not say** whether filters exist or were removed in Vue 3; the VUE3G does not mention them. Answer NOT COVERED and point to the official migration guide (it is not in the collection).

## Communication between components: summary of the text (p.107-110)
Props (parent -> child), events (child -> parent), event bus on `$root` and, when "you outgrow this", Vuex (file 05).
