# Step-by-step procedures in JavaScript

This file collects working recipes: each one says when to use it, the steps, how to verify the result, the pitfalls, and where the information comes from (source and era). The sources are the Spec (ECMA-262, 17th edition, normative), the EJpt (*Eloquent JavaScript* in Portuguese, a modern edition that declares it uses "a versão 2024 do JavaScript" [the 2024 version of JavaScript], EJpt p.9) and the EJ1 (the English 1st edition, from 2007 and revised in 2013, **all [DATED]**). Pages are the PDF pages, not the printed ones. To locate a recipe, Grep for the section title (for example `## 6.` or `### 6.3`). Recipes that depend on the environment carry **[HOST]**. Where the EJ1 and the EJpt disagree, the Spec rules, the EJpt explains modern usage and the EJ1 serves only as historical context; the disagreements are collected in section 13.

## Contents

1. Debugging: console, strict mode, error types, reading messages and the stack
2. Testing and writing functions (with the EJpt exercises)
3. Arrays and objects: copying, mutation, sorting
4. Regular expressions: building, testing, groups, lookahead, replace
5. Converting and formatting dates
6. Asynchronous code: Promise, async/await, errors, parallelism, the event loop
7. ESM modules and NPM/CommonJS [HOST]
8. Node.js: fs, http, streams [HOST]
9. DOM and events [HOST]
10. fetch, HTTP and forms [HOST]
11. Canvas [HOST]
12. Book projects: what each one teaches
13. Disagreements between the sources
14. Source passages that must not be reproduced
15. Gaps

## Label convention

**[HOST]** is behavior defined by the environment (browser, Node, `console`, timers, `prompt`, `fetch`, DOM). **[DATED]** is what comes from the whole EJ1, from `with`, from Annex B or from what the source calls legacy. **[VERSION-DEPENDENT]** marks a feature that the source attributes to a given edition. **[inference]** and **[extrapolation]** are connections or knowledge that are not written in the sources. When the Spec does not date a feature, the text says "version not stated in the sources".

---

## 1. Debugging: console, strict mode, error types, reading messages and the stack

### 1.1 Understand what kind of problem it is

**When to use:** at the first sign of a wrong result, before touching the code.

**Steps:**
1. Classify the bug. The EJpt distinguishes confused thinking (harder to diagnose) from a mistake in translating the thinking into code (EJpt p.167).
2. Find out *when* JavaScript complains. A grammar violation raises an error immediately, before execution. Calling something that is not a function or reading a property of `undefined` only raises an error when the action is attempted. Nonsensical computation often just yields `NaN` or `undefined` and the program carries on, so the error shows up far from its origin or not at all (EJpt p.168).
3. If there is an unexpected `NaN`, look for an accidental type conversion: converting `"five"` or `undefined` to a number gives `NaN`, and `NaN` contaminates the following calculations (EJpt p.24).

**Verification:** you can say in one sentence which bad value was born where. The line pointed to by the message may be only the first place where a bad value, produced earlier, was misused (EJpt p.173).

**Pitfalls:** the language accepts absurdities such as `true * "monkey"` without protest (EJpt p.168). In the Spec, an *early error* is detected before any evaluation of the script; errors that are not early errors only appear when the construct executes, and an implementation may not promote a runtime error to an early error (Spec p.445).

**Source/era:** EJpt ch. 8 (modern); Spec p.445 (standard).

### 1.2 Enable strict mode

**When to use:** in any new file that is not a module or class, to turn silent failures into errors.

**Steps:**
1. Put the string `"use strict"` at the top of the file or in a function body (EJpt p.168). In the Spec the directive only counts if it is in the directive prologue (the initial statements that are just string literals) and is exactly `"use strict"` or `'use strict'`, with no escape or line continuation inside (Spec p.246–247).
2. Remember that code inside classes and modules is already strict automatically (EJpt p.169).
3. Run the code and read the new errors.

**What changes (EJpt p.168–170):**
- Assigning to an undeclared binding (forgetting `let`) throws `ReferenceError` instead of silently creating a global. This does not help if a binding of the same name is already visible: the value is overwritten without warning (EJpt p.169).
- `this` is `undefined` in a function called outside a method; outside strict mode, it points to the global scope object (EJpt p.169). The Spec confirms that in strict mode `this` is not coerced to an object, including in `apply`/`call` (Spec p.861).
- Calling a constructor without `new` no longer creates a global: it throws `TypeError` (the book quotes the message "Cannot set property 'name' of undefined", which varies by engine) (EJpt p.169–170). Constructors created with `class` always complain without `new`, even outside strict mode (EJpt p.170).
- Function parameters with duplicate names are forbidden (EJpt p.170; in the Spec it is a `SyntaxError`, Spec p.861).
- `with` is removed (EJpt p.170; in the Spec it is a `SyntaxError`, Spec p.861). **[DATED]**
- Other restrictions listed in Spec p.861: `delete` of a variable is a `SyntaxError`; writing to a non-writable property, to an accessor without a setter, or to a non-extensible object throws `TypeError`; `eval` and `arguments` cannot be an assignment target or a binding name; legacy octal literals are forbidden.

**Verification:** `"use strict"; undeclaredVar = 1;` throws `ReferenceError` (Spec p.861; the example is [extrapolation]).

**Pitfalls:** the EJpt concludes that `"use strict"` rarely hurts and may help (EJpt p.170). Words such as `let`, `static`, `yield`, `package` become reserved only in strict mode (Spec p.861).

**Source/era:** EJpt p.168–170; Spec p.246–247, p.861. The EJ1 does not cover strict mode in the pages read [DATED].

### 1.3 Use `console.log` strategically **[HOST]**

**When to use:** when the error message does not reveal the cause.

**Steps (EJpt p.173–174):**
1. Resist changing the code at random.
2. Form a theory about the cause.
3. Make observations to test the theory: print the suspect value at the start of the loop or function.
4. Fix the cause, not the symptom.

**Book example:** `numberToString(13)` printed garbage such as `1.5e-323`; printing `n` on each iteration showed 13, 1.3, 0.13, 0.013 and so on, because `n /= base` does not give an integer. The fix was `n = Math.floor(n / base)` (EJpt p.173–174).

**Pitfalls:** `console.log` accepts several arguments (`console.log("x is", x)`) (EJpt p.34). In the browser the output goes to the JS console (F12, or command-option-I on a Mac) and in Node to the terminal (EJpt p.34, p.459–460) **[HOST]**. The EJ1 console and functions such as `print` and `show` belonged to the book itself, not to the language (EJ1 p.17) **[DATED]**.

**Source/era:** EJpt p.34, p.173–174.

### 1.4 Pause with a breakpoint or `debugger` **[HOST]**

**Steps:** open the browser's developer tools, set a breakpoint on a line (details vary by browser) or write the keyword `debugger` in the code; when the tools are active, execution pauses and you inspect the bindings (EJpt p.174–175).

**Source/era:** EJpt p.174–175.

### 1.5 Read error types, messages and the stack

**When to use:** whenever an exception appears.

**Steps:**
1. Read the error type. Per the Spec: `RangeError` is a value outside the allowed range; `ReferenceError` is an invalid reference; `SyntaxError` is a parsing error; `TypeError` is an unsuccessful operation that does not fit the other types; `URIError` is incorrect use of the global URI functions; `EvalError` exists only for compatibility (Spec p.484). Example: `decodeURIComponent("%")` throws `URIError` (Spec p.456).
2. Read `message` and, if present, `stack`. `Error` objects have `message` and record the stack trace in `stack`, with the function where it occurred and who called it (EJpt p.178). In the Spec, `message` is a non-enumerable property and `new Error("failed", { cause: e })` installs `cause` (Spec p.482, p.487). A **[HOST]** detail: the format of `stack` and the exact text of messages vary by engine (the book warns about this when quoting messages, EJpt p.76, p.169–170).
3. Follow the stack from the bottom up to the first frame that is your code.
4. For stack overflow, the typical messages are "out of stack space" or "too much recursion" and the EJpt does not state the exception type (EJpt p.58; EJ1 p.37). Look for recursion without a base case.
5. Reading a property of `null` or `undefined` throws an error (EJpt p.76; EJ1 p.44). So does destructuring those values (EJpt p.98).

**Verification:** you know whether the error is yours (logic), the environment's (external data) or one of language usage.

**Pitfalls:**
- An uncaught exception is handled by the environment **[HOST]**: in the browser the description goes to the console; in Node the whole process is aborted (EJpt p.180–181).
- An unhandled promise rejection is also detected and reported by the environment, via a host hook (EJpt p.245; Spec p.768).
- Exceptions thrown inside EJ1 event callbacks could not be caught by the book's console: a handler that "does not work" may be aborting due to an error (EJ1 p.211) **[DATED]**.

**Source/era:** Spec p.456, p.482–487; EJpt p.58, p.76, p.98, p.178, p.180–181, p.245.

### 1.6 Throw and catch with care (try/catch/finally, selective catching)

**When to use:** when designing how errors propagate.

**Steps:**
1. For an error that the caller must consider explicitly and that is common, a special return value (`null`, `undefined`, `-1`) is enough (EJpt p.175–176). Limits: if the function can already return any value, the result must be wrapped (like the iterator's `{done, value}`), and ten calls require ten checks (EJpt p.176; EJ1 p.70).
2. Otherwise, `throw` an `Error` (any value can be thrown). The exception unwinds the stack to the nearest `catch`; intermediate functions can ignore the matter (EJpt p.176–178).
3. Use `finally` for cleanup that must happen either way. It runs when the `try` throws but does not suppress the exception (EJpt p.179–180). Book example: give the money back to the account if the failure occurred between withdrawing and depositing (EJpt p.180).
4. Catch selectively: JavaScript does not filter by type in `catch`, so test `e instanceof MyError` and rethrow (`throw e`) the rest. Comparing `message` is fragile (EJpt p.181–183). Define `class InputError extends Error {}` to have a type of your own (EJpt p.182–183).
5. Use internal assertions only for easy-to-make mistakes, for example throwing if `firstElement([])`; not for every bad input (EJpt p.183–184).

**Verification:** deliberately reintroduce a typo (the book uses `promtDirection`) and check that the undefined-binding error appears instead of being swallowed (EJpt p.181–183).

**Pitfalls:** catching everything indiscriminately buries the real cause (EJpt p.181–182). Reordering operations or computing new values instead of mutating data reduces the damage of an exception in the middle (EJpt p.179). Throwing a string is a bad idea because it makes the type hard to recognize (EJ1 p.75) **[DATED]**.

**Source/era:** EJpt p.175–184 (modern); EJ1 p.68–75 (dated, same concept, no `class`).

---

## 2. Testing and writing functions (with the EJpt exercises)

### 2.1 Write a pure function first

**When to use:** whenever the result can be expressed as a value.

**Steps:**
1. Choose the form: function expression (`const f = function(x) {...}`), declaration (`function f(x) {...}`) or arrow (`x => x * x`) (EJpt p.51, p.55–56, p.69). An arrow with a one-expression body, without braces, already returns that expression; with braces a `return` is needed (EJpt p.56). Arrow functions were added in 2015 according to the book **[VERSION-DEPENDENT]** (EJpt p.56). An arrow has no `this` of its own (EJpt p.128).
2. Avoid side effects and dependence on external state. A pure function is testable in isolation, and a call can be replaced by its return value (EJpt p.68). There is no need to avoid all impure ones: `console.log` has no pure version (EJpt p.69).
3. If the function returns an object literal in a shorthand arrow, wrap it in parentheses: `n => ({prop: n})`, since a leading `{` is read as a block (EJpt p.79).
4. Optional parameters: extra arguments are ignored and missing ones become `undefined`; use a default value `function f(n, step = 1)` (applies when the argument is missing or `undefined`) (EJpt p.58–59). For a variable number use `...rest` (EJpt p.94).
5. To create a function: extract repeated code, or name a function that does not exist yet and write the body afterwards. Difficulty naming indicates an unclear concept; prefer functions that do a single concept (`zeroPad` instead of `printZeroPaddedWithLabel`) (EJpt p.65–67).
6. Write something correct and simple first; measure before optimizing (the recursive version of `power` costs about three times a loop, EJpt p.62; in the EJ1 it was about ten times, EJ1 p.36 **[DATED]**).

**Pitfalls:**
- Function declarations are "hoisted": they can be used above the definition, in the same scope (EJpt p.55). The text states this only for declarations.
- Scope: `let`/`const` have block scope; `var` respects only function scope (EJpt p.52–53) **[DATED]**. In the EJ1 blocks do not create scope and `let` appears only as a future feature (EJ1 p.34).
- Closures: the function sees the environment in which it was created, not that of the call (EJpt p.60–61).
- Stack overflow in infinite recursion (EJpt p.58).

**Source/era:** EJpt ch. 3 (p.50–71); EJ1 ch. 3 (p.30–41) [DATED].

### 2.2 Write simple automated tests

**When to use:** when a manual check starts to repeat.

**Steps:**
1. Reduce the code to functions that receive values and return values; the fewer external objects, the easier to test (EJpt p.172–173).
2. Write a mini-test with a label: `test(label, body)` prints `Failed: <label>` when `body()` returns false (EJpt p.172). The book's example tests `toUpperCase` with Latin, Greek and Arabic, which has no uppercase (EJpt p.172).
3. When the repetition becomes annoying, adopt a *test runner*, which provides functions to express tests and useful information on failures (EJpt p.172). Which runner to use is not stated in the sources.
4. Run the suite after every change to catch regressions (EJpt p.171–172).

**Source/era:** EJpt p.171–173. The EJ1 recommends testing pure functions directly in the console (EJ1 p.32) [DATED].

### 2.3 Solve the EJpt exercises (map of what each one trains)

Use the table to choose exercises and check the concept. Solutions and hints are on the book's website; the "Display hints..." button in the text is interface noise (EJpt p.47–48).

| Exercise | What it trains | Page |
|---|---|---|
| Triangle with a loop | `for`, string `.length`, concatenation | EJpt p.47–48 |
| FizzBuzz | `%`, `if`/`else if`, order of conditions (multiple of 3 and 5 last or first) | EJpt p.48 |
| 8x8 chessboard | nested loops, `\n`, then parameterizing `size` | EJpt p.48–49 |
| Recursive `isEven` | base cases 0 and 1, N − 2; what happens with −1 is a question from the book | EJpt p.70–71 |
| `range`, `sum` (optional step, including negative) | arrays, `push`, `sum(range(1,10))` gives 55 | EJpt p.100–101 |
| `reverseArray`, `reverseArrayInPlace` | copying versus mutation | EJpt p.101–102 |
| Linked list `{value, rest}` | nested objects, recursion (`nth`) | EJpt p.102–104 |
| `deepEqual` | `===`, recursion, `typeof null` is `"object"`, `Object.keys` | EJpt p.104 |
| Flattening, `loop`, `every`, `dominantDirection` | `reduce`+`concat`, higher-order functions | EJpt p.122–124 |
| `compareRobots`, `PGroup` | measuring with equal tasks; persistent structure | EJpt p.164–166 |
| `reliableMultiply`, locked box | selective catching, `finally` | EJpt p.185–187 |
| Regexp golf, quoting style, numbers again | regex (section 4); visual tool debuggex.com **[HOST/external]**; `verify(regexp, yes, no)` | EJpt p.215–218 |
| Quiet Times, Real Promises, `Promise_all` | `async`/`await`, `Promise.all`, single promise state (section 6) | EJpt p.260–263 |
| Content negotiation, a JavaScript workbench, Conway's Game of Life | `Accept` header in `fetch`; `Function` constructor (risk: EJpt p.228); rules applied to the whole generation | EJpt p.427–429 |
| DOM and canvas exercises (table, `byTagName`, balloon, mouse trail, tabs, shapes, pie chart, bouncing ball) | sections 9 and 11 | EJpt p.314–317, p.338–340, p.397–400 |

**Procedure for any exercise:** write the solution, run it with the examples from the statement, compare with the solution on the website and only then consider the exercise understood (EJpt p.9; EJ1 p.6).

**Source/era:** EJpt, pages in the table.

---

## 3. Arrays and objects: copying, mutation, sorting

### 3.1 Create, read and update objects

**Steps:**
1. Create with `{name: value}`. Names that are not valid identifiers need quotes in the literal and brackets on access (EJpt p.78–79, p.76).
2. Read with `obj.x` (literal name) or `obj[expr]` (the expression is evaluated and converted to a string) (EJpt p.76).
3. Assigning to an existing property replaces it; a nonexistent one is created. Reading a nonexistent property gives `undefined` (EJpt p.78–79).
4. `delete obj.x` removes the property; `"x" in obj` reports whether it exists. Assigning `undefined` keeps the property (`in` gives `true`) (EJpt p.79–80).
5. `Object.keys(obj)` lists own names; `Object.hasOwn(obj, name)` ignores the prototype (EJpt p.80, p.138).
6. Shorthand: `{events, squirrel}` is equivalent to `{events: events, squirrel: squirrel}` (EJpt p.83). Dynamic name: `{[expr]: value}` (EJpt p.142, p.425).
7. Optional access: `a?.b`, `a?.[0]`, `f?.()` return `undefined` if the base is `null`/`undefined` (EJpt p.98). Version not stated in the sources.

**Pitfall of braces `{`:** at the start of a statement they open a block; in other positions they describe an object (EJpt p.79).

**Source/era:** EJpt ch. 4; EJ1 p.43–46 (`delete`, `in`, `for (var x in obj)`) [DATED].

### 3.2 Understand mutation and identity

**Rule:** numbers, strings and booleans are immutable; objects (including arrays) are mutable (EJpt p.81). `==` between objects compares identity: two distinct objects with the same properties are different, and there is no built-in deep comparison (EJpt p.82). `const` prevents reassigning the binding, but does not prevent changing the object's contents (EJpt p.82).

**Verification:** ask "do two bindings point to the same object?". If so, a change through one shows up in the other (EJpt p.81–82).

**Source/era:** EJpt p.81–82; EJ1 p.46 (same concept) [DATED].

### 3.3 Copy without mutating the original

**When to use:** when updating state, avoiding side effects, or when other code holds the same reference.

**Steps:**
1. Array: `slice()` with no arguments copies the whole array (EJpt p.91, p.434). `concat` returns a new array and treats a non-array argument as a one-element array (EJpt p.91–92). Spread `[...a, x]` also copies (EJpt p.94).
2. Remove index `i` without mutating: `a.slice(0, i).concat(a.slice(i + 1))` (EJpt p.91).
3. Object: `{...old, y: 5}` copies the properties and, if one is repeated, the last value wins (EJpt p.95). With a dynamic name: `{...state.notes, [selected]: value}` (EJpt p.425). `Object.assign(target, source)` **mutates** the target (EJpt p.80).
4. State update: `{...state, ...action}` (EJpt p.435).
5. To lock an existing object there is `Object.freeze`, but the EJpt prefers convention, since a silently ignored write is as confusing as an error (EJpt p.157). In the Spec, `freeze` applies the FROZEN level, returns the argument without error if it is not an object, and throws `TypeError` if it fails (Spec p.463).

**Pitfalls:** these copies are shallow; nested objects remain shared [inference from EJpt p.81–82]. Deep copy is not in the sources read (see Gaps). `Object.assign` and spread copy only what the object itself has [inference]; do not confuse with prototype inheritance (EJpt p.129–130).

**Source/era:** EJpt p.80, p.91–95, p.157, p.425, p.434–435; Spec p.463.

### 3.4 Sort

**When to use:** when you need an order different from the original.

**Steps:**
1. Know that `sort` sorts **the array itself** and returns it (Spec p.636). To avoid mutating, copy first (`[...a].sort(...)`, [inference] from EJpt p.94 and Spec p.636) or use `toSorted`, the non-mutating version (Spec p.641; version not stated in the sources).
2. **Without a comparator, the order is by string**: `[10, 9, 1].sort()` puts 10 before 9 (Spec p.638). For numbers pass `(a, b) => a - b` (the example from the Spec's own note, p.638).
3. With a comparator, the return is converted with `ToNumber` and `NaN` becomes 0, that is, a tie (Spec p.638).
4. The sort is **stable**: equal items keep their relative order (Spec p.638). `undefined` values go to the end, then the holes, without calling the comparator (Spec p.637–638).
5. An inconsistent comparator (variable result, non-numeric return, one that alters the array) leaves the final order implementation-defined (Spec p.637–638). If the comparator throws, the sort stops and the error propagates (Spec p.637).
6. For strings, comparison with `<` uses the Unicode codes from left to right; uppercase comes before lowercase and it is not dictionary order (EJpt p.21; EJ1 p.13).

**Verification:** test with numbers of different sizes (10, 9, 1), with duplicates and with `undefined`.

**Source/era:** Spec p.636–641; EJpt p.21. The EJpt and the EJ1 have no `sort` recipe; the rule comes only from the Spec.

### 3.5 Iterate, transform and combine

**Steps:**
1. Iterate: `for (let x of array)` works with arrays, strings and other iterables (EJpt p.87, p.100). `forEach` is the function version (EJpt p.111). The EJ1 enumerates with `for (var x in obj)` over property names (EJ1 p.53–54) **[DATED]**.
2. Filter: `filter(test)` returns a new array with the elements for which `test` is true (EJpt p.112–113).
3. Transform: `map(f)` returns a new array of the same length (EJpt p.113). The word "map" also names the key-value structure (EJpt p.136).
4. Reduce: `reduce(combine, initial)`; the initial value may be omitted if the array has at least one element (EJpt p.114–115). An empty array without an initial value is not handled in the sources read (see Gaps). In the Spec, `forEach`, `map`, `reduce` and similar only visit existing indices and skip holes, whereas `includes` and `find*` read holes as `undefined` (Spec p.625, p.628).
5. Search: `includes`, `indexOf` (returns `-1` if not found), `lastIndexOf`, `find` (first element or `undefined`), `some`, `every` (`every([])` is `true`) (EJpt p.86, p.90–91, p.118, p.120, p.123).
6. Compose in a pipeline (filter, extract, average). Cost: intermediate arrays; for huge arrays processed many times the imperative loop may pay off (EJpt p.116–117).
7. Flatten: `reduce` + `concat` (EJpt p.122); the Spec also defines `flatMap` (one level) (Spec p.627).
8. Mutate on purpose: `push`/`pop` at the end, `unshift`/`shift` at the start (queues); `reverseArrayInPlace` is the fast mutating version of `reverseArray`, but the pure one is more useful (EJpt p.77, p.90, p.101–102); `splice` removes and inserts in the same array (Spec p.638–639).
9. Map with arbitrary keys: a plain object inherits from `Object.prototype` (`"toString" in obj` is `true`); use `Object.create(null)`, `Map` (`set`, `get`, `has`) or `Object.hasOwn` (EJpt p.136–138). In the EJ1 the defense was `hasOwnProperty` (EJ1 p.129–131) **[DATED]**.

**Pitfalls:** `childNodes` and DOM collections are not real arrays; use `Array.from` (EJpt p.297, p.302). Strings: `length` and `[i]` count 16-bit code units; emoji take two (EJpt p.118–119); `for...of` on a string iterates over real characters and `codePointAt` gives the code point (EJpt p.119).

**Source/era:** EJpt ch. 4–5. The EJ1 equivalents (`forEach`, `map`, `reduce`, `filter` reimplemented by hand) are in EJ1 p.77–82, p.109–110 [DATED]; the EJ1 does not state whether these methods existed natively (EJ1 p.77).

---

## 4. Regular expressions: building, testing, groups, lookahead, replace

### 4.1 Build a regex

**When to use:** to describe patterns in text (validation, extraction, replacement).

**Steps:**
1. Literal form `/abc/` or constructor `new RegExp("abc", "gi")` (EJpt p.189, p.206).
2. In the literal, write `\/` for a slash; backslashes that do not form special codes (such as `\n`) are preserved and change the meaning (EJpt p.189). Characters with special meaning become literal with `\`: `/A\+/` (EJpt p.189).
3. In the constructor, the regex comes from an ordinary string, so double the backslashes: `"\\s"` (EJpt p.206; EJ1 p.183–184).
4. To build the regex from user text, escape first: `name.replace(/[\\[.+*?(){|^$]/g, "\\$&")` (EJpt p.207). The set listed in the book does not include `]` or `}` [inference].
5. Options go after the final slash or in the 2nd argument: `i` ignores case, `g` global, `y` sticky, `u` Unicode (EJpt p.214). The Spec accepts the flags `d g i m s u v y`; any other letter or a repetition is a `SyntaxError`, and `u` and `v` together too (Spec p.598–599). `d`, `m`, `s`, `v` do not appear in the EJpt (version not stated in the sources).

**Pitfalls:** without `^` and `$` a pattern matches at any position: `getDate` would extract dates from "100-1-30000" (EJpt p.198). Omitting the anchors produces code that almost always works, with a hard-to-find bug (EJpt p.212).

**Source/era:** EJpt p.189–215; EJ1 p.177–184 [DATED] (same basic syntax); Spec p.598–599.

### 4.2 Test and find positions

**Steps:**
1. `regex.test(string)` returns a boolean and is true if there is a match at any position (EJpt p.190).
2. `string.search(regex)` returns the index of the first match or `-1`, like `indexOf` with a regex, but without a start offset (EJpt p.207).
3. `regex.exec(string)` returns `null` or an array-like object with the match at index 0 and the `index` property (EJpt p.195). `string.match(regex)` without `g` behaves similarly; with `g` it returns only the matched strings (EJpt p.196, p.209).
4. For all matches with details use `matchAll`, which requires the `g` flag and is iterated with `for...of`; each item has `match[0]` and `match.index` (EJpt p.209–210). In the Spec, `matchAll` creates a new regexp and returns an iterator (Spec p.604).

**Pitfalls:** the EJpt describes `matchAll` as "um array de arrays" [an array of arrays] on p.210, but the example iterates it with `for...of`; treat it as iterable (see section 13).

**Source/era:** EJpt p.190–210; EJ1 p.177–181 (`search`, `test`, `match`) [DATED].

### 4.3 Sets, shortcuts, repetition and alternation

**Steps:**
1. Set `[abc]`, range `[0-9]` (Unicode code order), negation `[^01]`; inside a set `.` and `+` lose their special meaning (EJpt p.190–192).
2. Shortcuts: `\d` digit, `\w` "word character", `\s` whitespace, `.` any character except newline; `\D \W \S` negate (EJpt p.191). In the Spec, without `s`, `.` excludes line terminators; the `s` flag (dotAll) makes `.` match them (Spec p.583). For any character including newline, the EJpt uses `[^]` (EJpt p.205).
3. Repetition: `+` (one or more), `*` (zero or more), `?` (optional), `{4}`, `{2,4}`, `{5,}` (EJpt p.193–194).
4. A group `( )` treats a fragment as a unit for the following operators; `boo+(hoo+)+` illustrates the reach of each `+` (EJpt p.195).
5. Alternation `|`; parentheses limit its reach: `/\d+ (pig|cow|chicken)s?/` (EJpt p.199–200).
6. International text: `\w` covers only the 26 Latin letters, digits and underscore; `é` and `β` do not match. `\s` recognizes all Unicode spaces. With the `u` option, `\p{L}` (letter), `\p{N}`, `\p{P}`, `\P{L}` (inverse) and `\p{Script=Greek}` work (EJpt p.192–193). Use `\d` for numbers that will be converted, since `Number` does not convert digits of other systems (EJpt p.193).

**Verification:** `/neighbou?r/` matches "neighbour" and "neighbor"; `/\p{L}/u.test("α")` is true (EJpt p.193–194).

**Pitfalls:** without `u`, `.`, `?` and `{n}` act on code units: `/🍎{3}/.test("🍎🍎🍎")` is false and `/<.>/.test("<🌹>")` is false; with `u` both give true (EJpt p.212–213). The EJ1 states that `{,4}` means four or fewer (EJ1 p.179); the EJpt lists only `{n}`, `{n,m}` and `{n,}` (EJpt p.194) **[DATED]**, see section 13.

**Source/era:** EJpt p.190–200, p.212–214; EJ1 p.177–180 [DATED].

### 4.4 Anchors, boundaries and lookahead

**Steps:**
1. `^` start and `$` end of input: `/^\d+$/` requires a string of only digits (EJpt p.198–199). `\b` is a word boundary and uses the simplistic `\w`, so it is unreliable outside English (EJpt p.199).
2. Positive lookahead `(?=...)` and negative `(?!...)` impose a condition without consuming characters: `/a(?=e)/.exec("braeburn")` gives `["a"]` (EJpt p.199).
3. The Spec also defines lookbehind `(?<=...)` and `(?<!...)` (Spec p.558, p.581), which the EJpt does not teach (version not stated in the sources). In Annex B (legacy syntax) **[DATED]**, lookahead can take a quantifier and lookbehind cannot (Spec p.845).

**Verification:** `/a(?! )/.exec("a b")` gives `null` (EJpt p.199).

**Source/era:** EJpt p.198–199; Spec p.558, p.581.

### 4.5 Capture groups, named and non-capturing

**Steps:**
1. The text of each parenthesized group appears in the array, in the order of the opening parenthesis: `/'([^']*)'/.exec("she said 'hello'")` gives `["'hello'", "hello"]` (EJpt p.196).
2. A group that did not participate gives `undefined` (`/bad(ly)?/.exec("bad")`); a repeated group keeps only the last capture; `(?:...)` groups without capturing (EJpt p.196).
3. To discard the whole match when destructuring: `const [_, month, day, year] = ...exec(text)` (EJpt p.198).
4. Named groups `(?<name>...)` become properties of `groups` in the result; without names, `groups` is `undefined` (Spec p.559, p.610–611). The EJpt does not cover them (version not stated in the sources). With the `d` flag, the result gains `indices` with the `[start, end]` pairs (Spec p.611).

**Pitfalls:** `exec` with a `g` or `y` regex uses and updates `lastIndex` (see 4.7).

**Source/era:** EJpt p.195–196, p.198; Spec p.559, p.610–611. The EJ1 uses `match` with groups in the same way (EJ1 p.180–181) [DATED].

### 4.6 Backtracking, greediness and performance

**Steps:**
1. Understand the engine: it tries to match from each position and returns the first match; when a branch fails, it goes back (backtracking) and tries the next; the first branch in written order wins (EJpt p.200–202).
2. Repetition is greedy: it matches as much as possible and backs off. Add `?` (`+?`, `*?`, `??`) for the minimum (EJpt p.205–206).
3. Guiding example: `/\/\/.*|\/\*[^]*\*\//g` on `"1 /* a */+/* b */ 1"` swallows the middle `+` and gives "1  1"; with `[^]*?` it gives "1 + 1" (EJpt p.205–206).
4. Avoid patterns that match the same stretch in many ways: `/([01]+)+b/` on a long run of 0s and 1s without `b` makes the work double with each character, and a few dozen characters are enough for the program to look stuck forever (EJpt p.202–203).

**Source/era:** EJpt p.200–206.

### 4.7 `lastIndex`, `g`, `y`

**Steps:**
1. `lastIndex` is only used when the regex has `g` or `y` **and** the search is done by `exec`; without them, `lastIndex` is treated as 0 (EJpt p.208; Spec p.610).
2. After a success, `exec` sets `lastIndex` right after the match; after a failure, it goes back to 0 (EJpt p.208).
3. `y` (sticky) only holds if the match starts exactly at `lastIndex`; `g` searches ahead: `/abc/g.exec("xyz abc")` matches, `/abc/y.exec("xyz abc")` gives `null` (EJpt p.208).

**Pitfall:** a global regex shared between calls carries residual `lastIndex`: `/\d/g` finds "1" in the first string and `null` in the second (EJpt p.209). Use global regexes only when needed (EJpt p.209).

**Source/era:** EJpt p.207–209; Spec p.610.

### 4.8 `replace`

**Steps:**
1. A string as the pattern replaces only the first occurrence: `"papa".replace("p", "m")` gives "mapa" (EJpt p.203). With a regex without `g` also only the first; with `g`, all (EJpt p.203; EJ1 p.181).
2. In the replacement string, `$1`..`$9` refer to groups and `$&` to the whole match: swapping "Surname, Name" for "Name Surname" with `/(\p{L}+), (\p{L}+)/gu` and `"$2 $1"` (EJpt p.203–204). Limit of 9 references in the EJ1 (EJ1 p.181).
3. Function as a replacement: it is called for each match with (whole match, groups...) and the return value goes in its place; the `minusOne` example decrements quantities and adjusts the plural (EJpt p.204; EJ1 p.181–182). In the Spec, after the groups come `position` and the string, and `groups` last, if there are names (Spec p.605).
4. A single `replace` with a regex and a function can replace several chained replacements, for example escaping `<>&"` at once (EJ1 p.182–183) **[DATED]**.

**Verification:** `"Borobudur".replace(/[ou]/g, "a")` gives "Barabadar" (EJpt p.203).

**Pitfalls:** `Number(amount)` is safe in the replacement only because the group matched `\d+` (EJpt p.204).

**Source/era:** EJpt p.203–204; Spec p.605; EJ1 p.181–183 [DATED].

**Applied example:** the INI file parser splits into lines with `split(/\r?\n/)` and tests each line, in order, with `match(/^(\w+)=(.*)$/)`, `match(/^\[(.*)\]$/)` and `/^\s*(;|$)/`, throwing an error on the rest; the `^` and `$` anchors avoid subtle bugs (EJpt p.210–212).

---

## 5. Converting and formatting dates

### 5.1 Create and read a date

**Steps:**
1. `new Date()` gives now; `Date.now()` or `new Date().getTime()` give milliseconds since 1970 in UTC (EJpt p.197–198; EJ1 p.57).
2. With components: `new Date(2009, 11, 9)` is December 9, 2009 — **month from 0 to 11**, day from 1; hour, minute, second and ms are optional and default to 0 (EJpt p.197; EJ1 p.56). In the Spec, with two or more arguments, the values are interpreted as **local time**, and excess months "wrap" into the next year (`month = 12` becomes January of the following year; day 0 becomes the last day of the previous month) (Spec p.518, p.522–523) [inference in the second part, from the formulas].
3. A numeric argument is read as milliseconds; a string argument goes through the same parser as `Date.parse` (Spec p.522; EJpt p.197).
4. Read with `getFullYear`, `getMonth` (0–11), `getDate`, `getDay` (day of the week, Sunday = 0), `getHours`, `getMinutes`, `getSeconds` (EJpt p.198, p.260; Spec p.524–526). `getYear` returns the year minus 1900 and the book considers it nearly useless **[DATED]** (EJpt p.198).
5. `Date.UTC(year, month, ...)` computes the timestamp in UTC, with default month 0 and default day 1 (Spec p.524).

**Verification:** `new Date(2009, 11, 9).getMonth()` must give 11.

**Pitfalls:** the classic mistake is forgetting that the month is 0-indexed (the book's `getDate` does `month - 1`, EJpt p.198). A year from 0 to 99 becomes 19xx with several arguments (Spec p.523). The output of `console.log` for dates depends on time zone and environment **[HOST]** (EJpt p.197).

**Source/era:** EJpt p.197–198; EJ1 p.56–58 [DATED]; Spec p.511, p.518, p.522–526.

### 5.2 Convert from text to date

**Steps:**
1. If the format is under your control, extract with a regex and build with the constructor: `/(\d{1,2})-(\d{1,2})-(\d{4})/.exec(text)` and `new Date(year, month - 1, day)` (EJpt p.198). Anchor with `^`/`$` (EJpt p.198).
2. The EJ1 does the same with `match` and throws `Error("No date found in ...")` if it does not match (EJ1 p.181) **[DATED]**.
3. For strings in a standard format, `Date.parse` and `new Date(string)` return the timestamp. Behavior outside the standard format is implementation-defined (Spec p.523). The Spec guarantees that `Date.parse(x.toString())`, `x.toUTCString()` and `x.toISOString()` reproduce `x.valueOf()` when ms = 0, but **not** `toLocaleString()` (Spec p.523–524).

**Pitfalls:** the invalid result is `NaN` as the time value; `toString` shows "Invalid Date" (Spec p.534).

**Source/era:** EJpt p.198; Spec p.522–524, p.534.

### 5.3 Format a date

**Steps:**
1. Standard and time zone change: `toISOString()` returns UTC in ISO format and throws `RangeError` if the date is invalid (Spec p.533). `toJSON()` returns `null` for an invalid date (this is what `JSON.stringify` uses) (Spec p.533).
2. Text for people: `toLocaleDateString`, `toLocaleString`, `toLocaleTimeString` return text in the environment's time zone and convention; if the `Intl` API (ECMA-402) exists, it defines the result; without it, it is implementation-defined **[HOST]** (Spec p.534).
3. Manual assembly: combine `getDate` etc. with `padStart(2, "0")` (`String(6).padStart(3, "0")` gives "006", EJpt p.93). The EJ1 uses its own `pad` function (EJ1 p.62–63) **[DATED]**.
4. Compare: `<` and `>` work; `==` between two equal Date objects gives `false`, so compare `getTime()` (EJ1 p.57; identity principle in EJpt p.82).
5. External packages (`format-date` with `require("ordinal")` etc.) appear only as a CommonJS example (EJpt p.226–227). The regex in that example, `M(MMM)?`, only accepts `M` or `MMMM`, and the tag `"M"` returns the month without adding 1; do not reproduce it (see section 14).

**Verification:** format a known date (for example `new Date(2017, 9, 13)`) and check the day, month and day of the week.

**Source/era:** Spec p.533–534; EJpt p.93, p.226–227; EJ1 p.57–58, p.62–63 [DATED].

---

## 6. Asynchronous code: Promise, async/await, errors, parallelism, the event loop

### 6.1 Decide the model

**Rule:** in the synchronous model, calling a slow function freezes the program; in the asynchronous one, the action is started, the program continues and is notified later, with the explicit waiting under the programmer's control (EJpt p.237–238). The browser and Node make slow operations asynchronous instead of using threads **[HOST]** (EJpt p.238).

**Verification:** does the operation involve network, disk or time? If so, do not use a synchronous API in a program that needs to respond (EJpt p.467).

**Source/era:** EJpt p.236–238.

### 6.2 Callbacks (original form)

**Steps:** pass a function that will be called at the end; `setTimeout(() => console.log("Tick"), 500)` is the example **[HOST]** (EJpt p.238–239). To sequence, nest the callbacks (EJpt p.239–240). In the Node/EJpt style the callback comes last and receives `(error, result)` (EJpt p.243, p.466).

**Pitfalls:** indentation grows with each step, loops become awkward, asynchronicity "infects" the calling functions and it is very hard to guarantee that failures reach the right callback (EJpt p.240, p.243).

**Source/era:** EJpt p.238–240, p.243. The EJ1 only uses callbacks and `onreadystatechange` (EJ1 p.233) [DATED]; the EJ1 has no Promise.

### 6.3 Create and consume Promises

**Steps:**
1. The Promise works like a receipt for a value that may not exist yet; `then(f)` registers the function for when there is a value and works even if the promise is already resolved (EJpt p.240).
2. `Promise.resolve(value)` wraps the value (returns the same promise if it already is one) (EJpt p.240–241; Spec p.777: it only reuses it if the constructor matches).
3. Wrapping a callback API: `new Promise((resolve, reject) => { ... })`; in the callback call `reject(error)` if there is an error, otherwise `resolve(value)` (EJpt p.241, p.244).
4. `then` returns another promise: it resolves with the value returned by the handler or with the result of the returned promise, which allows chaining (EJpt p.241–242). `then(JSON.parse)` is a useful synchronous step (EJpt p.242).
5. A promise changes state only once; extra calls to `resolve`/`reject` are ignored (EJpt p.247, p.262).

**Verification:** order: `Promise.resolve("Done").then(console.log); console.log("Me first!")` prints "Me first!" first (EJpt p.257–258).

**Source/era:** EJpt p.240–243; Spec p.777.

### 6.4 Handle errors in a chain

**Steps (EJpt p.243–245):**
1. A rejection carries a reason. Success handlers are ignored after a failure, and the rejection follows through the promise returned by `then`.
2. An exception thrown inside a handler rejects the promise of that `then`; `Promise.reject(x)` creates an already rejected one.
3. `catch(handler)` handles the rejection and returns a new promise: it resolves with the original value if there was no failure, or with the handler's return. `then(accept, reject)` is the shortcut.
4. A handler that does not match the outcome (success/failure) is skipped; the one that matches defines the next state.

**Verification:** book example: rejected, first `then` skipped, `catch` returns "nothing", the next `then` receives "nothing" (EJpt p.245).

**Pitfalls:** an unhandled rejection is reported by the environment **[HOST]** (EJpt p.245; Spec p.768). Distinguishing a timeout from a real failure by comparing the reason with the string "Timed out" depends on the reason being exactly that (EJpt p.248) [inference]. In `fetch`, an HTTP error does not reject the promise (see section 10.2).

**Source/era:** EJpt p.243–245; Spec p.768.

### 6.5 Use `async` and `await`

**When to use:** when the logic is linear (always waits for the previous step) and chains of `then` or recursion become verbose (EJpt p.249).

**Steps:**
1. Mark the function with `async` (also methods, `async name => {...}`) (EJpt p.250, p.258). It returns a promise resolved with the `return` and rejected if the body throws (EJpt p.250).
2. Inside it, `await promise` pauses until resolution. If the promise rejects, an exception is thrown **at the point of the `await`**, so a surrounding `try/catch` works (EJpt p.250).
3. Normal loops can contain `await`; the `crackPasscode` example uses two nested `for` loops, `try { await withTimeout(...) } catch` and `break` (EJpt p.249–250). With plain `then`, the loop required recursion (EJpt p.247–248).
4. In the Spec, `Await` converts the value with `PromiseResolve` and resumes the function with the value or by throwing the reason; the synchronous part of the function runs up to the first `await` [inference] (Spec p.798).
5. The EJpt compares the `async` function to a special kind of generator (EJpt p.252). The book does not say since which edition `async`/`await` exist (version not stated in the sources).

**Pitfalls:** the function does not execute more than once from start to finish; it may freeze at each `await` (EJpt p.250). Keep understanding promises, since you handle them directly (EJpt p.250).

**Source/era:** EJpt p.249–252, p.258; Spec p.795–798.

### 6.6 Run in parallel

**Steps:**
1. Fire all the operations without waiting for each one: a loop that calls `request` for each IP and keeps the promises (EJpt p.253). To swallow expected failures, `.catch(() => {})` (EJpt p.253).
2. `Promise.all(array)` returns a promise of an array of results in the same order; it rejects if any rejects (EJpt p.254–255; Spec p.771–772). The other promises keep running even after a rejection [inference] (Spec p.772). An empty array resolves with `[]` (Spec p.772).
3. Other combinators defined by the Spec (the EJpt does not teach them; version not stated): `Promise.allSettled` waits for all and returns `{status, value|reason}` (Spec p.773–774); `Promise.any` fulfills with the first fulfilled and rejects with `AggregateError` if all reject (Spec p.774–775); `Promise.race` copies the first to settle and never settles with an empty iterable (Spec p.776).
4. With `async`: `await Promise.all(files.map(async f => ...))` (EJpt p.258–259).
5. Timing: `const wait = time => new Promise(ok => setTimeout(ok, time))` wraps the timer **[HOST]** (EJpt p.255–256); `withTimeout(promise, ms)` forwards `promise.then(resolve, reject)` and schedules a `setTimeout` that rejects with `"Timed out"`, which works because a promise settles only once (EJpt p.247). For a steady pace, create the `wait` before sending the frame and wait for both [inference about the reason] (EJpt p.255–256).

**Verification:** measure the time: with N operations of similar duration, the total should be close to one, not to N added together (EJpt p.237–238).

**Source/era:** EJpt p.252–255, p.258–259; Spec p.771–776.

### 6.7 Understand the event loop and avoid concurrency bugs

**Rules (EJpt p.256–258):**
1. Each callback and the main script run to completion without interruption; only one program at a time; incoming events go into a queue. Slow code delays everything else **[HOST]**. The Spec formalizes this: a Job only runs when there is no running context, only one at a time per agent, and it runs to completion; browsers and Node give Promise Jobs higher priority than other work **[HOST]** (Spec p.186–187).
2. The callback runs on a call stack of its own; therefore `try/catch` around `setTimeout` does **not** catch an exception thrown inside the callback (EJpt p.256–257).
3. Promises resolve as a new event: the `then` of an already resolved promise runs after the current script finishes (EJpt p.257–258).
4. Example: with a 20 ms timeout, a `while` occupying 50 ms blocks the firing, and the printed times depend on the machine (EJpt p.257).

**Typical bug:** `list += name + await ...` inside `files.map(async ...)`. The `+=` reads the current value of `list` at the start and writes after the `await`, so each callback starts from an empty string and only one line survives. Fix: return the lines through `map`, use `await Promise.all(...)` and `join("\n")` (EJpt p.258–259). Lesson: computing new values is less error-prone than altering existing values (EJpt p.259).

**Verification:** at each `await`, ask "what could other code have changed here?" (EJpt p.258).

**Source/era:** EJpt p.256–259; Spec p.186–187. The EJ1 notes that two handlers never run at the same time, including those of `setTimeout` (EJ1 p.208) [DATED] **[HOST]**.

### 6.8 Generators

**Steps:** declare with `function*`; calling it returns an iterator; each `next()` executes up to a `yield` and delivers the value; the return ends it (EJpt p.250–251). `yield` is only valid directly in the generator body (EJpt p.251). Typical use: iterators, for example `Group.prototype[Symbol.iterator] = function*() {...}` (EJpt p.251).

**Verification:** `for (const n of powers(3))` with `break` on exceeding 50 prints 3, 9, 27 (EJpt p.250–251).

**Source/era:** EJpt p.250–251.

---

## 7. ESM modules and NPM/CommonJS [HOST]

### 7.1 Decide: script, ES module or CommonJS

**Rule:** since ECMAScript 2015 there are two kinds of program: **scripts**, whose bindings go to the global scope, and **modules**, with their own scope and `import`/`export` **[VERSION-DEPENDENT: ES2015, according to the EJpt]** (EJpt p.221). Original JavaScript had no modules and scripts shared the same global scope, with name conflicts (EJpt p.220–221). The EJpt states that there is no longer any reason to write new programs in CommonJS (EJpt p.229).

**Verification:** does the file use `import`/`export`? Then it is a module and is strict automatically (EJpt p.169).

**Source/era:** EJpt p.219–221, p.229; the EJ1 has no native modules and uses the immediately invoked anonymous function pattern with `provide` (EJ1 p.171–172) **[DATED]**.

### 7.2 Write and use ES modules

**Steps (EJpt p.221–223):**
1. Export before a function, class or binding: `export function dayName(...)`. What is not exported stays private (EJpt p.221).
2. Import: `import {dayName} from "./dayname.js"`; the module is identified by a string (EJpt p.221–222).
3. Rename with `as`: `import {dayName as nomDeJour} from ...` (EJpt p.222).
4. Single export: `export default ...`, imported **without braces** (`import seasonNames from "./seasonname.js"`) (EJpt p.222).
5. Namespace: `import * as dayName from "./dayname.js"` and use `dayName.dayName(3)` (EJpt p.223).
6. Keep `import`/`export` in the outer body of the module: they cannot be inside a function, loop or block, since they are resolved at load time (EJpt p.222).
7. Name resolution depends on the platform **[HOST]**: the browser treats it as a web address and Node as a file (EJpt p.222). In the browser use `<script type="module">` and relative URLs (EJpt p.289; version not stated).

**Verification:** when a module executes, all dependents (transitively) are loaded first and the exports become available (EJpt p.222).

**Pitfalls:** in the Spec, `export default function () {}` gives the anonymous function the `name` `"default"` [inference] (Spec p.445). Circular dependency: many systems forbid it, because no load order guarantees already-loaded dependencies (EJpt p.234).

**Source/era:** EJpt p.220–223; Spec ch. 16 (modules).

### 7.3 Read and write CommonJS

**When to use:** only to maintain or consume existing code.

**Steps (EJpt p.225–228):**
1. A CommonJS module is a script with two bindings: the function `require(name)` (loads and returns the interface) and the object `exports` (starts empty; add properties): `exports.formatDate = ...`.
2. Consume with `const {days, months} = require("date-names")`.
3. `require` is a normal function called during execution; it can be inside functions and accepts any expression that yields a string. `import` runs before the module and only accepts a string literal (EJpt p.228).
4. The book's simplified loader uses `require.cache` (created with `Object.create(null)`), reads the code, builds `Function("require, exports", code)` and calls it (EJpt p.227–228).
5. The pre-2015 pattern was the IIFE with the interface in a global, which isolates but does not declare dependencies (EJpt p.225–226) **[DATED]**.

**Pitfalls:** the `Function` constructor with external text is dangerous (whoever injects the string runs anything) (EJpt p.228). `readFile` does not exist in standard JavaScript; each environment provides its own **[HOST]** (EJpt p.228). Cycles in CommonJS work only in a restricted form: no module in the cycle may use the other's interface before it finishes loading (EJpt p.235). Mixing the two systems is awkward, since the native system coexists uncomfortably with CommonJS (EJpt p.233); in Node, ES modules can import from CommonJS (EJpt p.229).

**Source/era:** EJpt p.225–229, p.233–235. The EJ1 treats `require` only as the book's own function, which loads scripts (EJ1 p.169) **[DATED]**.

### 7.4 Use NPM packages **[HOST]**

**When to use:** to reuse distributable code (modules, dependencies and documentation) without copying it (EJpt p.223).

**Steps:**
1. Install: `npm install ini` downloads the package into `node_modules` in the current directory (**local** installation, per project) (EJpt p.462–463). Installing comes with Node (EJpt p.224, p.462).
2. Use: `import {parse} from "ini"` or, in the REPL, `const {parse} = require("ini")`; `parse("x = 10\ny = 20")` gives `{x: "10", y: "20"}` (values are strings) (EJpt p.225, p.463).
3. Register the dependencies in `package.json` (created by hand or with `npm init`): author, name, description, version, entry point (`main`), `dependencies` map and license (EJpt p.463–464). `npm install` without a name installs what is listed; installing a new package adds it (EJpt p.464).
4. Versions: NPM requires semantic versioning, three numbers (2.3.0); a compatible new feature raises the middle one, a breaking change raises the first. `^2.3.0` accepts from 2.3.0 up to before 3.0.0 (EJpt p.464–465). The third number is not explained in the text (EJpt p.464). For an exact version: `npm install mime-types@2.1.0` (EJpt p.474).
5. Publish with `npm publish` in a directory with `package.json`, using a name that is still free (EJpt p.465).
6. Check the license: by default the author retains the copyright; some licenses require the same license on derivatives, others only ask to keep the notice; the JavaScript community uses the latter more (EJpt p.224–225).

**Pitfalls:** NPM hosts thousands of packages of varying quality (over three million at the time of the book) (EJpt p.224). Packages may need compilation (for example TypeScript), bundling into a single file (bundler) and minification; the book does not detail these tools (EJpt p.229–230).

**Source/era:** EJpt p.223–225, p.229–230, p.462–465. The EJ1 does not cover NPM [DATED].

---

## 8. Node.js: fs, http, streams [HOST]

Everything in this section is **[HOST]**: Node is not part of the language. The EJpt requires Node 18 or higher (EJpt p.459).

### 8.1 Run scripts and read arguments

**Steps:**
1. `node hello.js` runs a file; `console.log` writes to standard output; `node` without a file opens the REPL (EJpt p.459–460).
2. `process.argv` is an array of strings with the `node` command and the script at positions 0 and 1, so the real arguments start at index 2; `process.exit(code)` ends with 0 for success (EJpt p.460–461).
3. There is no `document` or `prompt`; there are `Array`, `Math`, `JSON` (EJpt p.461).
4. ES modules in `.mjs`, with `import`/`export`; paths starting with `/`, `./` or `../` are files, `"node:fs"` is a built-in module, and bare names come from `node_modules` (EJpt p.461–462).

**Book example:** `node main.mjs JavaScript` prints "tpircSavaJ" using `Array.from(string).reverse().join("")` (EJpt p.462).

**Source/era:** EJpt p.458–462.

### 8.2 Read and write files (`node:fs`)

**Steps:**
1. Callbacks: `readFile(path, "utf8", (error, text) => ...)`; without an encoding the result is a `Buffer` (an array-like object of bytes) (EJpt p.465–466). `writeFile(path, data, callback)` writes a string in UTF-8 by default (EJpt p.466). There are also `readdir`, `stat`, `rename`, `unlink` (EJpt p.466).
2. Promises: import from `node:fs/promises` and use `readFile("file.txt","utf8").then(...)` or `await` (EJpt p.467).
3. Synchronous variants (`readFileSync`) block the whole program and are only for when asynchronicity gets in the way (EJpt p.467).
4. File streams: `createReadStream` and `createWriteStream` (EJpt p.469–470).
5. Node errors have cryptic `code`s such as `"ENOENT"` (file does not exist) (EJpt p.475).

**Verification:** handle `error` first in the callback. The pattern `if (error) throw error;` merely rethrows (EJpt p.465).

**Source/era:** EJpt p.465–467, p.475. The EJ1 does not cover Node [DATED].

### 8.3 HTTP server (`node:http`)

**Steps (EJpt p.467–469):**
1. `createServer((request, response) => {...})` and `server.listen(8000)`.
2. `request.url` carries the path; `request.method` the action.
3. `response.writeHead(status, headers)`, `response.write(...)` (can be called several times) and `response.end()`.
4. The process does not end by itself while it is listening; stop it with ctrl-C.
5. To make requests, `fetch` is global in Node and the author recommends it instead of `http.request` (EJpt p.469).

**Source/era:** EJpt p.467–469.

### 8.4 Streams: read with events and forward with `pipe`

**Steps:**
1. A writable stream has `write` and `end`; the `response` is one (EJpt p.469).
2. A readable stream (like `request`) emits `"data"` with a `Buffer` (decode with `toString()`, UTF-8) and `"end"`; event emitters have `on(name, function)` (EJpt p.469–470).
3. `from.pipe(to)` forwards everything and closes the output when done. Since `pipe` does not return a promise, wrap it: register `"error"` on both streams to reject and `"finish"` on the destination to resolve (EJpt p.476–477).

**Verification:** the example server returns the body in uppercase; a `fetch` POST with "Hello server" receives "HELLO SERVER" (EJpt p.470).

**Source/era:** EJpt p.469–470, p.476–477.

### 8.5 File server (complete procedure from ch. 20)

**Steps (EJpt p.470–477):**
1. Map GET (read), PUT (write), DELETE (remove) to the file at the request path, starting from the working directory.
2. Keep handlers in an object without a prototype (`methods`); each is `async` and returns `{body, status = 200, type = "text/plain"}`; if the method does not exist, use `notAllowed` (405). Errors with `status` go back as they are; others become 500.
3. If `body` has `pipe`, forward it; otherwise pass it to `response.end` (`body?.pipe`).
4. Protect the path (`urlPath`): create `new URL(request.url, "http://d")`, take `pathname`, apply `decodeURIComponent`, resolve with `resolve` from `node:path` starting at `process.cwd()` and require that the result start with the base directory + `sep`; otherwise throw `{status: 403, body: "Forbidden"}` (EJpt p.472–473). This prevents directory traversal with `../`.
5. GET: `stat`; `ENOENT` becomes 404; a directory returns `readdir` joined by line breaks; a file returns `createReadStream` and `type` from the `mime-types` package (`lookup`) (EJpt p.474–475).
6. DELETE: a missing file gives 204 (idempotence); a directory uses `rmdir`; a file uses `unlink` (EJpt p.475–476).
7. PUT: forward the body to `createWriteStream` with `pipeStream` and respond 204 (EJpt p.476–477).
8. Test with `curl` (`-X` method, `-d` body) (EJpt p.477).

**Pitfalls:** the code throws a plain object (not `Error`) with `status`, which the `catch` recognizes (EJpt p.471, p.473). When accepting network connections, think about security (EJpt p.473). The text says the command installs "uma versão específica de mime" [a specific version of mime], but the package is called `mime-types` (EJpt p.474).

**Exercises:** `grep`-style search with regex and files (recursive over directories), the `MKCOL` method with `mkdir`, and a "public space on the web" with a page editable through a form, working outside the exposed directory (EJpt p.478–480).

**Source/era:** EJpt p.470–480.

---

## 9. DOM and events [HOST]

Everything in this section is **[HOST]**. The EJ1 covers the same subject with the APIs and workarounds of its time (IE) **[DATED]**.

### 9.1 Document, HTML and `<script>`

**Steps:**
1. The browser parses the HTML and keeps a live data structure, the DOM; modifying it updates the screen (EJpt p.293). `document`, `document.documentElement`, `document.head` and `document.body` give access (EJpt p.295; EJ1 p.196).
2. `<script>` executes when the browser encounters it; always close with `</script>`, even with `src` (EJpt p.288–289). If the content needs the whole document, wait for the `"load"` event (EJpt p.333).
3. Event attributes such as `onclick` accept code; watch the quotes (EJpt p.289–290).

**Pitfalls:** the browser does not repaint or respond while a JS program runs; that is why animation loops use `requestAnimationFrame` (EJpt p.312). Keep `<!doctype html>`, `charset` and `html/head/body` in real documents (EJpt p.288).

**Source/era:** EJpt p.286–295; EJ1 p.196–197 [DATED].

### 9.2 Navigate and find nodes

**Steps:**
1. The DOM is a tree: `parentNode`, `childNodes` (only on elements), `firstChild`, `lastChild`, `previousSibling`, `nextSibling`, `children` (elements only) (EJpt p.298). `nodeType` 1 is an element, 3 text, 8 a comment (EJpt p.296); the EJ1 adds 9 for `document` (EJ1 p.197). `nodeName` comes in uppercase (EJpt p.316; EJ1 p.197).
2. Avoid fixed paths from `document.body`; whitespace creates text nodes (EJpt p.299). Prefer searches.
3. `getElementById`, `getElementsByTagName`, `getElementsByClassName` (EJpt p.299–300), and `querySelector` (first or `null`) and `querySelectorAll` (non-live `NodeList`) with CSS selectors (EJpt p.309–310).
4. **Live** collections (`getElementsByTagName`, `childNodes`) change with the document; for a stable loop copy with `Array.from` (EJpt p.302).
5. For the text of a text node use `nodeValue` (EJpt p.298–299).

**Verification:** `querySelectorAll("p > .animal")` counts only direct children (EJpt p.310).

**Pitfalls:** `NodeList` is not an array (no `slice` or `map`) (EJpt p.297). Removing nodes while traversing a live collection requires iterating backwards or copying first (EJpt p.302). The EJ1 keeps `$` as a shortcut for `getElementById` (EJ1 p.199) **[DATED]**.

**Source/era:** EJpt p.295–300, p.309–310.

### 9.3 Create, insert, move and remove nodes

**Steps (EJpt p.300–303):**
1. `document.createElement(tag)` and `document.createTextNode(text)`.
2. `appendChild(n)`, `insertBefore(new, reference)`, `replaceChild(new, old)` (the new one is the first argument) and `remove()`.
3. A node exists in one place only; inserting it again moves it.
4. Create a helper `elt(type, ...children)` to reduce repetition (EJpt p.302–303); the ch. 19 version applies `Object.assign(dom, props)`, that is, node **properties** (EJpt p.435–436), whereas the ch. 16 one uses `setAttribute` (EJpt p.352).
5. Attributes: many are properties of the same name; custom ones via `getAttribute`/`setAttribute`; prefix yours with `data-` (EJpt p.303). `class` is `className` as a property (EJpt p.304); `tabindex` is `tabIndex` (EJpt p.453).
6. Content replacement: the EJ1 uses `innerHTML` (interprets as HTML) and `nodeValue` (plain text) (EJ1 p.198–199) **[DATED]**.

**Verification:** moving the 3rd paragraph before the 1st gives Three/One/Two (EJpt p.301).

**Pitfalls:** the EJ1 warns that IE required `tbody` in tables created through the DOM and that `style` did not accept `setAttribute` in that browser (EJ1 p.200, p.203) **[DATED]**.

**Source/era:** EJpt p.300–304; EJ1 p.199–204 [DATED].

### 9.4 Style and layout

**Steps:**
1. `element.style.property = "value"`; hyphenated names become camelCase (`fontFamily`) (EJpt p.307–308). Numbers need a unit (`"px"`); only `0` is exempt (EJpt p.313; EJ1 p.206).
2. `display: none` hides without removing (EJpt p.307).
3. `position`: `static` (default), `relative`, `absolute` (out of the flow, relative to the nearest positioned ancestor or to the document) and `fixed` (does not scroll with the document) (EJpt p.311, p.331).
4. Measurements: `offsetWidth`/`offsetHeight` (total) and `clientWidth`/`clientHeight` (inner); `getBoundingClientRect()` gives `top`, `bottom`, `left`, `right` in the window; add `pageXOffset`/`pageYOffset` for document coordinates (EJpt p.304–305).
5. Style rules (CSS): selectors `.class`, `#id`, `p > a`, `p a`; the most specific rule wins and the `style` attribute has the highest precedence (EJpt p.308–309).

**Performance pitfall:** reading layout (`offsetHeight`, `getBoundingClientRect`) forces the computation; alternating layout reads and DOM changes in a loop is slow (32 ms against 1 ms in the 2,000 px example) (EJpt p.305–306).

**Source/era:** EJpt p.304–309, p.311–313.

### 9.5 Animate

**Steps:** use `requestAnimationFrame(f)`; `f` receives the time; compute the advance from the time difference (not a fixed step) and reschedule; `cancelAnimationFrame` cancels (EJpt p.311–312, p.335). For circular position: `Math.cos` for x and `Math.sin` for y, angle in radians (2π is the full turn) (EJpt p.312–313). The EJ1 uses `setInterval` every 100 ms for the same purpose (EJ1 p.206–207) **[DATED]**.

**Pitfall:** in hidden tabs the browser suspends `requestAnimationFrame`; limit the step (`Math.min(time - lastTime, 100) / 1000`) (EJpt p.366).

**Source/era:** EJpt p.311–313, p.335, p.366.

### 9.6 Register and remove event handlers

**Steps:**
1. `element.addEventListener("click", function)` registers; several handlers are allowed; an `onclick` attribute accepts only one (EJpt p.319–320).
2. The handler receives the event object (`type`, `target`, `button`, `key`...) (EJpt p.321).
3. To remove, use `removeEventListener` with **the same** function value: name the function (example `once`) (EJpt p.320).
4. The EJ1 needs `attachEvent` in IE and `addEventListener` in the others, and `event || window.event` (EJ1 p.209–211) **[DATED]**.

**Verification:** `window.addEventListener("click", () => console.log("You knocked?"))` prints on every click (EJpt p.319).

**Pitfalls:** passing a new anonymous function to `removeEventListener` removes nothing [inference from EJpt p.320].

**Source/era:** EJpt p.318–321.

### 9.7 Propagation, delegation and default action

**Steps:**
1. The event bubbles from the origin node up to the document and the window (EJpt p.321–322). `stopPropagation()` stops the bubbling; `event.target` indicates the origin (EJpt p.322).
2. **Delegation:** register a handler on the outer node and test `event.target.nodeName == "BUTTON"` instead of one per button (EJpt p.322–323).
3. `preventDefault()` cancels the default action (following a link, scrolling) and the handlers run before it (EJpt p.323). Some events cannot be intercepted, such as the close-tab shortcut in Chrome (EJpt p.324).
4. `focus` and `blur` do **not** propagate; neither does `load` on elements (EJpt p.332–333).
5. EJ1 equivalents: `stopPropagation`/`preventDefault` and, in IE, `cancelBubble`/`returnValue`; its own `normaliseEvent` unifies `target`, `relatedTarget`, `pageX`/`pageY` (EJ1 p.214–216) **[DATED]**.

**Pitfall:** only interfere with expected behavior for a good reason (EJpt p.324). `preventDefault` on `scroll` does not prevent scrolling (EJpt p.332).

**Source/era:** EJpt p.321–324, p.332–333.

### 9.8 Keyboard, mouse and touch

**Steps:**
1. Keyboard: `"keydown"` (repeats if the key is held) and `"keyup"`; use `event.key` (`"Enter"`, `"ArrowUp"`, `"v"` and `"V"`); modifiers in `shiftKey`, `ctrlKey`, `altKey`, `metaKey` (EJpt p.324–325). The target is the focused node or `document.body`; ordinary elements need `tabindex` (EJpt p.325). For typed text, prefer the field's `"input"` event (EJpt p.325–326). The EJ1 used `keyCode`, `charCode` and `keypress` (EJ1 p.213–214) **[DATED]**.
2. Mouse: `"mousedown"`, `"mouseup"`, `"click"` (on the node that contains both), `"dblclick"`, `"mousemove"` (EJpt p.326–327). Coordinates: `clientX/Y` (window) and `pageX/Y` (document) (EJpt p.326–327). `button` (0 left, 1 middle, 2 right) differs from `buttons` (sum: left 1, right 2, middle 4; 0 = none) (EJpt p.321, p.328–329).
3. Dragging: register `mousemove` on the `window` and remove it when `event.buttons == 0`; the resizable bar example computes `Math.max(10, bar.offsetWidth + dist)` (EJpt p.328).
4. Touch: `"touchstart"`, `"touchmove"`, `"touchend"`, with `event.touches` (list with `clientX`, `pageX`...); call `preventDefault` to avoid scrolling and simulated mouse events (EJpt p.329–330).
5. Scrolling: `"scroll"`; `max = document.body.scrollHeight - innerHeight`; width `${(pageYOffset / max) * 100}%` (EJpt p.331–332).
6. Focus and load: `"focus"`/`"blur"`; `"load"` on `window`; `"beforeunload"` with `preventDefault` and `returnValue` (most browsers no longer show the text) (EJpt p.332–333).

**Pitfalls:** not every keyboard fires key events (virtual Android, input method editors) (EJpt p.325–326). For keys captured by a game, stop the event, otherwise the arrows scroll the page (EJpt p.364; EJ1 p.225).

**Source/era:** EJpt p.324–333; EJ1 p.211–216, p.226–227 [DATED].

### 9.9 Timers, debounce and web workers

**Steps:**
1. `setTimeout`/`clearTimeout`, `setInterval`/`clearInterval`; keep the returned value to cancel (EJpt p.335–336). In the EJ1 the first argument could also be a string of code (EJ1 p.145) **[DATED]**.
2. **Debounce:** in the handler, `clearTimeout(timeout); timeout = setTimeout(...)`; the action only happens after a pause. `clearTimeout` with an undefined value or an already fired timer is harmless (EJpt p.336–337).
3. **Spacing (throttle):** keep the last event in `scheduled` and only schedule a timeout if nothing is scheduled (EJpt p.337).
4. **Web worker:** `new Worker("file.js")`; communication via `postMessage` and the `"message"` event; only JSON-serializable values, received as a copy; they do not share the global scope (EJpt p.334–335).

**Pitfalls:** heavy handlers or many short ones delay the event loop and all interaction (EJpt p.334).

**Source/era:** EJpt p.334–337.

---

## 10. fetch, HTTP and forms [HOST]

### 10.1 Understand the HTTP request

**Steps (EJpt p.401–404):** the browser opens a TCP connection (port 80 by default for HTTP) and sends method + path + version, headers (`Host`, `User-Agent`), a blank line and an optional body; the response brings `HTTP/1.1 200 OK`, headers (`Content-Type`, `Content-Length`) and a body. Methods: GET (retrieve), DELETE (delete), PUT (create/replace), POST (send). Status: 2xx success, 4xx request error (404), 5xx server error. GET and DELETE do not send a body (EJpt p.404). HTTPS adds a certificate and encryption (EJpt p.410). HTTP/2 keeps the concepts (EJpt p.403).

**Source/era:** EJpt p.283–285, p.401–404, p.410; EJ1 p.185–186, p.230 [DATED] (same concept, HTTP/1.0 still in use).

### 10.2 Use `fetch`

**Steps (EJpt p.406–408):**
1. `fetch(url)` returns a promise of `Response` (`status`, `headers`). `response.text()` and `response.json()` return another promise (the body may take time); `json()` rejects if it is not valid JSON.
2. Options in the 2nd argument: `method`, `body` (PUT/POST), `headers`. Example: `{headers: {Range: "bytes=8-19"}}`.
3. A relative URL without a protocol is relative to the document; starting with `/` it replaces the path.

**Critical pitfall:** the promise **resolves even with an error status**; it only rejects on a network error or a nonexistent server (EJpt p.407). Wrap it: `fetchOK` throws `Error(response.statusText)` if `status >= 400` (EJpt p.498).

**Verification:** `fetch("example/data.txt").then(r => r.text()).then(console.log)` (EJpt p.407). `headers.get` ignores case (EJpt p.406–407).

**Limit:** for security the browser only allows requests to other domains if the server responds with `Access-Control-Allow-Origin` (EJpt p.408–409).

**Source/era:** EJpt p.406–409. The EJ1 uses `XMLHttpRequest` with `open`, `send`, `readyState == 4`, `status` and `responseText`, requiring `ActiveXObject` in old IE (EJ1 p.231–234) **[DATED]**.

### 10.3 Work with JSON

**Steps:** `JSON.stringify(value)` serializes and `JSON.parse(text)` rebuilds (EJpt p.99–100). JSON requires property names in double quotes, only simple data and no comments (EJpt p.99). In the Spec, `JSON.stringify` replaces `NaN`/`Infinity` with `null`, returns `undefined` (not a string) for `undefined` and functions, and consults `toJSON` (Spec p.741–742). `JSON.parse` accepts a *reviver*; a trailing comma, single quotes and comments are `SyntaxError` [inference] (Spec p.735).

**Pitfall:** the EJ1 read JSON with `eval("(" + json + ")")`, which executes any code; today use `JSON.parse` (EJ1 p.234) **[DATED]**.

**Source/era:** EJpt p.99–100; Spec p.735–745.

### 10.4 Forms

**Steps:**
1. `<form method="GET" action="...">`: the fields become `?name=value&other=value` in the URL (the `name` defines the key); POST sends in the body. Use GET without side effects and POST to change something (EJpt p.404–406; EJ1 p.189–190). Special characters are escaped with `%XX`; use `encodeURIComponent`/`decodeURIComponent` (EJpt p.405; Spec p.455–457).
2. To handle it in JavaScript, listen for `"submit"` and call `preventDefault()` (otherwise the page reloads); validate or send with `fetch` (EJpt p.415–416, p.500–501).
3. `form.elements` acts like a map by `name`; a field inside `<form>` has `form` (EJpt p.415).
4. Text: `value`, `selectionStart`/`selectionEnd`; `"change"` only fires when the field loses focus; `"input"` on every change (EJpt p.416–417).
5. Checkbox/radio: `checked`; radios with the same `name` are exclusive; use `<label>` (EJpt p.418). `<select>`: `value`, `options`, `selected`, `multiple` (EJpt p.419–420).
6. Focus: `focus()`/`blur()`, `document.activeElement`, `autofocus`, `tabindex`, `disabled` (EJpt p.413–414).
7. File: `input.files`; read with `FileReader` (`readAsText`, `readAsDataURL`; events `"load"` and `"error"`), which the book wraps in a promise (EJpt p.420–422, p.447).
8. Storage: `localStorage.setItem/getItem/removeItem` stores only strings (use `JSON.stringify`/`parse`); `getItem` of a missing key gives `null`, and `JSON.parse(null)` gives `null`, letting `??` supply the default; `sessionStorage` lasts for the session (EJpt p.423–425).

**Verification:** in the notes app, reloading the page keeps the notes (EJpt p.423–425).

**Pitfalls:** disable the button during the request to avoid a double click (EJpt p.414). The EJ1 switched the type of the `submit` button to `button` and called `userForm.submit()`, and also validates on `submit` as a better alternative (EJ1 p.190, p.192–193, p.227) **[DATED]**.

**Source/era:** EJpt p.404–425.

---

## 11. Canvas [HOST]

### 11.1 Draw shapes

**Steps (EJpt p.374–377):**
1. `<canvas width="..." height="...">`; without attributes, 300×150. A new canvas is transparent.
2. `const cx = canvas.getContext("2d")` (also `webgl`, `webgpu`; the book covers only 2D).
3. The properties `fillStyle`, `strokeStyle`, `lineWidth` apply to the following drawings; `fillRect`, `strokeRect`, `clearRect`.
4. Paths: `beginPath()`, `moveTo`, `lineTo`, `closePath()`, then `stroke()` or `fill()` (which closes the path implicitly). Paths are described only by side effect; they are not values.
5. Curves: `quadraticCurveTo`, `bezierCurveTo`, `arc(cx, cy, radius, start, end)` (radians, clockwise; full circle with end > 2π) (EJpt p.377–380).
6. Text: `fillText(text, x, y)` with `font`, `textAlign`, `textBaseline` (EJpt p.381–382).

**Verification:** `context.fillStyle = "red"; context.fillRect(10, 10, 100, 50)` (EJpt p.374–375).

**Pitfall:** `arc` connects to the previous segment; use `moveTo` or a new path (EJpt p.379–380). Pie chart: start at `-0.5 * Math.PI`, draw `arc` and `lineTo` to the center (EJpt p.380–381).

### 11.2 Images and sprites

**Steps:** `drawImage` with `<img>`; only draw after the `"load"` event, otherwise nothing appears (EJpt p.382). With nine arguments: source (x, y, width, height) and destination (EJpt p.383). Sprite animation: `setInterval`, `clearRect`, `cycle = (cycle + 1) % 8` (EJpt p.383–384). In the game, an image that has not loaded simply is not drawn in the first frames and corrects itself in the following ones (EJpt p.392).

### 11.3 Transformations

**Steps:** `scale`, `translate`, `rotate` accumulate and affect what comes after; **order matters** (EJpt p.384–386). Mirroring: `translate(around, 0)`, `scale(-1, 1)`, `translate(-around, 0)` (`flipHorizontally`) (EJpt p.386). Wrap in `save()` and `restore()` (state stack); `resetTransform()` clears everything (EJpt p.387). Recursion: the `branch` function uses `save`/`restore` at each level; without them the figure stops being a tree (EJpt p.388).

**Pitfall:** `cx.scale(-1, 1)` before `drawImage` moves the image off screen; compensate (EJpt p.385). Transformations make bitmap drawing slower; the exercise asks for a precomputed mirror (EJpt p.399–400).

### 11.4 Choose between DOM, SVG and canvas

**Criterion (EJpt p.394–396):** plain HTML integrates text well; SVG is crisp at any zoom and lets you modify shapes and listen for events per element; canvas is pixel-based, cheaper for many small shapes and allows pixel-by-pixel effects (ray tracer, post-processing), but keeps no structure. They can be combined. In SVG, `xmlns` defines the namespace and the elements are manipulable through `setAttribute` (EJpt p.373–374).

**Source/era (section 11):** EJpt p.372–400. The EJ1 has no canvas chapter in the pages read [DATED].

---

## 12. Book projects: what each one teaches

### 12.1 Delivery robot (EJpt ch. 7, p.152–166)
- **Graph:** array of "A-B" strings converted by `buildGraph` with `Object.create(null)`, `split("-")` and destructuring (EJpt p.153–154).
- **Immutable state:** `VillageState.move` returns `this` if there is no road, otherwise a new state with `map` and `filter` over the parcels; `Object.freeze` is discussed but dispensed with (EJpt p.155–157).
- **Robot = function** `(state, memory) => {direction, memory}`; `runRobot` runs turns; `randomRobot` ignores the memory (EJpt p.158–159, p.161).
- **Path finding:** `findRoute` with a work list `{at, route}`, in discovery order (breadth), discarding places already seen (EJpt p.161–163); `goalOrientedRobot` uses the memory as the route (EJpt p.163–164). The EJ1 uses the same problem with `possibleRoutes`, `flatten` and A* with a binary heap (EJ1 p.102–124, p.242–247) **[DATED]**.
- **Teaches:** abstraction, immutability, functions as data, search, fair measurement (`compareRobots`) (EJpt p.164–166).

### 12.2 Egg, a programming language (EJpt ch. 12, p.264–281)
- **Recursive parser** `parseExpression`/`parseApply` produces a tree with `value`, `word`, `apply` nodes (EJpt p.265–270).
- **Evaluator** `evaluate(expr, scope)` with `specialForms` (`if`, `while`, `do`, `define`, `fun`) and scope as a prototype chain (EJpt p.270–276).
- **Environment** `topScope` with operators created by `Function`; `run` creates a new scope (EJpt p.274–275).
- **Teaches:** interpreter versus compilation (EJpt p.277), "cheating" by reusing JS, domain-specific languages (EJpt p.278), closures and scope.
- **Exercises:** arrays, closure, `#` comments, `set` (EJpt p.278–281).

### 12.3 Platform game (EJpt ch. 16, p.342–371)
- **Data:** `Level` reads a text plan (`.`, `#`, `+`, `@`, `o`, `=`, `|`, `v`), persistent `State` and actors with `update` (EJpt p.344–351).
- **Display:** `DOMDisplay` with a background table and absolute `div`s; `scrollPlayerIntoView` (EJpt p.352–358); later `CanvasDisplay` with the same `syncState`/`clear` interface (EJpt p.389–394).
- **Simple physics:** small steps, collision by rectangles with `touches` and `overlap`, movement per axis (EJpt p.358–364).
- **Control:** `trackKeys`, `runAnimation` (step limited to 100 ms), `runLevel` (promise), `runGame` (`async`) (EJpt p.364–368).
- **Teaches:** separating state, logic and display; `requestAnimationFrame`; promises in the game flow. Exercises: lives, pause, monster (EJpt p.368–371).
- The display sits behind an interface passed to the game, which made it possible to swap `DOMDisplay` for `CanvasDisplay` (EJpt p.352, p.389).

### 12.4 Pixel art editor (EJpt ch. 19, p.430–457)
- **Architecture:** single state (`picture`, `tool`, `color`), actions dispatched to `dispatch`, components with `dom` and `syncState` (EJpt p.431–433).
- **Immutable:** `Picture.draw` returns a copy; `updateState` does `{...state, ...action}` (EJpt p.434–435); the canvas `syncState` compares by identity (EJpt p.436–437).
- **Tools:** `draw`, `rectangle` (redraws from the original state), `fill` (grid search) and `pick` (EJpt p.442–444).
- **Files:** save with `canvas.toDataURL()` and a `download` link; load with `FileReader`, `<img>`, `getImageData`, hex with `toString(16).padStart(2, "0")` (EJpt p.445–449).
- **Undo:** `done` and `doneAt` with a 1 s threshold (EJpt p.449–450); `startPixelEditor` with destructured defaults (EJpt p.451).
- **Author's reflection:** the browser programming model is hard and that is why abstractions are used; React and Svelte are mentioned as popular "at the time of writing" (EJpt p.452–453).
- **Exercises:** shortcuts, efficient drawing, circles, correct lines (EJpt p.453–457).

### 12.5 Skill-sharing website (EJpt ch. 21, p.481–504)
- **Architecture:** Node server keeps talks (title, presenter, summary, comments); client in the browser; interface at `/talks` with JSON (EJpt p.482–486).
- **Long polling:** the client keeps a pending request with `If-None-Match` and `Prefer: wait=90`; the server responds when there is a change (new version as `ETag`) or 304 on timeout (EJpt p.483–487, p.494–495).
- **Server:** `Router` with a regex per route; `serve-static`; `SkillShareServer` with `version`, `waiting`, `updated()`; data validation (400) (EJpt p.487–495).
- **Client:** state `{talks, user}`, `handleAction`, `fetchOK`, `pollTalks`, rendering by functions; `localStorage` for the name (EJpt p.497–503). JSX and templates are mentioned as alternatives (EJpt p.500).
- **Teaches:** applied HTTP, idempotence, input validation, action flow, recovery from network failures. The interface has no access control (EJpt p.487).
- **Exercises:** persist to disk; avoid losing the comment field when redrawing (EJpt p.504).

---

## 13. Disagreements between the sources

When the sources disagree, the Spec (standard) rules, then the EJpt (modern explanation) and last the EJ1 (dated).

| Subject | EJ1 says | EJpt says | Spec | Rules |
|---|---|---|---|---|
| Variable declarations | only `var`, no block scope; `let` appears as a future feature (EJ1 p.34) | block-scoped `let`/`const`; `var` is pre-2015 (EJpt p.31–32, p.52–53) | — | EJpt |
| Cost of recursion | about ten times slower than a loop (EJ1 p.36) | about three times (EJpt p.62) | — | EJpt; the value depends on the engine |
| Enumerating properties | `for (var x in obj)` (EJ1 p.53–54) | `Object.keys` and `for...of` (EJpt p.80, p.87) | — | EJpt |
| Own property | `hasOwnProperty` and `propertyIsEnumerable` (EJ1 p.130–132) | `Object.hasOwn` (EJpt p.138) | — | EJpt (version not stated) |
| Creating an object with a prototype | `clone` function with a throwaway constructor (EJ1 p.151–152) | `Object.create` and `class` (EJpt p.130–131) | — | EJpt |
| JSON | `eval` with parentheses (EJ1 p.234) | `JSON.parse`/`stringify` (EJpt p.100) | ECMA-404 format (Spec p.734–735) | Spec and EJpt |
| Events | `attachEvent` in IE, `addEventListener` in the others, `event || window.event` (EJ1 p.209–211) | `addEventListener` (EJpt p.319) | — | EJpt [HOST] |
| HTTP requests in the browser | `XMLHttpRequest`, `ActiveXObject` (EJ1 p.231–233) | `fetch` (EJpt p.406) | — | EJpt [HOST] |
| Quantifier `{,4}` | four or fewer (EJ1 p.179) | only `{n}`, `{n,m}`, `{n,}` (EJpt p.194) | not confirmed in the parts of the Spec consulted | EJpt; treat `{,4}` as doubtful |
| `matchAll` | does not appear | "retorna um array de arrays" [returns an array of arrays] (EJpt p.210), but the example iterates with `for...of` | returns an iterator (Spec p.604) | Spec |
| Dates | `getFullYear` etc. (EJ1 p.57) | `getYear` is useless (EJpt p.198) | month 0 to 11 (Spec p.511) | Spec |
| Reserved words | ES3 list with `abstract`, `byte`, `char`... (EJ1 p.21) | modern list with `let`, `yield`, `static`... (EJpt p.32) | reserved only in strict mode: `let`, `static`, `yield`... (Spec p.861) | EJpt and Spec |
| Edition origin | 1st edition (2007/2013) | "2024 version" (EJpt p.9); exact edition [inference] | 17th ed. | — |

---

## 14. Source passages that must not be reproduced

These are errors, noise or truncations that the sources have; do not copy them as truth.

- **EJpt p.35–37 and EJ1 p.17:** the example prints "Your number is the square root of ..." but computes the **square** (`theNumber * theNumber`).
- **EJpt p.210:** `matchAll` "retorna um array de arrays" [returns an array of arrays] contradicts the example (it is iterable).
- **EJpt p.227:** the `formatDate` example with `M(MMM)?` only handles `M` and `MMMM`, and returns `getMonth()` without adding 1.
- **EJpt p.491:** in `serveFromRouter` the `catch` receives `error` but the body uses `String(err)`, which would throw `ReferenceError`.
- **EJpt p.474:** the text says it installs "uma versão específica de mime" [a specific version of mime], but the package is `mime-types`.
- **EJpt p.448:** "dois dígitos de base 16 podem expressar 162 = 256" [two base-16 digits can express 162 = 256] is 16² (lost exponent).
- **EJpt p.460:** the REPL `> 1 + 1` appears without the result `2` (extraction loss).
- **EJpt p.84:** the pizza frequency table and the phi formula came out incomplete; the values 76, 9, 4, 1 can be deduced from `phi([76, 9, 4, 1])` (EJpt p.85–86).
- **EJpt p.159:** text truncated mid-sentence (explanation of `VillageState.random`). **EJpt p.234:** the circular dependencies exercise continues on p.235.
- **EJpt p.5:** the numbering of the steps in the Portuguese listing is shifted to after the text of each step.
- **EJ1 p.226:** `self.content = null` in the animated version of `clearContent` (should be `this.content`).
- **EJ1 p.188:** `timeWriter` without a definition (incomplete excerpt).
- **EJ1 p.179:** `{,4}` as a quantifier.
- **General noise:** "Display hints...", "◂ ● ▸ ?", "Ex. N.N" markers, displaced epigraphs in English, and missing figures (EJpt p.101–104, p.123, p.149–151, p.164–166, p.479–480; EJ1 p.13, p.19, p.22). None of this is technical content.
- **Instructions in the sources:** no page read carried orders to an agent; the imperatives are exercise statements.

---

## 15. Gaps

The sources read do **not** cover, or cover only in part, the following; for these items there is no supported recipe here.

- **Strict mode in the EJ1** and `use strict` beyond what the EJpt and Spec Annex C say.
- **Deep copy** of objects (`structuredClone` and similar): not in the sources read.
- **`reduce` on an empty array without an initial value:** the EJpt describes only the case with at least one element (EJpt p.115).
- **Lookbehind, named groups, flags `d`, `s`, `v`, `matchAll` with details:** only in the Spec (p.558–559, p.583, p.598, p.604, p.610–611), with no usage examples; the EJpt does not teach them.
- **`Promise.allSettled`, `any`, `race`:** only in the Spec; edition in which they were added not stated.
- **`toSorted`, `with`, native `flatMap`, `Object.groupBy`:** in the Spec (Spec p.627, p.641); dates not stated. The EJpt does not mention them.
- **Dates:** time zones beyond `getTimezoneOffset` (EJ1 p.57–58), `Intl.DateTimeFormat` and date libraries: not covered.
- **Exception type of a stack overflow:** not named by the sources (EJpt p.58; EJ1 p.37). Exact error messages vary by engine.
- **TypeScript:** only mentioned (EJpt p.171).
- **Top-level `await` in modules, `for await`, async iterators:** the Spec deals with async iterators (Spec p.764), but the recipes were not detailed in the sources read.
- **Real test runners, linters, formatters, bundlers and minifiers:** only mentioned (EJpt p.172, p.229–230).
- **WebSockets:** only mentioned (EJpt p.484). **Accessibility, advanced SVG, WebGL/WebGPU:** not covered (EJpt p.374).
- **Web application security** (XSS, CSRF, authentication): the EJpt only mentions sandbox, CORS and HTTPS (EJpt p.290, p.408–410); the skill-sharing project warns that it has no access control (EJpt p.487).
- **Official exercise solutions:** they are on the book's website and not in the extracted text; "Display hints..." carries no content.
- **Exact ECMAScript version** of each feature: the EJpt only dates classes, symbols, arrow functions, modules and `getYear`/ES3/ES5/ES6 in general terms (EJpt p.9, p.56, p.132, p.141, p.221); the other features stay as "version not stated in the sources", and the Spec does not date individual features.
- **EJ1 after p.247 and appendices beyond `switch`, `with`, `do`, labels and binary heap:** not used.
