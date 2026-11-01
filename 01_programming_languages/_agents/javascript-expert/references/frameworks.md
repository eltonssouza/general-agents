# Decision frameworks in JavaScript

This file gathers decision trees: question, criteria, recommendation according to the source (with pages) and, at the end of each tree, what EJ1 [DATED] says differently. Use it for the question "which construct should I choose?"; for the exact behavior, follow the cited Spec pages. Grep the titles (`## N.`, `### Dn.m`) to locate the topic.

## Contents

1. Conventions and how to read the trees
2. var, let, const and scope
3. Equality, coercion and `Object.is`
4. Declared function, expression, arrow and constructor (this, arguments)
5. Object literal, class, constructor function/prototype and Map
6. Inheritance, composition and private `#` fields
7. Iteration: for, for-of, for-in, forEach, map, filter, reduce
8. Asynchrony: callbacks, Promise, async/await, generators and parallelism
9. Error handling
10. Modules (ESM, CommonJS, NPM) [HOST]
11. Strings and regular expressions
12. Immutability
13. Destructuring, rest and spread
14. undefined, null, `?.` and `??`
15. JSON
16. DOM and events [HOST]
17. Errors and truncated passages in the sources (do not reproduce)
18. Divergences between sources
19. Gaps

---

## 1. Conventions and how to read the trees

**Sources.** Spec = ECMA-262, 17th edition (ECMAScript 2026), normative. EJpt = *Eloquent JavaScript* in Portuguese, modern edition (the text says it uses the 2024 version of JavaScript, EJpt p.9; that it is the 4th edition is [inference]). EJ1 = *Eloquent JavaScript*, 1st edition (2007, revised in 2013; EJ1 p.247): everything in it is [DATED]. Pages are those of the PDF.

**Hierarchy.** For language behavior, the Spec prevails. EJpt explains and gives opinions (for example, prefer `===`, EJpt p.25); a book's opinion is not a language rule. EJ1 serves to recognize old code.

**Labels.** [DATED]: EJ1, `with`, Annex B, what the source calls legacy. [VERSION-DEPENDENT]: the source attributes it to an edition. [HOST]: defined by the environment (browser, Node.js, DOM, timers, `fetch`, `prompt`, `console`). [inference]: a link made from the cited pages. [extrapolation]: knowledge outside the sources.

**Versions.** The Spec does not say in which edition each feature was introduced, except in the annexes (Spec p.865–869). Where the edition is not stated, the file writes "version not stated in the sources". EJpt dates only `class`, arrow functions and symbols to 2015 (EJpt p.56, p.132, p.141); ECMAScript 3 was the standard from about 2000 to 2010, version 5 came out in 2009 (EJpt p.9).

---

## 2. var, let, const and scope

### D2.1 Which keyword to use to declare a binding?

**Criteria.** Will the binding be reassigned? New or old code? Block or function scope?

**Recommendation according to the source.**
- Reassigned: `let` (EJpt p.30–31). Never reassigned: `const`, which gives a name to a value (EJpt p.31–32). EJpt does not literally say "use `const` by default"; that is [inference].
- `var` is the pre-2015 form, which behaves strangely and is rarely used (EJpt p.31–32): only to maintain old code.
- `const` does not freeze the contents: the binding is not reassignable, but the object can change (EJpt p.82).
- `let`/`const` have block scope; `var`, only function or global scope (EJpt p.52–53). Scope is lexical (EJpt p.53–54); an inner name shadows the outer one (EJpt p.53).

**Spec guarantees.**
- `let`/`const` exist from the creation of the environment, but are not accessible until the `LexicalBinding` is evaluated (temporal dead zone) (Spec p.327); reading or writing before that throws `ReferenceError` (Spec p.167–168).
- `var` is born `undefined` and the same variable serves several declarations of the same name; the initializer runs when the declaration is executed (Spec p.328–329).
- `SyntaxError`: `const` without an initializer, the name `let`, duplicates in the same declaration (Spec p.328); lexical duplicates or lexical + `var` in the same block (Spec p.326).
- Reassigning an immutable binding throws `TypeError` in strict mode or with a "strict binding"; in sloppy mode it may fail silently (Spec p.167). That `const x = 1; x = 2` gives `TypeError` is [inference].
- Each block creates a new environment (Spec p.326); the body of a `switch` is a single scope, so a repeated `let` in two `case` clauses conflicts (Spec p.348, p.350).

**EJ1 [DATED].** Only `var` (EJ1 p.15); blocks do not create scope, which the author calls a design mistake; `let` appears only as a promise of "Harmony" (EJ1 p.34). The list of reserved words in EJ1 (EJ1 p.21) is from that time; use the one in EJpt (EJpt p.32).

### D2.2 What does a closure capture in a loop?

- `for (let ...)`: a copy of the bindings per iteration, created before the increment (Spec p.336–337); `const` has no per-iteration list (Spec p.337). `for-of`/`for-in` with `let`/`const`: a new environment per iteration (Spec p.342–343). `var` is a single variable (Spec p.328); that closures in a `var` loop see the same value is [inference].
- A closure keeps access to the bindings of the scope where it was born, even after the call (EJpt p.60–61; EJ1 p.35–36).

### D2.3 Can I use the function before declaring it?

- A `function f() {}` declaration is hoisted to the whole scope (EJpt p.55; EJ1 p.39). In the Spec: at the top of a Script/function it counts as `var` (Spec p.125, p.135–136); at the top of a Module it is lexical (Spec p.126); in a block, initialized on block entry (Spec p.326–327).
- A function assigned to `const`/`let` is not hoisted by the same mechanism [inference]; EJpt only asserts the hoisting of declarations (EJpt p.55).

### D2.4 Use strict mode?

- `"use strict"` at the top of the file or function: assigning to an undeclared binding throws `ReferenceError` (EJpt p.168–169; Spec p.81); `this` is `undefined` in a call that is not a method call; a constructor without `new` fails; duplicate parameters are forbidden (EJpt p.169–170). It rarely does harm (EJpt p.170).
- Classes and modules are automatically strict (EJpt p.169; Spec p.376). In sloppy mode, assigning to an unresolvable name creates a global property (Spec p.81).
- `"use strict"` in a function with non-simple parameters is a `SyntaxError` (Spec p.360).
- Pitfall: if the name already exists in a visible scope, the assignment silently overwrites it (EJpt p.169).
- Scripts share the global scope: a global `let` and a global `var` of the same name in distinct scripts fail at run time with `SyntaxError` (Spec p.400–401).

---

## 3. Equality, coercion and `Object.is`

### D3.1 Which equality operator?

**Criteria.** Are the types known? Do I need to handle `null` and `undefined` together? Do I need to distinguish `+0` from `-0`?

**Recommendation according to the source.**
1. Default: `===`/`!==`, with no conversion. EJpt recommends them defensively; `==` only when sure the types coincide (EJpt p.25).
2. "Has a value?": `x == null`, since with `null`/`undefined` on one side the result is `true` only if the other is also nullish (EJpt p.24–25). Alternatives: `??` and `?.` (D14).
3. `NaN` is different from itself (EJpt p.22). Test with `Number.isNaN`, without conversion (EJpt p.36; Spec p.488–489). The global `isNaN` converts first (Spec p.453). Function-free test: `x !== x` (Spec p.453).
4. Equality that equates `NaN` and distinguishes `±0`: `Object.is` (SameValue, Spec p.465, p.99). SameValueZero (in `includes`, `Map`, `Set`) equates `±0` and `NaN` (Spec p.100, p.628, p.675, p.682).
5. Objects: `==` and `===` compare identity (EJpt p.82). There is no built-in deep comparison; write a `deepEqual` (EJpt p.104).
6. Array search: `includes` finds `NaN`; `indexOf` uses strict equality and does not find it (Spec p.628–629).

**Rules of `==` (Spec p.101–102).** Same type: like `===`. `null == undefined`. Number vs String: the string becomes a Number. Boolean becomes Number. Object vs primitive: `ToPrimitive`. BigInt vs Number: mathematical comparison. Everything else: `false`. `null == 0` is `false` [inference]. `==` is not transitive: `new String("a") == "a"` and the reverse are `true`, but two distinct `String` objects are not `==` (Spec p.312). EJpt examples: `8 * null` is 0, `"5" - 1` is 4, `"5" + 1` is `"51"` (EJpt p.24).

**`switch` uses `===`** (Spec p.350).

**Relational comparison.** Strings compare by UTF-16 code unit, without normalization (Spec p.101, p.312; EJpt p.21: uppercase "less", not dictionary order). For language-aware ordering, `localeCompare` depends on the environment [HOST] (Spec p.544).

**EJ1 [DATED].** The same underlying rules (`false == 0`, `"" == 0`, `"5" == 5` are `true`; `===` does not convert; EJ1 p.26). Tests nullish with `something == undefined` (EJ1 p.26) and `NaN` only with `isNaN` (EJ1 p.28).

### D3.2 How does a condition convert values?

- Falsy: `false`, `undefined`, `null`, `+0`, `-0`, `NaN`, `0n`, the empty string; everything else is truthy (Spec p.89). EJpt lists `0`, `NaN`, `""` for the purposes of `||` (EJpt p.26).
- `if (x)` fails when `0` or `""` are valid; be explicit with `=== null` or `=== undefined` (EJ1 p.27, still useful [inference]).
- For defaults, `||` falls back on any falsy value; `??` only on nullish (D14.1).

### D3.3 Addition or concatenation?

- `+` applies `ToPrimitive`; if either side becomes a string, it concatenates; otherwise `ToNumeric` (Spec p.317). Number + BigInt throws `TypeError` (Spec p.317). Without a hint, `Date` acts as a string and other objects as a number (Spec p.318).
- Convert explicitly with `Number`/`String` (EJpt p.35; EJ1 p.28). `Number("text")` gives `NaN` (EJpt p.36); `parseInt`/`parseFloat` read only the valid prefix (Spec p.453–454).

---

## 4. Declared function, expression, arrow and constructor (this, arguments)

### D4.1 Which function form?

**Criteria.** Does it need its own `this` or to be a constructor? Does it need `arguments`? Is it a short callback? Does it need to be called before being defined? Does it need a name for recursion?

| Situation | Form | Source |
|---|---|---|
| Reusable function, used before being defined | declaration | EJpt p.55 |
| Function stored in a binding | expression `const f = function () {}` | EJpt p.51, p.54–55 |
| Short callback, `this` of the context | arrow | EJpt p.56, p.128 |
| Object or class method | shorthand `find(a) {}` | EJpt p.128 |
| Constructor | `class` | EJpt p.130–133 |
| Pausable, generates an iterator | `function*` | EJpt p.250–251 |
| Waits for promises | `async function` | EJpt p.249–250 |

- Arrow: an expression body returns the value; with braces it requires `return` (EJpt p.56). Introduced in 2015 [VERSION-DEPENDENT] (EJpt p.56). Returning an object literal requires parentheses (EJpt p.79).
- Spec: an arrow has no `arguments`, `super`, `this` or `new.target` of its own (Spec p.364); without `MakeConstructor`, so it is not a constructor [inference]; no line break before `=>` (Spec p.363).
- Ordinary functions have their own `this` and `prototype` (Spec p.361–363). Methods, bound functions and arrows have no `prototype` (Spec p.476). `async` functions are not constructors (Spec p.388–389). A class called without `new` throws `TypeError` (Spec p.384–385).
- Named expression: the name is valid only inside the body, for recursion (Spec p.362).
- Duplicate parameters: only in a simple list and a non-strict function; never in arrows and methods (Spec p.355).

**EJ1 [DATED].** Only declaration and expression with `function` (EJ1 p.30–31, p.39); no arrows or shorthand methods.

### D4.2 What is `this`?

- `obj.m()`: `this` is `obj` (EJpt p.127; Spec p.294). Call without a reference: `this` is `undefined` in the Spec (Spec p.294), but sloppy functions still convert it (Spec p.473). `(0, obj.f)()` loses the `this` [inference] (Spec p.324).
- A nested ordinary function has a different `this`; an arrow uses the surrounding one (EJpt p.128).
- `call`, `apply`, `bind` fix `this`; arrow and bound ignore `thisArg` (EJpt p.127; Spec p.472–474).
- In a derived constructor, `this` only exists after `super()` (Spec p.295).

**EJ1 [DATED].** Every call creates a new `this`; ways out: a `self`/`that` variable, or the book's `bind` and `method` helpers (EJ1 p.141–142).

### D4.3 How many arguments?

- Extra arguments are ignored and missing ones are `undefined`, without warning (EJpt p.58). Default value: `function f(n, step = 1)`, which also applies to an explicit `undefined` (EJpt p.59).
- Variable: rest parameter (EJpt p.94). The function's `length` counts the parameters before the first one with a default or rest (Spec p.359).

**EJ1 [DATED].** The `arguments` object: looks like an array, but without methods and with a `length` that is not updated (EJ1 p.64); optional parameters via `arguments.length < 2` (EJ1 p.64).

### D4.4 Recursion or loop?

- Recursion is natural for problems that branch (EJpt p.63); it costs more than iterating (EJpt p.62). Write the correct version first and measure later (EJpt p.62). An exhausted stack produces an environment message (EJpt p.58).
- Tail calls only count in strict code and outside async/generators [VERSION-DEPENDENT]; the Spec does not say whether engines implement them, so do not count on it (Spec p.392–397) [inference].

---

## 5. Object literal, class, constructor function/prototype and Map

### D5.1 Which structure holds the data?

**Criteria.** Fixed or dynamic names? Are keys strings? Is there per-instance behavior? Is the key an object that should not prevent collection?

**Recommendation according to the source.**
1. **Record with fixed names:** object literal (EJpt p.100), with shorthand `{events}` (EJpt p.83) and computed names `[expr]` (EJpt p.142).
2. **Instances with behavior:** `class` (EJpt p.130–133), without creating a class reflexively for every concept (EJpt p.154–155).
3. **Dynamic dictionary:** `Map`. A plain object inherits from `Object.prototype` (`"toString" in ages` is `true`); ways out: `Object.create(null)`, `Map` (any key type), or `Object.hasOwn` (EJpt p.136–138).
4. **Set:** `Set` (EJpt p.444; Spec p.682). Algebra methods (`union` etc.) exist, version not stated, and require a set-like argument: an Array throws `TypeError` (Spec p.682–683, p.685–690).
5. **Data attached to an object without preventing collection:** `WeakMap`/`WeakSet`, with no enumeration; reading with an invalid key is silent, writing throws `TypeError` (Spec p.692–695). EJpt does not cover it.

**`Map` details (Spec).** SameValueZero, `-0` becomes `+0`, objects by identity (Spec p.675, p.697); insertion order; `set` on an existing key keeps its position; items added during `forEach` are visited (Spec p.679–680); the constructor requires `new` and pairs (Spec p.675–676). `Map.groupBy` returns a `Map`, `Object.groupBy` an object with no prototype, version not stated (Spec p.677, p.464).

**Object details (Spec).** `Object.keys`/`values`/`entries`: own enumerable string keys (Spec p.462, p.465–466). `in` includes inherited ones (Spec p.310); `Object.hasOwn` only own (Spec p.464). `__proto__` and `__defineGetter__` are legacy [DATED] (Spec p.468–469).

**EJ1 [DATED].** A set as an object with `true`, `in` and `delete` (EJ1 p.45–46), with the pitfall `"constructor" in {}` (EJ1 p.129); remedy with `hasOwnProperty` and `propertyIsEnumerable` (EJ1 p.130–132) or the `Dictionary` type (EJ1 p.132). If the key `hasOwnProperty` exists, use `Object.prototype.hasOwnProperty.call` (EJ1 p.130–131). For the author, objects have two roles (values with methods; sets of properties) and prototypes get in the way of the second (EJ1 p.131).

### D5.2 Class, constructor function or factory?

- New code: `class`, in which the `constructor` becomes the function and the methods go on the `prototype` (EJpt p.131). `class` is from 2015 [VERSION-DEPENDENT] (EJpt p.132). Fields (`speed = 0;`) live on the instance (EJpt p.132–133), version not stated. Getter, setter and `static` (EJpt p.139–141).
- Immutable data shared by all instances lives on the prototype (EJpt p.349).
- `Object.create(proto)` creates an object with the given prototype; the argument must be an object or `null` (EJpt p.130; Spec p.461–462). Writing to a property never alters the prototype (EJpt p.134–135).
- In the Spec, `proto.constructor` is not enumerable (Spec p.385); a named class only binds its name after being evaluated (Spec p.386); static fields and `static {}` blocks run last (Spec p.385–386).
- Symbols serve as property names without collision (EJpt p.141–142).

**EJ1 [DATED].** Constructor function with `new` (EJ1 p.126–127); shared members on the `prototype`, per-instance data in the constructor (EJ1 p.129); without `Object.create`, uses `clone` (EJ1 p.151–152).

---

## 6. Inheritance, composition and private `#` fields

### D6.1 Inherit or compose?

**Criteria.** Is the relation "is a"? Will the types evolve together?

**Recommendation according to the source.**
- Encapsulation and polymorphism are great; inheritance is more controversial, since it ties classes together and tangles them, and should not be the first tool (EJpt p.147). Treating the isolated object as the unit is unfortunate, since functionality usually involves several classes (EJpt p.127).
- EJ1 gives the criterion: a subtype only when "is a"; Piano does not inherit from `Array` (ambiguity of `piano[0]`), better to have `keys` and `pedals` properties (EJ1 p.159). Seeing this as object composition is [inference]; the sources only use "composition" for functions (EJ1 p.100–101).
- `extends` creates a subclass, the constructor calls `super(...)` (EJpt p.146–147). Extend `Error` and filter with `instanceof` (EJpt p.182–183).
- Spec: `extends` of a non-constructor, or with a `prototype` that is neither an object nor `null`, throws `TypeError`; `extends null` is accepted (Spec p.384). `super()` in a class without `extends` is a `SyntaxError` (Spec p.376).

**EJ1 [DATED].** Inheritance with `clone` and `Super.call(this, ...)` (EJ1 p.152); `inherit`/`create`/`extend` (EJ1 p.160–161); mix-ins and multiple inheritance, which the author says to ignore in most cases (EJ1 p.164–165).

### D6.2 How to make something private?

- Prefix `#` on a field or method: visible only inside the class (EJpt p.133); private fields are declared in the body (EJpt p.134). Version not stated.
- Spec: each `#name` is unique per evaluation of the class (Spec p.384); a missing `PrivateGet` and assignment to a private method throw `TypeError`; adding the same member twice also does (Spec p.110–111). `#x in obj` tests the brand (Spec p.310). `#constructor` is forbidden (Spec p.377).

**EJ1 [DATED].** No privacy; a comment and a `_` prefix by convention (EJ1 p.143–144).

---

## 7. Iteration: for, for-of, for-in, forEach, map, filter, reduce

### D7.1 Which way to traverse?

**Criteria.** Do I need to interrupt? Transform, filter, accumulate, or only cause an effect? Is there an `await` inside? What is the structure?

**Tree.**
1. Count or free condition: `for`, `while`, `do ... while` (body runs at least once) (EJpt p.38–42); `break` and `continue` (EJpt p.42–43). Labels serve outer `break`/`continue`; there is no `goto` (Spec p.351).
2. Values of an array, string or iterable: `for (const x of c)` (EJpt p.87). On a string it iterates by code points (EJpt p.119; Spec p.557).
3. Transform: `map`, same `length` (EJpt p.113–114; Spec p.630–631). Filter: `filter` (EJpt p.112–113).
4. Accumulate: `reduce(f, initial)` (EJpt p.114–115). An empty array without an initial value throws `TypeError` (Spec p.632–633).
5. Some/all: `some`/`every`; `every([])` is `true`, `some([])` is `false` (Spec p.622, p.636; EJpt p.123). Find: `find`, `findIndex`, `findLast` (EJpt p.120; Spec p.624–626).
6. Effect only: `for-of` or `forEach` (EJpt p.111).
7. Object keys: `Object.keys`/`entries` with `for-of` (EJpt p.80, p.138).

**Selection criteria.**
- A `filter` + `map` + `reduce` pipeline is readable, but creates intermediate arrays; the imperative loop does less work and may be worth it on huge arrays (EJpt p.115–117).
- Exiting early: `break`/`return` do not cross the `forEach` callback (EJ1 p.107); use `for-of`, `some`, `every` (EJpt p.118, p.122–123).
- `await` in `forEach`/`map` does not make the loop wait **[inference]** (EJpt shows only the shared-state bug in `map(async ...)`, EJpt p.258–259; `forEach` is not treated with `await`; Spec p.627) (D8.3). In async code, use `for`/`for-of` (EJpt p.249–250).
- The DOM `NodeList` has no `map`; use `Array.from` (EJpt p.297, p.302) [HOST].
- `sort` mutates the array, sorts as strings without a comparator (`10` before `9`), is stable, and an inconsistent comparator leaves the order up to the implementation (Spec p.636–638). Non-mutating versions (`toSorted` etc.): version not stated (Spec p.640–643).

**EJ1 [DATED].** `forEach`, `map`, `reduce`, `filter`, `any`, `every` are functions from the book itself, with the function as the first argument (EJ1 p.78–82, p.108–110); ES5 would bring some natively (EJ1 p.6). No `for-of`: `for (var i = 0; ...)` (EJ1 p.77). To leave `forEach`, a sentinel value `Break` is thrown (EJ1 p.107–108).

### D7.2 When to use `for-in`?

- Spec: only string keys, own and inherited, enumerable, at most once; additions during enumeration have no guarantee (Spec p.343). The order is deterministic only under restricted conditions (Spec p.343–344). `for-in` over `undefined`/`null` ends without error (Spec p.341–342).
- EJpt does not teach `for-in`; it teaches `Object.keys` (EJpt p.80, p.138). For own keys only, prefer `Object.keys`/`entries` [inference].
- `for-of` calls the iterator's `return` when leaving early (Spec p.343, p.116); `for-in` does not.

**EJ1 [DATED].** `for (var x in obj)` is the way to enumerate (EJ1 p.53–54); hidden properties do not appear, those created by the program always do (EJ1 p.66–67); extending `Object.prototype` breaks other people's `for-in` (EJ1 p.129, p.133–134).

### D7.3 `switch` or `if`?

`switch` uses `===`, falls through from one `case` to the next until a `break`, and `default` can be in any position (Spec p.349–350). EJpt finds the syntax awkward and warns about a forgotten `break` (EJpt p.44–45); EJ1 prefers chains of `if` (EJ1 p.240).

---

## 8. Asynchrony: callbacks, Promise, async/await, generators and parallelism

### D8.1 How to wait for something slow?

**Criteria.** Does the API offer a callback or a Promise? Do the steps depend on each other?

**Tree.**
1. Callback-only API: wrap in `new Promise((resolve, reject) => ...)`, calling `reject(error)` on error (EJpt p.241, p.244, p.422). Example: `wait(t)` with `setTimeout` (EJpt p.255–256). `setTimeout` is [HOST] (EJpt p.239).
2. Dependent steps: `async`/`await` (EJpt p.249–250); you still need to understand Promises, but async is usually more pleasant than chained `then` (EJpt p.250).
3. Short transformation: chained `then` (EJpt p.241–242). A handler that is not a function is ignored (Spec p.779).
4. Plain callback: the `(error, value)` convention, verbose and error-prone (EJpt p.243, p.466).

**Spec guarantees.**
- States: pending, fulfilled, rejected; resolved is not fulfilled (`resolve(anotherPromise)` leaves it pending) (Spec p.764). The first call of `resolve`/`reject` wins (Spec p.766; EJpt p.247).
- Thenables are called in a later Job, never synchronously (Spec p.766); `then` reactions run as Jobs: even an already-resolved promise only fires after the current script (Spec p.768; EJpt p.257–258).
- An `async` function always returns a Promise; an error in the parameters becomes a rejection (Spec p.389). `await` requires an operand and is only valid in an async function or module (Spec p.387–388, p.402).
- The number of Jobs per `await` was reduced in ES2019, which may change the order between `then` and `await` [VERSION-DEPENDENT] (Spec p.869).
- An unhandled rejection is reported by the host [HOST] (Spec p.768; EJpt p.245).

**EJ1 [DATED].** No Promise, async or generator; asynchrony via `XMLHttpRequest` with `onreadystatechange` and `readyState == 4` [HOST] (EJ1 p.233) and `success`/`failure` callbacks (EJ1 p.237). The synchronous form freezes the browser (EJ1 p.233).

### D8.2 In series or in parallel?

- **Series** (dependent): successive `await`; total time is the sum (EJpt p.237, p.249–250).
- **Parallel** (independent): fire everything without waiting and await together (EJpt p.253). `Promise.all` delivers an array in input order (EJpt p.254–255; Spec p.771); rejects with the reason of the first rejection, and the others keep running [inference] (Spec p.771–772); empty resolves `[]` (Spec p.772).
- **All results:** `Promise.allSettled` returns `{status, value|reason}` (Spec p.773–774). **First success:** `Promise.any`, which rejects with `AggregateError` and `errors` in input order (Spec p.774–775). **First to finish:** `Promise.race`; empty never settles (Spec p.776). Version not stated; EJpt only covers `all`. EJpt does a timeout by hand (EJpt p.247); `race` would be the alternative [inference].
- `Promise.try` and `Promise.withResolvers`: version not stated (Spec p.777).
- Do not swallow errors blindly: the `.catch(() => {})` of EJpt p.253 is a decision of the example.

### D8.3 How to avoid concurrency bugs?

- In asynchronous code there are gaps in which other code runs (EJpt p.258). Classic bug: `list += ... await ...` inside `files.map(async ...)` loses lines; return values from the promises and join them with `join` after `Promise.all` (EJpt p.258–259).
- `try/catch` around the one who schedules does not catch an exception from the callback (EJpt p.256–257).
- Slow code delays all events, since the environment runs one program at a time [HOST] (EJpt p.257).

### D8.4 Generator, async generator and `for await`?

- `function*` returns an iterator; each `next()` runs up to a `yield` (EJpt p.250–251); simplifies iterators (EJpt p.251). Async is a special kind of generator (EJpt p.252).
- Spec: calling the generator does not execute the body (Spec p.369); `yield*` delegates `next`/`throw`/`return` (Spec p.371–372); `yield` is not valid in the parameters (Spec p.369). `async function*` allows `yield` and `await`; `for await` only in a context with `await` (Spec p.372–373, p.338). EJpt does not cover async generators.
- Protocol: `Symbol.iterator` returns an object with `next()` that returns `{value, done}` (EJpt p.143).

---

## 9. Error handling

### D9.1 Special value or exception?

**Criteria.** Programmer error or expected condition? Can the immediate caller recover? Can the return be any value?

**Recommendation according to the source.**
- Two kinds of problem: programmer error (fix it) and genuine use (react or fail cleanly) (EJ1 p.68).
- A special value (`null`, `undefined`, `-1`) serves common errors that the caller must consider (EJpt p.175–176); it fails if the function can already return any value, and forces a check at every call (EJpt p.176; EJ1 p.70).
- An exception when the handling is far away; it unwinds the stack to the nearest `try` (EJpt p.176; EJ1 p.70–71).
- An assertion only for bugs that are easy to make (EJpt p.183–184). Silent functions are dangerous (EJ1 p.69).

### D9.2 How to catch?

- `try`/`catch` (EJpt p.177); `catch` without a parameter and with destructuring are accepted (Spec p.353).
- There is no selective catching by type: filter with `instanceof` and rethrow the rest (EJpt p.181–183; EJ1 p.74). Comparing `message` is fragile (EJpt p.182). An indiscriminate `catch` swallowed a typo (EJpt p.181–182).
- Cleanup: `finally`, which does not suppress the exception (EJpt p.179–180); an abrupt `finally` replaces the previous result (Spec p.354).
- Any value can be thrown (EJpt p.176; Spec p.352–353); EJ1 prefers unique objects to strings (EJ1 p.75).
- `Error` holds `message` and `stack` (EJpt p.178); `message` is non-enumerable and `cause` comes in through the option (Spec p.482, p.487), version not stated.

### D9.3 Which error does the language throw?

| Situation | Type | Source |
|---|---|---|
| `let`/`const` before initialization; unresolvable name | `ReferenceError` | Spec p.81, p.167–168 |
| Property of `null`/`undefined`; `new` on a non-constructor; calling a non-function; destructuring nullish | `TypeError` | Spec p.81, p.293–294, p.319–320 |
| Invalid code or JSON | `SyntaxError` | Spec p.735 |
| Out of range (`toFixed`, `repeat`, `with`, `fromCodePoint`) | `RangeError` | Spec p.492, p.547–548, p.643, p.538–539 |
| Stray `%` in `decodeURIComponent` | `URIError` | Spec p.456 |
| `Promise.any` without success | `AggregateError` | Spec p.774–775 |

Writing to a non-writable property: `TypeError` in strict mode, silence in sloppy mode (Spec p.81, p.317). EJpt and EJ1 do not name the exhausted-stack error (EJpt p.58; EJ1 p.37).

### D9.4 Errors in asynchronous code

- A rejection propagates through the chain; `catch(f)` is `then(undefined, f)` (EJpt p.243–245; Spec p.778). A rejected `await` becomes an exception at the point of the `await` (EJpt p.250). `finally` receives no argument and does not change the value or reason, unless it throws (Spec p.778–779).
- `fetch` only rejects on network failure; an error status resolves (EJpt p.407) [HOST]; check the status or wrap it (`fetchOK`, EJpt p.498).
- Uncaught exception: console in the browser, aborts the process in Node.js [HOST] (EJpt p.180–181).

---

## 10. Modules (ESM, CommonJS, NPM) [HOST]

### D10.1 ESM or CommonJS?

**Criteria.** Browser or Node.js? New or legacy code? Dynamic loading?

**Recommendation according to the source.**
- New code: ES modules. EJpt says there is no longer a reason to write new programs in CommonJS; most popular NPM packages already offer ES modules and Node.js lets ES modules import from CommonJS (EJpt p.229).
- Scripts share the global; modules have their own scope and `import`/`export`, since ES2015 [VERSION-DEPENDENT] (EJpt p.221). Browser: `type="module"` (EJpt p.289). Node.js: `.js` is CommonJS, `.mjs` is an ES module (EJpt p.461). Name resolution depends on the platform [HOST] (EJpt p.222, p.461–462).
- `import`/`export` only at the top of the module, resolved before execution; `require` is an ordinary function, accepts an expression and can be inside a function (EJpt p.222, p.228).
- `import()` returns a Promise; failures reject and it resolves to the namespace (Spec p.299–300).
- One `export default` per module; more than one is a `SyntaxError` (Spec p.402). Importing a nonexistent or ambiguous name is a `SyntaxError` at link time (Spec p.428). Named imports are live bindings [inference] (Spec p.428–429).
- Life cycle: load (host), link (no side effects, repeatable), evaluate (once; the error is memoized) (Spec p.410–414, p.417–418). Dependencies evaluate before the importer, in textual order (Spec p.404, p.414).
- Top-level `await` makes the module behave like an async function; importers wait (Spec p.426, p.429–430), version not stated.
- `import.meta` and specifier resolution belong to the host [HOST] (Spec p.301, p.432–433).
- Cycles: CommonJS tolerates a restricted form (EJpt p.234–235); the Spec handles cycles in ES modules (Spec p.418–419).

**EJ1 [DATED].** No modules: one file per module, `<script>` in order, a homemade `require` with `eval` (EJ1 p.167–169); IIFE with `provide` exporting to `window` (EJ1 p.171–172). EJpt shows the IIFE as a pre-2015 technique (EJpt p.225–226).

### D10.2 Packages and NPM [HOST]

- NPM is a repository and installer; `package.json` holds name, version and dependencies (EJpt p.224, p.463–464). Semantic versioning: the middle number goes up with compatible novelty, the first with a breaking change; `^2.3.0` covers up to before 3.0.0 (EJpt p.464–465). Check licenses (EJpt p.224–225).
- Module interface: simple, predictable, functions instead of stateful objects, focused modules that compute values (EJpt p.230–231).
- `eval` and `new Function` execute text and are dangerous: EJpt treats only the `Function` constructor (EJpt p.228), EJ1 treats `eval` (EJ1 p.168, p.234), the Spec defines both (Spec p.449, p.471); the host may block them [HOST] (Spec p.450).

---

## 11. Strings and regular expressions

### D11.1 Which text tool to use?

**Criteria.** Fixed substring or structure? Can the text have emoji or other alphabets? Do I want one or all occurrences?

- **Does a substring exist?** `includes`, `startsWith`, `endsWith`; they throw `TypeError` with a RegExp (Spec p.541–542, p.552–553). `indexOf` returns `-1` if not found (Spec p.542–543). `at` out of range gives `undefined`, `charAt` gives `""`, `charCodeAt` gives `NaN` (Spec p.540).
- **Cut:** `slice` accepts negatives counting from the end; `substring` swaps out-of-order arguments (Spec p.551, p.553).
- **Split:** `split` and `join` (EJpt p.93); `split("")` breaks surrogate pairs [inference] (Spec p.551–552).
- **Pad, repeat, trim:** `padStart`, `repeat` (`RangeError` for negative or `Infinity`), `trim` (Spec p.546–548, p.555–556; EJpt p.92–93).
- **Replace:** `replace` with a string replaces only the first; `replaceAll` replaces all and throws `TypeError` with a RegExp without `g` (Spec p.548, p.550); version not stated. Patterns `$&`, `$n`, `$<name>`; with a string search there are no groups, so `$1` stays literal (Spec p.548–550; EJpt p.203–204). The replacement function receives `(match, groups..., position, string)` (Spec p.605; EJpt p.204).
- **Case and normalization:** `toLowerCase`/`toUpperCase` can change the length (Spec p.553–554); `normalize` (default NFC; an invalid form gives `RangeError`) (Spec p.546).
- **Building text:** template literal with `${}` (EJpt p.20). For HTML, build DOM nodes instead of concatenating (EJ1 p.93–94; EJpt p.301–303).
- **Unicode:** strings are 16-bit units; `length` and `str[i]` count units; emoji take two (EJpt p.118–119). `codePointAt` and `for-of` work with code points (EJpt p.119; Spec p.541, p.557). `isWellFormed` and `toWellFormed`: version not stated (Spec p.543, p.555).

**EJ1 [DATED].** No `includes`/`startsWith`: it writes `startsWith` with `slice` (EJ1 p.51–52) and uses `indexOf`/`charAt` (EJ1 p.50–52). Prefers `join` over `+=` for the performance of the time (EJ1 p.96–97). Nothing about surrogate pairs.

### D11.2 When to use regex?

**Criteria.** Does the pattern have structure (alternative, repetition, group)? Do I need to extract parts? Is the input trusted?

- For structure (dates, INI, comments) use regex (EJpt p.198, p.210–212, p.204–206). In EJ1, extracting the date with `match` is better than slicing by position, because it validates the format (EJ1 p.181). Resist using them for what they do not express well (EJpt p.214–215).
- Literal `/abc/` or `new RegExp("abc", "gi")`; in the string, double the backslash (`"\\s"`) (EJpt p.189, p.206). Escape interpolated text before building the pattern (EJpt p.206–207).
- Anchors `^`/`$`: without them the regex matches at any position and produces rare bugs (EJpt p.198, p.212). `\b` uses the simplistic `\w` (EJpt p.199).
- **Non-English text:** `\w` covers only ASCII; use `\p{L}` with the `u` flag (EJpt p.192–193). In the Spec, `\p{...}` only accepts names from the tables, case-sensitive, otherwise `SyntaxError` (Spec p.593–597). Without `u`, `.`, `?` and `{n}` operate on code units (EJpt p.212–213; Spec p.571). Mode `v`: version not stated, absent from EJpt (Spec p.590–592).
- **Greedy or lazy:** `+ * ? {}` match the maximum; with a `?` after, they match the minimum (EJpt p.204–206; Spec p.575–576). Many bugs come from unwanted greediness (EJpt p.206).
- **Performance:** patterns that match the same stretch in many ways (`/([01]+)+b/`) grow exponentially (EJpt p.202–203).
- **State pitfalls:** `lastIndex` only matters with `g` or `y` (EJpt p.208; Spec p.610); a shared global regex may start at a residual index (EJpt p.209); `test` with `g` alternates results [inference] (Spec p.610). `match` with `g` returns only the strings (EJpt p.209; Spec p.603). `matchAll` requires `g` and returns an iterable (Spec p.546; EJpt p.209–210). `split` with a regex ignores `g` and `y` (Spec p.608).
- Look-ahead `(?=)` and `(?!)` do not consume (EJpt p.199). A non-participating group is `undefined` and a repeated group keeps the last capture (EJpt p.196; Spec p.575, p.577).

**EJ1 [DATED].** Equivalent basic syntax (EJ1 p.177–184); no `\p`, `u`, `y`, `matchAll`. The book says that `{,4}` means four or fewer (EJ1 p.179); the Spec does not list that form (Spec p.582): do not reproduce.

---

## 12. Immutability

### D12.1 Mutate or copy?

**Criteria.** Do I need the previous value (undo, compare by identity)? Is there asynchronous code? Is the data huge?

- Primitives are immutable; objects are mutable and compared by identity (EJpt p.81–82). Pure functions are easy to combine and test, with no obligation to avoid the impure ones (EJpt p.68–69).
- Copy with `slice`/`concat` (EJpt p.91–92), array and object spread (EJpt p.94–95) and `{...state, ...action}` (EJpt p.435). In object spread, the last value wins (EJpt p.95).
- Persistent structures behave like strings and numbers and make it easier to manage complexity, even though the design is harder without help from the language (EJpt p.156–157). Gains shown: comparing by identity to avoid work (EJpt p.436–437), redoing the rectangle from the original state (EJpt p.442–443), undo history (EJpt p.449).
- In asynchronous code, computing new values is less error-prone than mutating (EJpt p.259).
- With a lot of data, mutating can pay off (EJpt p.117).

### D12.2 `Object.freeze` or convention?

- EJpt prefers convention: with `freeze` writes are silently ignored, which confuses as much as an error (EJpt p.157).
- Spec: `freeze` makes own properties non-configurable and data properties non-writable; accessors only become non-configurable (Spec p.106); in strict mode, writing throws `TypeError` (Spec p.317). A primitive passed to `freeze` comes back without error, and `isFrozen` of a primitive is `true` (Spec p.463, p.465); this treatment is from ES2015 [VERSION-DEPENDENT] (Spec p.868). It is shallow [inference] (Spec p.106). `seal` and `preventExtensions`: Spec p.465–466.

### D12.3 Shallow and deep copy

- `Object.assign` copies own enumerable properties (strings and symbols), with `Get`/`Set`, firing getters and setters (Spec p.461). Object spread is equivalent to `CopyDataProperties` [inference]: a nullish source is not an error (Spec p.109).
- There is no built-in deep copy in the sources; `structuredClone` is not mentioned. EJpt only writes `deepEqual` (EJpt p.104).

### D12.4 Array methods

Mutate: `push`, `pop`, `shift`, `unshift` (EJpt p.77, p.90), `sort`, `reverse`, `splice`, `fill` (Spec p.622–623, p.636–640). Do not mutate: `slice`, `concat` (EJpt p.91–92), `map`, `filter`, `flat` (Spec p.623–631), and `toSorted`, `toReversed`, `toSpliced`, `with` (version not stated; `with` throws `RangeError` out of range) (Spec p.640–643).

**EJ1 [DATED].** Reinforces `concat` (new) against `push` (mutates): extending a route with `push` corrupts the branches (EJ1 p.111). Functions that mutate the received set are accepted by design (EJ1 p.54–55).

---

## 13. Destructuring, rest and spread

### D13.1 Rest, spread or `arguments`/`apply`?

| Need | Current choice | EJ1 [DATED] |
|---|---|---|
| Variable number of arguments | rest `...nums` (EJpt p.94) | `arguments` (EJ1 p.64) |
| Array as arguments | `f(...a)` (EJpt p.94; Spec p.296) | `apply(null, a)` (EJ1 p.79–80) |
| Join arrays | `[...a, ...b]` (EJpt p.94) | `concat` (EJ1 p.99) |
| Copy an object changing fields | `{...o, y: 5}` (EJpt p.95) | none |

- Rest is the last parameter (EJpt p.94). Spread in a call uses a synchronous iterator; a non-iterable fails in `GetIterator` (Spec p.296).

### D13.2 Destructuring

**Criteria.** Can the source be nullish? Do I need defaults?

- Array `[a, b]` and object `{name}`, in `let`/`const`/`var` and parameters (EJpt p.97–98, p.115, p.163). `_` discards positions (EJpt p.198).
- Destructuring `null`/`undefined` throws an error (EJpt p.98); in the Spec, an object pattern does `RequireObjectCoercible`, even with `{}` (Spec p.319–320). An array pattern uses an iterator and closes it if it did not finish (Spec p.320–321).
- A default only fires with `undefined`, not with `null` (Spec p.321; EJpt p.59, p.451).
- Object rest: a new object with the remaining own enumerable properties [inference] (Spec p.320, p.322). A declaration with a pattern requires an initializer (Spec p.328).
- Parameters with defaults or destructuring make the list non-simple and forbid `"use strict"` in the body (Spec p.357–360).

**EJ1 [DATED].** No destructuring, rest or spread in the sources.

---

## 14. undefined, null, `?.` and `??`

### D14.1 Default value: `||`, `??` or default parameter?

- `||` returns the left side if truthy; `0`, `NaN` and `""` also fall to the default (EJpt p.25–26; Spec p.313). `??` only falls on `null`/`undefined`, and EJpt considers it generally preferable (EJpt p.26; Spec p.313).
- A default parameter only for a missing or `undefined` argument (EJpt p.59).
- `a ||= b`, `a &&= b`, `a ??= b` do not assign when there is short-circuiting, so setters do not fire (Spec p.316); they require a simple target (Spec p.315). `??` does not mix with `&&`/`||` without parentheses [inference] (Spec p.313).

**EJ1 [DATED].** Only `||`/`&&`, for example `input || "dear"` (EJ1 p.28–29).

### D14.2 `undefined` or `null`?

- The difference is a design accident; treat them as almost interchangeable (EJpt p.23–24; EJ1 p.26).
- `undefined` arises in a binding without a value (EJpt p.31), a function without `return` (EJpt p.52), a missing argument (EJpt p.58), a nonexistent property (EJpt p.78) and a `find` without a result (EJpt p.120). EJpt uses `null` for "not found" on purpose (EJpt p.63–64, p.117–118), and `localStorage` returns `null` [HOST] (EJpt p.425).
- `typeof null` is `"object"` (Spec p.305; EJpt p.104). `typeof` of an undeclared name gives `"undefined"` without throwing (Spec p.305).
- Absent property or one with value `undefined`: `in` (own and inherited) or `Object.hasOwn` (EJpt p.80, p.138; Spec p.310, p.464).

### D14.3 Optional access

- `a?.b` gives `undefined` if `a` is nullish; also `a?.[0]` and `f?.()` (EJpt p.98). In the Spec the whole chain short-circuits and only `undefined`/`null` trigger it (Spec p.297); `a?.b()` preserves `this` (Spec p.298); `?.` followed by a template is a `SyntaxError` (Spec p.291).
- Do not use it to hide a bug: reading a property of `null` throws an error, and that usually indicates a defect [inference] (EJpt p.76; EJ1 p.44).

---

## 15. JSON

### D15.1 How to serialize and read data?

- `JSON.stringify` and `JSON.parse` (EJpt p.100); JSON requires names in double quotes, only simple data, no comments (EJpt p.99). `localStorage` stores only strings (EJpt p.424); `JSON.parse(null)` returns `null` (EJpt p.425). `postMessage` accepts only values representable in JSON, received by copy (EJpt p.335) [HOST]. `response.json()` rejects if the body is not JSON (EJpt p.407).
- **`stringify` (Spec p.739–745).** Order: `toJSON`, replacer, unwrapping of wrappers (Spec p.742). `undefined`, functions and symbols vanish in objects and become `null` in arrays (Spec p.741–744). `NaN`/`Infinity` become `null` (Spec p.741–742). BigInt throws `TypeError`; so does a cycle (Spec p.741–744). `Date` has `toJSON` (Spec p.533). `Map` and `Set` serialize as empty [inference] (Spec p.743–744). `stringify(undefined)` returns `undefined` (Spec p.742).
- **`parse` (Spec p.735–738).** Invalid text throws `SyntaxError`; duplicate key: the last one counts; `reviver` runs from the inside out and returning `undefined` deletes. `rawJSON`: version not stated (Spec p.739).

**EJ1 [DATED].** Reads JSON with `eval("(" + json + ")")` and trusts the same domain (EJ1 p.234); do not use `eval`. The book's `serializeJSON` is manual (EJ1 p.235–237).

---

## 16. DOM and events [HOST]

Everything here is defined by the browser; the Spec does not cover the DOM.

### D16.1 Locate and change elements

- Avoid fixed paths from `document.body` (EJpt p.299). `getElementById` (EJpt p.300); `querySelector`/`All` with a CSS selector, non-live result (EJpt p.309–310); `getElementsByTagName` and `childNodes` are live; use `Array.from` for a stable loop (EJpt p.302). None is an array (EJpt p.297, p.310).
- Change: `createElement`, `appendChild`, `insertBefore`, `replaceChild`, `remove`; a node exists in only one place (EJpt p.300–303). Custom attributes: prefix `data-`; `class` is `className` (EJpt p.303–304). The `elt` helper of EJpt p.435 assigns properties, so `tabindex` becomes `tabIndex` (EJpt p.453).
- Styles: `style` in camelCase, a number requires a unit (EJpt p.307–308, p.313). Reading layout forces computation (EJpt p.305–306).
- Plain text: `nodeValue`/`textContent`; `innerHTML` interprets HTML (EJ1 p.198–199). The risk of HTML injection is not mentioned in the sources.

**EJ1 [DATED].** Words renamed because of IE (`className`, `htmlFor`), tables with `tbody` (EJ1 p.200–203).

### D16.2 Events

- `addEventListener` accepts several handlers; `onclick` only one (EJpt p.320). `removeEventListener` requires the same function (EJpt p.320).
- Propagation up to the window; `stopPropagation` interrupts; `target` and delegation avoid one handler per element (EJpt p.321–323). `preventDefault` cancels the default action (EJpt p.323); on `scroll` it does not prevent scrolling (EJpt p.332).
- Typed text: the `input` event, not key events (EJpt p.325–326, p.417); `change` on text only on losing focus (EJpt p.417). `submit` with `preventDefault` validates or uses `fetch` (EJpt p.415–416).
- Frequent events: *debounce* (EJpt p.336–337). Handlers wait for the current script; a heavy task delays interaction, use *web workers* (EJpt p.333–335). Animation with `requestAnimationFrame` and time difference (EJpt p.311–312).

**EJ1 [DATED].** Two event models (`attachEvent` in IE and `addEventListener`), `window.event`, `srcElement`, `keyCode` (EJ1 p.209–216). It is still worth detecting the feature, not the browser (EJ1 p.194–195, p.209–210).

### D16.3 Network data and storage

- `fetch(url)` returns a promise of `Response`; `response.text()`/`json()` another promise; options `{method, body, headers}` (EJpt p.406–408). Requests to another domain require `Access-Control-Allow-Origin` (EJpt p.408–409).
- `GET` without side effects; `POST`/`PUT`/`DELETE` to change state (EJpt p.406, p.475–476). `localStorage` persists strings, `sessionStorage` until the end of the session (EJpt p.423–425).
- Larger applications: a single state, interface derived from it, actions with `dispatch` (EJpt p.431–433, p.497). Real time: *long polling* with `ETag`/`If-None-Match` (EJpt p.483–487).
- DOM, SVG or canvas: DOM/HTML for text and interface, SVG for sharp manipulable graphics, canvas for pixels and many tiny elements; canvas requires clearing and redrawing (EJpt p.373, p.394–396).

**EJ1 [DATED].** `XMLHttpRequest` with `ActiveXObject` in IE (EJ1 p.231–234); only the origin domain (EJ1 p.231).

---

## 17. Errors and truncated passages in the sources (do not reproduce)

**Content errors.**
- `prompt` example that says "square root" but computes the square: EJpt p.35–37; EJ1 p.17.
- `serveFromRouter` uses `String(err)` in a `catch (error)`: EJpt p.491.
- `self.content = null` instead of `this.content`: EJ1 p.226.
- `{,4}` as a quantifier: EJ1 p.179.
- `matchAll` described as an array of arrays, but used with `for-of`: EJpt p.210; the Spec says iterator (Spec p.546).
- `formatDate`: the regex `M(MMM)?` accepts only `M` or `MMMM`, and `"M"` returns `getMonth()` without adding 1: EJpt p.227.
- Installation of "a specific version of mime" when the package is `mime-types`: EJpt p.474.
- 52-bit mantissa corrected to 53 in a note; six types without `null`; `arguments` called an array: EJ1 p.10, p.29, p.9, p.79 (versus p.64).
- `Script : [empty]` returns `undefined` in a Boolean algorithm: Spec p.398. `[[EvaluationError]]` described in two ways: Spec p.408.

**Truncations and extraction losses.** EJpt p.159 (sentence cut off), p.234 (exercise cut off), p.387 (`branch` code missing), p.463 (`package.json` missing), p.84 (pizza table), p.460 (REPL result), p.448 ("162" for 16²). EJ1 p.188 (`timeWriter`), p.203 ("starting with ts"), p.247 (note in the middle of the code). Spec p.136, p.345, p.397, p.444 (sections cut off); Spec p.419–422 (tables without values). The markers "Display hints..." and "◂ ● ▸ ?" are not content.

---

## 18. Divergences between sources

In each item: what each source states and which prevails. General rule: the Spec is the norm, EJpt the modern explanation, EJ1 dated.

1. **Block scope.** EJ1 p.34: blocks do not create scope. EJpt p.52–53: `let`/`const` have block scope. Spec p.326: each block creates an environment. Spec and EJpt prevail.
2. **Hoisting.** EJ1 p.39 and EJpt p.55: declarations hold in the whole scope. Spec: `var`-like at the top of a Script/function (Spec p.135–136), lexical in a module (Spec p.126), initialized on block entry (Spec p.326–327); the legacy web semantics creates an outer `var` [HOST] [DATED] (Spec p.400–401). The Spec prevails.
3. **Falsy values.** EJ1 p.26–28: `0`, `""`, `null`, `undefined`, `false`, `NaN`. EJpt p.26: `0`, `NaN`, `""`. Spec p.89 adds `-0` and `0n`. The Spec prevails.
4. **Default value.** EJ1 p.28–29 uses `||`; EJpt p.26 prefers `??`. The choice is by criteria (D14.1).
5. **Maps.** EJ1 p.129–132 uses `hasOwnProperty`/`Dictionary`; EJpt p.136–138 uses `Map`, `Object.create(null)`, `Object.hasOwn`. Spec and EJpt prevail.
6. **Prototypes.** EJ1 p.151–152: no `Object.create`; EJpt p.130 and Spec p.461–462: `Object.create`.
7. **Inner `this`.** EJ1 p.141–142: `self`/`bind`; EJpt p.128 and Spec p.364: arrow.
8. **What to throw.** EJ1 p.75: strings rarely serve; EJpt p.176 and Spec p.352–353: any value. EJ1's recommendation holds as good practice [inference]; EJpt p.473 throws a plain object.
9. **Cost of recursion.** EJ1 p.36: about ten times; EJpt p.62: about three. Measurements of their time; do not cite as a rule.
10. **Safe integers.** EJ1 p.10: below 2^52 (corrected in EJ1 p.29 to 53 bits); EJpt p.15–16: range of 9 quadrillion; Spec p.489: 2^53 − 1. The Spec prevails.
11. **Types.** EJ1 p.9: six types; EJpt p.27: four categories; Spec p.305 includes `symbol` and `bigint`. The Spec prevails.
12. **JSON.** EJ1 p.234: `eval`; EJpt p.99–100 and Spec p.735: `JSON.parse`.
13. **Events.** EJ1 p.208–217: IE and standard models; EJpt p.319–326: `addEventListener`, `event.key`. EJpt prevails [HOST].
14. **Leaving `forEach`.** EJ1 p.107–108: `Break` exception; EJpt p.118, p.122–123 and Spec p.622, p.636: `some`/`every`.
15. **`with`.** EJ1 p.241: presented without a warning; EJpt p.170: removed in strict mode and not discussed; Spec p.347: LEGACY, `SyntaxError` in strict mode. The Spec prevails.
16. **Modules.** EJ1 p.167–172: modules by convention (that the language had no built-in system is **[inference]**, p.167 does not state it); EJpt p.220–229: ESM since ES2015, CommonJS legacy; Spec p.398–444. Spec and EJpt prevail.
17. **Timers with a string.** EJ1 p.145: accepts a function or a code string; EJpt p.335–336: function only. The string is [DATED] and risky like `eval`.
18. **Stack error.** No source names the type (EJpt p.58; EJ1 p.37).

---

## 19. Gaps

What the sources consulted for this file do not cover, or cover only in part:

- **Promise.** EJpt only treats `Promise.all` (EJpt p.254–255). `allSettled`, `any`, `race`, `finally`, `try` and `withResolvers` appear only in the Spec (Spec p.771–778), without an edition.
- **Async iteration.** `for await` and async generators only in the Spec (Spec p.338, p.372–375).
- **Structures.** `WeakMap`, `WeakSet`, `WeakRef`, set algebra, `Object.groupBy`/`Map.groupBy` only in the Spec; `structuredClone` is not mentioned; Proxy and Reflect without a decision tree.
- **Errors.** The exact type of the error for an exhausted stack, for access to a missing private field and for reassigning a `const` (here [inference], Spec p.167).
- **ASI.** EJpt says to always use `;` (EJpt p.29–30); the rules are in the Spec (Spec p.269–271), with no criterion for when to omit.
- **Outside the sources:** tests beyond a mention of test runners (EJpt p.171–173), TypeScript beyond one mention (EJpt p.171), linters, `AbortController`, `queueMicrotask`, DOM observers, accessibility, DOM security (XSS, `innerHTML`), ReDoS (only the warning of EJpt p.202–203).
- **Node.js.** Only the basics (EJpt p.458–480).
- **EJ1.** Has no `let`/`const`, arrow, `class`, Promise, `async`, modules, destructuring, rest/spread, `for-of`, `Map`/`Set`: every recommendation of it is [DATED].
- **Versions.** The Spec does not state the edition of `replaceAll`, `matchAll`, `at`, `flat`, `toSorted`, `Object.hasOwn`, `Promise.any`, top-level `await`, private fields, `cause`, mode `v`, among others; the annexes only record incompatibilities (Spec p.865–869).
- **Terms.** The sources do not use "object composition" as an alternative to inheritance (D6.1 is [inference]).
