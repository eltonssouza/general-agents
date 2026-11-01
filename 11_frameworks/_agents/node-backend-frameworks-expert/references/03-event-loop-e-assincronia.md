# 03 — Event loop, timers, callbacks, promises, async/await, EventEmitter

Source: NODEHB (6/9/2018). Pages = PDF. The figures on p.90-96 (call stack and iterations) have no text; they were rendered and only show the sequence `foo()`, `console.log('foo')`, `bar()`, `console.log('bar')`, `baz()`, `console.log('baz')` as iterations.

## Event loop (NODEHB p.85-98)
- **[from source]** JavaScript code runs on **a single thread**: one thing at a time; this simplifies programming, but requires **not blocking** (synchronous network calls, infinite loops) (p.86).
- **[from source]** Code that takes long to return control to the event loop blocks all JavaScript (and the UI, in the browser). Almost all I/O primitives are non-blocking; being blocking is the exception — hence callbacks, promises and async/await (p.86-87).
- **[from source]** The **call stack** is LIFO; the loop checks the stack on each iteration and runs whatever is there (p.87-93). The `foo → bar → baz` example prints foo, bar, baz (p.88-89).
- **[from source]** `setTimeout(fn, 0)` defers `fn` until after everything on the stack: the example prints `foo`, `baz`, `bar` (p.93-94). When the timer expires, the callback goes to the **message queue** (the same one that receives click events, keyboard events, fetch responses); the loop gives priority to the stack and only then takes items from the queue (p.97). The waiting time happens "elsewhere", in environment threads (p.97).
- **[from source]** **Job queue (ES6)**: used by Promises; the result runs right after the current function, before the message queue items. The example prints `foo`, `baz`, the promise message, `bar` (p.97-98). The text's analogy: regular line vs fast pass.

## process.nextTick and setImmediate (NODEHB p.99-100)
- **[from source]** Each full turn of the loop is a "tick". `process.nextTick(fn)` runs `fn` at the end of the current operation, **before the next tick**; always before `setTimeout` and `setImmediate` (p.99-100).
- **[from source]** `setImmediate(fn)` runs on the next iteration; `setTimeout(fn, 0)` is very similar, and the order between them "depends on several factors" (p.100).

## Timers (NODEHB p.100-105)
`setTimeout(fn, ms, ...args)` returns an id for `clearTimeout` (p.101-102); delay 0 = "as soon as possible, after the current function" (p.102); `setInterval` + `clearInterval` (p.102-103). **[from source]** `setInterval` does not consider when the function finished: long runs can overlap; solution: **recursive setTimeout** (p.104-105). `setImmediate` is standard in Node (p.102, p.105). Note: the recursive setTimeout snippet on p.105 is incomplete/noisy in the capture.

## Callbacks (NODEHB p.105-110)
- **[from source]** JS is synchronous by default and single-threaded (p.105-106). Callback = a function passed as a value, called when the event occurs (p.107-108).
- **[from source]** Node convention: **error-first** — the first parameter is the error (`null` if there is no error) (p.109). Example `fs.readFile('/file.json', (err, data) => { if (err !== null) ... })`.
- **[from source]** Problem: each callback adds a nesting level (p.110). Alternatives: Promises (ES6) and async/await (ES8) (p.110).

## Promises (NODEHB p.110-118)
- **[from source]** A promise = a proxy for a value that will become available; it starts **pending**, ends resolved or rejected (p.111). Standardized in ES2015; superseded in use by async functions in ES2017, but still the foundation (p.111).
- **[from source]** Created with `new Promise((resolve, reject) => ...)` (p.112). Consumed with `.then(...)` and `.catch(...)` (p.112-113).
- **[from source]** Chaining: example with `fetch` (`status` → `json` → data); if a step rejects, control goes to the **nearest `catch`** below, skipping the intermediate `then`s (p.113-115). Errors can be thrown inside `catch` and handled by another `catch` ("cascade") (p.115-116).
- **[from source]** `Promise.all([...])` waits for all and delivers an array; `Promise.race([...])` runs the callback **once**, with the first one resolved (p.116-118).
- **[from source]** Common error "Uncaught TypeError: undefined is not a promise": use `new Promise()`, not `Promise()` (p.118).

## Async/await (NODEHB p.118-123)
- **[from source]** ES2017; a combination of promises and generators, a higher-level abstraction over promises; **it is built on promises** (p.118). Reduces boilerplate and the "don't break the chain" limitation (p.118-119).
- **[from source]** An `async` function **always returns a promise**; `await` only inside an `async` function and pauses the calling code until the promise resolves/rejects (p.119-121). Example: "Before / After / I did something (after 3 s)" (p.120).
- **[from source]** Comparison of the same flow (`fetch` of users) with promises and with await: the second is more readable (p.121-122); chaining async functions in series is simple (p.122-123); debugging is easier because the debugger treats it as synchronous code (p.123).

## EventEmitter (NODEHB p.123-125 and p.173-178)
- **[from source]** `events` module: `const EventEmitter = require('events')`; `on` registers a callback, `emit` fires it; `addListener` is an alias of `on` (p.124-125). Extra arguments of `emit` go to the handler (p.125). `once`, `removeListener`/`off`, `removeAllListeners` (p.125, p.176-177).
- **[from source]** Reference (p.173-178): events `newListener`/`removeListener`; `emit` calls the listeners **synchronously in registration order** (p.174); `getMaxListeners` defaults to **10**, adjustable via `setMaxListeners` (p.175, p.177-178); `off` was added in **Node 10** (p.176); `prependListener`/`prependOnceListener` (p.176-177); `eventNames`, `listenerCount`, `listeners` (p.174-175).

Related: `05-fs-path-os-events-streams.md` (streams use events), `casos-e-antipadroes.md`. Linter: NODE-ERR-FIRST, NODE-PROMISE-NEW, NODE-SETINTERVAL-ASYNC, NODE-SYNC-HANDLER.
