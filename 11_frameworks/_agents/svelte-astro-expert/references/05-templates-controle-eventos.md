# 05. Template flow control and events (SVHB p.39-49)

[DATED] handbook syntax (2019).

## `{#if}` (p.39-42)
- **[from source] (SVHB p.39-40)** `{#if isRed}...{/if}`: the block appears when the condition is **truthy** (empty string and 0 are falsy; `true` is truthy).
- **[from source] (SVHB p.40-41)** `{:else}` for the opposite case; any JavaScript expression works (including `!isRed`); `{:else if other}` chains conditions.
- **[from source] (SVHB p.41-42)** there can be several blocks and nesting.

## `{#each}` (p.42-44)
- **[from source] (SVHB p.42)** `{#each dogs as dog}<li>{dog}</li>{/each}`; index with `{#each dogs as dog, index}` (starts at 0).
- **[from source] (SVHB p.43-44)** when **editing lists dynamically (adding/removing)**, always pass an **identifier** (key) in parentheses: `{#each dogs as dog (dog)}`, `{#each dogs as dog, index (dog.id)}`. If each item has a unique id, use it (better than the whole object).

## `{#await}` (p.44-45)
- **[from source] (SVHB p.44)** handles promises directly in the template, with different UI for the states: pending, resolved, rejected. `{#await fetchImage}` (pending), `{:then data}` (resolved).
- **[from source] (SVHB p.45)** `{:catch error}` handles rejection. The text's example fetches an image with `fetch` (sample data; it is the example's network call, not something the agent runs).

## DOM events (p.45-47)
- **[from source] (SVHB p.45-46)** `on:<event>` in the template: `on:click`, `on:mousemove`; the handler can be inline or defined in `<script>`; it receives the event object as an argument (p.46). The author prefers inline when the code is 2-3 lines.
- **[from source] (SVHB p.47)** **modifiers**: `on:click|stopPropagation|preventDefault={fn}`; the two most used are `stopPropagation` and `preventDefault`; others: `capture`, `once`, `self`.

## Custom events (p.47-49)
- **[from source] (SVHB p.47-48)** import `createEventDispatcher` from `svelte`; `const dispatch = createEventDispatcher()`; `dispatch('eventName')`; the consumer listens with `on:eventName={...}`.
- **[from source] (SVHB p.48-49)** the second argument of `dispatch` (value or object) is available in the event object.
- NOT COVERED: event forwarding (`on:click` without a handler), events on components with forwarding, event syntax of later versions (the linter only flags `onclick=` as `SVL-EV02`, info).

## Rules the linter applies
`SVL-E01` (each without key, p.43), `SVL-AW01` (await without catch, p.45), `SVL-EV01` (submit without preventDefault, p.47), `SVL-D01` (dispatch without `createEventDispatcher`, p.47-48).
