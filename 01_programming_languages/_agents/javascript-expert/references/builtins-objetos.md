# Built-ins catalog: global objects and functions (lookup by name)

How to use this file: look up the object name (each object has a `###` subsection with a stable title, for example `### Object`, `### Promise`, `### Date`) and read the table. Each row gives Member, Signature, what it does and edge cases, the error thrown, the source page, and the mark (legacy, version, host). Primary and normative source: Spec (ECMA-262, 17th edition, ECMAScript 2026), with PDF pages. This file covers clauses 17 to 21 (except String, which is in another file), 25.3 to 28 of the Spec, and the start of the memory model. Reading rule: the Spec almost never says in which edition a feature was introduced; when the Mark column says "version not stated", it means exactly that, not that the feature is old or new. Abbreviations: Spec (ECMA-262), EJ1 (Eloquent JavaScript, 1st edition, dated), EJpt (Eloquent JavaScript in Portuguese, modern edition). In this file only the Spec was the content source, unless mentioned. Marks: [DATED], [VERSION-DEPENDENT], [HOST], [inference], [extrapolation].

## Contents

1. General conventions of the built-ins
2. Global object and global functions
3. Object
4. Function
5. Boolean
6. Symbol
7. Error, native types and AggregateError
8. Number
9. BigInt
10. Math
11. Date
12. JSON
13. WeakRef and FinalizationRegistry
14. Atomics
15. DataView
16. Iteration interfaces and Iterator (helpers)
17. Promise
18. Generators, async generators and async functions
19. Reflect
20. Proxy
21. Module Namespace
22. Divergences and observations between sources
23. Truncated or noisy passages in the sources (do not reproduce)
24. Gaps

---

## 1. General conventions of the built-ins

### Error handling and language extensions (clause 17)

| Topic | Rule | Page | Mark |
|---|---|---|---|
| Early error | An error detectable before evaluating the Script that contains the construct; it prevents evaluation. In a Script it is reported at parse time; in a Module, when the module would be evaluated (it is never initialized); in `eval`, at the call. Every error that is not an early error is a runtime error | Spec p.445 | normative |
| Promotion forbidden | The implementation may not promote to an early error something that would only fail at run time, even if it proves it would always fail; it may only warn. Code with a guaranteed error in a branch that is never executed does not break the script | Spec p.445 | normative; the consequence is [inference] |
| Permitted extensions | Hosts may extend the syntax of Script, Module and of regex patterns and flags, and provide extra types, values, objects and functions. As a result, `eval`, regex literals, `Function` and `RegExp` may have host-defined behavior instead of `SyntaxError`, and a global variable lookup may stop raising `ReferenceError` | Spec p.445 | [HOST] |
| Forbidden extensions (functions) | Strict functions, arrows, methods, generators, async generators, classes, async functions and async arrows may not have own properties `"caller"` or `"arguments"`; the same holds for built-ins, functions created by `bind`, and functions created by `Function` in strict mode; `arguments` objects may not have an own `"caller"` | Spec p.445 | normative |
| Forbidden extensions (syntax) | Unicode regex may not accept ASCII letters as IdentityEscape; `:` may not immediately follow a BindingIdentifier; the early error of 12.9.3.1 is not relaxed in strict mode; templates do not admit legacy octal escapes; `ImportCall` may not be extended; in strict code the Annex B extensions B.3.1, B.3.2, B.3.3 and B.3.5 are not supported; when parsing with Module, the lexical extensions of B.1.1 are not supported | Spec p.445–446 | normative; Annex B is [DATED] |
| `toLocaleString` and similar | Methods defined by ECMA-402 may not be extended beyond it | Spec p.445–446 | [HOST] |

### Conventions of standard built-in objects (clause 18)

| Topic | Rule | Page |
|---|---|---|
| Nature | Callable built-ins are built-in function objects, with `[[Extensible]]` true and `[[Realm]]` (the creation realm) | Spec p.446 |
| Missing arguments | Treated as `undefined` | Spec p.446 |
| Extra arguments | They are evaluated and ignored; the implementation may give them its own behavior, as long as it does not throw `TypeError` merely because of an extra argument. Recommendation: new capabilities enter as new functions, not new parameters | Spec p.446 |
| Default prototypes | Every built-in function/constructor has `Function.prototype` as `[[Prototype]]`; every built-in prototype has `Object.prototype`, except `Object.prototype` itself | Spec p.446 |
| Call versus construct | Constructor algorithms apply to both `[[Call]]` and `[[Construct]]`; they distinguish by `NewTarget` being `undefined` (call). Built-ins that are not constructors have neither `[[Construct]]` nor `prototype`, barring exceptions | Spec p.447 |
| `length` | Non-negative integer: required parameters in the header (optional and rest do not count); Spec example: `Array.prototype.map` has 1. Attributes: not writable, not enumerable, configurable | Spec p.447 |
| `name` | String with the Spec name; anonymous ones use empty; methods use the key; getter and setter have the prefixes `"get "` and `"set "`; Symbol keys have a specified name. Same attributes as `length` | Spec p.447 |
| Default attributes | Data properties of clauses 19–28 and B.2: writable, not enumerable, configurable, unless indicated; accessors: not enumerable, configurable, and if there is only a getter the setter is `undefined` (and vice versa) | Spec p.447 |

Example (application of the rule, [inference]): `Object.getOwnPropertyDescriptor(Math, "max")` shows a non-enumerable, writable and configurable property (Spec p.447).

---

## 2. Global object and global functions

### Global object

The global object is created before any execution context; it has no `[[Construct]]` (it is not used with `new`) nor `[[Call]]` (it is not called); its `[[Prototype]]` is host-defined; it may have extra host properties, including one that points to itself (Spec p.447–448) [HOST].

### Value properties

| Member | What it does / edge cases | Attributes | Page | Mark |
|---|---|---|---|---|
| `globalThis` | Value of `this` of the realm's global environment | writable, not enumerable, configurable | Spec p.448 | version not stated |
| `Infinity`, `NaN`, `undefined` | The values +∞, NaN and undefined | not writable, not enumerable, not configurable | Spec p.448 | normative |

Pitfall [extrapolation from the attributes]: since they are neither writable nor configurable, assigning to the global `undefined`, `NaN` or `Infinity` does not change them (silent in sloppy mode, `TypeError` in strict mode).

### Global functions

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `eval` | `eval(x)` | If `x` is not a string, returns `x` untouched. Otherwise parses it as a Script; text with no body returns `undefined`. Direct eval creates a lexical environment child of the caller's and uses the caller's variable environment and private environment; indirect eval uses the global environment and has no private environment. If the caller or the text is strict, `var` and functions go in a new variable environment, visible only to the eval; `let`, `const` and `class` always go to a new lexical environment. Result: the completion value of the body (empty becomes `undefined`) | `SyntaxError` (parse; `new.target` outside a function; `super.prop` outside a method; `super()` outside a derived constructor; `arguments` in a class field initializer) | Spec p.448–449 | the host may block it [HOST] |
| Eval declarations | (EvalDeclarationInstantiation) | In sloppy mode at global level, an eval `var` that collides with a global lexical declaration is an error; in sloppy direct eval, a `var` that would "rise" over a lexical binding of an intermediate block is an error (optional exception for a simple `catch` parameter in browsers); if a global function or var cannot be declared, error; several functions with the same name: the last one wins; optional compatibility block for functions declared in blocks | `SyntaxError`, `TypeError` | Spec p.450–452 | [HOST], [DATED] (web compatibility, "NORMATIVE OPTIONAL") |
| `HostEnsureCanCompileStrings` | (hook) | The host may block `eval` and the `Function` constructors; default: does not block | host-defined error | Spec p.450 | [HOST] |
| `isFinite` | `isFinite(number)` | Converts with `ToNumber` and returns `true` if finite. Unlike `Number.isFinite`, it coerces (`isFinite("12")` is `true`) | whatever `ToNumber` throws | Spec p.452 | coercion is [inference] |
| `isNaN` | `isNaN(number)` | Converts with `ToNumber`; `true` only if the result is `NaN` (`isNaN("abc")` is `true`). Function-free test: `X !== X` | whatever `ToNumber` throws | Spec p.453 | [inference] for the example |
| `parseFloat` | `parseFloat(string)` | Converts to string, strips leading whitespace, reads the longest prefix that is a decimal literal; with no valid prefix returns `NaN`; the rest is ignored without warning (`parseFloat("3.14abc")` gives 3.14) | — | Spec p.453 | example [inference] |
| `parseInt` | `parseInt(string, radix)` | `ToString` and leading whitespace removal; a leading `+`/`-` gives the sign; `radix` via `ToInt32`: 0 or `undefined` uses 10, except prefix `0x`/`0X` (then 16); a radix other than 0 outside 2–36 returns `NaN` (does not throw); the `0x` prefix is only removed with radix 16 or absent; reads digits (letters are worth 10–35) up to the first invalid one; with no digit, `NaN`; a zero result is `-0` for a negative sign (`parseInt("-0")` gives `-0`). In base 10 with more than 20 significant digits the digits after the 20th may be zeroed; in bases other than 2, 4, 8, 10, 16, 32 the value may be approximated | whatever `ToString`/`ToInt32` throw | Spec p.453–454 | numeric detail is implementation-dependent |
| `decodeURI` | `decodeURI(encodedURI)` | Decodes UTF-8 `%XX`, but preserves the sequences that correspond to `; / ? : @ & = + $ , #` | `URIError` | Spec p.454 | — |
| `decodeURIComponent` | `decodeURIComponent(s)` | Decodes everything (empty preserve set) | `URIError` (stray `%`, invalid hex, invalid or overlong UTF-8, 1-byte sequence or more than 4 bytes) | Spec p.455–457 | — |
| `encodeURI` | `encodeURI(uri)` | Encodes in UTF-8 as uppercase `%XX`; leaves letters, digits, `- . ! ~ * ' ( )` and `; / ? : @ & = + $ , #` unescaped | `URIError` (lone surrogate) | Spec p.455–456 | — |
| `encodeURIComponent` | `encodeURIComponent(c)` | Same, but without the extra set (encodes `; / ? : @ & = + $ , #`); `encodeURIComponent("a b&c")` gives `a%20b%26c` | `URIError` (lone surrogate) | Spec p.455–456 | example [inference] |

Notes on the URI functions: the reserved set comes from RFC 2396, not RFC 3986, and the Spec says that handling of web pages is outside its scope (Spec p.454) [DATED with respect to the RFCs]. A code point may generate several `%XX` sequences (Spec p.456). RFC 3629 forbids decoding invalid sequences, for example `0xC0 0x80` does not become code unit 0 (Spec p.457). `ParseHexOctet` validates each `%XX` on decode (Spec p.457).

### Constructors and namespaces exposed on the global

Constructors: `AggregateError`, `Array`, `ArrayBuffer`, `BigInt`, `BigInt64Array`, `BigUint64Array`, `Boolean`, `DataView`, `Date`, `Error`, `EvalError`, `FinalizationRegistry`, `Float16Array`, `Float32Array`, `Float64Array`, `Function`, `Int8Array`, `Int16Array`, `Int32Array`, `Iterator`, `Map`, `Number`, `Object`, `Promise`, `Proxy`, `RangeError`, `ReferenceError`, `RegExp`, `Set`, `SharedArrayBuffer`, `String`, `Symbol`, `SyntaxError`, `TypeError`, `Uint8Array`, `Uint8ClampedArray`, `Uint16Array`, `Uint32Array`, `URIError`, `WeakMap`, `WeakRef`, `WeakSet` (Spec p.457–460). Namespaces: `Atomics`, `JSON`, `Math`, `Reflect` (Spec p.460). Note that `Float16Array` appears as a global in this edition (Spec p.458); the edition of introduction is not stated.

---

## 3. Fundamental objects

### Object

Constructor: `Object(value)` can be called as a function (conversion) or with `new`, and used in `extends`. If `NewTarget` is neither `undefined` nor `Object` itself (subclass), it creates an object from the constructor; if `value` is `undefined` or `null`, it returns a new empty object with prototype `Object.prototype`; otherwise it returns `ToObject(value)` (Spec p.461). `Object(5)` returns a wrapped Number [inference].

#### Static members of Object

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Object.assign` | `(target, ...sources)` | `ToObject(target)`; a single argument returns the target; for each non-null/undefined source copies own enumerable properties (string and symbol keys) reading with `Get` and writing with `Set`; returns the target; `length` 2. Target setters fire, source getters run, shallow copy [inference] | `TypeError` for an `undefined`/`null` target [inference]; a failing `Set` throws | Spec p.461 | — |
| `Object.create` | `(O, Properties)` | `O` must be an object or `null`; creates an object with that prototype; if `Properties` is not `undefined`, applies `ObjectDefineProperties` | `TypeError` | Spec p.461–462 | — |
| `Object.defineProperties` | `(O, Properties)` | `O` an object; converts `Properties` with `ToObject`, first collects the descriptors of the own enumerable ones and only then defines them all; returns `O` | `TypeError` | Spec p.462 | — |
| `Object.defineProperty` | `(O, P, Attributes)` | `O` an object; key via `ToPropertyKey`; `Attributes` via `ToPropertyDescriptor`; defines, throwing on failure; returns `O` | `TypeError` | Spec p.462 | — |
| `Object.entries` | `(O)` | `ToObject`; array of `[key, value]` pairs of the own enumerable string-keyed properties | `TypeError` for `undefined`/`null` [inference] | Spec p.462 | — |
| `Object.freeze` | `(O)` | Non-object: returns `O` without error; otherwise level FROZEN; failure is an error | `TypeError` | Spec p.463 | — |
| `Object.fromEntries` | `(iterable)` | Requires a value coercible to an object; creates a plain object and adds each pair (key via `ToPropertyKey`) from the iterable | `TypeError` for `undefined`/`null` [inference] | Spec p.463 | version not stated |
| `Object.getOwnPropertyDescriptor` | `(O, P)` | `ToObject(O)`, `ToPropertyKey(P)`; returns a descriptor as an object or `undefined` | `TypeError` if `O` is null | Spec p.463 | — |
| `Object.getOwnPropertyDescriptors` | `(O)` | Object with the descriptors of all own keys (string and symbol); keys without a descriptor are omitted | — | Spec p.463 | version not stated |
| `Object.getOwnPropertyNames` | `(O)` | Array of own string keys (includes non-enumerable) | — | Spec p.463 | — |
| `Object.getOwnPropertySymbols` | `(O)` | Array of own symbol keys (both use `GetOwnPropertyKeys`, which does `ToObject` and filters by type) | — | Spec p.464 | — |
| `Object.getPrototypeOf` | `(O)` | `ToObject(O)` and returns the prototype | `TypeError` for null [inference] | Spec p.464 | — |
| `Object.groupBy` | `(items, callback)` | Groups elements of an iterable by the key the callback returns (converted to a property key); callback in ascending order with `(element, index)`; result is an object with no prototype whose properties are arrays | — | Spec p.464 | version not stated |
| `Object.hasOwn` | `(O, P)` | `ToObject(O)`, `ToPropertyKey(P)` and checks for an own property | `TypeError` for null [inference] | Spec p.464 | version not stated |
| `Object.is` | `(v1, v2)` | Uses `SameValue` (distinguishes +0 from -0; `NaN` equals `NaN` [inference from the name]) | — | Spec p.465 | — |
| `Object.isExtensible` | `(O)` | Non-object: `false` | — | Spec p.465 | — |
| `Object.isFrozen`, `Object.isSealed` | `(O)` | Non-object: `true` (primitives count as already frozen and sealed) | — | Spec p.465 | — |
| `Object.keys` | `(O)` | Array of own enumerable string keys | `TypeError` for null [inference] | Spec p.465 | — |
| `Object.preventExtensions` | `(O)` | Non-object: returns `O`; if `[[PreventExtensions]]` returns false, error | `TypeError` | Spec p.465 | — |
| `Object.prototype` | property | Not writable, not enumerable, not configurable | — | Spec p.465 | — |
| `Object.seal` | `(O)` | Non-object: returns `O`; otherwise level SEALED; failure is an error | `TypeError` | Spec p.465–466 | — |
| `Object.setPrototypeOf` | `(O, proto)` | `O` coercible to an object; `proto` an object or `null`; if `O` is not an object returns `O`; failure of `[[SetPrototypeOf]]` is an error | `TypeError` | Spec p.466 | — |
| `Object.values` | `(O)` | Array of the values of the own enumerable string-keyed properties | `TypeError` for null [inference] | Spec p.466 | — |

General pitfall: functions that do `ToObject` throw on `undefined`/`null`; `freeze`, `seal` and `preventExtensions` with primitives do not throw, they only return the value (Spec p.463, 465).

#### Object prototype

`Object.prototype` has `[[Extensible]]` true, `[[Prototype]]` `null` and is an immutable prototype object (its `[[SetPrototypeOf]]` is special, 10.4.7.1); therefore its prototype cannot be changed [inference] (Spec p.466). The initial `constructor` is `%Object%` (Spec p.466). Ordinary instances have no special properties beyond the inherited ones (Spec p.470).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `hasOwnProperty` | `(V)` | Converts the key first and only then does `ToObject(this)`, to preserve exceptions from earlier versions even with a null `this` | `TypeError` for null `this` | Spec p.466 | — |
| `isPrototypeOf` | `(V)` | `V` a non-object: `false`; walks up the chain of `V` comparing with `this`; the order of the steps preserves earlier behavior | — | Spec p.466–467 | — |
| `propertyIsEnumerable` | `(V)` | Key via `ToPropertyKey`, `ToObject(this)`; returns whether the own property exists and is enumerable; does not look at the chain | — | Spec p.467 | — |
| `toLocaleString` | `([reserved1[, reserved2]])` | Calls the `this`'s `toString` via `Invoke`; parameters reserved for ECMA-402; Array, Number, Date and `%TypedArray%` have their own versions | — | Spec p.467 | [HOST] for locale |
| `toString` | `()` | `undefined` gives `"[object Undefined]"`, `null` gives `"[object Null]"`; otherwise `ToObject(this)` and an internal tag (Array, Arguments, Function, Error, Boolean, Number, String, Date, RegExp or Object), which is replaced by `Symbol.toStringTag` if that is a string; result `"[object " + tag + "]"`. The Spec warns that it is not a reliable type test and that `toStringTag` can invalidate legacy tests | — | Spec p.467–468 | — |
| `valueOf` | `()` | Returns `ToObject(this)` | `TypeError` for null | Spec p.468 | — |
| `__proto__` | accessor | Getter: `ToObject(this)` and returns the prototype. Setter: `this` coercible to an object; a value that is neither an object nor `null`, or a non-object `this`: returns `undefined` doing nothing; failure to change is an error. Not enumerable, configurable | `TypeError` | Spec p.468 | [DATED] ("NORMATIVE OPTIONAL, LEGACY") |
| `__defineGetter__`, `__defineSetter__` | `(P, fn)` | `ToObject(this)`; defines an enumerable, configurable accessor with only that function; returns `undefined` | `TypeError` if `fn` is not callable | Spec p.469 | [DATED] |
| `__lookupGetter__`, `__lookupSetter__` | `(P)` | Walk up the chain until the property is found; return the getter/setter if it is an accessor, otherwise `undefined` | — | Spec p.469 | [DATED] |

---

## 4. Function

### Function

Constructor `Function(...parameters, body)`: calling without `new` is equivalent to `new`; it can be used in `extends`, but subclasses need `super`; there is no syntax for subclasses beyond the GeneratorFunction, AsyncFunction and AsyncGeneratorFunction constructors (Spec p.470). The last argument is the body; the earlier ones are parameters and may come together in one string (`("a,b","c", ...)`) (Spec p.470). `CreateDynamicFunction` (Spec p.470–472): converts each argument with `ToString`; the host may block it [HOST]; the stored source code is `function anonymous(<params>\n) {\n<body>\n}` (prefixes `function*`, `async function`, `async function*` according to the kind); parameters and body are parsed separately and each must be valid on its own (the Spec example `new Function("/*", "*/ ) {")` does not create a function); any error is `SyntaxError`; the scope is the realm's global environment, not the creator's local one; the name is `"anonymous"`; normal functions get a `prototype` and are constructors; generators and async generators get their own `prototype`; async functions are not constructors and have no `prototype` (Spec p.471–472).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Function.length` | property | 1 | — | Spec p.472 | — |
| `Function.prototype` (property) | property | Not writable, not enumerable, not configurable | — | Spec p.472 | — |
| `Function.prototype` (object) | — | It is itself a built-in function: accepts any argument and returns `undefined`; no `[[Construct]]`, no `prototype`; `length` 0, empty `name`. It is a function for compatibility with pre-ES2015 code | — | Spec p.472–473 | [VERSION-DEPENDENT] (reason tied to ES2015) |
| `apply` | `(thisArg, argArray)` | `this` callable; `argArray` `undefined`/`null` calls with no arguments, otherwise converts the array-like into a list; tail-call optimization may exist. `thisArg` is passed unmodified (Edition 3 replaced `undefined`/`null` with the global and did `ToObject`; non-strict functions still do this on entry). Arrow and bound ignore `thisArg` | `TypeError` if `this` is not callable | Spec p.472–473 | Edition 3 [DATED] |
| `bind` | `(thisArg, ...args)` | Creates a bound function (exotic, no `prototype`). `length` = `max(target's length - number of pre-applied args, 0)` when the target's `length` is numeric (∞ stays ∞, -∞ becomes 0, non-Number becomes 0); `name` = `"bound " + name` (non-string name becomes empty). If the target is an arrow or bound, the new `thisArg` has no effect | `TypeError` if `this` is not callable | Spec p.473 | — |
| `call` | `(thisArg, ...args)` | Calls with `thisArg` and the arguments; same Edition 3 and arrow/bound notes | `TypeError` if not callable | Spec p.473–474 | — |
| `constructor` | property | Initial: `%Function%` | — | Spec p.474 | — |
| `toString` | `()` | If stored source text exists and the host allows exposing it, returns exactly that text; a built-in returns an implementation-defined representation with NativeFunction syntax (`function name(params) { [ native code ] }`); a callable object without source returns NativeFunction | `TypeError` if `this` is not a function | Spec p.474 | [HOST] (`HostHasSourceTextAvailable`, default `true`, Spec p.476) |
| `[Symbol.hasInstance]` | `(V)` | Uses `OrdinaryHasInstance(F, V)`; not writable, not enumerable, not configurable (avoids tampering that would expose a bound function's target). `v instanceof F` is equivalent to `F[Symbol.hasInstance](v)` | — | Spec p.474–475 | — |

Properties of function instances (Spec p.475–476): `length` (not writable, not enumerable, configurable), `name` (no semantic meaning; anonymous functions without a contextual name use empty) and `prototype` (writable, not enumerable, not configurable; exists on functions that can be constructors). Functions created by `bind`, by method definition (other than generator or async generator) and arrows have no `prototype` (Spec p.476).

---

## 5. Boolean

### Boolean

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Boolean` | `Boolean(value)` | `ToBoolean(value)`. Without `new` returns the primitive; with `new` creates an object with `[[BooleanData]]`. `new Boolean(false)` is an object (truthy), `Boolean(false)` is `false` [inference] | — | Spec p.476 | — |
| `Boolean.prototype` | property/object | Not writable/enumerable/configurable; the prototype itself is a Boolean object with value `false` | — | Spec p.476–477 | — |
| `toString` | `()` | `"true"` or `"false"` via `ThisBooleanValue` | `TypeError` if `this` is neither a boolean nor a Boolean object | Spec p.477 | — |
| `valueOf` | `()` | Returns the primitive via `ThisBooleanValue` | `TypeError` likewise | Spec p.477 | — |

---

## 6. Symbol

### Symbol

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Symbol` | `Symbol([description])` | Returns a new Symbol on each call (`Symbol("a") !== Symbol("a")` [inference]); `description` `undefined` stays `undefined`, otherwise `ToString`. Not for `new` nor subclassing | `TypeError` with `new` | Spec p.477–478 | [VERSION-DEPENDENT] (symbols are a later-edition feature; the Spec does not date it) |
| `Symbol.for` | `(key)` | Converts the key to a string and consults the global registry (append-only list, shared across realms, initially empty); returns the existing one or creates, registers and returns | — | Spec p.478 | — |
| `Symbol.keyFor` | `(sym)` | Returns the registry key, or `undefined` if the symbol was not registered | `TypeError` if `sym` is not a Symbol | Spec p.479, 482 | — |
| `description` | getter | `ThisSymbolValue(this)` and returns the description (may be `undefined`); no setter | `TypeError` if `this` is invalid | Spec p.480 | — |
| `toString` | `()` | `"Symbol(" + description + ")"` (empty description if `undefined`) | `TypeError` | Spec p.480–481 | — |
| `valueOf` | `()` | Returns the primitive symbol | `TypeError` | Spec p.481 | — |
| `[Symbol.toPrimitive]` | `(hint)` | Returns the primitive symbol, ignoring `hint`; name `"[Symbol.toPrimitive]"`; not writable, not enumerable, configurable | — | Spec p.481 | — |
| `[Symbol.toStringTag]` | property | Value `"Symbol"`; not writable, not enumerable, configurable | — | Spec p.481 | — |

`Symbol.prototype` is an ordinary object, is not a Symbol instance and has no `[[SymbolData]]` (Spec p.480). `ThisSymbolValue` accepts a symbol or an object with `[[SymbolData]]` (Spec p.481).

#### Well-known symbols

Properties of `Symbol`, all not writable, not enumerable, not configurable (Spec p.478–480): `asyncIterator`, `hasInstance` (p.478); `isConcatSpreadable`, `iterator`, `match`, `matchAll`, `replace`, `search`, `species` (p.479); `split`, `toPrimitive`, `toStringTag`, `unscopables` (p.480). The effects of each appear in the methods that consult them (for example `hasInstance` in Function, `toPrimitive` in Date, `species` in Promise, `toStringTag` in `Object.prototype.toString`).

Pitfall: `Symbol.for("a")` returns the same symbol on every call, including across realms (Spec p.478).

---

## 7. Error, native types and AggregateError

### Error

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Error` | `Error(message[, options])` | Calling without `new` is equivalent to calling with `new`. Creates an object with `[[ErrorData]]`; if `message` is not `undefined`, it becomes a string and is stored as a non-enumerable `message` property; then installs `cause`. Can be used in `extends` | — | Spec p.482 | — |
| `cause` (option) | `options.cause` | `InstallErrorCause`: if `options` is an object and has the property `"cause"` (including inherited, since it uses `HasProperty`), creates a non-enumerable `cause`. `new Error("x", { cause: e }).cause === e` [inference] | — | Spec p.487 | version not stated |
| `Error.isError` | `(arg)` | `true` if `arg` is an object with `[[ErrorData]]`, otherwise `false`; does not throw. `[[ErrorData]]` only identifies Error, AggregateError and NativeError for `Object.prototype.toString` and `Error.isError` | — | Spec p.483 | version not stated |
| `Error.prototype` | object | Ordinary, not an Error instance; `constructor` `%Error%`; `message` `""`; `name` `"Error"`. The `Error.prototype` property is not writable, not enumerable, not configurable | — | Spec p.483 | — |
| `toString` | `()` | `this` must be an object; reads `name` (default `"Error"`) and `message` (default empty), both to string; if `name` is empty returns `message`; if `message` is empty returns `name`; otherwise `name + ": " + message` | `TypeError` if `this` is not an object | Spec p.483 | — |

### Native error types

| Type | When the Spec uses it | Page | Mark |
|---|---|---|---|
| `EvalError` | No longer used by the Spec itself; exists for compatibility with earlier editions | Spec p.484 | [DATED] |
| `RangeError` | Value outside the allowed set or range | Spec p.484 | — |
| `ReferenceError` | Invalid reference detected | Spec p.484 | — |
| `SyntaxError` | Parsing error | Spec p.484 | — |
| `TypeError` | Unsuccessful operation when no other type describes the cause | Spec p.484 | — |
| `URIError` | Use of the global URI functions in a way incompatible with the definition | Spec p.484 | — |

Common structure: each constructor, called as a function, is equivalent to `new` with the same arguments; can be used in `extends`; same logic of non-enumerable `message` and `cause`. The `[[Prototype]]` of each constructor is `%Error%` (so `Object.getPrototypeOf(TypeError) === Error`); the constructor's `name` is its name; each has its own prototype whose `[[Prototype]]` is `Error.prototype`, with `constructor`, empty `message` and `name` equal to the name; these prototypes are not Error instances; instances have `[[ErrorData]]` (Spec p.484–486).

### AggregateError

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `AggregateError` | `AggregateError(errors, message[, options])` | Without `new` equivalent to with `new`; the constructor's `[[Prototype]]` is `%Error%`. `message` and `cause` as in Error; then converts the iterable `errors` into a list and defines the `errors` property (array; non-enumerable, writable, configurable). The iterable comes before the message, unlike Error | iteration errors propagate | Spec p.486 | version not stated |
| Prototype | — | Ordinary; `[[Prototype]]` `Error.prototype`; empty `message`; `name` `"AggregateError"` | — | Spec p.487 | — |

---

## 8. Number

### Number

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Number` | `Number(value)` | With an argument, `ToNumeric`; if the result is a BigInt converts to Number (may lose precision); with no argument, `+0`. Without `new` returns a primitive; with `new`, an object with `[[NumberData]]`. `Number(10n)` gives 10 [inference] | whatever `ToNumeric` throws (Symbol) [inference] | Spec p.487–488 | — |
| `Number.EPSILON` | constant | Difference between 1 and the smallest representable value greater than 1 (approx. 2.22 × 10^-16) | — | Spec p.488 | — |
| `Number.isFinite` | `(n)` | `false` if not a Number or not finite; no coercion | — | Spec p.488 | — |
| `Number.isInteger` | `(n)` | `true` for an integral Number | — | Spec p.488 | — |
| `Number.isNaN` | `(n)` | `false` if not a Number; `true` if `NaN`; does not convert (unlike the global) | — | Spec p.488–489 | — |
| `Number.isSafeInteger` | `(n)` | `true` if an integer with absolute value up to 2^53 - 1. Above that, the Number of an integer is shared with at least one other (9007199254740992 and 9007199254740993 give the same Number) | — | Spec p.489 | — |
| `Number.MAX_SAFE_INTEGER` | constant | 9007199254740991 (2^53 - 1) | — | Spec p.489 | — |
| `Number.MIN_SAFE_INTEGER` | constant | -9007199254740991 | — | Spec p.489 | — |
| `Number.MAX_VALUE` | constant | Approx. 1.7976931348623157 × 10^308 | — | Spec p.489 | — |
| `Number.MIN_VALUE` | constant | Approx. 5 × 10^-324, smallest positive (denormalized; if the implementation does not support denormals, it is the smallest representable positive) | — | Spec p.490 | — |
| `Number.NaN`, `NEGATIVE_INFINITY`, `POSITIVE_INFINITY` | constants | NaN, -∞, +∞ | — | Spec p.490 | — |
| `Number.parseFloat`, `Number.parseInt` | functions | They are the same objects as the globals | — | Spec p.490 | — |
| `Number.prototype` | property | Not writable, not enumerable, not configurable | — | Spec p.490 | — |

All Number constants are not writable, not enumerable and not configurable (Spec p.488–490).

#### Number prototype

The prototype is a Number object with value `+0`; the methods are not generic: `this` must be a Number or an object with `[[NumberData]]`, otherwise `TypeError` (Spec p.490, 494). The initial `constructor` is `%Number%` (Spec p.491).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `toExponential` | `(fractionDigits)` | Exponential notation with one digit before the point and `fractionDigits` after; `undefined` uses the digits needed to identify the number; `ToIntegerOrInfinity`. A non-finite value returns the standard `NaN`/`Infinity` text before checking the range (`NaN.toExponential(500)` gives `"NaN"`). Zero gives exponent `+0`; the exponent always has a sign | `RangeError` outside 0–100 | Spec p.491–492 | — |
| `toFixed` | `(fractionDigits)` | Fixed point with N places; `undefined` is 0; non-finite returns the standard text; `x >= 10^21` returns the normal `ToString` (exponential); picks the integer n with n/10^f closest to x and, on a tie, the larger n. `(1000000000000000128).toFixed(0)` gives `"1000000000000000128"` while `toString` gives `"1000000000000000100"` | `RangeError` if infinite or outside 0–100 | Spec p.492 | — |
| `toLocaleString` | `([reserved1[, reserved2]])` | With ECMA-402 follows that specification; otherwise host locale formatting, possibly equal to `toString` | — | Spec p.493 | [HOST] |
| `toPrecision` | `(precision)` | `undefined` returns `ToString(x)`; non-finite returns the standard text (checked before the range); generates `precision` significant digits; exponential if the exponent is less than -6 or greater than or equal to `precision`, otherwise fixed point | `RangeError` outside 1–100 | Spec p.493–494 | — |
| `toString` | `([radix])` | `radix` an integer from 2 to 36; `undefined` is 10; the function's `length` is 1 | `RangeError` outside 2–36 | Spec p.494 | — |
| `valueOf` | `()` | Returns the primitive via `ThisNumberValue` | `TypeError` | Spec p.494 | — |

---

## 9. BigInt

### BigInt

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `BigInt` | `BigInt(value)` | Type conversion. `ToPrimitive` with hint number; if it is a Number uses `NumberToBigInt` (requires an integer); other primitives go through `ToBigInt`. Not for `new` nor subclassing | `TypeError` with `new`; `RangeError` for a non-integer Number (`BigInt(1.5)`, `NaN`, `Infinity`) | Spec p.494–495 | version not stated |
| `BigInt.asIntN` | `(bits, bigint)` | `bits` via `ToIndex`, `bigint` via `ToBigInt`; computes modulo 2^bits and, if the result is greater than or equal to 2^(bits-1), subtracts 2^bits (signed two's complement) | error from `ToIndex`/`ToBigInt` | Spec p.495 | — |
| `BigInt.asUintN` | `(bits, bigint)` | Same, returning the unsigned modulo 2^bits (`BigInt.asUintN(8, 257n)` gives `1n` [inference]) | likewise | Spec p.495 | — |
| `BigInt.prototype` | property | Not writable, not enumerable, not configurable | — | Spec p.495 | — |
| `toLocaleString` | `([r1[, r2]])` | With ECMA-402 follows that; otherwise implementation-defined | — | Spec p.496 | [HOST] |
| `toString` | `([radix])` | Like Number: radix 2–36, `undefined` is 10 | `RangeError` outside the range; `TypeError` if `this` is not a BigInt | Spec p.496 | — |
| `valueOf` | `()` | Returns the primitive BigInt via `ThisBigIntValue` | `TypeError` | Spec p.496 | — |
| `[Symbol.toStringTag]` | property | `"BigInt"`; not writable, not enumerable, configurable | — | Spec p.497 | — |

The prototype is an ordinary object, not a BigInt object (Spec p.495–496); instances inherit from it and have `[[BigIntData]]` (Spec p.497).

---

## 10. Math

### Math

`Math` is an ordinary object, the value of the global property `"Math"`, with prototype `Object.prototype`; it has neither `[[Construct]]` nor `[[Call]]`, so `new Math()` and `Math()` fail (Spec p.497; the expected `TypeError` is [inference]). `Math[Symbol.toStringTag]` is `"Math"` (not writable, not enumerable, configurable) (Spec p.498).

Precision: for `acos, acosh, asin, asinh, atan, atanh, atan2, cbrt, cos, cosh, exp, expm1, hypot, log, log1p, log2, log10, pow, random, sin, sinh, tan, tanh` the Spec only requires results in the boundary cases; otherwise the result is an approximation and the algorithm is the implementation's; it recommends (without requiring) the IEEE 754-2019 algorithms of fdlibm (Spec p.498) [HOST]. Consequence [inference]: the last digit may differ between engines. Convention: almost all start with `ToNumber` (whatever the conversion throws propagates) and preserve the sign of zero in several cases (Spec p.499–508).

#### Constants (not writable, not enumerable, not configurable; Spec p.497–498)

| Member | Approximate value | Page |
|---|---|---|
| `Math.E` | 2.718281828459045 | Spec p.497 |
| `Math.LN10` | 2.302585092994046 | Spec p.497 |
| `Math.LN2` | 0.6931471805599453 | Spec p.497 |
| `Math.LOG10E` | 0.4342944819032518 (approx. inverse of LN10) | Spec p.497 |
| `Math.LOG2E` | 1.4426950408889634 (approx. inverse of LN2) | Spec p.498 |
| `Math.PI` | 3.141592653589793 | Spec p.498 |
| `Math.SQRT1_2` | 0.7071067811865476 (approx. inverse of SQRT2) | Spec p.498 |
| `Math.SQRT2` | 1.4142135623730951 | Spec p.498 |

`Math.PI = 3` changes nothing (in strict mode, an error) [inference].

#### Functions

Errors: none throws by itself, except through conversion (`ToNumber`) and `sumPrecise`.

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `abs` | `(x)` | NaN gives NaN; -0 gives +0; -Infinity gives +Infinity | — | Spec p.499 | — |
| `acos` | `(x)` | Radians from 0 to π; NaN or outside [-1, 1] gives NaN; 1 gives +0 | — | Spec p.499 | — |
| `acosh` | `(x)` | NaN and +Infinity return themselves; 1 gives +0; less than 1 gives NaN | — | Spec p.499 | — |
| `asin` | `(x)` | From -π/2 to π/2; NaN and ±0 return themselves; outside [-1, 1] gives NaN | — | Spec p.499 | — |
| `asinh` | `(x)` | Non-finite values and ±0 return themselves | — | Spec p.499 | — |
| `atan` | `(x)` | From -π/2 to π/2; NaN and ±0 themselves; ±Infinity gives ±π/2 | — | Spec p.500 | — |
| `atanh` | `(x)` | NaN and ±0 themselves; absolute value greater than 1 gives NaN; 1 gives +Infinity; -1 gives -Infinity | — | Spec p.500 | — |
| `atan2` | `(y, x)` | Order (y, x) is intentional; result from -π to π; converts y and then x. NaN in either gives NaN. Infinities: (+Inf,+Inf) π/4; (+Inf,-Inf) 3π/4; (+Inf, finite) π/2 and negative analogues. y = +0: x positive or +0 gives +0, otherwise π; y = -0: x positive or +0 gives -0, otherwise -π. `atan2(0, -0)` gives π and `atan2(-0, -0)` gives -π. Swapping the order gives the wrong angle [inference] | — | Spec p.500–501 | — |
| `cbrt` | `(x)` | Cube root; non-finite values and ±0 themselves | — | Spec p.501 | — |
| `ceil` | `(x)` | Smallest integer not less than x; x in (-1, -0) gives -0 (`Object.is(Math.ceil(-0.5), 0)` is false [inference]); equivalent to `-Math.floor(-x)` | — | Spec p.501 | — |
| `clz32` | `(x)` | `ToUint32` and counts leading zero bits in 32 bits; 0 gives 32 | — | Spec p.501 | — |
| `cos` | `(x)` | Radians; non-finite gives NaN; ±0 gives 1 | — | Spec p.501–502 | — |
| `cosh` | `(x)` | ±Infinity gives +Infinity; ±0 gives 1 | — | Spec p.502 | — |
| `exp` | `(x)` | NaN and +Infinity themselves; ±0 gives 1; -Infinity gives +0 | — | Spec p.502 | — |
| `expm1` | `(x)` | exp(x) - 1 with precision near 0; -Infinity gives -1 | — | Spec p.502 | — |
| `floor` | `(x)` | Largest integer not greater than x; x in (0, 1) gives +0; equivalent to `-Math.ceil(-x)` | — | Spec p.502–503 | — |
| `fround` | `(x)` | Rounds to binary32 (ties to even) and back to binary64 | — | Spec p.503 | — |
| `f16round` | `(x)` | Same via binary16. Not equivalent to `fround` followed by rounding to 16 bits: for k = 1.00048828125000022204 the Spec gives 1.0009765625 and 1 | — | Spec p.503 | version not stated |
| `hypot` | `(...args)` | `ToNumber` on all first; any ±Infinity gives +Infinity even with NaN (`Math.hypot(NaN, Infinity)` gives Infinity); then NaN; all zeros (including no arguments) gives +0; `length` 2; must avoid naive overflow and underflow | conversion error | Spec p.503–504 | — |
| `imul` | `(x, y)` | `ToUint32` on both, product modulo 2^32 reinterpreted as signed | — | Spec p.504 | — |
| `log` | `(x)` | NaN and +Infinity themselves; 1 gives +0; ±0 gives -Infinity; negative gives NaN | — | Spec p.504 | — |
| `log1p` | `(x)` | ln(1+x); -1 gives -Infinity; less than -1 gives NaN | — | Spec p.504 | — |
| `log10`, `log2` | `(x)` | Same pattern as `log` | — | Spec p.504–505 | — |
| `max` | `(...args)` | `ToNumber` on all before examining NaN; with no arguments gives -Infinity; NaN is contagious; +0 is greater than -0; `length` 2 | conversion error | Spec p.505–506 | — |
| `min` | `(...args)` | Symmetric: with no arguments gives +Infinity; -0 is less than +0; `length` 2 | conversion error | Spec p.505–506 | — |
| `pow` | `(base, exponent)` | Converts base and then exponent and delegates to `Number::exponentiate` (details in another file) | conversion error | Spec p.506 | — |
| `random` | `()` | Number in [0, 1) approximately uniform; implementation algorithm; each distinct realm must produce a distinct sequence. No seed and no reproducibility guarantee; not for cryptography [extrapolation] | — | Spec p.506 | [HOST] |
| `round` | `(x)` | Nearest integer; ties go toward +Infinity; x in (0, 0.5) gives +0; x in [-0.5, -0) gives -0. `Math.round(3.5)` is 4 and `Math.round(-3.5)` is -3; not always equal to `Math.floor(x + 0.5)` | — | Spec p.506 | — |
| `sign` | `(x)` | NaN and ±0 themselves; negative -1; otherwise 1 | — | Spec p.506 | — |
| `sin` | `(x)` | NaN and ±0 themselves; ±Infinity gives NaN | — | Spec p.507 | — |
| `sinh` | `(x)` | Non-finite values and ±0 themselves | — | Spec p.507 | — |
| `sqrt` | `(x)` | NaN, ±0 and +Infinity themselves (-0 returns -0); negative (including -Infinity) gives NaN | — | Spec p.507 | — |
| `sumPrecise` | `(items)` | Sum of an iterable of Numbers without accumulating intermediate rounding; `RequireObjectCoercible`; initial state -0, so an empty iterable or one with only -0 gives -0; NaN gives NaN; +Infinity and -Infinity together give NaN; only +Infinity or only -Infinity gives that infinity; a non-Number element (including strings) throws and closes the iterator; a count of 2^53 - 1 throws `RangeError` | `TypeError`, `RangeError` | Spec p.507–508 | version not stated |
| `tan` | `(x)` | NaN and ±0 themselves; ±Infinity gives NaN | — | Spec p.508 | — |
| `tanh` | `(x)` | ±0 and NaN themselves; ±Infinity gives ±1 | — | Spec p.508 | — |
| `trunc` | `(x)` | Removes the fractional part; x in (0, 1) gives +0; in (-1, 0) gives -0 | — | Spec p.509 | — |

---

## 11. Date

### Date

#### Time values and calendar

| Topic | Rule | Page |
|---|---|---|
| Time value | Number: finite integer (milliseconds) or `NaN`. Epoch: 1/1/1970 00:00 UTC is the value +0; proleptic Gregorian calendar; day of 86,400 s; no leap seconds | Spec p.509 |
| Range | From -8,640,000,000,000,000 to +8,640,000,000,000,000 ms (±100,000,000 days; about ±273,790 years); an operation with `NaN` gives `NaN` | Spec p.509 |
| Calendar | Month from 0 (January) to 11; day of month from 1 to 31; day of week from 0 (Sunday) to 6; `WeekDay(+0)` is 4 (Thursday). Leap year: a multiple of 4 that is a multiple of 400 or is not a multiple of 100 | Spec p.509–512 |
| `MakeTime` | Any non-finite argument gives NaN; truncates each one; adds in the order (h, m, s, ms) because floating point is not associative | Spec p.517–518 |
| `MakeDay` | Non-finite gives NaN; truncates; excess months roll over into the year; day 0 or month 12 "overflow" [inference]; outside the range gives NaN | Spec p.518 |
| `MakeFullYear` | NaN gives NaN; truncates; years from 0 to 99 become 1900 + year (`new Date(99, 0)` is 1999, `new Date(100, 0)` is the year 100) | Spec p.518 |
| `TimeClip` | Non-finite or absolute value above 8.64e15 gives NaN; otherwise truncates | Spec p.518 |
| `LocalTime` / `UTC` | Convert between UTC and the local time of the system time zone. In `UTC(t)`, a repeated local time (end of daylight saving time) uses the offset before the transition; a nonexistent local time also uses the offset before the transition (pushes the time forward). Spec examples in New York: 01:30 on 11/5/2017 is UTC-04; 02:30 on 3/12/2017 is UTC-05. `UTC(LocalTime(t))` does not always return t | Spec p.516–517 |
| Time zones | Identifiers made of ASCII code units, named or by offset; "UTC" mandatory and primary; ECMA-402 implementations must support IANA Zone and Link names. `GetNamedTimeZoneEpochNanoseconds`, `GetNamedTimeZoneOffsetNanoseconds`, `AvailableNamedTimeZoneIdentifiers` and `SystemTimeZoneIdentifier` are host-defined; without political rules only "UTC" | Spec p.513–516 [HOST] |

Interchange format (Spec p.519–521): `YYYY-MM-DDTHH:mm:ss.sssZ`, a simplification of ISO 8601; date-only forms (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`) and date-time forms (`THH:mm`, `THH:mm:ss`, `THH:mm:ss.sss`) with an optional offset; `24:00` is the midnight at the end of the day; only numeric offsets (there is no standard for abbreviations such as CET or EST). Expanded year: always 6 digits with a sign; year 0 is `+000000`, and `-000000` is invalid; expanded years outside the range are not recognized by `Date.parse` (gives NaN) (Spec p.520). Offsets accept two-digit hours, minutes, seconds and a fraction (up to 9 digits), in extended or basic form (Spec p.520–522).

#### Constructor and static members

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Date` | `Date(...values)` | Without `new` returns a string of the current instant (ignores arguments), not a Date. With no arguments: the current instant. One argument: a Date copies the value; otherwise `ToPrimitive` and, if a string, interprets it as `Date.parse`, otherwise `ToNumber`; then `TimeClip`. Two or more: `ToNumber` on each, year via `MakeFullYear`, day defaults to 1 and the rest to 0, interpreted as local time, then `TimeClip`. `length` 7. Subclasses need `super` | — | Spec p.522–523 | — |
| `Date.now` | `()` | Current time value (UTC) | — | Spec p.523 | — |
| `Date.parse` | `(string)` | `ToString` and interprets it. Tries the interchange format first; outside it the implementation may use heuristics, and unrecognizable or out-of-bounds strings must give NaN. Missing parts: MM and DD become 01, HH/mm/ss become 00, sss becomes 000. A date-only form is UTC; a date-time form without an offset is local time (`"2020-01-01"` and `"2020-01-01T00:00"` may differ depending on the time zone [inference]). Round trip guaranteed for `valueOf`, `toString`, `toUTCString` and `toISOString` with ms 0; not for `toLocaleString` | — | Spec p.523–524 | [HOST] outside the standard format |
| `Date.UTC` | `(year[, month[, date[, hours[, minutes[, seconds[, ms]]]]]])` | `ToNumber`; year via `MakeFullYear`; month defaults to 0, day to 1, the rest to 0; returns a time value (Number, not Date) interpreting in UTC; `length` 7 | — | Spec p.524 | — |
| `Date.prototype` | property | Not writable, not enumerable, not configurable | — | Spec p.524 | — |

#### Date prototype

The prototype is ordinary, not a Date (no `[[DateValue]]`); unless indicated the methods are not generic and require `[[DateValue]]` (the Spec states the `TypeError` explicitly in `toString`; in the others the link to `RequireInternalSlot` is [extrapolation]) (Spec p.524, 534). The initial `constructor` is `%Date%` (Spec p.524).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `getDate`, `getDay`, `getFullYear`, `getHours`, `getMilliseconds`, `getMinutes`, `getMonth`, `getSeconds` | `()` | If the time value is NaN they return NaN; otherwise apply the calendar function over local time | `TypeError` if `this` is not a Date [extrapolation] | Spec p.524–526 | — |
| `getUTCDate`, `getUTCDay`, `getUTCFullYear`, `getUTCHours`, `getUTCMilliseconds`, `getUTCMinutes`, `getUTCMonth`, `getUTCSeconds` | `()` | Same pattern without conversion to local time | likewise | Spec p.526–527 | — |
| `getTime`, `valueOf` | `()` | Return the `[[DateValue]]` (NaN remains) | likewise | Spec p.526, 537 | — |
| `getTimezoneOffset` | `()` | `(t - LocalTime(t)) / msPerMinute`: positive when the local time zone is behind UTC [inference]; NaN gives NaN | likewise | Spec p.526 | — |
| `setDate(date)`, `setMilliseconds(ms)`, `setMinutes(min[, sec[, ms]])`, `setMonth(month[, date])`, `setSeconds(sec[, ms])` | per signature | Convert the arguments with `ToNumber` before checking NaN (conversion errors occur even with an invalid date); if the current value is NaN they return NaN without storing; omitted arguments reuse the current values; apply `TimeClip(UTC(...))`, store and return the new value. `length`: setMinutes 3, setMonth 2, setSeconds 2 | conversion error | Spec p.528–530 | — |
| `setHours` | `(hour[, min[, sec[, ms]]])` | Same pattern; `length` 4 | likewise | Spec p.528–529 | — |
| `setFullYear` | `(year[, month[, date]])` | The one exception: if the current value is NaN it uses +0 as the base (allows "fixing" an invalid Date); `length` 3 | likewise | Spec p.528 | — |
| `setTime` | `(time)` | `ToNumber` and `TimeClip` without local conversion; works even with a current value of NaN | — | Spec p.530 | — |
| `setUTCDate`, `setUTCFullYear`, `setUTCHours`, `setUTCMilliseconds`, `setUTCMinutes`, `setUTCMonth`, `setUTCSeconds` | per signature | UTC versions (without `LocalTime`/`UTC`); `setUTCFullYear` uses +0 if NaN; `length`: FullYear 3, Hours 4, Minutes 3, Month 2, Seconds 2 | likewise | Spec p.530–533 | — |
| `toDateString` | `()` | NaN gives `"Invalid Date"`; otherwise "Day Month dd yyyy" in local time | — | Spec p.533, 535 | — |
| `toISOString` | `()` | Interchange format in UTC, full, with `Z` | `RangeError` if NaN or the year is not representable | Spec p.533 | — |
| `toJSON` | `(key)` | `key` ignored; `ToObject(this)`, `ToPrimitive` with hint number; a non-finite Number gives `null`; otherwise calls `toISOString`. Generic, but requires `toISOString`. `JSON.stringify` of an invalid Date gives `null` while `toISOString` throws [inference] | `TypeError` if there is no callable `toISOString` [inference] | Spec p.533 | — |
| `toLocaleDateString`, `toLocaleString`, `toLocaleTimeString` | `([r1[, r2]])` | With ECMA-402 they follow that; otherwise an implementation-defined readable string for the date part, the full value or the time part in the environment's time zone and locale | — | Spec p.534 | [HOST] |
| `toString` | `()` | `ToDateString`: NaN gives `"Invalid Date"`; otherwise local date, time and time zone; `Date.parse(d.toString()) = d.valueOf()` for multiples of 1000 | `TypeError` if `this` is not a Date | Spec p.534–536 | — |
| `toTimeString` | `()` | NaN gives `"Invalid Date"`; otherwise local time plus time zone (time zone name in parentheses, implementation-defined) | — | Spec p.536 | [HOST] for the name |
| `toUTCString` | `()` | Based on the HTTP-date of RFC 7231: "Day, dd Month yyyy hh:mm:ss GMT"; NaN gives `"Invalid Date"` | — | Spec p.537 | — |
| `[Symbol.toPrimitive]` | `(hint)` | Dates are unique in treating the hint `"default"` as `"string"` (the other built-ins treat it as number); uses `OrdinaryToPrimitive` string-first or number-first. `date + 1` concatenates; `date - 1` and comparisons use the numeric hint [inference]. Not writable, not enumerable, configurable | `TypeError` if `this` is not an object or `hint` is not `"default"`, `"string"`, `"number"` | Spec p.537 | — |

Date instances are ordinary objects with `[[DateValue]]` (Spec p.537). Annex B legacy members for Date: `getYear` (local year minus 1900, with `TypeError` if not a Date), `setYear` (uses +0 if NaN and `MakeFullYear`) and `toGMTString` (the same object as `toUTCString`); the Spec recommends `getFullYear`, `setFullYear` and `toUTCString` (Spec p.854; EJpt p.198 also discourages `getYear`) [DATED].

---

## 12. JSON

### JSON

Ordinary object `%JSON%`, global `JSON`, with neither `[[Construct]]` nor `[[Call]]`; has `parse`, `stringify` and, in this edition, `rawJSON` and `isRawJSON` (Spec p.734, 739). The format is exactly that of ECMA-404, with no removals or extensions; extensions must go in another function, never in `JSON.parse` (Spec p.734–735). `JSON[Symbol.toStringTag]` is `"JSON"` (Spec p.745).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `JSON.parse` | `(text[, reviver])` | `ToString(text)`, `ParseJSON`; without a callable reviver returns the value. Duplicate keys: the last wins. A duplicate `__proto__` is not an error and does not change the prototype as in a literal. Reviver: called from the inside out (children before parents), with `this` equal to the container and `(key, value, context)`; `context.source` carries the exact text only for an unmodified primitive (same value by `SameValue`); returning `undefined` deletes the property, another value redefines it (without throwing on failure); arrays iterate up to the current `length`; objects over their own enumerable properties. `length` 2. Trailing comma, single quotes, comments and `undefined` are invalid [inference] | `SyntaxError` if the text is not valid JSON | Spec p.735–738 | `context.source` version not stated |
| `JSON.rawJSON` | `(text)` | `ToString`; empty is an error; the first character must be a lowercase ASCII letter, a digit, a double quote or a hyphen; the last must be a lowercase letter, a digit or a double quote (therefore never `]`, `}`, `-` or whitespace); goes through `ParseJSON` and the result must be a primitive; returns a frozen object with prototype `null` and the `rawJSON` property. Serves to preserve a large integer in serialization | `SyntaxError` | Spec p.739 | version not stated |
| `JSON.isRawJSON` | `(O)` | `true` if `O` is an object with `[[IsRawJSON]]` | — | Spec p.734 | version not stated |
| `JSON.stringify` | `(value[, replacer[, space]])` | Returns a JSON string or `undefined`. `replacer` function: called with `this` equal to the holder and `(key, value)`; `replacer` array: inclusion list of names (String, Number or wrappers; duplicates removed; applies to objects, not arrays). `space`: Number becomes `min(10, n)` spaces (less than 1 means no indentation); String uses the first 10 characters; any other type, no indentation. `length` 3. Creates a wrapper with an empty key. Order in `SerializeJSONProperty`: (1) if it is an object or BigInt and has a callable `toJSON`, calls it with the key; (2) applies the replacer; (3) an object with `[[IsRawJSON]]` is emitted literally; (4) unwraps Number, String, Boolean, BigInt wrappers; (5) `null`, `true`, `false`, strings in quotes, finite numbers via `ToString`, non-finite (`NaN`, `±Infinity`) become `"null"`; (6) a primitive BigInt throws; (7) a non-callable object becomes an array or object; the rest (`undefined`, functions, symbols) return `undefined`. In objects the property is omitted; in arrays it becomes `null`. Strings: `"` and `\` escaped, control characters as `\uHHHH` or short forms, lone surrogates as lowercase `\u` (well-formed JSON). Keys: replacer list or own enumerable string keys (symbols ignored [inference]). Empty object `{}`, empty array `[]`. `JSON.stringify({a:[1,undefined]})` gives `{"a":[1,null]}` [inference] | `TypeError` on a cycle (object stack) and for BigInt without `toJSON` | Spec p.739–745 | — |

---

## 13. WeakRef and FinalizationRegistry

### WeakRef

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `WeakRef` | `new WeakRef(target)` | A reference that does not prevent collection of an object or symbol. Runs `AddToKeptObjects(target)`, keeping the target alive during the current synchronous execution. Can be extended | `TypeError` without `new`; `TypeError` if the target cannot be held weakly (`new WeakRef(1)`) | Spec p.745–746 | version not stated |
| `deref` | `()` | Returns the target or `undefined` if it was collected. If it returns something other than `undefined`, the target is not collected until the end of the current execution, so a second `deref` in the same synchronous stretch cannot give `undefined` | `TypeError` if `this` is not a WeakRef | Spec p.746–747 | — |
| `[Symbol.toStringTag]` | property | `"WeakRef"` | — | Spec p.747 | — |

The moment of collection is not specified; do not build deterministic logic on it [inference]. The prototype is ordinary and without `[[WeakRefTarget]]`; `constructor` is `%WeakRef%` (Spec p.746).

### FinalizationRegistry

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `FinalizationRegistry` | `new FinalizationRegistry(cleanupCallback)` | Cleanup registry for collected targets; stores the realm, the callback (via `HostMakeJobCallback`) and `[[Cells]]` | `TypeError` without `new` or with a non-callable callback | Spec p.747–748 | [HOST] for callback execution; version not stated |
| `register` | `(target, heldValue[, unregisterToken])` | Adds a cell and returns `undefined`. `heldValue` stays alive while the cell exists, without keeping the target and token alive | `TypeError` if `this` is invalid; target or token (if given) not held weakly; `target` equal to `heldValue` (`SameValue`) | Spec p.748–749 | — |
| `unregister` | `(unregisterToken)` | Removes all cells with that token (`SameValue`); `true` if it removed any, otherwise `false` | `TypeError` if the token cannot be held weakly | Spec p.749 | — |
| `[Symbol.toStringTag]` | property | `"FinalizationRegistry"` | — | Spec p.749 | — |

The callback would receive the `heldValue`, not the collected object [inference]; the occurrence and timing of the callback are not guaranteed [extrapolation].

---

## 14. Atomics

### Atomics

Ordinary object `%Atomics%`, global `Atomics`, with neither `[[Construct]]` nor `[[Call]]`; operates indivisibly on shared memory and offers waiting and notification between agents; `Atomics[Symbol.toStringTag]` is `"Atomics"` (Spec p.723, 734). Common validations: `ValidateIntegerTypedArray` (integer types without clamp; for `wait`/`notify` only `Int32Array` or `BigInt64Array`; another type gives `TypeError`), `ValidateAtomicAccess` (`ToIndex`; `RangeError` if the index is greater than or equal to the length) and `RevalidateAtomicAccess` after the coercions (`TypeError` if the array went out of bounds, `RangeError` if the index exceeds the buffer) (Spec p.724–725). Read-modify-write operations convert the value (`ToBigInt` for BigInt arrays; otherwise `ToIntegerOrInfinity`) and return the old value (Spec p.730).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `add`, `and`, `or`, `sub`, `xor` | `(typedArray, index, value)` | Atomic operation; returns the previous value | `TypeError`, `RangeError` | Spec p.731–734 | — |
| `compareExchange` | `(typedArray, index, expected, replacement)` | Compares bytes after conversion to the element type; on a SAB uses SEQ-CST semantics; returns the value read (before the exchange), whether or not it swapped | likewise | Spec p.731 | — |
| `exchange` | `(typedArray, index, value)` | Stores and returns the old value | likewise | Spec p.732 | — |
| `isLockFree` | `(size)` | `ToIntegerOrInfinity`; 1, 2 and 8 depend on the implementation; 4 is always `true`; others `false`. All operations remain atomic | — | Spec p.732 | [HOST] for 1, 2, 8 |
| `load` | `(typedArray, index)` | Atomic SEQ-CST read | likewise | Spec p.732 | — |
| `store` | `(typedArray, index, value)` | Stores SEQ-CST and returns the coerced value `v` (not the old one, and not the "wrapped" value actually stored) | likewise | Spec p.733 | — |
| `wait` | `(typedArray, index, value, timeout)` | Suspends the agent; returns `"ok"`, `"timed-out"` or `"not-equal"`. Only `Int32Array`/`BigInt64Array` over a SharedArrayBuffer; value via `ToInt32`/`ToBigInt64`; timeout via `ToNumber`: NaN and +Infinity wait without limit, -Infinity and negatives become 0. The implementation may add an unpredictable extra time | `TypeError` (non-shared buffer, wrong type, agent that cannot suspend) | Spec p.727–728, 733 | [HOST] (`AgentCanSuspend`) |
| `waitAsync` | `(typedArray, index, value, timeout)` | Does not block; returns `{ async: false, value: "not-equal" }` if the value differs, `{ async: false, value: "timed-out" }` with timeout 0, or `{ async: true, value: <Promise> }` that fulfills with `"ok"` or `"timed-out"`. A finite timeout schedules a job via `HostEnqueueTimeoutJob` | likewise | Spec p.728–729, 733 | [HOST] |
| `notify` | `(typedArray, index, count)` | Wakes up to `count` waiters in FIFO order and returns how many it woke; `count` `undefined` means all; on a non-shared buffer returns +0 | `TypeError`, `RangeError` | Spec p.733–734 | — |

Internal structures (Waiter Record, WaiterList, critical section) and the fact that the resolution of `waitAsync` promises between agents uses `HostEnqueueGenericJob` are in Spec p.723–727 [HOST]. The informative note about growable `SharedArrayBuffer` recommends in-place growth (reserved virtual memory), requires new memory to be zeroed and forbids mixing of bits (tearing) (Spec p.715).

---

## 15. DataView

### DataView

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `DataView` | `new DataView(buffer[, byteOffset[, byteLength]])` | `buffer` must have the ArrayBuffer slots; offset via `ToIndex`; without `byteLength` and with a fixed-size buffer it covers up to the end; a resizable buffer or growable SAB leaves the length as AUTO (the view tracks the buffer); with `byteLength` (via `ToIndex`), `offset + byteLength` cannot go past the buffer. The checks are redone after creating the object. Subclasses need `super` | `TypeError` without `new`, without a buffer slot or with a detached buffer; `RangeError` if the offset or length exceed the buffer | Spec p.717–718 | — |
| `buffer` | getter | Returns the underlying buffer | — | Spec p.718 | — |
| `byteLength`, `byteOffset` | getters | Length and offset of the view | `TypeError` if the view is out of bounds | Spec p.719 | — |
| `getInt8`, `getUint8` | `(byteOffset)` | One byte | same as below | Spec p.720 | — |
| `getInt16`, `getUint16`, `getInt32`, `getUint32`, `getFloat16`, `getFloat32`, `getFloat64`, `getBigInt64`, `getBigUint64` | `(byteOffset[, littleEndian])` | Reads and converts; absent `littleEndian` is `false`, that is, big-endian | `TypeError` if `this` is not a DataView or the view is out of bounds; `RangeError` if `index + size` goes past the view | Spec p.719–721 | `getFloat16` version not stated |
| `setInt8`, `setUint8` | `(byteOffset, value)` | One byte | likewise | Spec p.721–722 | — |
| `setInt16`, `setUint16`, `setInt32`, `setUint32`, `setFloat16`, `setFloat32`, `setFloat64`, `setBigInt64`, `setBigUint64` | `(byteOffset, value[, littleEndian])` | Observable order: validates `this`, converts the index (`ToIndex`), converts the value (`ToBigInt` for the BigInt types, `ToNumber` for the others), converts `littleEndian` and only then checks bounds (side effects of `valueOf` occur before). Returns `undefined` | likewise | Spec p.717, 721–722 | `setFloat16` version not stated |
| `[Symbol.toStringTag]` | property | `"DataView"` | — | Spec p.722 | — |

Details: a view of length 0 with an offset exactly equal to the buffer size does not count as out of bounds (Spec p.716). The prototype does not have the slots; `DataView.prototype.byteLength` and the like throw `TypeError` [inference] (Spec p.718). Reading little-endian data without passing `true` gives swapped values [inference from usage].

---

## 16. Iteration interfaces and Iterator (helpers)

### Common interfaces

| Interface | Requires | Notes | Page |
|---|---|---|---|
| Iterable | `[Symbol.iterator]`, a function that returns an iterator | — | Spec p.749–750 |
| Iterator | `next` returning an IteratorResult; optional `return` and `throw` | After `done: true`, subsequent calls should keep `done: true` (not enforced); `return` signals that there will be no more `next`; `throw` signals an error condition. Arguments of `next` depend on the iterator; `for-of` passes no arguments. Callers must check for the existence of `return`/`throw`; `for-of`, `yield*` and array destructuring do the check | Spec p.750 |
| Async Iterable | `[Symbol.asyncIterator]` returning an async iterator | — | Spec p.750–751 |
| Async Iterator | `next` returning a promise of an IteratorResult; `return` and `throw` optional, also with promises | The `value` should not be a thenable (not enforced); `for-await-of` and `yield*` check `return`/`throw` | Spec p.751–752 |
| IteratorResult | boolean `done` (absent means `false`) and `value` | `value` is the current element with `done` false, or the return value with `done` true | Spec p.752 |

None of this is enforced by the engine: misbehaving iterators may resume after `done: true` [inference].

### Iterator

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Iterator` | `Iterator()` | Global `Iterator`, meant for `extends`. Called without `new` or with a direct `new Iterator()` it does not instantiate | `TypeError` | Spec p.753 | version not stated |
| `Iterator.concat` | `(...items)` | Eagerly validates that each item is an Object with `[Symbol.iterator]`; returns a lazy helper that opens each iterable in order and closes the inner one if the consumer finishes | `TypeError` (not an object, no `@@iterator`, non-object result) | Spec p.754 | version not stated |
| `Iterator.from` | `(O)` | Gets an iterator from `O` (accepts primitive strings); if it inherits from `%Iterator%` returns it directly, otherwise returns a wrapper (`%WrapForValidIteratorPrototype%`) whose `next` calls the original and whose `return` calls the original if it exists (otherwise `{undefined, done: true}`). Useful for giving helpers to iterator-like objects [inference] | — | Spec p.754–755 | version not stated |
| `Iterator.prototype` | property | Not writable, not enumerable, not configurable; `[[Prototype]]` is `Object.prototype`; reachable via `Object.getPrototypeOf(Object.getPrototypeOf([][Symbol.iterator]()))` | — | Spec p.755 | — |
| `constructor` | accessor | Getter returns `%Iterator%`; setter uses `SetterThatIgnoresPrototypeProperties`; not enumerable, configurable; reason: web compatibility | — | Spec p.755–756 | — |
| `[Symbol.toStringTag]` | accessor | Getter returns `"Iterator"`; setter same as the previous | — | Spec p.761 | — |
| `[Symbol.iterator]` | `()` | Returns `this`; name `"[Symbol.iterator]"`; every iterator is also iterable | — | Spec p.761 | — |

#### Helper methods

Common pattern (Spec p.756–761): `this` must be an Object (otherwise `TypeError`); a non-callable function argument throws `TypeError` and closes the iterator first; the callback runs with `this` equal to `undefined` and arguments `(value, counter)` with the counter starting at 0 (`reduce` receives `(accumulator, value, counter)`); if the callback throws, the source is closed before the error propagates; `drop`, `filter`, `flatMap`, `map`, `take` return a lazy helper, while `every`, `find`, `forEach`, `reduce`, `some`, `toArray` consume immediately; the source's `next` is obtained once by `GetIteratorDirect`. The methods operate on any object with `next`, not only on those inheriting from `Iterator` (Spec p.756).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `drop` | `(limit)` | `ToNumber`; discards the first `limit` values and passes the rest through; `Infinity` allowed | `RangeError` for NaN or negative (closing the iterator) | Spec p.756 | version not stated |
| `every` | `(predicate)` | `true` if all satisfy (or empty); at the first falsy closes and returns `false` | `TypeError` | Spec p.756–757 | — |
| `filter` | `(predicate)` | Delivers only values with a truthy predicate | `TypeError` | Spec p.757 | — |
| `find` | `(predicate)` | First value that satisfies, closing the iterator; otherwise `undefined` | `TypeError` | Spec p.757 | — |
| `flatMap` | `(mapper)` | Applies the mapper and gets an iterator from the result in a mode that rejects primitives (strings included); delivers the inner elements; ending early closes the inner one and then the outer one | `TypeError` if the result is a primitive | Spec p.758 | — |
| `forEach` | `(procedure)` | Calls for each element; returns `undefined` | `TypeError` | Spec p.758 | — |
| `map` | `(mapper)` | Delivers the mapper's result for each value | `TypeError` | Spec p.759 | — |
| `reduce` | `(reducer[, initialValue])` | Without an initial value, the first becomes the accumulator (counter starts at 1); with an initial value, the counter starts at 0 | `TypeError` if empty and no initial value | Spec p.759 | — |
| `some` | `(predicate)` | `true` at the first truthy (closing); `false` if it runs out | `TypeError` | Spec p.759–760 | — |
| `take` | `(limit)` | Same validation as `drop`; delivers at most `limit` values and closes the source on reaching the limit (limit 0 closes without consuming) | `RangeError` | Spec p.760 | — |
| `toArray` | `()` | Consumes everything and returns an array | — | Spec p.760–761 | — |

Example (own): `Iterator.from([1,2,3,4]).filter(x => x % 2).map(x => x * 10).toArray()` gives `[10, 30]`. Pitfalls: helpers return iterators, not arrays; an iterator is consumed and does not restart; infinite iterators require `take` or methods that close early [inference]; `"3"` works as a limit via `ToNumber` (Spec p.756, 760).

#### Internal helper objects

`%IteratorHelperPrototype%` inherits from `%Iterator.prototype%`: `next()` resumes the internal generator; `return()` requires `[[UnderlyingIterators]]` (otherwise `TypeError`) and, if the helper has not started yet, completes and closes the underlying iterators returning `{value: undefined, done: true}`; tag `"Iterator Helper"` (Spec p.753). `%AsyncIteratorPrototype%` inherits from `Object.prototype` and its `[Symbol.asyncIterator]` returns `this` (Spec p.761). The Async-from-Sync Iterator is never accessible to code; it adapts a synchronous iterator (for example for `for-await-of`): `next` and `return` forward through the `Continuation` (synchronous errors become a rejected promise; a missing `return` resolves `{value, done: true}`; a non-object result rejects with `TypeError`); a missing `throw` closes the synchronous iterator and rejects with `TypeError` (Spec p.762–763). The `Continuation` awaits the `value` and closes the synchronous iterator if the value rejects (when `done` is false and `closeOnRejection` is true) (Spec p.764).

---

## 17. Promise

### Promise

Concepts: three exclusive states (pending, fulfilled, rejected); settled means not pending; resolved means settled or "locked in" to follow another promise (so it may still be pending); resolve or reject on an already resolved promise has no effect (Spec p.764). Reactions run as jobs enqueued by the host (`HostEnqueuePromiseJob`), never synchronously (Spec p.768–769) [HOST]. `HostPromiseRejectionTracker` is a host hook for unhandled rejections ("reject" when rejecting without a handler, "handle" when a handler is added later); the default does nothing, and "unhandled rejection" warnings are environment behavior (Spec p.768) [HOST].

Resolving functions (`CreateResolvingFunctions`, Spec p.766): `resolve` and `reject` share an already-called flag (the first call wins). `resolve(x)`: if `x` is the promise itself, rejects with `TypeError`; if `x` is not an object, fulfills with `x`; if reading `x.then` throws, rejects with the error; if `then` is not callable, fulfills with `x`; if it is callable, enqueues a job that calls `x.then(resolve, reject)` (the promise becomes resolved and pending). The thenable's `then` never runs synchronously inside `resolve` (Spec p.766, 769–770). Resolving with another promise costs extra jobs, so the microtask order differs from returning a plain value [inference].

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Promise` | `new Promise(executor)` | Creates a pending promise, calls `executor(resolve, reject)` synchronously; if the executor throws, calls `reject`, which has no effect if `resolve` was already called. The executor's return is ignored | `TypeError` without `new` or with a non-callable executor | Spec p.770–771 | — |
| `Promise.all` | `(iterable)` | Fulfills with an array in input order or rejects with the reason of the first rejection. `this` must be a constructor; looks up `this.resolve` (non-callable becomes a rejection); iterates synchronously, `promiseResolve` per item; the pending counter starts at 1 and each callback has an already-called flag; an empty iterable fulfills with `[]`; an iteration error closes the iterator and rejects. The other promises keep running after a rejection [inference] | `TypeError` (converted into a rejection) if `this` is not a constructor | Spec p.771–772 | — |
| `Promise.allSettled` | `(iterable)` | Fulfills with an array of `{status: "fulfilled", value}` or `{status: "rejected", reason}` after all have settled; only rejects on an iteration error or an invalid `resolve` | likewise | Spec p.773–774 | — |
| `Promise.any` | `(iterable)` | Fulfills with the first fulfilled value; if all reject, rejects with an `AggregateError` whose `errors` property (non-enumerable, writable, configurable) lists the reasons in input order; an empty iterable rejects with empty `errors` [inference] | likewise | Spec p.774–775 | — |
| `Promise.race` | `(iterable)` | Settles as the first one to settle; an empty iterable or entries that never finish produce a promise that never settles | likewise | Spec p.776 | — |
| `Promise.reject` | `(r)` | New promise rejected with `r`, using `this` as the constructor; does not unwrap (`Promise.reject(p)` rejects with `p`) [inference] | — | Spec p.776 | — |
| `Promise.resolve` | `(x)` | If `x` is a promise whose `x.constructor` is the same `this`, returns `x` (`Promise.resolve(p) === p`); otherwise creates a new one and resolves. Reading `x.constructor` can throw through a getter | `TypeError` if `this` is not an object | Spec p.777 | — |
| `Promise.try` | `(callback, ...args)` | Calls `callback(...args)` synchronously with `this` `undefined`; an exception becomes a rejected promise, a return becomes a resolved promise | `TypeError` if `this` is not an object | Spec p.777 | version not stated |
| `Promise.withResolvers` | `()` | Returns `{ promise, resolve, reject }` using `this` as the constructor | — | Spec p.777 | version not stated |
| `Promise[Symbol.species]` | getter | Returns `this`; name `"get [Symbol.species]"`; lets subclasses control the constructor of derived promises | — | Spec p.778 | — |
| `Promise.prototype` | property | Not writable, not enumerable, not configurable | — | Spec p.775 | — |
| `catch` | `(onRejected)` | Equivalent to `this.then(undefined, onRejected)`, invoking `then` dynamically | — | Spec p.778 | — |
| `finally` | `(onFinally)` | Constructor via `SpeciesConstructor`. A non-callable `onFinally` is passed as both handlers (ignored). Callable: runs with no arguments, waits for the return and returns the original value or reason; if `onFinally` throws or returns a rejected promise, that failure replaces the result | `TypeError` if `this` is not an object | Spec p.778–779 | — |
| `then` | `(onFulfilled, onRejected)` | Creates a derived promise via `SpeciesConstructor` and `PerformPromiseThen`: non-callable handlers become pass-through; pending attaches reactions; fulfilled or rejected enqueues a job; marks the promise as handled | `TypeError` if `this` is not a promise | Spec p.779–780 | — |
| `[Symbol.toStringTag]` | property | `"Promise"` | — | Spec p.780 | — |

Instances have `[[PromiseState]]`, `[[PromiseResult]]`, reaction lists and `[[PromiseIsHandled]]` (Spec p.780). The prototype is not an instance, so `then` called on it fails through `IsPromise` (Spec p.778–779). `NewPromiseCapability(C)` throws `TypeError` if `C` is not a constructor or if `resolve` or `reject` do not end up callable (Spec p.767).

---

## 18. Generators, async generators and async functions

### Generators and GeneratorFunction

| Member | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|
| `%GeneratorFunction%` | Intrinsic constructor with no global name; `GeneratorFunction(...params, body)` delegates to `CreateDynamicFunction` with the generator kind; calling it as a function is equivalent to `new`; `length` 1, `name` `"GeneratorFunction"`, `[[Prototype]]` `%Function%` | `SyntaxError` as in Function | Spec p.781–782 | analogous to `eval` regarding risks [extrapolation] |
| Typical generator function | Not a constructor; its `prototype` (writable, not enumerable, not configurable) has no `constructor`; chain: instance, `g.prototype`, `%GeneratorPrototype%` (`next`, `return`, `throw`, tag `"Generator"`), `%Iterator.prototype%`, `Object.prototype` | — | Spec p.781–783 | — |
| `next(value)` | Resumes passing `value` as the result of the pending `yield` | `TypeError` if `this` is not a generator or if it is already running | Spec p.785, 787 | — |
| `return(value)` | Resumes with a return completion, running pending `finally` blocks; a generator not started or already completed becomes completed and returns `{value, done: true}` | likewise | Spec p.786–788 | — |
| `throw(exception)` | Resumes throwing at the point of the `yield`; a completed generator rethrows; one not started becomes completed | likewise | Spec p.786–788 | — |

States: SUSPENDED-START, SUSPENDED-YIELD, EXECUTING, COMPLETED (Spec p.786). Completed generator: `next()` gives `{value: undefined, done: true}` (Spec p.787). End of the body: `return x` gives `{value: x, done: true}`; an exception propagates and leaves the generator completed forever (Spec p.787). A generator does not restart [inference]. With `function* g(){ const x = yield 1; return x; }`, `it.next(); it.next(5)` gives `{value:5, done:true}` [inference].

### Async generators

| Member | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|
| `%AsyncGeneratorFunction%` | Same as the previous with the async generator kind; `name` `"AsyncGeneratorFunction"`; the instances' `prototype` without `constructor` | — | Spec p.783–785 | — |
| `next`, `return`, `throw` | Always return a Promise and never throw: an invalid `this` becomes a rejection with `TypeError`. Requests enter a queue (`[[AsyncGeneratorQueue]]`) served in order; states include DRAINING-QUEUE. `yield` completes the request with `done: false` and, if there are requests in the queue, continues without suspending; resuming with `return` at a `yield` awaits the value and, if it rejects, the rejection is thrown inside the generator | `TypeError` (as a rejection) | Spec p.789–795 | — |
| `[Symbol.toStringTag]` | `"AsyncGenerator"` | — | Spec p.791 | — |

### Async functions

`%AsyncFunction%`: a constructor with the async kind, `name` `"AsyncFunction"`, `length` 1; instances are not constructors (no `[[Construct]]`) and have no `prototype`, so `new asyncFn()` throws `TypeError` [inference] (Spec p.795–797). The async function always returns a promise: normal end resolves with `undefined`, `return v` resolves with `v` (a returned promise is flattened by the `resolve` rule), an exception rejects (Spec p.797–798). `Await(value)` applies `PromiseResolve(%Promise%, value)` and resumes with the value, or throws the reason at the point of the `await`; if `PromiseResolve` throws (a `constructor` getter), the exception occurs at the `await` (Spec p.798). The synchronous part runs up to the first `await` [inference].

---

## 19. Reflect

### Reflect

`Reflect` is an ordinary object (`[[Prototype]]` `Object.prototype`), with neither `[[Construct]]` nor `[[Call]]` (Spec p.799); `Reflect[Symbol.toStringTag]` is `"Reflect"` (Spec p.801). It mirrors the internal object operations; when the target must be an object and is not, it throws `TypeError` (Spec p.799–801). Keys go through `ToPropertyKey` (Spec p.799). Unlike `Object.defineProperty`, the versions that return a boolean do not throw on a definition failure [inference]; typical use: forwarding the operation to the target inside Proxy traps [inference].

| Member | Signature | What it does | Error thrown | Page |
|---|---|---|---|---|
| `Reflect.apply` | `(target, thisArgument, argumentsList)` | Calls `target` with `this` and a list taken from an array-like (`PrepareForTailCall`) | `TypeError` if not callable or the list is invalid | Spec p.799 |
| `Reflect.construct` | `(target, argumentsList[, newTarget])` | Constructs like `new`, with an optional `newTarget` | `TypeError` if `target` or `newTarget` are not constructors | Spec p.799 |
| `Reflect.defineProperty` | `(target, key, attributes)` | Defines a property; returns a boolean | `TypeError` if the target is not an object | Spec p.799 |
| `Reflect.deleteProperty` | `(target, key)` | Removes; returns a boolean | likewise | Spec p.799 |
| `Reflect.get` | `(target, key[, receiver])` | Reads; `receiver` defaults to `target` (affects the `this` of getters) | likewise | Spec p.799–800 |
| `Reflect.getOwnPropertyDescriptor` | `(target, key)` | Descriptor or `undefined` | likewise | Spec p.800 |
| `Reflect.getPrototypeOf` | `(target)` | Returns the prototype | likewise | Spec p.800 |
| `Reflect.has` | `(target, key)` | Equivalent to `key in target` | likewise | Spec p.800 |
| `Reflect.isExtensible` | `(target)` | Boolean | likewise | Spec p.800 |
| `Reflect.ownKeys` | `(target)` | Array with all own keys (strings and symbols) | likewise | Spec p.800 |
| `Reflect.preventExtensions` | `(target)` | Makes it non-extensible; boolean | likewise | Spec p.800 |
| `Reflect.set` | `(target, key, V[, receiver])` | Assigns; `receiver` defaults to `target`; boolean | likewise | Spec p.800–801 |
| `Reflect.setPrototypeOf` | `(target, proto)` | Sets the prototype; boolean | `TypeError` if the target is not an object or `proto` is neither an object nor `null` | Spec p.801 |

---

## 20. Proxy

### Proxy

| Member | Signature | What it does / edge cases | Error thrown | Page |
|---|---|---|---|---|
| `Proxy` | `new Proxy(target, handler)` | Delegates to `ProxyCreate`; the constructor's `[[Prototype]]` is `Function.prototype`; it has no `prototype` property, because proxies have no `[[Prototype]]` to initialize | `TypeError` without `new` | Spec p.801 |
| `Proxy.revocable` | `(target, handler)` | Returns `{ proxy, revoke }`; `revoke()` clears `[[ProxyTarget]]` and `[[ProxyHandler]]` (they become `null`); later calls do nothing. Operations on a revoked proxy fail [inference]; the traps and invariants are outside the material covered here (10.5) | — | Spec p.801–802 |

---

## 21. Module Namespace

### Module Namespace

An exotic object that gives access, through properties, to the exported bindings of a module; there is no constructor function; it is created for each module imported by an `ImportDeclaration` with `NameSpaceImport` (`import * as ns`). Besides the rules of 10.4.6, it has the own property `[Symbol.toStringTag]` with value `"Module"`, not writable, not enumerable and not configurable; thus `Object.prototype.toString.call(ns)` gives `[object Module]` [inference] (Spec p.802). Effect of `export default` with an anonymous function or class: it receives the name `"default"` and the value is bound to the internal name `*default*` (Spec p.445) [VERSION-DEPENDENT: modules]. The other rules are outside this file.

### Memory model (summary of the role)

Specifies the possible orders of shared data block events generated by TypedArrays over `SharedArrayBuffer` and by `Atomics`. Without data races, behavior is sequentially consistent; with races, accesses may look inconsistent, without undefined behavior; the model is axiomatic (constraints over event graphs), not algorithmic (Spec p.802). Atomic accesses are SEQ-CST with a total order; ordinary accesses are UNORDERED and may tear values (`[[NoTear]]`); there are no intermediate orders of the release-acquire kind (Spec p.803–804). Synchronize events and host events (sending a `SharedArrayBuffer` between agents, for example) are [HOST] (Spec p.804). The relations `is-agent-order-before`, `reads-bytes-from`, `host-synchronizes-with` and `synchronizes-with` are in Spec p.806–807; `happens-before` and the validity rules are outside what the sources read cover.

---

## 22. Divergences and observations between sources

- In this range no divergence between Spec, EJ1 and EJpt was recorded: the notes used for this file come only from the Spec, except the mention of EJpt p.198 about `getYear`. Precedence rule: the Spec is the norm; EJpt is the modern explanation; EJ1 is dated.
- Within the Spec itself: `Function.prototype.apply`/`call` pass `thisArg` unmodified, unlike Edition 3 (which replaced `undefined`/`null` with the global); non-strict functions still do the replacement on entry (Spec p.473–474) [DATED regarding Edition 3].
- `Date` is the only built-in that treats the `ToPrimitive` hint `"default"` as `"string"` (Spec p.537).
- The same text may give different results as a literal and as JSON (property definition differs in `ParseJSON`, for example a duplicate `__proto__`) (Spec p.735).

---

## 23. Truncated or noisy passages in the sources (do not reproduce)

- Section titles appear at the end of each page of the extracted text and method headers are separated from the body; the assignment of steps to methods was done by the order of the titles (Spec p.445–496, 715–763, 764–807). Do not reproduce method names deduced only by position without checking.
- Spec p.457–460 carry almost only cross-references ("See X.Y.Z") with no normative content of their own; the correspondence between title and cross-reference is not guaranteed line by line.
- Spec p.445 opens in the middle of `export default AssignmentExpression ;`; p.715 opens in the middle of a note ("NOTE 2" appears without "NOTE 1"); p.496 ends at `ThisBigIntValue`; the memory model material ends cut off at 29.6.5 (Spec p.807).
- Formulas flattened in the extraction (`253 - 1` for 2^53 - 1; `2bits - 1` for 2^(bits-1); `10f` for 10^f): use the correct mathematical reading (Spec p.489, 491, 495).
- Typographical error in the source: "the the" in `JSON.rawJSON` (Spec p.739). The marker "NORMATIVE OPTIONAL" before `WeakRef.prototype.constructor` on p.746 is not explained (do not reproduce as a rule).
- Figure 6 (GeneratorFunction relations) came without arrows; the relations were reconstructed from the text (Spec p.781).

---

## 24. Gaps

- Version of introduction of each feature: the Spec (and the notes) do not say in which edition were introduced, among others, `Object.groupBy`, `Object.hasOwn`, `Math.sumPrecise`, `Math.f16round`, `Float16Array`/`getFloat16`, `Iterator.concat`, Iterator helpers, `Promise.try`, `Promise.withResolvers`, `Error.isError`, `JSON.rawJSON`, the reviver's `context.source` and `Atomics.waitAsync`. Do not state "since ES20XX".
- Outside this file: String and its methods, RegExp, Array, Map/Set/WeakMap/WeakSet, TypedArrays and ArrayBuffer (the text only mentions the globals), `Intl` (ECMA-402, only mentioned), the full Annex B (here only `__proto__`, the legacy accessors and `getYear`/`setYear`/`toGMTString`) and Annexes E/F.
- Algorithm details omitted: `CreateJSONParseRecord`, the full `DoWait`, `AsyncGeneratorStart/Resume/DrainQueue`, `ToBigInt`, `Number::exponentiate`, `SameValue`, `ToObject` (errors inferred), Proxy traps (10.5) and `OrdinaryHasInstance`.
- `ToIndex`: the error type for an invalid index in DataView/Atomics is not detailed in the notes (`RangeError` is [inference]).
- Usage examples (marked [inference] or "own") do not come from the books; EJ1 and EJpt were not used in this range, except EJpt p.198.
