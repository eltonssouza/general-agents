# 04 - Reactivity, methods, computed and watch (Vue 2, 2018; Vue 3 in 06) [DATED]

Source: VUEHB p.88-95 (Vue 2 Options API) and VUE3G p.2, 6 (reactivity and `ref` in Vue 3).

## What the sources say about "reactivity"
- [from source] (VUEHB p.75) The interpolation is updated when any `data` property it depends on changes; `v-once` turns it off.
- [from source] (VUEHB p.6) Vue tracks dependencies automatically and re-renders only the affected components (author's comparison with React).
- [from source] (VUE3G p.2) Reactivity: Vue tracks changes in JavaScript state and updates the DOM efficiently. Declarative rendering: the template describes the HTML output from the state.
- [from source] (VUE3G p.6) In the Composition API, `ref(0)` creates reactive state; in the script you access `count.value`; in the template you use `count` directly.
- [from source] (VUE3G p.7) The Composition API requires understanding how reactivity works; the Options API "abstracts away the details of reactivity".
- **NOT COVERED:** how the tracking is implemented (getters/setters, Proxy), reactivity limitations on arrays/objects, `reactive`, Composition API `computed`/`watch`.

## Methods (p.88-90)
- [from source] (VUEHB p.88) A method is a function associated with the instance, declared in `methods`; typical for `v-on` handlers.
- [from source] (VUEHB p.88-89) It accepts parameters passed in the template and accesses data through `this.property`. `this.data.name` raises an error (p.89-90).

## Watchers (p.90-91)
- [from source] (VUEHB p.90-91) `watch` observes **one** state property and runs a function when it changes; the function receives the new and old value (in that order). They cannot be queried in the template like computed properties.

## Computed (p.91-94)
- [from source] (VUEHB p.91-92) Interpolation only admits one expression and the template should handle display; computed serves for more than one expression and more declarative templates. You do not write `{{ count() }}`: Vue invokes the function. Use a regular function (not an arrow) to have `this`.
- [from source] (VUEHB p.93) Difference from methods: methods must be called; **computed is cached** until the property it depends on changes.
- [from source] (VUEHB p.93-94) Computed only updates when a reactive source changes. `Date.now()` in a computed renders once and does not update; for that the text points to a method.

## When to use what (p.94-95)
| Use | When (according to the text) |
|---|---|
| **method** | react to a DOM event; call a function when something happens; can be called from computed/watch (p.94) |
| **computed** | compose new data from existing data; template variable formed by one or more properties; shorten a nested name; value referenced in the template (cache); listen to changes in more than one property (p.94-95) |
| **watch** | act when a piece of data changes; listen to a prop change; only one specific property (not several); observe until a certain value is reached (p.95) |

## Supported pitfalls
- `Date.now()`/non-reactive values inside computed (p.93-94).
- Arrow function in computed/methods when `this` is used (p.92, 106).
- Mutating a prop in the child (p.107).
- Expecting watch to accept several properties (p.95).
