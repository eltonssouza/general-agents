# 04. Slots, lifecycle and bindings (SVHB p.28-39)

[DATED] handbook syntax (2019).

## Slots (p.28-30)
- **[from source] (SVHB p.28)** slots allow composing components (or, seen from the other side, configuring the imported component). Defined with `<slot />` or `<slot></slot>`; in `Button.svelte`: `<button><slot /></button>`.
- **[from source] (SVHB p.29)** for those coming from React, it is the equivalent of `{props.children}`. Whoever imports places the content between the component's opening and closing tags. There can be **default content** inside the `<slot>` when the slot is not filled.
- **[from source] (SVHB p.29-30)** several slots are told apart by **name**: `<slot name="before" />`; the single unnamed slot is the default one. In use: `<p slot="before">...</p>`.
- **[inference]** the usage examples on p.29-30 write lowercase `<button>` where, to use the imported component, the logic calls for `<Button>`; treat it as an error in the example and do not copy it.
- NOT COVERED: props on slots (slot props), `$$slots`.

## Lifecycle events (p.30-32)
- **[from source] (SVHB p.30-31)** `onMount` (after rendering), `onDestroy` (after destroying), `beforeUpdate` (before updating the DOM), `afterUpdate` (after). They are not available by default: `import { onMount, onDestroy, beforeUpdate, afterUpdate } from 'svelte'`.
- **[from source] (SVHB p.31)** common use of `onMount`: fetching data from other sources. `onDestroy`: cleaning up whatever was started (timers, `setInterval`).
- **[from source] (SVHB p.32)** the function **returned** by `onMount` plays the role of `onDestroy`; example with a `setInterval` created on mount and `clearInterval` in the returned function. (The text's example uses `onMount(async () => ...)`; how other versions handle an async `onMount` with a function return: NOT COVERED, linter rule `SVL-L03` as `[extrapolation]`.)
- NOT COVERED: `tick`, order between parent and child hooks, SSR.

## Bindings (p.32-39)
- **[from source] (SVHB p.33)** `bind:value` creates a **two-way** binding between a state variable and a form field (very useful in forms). The variable must be `let`/`var`, **not `const`**. It works on inputs of several types, `textarea` and `select`.
- **[from source] (SVHB p.34-35)** checkbox/radio: `bind:checked`, `bind:group`, `bind:indeterminate`. `bind:group` associates an **array** with a set of checkboxes and fills it according to the choices (example `goodDogs`).
- **[from source] (SVHB p.35-37)** `select` with `bind:value`; if the `option`s come from an array of objects, the selected value is **the object**, not a string; with `multiple`, the variable is an array.
- **[from source] (SVHB p.37)** `bind:files` (input file), `bind:open` (details), media properties (`currentTime`, `duration`, `paused`, `buffered`, `seekable`, `played`, `volume`, `playbackRate`), `textContent`/`innerHTML` on `contenteditable`.
- **[from source] (SVHB p.37-38)** read-only: `offsetWidth`, `offsetHeight`, `clientWidth`, `clientHeight` on block elements (not void or inline).
- **[from source] (SVHB p.38)** `bind:this={variable}` gives a reference to the DOM element; useful after mounting (for example inside `onMount()`).
- **[from source] (SVHB p.38-39)** `bind:` on **component props**: `<Car bind:inMovement={carInMovement} />` binds the `inMovement` prop exported by the child (`export let inMovement = false`) to the parent's variable.
- NOT COVERED: bindings in `each` with nested objects, `bind:` on components with stores.
