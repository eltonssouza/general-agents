# 03. State across components: props, context and stores (SVHB p.21-28)

[DATED] handbook syntax (2019). `svelte/store` and the functions below are what the text shows; changes in later versions: NOT COVERED.

## Strategy 1: props and "lifting state up" (p.21-22)
- **[from source] (SVHB p.21-22)** when a component needs to share data with another, the state moves up to a common ancestor and comes back down through props to whoever needs it. The author considers this the best technique because it is simple.

## Strategy 2: context API (p.22-23)
- **[from source] (SVHB p.22)** when props are not practical (components very far apart in the tree), use the context API: `setContext('key', object)` and `getContext('key')`, both imported from `svelte`; it is used to communicate with **descendants** without passing props down.
- **[from source] (SVHB p.23)** `getContext` only retrieves the key **in the component that called `setContext` or in its descendants**. For communication between two different trees: stores.

## Strategy 3: stores (p.23-28)
- **[from source] (SVHB p.23-24)** import `writable` from `svelte/store`; `const username = writable('Guest')`. It can live in a `.js` file (e.g. `store.js`), since it is not a component; components import from there.
- **[from source] (SVHB p.24)** `username.set('new')` replaces the value; `username.update(existing => ...)` receives the current value in a callback.
- **[from source] (SVHB p.25)** `get(username)` (imported from `svelte/store`) reads the value once; prefixing with **`$`** (`$username`) creates a reactive variable: the component re-renders when the value changes. Svelte **reserves `$`** and prevents its use for anything that is not a store value (do not prefix DOM references with `$`). `username.subscribe(new => ...)` is used to run logic on every change.
- **[from source] (SVHB p.26-27)** **readable stores** have no external `set()` or `update()`: `readable(0)`; an optional function after the initial value receives `set` and updates the store on its own (examples with `setTimeout` and `setInterval`). Usage in the component: `{$count}`.
- **[from source] (SVHB p.27-28)** **derived stores**: `derived(username, $username => `Welcome ${$username}`)`; the first argument is the existing store, the second is the function that receives its value. Usage: `{$username} {$welcomeMessage}`.
- NOT COVERED: custom stores, `readonly`, stores with objects/arrays, persistence, SSR with stores.

## Rules the linter applies (see `scripts/svelte_lint.py --rules`)
`SVL-S01` (user-declared $, p.25), `SVL-S02` ($x without x, p.25), `SVL-ST01` (set/update on readable, p.26), `SVL-ST02` (missing `svelte/store` import, p.23).
