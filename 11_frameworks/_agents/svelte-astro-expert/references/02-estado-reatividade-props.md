# 02. State, reactivity and props (SVHB p.14-21)

[DATED] handbook syntax (2019, pre-runes). Whether these patterns are the recommended ones today: NOT COVERED.

## Local state (p.14-16)
- **[from source] (SVHB p.14)** state is any data the component needs in order to render (e.g. the text of an input); it is defined in `<script>`: `let count = 0`.
- **[from source] (SVHB p.14-15)** to update it, a plain JavaScript **assignment** is enough: `count = count + 1` or `count++`. The example uses `on:click={incrementCount}` on a button. The text contrasts this with React (`useState()` and a setter) and calls the syntax more "JavaScript-like".
- **[from source] (SVHB p.15)** golden rule: **an assignment is needed when changing the value**, otherwise Svelte may not notice the change. For strings and numbers (immutable) this is natural.
- **[from source] (SVHB p.15-16)** for arrays, methods that mutate the array in place (`push()`, `pop()`, `shift()`, `splice()`...) are **not** detected because there is no assignment. Ways out: reassign afterwards (`list.push(4); list = list`, which the text calls a "quirk") or avoid the problem with spread: `list = [...list, 4]`.
- **[inference]** the text lists four methods and an ellipsis; treating `unshift/sort/reverse` the same way is an analogy (the linter flags it as `SVL-A02`, info).

## Reactivity with `$:` (p.16-19)
- **[from source] (SVHB p.16-17)** the special syntax `$:` defines a block that Svelte **re-runs when any variable referenced in it changes**. Example: `$: console.log(`${count}`)`.
- **[from source] (SVHB p.18)** there can be several `$:`; a block with braces `{}` groups several statements.
- **[from source] (SVHB p.18-19)** the block can update other variables (e.g. `double = count * 2` inside the `$:`).
- NOT COVERED: execution order of the blocks, hidden dependencies, modern equivalent.

## Props (p.19-21)
- **[from source] (SVHB p.19)** importing a component: `import SignupForm from './SignupForm.svelte'`, relative path (`./` same folder, `../` goes up). It is used as a tag; a parent/child relationship is formed. Props work like HTML attributes and are **one-way communication** (parent -> child).
- **[from source] (SVHB p.20)** pass `disabled="{true}"`; in the child, `export let disabled` exposes the prop to the parent. A variable can be passed; `{disabled}` is shorthand for `disabled={disabled}`.
- **[from source] (SVHB p.21)** when the parent's variable changes (example with `setTimeout`), the child receives the new value.
- Two-way: `bind:` on a component prop (see `04-slots-lifecycle-bindings.md`, SVHB p.38-39).
- NOT COVERED: default values beyond `export let disabled`, prop validation, rest/spread props.
