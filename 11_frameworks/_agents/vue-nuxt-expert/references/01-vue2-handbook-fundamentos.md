# 01 - Fundamentals in the handbook (Vue 2, July 2018) [DATED]

Source: VUEHB p.2-17. Everything here comes from a 2018 article about what the text calls "Vue"; the version is Vue 2 by inference (INDEX §2).

## Overview and positioning (p.2-7)
- [from source] (VUEHB p.2) The author describes Vue as a popular front-end framework, "simple, small (~24KB)" and performant. [DATED] size and numbers from 2018.
- [from source] (VUEHB p.3) A framework abstracts the interaction with the browser and the DOM: instead of manipulating elements by reference, the developer defines them declaratively. The text places React, Angular and Vue as the "second wave" of frameworks.
- [from source] (VUEHB p.4) Popularity cited: more than 100 thousand GitHub stars in June 2018 and ~350 thousand weekly npm downloads. [DATED]
- [from source] (VUEHB p.4-5) Vue is "progressive": it can enter an app with a simple `script` tag and grow to manage the whole view layer; it does not require knowing webpack/Babel/npm to get started.
- [from source] (VUEHB p.6) Author's comparison: Vue took part of its template syntax from Angular (AngularJS) without the opinionated stack; from React it took the Virtual DOM, with automatic dependency management that re-renders only the components affected by the state change. The text states that, in React, child components re-render by default and `shouldComponentUpdate` is needed. **Author's opinion in 2018**, it measures nothing.
- [from source] (VUEHB p.6-7) JSX is possible but rarely used; HTML templates are the common path. `vue-router` and `vuex` are official packages maintained by the core. Vue is an "indie" project, with no corporation behind it (p.7).

## First app, no build (p.8-9)
- [from source] (VUEHB p.8) An HTML page with `<div id="example">{{ hello }}</div>`, the tag `<script src="https://unpkg.com/vue">` and `new Vue({ el: '#example', data: { hello: 'Hello World!' } })` shows "Hello World!". Scripts go at the end of `body` so they run after the DOM.
- [from source] (VUEHB p.8-9) `el` is a CSS selector (or `HTMLElement`); `data` is the object with what Vue should render; `{{ }}` marks the dynamic part of the template.

## Default Vue CLI app (p.10-17)
- [from source] (VUEHB p.10) Two paths: `vue create <name>` locally or CodeSandbox (nothing to install).
- [from source] (VUEHB p.11) Initial structure cited: `index.html`, `src/App.vue`, `src/main.js`, `src/assets/logo.png`, `src/components/HelloWorld.vue` (besides `package.json`). `index.html` only has `<div id="app">`.
- [from source] (VUEHB p.12) `main.js` imports `Vue` and `App`, sets `Vue.config.productionTip = false` (suppresses the development-mode tip) and creates `new Vue({ el: '#app', components: { App }, template: '<App/>' })`.
- [from source] (VUEHB p.12-14) `App.vue` is a Single File Component with three blocks (HTML, JS, CSS); it imports `HelloWorld` and registers it in `components`. The CSS of `App.vue` is not `scoped`.
- [from source] (VUEHB p.14-15) `HelloWorld.vue` has `<style scoped>`; scoped CSS receives a class applied transparently by Vue and does not leak. The message comes from `data` and appears as `{{ msg }}`: inside the template you use `msg`, not `data.msg`.
- Truncation: part of the code on these pages is incomplete in the capture (INDEX §3).

## Usage notes for the agent
- For "how do I start a Vue project?" the handbook answers with Vue CLI 3 (file 09). The VUE3G (Vue 3) does **not** mention Vue CLI; it only says that "Vue will handle all the build tools setup" (VUE3G p.4). Do not state which scaffolding tool is the current one: NOT COVERED (see 06/10 for what each source says).
