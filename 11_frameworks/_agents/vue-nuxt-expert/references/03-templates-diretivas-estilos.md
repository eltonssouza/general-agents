# 03 - Templates, interpolation, directives and styles (Vue 2, 2018) [DATED]

Source: VUEHB p.71-87. For what Vue 3 says about templates: VUE3G p.2 and 4 (file 06).

## Templates and interpolation (p.71-75)
- [from source] (VUEHB p.71) The template language is a **superset of HTML**: any HTML is a valid template; Vue adds interpolation and directives.
- [from source] (VUEHB p.72-73) `{{ name }}` reads the `data` property directly (not `this.data.name`), through an internal Vue binding. In an SFC, `data()` must be a regular function so as not to lose `this` (p.73).
- [from source] (VUEHB p.74) Inside the interpolation fits **a single JavaScript expression** (e.g. a ternary); globals such as `Math` and `Date` are accessible. It is recommended to avoid complex logic in the template: experiment there and then move it to a computed or method.
- [from source] (VUEHB p.75) The interpolated value is updated when the data properties it depends on change; `v-once` prevents this. The result is always **escaped**; for HTML use `v-html`.

## Styles and classes (p.75-80)
- [from source] (VUEHB p.75-76) Static inline style with `style`; dynamic with `:style` (shorthand for `v-bind:style`) receiving an object; hyphenated properties require quotes or the camelCase form (`textDecoration`); it also accepts a computed property.
- [from source] (VUEHB p.76-77) Classes: plain CSS with `class`; `<style lang="scss">` for SCSS; `:class="{underline: isUnderlined}"` binds the class to a boolean property.
- [from source] (VUEHB p.78-80) `:class` also accepts a string coming from data, an array (`[decoration, weight]`), an inline object, a combination (`[decoration, {weight: isBold}]`) and a computed property that returns an object (useful with many classes). In a computed you need `this.property`; in the template, you do not (p.80).
- [from source] (VUEHB p.80) CSS processed by Vue automatically receives vendor prefixes; the text relates this to "IE9+" browsers. [DATED]

## Directives (p.80-87)
Directives are attributes that start with `v-` (p.81).
| Directive | What the text says | Page |
|---|---|---|
| `v-text` | equivalent to interpolation (`<span v-text="name">`) | 81 |
| `v-once` | renders once, without updating | 81-82 |
| `v-html` | interprets HTML; interpolation escapes and this "protects from XSS" automatically; `v-html` does not escape | 82 |
| `v-bind` (`:`) | required on attributes; interpolation only works in the tag content | 82 |
| `v-model` | two-way binding on form fields (`input`, `select`) | 83 |
| expressions | any JS expression inside directives; ternary allowed | 83-84 |
| `v-if` / `v-else` / `v-else-if` | dedicated conditionals | 84 |
| `v-for` | list; `item in items`; with index `(todo, index) in todos`; combine with `v-bind` for item properties | 84-85 |
| `v-on` (`@`) | listens to a DOM event and calls a method; accepts parameters and a short expression (`counter = counter + 1`) | 85-86 |
| `v-show` | keeps the element in the DOM with `display: none` when false | 87 |
| modifiers | `.prevent`, `.stop`, `.capture`, `.self`, `.once`, `.passive` | 87, 102 |
| custom directives | they exist; the text only points to the official documentation | 87-88 |

- [from source] (VUEHB p.118) For a field that updates on every keystroke use `@input`; `@change` only fires when focus leaves the field.
- **The handbook does not mention `:key` in `v-for`.** Answer NOT COVERED about `key`; any guidance is `[extrapolation]`. (checked: p.84-85)

## Cautions the text supports
- Interpolation escapes; `v-html` does not: [inference] do not use `v-html` with untrusted content (the basis is p.82; the recommendation is a deduction).
- More than one expression in the interpolation: not allowed (p.74).
- Attribute with `{{ }}`: does not work; use `v-bind`/`:` (p.82).
- A form without `.prevent` reloads the page (p.87).
