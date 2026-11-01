# JavaScript cases, pitfalls and anti-patterns

This file gathers, for quick lookup, what usually goes wrong in JavaScript, why it goes wrong, how to fix it and what to avoid. Grep for the topic heading (for example `## 2.11`) or for the error message. Every row carries its source with the PDF page: `Spec` = ECMA-262, 17th edition (ES2026), normative; `EJpt` = *Eloquent JavaScript* in Portuguese, modern edition; `EJ1` = *Eloquent JavaScript*, 1st edition (2007/2013), entirely **[DATED]**. Where the standard, the modern explanation and the old book disagree, the Spec prevails; see section 6.

## Table of contents

1. Conventions, labels and columns
2. Part 1 — Tables by topic
   - 2.1 Coercion and equality
   - 2.2 Numbers (floating point, NaN, BigInt, parseInt)
   - 2.3 Strings and Unicode
   - 2.4 Arrays (holes, sort, copy and alias, length)
   - 2.5 Objects and prototypes
   - 2.6 `this` and arrow functions
   - 2.7 Scope, hoisting, TDZ and closures in loops
   - 2.8 Automatic semicolon insertion (ASI)
   - 2.9 Classes
   - 2.10 Iterators and generators
   - 2.11 Asynchronous code
   - 2.12 Modules and packages
   - 2.13 Regular expressions
   - 2.14 Date
   - 2.15 JSON
   - 2.16 Native errors: when they occur
   - 2.17 `eval`, `with` and `Function` [DATED]
   - 2.18 Other built-in objects (Proxy, collections, buffers)
   - 2.19 [HOST]: DOM, events, network, canvas, Node
3. Part 2 — Anti-patterns and the alternative
4. Part 3 — Annex B and legacy to avoid
5. Part 4 — Errors and inconsistencies in the books and in the extracted text (do not reproduce)
6. Divergences between the sources
7. Gaps

## 1. Conventions, labels and columns

- Table columns: **Symptom or message | Cause | Fix | Source | Origin | Era**. "Origin" says which source supports the row (Spec, EJpt, EJ1 or a combination).
- "Era": `current` (holds in the 2026 Spec and in the modern book); `[DATED]` (all of EJ1, Annex B, `with`); `[VERSION-DEPENDENT]` (the source attributes it to a specific edition); `[HOST]` (defined by the environment: browser, Node, DOM, timers, `console`, `fetch`); `version not stated` (the sources do not say since when it exists).
- Labels in the body: **[inference]** is a connection made here; **[extrapolation]** is knowledge outside the sources, used only when indispensable.
- The Spec does not give error message names; the messages quoted by the books vary by engine (EJpt p.76; EJ1 p.44).
- The example code is short and rewritten; it is not copied from the books.

## 2. Part 1 — Tables by topic

### 2.1 Coercion and equality

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `"5" + 1` gives `"51"`, but `"5" - 1` gives 4 | `+` tries to concatenate; `-` converts to number. In the Spec, `+` applies ToPrimitive and concatenates if either side becomes a string | Convert beforehand with `Number(...)`; avoid numeric operators on strings | EJpt p.24, p.35; Spec p.317; EJ1 p.28 | EJpt+Spec+EJ1 | current |
| `"five" * 2` and `8 * undefined` give `NaN`, and the `NaN` contaminates the following calculations | Converting non-numeric text to a number produces NaN | Look for accidental conversion; test with `Number.isNaN` | EJpt p.24, p.36; EJ1 p.28 | EJpt+EJ1 | current |
| `0 == false` and `"" == false` are true, `"" === false` is false | `==` converts different types; Boolean becomes Number before comparing | Use `===` and `!==` by default | EJpt p.25; Spec p.102 | EJpt+Spec | current |
| `null == 0` is false, `null == undefined` is true | With `null`/`undefined` on one side, only those two are `==` to each other | `x == null` works as a "no value" test when intentional | EJpt p.24–25; Spec p.101–102; EJ1 p.26 | EJpt+Spec+EJ1 | current |
| `variable == false` also holds for `0` and `""` | `==` coercion | Explicit `=== false` or `=== null` | EJ1 p.26–27 | EJ1 | [DATED] |
| `if (value)` rejects valid `0`, `""` and `NaN` | Falsy: `0`, `NaN`, `""`, `null`, `undefined`, `false` (and `0n`) | Compare explicitly; use `??` | EJpt p.26; EJ1 p.26–28; Spec p.89 | EJpt+EJ1+Spec | current |
| `x \|\| 100` replaces `0` with 100 | `\|\|` tests falsiness and returns one of the operands | `x ?? 100` only replaces `null`/`undefined` | EJpt p.26; Spec p.313 | EJpt+Spec | current |
| `a ?? b` mixed with `&&`/`\|\|` without parentheses | The `??` grammar accepts BitwiseOR on each side, not `&&`/`\|\|` | Explicit parentheses **[inference]** | Spec p.313 | Spec | current |
| `new String("a") == "a"` and `"a" == new String("a")` are true, but two equal wrappers are `==` false | `==` is not transitive; wrappers are objects compared by identity | Work with primitives; avoid `new String`, `new Boolean` | Spec p.312, p.476 | Spec | current |
| Two objects with the same content give `==` false | `==` and `===` on objects compare identity | Write a deep comparison (`deepEqual`) | EJpt p.82, p.104; EJ1 p.46; Spec p.102 | EJpt+EJ1+Spec | current |
| `NaN == NaN` is false | NaN is the only value different from itself | `Number.isNaN(x)`, `x !== x` or `Object.is` | EJpt p.22; EJ1 p.28; Spec p.453, p.465 | EJpt+EJ1+Spec | current |
| `isNaN("abc")` is true; `isFinite("12")` is true | The global functions coerce the argument; the `Number` ones do not | Prefer `Number.isNaN` and `Number.isFinite` | Spec p.452–453, p.488–489 | Spec | current |
| `typeof null` gives `"object"` | Spec rule (historical accident according to the book) | Test `x === null` before `typeof x === "object"` | Spec p.305; EJpt p.104 | Spec+EJpt | current |
| `typeof undeclared` does not throw | An unresolvable reference in `typeof` returns `"undefined"` | Use it to detect an optional feature | Spec p.305 | Spec | current |
| `date + 1` concatenates text; `date - 1` subtracts | Date treats the "default" hint as "string" | Use `getTime()`/`Number(date)` for arithmetic | Spec p.318, p.537 | Spec | current |
| `TypeError` when doing `"" + symbol` or `Number(symbol)` | ToString and ToNumber of Symbol throw | `String(symbol)` or `.description` | Spec p.89, p.96, p.480, p.538 | Spec | current |
| `"Z" < "a"` is true; `"10" < "9"` is true | String comparison by UTF-16 code unit, with no dictionary order or normalization | `localeCompare` (order depends on the environment) or a numeric comparator | EJpt p.21; Spec p.101, p.544; EJ1 p.13 | EJpt+Spec+EJ1 | current / [HOST] |
| `<=` and `>=` with `NaN` give `false` | The undefined comparison result becomes false | Handle NaN first | Spec p.309 | Spec | current |
| `1n + 1` throws `TypeError` | Operators do not mix Number and BigInt | Convert explicitly (`BigInt(n)` or `Number(b)`) | Spec p.317, p.88 | Spec | current |
| `"a" in "text"` throws `TypeError` | The right-hand side of `in` must be an object | Use `includes`/`indexOf` on strings | Spec p.310 **[inference]** | Spec | current |
| Template with a symbol in `${}` throws an error | Template conversion is ToString, not the `+` one | `String(symbol)` | Spec p.288 | Spec | current |

### 2.2 Numbers (floating point, NaN, BigInt, parseInt)

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| Inexact fractional results | 64-bit numbers: integers below the limit are exact, fractions are approximations | Treat fractions as approximations; `Number.EPSILON` is available, and using it as a tolerance is **[extrapolation]** | EJpt p.16; EJ1 p.10; Spec p.488 | EJpt+EJ1+Spec | current |
| Large integers "stick": 9007199254740992 and ...993 are the same Number | Above 2^53−1 several integers share one Number | `Number.isSafeInteger`; use BigInt | Spec p.489 | Spec | current |
| Book says 52 bits of precision, note says 53 | Simplification in the old book | Follow the Spec (limit 2^53−1) | EJ1 p.10, p.29; Spec p.489 | EJ1+Spec | [DATED] |
| Calculations with `Infinity` become `NaN` (`Infinity - Infinity`, `0/0`) | Indeterminate forms | Validate inputs | EJpt p.17–18 | EJpt | current |
| `Math.max()` with no arguments gives `-Infinity`; `Math.min()` gives `+Infinity`; a NaN is contagious | Initial values of the reduction | Check for an empty array; use spread for arrays | Spec p.505–506; EJpt p.94 | Spec+EJpt | current |
| `Math.round(-3.5)` is -3; `Math.round(-0.5)` and `Math.ceil(-0.5)` give `-0` | Ties go toward +Infinity; negative zero is preserved | `Object.is` distinguishes `-0`; add `0` if the sign is a problem **[extrapolation]** | Spec p.501, p.506 | Spec | current |
| `Math.random()` repeats or seems predictable | Pseudorandom in [0, 1); no seed and no cryptographic guarantee | Integer: `Math.floor(Math.random() * n)`; security is outside the sources | EJpt p.96–97; Spec p.506 | EJpt+Spec | current / [HOST] |
| `parseInt("-0")` gives `-0`; radix outside 2–36 gives `NaN`; text after the digits is ignored | Prefix reading; without radix it uses 10, or 16 with `0x` | Pass the base explicitly **[extrapolation]**; validate the whole text | Spec p.453–454 | Spec | current |
| `parseFloat("3.14abc")` gives 3.14, but `Number("3.14abc")` gives `NaN` | `parseFloat` reads the longest prefix; `Number` requires the whole string | Choose according to the rigor wanted | Spec p.89–90, p.453 | Spec | current |
| `Number("")` and `Number("  ")` give 0; `Number("1_000")` gives `NaN` | StringToNumber: empty is 0 and the `_` separator is not valid in strings | Check for an empty string first | Spec p.89–90 | Spec | current |
| `Number("0b101")` and `Number("0o17")` convert | ES2015 change (it used to be NaN) | Know the environment's edition | Spec p.867 | Spec | [VERSION-DEPENDENT] |
| `BigInt(1.5)` throws `RangeError`; `new BigInt(1)` throws `TypeError`; `BigInt("x")` throws `SyntaxError` | The number must be an integer; BigInt is not a constructor; invalid string | `BigInt(Math.trunc(x))`; no `new` | Spec p.95, p.495 | Spec | current |
| `1n / 0n` and a negative exponent throw `RangeError`; `>>>` with BigInt throws `TypeError` | BigInt rules | Handle a zero divisor | Spec p.64–65, p.317 | Spec | current |
| `JSON.stringify` with BigInt throws `TypeError`; `+1n` throws `TypeError` | No implicit serialization or unary conversion | `toJSON` or `String(b)`; `Number(b)` | Spec p.742, p.305 **[inference]**, p.488 | Spec | current |
| `toFixed`, `toPrecision`, `toExponential`, `toString(radix)` throw `RangeError` | Arguments outside 0–100, 1–100, 0–100, 2–36 | Validate; `NaN.toFixed(500)` does not throw | Spec p.491–494 | Spec | current |
| `(1e21).toFixed(2)` returns exponential text; ties go to the larger | `toFixed` rule | Check the range | Spec p.492 | Spec | current |
| Bitwise operators "wrap" large values | ToInt32/ToUint32 reduce modulo 2^32 | Do not use for integers above 32 bits | Spec p.92–93 | Spec | current |
| `-2 ** 2` is a syntax error | The left side of `**` cannot be unary **[inference]** | `(-2) ** 2` | Spec p.306 | Spec | current |
| `x++` with `x = "5"` returns the number 5 | Postfix returns the old value already converted | Convert beforehand | Spec p.302 | Spec | current |

### 2.3 Strings and Unicode

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `length` of an emoji gives 2; `s[0]` returns half a character | Strings are 16-bit code units | `for...of`/spread walk code points; `codePointAt` | EJpt p.19, p.118–119; Spec p.50, p.557 | EJpt+Spec | current |
| `split("")` splits surrogate pairs | Splits by code unit | Spread the string with spread/`Array.from` **[inference]** | Spec p.552 **[inference]**, p.557 | Spec | current |
| `charAt` out of range gives `""`; `at` and `codePointAt` give `undefined`; `charCodeAt` gives `NaN` | Different return values for an invalid position | Choose the method knowing its return value | Spec p.540–541 | Spec | current |
| `String.fromCharCode(70000)` does not fail; `fromCodePoint(-1)` throws `RangeError` | `fromCharCode` reduces modulo 2^16; `fromCodePoint` validates | Use `fromCodePoint` for code points | Spec p.538–539 | Spec | current |
| `"papa".replace("p","m")` replaces only the first | A string as pattern replaces the first occurrence | `replaceAll` or a regex with `g` | EJpt p.203; EJ1 p.181; Spec p.548, p.550 | EJpt+EJ1+Spec | current |
| `replaceAll(/x/, ...)` throws `TypeError` | Regex without `g` | Add `g` | Spec p.550 | Spec | current |
| `$1` stays literal in `replace` with a string as the search | There are no groups when the search is a string | Use a regex with groups | Spec p.548–549 | Spec | current |
| `startsWith`, `endsWith`, `includes` throw `TypeError` with a regex; `indexOf` accepts it | Regex is rejected on purpose | Use text, or `test`/`search` | Spec p.541–543 | Spec | current |
| `substring(5, 2)` swaps the arguments; negatives become 0; `slice` counts from the end | Distinct rules | Prefer `slice` | Spec p.551, p.553 | Spec | current |
| `"a".repeat(-1)` and `repeat(Infinity)` throw `RangeError` | `count` validation | Validate | Spec p.547–548 | Spec | current |
| `padStart` does nothing with an empty fill or a smaller length | Returns the original | Check the arguments | Spec p.547 | Spec | current |
| `normalize("x")` throws `RangeError` | Only NFC, NFD, NFKC, NFKD | Pass a valid form | Spec p.546 | Spec | current |
| "Equal" strings compare as different | No normalization, no canonical equivalence in `===` | `normalize()` before comparing | Spec p.50, p.312, p.546 | Spec | current |
| `toUpperCase` changes the length; `up.lower` does not return to the original | Standard Unicode conversion, context-sensitive | Do not assume symmetry | Spec p.554 | Spec | current |
| `encodeURIComponent` throws `URIError` | Lone surrogate in the string | `toWellFormed()` beforehand | Spec p.456, p.555 | Spec | version not stated (`toWellFormed`) |
| Assigning a property to a string/number does not persist; changing a letter of a string does not work | Primitives are immutable; `new String("abc")[0] = "x"` fails | Create a new string | EJpt p.81, p.92; Spec p.219–221 | EJpt+Spec | current |
| A line break inside quotes is an error; inside backticks it is valid | Only templates accept a literal line terminator | Backticks or `\n` | EJpt p.18; EJ1 p.11; Spec p.261–266 | EJpt+EJ1+Spec | current |
| `SyntaxError` with `"\07"` or `\8` in strict | Legacy octal escape forbidden in strict | Use `\x07` or `\u0007` | Spec p.262–263 | Spec | [DATED] (legacy) |
| Template with `\01` or an incomplete `\u{`: error; with a tag, the cooked text is `undefined` | `NotEscapeSequence` is only valid in a tagged template | `String.raw` for raw text | Spec p.267, p.285, p.539 | Spec | current |
| `localeCompare` sorts differently across environments | Order depends on the host locale | Do not assume identical order | Spec p.544 | Spec | [HOST] |

### 2.4 Arrays (holes, sort, copy and alias, length)

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `new Array(3)` creates 3 holes; `Array("3")` creates `["3"]`; `new Array(1.5)` throws `RangeError` | A numeric argument is the length | `Array.of(7)`, `Array.from({length: 3}, fn)`, `new Array(n).fill(v)` | Spec p.615–616, p.618; EJpt p.434 | Spec+EJpt | current |
| `forEach`, `map`, `indexOf`, `some` skip holes; `includes`, `find*`, `toSorted` read them as `undefined` | They test `HasProperty` or not | Avoid sparse arrays; fill them | Spec p.625, p.628, p.641 | Spec | current |
| `[10, 9, 1].sort()` gives `[1, 10, 9]` | Without a comparator it sorts as strings | `sort((a, b) => a - b)` **[inference]** | Spec p.638 | Spec | current |
| `sort` with an invalid comparator throws `TypeError`; an inconsistent comparator gives implementation-defined order | Validation and contract | A consistent comparator without side effects | Spec p.636–638 | Spec | current |
| `sort`, `reverse`, `splice`, `fill`, `copyWithin` change the original | They operate in place | `toSorted`, `toReversed`, `toSpliced`, `with` | Spec p.640–643 | Spec | version not stated |
| `with(i, v)` throws `RangeError` out of range; `at` returns `undefined` | Different rules | Check the index | Spec p.619, p.643 | Spec | version not stated |
| `const b = a` and changing `b` changes `a` | Same object (identity) | `slice()`, spread, `concat` (shallow copy) | EJpt p.81–82, p.91, p.94; EJ1 p.46 | EJpt+EJ1 | current |
| `const` with an array/object still allows `push` | `const` prevents rebinding, not mutating the value | `Object.freeze` (shallow) or an immutability convention | EJpt p.82, p.157 | EJpt | current |
| `length = 2` deletes elements; a non-configurable element locks `length` | Reducing `length` deletes | Be careful with `length` | EJ1 p.67; Spec p.219, p.644 | EJ1+Spec | current |
| `arr.length = -1` throws `RangeError` | Length must be uint32 | Validate | Spec p.219 | Spec | current |
| `[1,2,]` has length 2, `[1,2,,]` has 3 | Only one trailing comma is a terminator | Avoid double commas | Spec p.278 | Spec | current |
| `reduce` on an empty array with no initial value throws `TypeError` | There is no initial accumulator | Pass an initial value | Spec p.632–633; EJpt p.115 | Spec+EJpt | current |
| `includes(NaN)` finds it, `indexOf(NaN)` does not | SameValueZero versus `===` | Choose according to the case | Spec p.628–630 | Spec | current |
| `typeof []` is `"object"`; `instanceof Array` fails across windows | Arrays are objects | `Array.isArray` | EJpt p.80; EJ1 p.235; Spec p.618 | EJpt+EJ1+Spec | current |
| `concat` with a non-array argument treats it as one element | Only arrays (or `isConcatSpreadable`) are spread | Wrap it in an array | EJpt p.91–92; Spec p.620 | EJpt+Spec | current |
| `push`, `concat`, `splice` throw `TypeError` at the 2^53−1 limit | Length ceiling | Practically rare | Spec p.620, p.631, p.639 | Spec | current |
| `NodeList`/`childNodes`/`arguments` have no `map`/`slice` | Array-like, not an array | `Array.from(x)`, rest parameters | EJpt p.297, p.302; EJ1 p.64, p.196 | EJpt+EJ1 | [HOST] / [DATED] |
| `filter`+`map` create intermediate arrays | Each step produces a new array | A single loop on huge arrays processed many times | EJpt p.117 | EJpt | current |
| Mutating during iteration: appended items are not visited | Range fixed before the 1st call | Do not mutate the iterated array | Spec p.622, p.627 | Spec | current |

### 2.5 Objects and prototypes

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `TypeError` when reading a property of `null`/`undefined` | Only those two values have no properties | `?.`; validate beforehand | EJpt p.76, p.98; EJ1 p.44; Spec p.81 | EJpt+EJ1+Spec | current |
| A typo in a property yields `undefined` silently | A nonexistent property gives `undefined` | An access function that throws (`roadsFrom`); assertions | EJpt p.78, p.168; EJ1 p.105–106 | EJpt+EJ1 | current |
| `"toString" in map` is true | The object inherits from `Object.prototype` | `Map`, `Object.create(null)`, `Object.hasOwn` | EJpt p.136–138; EJ1 p.129; Spec p.464 | EJpt+EJ1+Spec | current |
| A key named `hasOwnProperty` breaks the check | It overrides the inherited method | `Object.hasOwn(o, k)` | EJ1 p.130–131; EJpt p.138 | EJ1+EJpt | [DATED] / current |
| `for...in` shows inherited properties and prototype extensions | Walks the prototype chain, enumerable strings only | `Object.keys`, `for...of` over `Object.entries` | EJ1 p.129, p.133; Spec p.343–344 | EJ1+Spec | [DATED] |
| `for...in` over `null`/`undefined` does not fail, it just does not iterate | Header rule | Know that there is no error | Spec p.341–342 | Spec | current |
| Key order is surprising | Integers ascending first, then strings by creation, then symbols | Do not depend on insertion order for numeric keys | Spec p.202 | Spec | current |
| Assigning to an inherited property "does not change" the prototype | A write creates an own property; if the inherited one is not writable, the assignment fails | Change the prototype directly | EJpt p.134–135; EJ1 p.128; Spec p.196–197 | EJpt+EJ1+Spec | current |
| `n => {prop: n}` gives `undefined` | The braces become the function body | `n => ({prop: n})` | EJpt p.79 | EJpt | current |
| A statement starting with `{` is a block, not an object | An expression cannot start with `{`, `function`, `class`, `let [` | Parentheses | EJpt p.79; Spec p.332 | EJpt+Spec | current |
| `delete obj.x` is not the same as assigning `undefined` | `in` remains true with `undefined` | `delete` when absence matters | EJpt p.79–80 | EJpt | current |
| `delete` of a name in strict: `SyntaxError`; of a non-configurable property: `TypeError` | Strict rules | Avoid `delete` on variables | Spec p.304 | Spec | current |
| A number as key becomes a string: `{1.0: "x"}` creates `"1"` | Keys are strings | Know the conversion | EJpt p.76; EJ1 p.45; Spec p.282–283 | EJpt+EJ1+Spec | current |
| The computed key is converted only after the right-hand side in `a[b] = c` | Evaluation order | Avoid keys with a side-effecting `toString` | Spec p.293 | Spec | current |
| `{__proto__: x}` sets the prototype; a duplicate is `SyntaxError`; `["__proto__"]` creates an ordinary property | Special literal rule | Avoid `__proto__`; `Object.create` | Spec p.281, p.283–284 | Spec | current (accessor: legacy) |
| `Object.assign` triggers setters and is a shallow copy; it ignores `null` sources | Uses `Get`/`Set` | Spread for copying; copy deeply by hand | Spec p.461; EJpt p.80, p.95 | Spec+EJpt | current |
| Spread `{...x}` with `x` null does not throw | CopyDataProperties ignores `null`/`undefined` | Know this | Spec p.109, p.283 | Spec | current |
| `Object.freeze` is shallow; writing to a frozen object is ignored in sloppy and `TypeError` in strict | FROZEN level only on own properties | Freeze inner levels; use strict | EJpt p.157; Spec p.317, p.463 | EJpt+Spec | current |
| `Object.freeze(1)` does not fail | Primitives are returned (ES2015 change) | Know that it does not validate | Spec p.463, p.868 | Spec | [VERSION-DEPENDENT] |
| `const {a} = null` throws `TypeError`, even with `{}` | RequireObjectCoercible | Default value `= {}` in the parameter | EJpt p.98; Spec p.155, p.319–320 | EJpt+Spec | current |
| `a?.b = 1` and `f() = 1` | An optional chain is not a target; a call as a target is a runtime error (sloppy, browser) | Assign without `?.` | Spec p.159–161, p.859 | Spec | current / [HOST] |
| `Object.defineProperty` fails with `TypeError`; `Reflect.defineProperty` returns a boolean | Variants throw or not | Choose the variant | Spec p.104, p.799 | Spec | current |
| Descriptor with `get` and `value` together: `TypeError` | Mixing accessor and data | Only one type | Spec p.83–84 | Spec | current |
| A property created by `defineProperty` is non-writable and non-enumerable | Defaults are `false` | Declare the attributes | Spec p.84 | Spec | current |
| `Object.prototype.toString` does not identify the type reliably | `Symbol.toStringTag` changes the tag | Do not use it as a type test | Spec p.468 | Spec | current |
| Changing the prototype of `Object.prototype` fails | Immutable prototype | Do not try | Spec p.234, p.466 | Spec | current |

### 2.6 `this` and arrow functions

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `this` is undefined inside a nested function | Every ordinary function has its own `this` | Arrow function, `bind`, or store it in a variable | EJpt p.128; EJ1 p.141–142; Spec p.473 | EJpt+EJ1+Spec | current / [DATED] (manual `bind`) |
| An extracted method (`const f = obj.m; f()`) loses the object | `this` comes from the call, not from the definition | `bind`, arrow, always call via the object | EJ1 p.142; Spec p.294 | EJ1+Spec | current |
| `(0, obj.f)()` loses `this` | The comma operator returns a value, not a reference **[inference]** | Call `obj.f()` | Spec p.294, p.324 | Spec | current |
| Sloppy: `this` is the global; strict: `undefined` | `this` coercion only in non-strict | `"use strict"`, classes and modules | EJpt p.169; Spec p.473, p.861 | EJpt+Spec | current |
| A constructor called without `new` creates a global in sloppy; `class` throws | In strict `this` is `undefined` | Use `class` | EJpt p.169–170; Spec p.384 | EJpt+Spec | current |
| `new` on an arrow throws `TypeError` | An arrow has no `prototype` or constructor **[inference]** | Use `function`/`class` | Spec p.364 | Spec | current |
| Arrow without its own `arguments`, `super`, `new.target` | Resolved in the outer environment | Rest parameters | Spec p.364 | Spec | current |
| `call`/`apply`/`bind` do not change the `this` of an arrow or of an already bound function | They ignore `thisArg` | Define it as a `function` | Spec p.473–474 | Spec | current |
| `this` before `super()` in a derived class: `ReferenceError` | `this` not yet initialized | `super()` first | Spec p.172, p.295 | Spec | current |
| `this` at module top level is `undefined` | Module rule | Do not depend on the global | Spec p.179 | Spec | current |

### 2.7 Scope, hoisting, TDZ and closures in loops

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| A variable "leaks" from `if`/`for` | `var` only respects function scope; in EJ1 blocks do not create scope | `let` and `const` | EJpt p.52–53; EJ1 p.34; Spec p.128, p.328 | EJpt+EJ1+Spec | current / [DATED] |
| Forgetting `let` creates a global (sloppy) or `ReferenceError` (strict) | Assignment to an unresolvable name | `"use strict"`; modules | EJpt p.168–169; Spec p.81, p.861 | EJpt+Spec | current |
| The strict-mode error does not help if the name already exists in a visible scope | It overwrites the existing one | Review names | EJpt p.169 | EJpt | current |
| `ReferenceError` when using `let`/`const`/`class` before the declaration (TDZ) | The binding exists but is not initialized | Declare before using | Spec p.167–168, p.327, p.386 | Spec | current |
| `for (let x of x)` fails | `x` is in TDZ when evaluating the right-hand side **[inference]** | Distinct names | Spec p.341 | Spec | current |
| `TypeError` when reassigning `const`; `SyntaxError` for `const` without an initializer | Immutable binding | `let` if it will be reassigned | Spec p.167, p.328 | Spec | current |
| `SyntaxError` when redeclaring `let` or mixing `let` and `var` in the same scope | Lexical duplicate | Unique names | Spec p.326, p.328 | Spec | current |
| A function called before its declaration works; a function in a `const` does not | Function declarations are hoisted | Declare before use in expressions | EJpt p.55; EJ1 p.39; Spec p.154 | EJpt+EJ1+Spec | current |
| A function declared in a block behaves differently per engine | Legacy web semantics | Avoid; use a function expression with `const` | Spec p.855–856 | Spec | [DATED] [HOST] |
| Closures in a loop see the same counter | A single variable (`var`) | `let` creates a copy per iteration; `for...of` with `const` likewise | Spec p.337, p.342–343 **[inference]** | Spec | current |
| A closure sees the creation environment, not the calling one | Lexical scope | Plan what the closure captures | EJpt p.61; EJ1 p.35; Spec p.180 | EJpt+EJ1+Spec | current |
| Shadowing hides an outer binding | The innermost prevails | Distinct names | EJpt p.53; EJ1 p.33 | EJpt+EJ1 | current |
| Redefining `print`, `max` or built-in names gives no warning | JS does not prevent reuse of standard names; only `let`/`const` warn on redeclaration | Namespaces such as `Math` | EJpt p.95; EJ1 p.17, p.65–66 | EJpt+EJ1 | current |
| Extra arguments are ignored, missing ones become `undefined` | JS does not validate the count | Default parameters; assertions | EJpt p.58; EJ1 p.40–41 | EJpt+EJ1 | current |
| A default value only fires with `undefined`, not with `null` | Parameter and destructuring rule | `??` in the body for `null` | EJpt p.59; Spec p.157, p.321 | EJpt+Spec | current |
| `"use strict"` in a function with non-simple parameters: `SyntaxError` | Parameter list rule | Put the directive in the file | Spec p.360 | Spec | current |
| A parameter with the same name as a `let` in the body: `SyntaxError` | Lexical conflict | Rename | Spec p.360 | Spec | current |
| `var` and global functions become properties of the global object; `let`/`const` do not, and they shadow | Composite global environment | `let`/`const` at script top level | Spec p.173–175 | Spec | current |
| `let x` and a repeated `case`: `SyntaxError` in `switch` | A single scope for the whole `switch` | Braces in each `case` | Spec p.348, p.350 | Spec | current |
| `catch (e) { var e = 1 }` changes the catch's `e` | Annex B allows it in non-strict | Avoid | Spec p.857, p.868 | Spec | [DATED] |
| Stack overflow (recursion without a base case, `isEven(-1)`) | Call stack full; the exception type is not named in the sources | Ensure a base case | EJpt p.58, p.70–71; EJ1 p.37 | EJpt+EJ1 | current |
| Recursion is slower than a loop (3x in EJpt, 10x in EJ1) | A call costs more than an iteration | Measure before optimizing | EJpt p.62; EJ1 p.36 | EJpt+EJ1 | [DATED] (numbers) |
| Duplicate labels or `break` without a target: `SyntaxError`; `continue` only in a loop | Static check | Check labels | Spec p.139–144, p.346 | Spec | current |

### 2.8 Automatic semicolon insertion (ASI)

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `return` followed by a line break returns `undefined` | Restricted production: `;` is inserted right after | Expression on the same line as `return` | Spec p.271–272, p.347 | Spec | current |
| A line starting with `(`, `[`, a backtick, `+`, `-` or a regex continues the previous one | There is no ASI in these cases | Explicit `;` on the previous line | Spec p.272–273 | Spec | current |
| `a = b` and `++c` on the next line: the `++` does not belong to `b` | Postfix does not accept a line break | `++` attached to the operand | Spec p.272 | Spec | current |
| `if (a > b)` line break and `else` | A `;` that would be an empty statement is not inserted | Braces | Spec p.272 | Spec | current |
| `for (a; b` line break `)` does not complete | The header's `;` is never inserted | Write both `;` | Spec p.271 | Spec | current |
| `{ 1 2 } 3` is invalid | Without a line break, ASI does not help | — | Spec p.271 | Spec | current |
| `throw`, `break` with a label, `continue`, `yield` + line break | Restricted productions | Same line | Spec p.270–271 | Spec | current |
| Arrow with a line break before `=>`; `async` with a line break before the function | `;` inserted and `SyntaxError` | Same line | Spec p.270–271 | Spec | current |
| A `/* ... */` comment containing a line break counts as a line terminator | Comment rule | Be careful in `return /* \n */ x` | Spec p.251 | Spec | current |
| `a = b` and `/hi/g.exec(c)` becomes a division | The context allows the division `/` | Explicit `;` | Spec p.248 | Spec | current |
| `let` + line break + identifier becomes a declaration (ES2015) | Edition change | `let` on the same line | Spec p.867 | Spec | [VERSION-DEPENDENT] |
| Books recommend always using `;` | The omission rules are complex | Use `;` | EJpt p.29–30; EJ1 p.20 | EJpt+EJ1 | current |

### 2.9 Classes

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `TypeError` when calling a class without `new` | A class constructor is not callable | `new` | EJpt p.131, p.170; Spec p.384 | EJpt+Spec | [VERSION-DEPENDENT] (`class` is ES2015 according to EJpt p.132) |
| `extends` of a non-constructor or with an invalid `prototype`: `TypeError` | Inheritance validation | Extend a class/constructor function | Spec p.384 | Spec | current |
| `super()` twice: `ReferenceError`; `this` before `super()`: `ReferenceError` | `this` binding | Call `super()` once, first | Spec p.172, p.295 | Spec | current |
| `super()` in a class without `extends` or in an ordinary method: `SyntaxError` | Only in the derived constructor | — | Spec p.376 | Spec | current |
| Two `constructor`s, a getter named `constructor`, a `constructor` field, `static prototype`: `SyntaxError` | Class early errors | Valid names | Spec p.376–377 | Spec | current |
| A field (`speed = 0;`) becomes an instance property, not a prototype one | Fields are per instance | A method on the prototype for what is shared | EJpt p.132–133 | EJpt | current |
| `arguments` in a field initializer: `SyntaxError` | Early error | Constructor parameter | Spec p.377 | Spec | current |
| Calling `#private` from outside fails; undeclared `#x`: `SyntaxError` | Private names are lexical to the class | `#x in obj` to test the brand | EJpt p.133–134; Spec p.110–111, p.310, p.379–380 | EJpt+Spec | current |
| Assigning to a private method or reading a missing private: `TypeError` | PrivateSet/PrivateGet rules | — | Spec p.110–111 | Spec | current |
| `#constructor` forbidden; duplicate private except a get/set pair | Early errors | — | Spec p.376–377 | Spec | current |
| Confusing `Ctor.prototype` with the prototype of the constructor itself | They are distinct things | `prototype` is the prototype of the instances | EJpt p.132 | EJpt | current |
| A subclass reads `this.length` before the private field is ready | The class's own getter is called early | Initialization order | EJpt p.146 | EJpt | current |
| Inheritance tangles classes; a piano is not an `Array` | Coupling between types | Composition | EJpt p.147; EJ1 p.159 | EJpt+EJ1 | current |
| The class name stays in TDZ until the end of evaluation; it is immutable from inside | Evaluation order | Do not use the class in computed keys | Spec p.384–386 | Spec | current |
| Classes are always strict | Rule | — | Spec p.247, p.376 | Spec | current |
| EJ1: inheritance via `clone`, restoring `constructor`, a mix-in runs the `Item` constructor twice | There was no `class`/`extends` | `class` and `extends` | EJ1 p.152, p.164–165 | EJ1 | [DATED] |

### 2.10 Iterators and generators

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `TypeError` in `for...of`/spread of a non-iterable value | `GetIterator` does not find `Symbol.iterator` | Check the type; `Array.from` for array-likes | Spec p.114, p.342 | Spec | current |
| `next` returns something that is not an object: `TypeError` | Iterator contract | Return `{value, done}` | Spec p.114–115, p.342; EJpt p.143 | Spec+EJpt | current |
| `break` in `for...of` calls the iterator's `return`; destructuring closes the iterator if it did not finish | IteratorClose | Implement `return` for cleanup | Spec p.116, p.155, p.320, p.343 | Spec | current |
| Calling the generator executes nothing | It stays suspended at the start | Call `next()` | Spec p.369 | Spec | current |
| Re-entering a running generator: `TypeError`; after the end `next()` gives `done: true` | Generator states | Do not re-enter; a generator does not restart | Spec p.787 | Spec | current |
| `yield` inside a function nested in the generator | `yield` only in the direct body | Recursion with `yield*` | EJpt p.251 | EJpt | current |
| `yield` in generator parameters: `SyntaxError` | Parameters are evaluated before it becomes resumable | — | Spec p.369 | Spec | current |
| `yield*` with an iterator without `throw`: `TypeError` | Protocol violation | Implement `throw` | Spec p.371–372 | Spec | current |
| Endless iteration when inserting into a `Map`/`Set` during traversal | Added entries are visited **[inference]** | Copy the keys beforehand | Spec p.679 | Spec | current |
| Returning the inner array's iterator exposes mutation | Shared state | `function*` generator | EJpt p.150–151 | EJpt | current |
| Iterator helpers consume the source; `take(NaN)` and `drop(-1)`: `RangeError`; empty `reduce`: `TypeError` | Iterators do not restart | `toArray` and finite filters | Spec p.759–760 | Spec | version not stated |
| Async iterator errors arrive as a rejection | Always a promise | `try/catch` with `await` | Spec p.790 | Spec | current |

### 2.11 Asynchronous code

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `try/catch` around `setTimeout` does not catch the callback's error | The callback runs on its own stack, later | Promises and `async/await` | EJpt p.256–257 | EJpt | [HOST] |
| `Promise.resolve("x").then(log); log("before")` prints "before" first | Promise reactions run as jobs after the script | Count on the asynchronous order | EJpt p.257–258; Spec p.764, p.768 | EJpt+Spec | current |
| Timeout fires late | Slow code blocks the event loop | Break up work; avoid long loops | EJpt p.257, p.334 | EJpt | [HOST] |
| Result lost when doing `list += ...` inside `map(async ...)` | `+=` reads before the `await` | Return values and join them with `join` after `Promise.all` | EJpt p.258–259 | EJpt | current |
| An unhandled rejection produces a warning from the environment | `HostPromiseRejectionTracker` | Always have a `catch` | EJpt p.245; Spec p.768 | EJpt+Spec | [HOST] |
| `.catch(() => {})` swallows errors | Silent failure | Only when the failure is expected (network) | EJpt p.253 | EJpt | current |
| `await` in a loop makes everything sequential | Each step waits for the previous one | `Promise.all` for independent items; sequential when one depends on another | EJpt p.249–250, p.254–255 | EJpt | current |
| `await` outside an `async` function | Only valid in `async`; at module top level it is valid | Mark it `async` | EJpt p.250; Spec p.387, p.402 | EJpt+Spec | [VERSION-DEPENDENT] (version not stated) |
| An `async` function returns a promise, not a value; parameter errors become a rejection | Spec behavior | `await` or `.then` | Spec p.389, p.797 | Spec | current |
| `new asyncFunction()` throws `TypeError` | Not a constructor | Call it normally | Spec p.797 | Spec | current |
| `reject` after `resolve` has no effect; `throw` after `resolve` is ignored | A promise changes state once | Plan for the 1st event | EJpt p.247, p.263; Spec p.766, p.770 | EJpt+Spec | current |
| `resolve(anotherPromise)` does not fulfill immediately | It stays resolved but pending; the thenable's `then` runs in a job | Wait for the chain | Spec p.764, p.766, p.769–770 | Spec | current |
| Resolving the promise with itself: `TypeError` | Self-resolution | — | Spec p.766 | Spec | current |
| `then(nonFunction)` is ignored and passes the result through | Empty handler | Pass a function | Spec p.779 | Spec | current |
| Forgetting the `return` inside `then` delivers `undefined` to the next step | The callback's value becomes the next promise's **[inference]** | Return the value | EJpt p.241 | EJpt | current |
| `finally` receives no arguments and does not replace the value, but an error in it replaces the result | `finally` rules | — | Spec p.778–779 | Spec | current |
| `Promise.all` rejects on the first failure, the others continue; empty resolves `[]`; empty `race` never finishes | Combinator contracts | `allSettled` to collect everything; `any` rejects with `AggregateError` | Spec p.771–776 | Spec | current |
| `Promise()` without `new` and an invalid executor: `TypeError` | Validation | — | Spec p.770 | Spec | current |
| `fetch` does not reject on 404/500 | The promise resolves even with a server error code and may reject on a network error (EJpt p.407) | Use a wrapper that rejects on an error code (`fetchOK`, EJpt p.498); checking `status` is **[extrapolation]** | EJpt p.407, p.498 | EJpt | [HOST] |
| Error/value callbacks require checking the error at every level | Verbose `(error, value)` convention | Promises | EJpt p.243, p.466 | EJpt | current |
| `if (error) throw error` inside the callback only rethrows | Example pattern | — | EJpt p.465 | EJpt | [HOST] |
| `...Sync` functions freeze the whole program | They block the loop | Asynchronous versions | EJpt p.467 | EJpt | [HOST] |
| `setInterval` without `clearInterval` keeps going forever | The timer persists | Keep the id and clear it | EJ1 p.206–207, p.226; EJpt p.335–336 | EJ1+EJpt | [HOST] |
| The order of `await` and `then` changed in ES2019 | Fewer jobs per `await` | Do not depend on tick counts | Spec p.869 | Spec | [VERSION-DEPENDENT] |

### 2.12 Modules and packages

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `import`/`export` inside a function or block | Only at module level, resolved at load time | Dynamic import `import()`, which returns a promise | EJpt p.222; Spec p.299–300 | EJpt+Spec | [VERSION-DEPENDENT] (ES2015 modules, EJpt p.221) |
| `import` does not accept an expression; `require` does | `import` requires a string literal | Use `import()` when dynamic | EJpt p.228 | EJpt | current |
| `SyntaxError`: two `export default`, exporting a nonexistent name, a nonexistent import | Early errors and linking | Review names | Spec p.402, p.418 | Spec | current |
| `import "x"` without a binding still executes the module | It creates a module request | — | Spec p.436 | Spec | current |
| `this` undefined, top-level `await`, `super`/`new.target` forbidden in a module | A module is different from a script | Know which mode is in use | Spec p.179, p.247, p.402 | Spec | current |
| Dependency cycle | CommonJS tolerates it if none uses the other's interface before loading; ES uses live bindings with TDZ | Avoid cycles | EJpt p.235; Spec p.178 | EJpt+Spec | current |
| An evaluation error repeats in the importers | Memoized error | Fix the cause | Spec p.413, p.417–418 | Spec | current |
| An `import()` failure is a rejection, not an exception | Returns a promise | `await` with `try/catch` | Spec p.299–300 | Spec | current |
| Module name resolved differently per environment | Browser: addresses; Node: files | Follow the host's rules | EJpt p.222, p.461–462 | EJpt | [HOST] |
| `require` in an ES file, `document` in Node | Node uses `.mjs` for ES modules; browser globals do not exist | Choose the right system | EJpt p.461 | EJpt | [HOST] |
| IIFE and CommonJS to isolate scope; globals stuck on `window` | There were no native modules | ES modules | EJpt p.225–226, p.229; EJ1 p.170–172 | EJpt+EJ1 | [DATED] |
| EJ1's `load()` only loads after the current script | Creates a `script` tag | Order the tags manually | EJ1 p.168 | EJ1 | [DATED] [HOST] |
| `Function`/`eval` to load code opens injection | Strings become a program | Avoid | EJpt p.228; EJ1 p.168 | EJpt+EJ1 | current |
| Dependencies break on a new version; the license may impose obligations | Packages evolve; copyright | `^` only accepts compatible versions; check the license | EJpt p.224–225, p.464–465 | EJpt | [HOST] |

### 2.13 Regular expressions

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `/\d/g.test` alternates `true`/`false` between calls | `lastIndex` persists with `g` or `y` | A new regex per use; reset `lastIndex` | EJpt p.209; Spec p.610, p.613 | EJpt+Spec | current |
| `match` with `g` brings neither groups nor `index` | It returns only the matched pieces | `matchAll` (requires `g`) | EJpt p.209–210; Spec p.546 | EJpt+Spec | current |
| `matchAll` without `g`: `TypeError` | Rule | Add `g` | Spec p.546 | Spec | current |
| A pattern freezes the program (`/([01]+)+b/`) | Exponential backtracking | Rewrite without nested repetition | EJpt p.202–203; Spec p.571 | EJpt+Spec | current |
| `/\/\*[^]*\*\//` swallows the text between two comments | Greedy repetition | Non-greedy form `*?` | EJpt p.205–206 | EJpt | current |
| A regex "works" but matches unexpected pieces | Missing `^` and `$` | Anchor it | EJpt p.198, p.212 | EJpt | current |
| `new RegExp("\\d")`: forgetting the doubled backslash | Strings consume one backslash | Double the backslashes | EJpt p.206; EJ1 p.183–184; Spec p.600 | EJpt+EJ1+Spec | current |
| Interpolating user text into a regex | Special characters change the pattern | Escape; the book's set omits `]` and `}` **[inference]**; `RegExp.escape` exists | EJpt p.206–207; Spec p.600 | EJpt+Spec | version not stated (`RegExp.escape`) |
| `\w`, `\b` do not match `é` or `β` | `\w` is ASCII only | `\p{L}` with the `u` flag | EJpt p.192–193, p.199; EJ1 p.178 | EJpt+EJ1 | current |
| `.`, `?`, `{3}` treat half an emoji; `/🍎{3}/` fails | Without `u` it operates on code units | `u` flag | EJpt p.212–213; Spec p.571 | EJpt+Spec | current |
| `\p{...}` without `u` or `v` does not work; `u` and `v` together: `SyntaxError` | Unicode modes | Use one flag | EJpt p.192; Spec p.598–599 | EJpt+Spec | current |
| Repeated or unknown flag: `SyntaxError` | Only `d g i m s u v y` | — | Spec p.284, p.598 | Spec | current |
| `//` is not an empty regex | It becomes a comment | `/(?:)/` | Spec p.265 | Spec | current |
| `exec` returns `null` | No match | Test before indexing | EJpt p.195; EJ1 p.180–181 | EJpt+EJ1 | current |
| A repeated group keeps only the last capture; a non-participating group is `undefined` | Reset at each iteration | Explicit groups | EJpt p.196; Spec p.575, p.577 | EJpt+Spec | current |
| A backreference to a group not yet captured matches empty | Rule | — | Spec p.584 | Spec | current |
| `search` ignores `lastIndex` and `g` | It does not use them | `exec` for a start position | Spec p.605–606; EJpt p.207 | Spec+EJpt | current |
| `replace`: `$1`…`$9` (EJpt) or up to 99 (Spec); the function receives the match, groups, position, string | Substitution | A function for logic | EJpt p.203–204; Spec p.549, p.605 | EJpt+Spec | current |
| `split` with a regex inserts the captures into the result | Rule | — | Spec p.607 | Spec | current |
| `.` does not match a line break | Without the `s` flag | `s` or `[^]` | EJpt p.191, p.205; Spec p.583 | EJpt+Spec | current |
| Lookahead is not revisited when backtracking; lookbehind reverses the order | Assertion semantics | — | Spec p.579–581 | Spec | current |
| `ſ` and `K` (Kelvin) match `/[a-z]/ui` but not `/[a-z]/i` | Case folding only with `u`/`v` | Know the mode | Spec p.587 | Spec | current |
| `[E-f]` with `i` matches punctuation | Range endpoints matter | Coherent ranges | Spec p.588 | Spec | current |
| A regex literal creates a new object at each evaluation | Different identity | Hoist to a constant if `g`/`y` matters | Spec p.264 | Spec | current |
| `{,4}` as up to four (EJ1) | Not a modern ECMAScript quantifier **[extrapolation]** | Use `{0,4}` | EJ1 p.179 | EJ1 | [DATED] |

### 2.14 Date

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `new Date(2009, 11, 9)` is December | Month is 0-based, day is 1-based | Subtract 1 when building; add 1 when displaying | EJpt p.197; EJ1 p.56; Spec p.511–512 | EJpt+EJ1+Spec | current |
| `getDay` 0 is Sunday | Convention | — | Spec p.512; EJpt p.260–261 | Spec+EJpt | current |
| `new Date(99, 0)` is 1999, `new Date(100, 0)` is the year 100 | `MakeFullYear` adds 1900 from 0 to 99 | Pass the full year | Spec p.518 | Spec | current |
| `Date()` without `new` returns text | Called as a function | `new Date()` or `Date.now()` | Spec p.522; EJpt p.197–198 | Spec+EJpt | current |
| One argument: a number is milliseconds, a string is parsed, a Date is copied | Polymorphic constructor | No ambiguity with the year | Spec p.522; EJpt p.197 | Spec+EJpt | current |
| `"2020-01-01"` is UTC, `"2020-01-01T00:00"` is local | Without a time zone: date only is UTC, date and time is local | Include `Z` or an offset | Spec p.523 | Spec | current |
| Non-standard formats give different results per engine | `Date.parse` accepts heuristics | Only the standard format | Spec p.523 | Spec | [HOST] |
| Local time repeated or nonexistent during daylight saving time | Disambiguation of `UTC(t)` | Compute in UTC | Spec p.514, p.517 | Spec | [HOST] |
| `console.log` output changes with the environment's time zone | System time zone | Do not compare local text | EJpt p.197; Spec p.515–516 | EJpt+Spec | [HOST] |
| `d1 == d2` is false for equal dates | Identity | `getTime()` | EJ1 p.57 | EJ1 | [DATED] |
| Invalid date: `NaN`, `"Invalid Date"`, `toISOString` throws `RangeError`, `JSON.stringify` gives `null` | Time value NaN | Validate `isNaN(d.getTime())` | Spec p.533–534 | Spec | current |
| `setFullYear` repairs an invalid date; other `setX` keep NaN | Special rule | — | Spec p.528 | Spec | current |
| `new Date(2020, 0, 32)` does not fail, it overflows; outside ±8.64e15 it becomes NaN | `MakeDay`/`TimeClip` | Validate | Spec p.509, p.518 | Spec | current |
| `date + 1` concatenates | The "default" hint is string | `getTime() + 1` | Spec p.537 | Spec | current |
| `getYear`, `setYear`, `toGMTString` | Legacy | `getFullYear`, `setFullYear`, `toUTCString` | EJpt p.198; Spec p.854 | EJpt+Spec | [DATED] |
| `toLocale*` and `Date.parse(toLocaleString())` do not guarantee a round trip | Host format | ISO | Spec p.524, p.534 | Spec | [HOST] |

### 2.15 JSON

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `JSON.parse` throws `SyntaxError` | Text outside ECMA-404 (names without double quotes, comments, trailing comma **[inference]**) | Generate valid JSON | Spec p.735; EJpt p.99 | Spec+EJpt | current |
| `JSON.stringify` omits `undefined`, functions and symbols in objects, and turns them into `null` in arrays | No representation | Explicit values | Spec p.741–744 | Spec | current |
| `NaN`/`Infinity` become `null`; `JSON.stringify(undefined)` returns `undefined` | Rules | Handle beforehand | Spec p.741–742 | Spec | current |
| Circular structure: `TypeError`; BigInt: `TypeError` | No standard solution | `toJSON`, `replacer` | Spec p.741–744 | Spec | current |
| Duplicate keys: the last one wins | Parse rule | — | Spec p.736–737 | Spec | current |
| A `reviver` returning `undefined` deletes the property | Rule | Return the value | Spec p.735, p.737–738 | Spec | current |
| `localStorage` stores only strings | Text storage | `JSON.stringify` when saving, `JSON.parse` when reading; a missing `getItem` gives `null` | EJpt p.423–425 | EJpt | [HOST] |
| Nonsensical network JSON corrupts the model | External data | Validate the fields | EJpt p.492–493 | EJpt | [HOST] |
| JSON read with `eval("(" + text + ")")` | It was the only way | `JSON.parse` | EJ1 p.234 | EJ1 | [DATED] |
| Web workers copy only what fits in JSON | Messages | Simple structures | EJpt p.335 | EJpt | [HOST] |

### 2.16 Native errors: when they occur

| Type | When it occurs (documented cases) | Source | Origin | Era |
|---|---|---|---|---|
| `SyntaxError` | Early errors before execution (Script, `eval`, `Function`); invalid `JSON.parse`; invalid regex; `BigInt("x")`; labels; `const` without a value; duplicate names | Spec p.95, p.245, p.328, p.445, p.598, p.735; EJpt p.168 | Spec+EJpt | current |
| `ReferenceError` | Reading an unresolvable name; TDZ; assigning to an undeclared name in strict; `this` before `super()`; uninitialized import binding; `f() = 1` in sloppy in the browser | Spec p.81, p.167–168, p.172, p.178, p.859; EJpt p.168–169 | Spec+EJpt | current |
| `TypeError` | `null`/`undefined` value in access or destructuring; calling a non-function; `new` on a non-constructor; reassigning `const`; BigInt/Number mixing; converting a Symbol; writing to a non-writable property in strict; empty `reduce`; `instanceof`/`in` with an invalid right-hand side; cycle or BigInt in `stringify`; generator re-entry; revoked `Proxy` | Spec p.81, p.89, p.96, p.167, p.293–294, p.310, p.317, p.632–633, p.742, p.787; EJpt p.76, p.170 | Spec+EJpt | current |
| `RangeError` | `new Array(1.5)`; `toFixed`/`toPrecision`/`toString(radix)` out of range; negative `repeat`; `fromCodePoint`; `normalize`; `BigInt(1.5)`; `toISOString` on an invalid date; `with` out of range; TypedArray offsets; `resize` beyond the maximum | Spec p.97, p.491–495, p.533, p.538–539, p.546–548, p.615, p.643, p.658–659, p.706–707 | Spec | current |
| `URIError` | `decodeURI*` with a malformed `%` or invalid UTF-8; `encodeURI*` with a lone surrogate | Spec p.456–457, p.484 | Spec | current |
| `EvalError` | Exists only for compatibility; the Spec no longer uses it | Spec p.484 | Spec | [DATED] |
| `AggregateError` | `Promise.any` when everything rejects; the iterable of errors comes before the message | Spec p.486, p.774–775 | Spec | current |
| Generic `Error` | Any value can be thrown; `message` is not enumerable; `cause` comes from the options; `stack` records the stack | Spec p.482–483, p.487; EJpt p.176, p.178 | Spec+EJpt | current |
| Stack overflow | Messages such as "out of stack space"/"too much recursion"; the type is not named in the sources | EJpt p.58; EJ1 p.37 | EJpt+EJ1 | [HOST] |

Error-handling pitfalls:

| Symptom | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| An indiscriminate `catch` hides bugs (a typo becomes "invalid input") | JS does not filter by type | `instanceof` of your own class and rethrow the rest; do not compare `message` | EJpt p.181–183 | EJpt | current |
| `finally` does not suppress the exception; `return`/`throw` in `finally` replaces the previous result | Rule | Simple cleanup in `finally` | EJpt p.180; Spec p.354 | EJpt+Spec | current |
| Half-done side effects after an exception (a bank with lost balance) | The exception interrupts the flow | Reorder, compute new values, `finally` | EJpt p.178–180 | EJpt | current |
| Throwing strings makes the failure hard to recognize | No type | `Error` objects or subclasses | EJ1 p.75; EJpt p.182–183 | EJ1+EJpt | [DATED] / current |
| An early error is not promoted to a runtime error (and vice versa) | Implementation rule | — | Spec p.445 | Spec | current |
| A special return value (`null`, `-1`) is ambiguous or spreads checks | Sentinels | Exceptions; wrap in `{value}` | EJpt p.175–176; EJ1 p.69–70 | EJpt+EJ1 | current |
| Debugging by random changes | Lack of a theory | Theory, `console.log`, `debugger` | EJpt p.173–175 | EJpt | current |

### 2.17 `eval`, `with` and `Function` [DATED]

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| `with` in strict or a module: `SyntaxError` | The Spec marks it as legacy | Destructuring | Spec p.347, p.861; EJpt p.170 | Spec+EJpt | [DATED] |
| `var x` inside `with` assigns to the object's property | Object environment in the chain | Do not use | Spec p.329 | Spec | [DATED] |
| New `Array.prototype` names would break code using `with` | `Symbol.unscopables` blocks them | — | Spec p.169, p.643–644 | Spec | [DATED] |
| Direct `eval` sees the local scope; indirect sees the global | Direct versus indirect | Avoid `eval` | Spec p.294, p.449; EJ1 p.168 | Spec+EJ1 | [DATED] |
| A strict `eval`'s `var`/function does not leak to the caller | New environment in strict | — | Spec p.449 | Spec | [DATED] |
| An `eval` `var` colliding with a global `let`: `SyntaxError` | Lexical conflict | — | Spec p.450 | Spec | [DATED] |
| A host policy blocks `eval` and `Function` | `HostEnsureCanCompileStrings` | — | Spec p.450 | Spec | [HOST] |
| `new Function(...)` does not see local variables; name "anonymous" | Global scope | Avoid | Spec p.471; EJpt p.228 | Spec+EJpt | [DATED] |
| `evalJSON`, `setTimeout("code")`, `onclick="code"` | Text becomes a program | `JSON.parse`, functions | EJ1 p.145, p.192–193, p.234 | EJ1 | [DATED] |
| `arguments.callee` throws `TypeError` in strict; own `caller` and `arguments` forbidden | Security | — | Spec p.223–224, p.445, p.861 | Spec | [DATED] |
| `debugger` only does something with an active tool | Depends on the host | — | Spec p.354–355; EJpt p.174–175 | Spec+EJpt | [HOST] |

### 2.18 Other built-in objects (Proxy, collections, buffers)

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| A Proxy throws `TypeError` when it "lies" about a non-configurable property or a non-extensible object; a revoked proxy always throws | Invariants checked at the operation | Respect the invariants; `Reflect` in the traps | Spec p.235–243 | Spec | current |
| A trap `set` without `true` fails | Falsy result | Return `true` **[inference]** | Spec p.240 | Spec | current |
| `new Proxy(1, {})` or without `new`: `TypeError` | Validation | — | Spec p.243, p.801 | Spec | current |
| `new Map([1, 2])`: `TypeError` | Items must be pair objects | `[[k, v]]` | Spec p.676 | Spec | current |
| `Map` keys: `NaN` works; `0` and `-0` are the same | SameValueZero | — | Spec p.675, p.697 | Spec | current |
| `Set` with an `other` array: `TypeError`; negative `size`: `RangeError` | Set operations require set-like | `new Set(array)` | Spec p.682–683 | Spec | version not stated |
| `new WeakRef(1)` throws; the target may be collected | Only objects and symbols; non-deterministic collection | Do not base logic on it | Spec p.745–747 | Spec | current |
| A detached buffer (`transfer`) makes views out of bounds; `resize` beyond the maximum: `RangeError` | Buffer state | Check `detached` | Spec p.706–708 | Spec | version not stated |
| TypedArray: assigning to an invalid numeric key does not create a property; `sort` is numeric | Canonical keys | — | Spec p.229–230, p.665 | Spec | current |
| `Symbol()` with `new`: `TypeError`; `Symbol("a") !== Symbol("a")`; `Symbol.for` shares | Symbols are unique | `Symbol.for` when sharing is needed | Spec p.478; EJpt p.141–142 | Spec+EJpt | [VERSION-DEPENDENT] (2015, EJpt p.141) |

### 2.19 [HOST]: DOM, events, network, canvas, Node

Everything below is environment behavior, not language behavior.

| Symptom or message | Cause | Fix | Source | Origin | Era |
|---|---|---|---|---|---|
| A loop over `getElementsByTagName` ends early when removing nodes | Live collection | Walk backwards, `Array.from`, or `querySelectorAll` (static) | EJpt p.302, p.310 | EJpt | [HOST] |
| `childNodes` has no `map`/`slice`; fixed paths break | NodeList; whitespace text nodes | Search by id/selector | EJpt p.297, p.299; EJ1 p.199 | EJpt+EJ1 | [HOST] |
| `nodeName` comes in uppercase | DOM convention | Compare in uppercase | EJ1 p.197–198; EJpt p.316 | EJ1+EJpt | [HOST] |
| `class` does not work as a property; `tabindex` becomes `tabIndex` | `className`; property names | Property names; `data-` for custom attributes | EJpt p.303–304, p.453; EJ1 p.200 | EJpt+EJ1 | [HOST] |
| A numeric style is ignored | The unit is missing | `"10px"`; only `0` is exempt | EJpt p.313; EJ1 p.206 | EJpt+EJ1 | [HOST] |
| Slow page when alternating layout reads and DOM writes | Forced recalculation | Measure once, write afterwards | EJpt p.305–306 | EJpt | [HOST] |
| A long loop freezes the page | No repaint while it runs | `requestAnimationFrame`; step proportional to time | EJpt p.312 | EJpt | [HOST] |
| `<script src>` without `</script>` swallows the rest | HTML parser | Always close it | EJpt p.289 | EJpt | [HOST] |
| `removeEventListener` does not remove | A function different from the registered one | Name the function | EJpt p.320 | EJpt | [HOST] |
| `onclick` accepts only one handler | Single attribute | `addEventListener` | EJpt p.320 | EJpt | [HOST] |
| The parent's handler runs when the child is clicked | Propagation | `stopPropagation`; delegation with `event.target` | EJpt p.321–323 | EJpt | [HOST] |
| `focus`/`blur`/`load` do not propagate; `preventDefault` does not stop `scroll` | Event rules | `focusin`, other events **[extrapolation]** | EJpt p.332–333 | EJpt | [HOST] |
| `button` (0/1/2) and `buttons` (1/2/4) differ | Inconsistent API | Check which one is used | EJpt p.321, p.329 | EJpt | [HOST] |
| `keydown` repeats; typing text per key is unreliable | Repetition, IME, virtual keyboard | `input` event | EJpt p.324–326, p.417 | EJpt | [HOST] |
| `change` on text only fires on losing focus | Rule | `input` | EJpt p.417; EJ1 p.227 | EJpt+EJ1 | [HOST] |
| The form reloads the page | Default `submit` action | `preventDefault` | EJpt p.415–416, p.500–501 | EJpt | [HOST] |
| Touch also fires mouse events | Compatibility | `preventDefault` on `touchstart` | EJpt p.329–330, p.438–439 | EJpt | [HOST] |
| Chosen file without content | Asynchronous reading | `FileReader` or a wrapping promise | EJpt p.421–422 | EJpt | [HOST] |
| `fetch` to another domain is blocked | Same-origin; CORS on the server | `Access-Control-Allow-Origin` header | EJpt p.408–409; EJ1 p.231 | EJpt+EJ1 | [HOST] |
| Data in the URL with `&` or a space breaks | Encoding | `encodeURIComponent` | EJpt p.405, p.485–486; EJ1 p.189 | EJpt+EJ1 | [HOST] |
| GET with a side effect; POST to change state | HTTP convention | GET read-only | EJpt p.406; EJ1 p.190 | EJpt+EJ1 | [HOST] |
| Synchronous `XMLHttpRequest` freezes; an early `responseText` is empty | Request state | Asynchronous with `readyState == 4` | EJ1 p.233 | EJ1 | [DATED] [HOST] |
| Canvas: `drawImage` before `load` does not draw | Image not yet loaded | Draw on `load` | EJpt p.382, p.392 | EJpt | [HOST] |
| Canvas: changing `width`/`height` clears; transformations persist | Context state | `save`/`restore`; `resetTransform` | EJpt p.387–388, p.454–455 | EJpt | [HOST] |
| Canvas: `scale(-1, 1)` throws the image out of view | Axis inverted around (0,0) | Mirror around the center | EJpt p.385–386 | EJpt | [HOST] |
| `arc` connects to the previous point | Continuous path | `moveTo` or a new path | EJpt p.379–380 | EJpt | [HOST] |
| Node: `process.argv` starts at index 2 | Includes `node` and the script | Read from 2 | EJpt p.460–461 | EJpt | [HOST] |
| A Node server does not end by itself | Active listening | Ctrl-C | EJpt p.468 | EJpt | [HOST] |
| Directory traversal (`/../secret`) | Unresolved path | `resolve` + prefix check | EJpt p.472–473 | EJpt | [HOST] |
| Reading without an encoding returns a `Buffer`; so does a stream `chunk` | Bytes | `"utf8"`, `toString()` | EJpt p.465–466, p.470 | EJpt | [HOST] |
| `ENOENT` and idempotent `DELETE` | Node codes; HTTP | Handle 404/204 | EJpt p.475–476 | EJpt | [HOST] |
| Long polling drops from inactivity | Idle connection | Maximum time and restart | EJpt p.484, p.501–502 | EJpt | [HOST] |
| Headers in Node arrive in lowercase | Node normalizes | `request.headers["if-none-match"]` | EJpt p.494 | EJpt | [HOST] |
| IE: `attachEvent`, `srcElement`, leaking memory, mandatory `tbody`, `ActiveXObject` | Old browser | Not needed today | EJ1 p.200, p.203, p.209–216, p.227–229, p.231 | EJ1 | [DATED] [HOST] |
| Detecting the browser by name | Unreliable | Detect the feature | EJ1 p.194–195, p.209–210 | EJ1 | [DATED] [HOST] |
| An exception in an event handler disappears from the book's console | The browser handles it | The browser's error console | EJ1 p.211 | EJ1 | [DATED] [HOST] |

## 3. Part 2 — Anti-patterns and the alternative

| Anti-pattern | Why it is bad | Alternative | Source | Origin | Era |
|---|---|---|---|---|---|
| `==` out of habit | Confusing conversion rules | `===`, or `== null` on purpose | EJpt p.24–25 | EJpt | current |
| `var` | Function scope, "strange" according to the book | `let`, `const` | EJpt p.31–32, p.52–53 | EJpt | [DATED] |
| Omitting `;` | Treacherous ASI | Always `;` | EJpt p.29–30; Spec p.273 | EJpt+Spec | current |
| Mutation and side effects where a pure function fits | Hard to test; race conditions | Pure functions, new values, persistent data | EJpt p.68–69, p.156–157, p.259 | EJpt | current |
| A plain object as a map | Inherits properties | `Map` or `Object.create(null)` | EJpt p.136–138 | EJpt | current |
| Ambiguous sentinel values | Hides failures | Exceptions; moderate assertions | EJpt p.175–176, p.183–184 | EJpt | current |
| A universal `catch` | Hides bugs | Filter and rethrow | EJpt p.181–183 | EJpt | current |
| An exception as an ad hoc `break` | The book itself calls it ad hoc | Higher-order function (`any`, `every`, `some`) | EJ1 p.107–108 | EJ1 | [DATED] |
| `eval`/`Function`/strings as code | Injection; strange scope | Functions, modules, `JSON.parse` | EJpt p.228; EJ1 p.168 | EJpt+EJ1 | [DATED] |
| State scattered across UI components | Each part knows all the others | A single state and `dispatch` of actions | EJpt p.431–433 | EJpt | current |
| Inheritance as the first tool | Couples classes | Composition | EJpt p.147; EJ1 p.159 | EJpt+EJ1 | current |
| Creating a class for every concept | Complexity | Reduce to the minimal state | EJpt p.154–155 | EJpt | current |
| Inventing generality before the need | Code never used | Correct and simple; measure before optimizing | EJpt p.62, p.68; EJ1 p.36–37 | EJpt+EJ1 | current |
| Building HTML by concatenation | Breaks with `<` and `&` | Data structure/`elt`/`createElement` | EJ1 p.93–94; EJpt p.302–303 | EJ1+EJpt | [DATED] / current |
| Concatenating a large string in a loop | Many discarded strings (argument of the time) | Array and `join` | EJ1 p.96–97 | EJ1 | [DATED] |
| Extending standard prototypes | Shows up in `for...in`; collisions | Utility functions | EJ1 p.129, p.133–134, p.173 | EJ1 | [DATED] |
| Polluting the global namespace | Silent collision | Modules | EJ1 p.170; EJpt p.220–221 | EJ1+EJpt | current |
| Modules that read the disk directly | Unusable in the browser | Receive the text; compose functions | EJpt p.230–231 | EJpt | current |
| An interface with a state object and ritual | Dependence on special types | Functions that compute values; plain arrays | EJpt p.231 | EJpt | current |
| Probing events in a loop (polling) | Unresponsive software | Handlers | EJpt p.318–319 | EJpt | [HOST] |
| Nested callbacks | Indentation and hard-to-trace errors | Promises, `async/await` | EJpt p.240, p.249–250 | EJpt | current |
| Changing shared state in asynchronous code | Gaps where other code runs | Compute and combine results | EJpt p.258–259 | EJpt | current |
| Reassigning built-in names | Breaks standard functions | Your own names | EJpt p.95; EJ1 p.17 | EJpt+EJ1 | current |
| A regex for everything | Sharp tool, awkward handle | A parser when the regex does not express it well | EJpt p.214–215 | EJpt | current |
| Browser detection | Fragile | Feature detection | EJ1 p.194–195, p.209–210 | EJ1 | [DATED] |
| Rigid "best practices" rules | For the author, boring and ineffective | Practice, mistakes and design sense | EJpt p.4; EJ1 p.2–3 | EJpt+EJ1 | author's opinion |
| Assertions for every bad input | Noisy code | Only for errors that are easy to make | EJpt p.184 | EJpt | current |

## 4. Part 3 — Annex B and legacy to avoid

Annex B is normative but optional outside browsers; browsers must support it; the Spec itself says the features have undesirable characteristics and should not be used in new code (Spec p.843). In modules and in strict code several extensions are not allowed (Spec p.446). Everything below is **[DATED]**.

| Legacy feature | What it does | Avoid in favor of | Source |
|---|---|---|---|
| `<!--` and `-->` comments | Line comment in scripts; not valid in modules | Normal comments | Spec p.843–844 |
| Legacy regex (without `u`/`v`) | Quantifiable lookahead, literal `{`, `\c` in a class, `[\d-x]` accepted, backreference becomes octal | `u`/`v` mode | Spec p.844–849 |
| `escape`/`unescape` | `%XX` and `%uXXXX` by code unit | `encodeURIComponent`/`decodeURIComponent` **[extrapolation]** | Spec p.849–851 |
| `substr` | Substring by position and length | `slice` | Spec p.851 |
| `anchor`, `big`, `bold`, `link`, `fontcolor` etc. | Generate HTML escaping only `"` | `createElement` | Spec p.851–853 |
| `trimLeft`/`trimRight` | Aliases of `trimStart`/`trimEnd` | New names | Spec p.853–854 |
| `getYear`/`setYear`/`toGMTString` | Year minus 1900; alias of `toUTCString` | `getFullYear`, `setFullYear`, `toUTCString` | Spec p.854; EJpt p.198 |
| `RegExp.prototype.compile` | Reinitializes a regex | Create a new one | Spec p.855 |
| Labelled functions; functions in blocks and in `if` (sloppy) | Web compatibility semantics | Function expression in `const` | Spec p.855–857 |
| `var` with the name of the `catch` parameter | Assigns to the parameter | Distinct name | Spec p.857 |
| `for (var x = 1 in obj)` | Initializer allowed only in non-strict (ES2017 according to the Spec) | Declare outside | Spec p.857–858, p.868 |
| `[[IsHTMLDDA]]` (`document.all`) | Object that acts like `undefined` | Do not use | Spec p.858 |
| `f() = 1` | `ReferenceError` at runtime (non-strict) | — | Spec p.859 |
| `__proto__`, `__defineGetter__`, `__lookupGetter__` | Legacy accessors | `Object.getPrototypeOf`, `defineProperty` | Spec p.468–469 |
| `with` | Inserts an object into the scope chain | Destructuring | Spec p.347 |
| Legacy octals (`017`, `089`, `\07`) | Error in strict | `0o17`, `\x07` | Spec p.257–259, p.262–264 |
| Duplicate parameters; coerced `this`; assignment to an undeclared name | Only in sloppy | Strict mode (list in Annex C) | Spec p.355, p.861 |
| `caller`/`arguments` on functions | Forbidden for strict and new functions | — | Spec p.445 |
| `arguments`, `var`, IIFE, `window` (EJ1) | Pre-ES2015 | Rest parameters, `let`, modules | EJ1 p.64, p.170–172 |

## 5. Part 4 — Errors and inconsistencies in the books and in the extracted text (do not reproduce)

Items for the agent not to repeat as if they were true.

### 5.1 Errors and slips in the books themselves

| Where | What is wrong or inconsistent | Treat as |
|---|---|---|
| EJpt p.35–37; EJ1 p.17 | The program prints the square, but the message says "square root" | Book error: use "square" |
| EJ1 p.226 | `self.content = null` where `this.content` was intended (`self` is the window) | Code error; do not copy |
| EJ1 p.9–10, p.29 | Text says 52 bits; a note corrects it to 53 (IEEE 754); 144 is not as expected | Simplification; Spec p.489 for the limit |
| EJpt p.210 | `matchAll` described as an "array of arrays", but the example iterates with `for...of` | Spec p.546: returns an iterator |
| EJpt p.227 | `"M"` returns `getMonth()` without +1; the regex `M(MMM)?` only accepts `M` or `MMMM` | Month is 0-based (EJpt p.197); add 1 |
| EJpt p.491 | `catch (error)` uses `String(err)` | Typo; it would use `ReferenceError` |
| EJpt p.474 | "specific version of mime" for the `mime-types` package | The package name is `mime-types` |
| EJ1 p.179 | `{,4}` described as up to four | Doubtful **[extrapolation]**; use `{0,4}` |
| EJ1 p.9 vs p.26 | List of six types without `null`, which only appears later | `null` is a separate value |
| EJ1 p.64 vs p.79 | `arguments` is not an array, and later the array arguments | Pseudo-array |
| EJ1 p.28 | Saying that `&&`/`\|\|` return booleans was a simplification | They return operands |
| EJ1 p.51, p.58 | Dates with slashes at one point and hyphens at another | Example inconsistency |
| EJ1 p.52 | Separator "comma" corrected to comma and space | Already self-corrected |
| EJ1 p.109 vs p.99 | `op["!="]` used, but outside the partial list of `op` | Incomplete list |
| EJ1 p.123 | `open.remove` used without showing the heap method | It is in Appendix 2 (EJ1 p.245–246) |
| EJ1 p.153 | Action written `"photosynthese"` | The book's spelling |
| EJ1 p.203 | Passage "starting with ts" truncated | Wording error |
| EJ1 p.185 | Path with `phalsall` and later `phalsal` | Typo |
| EJpt p.59 | Function body with `};` in a declaration | Not a runtime error |
| EJpt p.19 | The example string contains English text | Language not translated |
| EJpt p.454 vs p.440 | `onMove(pos, this.state, dispatch)` in the exercise, `onMove(pos, this.state)` in the chapter | Different versions |
| EJpt p.414 | `tabindex` 1 and 2 as a demonstration | Only demonstrates the effect |
| EJpt p.486 | `Content-Length` 92 and 72 do not match the bodies | Illustrative |
| EJpt p.490–491 | `serveFromRouter` called before being defined, works through hoisting | Declaration hoisting (EJpt p.55) |
| EJpt p.80, p.83 | Journal "array of objects" and later `journal = []` | Didactic continuity |
| EJpt p.9, p.32, p.107, p.121, p.188, p.190, p.265, p.297, p.301, p.307, p.331, p.333, p.344, p.345, p.367, p.372, p.379, p.399, p.404, p.406, p.416, p.432, p.433, p.434 | Typos or agreement errors in the translation (for example "padrãoes", "funçãoões", "imagems") | Noise; does not change the technical meaning |
| EJpt p.448 | "162" in place of 16 squared | Extraction error |
| EJpt p.84 | Phi formula and table incomplete | Reconstruct from p.85–86 |

### 5.2 Truncations and extraction noise

| Where | Problem |
|---|---|
| EJpt p.159 | Text cut in the middle of a sentence |
| EJpt p.234–235 | Exercise "Circular dependencies" cut off; continues on p.235 |
| EJpt p.387–388 | `branch` example announced on p.387, shown on p.388 |
| EJpt p.463 | Explanation of `package.json` cut off |
| EJpt p.460 | `1 + 1` in the REPL without the result line |
| EJpt p.398 | Code comment cut off ("loo") |
| EJpt (several) | Interface markers "Display hints..." and "◂ ● ▸ ?"; epigraphs in English and misplaced; lost diagrams and figures (p.238, p.267, p.294, p.313, p.343, p.383, p.397, p.443, p.456) |
| EJ1 p.29, p.41, p.166, p.184, p.195, p.238 | Footnotes out of order or with the number glued to the text ("2^64" becomes "264") |
| EJ1 (several) | Stray "Ex. N.N" markers at the end of a page; missing figures (p.102, p.113, p.118, p.196, p.242–243) |
| EJ1 p.188 | `timeWriter` used without a definition |
| EJ1 p.247 | Copyright line in the middle of `sinkDown` |
| Spec p.136–137 | `TopLevelVarScopedDeclarations` cut between pages |
| Spec p.188 | Ends in the middle of section 9.5.4 |
| Spec p.273 | List of restricted productions truncated |
| Spec p.288 | Section 13.2.9 with headings only |
| Spec p.345 | Ends in the middle of section 14.7.5.10 |
| Spec p.397 | Ends with section markers without a body |
| Spec p.444 | The evaluation of `export default` expression is missing (it appears in Spec p.445) |
| Spec p.607 | `split` example with capture cut off |
| Spec p.646 | Table 70 without the sizes in bytes |
| Spec p.668 | `AllocateTypedArrayBuffer` cut off |
| Spec p.813–842 | They exist in the PDF (memory model and Annex A), but were not distilled into the references |
| Spec p.860, p.862, p.866, p.870 | Empty pages |
| Spec p.158–159 | Grouping of `AssignmentTargetType` for `f().x` ambiguous at the page break |
| Spec p.398 | `Script : [empty]` returns `undefined` in an algorithm that returns Boolean (source slip) |
| Spec p.408, p.413 | `EvaluationError` described as `undefined` and as EMPTY |
| Spec p.419 | Order 2 of `AsyncEvaluationOrder` does not appear |
| Spec p.808 | The word "execution" repeated |
| Spec p.849 | Table called "Table 1" in the text and "Table B.1" in the title |
| Spec p.868 | `Object.isExtensible` does not explicitly say it returns `false` |
| Spec (in general) | Section headings at the end of each page; flattened exponents ("253 - 1" is 2^53 − 1); symbol 𝔽 glued to the text |

## 6. Divergences between the sources

Rule: the Spec is the standard; EJpt is the modern explanation; EJ1 is dated.

| Topic | EJ1 | EJpt | Spec | Prevails |
|---|---|---|---|---|
| Block scope | Blocks do not create scope; `let` only as a future feature (EJ1 p.34) | `let`/`const` have block scope; `var` does not (EJpt p.52–53) | A block creates a lexical environment (Spec p.326) | Spec |
| Reserved words | List with `char`, `class`, `goto` etc. (EJ1 p.21) | List with `let`, `yield`, `static` (EJpt p.32) | Its own list; `let`/`static` only in strict; `await`/`yield` contextual (Spec p.255) | Spec |
| Falsy values | `0`, `""`, `null`, `undefined`, `false`, `NaN` (EJ1 p.26–28) | `0`, `NaN`, `""` and null values (EJpt p.26) | Includes `0n`; `IsHTMLDDA` in the host (Spec p.89) | Spec |
| `with` | Described without a warning (EJ1 p.241) | So wrong it is not discussed (EJpt p.170) | Legacy, forbidden in strict (Spec p.347) | Spec |
| Unicode in strings | Unicode assigns numbers to characters (EJ1 p.13) | Strings have 16 bits per element; emoji take two (EJpt p.19) | Length in code units (Spec p.50) | Spec |
| Cost of recursion | About ten times (EJ1 p.36) | About three times (EJpt p.62) | Not stated | Measure; numbers are dated |
| `className` | Because of IE (EJ1 p.200) | Historical keyword reason (EJpt p.304) | Not defined (DOM belongs to the host) | [HOST] |
| Strict mode | Not discussed | `"use strict"`; classes and modules are already strict (EJpt p.169) | Strict classes and modules (Spec p.247) | Spec |
| JSON | Read with `eval` (EJ1 p.234) | `JSON.parse`/`stringify` (EJpt p.100) | `JSON.parse` throws `SyntaxError` (Spec p.735) | Spec |
| `getYear` | Does not discuss it | "Largely useless" (EJpt p.198) | Annex B legacy (Spec p.854) | Spec |
| Native functions and `apply` | In IE not all have `apply` (EJ1 p.80) | Does not mention it | Native functions are functions (Spec p.247) | Spec / [DATED] |
| `matchAll` | Does not exist | "Array of arrays" but iterable in the example (EJpt p.210) | Iterator; `g` required (Spec p.546) | Spec |
| Stack overflow | Browser messages (EJ1 p.37) | Same (EJpt p.58) | Type not named in the sources | Type not stated |
| EJpt edition | — | Says it uses "the 2024 version" (EJpt p.9); dates such as Oct/2023 (EJpt p.402) and Feb/2024 (EJpt p.197) | — | **[inference]**: recent edition; number not declared |
| EJ1 edition | Written in 2007, revised through 2013 (EJ1 p.247) | — | — | All [DATED] |
| Features by edition | ES5 and "Harmony" as the future (EJ1 p.6) | Only `class`, Symbol, arrow and modules get a year (2015) (EJpt p.56, p.132, p.141, p.221) | Annex F lists changes by edition (Spec p.867–869) | Spec for what it dates |

## 7. Gaps

- The Spec does not say in which edition most features entered; only Annexes E and F and occasional notes (for example ES2015, ES2017, ES2018, ES2019 in Spec p.867–869). For the rest: version not stated in the sources.
- Exact error messages (text) are not in the Spec; the books quote messages from specific engines (EJpt p.76, p.170).
- The type of the stack overflow exception is not named in any source.
- Whether engines implement tail-position calls is not stated (Spec p.392–397).
- Spec p.813–842 exist in the PDF (end of the memory model and Annex A, grammar summary), but were not distilled into the references.
- Web application security (XSS, CSRF, cookies) and APIs such as `structuredClone` and `queueMicrotask` are not in the sources; EJpt only covers HTTPS, CORS and directory traversal (EJpt p.408–410, p.472–473).
- The solutions to the books' exercises are not included (EJpt: "Display hints..." with no content).
