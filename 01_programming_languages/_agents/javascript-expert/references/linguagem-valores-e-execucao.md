# Language: values, types, conversions and execution model (Spec)

This file is a concept-organized lookup of what the **Spec** (ECMA-262, 17th edition, ECMAScript 2026, normative) says about types and values, conversions, comparison, operations on objects, scope, Environment Records, realms, execution contexts, jobs, agents, WeakRef and ordinary/exotic objects. Step-by-step algorithms are omitted; what remains are the observable effect, the errors thrown and the edge cases. Citations in the format `(Spec p.N)` use the PDF page, not the printed one. The Spec does not state in which edition each feature entered (except for occasional notes); where this matters, the text says "version not stated in the sources". Labels: **[HOST]** (defined by the environment), **[DATED]** (legacy), **[VERSION-DEPENDENT]**, **[inference]** and **[extrapolation]**. Use Grep on the `##`/`###` headings to jump to a topic.

## Contents

1. Overview and conformance
2. Spec conventions that affect reading
3. Language types
4. Specification types
5. Type conversions
6. Tests and comparison
7. Operations on objects
8. Operations on iterators
9. Scope and declarations (var, let, const, hoisting, TDZ, labels, function names)
10. Environment Records
11. Realms, execution contexts, jobs and agents
12. WeakRef and FinalizationRegistry
13. Ordinary objects
14. Functions (ECMAScript and built-in)
15. Exotic objects
16. Proxy (start of 10.5)
17. Points of attention across excerpts
18. Do not reproduce
19. Gaps

---

## 1. Overview and conformance

### 1.1 What the Spec defines
- Defines the general-purpose language ECMAScript 2026 (Spec p.25). The language is object-oriented and serves to compute and manipulate objects **within a host environment**; it does not provide for external data input or output, which come from objects supplied by the environment (Spec p.26). **[HOST]**
- It was designed for scripts on the web and today serves several hosts; the core is specified separately from any host (Spec p.27). Browser and web server are examples of hosts with their own objects (windows, events, requests, files) (Spec p.27). **[HOST]**
- Organization: clauses 6–10 form the execution environment, 11–17 the language itself, 18–28 the standard library, 29 the memory consistency model (Spec p.35).

### 1.2 Conformance
- A conforming implementation must support all the types, values, objects, properties, functions and the syntax/semantics described; the source text follows the latest version of Unicode/ISO 10646 (Spec p.25).
- If it offers an internationalization API, it must follow ECMA-402 compatible with this edition; the presence of `Intl` is not required by this excerpt (Spec p.25). **[HOST]**
- Extensions are allowed (types, values, objects, properties, functions, syntax, including use of future reserved words), except those listed as "Forbidden Extension" and the redefinition of facilities that are not implementation-defined, implementation-approximated or host-defined (Spec p.25). Consequence **[inference]**: an engine may have extra properties; depending on them is not portable.
- **Normative Optional**: may or may not be implemented; browsers generally implement everything (refers to Annex B); if part of the optional behavior is implemented, all of that of the containing clause must be (Spec p.25).
- **Legacy**: must be implemented unless it is also Normative Optional; the feature has undesirable characteristics, is not part of the core and must not be used in new code (Spec p.25). **[DATED]** as a category.

### 1.3 Strict mode (strict variant)
- The language defines a strict variant that excludes certain features, changes the detailed semantics of some and **specifies additional error conditions reported by exception** where normal mode does not consider them errors (Spec p.30).
- Selection happens per **source text unit** (11.2.2, outside the scope of this file); a program may mix strict and non-strict units, and the mode only applies to code defined within a strict unit. The implementation must support both variants and the mix (Spec p.30).
- Observable strict effects that appear in the sections below: assignment to an unresolvable name throws `ReferenceError` (section 4.2); `[[Set]]` returning `false` becomes `TypeError` (section 4.2); `this` is not converted to the global object (section 14.1); `arguments` is unmapped (section 15.4); modules are always strict (section 10.7).

### 1.4 Host/implementation terminology
| Term | Meaning | Page |
|---|---|---|
| implementation-defined | definition deferred without qualification; the Spec recommends no behavior | Spec p.27 |
| implementation-approximated | deferred, but with an ideal behavior recommended (example: `Math.exp`) | Spec p.27 |
| host-defined | deferred and listed in Annex D; may also be defined by non-hosts | Spec p.27 |
| host hook | abstract operation defined by an external source; must return a normal completion or throw | Spec p.27 |
| host environment | set of host-defined choices; typically provides I/O as host-defined properties of the global object | Spec p.28 |

Example of an external host: the WHATWG HTML specification (Spec p.27). **[HOST]**

### 1.5 Object model (informal view)
- Object = collection of zero or more properties with attributes; properties hold primitives, objects or functions. **Function** is a callable object; a function bound to an object through a property is a **method** (Spec p.28).
- Primitives: Undefined, Null, Boolean, Number, BigInt, String, Symbol (Spec p.28).
- The language is not fundamentally class-based, despite the `class` syntax; constructors are functions with a `"prototype"` property used for inheritance and shared properties (Spec p.28). Syntactic class definitions exist from ECMAScript 2015 on (Spec p.29). **[VERSION-DEPENDENT]** (ES2015)
- Prototype chain: property reads use the first occurrence of the name in the chain, starting with the object itself (Spec p.29). State, methods and structure are all inherited, unlike in class-based languages (Spec p.29). The constructor's own properties (for example `P1`, `P2` in Figure 1) are not seen by instances, and there is no implicit link between the constructor and its prototype (Spec p.29).
- Calling a constructor without `new` has an effect that depends on the constructor: `Date()` returns text, not an object (Spec p.29).
- Glossary 4.4 (summary): an ordinary object has the default behavior of the essential internal methods; an exotic object lacks one or more of them (Spec p.31); a method is a function in a property and receives the object as `this` when called as a method (Spec p.34); an "own property" is on the object, an "inherited" one comes from the prototype (Spec p.35).

---

## 2. Spec conventions that affect reading

- **Grammars**: lexical and RegExp grammars use `::`, the numeric string grammar uses `:::`, the syntactic grammar uses `:` (Spec p.36–37). Parsing is a single application of the syntactic grammar over the tokens; leftover tokens are a syntax error (Spec p.36). Each `eval` call with the same string produces an independent parse (Spec p.37).
- **`[no LineTerminator here]`** marks restricted productions; the Spec's example is `throw` followed by an expression (Spec p.42). Outside them, line breaks between tokens do not affect acceptance (Spec p.43). A `/*…*/` comment containing a line break is replaced by **one** line terminator in the stream, which can trigger automatic semicolon insertion (Spec p.36). **[inference]** as to the practical effect.
- **Cover grammars**: object/array literals and destructuring patterns share generalized productions; if reparsing as a pattern does not yield a single instance, there is an early Syntax Error (Spec p.37).
- **Early errors**: the implementation validates all rules before the **first evaluation** of a Script or Module; a violation makes the code invalid and unevaluable (Spec p.47). **[inference]**: an early error prevents any part of the script from running.
- **`?` and `!`** in algorithms: `?` propagates an abrupt completion, `!` asserts a normal completion (Spec p.45–46). "Throw a TypeError" is equivalent to returning a throw completion with a new `TypeError` (Spec p.45).
- **Mathematics**: Numbers (IEEE 754-2019 binary64) and BigInts are distinct from mathematical values; `𝔽(x)` converts to Number, `ℤ(x)` to BigInt, `ℝ(x)` to a mathematical value; mixed-type operands are not defined (Spec p.47–48). `x modulo y` has the sign of `y` (Spec p.48). In intervals, `-0` is less than `+0` and NaN is never included (Spec p.48).
- **Identity**: values without identity (undefined, null, Booleans, Strings, Numbers, BigInts) are equal if their characteristics are equal; values with identity (objects and Symbols not created by `Symbol.for`) are only equal to themselves. Symbols from `Symbol.for` have specification identity but not language identity (Spec p.49).
- Value notation: language values in bold, code in monospace (Spec p.49).

---

## 3. Language types

Language types (manipulated by the programmer): **Undefined, Null, Boolean, String, Symbol, Number, BigInt, Object** (Spec p.49). The remaining Spec values are specification types (section 4).

### 3.1 Undefined, Null, Boolean
- Undefined has the single value `undefined`; every variable with no assigned value holds it (Spec p.50). Null has the single value `null` (Spec p.50). Boolean has `true` and `false` (Spec p.50).
- Glossary: `null` represents the intentional absence of an object value (Spec p.32). A Boolean object is an instance of `Boolean` created with `new`, with an internal slot and coercible to boolean (Spec p.32).

### 3.2 String
- Ordered sequence of zero or more 16-bit unsigned integers, of maximum length 2^53 − 1; normally each element is a UTF-16 code unit (Spec p.50). `length` counts 16-bit units, not characters (Spec p.50).
- The language **does not restrict** values or relations between units; operations that interpret code points must deal with ill-formed subsequences (Spec p.50). A lone surrogate is a valid string.
- Surrogates: 0xD800–0xDBFF (leading) and 0xDC00–0xDFFF (trailing). A leading followed by a trailing forms a pair and becomes the code point `(c1 − 0xD800) × 0x400 + (c2 − 0xDC00) + 0x10000`; an unpaired surrogate becomes the code point of the same value (Spec p.50).
- **Normalization**: only `String.prototype.normalize` and `String.prototype.localeCompare` normalize; no other operation normalizes implicitly. Results do not depend on locale unless indicated (Spec p.50). Pitfall **[inference]**: visually identical strings may differ.
- `StringIndexOf`: the empty string is found at every position, including after the last unit, provided `fromIndex ≤ length` (Spec p.51).
- Relational comparison of strings is by UTF-16 code unit, not by code point, and without normalization (see section 6.4).
- ASCII word characters for the Spec: `A–Z`, `a–z`, `0–9`, `_` (Spec p.51).
- A String object has an internal slot with the value and `String` as a function converts to a String value (Spec p.33).

### 3.3 Symbol
- **Non-String** values that can be property keys; each Symbol is unique and immutable, with a `[[Description]]` slot (String or `undefined`) (Spec p.51).
- **Well-known symbols** are built-in values referenced by algorithms, generally keys that work as extension points; **shared by all realms** (Spec p.52). The current notation is `%Symbol.name%` (earlier editions: `@@name`) (Spec p.52). The `[[Description]]` of each is `"Symbol.<name>"` (Spec p.52–53).

| Symbol | Role | Who consults it | Page |
|---|---|---|---|
| `Symbol.asyncIterator` | method that returns the default async iterator | `for-await-of` | Spec p.52 |
| `Symbol.hasInstance` | decides whether a constructor recognizes an object as an instance | `instanceof` | Spec p.52 |
| `Symbol.isConcatSpreadable` | boolean; if true, the object is flattened | `Array.prototype.concat` | Spec p.52 |
| `Symbol.iterator` | method that returns the default iterator | `for-of` | Spec p.52 |
| `Symbol.match` | matches the regex against a string | `String.prototype.match` | Spec p.52 |
| `Symbol.matchAll` | returns an iterator of the matches | `String.prototype.matchAll` | Spec p.52 |
| `Symbol.replace` | replaces matched portions | `String.prototype.replace` | Spec p.52 |
| `Symbol.search` | returns the index of the match | `String.prototype.search` | Spec p.52 |
| `Symbol.species` | constructor function used to create derived objects | derived-object constructors | Spec p.53 |
| `Symbol.split` | splits the string at the matches | `String.prototype.split` | Spec p.53 |
| `Symbol.toPrimitive` | converts the object to a primitive | `ToPrimitive` | Spec p.53 |
| `Symbol.toStringTag` | String used in the default description of the object | `Object.prototype.toString` | Spec p.53 |
| `Symbol.unscopables` | names (own and inherited) excluded from `with` bindings | `with` environment | Spec p.53 |

`Symbol.unscopables` only makes sense for `with`, which is legacy **[DATED]** (the legacy marking comes from Annex B, outside the scope of these pages **[extrapolation]**).

### 3.4 Number
- Built-in numeric types: Number and BigInt (Spec p.53). **There is no implicit conversion between them**: you must call `Number` and `BigInt`; the Spec explains that the old implicit conversions would be lossy and that this was avoided for BigInt to minimize programmer error (Spec p.55).
- Representation: exactly 18,437,736,874,454,810,627 values (2^64 − 2^53 + 3), those of IEEE 754-2019 binary64, **except** that the 2^53 − 2 distinct NaNs form **a single** NaN for ECMAScript code. There are `+Infinity`, `-Infinity`, and **two distinct zeros**, `+0` and `-0` (Spec p.55).
- Finite non-zero values: normalized `s × m × 2^e` (m in [2^52, 2^53), e in [−1074, 971]) and denormalized (e = −1074). Every integer of magnitude ≤ 2^53 is representable (Spec p.55–56).
- The Number value of a real `x`: the closest one; a tie goes to the even significand (`roundTiesToEven`); overflow becomes ±∞; a chosen zero becomes `-0` only if x < 0 (Spec p.56).
- Operations that only handle integer ranges (32 bits, 16 bits) accept any Number and convert it beforehand (Spec p.56).

**Edge cases by operator (Number)**

| Operation | Edge result | Page |
|---|---|---|
| `-x` | NaN stays NaN | Spec p.56 |
| `~x` | `ToInt32` and bit complement | Spec p.56 |
| `**` | exponent NaN → NaN; exponent ±0 → 1 (including base NaN); base NaN with another exponent → NaN; base ±1 with exponent ±∞ → NaN; base 1 with exponent NaN → NaN; negative base and non-integer exponent → NaN | Spec p.57 |
| `*` | ∞ × ±0 → NaN; multiplication is not necessarily associative | Spec p.57–58 |
| `/` | ∞/∞ → NaN; ±0/±0 → NaN; x/+0 → +∞ if x > 0, otherwise −∞; finite/∞ → ±0 | Spec p.58 |
| `%` | NaN if n is ±∞ or d is ±0; d = ±∞ returns n; n = ±0 returns n; remainder of truncated division; **remainder 0 with negative n gives `-0`** | Spec p.58–59 |
| `+` | +∞ + −∞ → NaN; `-0 + -0` → `-0`; not necessarily associative | Spec p.59 |
| `-` | equivalent to `x + (−y)` | Spec p.59 |
| `<<` `>>` | `ToInt32` on the left, `ToUint32` on the right; count modulo 32 | Spec p.59–60 |
| `>>>` | `ToUint32` on both; count modulo 32; unsigned 32-bit result | Spec p.60 |
| `<` (IsLessThan) | NaN on either side → `undefined`; +0 vs −0 → false | Spec p.60 |
| equality (Number::equal) | NaN → false; **+0 and −0 are equal** | Spec p.60 |
| SameValue | NaN = NaN; **+0 ≠ −0** | Spec p.61 |
| SameValueZero | NaN = NaN; +0 = −0 | Spec p.61 |
| `& ^ \|` | `ToInt32` on both, 32-bit operation, back to Number | Spec p.61–62 |

The reading `NaN ** 0 === 1` follows from the order of the steps (exponent 0 is checked before base NaN) (Spec p.57). The Spec's note states that the case `1 ** Infinity` (NaN) differs from IEEE 754-2019 for historical compatibility (Spec p.57).

`%` accepts floating-point operands and is not the IEEE 754 "remainder"; it is analogous to Java's integer remainder and C's `fmod` (Spec p.59).

**Number to string (radix)**: radix from 2 to 36; NaN → `"NaN"`; ±0 → `"0"`; +∞ → `"Infinity"`; negative gets `"-"` (Spec p.62). In base 10, the smallest number of digits that identifies the value; positional notation if the decimal exponent `n` is between −5 and 21, otherwise scientific with `e+`/`e-` (for example `1.2e+3`) (Spec p.62). In other bases it is always positional (Spec p.62). For any Number except `-0`, `ToNumber(ToString(x))` returns `x` (guidance, Spec p.63).

### 3.5 BigInt
- Integer of any size; in bitwise operations it acts as a two's-complement bit string with infinite 1 bits on the left for negatives (Spec p.63).

| Operation | Rule and errors | Page |
|---|---|---|
| `-x`, `~x` | `~x` = −x − 1 | Spec p.63 |
| `**` | negative exponent throws `RangeError`; `0n ** 0n` = 1n | Spec p.64 |
| `*`, `+`, `-` | exact | Spec p.64 |
| `/` | divisor 0 throws `RangeError`; quotient truncated toward zero | Spec p.64 |
| `%` | divisor 0 throws `RangeError`; sign of the result is that of the dividend | Spec p.64 |
| `<<` | y < 0 is equivalent to `floor(x / 2^(−y))`; otherwise `x × 2^y` | Spec p.65 |
| `>>` | equivalent to `<<` with −y | Spec p.65 |
| `>>>` | **always throws `TypeError`** | Spec p.65 |
| `& \| ^` | bitwise in two's complement with sign extension | Spec p.65–67 |
| toString | radix 2–36, `"-"` for negatives | Spec p.67 |

Unlike Number, `x / 0n` does not give Infinity: it throws (Spec p.64). Mixing BigInt and Number in operators has no implicit conversion (Spec p.55); the type of the error in that case is not in this excerpt.

### 3.6 Object and properties
- An object is a collection of **data** properties (key → value + attributes) or **accessor** properties (key → get/set functions + attributes) (Spec p.67).
- Property key: String or Symbol, including the empty string. "Integer index" = a name whose `CanonicalNumericIndexString` is an integral Number in [+0, 2^53 − 1]; "array index" = an integer index in [+0, 2^32 − 2]. **`"-0"` is neither** (Spec p.67).
- `get` and `set` reach own and inherited properties; own keys are distinct from each other (Spec p.67). Every function is a member of the Object type (Spec p.67–68).

**Attributes (Table 3, Spec p.68)**

| Attribute | Property type | Default | Effect |
|---|---|---|---|
| `[[Value]]` | data | `undefined` | value read by `get` |
| `[[Writable]]` | data | `false` | if false, `[[Set]]` does not change `[[Value]]` |
| `[[Get]]` | accessor | `undefined` | if an object, must be a function; called with no arguments on each read |
| `[[Set]]` | accessor | `undefined` | called with one argument (the assigned value) |
| `[[Enumerable]]` | both | `false` | if true, `for-in` enumerates it |
| `[[Configurable]]` | both | `false` | if false: cannot be deleted, cannot switch data↔accessor, cannot change attributes except changing `[[Value]]` or setting `[[Writable]]` to `false` |

The Spec's defaults apply when the creation does not specify the attribute (Spec p.68). Applying this to `Object.defineProperty` is an **[extrapolation]**; the exact behavior of `DefineOwnProperty` is in section 13.

### 3.7 Internal methods and slots
- Internal methods define runtime behavior; they are not part of the language and are named between `[[ ]]`. An object that does not support an internal method that is used throws `TypeError` (Spec p.69). Internal slots are not properties, are not inherited, and in general cannot be added after creation (Spec p.69). Every object has `[[PrivateElements]]`, initially empty (Spec p.69).
- An object that imitates an exotic type without having the same collection of internal methods is **not recognized** as that type (Spec p.69).

**Essential internal methods (Table 4, Spec p.70)**

| Method | Return | Meaning |
|---|---|---|
| `[[GetPrototypeOf]]()` | Object or Null | who provides inherited properties |
| `[[SetPrototypeOf]](obj\|null)` | Boolean | associates another inheritance object; `false` if it could not |
| `[[IsExtensible]]()` | Boolean | whether properties can be added |
| `[[PreventExtensions]]()` | Boolean | prevents additions; `true` if it succeeded |
| `[[GetOwnProperty]](key)` | descriptor or undefined | own property |
| `[[DefineOwnProperty]](key, desc)` | Boolean | creates/changes; `false` if it could not |
| `[[HasProperty]](key)` | Boolean | own or inherited |
| `[[Get]](key, Receiver)` | any | `Receiver` is `this` if there is code |
| `[[Set]](key, value, Receiver)` | Boolean | `false` if it could not |
| `[[Delete]](key)` | Boolean | `true` if removed or nonexistent; `false` if it remains |
| `[[OwnPropertyKeys]]()` | List of keys | all own keys |

Functions add `[[Call]]` (callable objects) and `[[Construct]]` (constructors, invoked by `new` or `super`); every constructor is a function, but not every function is a constructor (Spec p.70–71).

**Internal method invariants (Spec p.71–73)**: they hold for ordinary and standard exotic objects; Proxy maintains them through runtime checks. Violating them may cause unpredictable behavior but must never compromise memory safety (Spec p.71). Summary:
- A "non-extensible" target is one already observed returning `false` from `[[IsExtensible]]` or `true` from `[[PreventExtensions]]` (Spec p.71). After that, `[[IsExtensible]]` is always `false` and `[[GetPrototypeOf]]` always returns the same value (Spec p.72). `[[SetPrototypeOf]]` on a non-extensible target returns `false` unless the value is the one already observed (Spec p.72).
- A property already observed as non-configurable: `[[Delete]]` returns `false`; `[[HasProperty]]` returns `true`; `[[DefineOwnProperty]]` returns `false` unless the data property is writable (it may become non-writable) or all attributes match (SameValue) (Spec p.72–73).
- A non-configurable, non-writable data property: `[[Get]]` always returns the same value and `[[Set]]` returns `false` unless the value is the same; a non-configurable accessor with `get` or `set` absent: `[[Get]]` returns `undefined` and `[[Set]]` returns `false` (Spec p.73).
- If the attributes or the existence of the property can change, it must be configurable; if `[[Writable]]` can go from false to true, the same applies (Spec p.72). A data property whose value varies requires `Writable` or `Configurable` to be true (Spec p.72).
- `[[OwnPropertyKeys]]` returns a list without duplicates, only valid keys, containing at least the observed non-configurable ones (and, on a non-extensible target, exactly the own ones) (Spec p.73).
- A circular prototype chain can cause infinite loops; the Spec cannot impose this as a general invariant (Spec p.72).

### 3.8 Well-known intrinsics
- Built-in objects cited by the algorithms, with identity **specific to each realm**; `%name%` is the intrinsic of the current realm (Spec p.74).
- With a global name (Table 6, summary): `Array`, `ArrayBuffer`, `AggregateError`, `Atomics`, `BigInt`, `BigInt64Array`, `BigUint64Array`, `Boolean`, `DataView`, `Date`, `decodeURI`, `decodeURIComponent`, `encodeURI`, `encodeURIComponent` (Spec p.74); `Error`, `eval`, `EvalError`, `FinalizationRegistry`, `Float16Array`, `Float32Array`, `Float64Array`, `Function`, `Int8Array`, `Int16Array`, `Int32Array`, `isFinite`, `isNaN`, `Iterator`, `JSON`, `Map`, `Math`, `Number`, `Object`, `parseFloat`, `parseInt`, `Promise`, `Proxy`, `RangeError` (Spec p.75); `ReferenceError`, `Reflect`, `RegExp`, `Set`, `SharedArrayBuffer`, `String`, `Symbol`, `SyntaxError`, `TypeError`, `Uint8Array`, `Uint8ClampedArray`, `Uint16Array`, `Uint32Array`, `URIError`, `WeakMap`, `WeakRef`, `WeakSet` (Spec p.76). Version in which `Float16Array` and `Iterator` entered: version not stated in the sources.
- Without a global name: `%ArrayIteratorPrototype%`, `%AsyncFromSyncIteratorPrototype%`, `%AsyncIteratorPrototype%`, `%ForInIteratorPrototype%`, `%MapIteratorPrototype%`, `%SetIteratorPrototype%`, `%RegExpStringIteratorPrototype%`, `%StringIteratorPrototype%`, `%AsyncFunction%`, `%AsyncGeneratorFunction%`, `%AsyncGeneratorPrototype%`, `%GeneratorFunction%`, `%GeneratorPrototype%` (Spec p.74–75); `%ThrowTypeError%` (function that throws `TypeError`) and `%TypedArray%` (superclass of the Typed Arrays) (Spec p.76).
- Each realm has its own: objects from different realms have different identities, while well-known symbols are shared (Spec p.74, p.52). The practical effect on `instanceof` across realms is an **[extrapolation]**.

---

## 4. Specification types

Meta-values used only inside the algorithms: Reference Record, List, Completion Record, Property Descriptor, Environment Record, Abstract Closure, Data Block. They may be intermediate results, but they never end up in object properties or JS variables (Spec p.77).

### 4.1 Completion Record
- Models return and control flow. Fields: `[[Type]]` (NORMAL, BREAK, CONTINUE, RETURN, THROW), `[[Value]]`, `[[Target]]` (label or EMPTY) (Spec p.78). "Abrupt completion" = everything except NORMAL (Spec p.79).
- Callable functions defined in the Spec only return normal or throw; the same applies to callable objects defined by the implementation (Spec p.79). Internal methods never return break/continue/return (Spec p.71).
- `UpdateEmpty` fills `[[Value]]` only if it is EMPTY (Spec p.79).

### 4.2 Reference Record, GetValue and PutValue
- Describes operators such as `delete`, `typeof`, assignment and `super`. Fields: `[[Base]]` (value, Environment Record or UNRESOLVABLE), `[[ReferencedName]]`, `[[Strict]]`, `[[ThisValue]]` (non-empty indicates a `super` reference) (Spec p.79–80).
- **GetValue**: unresolvable reference → `ReferenceError`; property reference → `ToObject` on the base (so `undefined`/`null` as base gives `TypeError`), `ToPropertyKey` on the name, then `[[Get]]`; environment reference → `GetBindingValue` (Spec p.81).
- **PutValue**: unresolvable in strict → `ReferenceError`; in sloppy creates a property on the global object; property reference → `ToObject` on the base and `[[Set]]`, and if this returns `false` in strict code → `TypeError`; environment → `SetMutableBinding` (Spec p.81).
- Derived example: assigning to a never-declared name throws `ReferenceError` in strict and creates a global in sloppy (Spec p.81).
- References to private members always have `[[Strict]]: true` (Spec p.82).

### 4.3 Property Descriptor
- Record whose fields are attributes. **Data** (has `[[Value]]` or `[[Writable]]`), **accessor** (has `[[Get]]` or `[[Set]]`), **generic** (neither); never data and accessor at the same time. "Fully populated" = accessor or data with all fields (Spec p.82).
- `FromPropertyDescriptor` creates a plain object with only the fields present (`value`, `writable`, `get`, `set`, `enumerable`, `configurable`) (Spec p.83).
- `ToPropertyDescriptor` (what `Object.defineProperty` expects as the 3rd argument **[inference]**): non-object argument → `TypeError`; queries each attribute with `HasProperty` (includes **inherited** ones) and reads it with `Get`, in the order enumerable, configurable, value, writable, get, set; `get`/`set` that are neither callable nor `undefined` → `TypeError`; `get` or `set` together with `value` or `writable` → `TypeError`; booleans go through `ToBoolean` (Spec p.83–84).
- `CompletePropertyDescriptor` uses defaults: value `undefined`, writable/enumerable/configurable `false`, get/set `undefined` (Spec p.84).

### 4.4 Others
- **List**: ordered sequence, 0-based; notation `« 1, 2 »` (Spec p.77). The Spec's **Set** ≠ ECMAScript's `Set` (Spec p.78).
- **Abstract Closure**: algorithm plus captured values; only returns normal or throw (Spec p.84–85).
- **Data Block**: fixed-size sequence of bytes initialized with zeros; `CreateByteDataBlock` throws `RangeError` if the size exceeds 2^53 − 1 or cannot be allocated (Spec p.85). A Shared Data Block is accessible to several agents (Spec p.85).
- **PrivateElement** (kinds FIELD, METHOD, ACCESSOR): a private field ≈ non-configurable, non-enumerable, writable data property; a private method ≈ the same but non-writable; a private accessor ≈ non-configurable and non-enumerable (Spec p.86). **Private Name** is a globally unique value with a `[[Description]]` (Spec p.87).

---

## 5. Type conversions

Abstract operations are not part of the language; they exist to specify semantics (Spec p.88). They accept any language value. **BigInt has no implicit conversions** (Spec p.88).

### 5.1 ToPrimitive
- A non-object passes through. An object: looks up `@@toPrimitive` (`GetMethod`); if it exists, calls it with hint `"default"`, `"string"` or `"number"`; an object result → `TypeError`. Without that method, `OrdinaryToPrimitive` with hint NUMBER by default (Spec p.88).
- With no hint, it behaves like NUMBER; only `Date` and Symbol objects override this, and `Date` treats the absence of a hint as STRING (Spec p.88).
- `OrdinaryToPrimitive`: hint string tries `toString` and then `valueOf`; otherwise `valueOf` and then `toString`. Uses the first callable whose return is not an object; if none qualifies → `TypeError` (Spec p.88–89).

### 5.2 ToBoolean
Falsy: `false`, `undefined`, `null`, `+0`, `-0`, `NaN`, `0n` and the empty string; everything else is truthy, including objects (Spec p.89). **[HOST]** in browsers, objects with an `[[IsHTMLDDA]]` slot are also falsy (step "normative optional") (Spec p.89).

### 5.3 ToNumber, ToNumeric and StringToNumber
- `ToNumeric`: `ToPrimitive(NUMBER)`; BigInt is returned; otherwise `ToNumber` (Spec p.89).
- `ToNumber` by type:

| Input | Result | Page |
|---|---|---|
| Number | itself | Spec p.89 |
| Symbol, BigInt | `TypeError` | Spec p.89 |
| `undefined` | NaN | Spec p.89 |
| `null`, `false` | +0 | Spec p.89 |
| `true` | 1 | Spec p.89 |
| String | `StringToNumber` | Spec p.89 |
| Object | `ToPrimitive(NUMBER)` and repeat | Spec p.89 |

- `StringToNumber` (StringNumericLiteral grammar): accepts spaces and line breaks at the ends; empty string or only spaces → `+0`; accepts leading zeros and the `+`/`-` sign on decimals; recognizes `Infinity` and `-Infinity`; accepts non-decimal literals (hex, etc.) **without a sign**; does **not** accept the `n` suffix or the `_` separator; invalid text → NaN (Spec p.89–90). `"-0"` gives `-0` (Spec p.91).
- With more than 20 significant digits, the digits beyond the 20th are zeroed or rounded up, the choice being up to the implementation (Spec p.91–92). **[IMPLEMENTATION-DEPENDENT]**

### 5.4 Conversions to integers

| Operation | Rule | Page |
|---|---|---|
| `ToIntegerOrInfinity` | `ToNumber`; NaN and ±0 → 0; infinities remain; otherwise truncates; never returns `-0` | Spec p.92 |
| `ToInt32` / `ToUint32` and 16/8 bits | `ToNumber`; non-finite or zero → +0; truncates and modulo 2^n; signed versions subtract 2^n if result ≥ 2^(n−1); `-0` becomes `+0` | Spec p.92–94 |
| `ToUint8Clamp` | NaN → 0; clamps to 0–255; rounds half to even (unlike `Math.round`); derived example: 1.5 → 2 and 2.5 → 2 **[inference]** | Spec p.94 |
| `ToLength` | `ToIntegerOrInfinity`; ≤ 0 → +0; cap 2^53 − 1 | Spec p.97 |
| `ToIndex` | `ToIntegerOrInfinity`; outside 0..2^53 − 1 → `RangeError` | Spec p.97 |
| `ToBigInt64` / `ToBigUint64` | `ToBigInt` and modulo 2^64 | Spec p.96 |

`ToInt32` and `ToUint32` are idempotent and `ToInt32(ToUint32(x)) = ToInt32(x)` (Spec p.92–93). They explain the conversion of operands of bitwise operators **[inference]**.

### 5.5 ToBigInt and StringToBigInt
- `ToBigInt`: `ToPrimitive(NUMBER)` and then: `undefined`, `null`, Number, Symbol → `TypeError`; Boolean → `1n`/`0n`; BigInt → itself; String → `StringToBigInt`, and if invalid → **`SyntaxError`** (Spec p.95).
- `StringToBigInt`: spaces at the ends, signed integer or non-decimal literal; empty or only spaces is 0; invalid → `undefined` internally (Spec p.95–96).

### 5.6 ToString, ToObject, ToPropertyKey
- `ToString`: String passes through; **Symbol → `TypeError`**; `undefined`, `null`, `true`, `false` become the corresponding text; Number and BigInt in base 10; object → `ToPrimitive(STRING)` and repeat (Spec p.96).
- `ToObject`: `undefined` and `null` → `TypeError`; Boolean, Number, String, Symbol and BigInt become wrapper objects with the corresponding data slot; an object passes through (Spec p.96–97).
- `ToPropertyKey`: `ToPrimitive(STRING)`; Symbol stays; the rest becomes String (Spec p.97).
- `CanonicalNumericIndexString`: `"-0"` → `-0`; returns the number if `ToString(ToNumber(s))` reproduces `s` exactly, otherwise `undefined` (Spec p.97). Its use in typed arrays is an **[extrapolation]** on this page; it is explicit in 10.4.5 (section 15.5).

### 5.7 Conversion summary table

| Value | ToBoolean | ToNumber | ToString |
|---|---|---|---|
| `undefined` | false | NaN | `"undefined"` |
| `null` | false | +0 | `"null"` |
| `true` / `false` | — | 1 / +0 | `"true"` / `"false"` |
| `0`, `-0`, `NaN` | false | itself | decimal form; `-0` → `"0"` (Spec p.62) |
| `0n` | false | `TypeError` | `"0"` |
| `""` | false | +0 | `""` |
| non-empty string | true | `StringToNumber` | itself |
| Symbol | true | `TypeError` | `TypeError` |
| object | true | via `ToPrimitive(NUMBER)` | via `ToPrimitive(STRING)` |

(Spec p.89, 96; Symbol being `true` follows from everything else is truthy, Spec p.89.)

---

## 6. Tests and comparison

### 6.1 Type predicates
- `RequireObjectCoercible`: `undefined`/`null` → `TypeError` (Spec p.98).
- `IsArray`: false for a non-object; true for an exotic Array; for Proxy it validates that it has not been revoked and consults the target (Spec p.98).
- `IsCallable` (has `[[Call]]`), `IsConstructor` (has `[[Construct]]`) (Spec p.98).
- `IsRegExp`: reads `@@match`; if it is not `undefined`, returns its `ToBoolean`; otherwise true if the object has `[[RegExpMatcher]]` (Spec p.99).
- `IsStringWellFormedUnicode`: false if there is a lone surrogate (Spec p.99).

### 6.2 SameValue, SameValueZero and `===`
| Operation | NaN vs NaN | +0 vs −0 | Page |
|---|---|---|---|
| IsStrictlyEqual (`===`) | different | equal | Spec p.102 |
| SameValue (`Object.is`) | equal | different | Spec p.99 |
| SameValueZero (Array/Map/Set) | equal | equal | Spec p.100 |

`IsStrictlyEqual`: different types → false; Number by `Number::equal`; the rest by `SameValueNonNumber` (strings by code units, BigInt and Boolean by value, the rest by identity) (Spec p.100, 102).

### 6.3 IsLooselyEqual (`==`)
- Same type → `===`; `null == undefined` is true; **[HOST]** in browsers, an `[[IsHTMLDDA]]` object is also `==` to `undefined`/`null` (Spec p.101–102).
- Number vs String → the string becomes a Number; BigInt vs String → the string becomes a BigInt (invalid → false); Boolean becomes Number before comparing; String/Number/BigInt/Symbol vs Object → `ToPrimitive` of the object; BigInt vs Number → exact mathematical comparison, false if not finite; any other case → false (Spec p.102).
- Pitfall **[inference]**: `null == 0` is false, because `null` is only `==` to `undefined` (Spec p.101–102).

### 6.4 IsLessThan (`<`, `>`, `<=`, `>=`)
- Returns true, false or `undefined` (some operand is NaN). `LeftFirst` preserves the left → right evaluation of the `ToPrimitive` effects (Spec p.100–101).
- Two strings: comparison by UTF-16 code unit, the shorter prefix comes first; **it is not by code point** and there is no normalization, so canonically equal strings in different forms may compare as different (Spec p.101).
- BigInt vs String: converts the string with `StringToBigInt`; if invalid → `undefined`. Others: `ToNumeric` on both; Number vs BigInt compares by mathematical value, handling NaN and infinities first (Spec p.101).

---

## 7. Operations on objects

- **MakeBasicObject** is the origin of every algorithmically created object: it adds an empty `[[PrivateElements]]`, uses the ordinary internal methods and sets `[[Extensible]]` = true. Exotic objects are assembled by overriding methods (Spec p.102–103).
- `Get(O, P)` calls `O.[[Get]](P, O)`; `GetV(V, P)` does `ToObject(V)`, hence `undefined`/`null` → `TypeError` and primitives work via a wrapper (Spec p.103).
- `Set(O, P, V, Throw)`: `[[Set]]` false with `Throw` true → `TypeError` (Spec p.103).
- `CreateDataProperty` defines data with writable, enumerable and configurable = true; returns `false` (without throwing) if the existing one is not configurable or the object is not extensible. `CreateDataPropertyOrThrow` throws `TypeError`. `DefinePropertyOrThrow` and `DeletePropertyOrThrow`: `false` → `TypeError` (Spec p.103–104).
- `GetMethod`: `undefined`/`null` → `undefined`; non-callable value → `TypeError` (Spec p.105).
- `Call(F, V, args)`: non-callable F → `TypeError`. `Construct(F, args, newTarget)`: `newTarget` defaults to F (Spec p.105–106).
- **Integrity levels** (Spec p.106): `SetIntegrityLevel` first calls `[[PreventExtensions]]` (false → returns false). SEALED makes each own property non-configurable; FROZEN also makes data properties non-writable (accessors only become non-configurable). `TestIntegrityLevel` returns false if the object is still extensible, without examining properties. Mapping to `Object.seal`/`Object.freeze` is an **[inference]** from the level names.
- **Array-like**: `LengthOfArrayLike` = `ToLength(Get(obj, "length"))`; any object for which this completes is array-like, without requiring indexed properties (Spec p.107). `CreateListFromArrayLike`: non-object → `TypeError` (Spec p.107).
- **Default `instanceof` (`OrdinaryHasInstance`)**: non-callable C → false; a bound function delegates to the target; non-object O → false; non-object `C.prototype` → `TypeError`; walks O's chain by SameValue (Spec p.108).
- **SpeciesConstructor**: reads `O.constructor` (`undefined` → default; non-object → `TypeError`) and `constructor[@@species]` (`undefined`/`null` → default; constructor → uses it; otherwise `TypeError`) (Spec p.108).
- **EnumerableOwnProperties**: considers only **String** keys with `enumerable` true; values read with `Get` at that moment (Spec p.108). Basis of `Object.keys/values/entries` **[inference]**.
- **CopyDataProperties**: a source of `undefined`/`null` is not an error (nothing to copy); copies own enumerable properties (strings and symbols) with `Get` (invokes getters), creating data properties on the destination (Spec p.109). Semantics of object spread/rest **[inference]**.
- **Private members** (Spec p.109–111): adding one that already exists → `TypeError`; `PrivateGet` with a missing member or an accessor without a getter → `TypeError`; `PrivateSet` on a missing member, on a method or on an accessor without a setter → `TypeError`. **[HOST]** `HostEnsureCanAddPrivateElement` may forbid private members on certain host exotic objects (Spec p.110). Private methods and accessors are shared between instances (Spec p.110). `InitializeInstanceElements` first adds private methods/accessors and then defines the fields, in order (Spec p.111).
- **GroupBy** (Spec p.112): `items` requires `RequireObjectCoercible`; non-callable callback → `TypeError`; key via `ToPropertyKey` (PROPERTY mode) or collection key (COLLECTION); an error in the callback closes the iterator; limit of 2^53 − 1 elements. Basis of `Object.groupBy`/`Map.groupBy` **[inference]**.
- `GetOptionsObject`: `undefined` → object with no prototype; object → itself; any other value → `TypeError` (Spec p.112).
- `SetterThatIgnoresPrototypeProperties`: non-object this → `TypeError`; this === home → `TypeError`; otherwise creates an own property with `CreateDataPropertyOrThrow` or does `Set` with Throw (Spec p.113).
- `GetFunctionRealm`: the function's realm; for bound, that of the target; for Proxy it validates not revoked and uses the target (Spec p.109).

---

## 8. Operations on iterators

- **Iterator Record**: `[[Iterator]]`, `[[NextMethod]]` (read **only once**), `[[Done]]` (Spec p.113).
- `GetIterator(obj, SYNC)` uses `@@iterator`; in ASYNC mode it tries `@@asyncIterator` and, if absent, falls back to `@@iterator` wrapping with `CreateAsyncFromSyncIterator`; no method → `TypeError` (Spec p.114). A non-object return from the method → `TypeError` (Spec p.114).
- `GetIteratorFlattenable`: non-object → `TypeError` (or accepts only String in ITERATE-STRING-PRIMITIVES mode); uses `@@iterator` if it exists, otherwise treats the object itself as an iterator (Spec p.114).
- `IteratorNext`: if `next` throws, marks Done and propagates; non-object result → Done and `TypeError` (Spec p.114–115). `IteratorComplete` = `ToBoolean(done)`; an error reading `done` or `value` marks Done (Spec p.115).
- **`IteratorClose`** (Spec p.116): looks up `return`; if absent, passes along the original completion; if it exists, calls it. Error priority: the **original throw wins** over the `return` error; otherwise the `return` error propagates; otherwise a `return` that returns a non-object → `TypeError`. This is what runs when exiting `for...of` early **[inference]**. `IteratorCloseAll` closes in reverse order; `AsyncIteratorClose` does `Await` on the result of `return` (Spec p.116–117).
- `CreateIteratorResultObject` creates an object with `value` and `done` (Spec p.117).

---


## 9. Scope and declarations (var, let, const, hoisting, TDZ, labels, function names)

The Spec handles this through static operations that extract from the grammar which names each construct declares and in what kind of scope (Spec p.118). Runtime behavior comes from the Environment Records (section 10).

### 9.1 Names introduced (BoundNames)
- A simple identifier → one name; destructuring patterns return the names of all elements, including `...rest`; empty `{}` and `[]` → none (Spec p.118–120). Derived example: `let [a, {b}] = x` introduces `a` and `b` **[inference]**.
- Formal parameters: union of the names of each one and of the rest (Spec p.120). Function, generator, async and `class` declarations → the identifier's name (Spec p.120–121).
- An anonymous declaration (only possible in `export default`) uses the synthetic name `"*default*"`, which is never accessible to ECMAScript code (Spec p.118, 120–121).
- `import` → names of the imported bindings; `import "mod"` → none; `export {…}` and `export … from` → none (Spec p.121–122).
- `IsConstantDeclaration` is true only for `const` (Spec p.123).

### 9.2 Lexical declarations
- In a block, `let`, `const`, `class` **and functions** are lexical; ordinary statements do not contribute (Spec p.124–125).
- `switch`: all `case`s and the `default` share **a single** block scope (Spec p.124). Consequence **[inference]**: a repeated `let` in two `case`s conflicts.
- A labeled function (`label: function f(){}`) counts as a lexical function declaration (Spec p.124–125, 127).
- **Script vs Module**: at the top of a **Script** functions are treated as `var`, not as lexical; at the top of a **Module** they are lexical; a Module's lexical names include all imports; `export var` is not among the lexical ones (Spec p.125–126).
- At the top of a function or script, the "TopLevel…" operations return the lexical declarations without the functions; hoistable functions enter as `var` (Spec p.135–137).

### 9.3 `var` declarations and hoisting
- `var` names are **hoisted** to the function/script scope, crossing blocks and statements (`if`, loops, `switch`, `try`, `with`, labels) (Spec p.128–130).
- `for (var …)` and `for (var x in/of …)` add the header names; `for (let …)` and `for (const …)` do **not** (lexical header) (Spec p.129).
- `catch (e) {…}`: the parameter does not count; only what is in the block (Spec p.130). Pitfall **[inference]**: `var` inside `if`/`for`/`try` does not create its own scope.
- Extension for `for-in` with `var` in Annex B.3.5 (legacy, web) (Spec p.129, 133, 138). **[DATED]**
- **Function hoisting**: `InstantiateFunctionObject` creates each function declaration (function, generator, async, async generator) at scope instantiation, with the current environment as the closure (Spec p.154). The exact moment is defined outside the excerpt; that the function exists before the statements is an **[inference]**. Duplicate declarations of the same function: the **last** one wins (Spec p.211).
- A `var` with the same name as a parameter starts with the **parameter's value**, not `undefined` (unless it is also the name of a declared function) (Spec p.213).
- **Functions in blocks (legacy web semantics)**: **[DATED] [HOST]** marked "NORMATIVE OPTIONAL"; in a browser (or a host with this semantics) and only in non-strict code, a `var` with the function's name is created (initial value `undefined`) when this would not cause an early error and the name is not a parameter; when the declaration in the block is evaluated, the value is copied to the function-level variable (Spec p.213).

### 9.4 let, const, class and TDZ
- `let`/`const`/`class` bindings are created **uninitialized** at function/block instantiation; they stay that way until the declaration is evaluated (Spec p.167, 213).
- Reading an uninitialized binding → `ReferenceError` (any mode) (Spec p.168). Writing to an uninitialized one → `ReferenceError` (Spec p.167). This is the *Temporal Dead Zone* **[inference]**.
- Immutable binding (`const`, imports): assignment throws `TypeError` if the code is strict or the binding is a "strict binding"; in sloppy with a non-strict binding, it fails silently (Spec p.167). `CreateImmutableBinding(N, true)` makes later assignment always throw (Spec p.164).
- `var` and parameters of non-strict functions are initialized by `PutValue` (hoisted, pre-initialized binding), not by `InitializeBinding`; therefore there is no TDZ for `var` (Spec p.154–156). A duplicate parameter name is handled this way (Spec p.156).
- In the global environment, `let`/`const`/`class` live in the declarative part and **shadow** same-named properties of the global object; global `var`/`function` become properties of the global object (Spec p.173–175). **[inference]** for the consequence.
- `HasRestrictedGlobalProperty(N)`: true if N is an own **non-configurable** property of the global object; it prevents a lexical declaration with that name (the Spec's example: `undefined`) (Spec p.176–177). `let undefined` at global level giving an error is an **[inference]**.
- `CanDeclareGlobalVar`: true if the own property already exists or if the global object is extensible (Spec p.177). `CanDeclareGlobalFunction`: true if it does not exist and it is extensible; or it exists and is configurable; or it is a data property that is `writable` and `enumerable` (Spec p.177). `CreateGlobalVarBinding` reuses an existing property without resetting it (Spec p.177). `CreateGlobalFunctionBinding` replaces the value (Spec p.178).

### 9.5 Binding initialization and destructuring
- `BindingInitialization`: with `environment` undefined it uses normal assignment (`var` and parameters of some non-strict functions) (Spec p.154).
- **Object** pattern: before destructuring it calls `RequireObjectCoercible`; `null`/`undefined` fail (the error class comes from the operation, whose text is not in the excerpt, so `TypeError` is an **[inference]**). An empty `{}` does nothing but still requires coercibility. `{...rest}` excludes the names already extracted (Spec p.155).
- **Array** pattern: obtains a sync iterator; if it has **not finished** at the end, it is **closed** with `IteratorClose` (calls `return`); if it finished, it is not (Spec p.155).
- Elisions consume a value and discard it; if the iterator is exhausted, the value is `undefined`; the default value only triggers for `undefined`, not for `null`; it is evaluated only when needed; `...x` collects the remainder into a new array (Spec p.156–157). Derived example: `const [a, , b = 5, ...r] = [1,2,undefined,4,5]` gives `a=1`, `b=5`, `r=[4,5]` **[inference]**.
- Inferred name (NamedEvaluation) applies to the initializer of a simple name, not to a nested pattern (Spec p.157).

### 9.6 Assignment targets (AssignmentTargetType)
- Classification `SIMPLE`, `WEB-COMPAT` or `INVALID` (Spec p.158).
- `SIMPLE`: identifier (except `eval` and `arguments` in strict, which are `INVALID`), `a.b`, `a[b]`, `a.#p`, `super.x`; parentheses delegate to the inside (Spec p.158–159).
- **`WEB-COMPAT` [HOST] [DATED]**: a function call as a target (`f() = 1`) is accepted if the host is a browser (or supports "Runtime Errors for Function Call Assignment Targets") and the code is not strict; otherwise `INVALID`. Marked "NORMATIVE OPTIONAL" (Spec p.159). In browser/sloppy this is not a parse error, it fails at runtime **[inference]**.
- `INVALID`: `this`, literals, array/object as a simple target, functions, classes, template, `super()`, `import()`, `new X`, `new.target`, `import.meta`, optional chain, unary/binary/logical/`??`/`?:` operators, assignment, arrow, `yield`, comma, `++x`/`x++` (Spec p.159–161). Derived examples: `x++ = 1` and `a?.b = 1` are invalid **[inference]**.

### 9.7 Inferred function name
- `HasName`: true for `function name(){}`, generators, async and `class Name {}`; false for anonymous ones and for **arrow** and async arrow (Spec p.146).
- `IsFunctionDefinition`: true for functions (named or not), classes and arrows; false for `this`, identifiers, literals, members, calls, operators (including `??`, `?:`, comma), assignments and `yield`; parentheses are transparent (Spec p.147–149). Hence `(function(){})` counts but `(0, function(){})` does not **[inference]**.
- `IsAnonymousFunctionDefinition` = is a function definition AND has no name; this is what triggers inference (Spec p.149). `IsIdentifierRef` distinguishes `x` from `(x)` (Spec p.149).
- `NamedEvaluation` evaluates the anonymous definition passing the name (key or Private Name); parentheses pass the name along; an anonymous `class` receives the name as an argument (Spec p.150).
- Class fields: if the field's expression is an anonymous definition, it receives the field's name (Spec p.207). `SetFunctionName`: a Symbol name becomes `"[description]"` (no description → empty); prefix `get`/`set`/`bound` becomes `prefix + " " + name`; `name` ends up `{writable: false, enumerable: false, configurable: true}` (Spec p.210).
- `PropName`: shorthand `{x}` → `"x"`; numeric literal → `ToString` of the number (`{1.0: a}` → `"1"`); computed and private → EMPTY (Spec p.161–162).
- Derived examples: `let f = () => {}` gives `f.name === "f"`; `let g = (0, () => {})` does not infer **[inference]**.

### 9.8 Labels (early errors)
- `ContainsDuplicateLabels`: true if the same label appears nested inside another of the same name; identical sibling labels are allowed; does not cross a function boundary (Spec p.137–140). Example: `a: { a: ; }` invalid; `a: ; a: ;` valid **[inference]**.
- `ContainsUndefinedBreakTarget`: `break label;` to a non-enclosing label → error; `break;` without a label is checked by another rule outside the excerpt (Spec p.140–143).
- `ContainsUndefinedContinueTarget`: `continue label;` is only valid if the label is **immediately** attached to an iteration statement; any other statement clears the pending labels (Spec p.143–146). Difference **[inference]**: `a: { while(1) { continue a; } }` is an error, `break a;` would be valid.
- These are parse errors, not runtime errors **[inference]**.

### 9.9 Contains (this, super, new.target in arrows)
- `Contains` does not look inside ordinary functions, generators, async; in classes it only looks at the `extends` and the computed names; static blocks return false (Spec p.151).
- **Arrows are transparent** only for `new.target`, `super` and `this` (Spec p.152). Hence arrows inherit `this`/`super`/`new.target` from the outer context **[inference]**.
- The name after the dot (`a.b`, `?.b`) does not count as a symbol (Spec p.152). `ComputedPropertyContains` looks only at the computed keys (Spec p.153).

---

## 10. Environment Records

Each time a block, function or `catch` is evaluated, **a new** Environment Record is created (Spec p.162). Every record has `[[OuterEnv]]` (chain = scope chain); programs do **not** access Environment Records directly (Spec p.162). Basis of closures **[inference]**.

### 10.1 Hierarchy
Abstract class with the concrete ones **Declarative**, **Object** and **Global**; **Function** and **Module** are subclasses of Declarative (Spec p.163).

| Type | Use | Page |
|---|---|---|
| Declarative | var/let/const, functions, `catch` | Spec p.163, 166 |
| Function | function invocation; `this` (except arrow), `super` state, `new.target` | Spec p.163, 171 |
| Module | module top level and imports; `[[OuterEnv]]` is the Global | Spec p.163, 178 |
| Object | properties of an object; used by `with` **[DATED]** and by the global part | Spec p.163, 169 |
| Global | outermost scope of Scripts, with no outer environment | Spec p.163, 173 |

### 10.2 Abstract methods
- `CreateMutableBinding(N, D)`: creates uninitialized; D indicates whether it can be deleted. `InitializeBinding(N, V)` gives the initial value (Spec p.164).
- `SetMutableBinding(N, V, S)`: S true and not changeable → `TypeError` (Spec p.165).
- `GetBindingValue(N, S)`: nonexistent binding with S → `ReferenceError`; **uninitialized → `ReferenceError` regardless of S** (Spec p.165).
- `DeleteBinding(N)`: removable → `true`; exists and not removable → `false`; does not exist → `true` (Spec p.165).
- `GetThisBinding` throws `ReferenceError` if `this` has not been initialized (Spec p.166).

### 10.3 Declarative
- Rare case: removed binding (by `delete` via `eval`) — in strict, assignment throws `ReferenceError`; in sloppy it recreates a deletable mutable binding (Spec p.167–168). **[DATED]** (sloppy `eval`)
- `DeleteBinding` only removes those marked deletable, which **[inference]** are those created by sloppy `eval` (Spec p.168). Ordinary Declarative records have neither `this` nor `super` (Spec p.168–169).

### 10.4 Object (with) [DATED]
- Binds names to the properties of a *binding object*, own and inherited, regardless of `[[Enumerable]]`; only String keys in IdentifierName form. There are no immutable bindings here (Spec p.169).
- `[[IsWithEnvironment]]` true gives the object as the implicit `this` in calls (Spec p.169). `HasBinding` in a `with` consults `Symbol.unscopables`: a truthy value blocks the name (Spec p.169). It serves to protect old code against new methods **[inference]**.
- `SetMutableBinding` with a missing property and S true → `ReferenceError`; `GetBindingValue` missing → `undefined` (S false) or `ReferenceError` (S true) (Spec p.170–171).

### 10.5 Function
- Fields: `[[ThisValue]]`, `[[ThisBindingStatus]]` (LEXICAL, INITIALIZED, UNINITIALIZED), `[[FunctionObject]]`, `[[NewTarget]]` (Spec p.172).
- In an arrow the binding is LEXICAL: `HasThisBinding` false and the lookup goes up (Spec p.172); `HasSuperBinding` false (Spec p.173).
- `BindThisValue` with `this` already initialized → `ReferenceError` (calling `super()` twice **[inference]**); `GetThisBinding` with UNINITIALIZED → `ReferenceError` (using `this` before `super()` **[inference]**) (Spec p.172).
- `HasSuperBinding` is true only with `[[HomeObject]]` defined (methods) (Spec p.173).

### 10.6 Global
- Composed of an Object Record (global object) plus a Declarative Record (Spec p.173–174). Object part: built-ins, global `function`/`generator`/`async` and `var`; declarative part: `let`/`const`/`class` (Spec p.173–174).
- Lookup: first the declarative part, then the object part (Spec p.174–175).
- `[[GlobalThisValue]]` can be any object chosen by the host (Spec p.174). **[HOST]**
- Global `CreateMutableBinding`/`CreateImmutableBinding` throw `TypeError` if a declarative binding with the name already exists (Spec p.174).
- `DeleteBinding`: declarative part first; otherwise own property of the global object via `[[Delete]]`; nonexistent → `true` (Spec p.175).
- Global `this`: `HasThisBinding` true and `GetThisBinding` returns `[[GlobalThisValue]]` (Spec p.176).

### 10.7 Module
- Has **immutable and indirect** import bindings (they point to a binding of another module); reading resolves the **current value** (live binding). Empty target environment or uninitialized binding → `ReferenceError` (Spec p.178).
- A module is always strict (S always true); `delete` on a module binding is an early error in strict (Spec p.178–179).
- `HasThisBinding` true and `GetThisBinding` returns **`undefined`**: `this` at module top level is `undefined` (Spec p.179).

### 10.8 Resolution and closures
- `GetIdentifierReference` walks `[[OuterEnv]]` with `HasBinding`; at the end of the chain the reference is UNRESOLVABLE (Spec p.179–180).
- `NewFunctionEnvironment` uses `F.[[Environment]]` as `[[OuterEnv]]` (the environment captured at creation = closure); `ThisBindingStatus` LEXICAL if arrow (Spec p.180). Lexical scope, not dynamic **[inference]**.

### 10.9 PrivateEnvironment
Tracks Private Names (`#x`) by class nesting; a new one on each class evaluation; `ResolvePrivateIdentifier` looks in the current class and goes up (Spec p.181). Two evaluations of the same class do not share `#x` **[inference]**.

---

## 11. Realms, execution contexts, jobs and agents

### 11.1 Realms
- All code is associated with a realm: intrinsics, global environment, loaded code and other state (Spec p.182). Fields: `[[AgentSignifier]]`, `[[Intrinsics]]`, `[[GlobalObject]]`, `[[GlobalEnv]]`, `[[TemplateMap]]`, `[[LoadedModules]]`, `[[HostDefined]]` (Spec p.182).
- `[[TemplateMap]]`: tagged template literal objects are canonicalized **per realm and per parse site**: the same position returns the same array of strings (Spec p.182).
- `InitializeHostDefinedRealm`: creates intrinsics, an initial context (Function and ScriptOrModule null), global object (the host may require a specific one) and global `this` (the host may require another object); then installs standard globals and host-defined globals (Spec p.183). **[HOST]**
- `CreateIntrinsics` adds restricted properties (those that throw) to `%Function.prototype%` (Spec p.183). The iframe example is not in the text **[extrapolation]**.

### 11.2 Execution contexts
- At most **one** context executes per agent (the one at the top of the stack) (Spec p.184). Components: code evaluation state, Function (or `null`), Realm, ScriptOrModule (Spec p.184). Transitions are normally LIFO, but some features require non-LIFO (Spec p.184).
- For ECMAScript code: `LexicalEnvironment` (resolves identifiers), `VariableEnvironment` (receives `var`), `PrivateEnvironment` (Spec p.185). Generator contexts also hold the generator (Spec p.185). Contexts are a Spec mechanism, not observable (Spec p.185).
- `ResolveBinding(name)` resolves from the current `LexicalEnvironment` taking strict into account; `GetThisEnvironment` goes up to an environment with `HasThisBinding` (arrows are "skipped"); `ResolveThisBinding` may throw `ReferenceError`; `GetNewTarget` reads the `this` environment, hence arrows inherit `new.target` (Spec p.185–186).

### 11.3 Jobs [HOST]
- Job = Abstract Closure with no parameters that starts a computation when no other is in progress (Spec p.186). The host schedules; the Spec fixes requirements (Spec p.186–187).
- Invariants (Spec p.187): the job only runs with no running context and an empty stack; **one job at a time per agent**; it runs **to completion** before another starts (basis of no preemption **[inference]**); it must return a normal completion handling its own errors.
- Browsers and Node.js treat Promise jobs with higher priority than other work; future jobs may have lower priority (Spec p.187). **[HOST]**
- `HostEnqueuePromiseJob`: promise jobs run in the **same order** in which they were enqueued (FIFO) and the active script/module must be the same as when they were enqueued (Spec p.189). The realm is that of the `then` function (thenable jobs) or of the handler; handler `undefined` → null realm and no code runs (Spec p.189). **[HOST]**
- `HostEnqueueTimeoutJob(job, realm, ms)`: runs after **at least** `ms` (Spec p.189). The link to `setTimeout` is an **[extrapolation]**.
- `HostEnqueueGenericJob`: schedules at some future time without additional priority or order (Spec p.188).
- `JobCallback`: jobs must use `HostMakeJobCallback`/`HostCallJobCallback`; non-browser hosts must use the default implementation; `HostMakeJobCallback` is called when the callback is passed (in `promise.then(f)`, in `then`), not when the reaction is scheduled (Spec p.187–188). The HTML specification uses this for the *incumbent settings object* (Spec p.187).

### 11.4 Agents and clusters
- Agent = contexts, stack, Agent Record and a thread; one thread may serve several agents if none has `[[CanBlock]]` true (e.g., tabs) (Spec p.189). Agent signifier is a globally unique opaque value (Spec p.189). **[HOST]**
- Agent Record (Spec p.190): `[[LittleEndian]]`, `[[CanBlock]]`, `[[Signifier]]`, `[[IsLockFree1]]`, `[[IsLockFree2]]`, `[[IsLockFree8]]` (4-byte atomics are always lock-free), `[[CandidateExecution]]`, `[[KeptAlive]]`, `[[ModuleAsyncEvaluationCount]]`. Lock-free does not imply wait-free (Spec p.190). `AgentCanSuspend` may be false on a document's main thread and true in workers (Spec p.191). **[HOST]**
- **Agent cluster**: largest set of agents that can share memory (at least that of `SharedArrayBuffer`); every agent belongs to one; agents that only exchange messages are never in the same cluster (Spec p.191). Invariants: same `[[LittleEndian]]`, same `IsLockFree`, distinct signifiers (Spec p.191–192).
- The host must not leave agents of the cluster active and others deactivated indefinitely; if an agent is terminated externally, the host terminates the whole cluster or allows a member to detect the termination (Spec p.192). **[HOST]**
- **Progress**: a blocked agent waits synchronously and indefinitely for an external event; only agents with `[[CanBlock]]` true block. Guarantees: every unblocked agent with a dedicated thread makes progress; among agents sharing a thread, some make progress; an agent does not block another except through blocking APIs (Spec p.193).

---

## 12. WeakRef and FinalizationRegistry

- The Spec **does not guarantee** that any object or symbol is collected; non-live ones may be freed after a long time or never (Spec p.193).
- A successful `WeakRef.prototype.deref` keeps the referent alive until the end of the synchronous work (`ClearKeptObjects`), so subsequent synchronous accesses return the same value (Spec p.193, 195). `AddToKeptObjects` creates a strong reference until the next `ClearKeptObjects` (Spec p.196).
- The `FinalizationRegistry` callback **may** be called after synchronous execution finishes; it never interrupts synchronous ECMAScript; scheduling is up to the host (Spec p.193, 195). **[HOST]** Callbacks may be omitted for any reason (dead registry, application shutting down) (Spec p.195). Correct code cannot depend on collection **[inference]**.
- `CleanupFinalizationRegistry`: the implementation **may** choose a cell with an EMPTY target, remove it and call the callback with the `[[HeldValue]]` and `this` `undefined`; an error from the callback propagates (Spec p.196).
- **Liveness**: a set S is live if some element is in `[[KeptAlive]]` or if a future "WeakRef-oblivious" execution observes the identity of some value of S (through `===` or use as a `Map` key). Being in a field, slot or property does not make it live; `WeakMap` keys, `WeakSet` members, `[[WeakRefTarget]]` and `[[UnregisterToken]]` do not keep it alive (Spec p.193–194).
- If S is not live, the implementation **may**, atomically: empty WeakRefs, registry cells, key **and** value of `WeakMap` entries, `WeakSet` elements (Spec p.194). If it chooses S, it empties **all** its values at once (Spec p.195). Optimizations such as dead-variable elimination may empty WeakRefs; rematerialization that empties a WeakRef whose identity is observable is forbidden (Spec p.195).
- `CanBeHeldWeakly(v)`: true for Object and for a Symbol **not** registered with `Symbol.for`. Only these can be a `WeakMap` key, a `WeakSet` element, a `WeakRef` target or a `FinalizationRegistry` target. Well-known symbols are accepted, but probably never collected, so they may "leak" associated values (Spec p.196).

---


## 13. Ordinary objects

### 13.1 Inheritance, extensibility and delegation
- Every ordinary object has `[[Prototype]]` (null or object) (Spec p.196) and `[[Extensible]]`. With `[[Extensible]]` false: properties cannot be added, the prototype cannot be changed and it cannot go back to true (Spec p.197).
- Property absent on O but present on the prototype: data → inherited for reading; **writable** data → assigning to O creates an own property; **non-writable** data → assignment fails; accessor → inherited for reading and writing (Spec p.196–197).
- Ordinary internal methods delegate to same-named operations; when they depend on another internal method, it is called on the object, respecting overridden exotic ones (Spec p.197).

### 13.2 Ordinary internal methods (effect)
| Method | Behavior | Page |
|---|---|---|
| `[[SetPrototypeOf]](V)` | `true` if V is the current one; `false` if non-extensible; `false` if it would create a cycle (checks only while the prototypes use the ordinary `[[GetPrototypeOf]]`); otherwise switches | Spec p.197–198 |
| `[[PreventExtensions]]` | sets `[[Extensible]]` to false and **always returns `true`** | Spec p.198 |
| `[[GetOwnProperty]]` | `undefined` or a complete descriptor | Spec p.198–199 |
| `[[HasProperty]]` | own, otherwise consults the prototype recursively | Spec p.200 |
| `[[Get]](P, Receiver)` | no own: prototype with the same Receiver; data: value; accessor: `undefined` without a getter, otherwise calls the getter with `this = Receiver` | Spec p.201 |
| `[[Delete]]` | nonexistent → `true`; configurable → removes; non-configurable → `false` | Spec p.202 |

### 13.3 DefineOwnProperty (ValidateAndApplyPropertyDescriptor)
- Nonexistent property: non-extensible → `false`; otherwise creates (accessor if the descriptor is an accessor one, otherwise data) with defaults for absent fields (Spec p.199–200). A descriptor with no fields → `true`, nothing changes (Spec p.200).
- **Non-configurable** current property: refuses (`false`) to make it configurable, change `enumerable`, switch data↔accessor, change `get`/`set` to a different value (SameValue); on non-writable data it refuses `writable: true` and only accepts a `value` equal by SameValue (Spec p.199–200).
- Data↔accessor conversion (if configurable) preserves `configurable` and `enumerable` and applies defaults to the others; the same type applies only the fields present (Spec p.200). That `Object.defineProperty` throws `TypeError` in these cases is an **[extrapolation]** (the excerpt deals with the boolean return).

### 13.4 [[Set]]
Returns a boolean, does not throw by itself (Spec p.201–202):
- No own: delegates to the prototype with the same Receiver; with no prototype, acts as if a writable/enumerable/configurable data property with `undefined` existed.
- Data: non-writable → `false`; non-object Receiver → `false`; Receiver without its own → `CreateDataProperty`; Receiver with an accessor or non-writable data → `false`; otherwise redefines only the `value`.
- Accessor: no setter → `false`; with a setter, calls it with `this = Receiver` and returns `true`.
- That `false` becomes `TypeError` only in strict is an **[extrapolation]** at this point (the conversion is in PutValue, Spec p.81).

### 13.5 Order of own keys
Ordinary `[[OwnPropertyKeys]]` (Spec p.202): (1) array indices in ascending numeric order; (2) other Strings in chronological order of creation; (3) Symbols in chronological order. Derived example: created `"b"`, `"2"`, `"a"`, `"1"` → order `"1"`, `"2"`, `"b"`, `"a"` **[inference]**. Uses in `Object.keys`, `for-in`, `JSON` are **[inference]**.

### 13.6 Creation
- `OrdinaryObjectCreate(proto)` sets `[[Prototype]]` and `[[Extensible]]` to true (Spec p.202–203).
- `GetPrototypeFromConstructor` reads `constructor.prototype`; if it is not an object, uses the default intrinsic **of the constructor's realm**, not of the current context (Spec p.203).
- `RequireInternalSlot(O, slot)`: `TypeError` if O is not an object or lacks the slot (basis of `this` checks in built-ins **[inference]**) (Spec p.203).

---

## 14. Functions (ECMAScript and built-in)

### 14.1 ECMAScript function
- Ordinary object with parameterized code closed over a lexical environment; strict or not (Spec p.204). Slots: `[[Environment]]`, `[[PrivateEnvironment]]`, `[[FormalParameters]]`, `[[ECMAScriptCode]]`, `[[ConstructorKind]]` (BASE/DERIVED), `[[Realm]]`, `[[ScriptOrModule]]`, `[[ThisMode]]`, `[[Strict]]`, `[[HomeObject]]`, `[[SourceText]]`, `[[Fields]]`, `[[PrivateMethods]]`, `[[ClassFieldInitializerName]]`, `[[IsClassConstructor]]` (Spec p.204–205).
- **`[[ThisMode]]`**: LEXICAL (arrow, `this` comes from the enclosing scope); STRICT (`this` exactly as passed); GLOBAL (`undefined`/`null` become the global object; other values go through `ToObject`) (Spec p.204; effect in `[[Call]]`, Spec p.205–207).
- **`[[Call]]`**: class constructor called without `new` → `TypeError` (created in the function's realm); otherwise a new context, `this` bound according to `[[ThisMode]]` (non-strict: `undefined`/`null` → global of the function's realm, primitives → wrapper of the function's realm) (Spec p.205–207).
- **`[[Construct]]`** (Spec p.207–208): BASE creates `this` from `newTarget.prototype` (default `%Object.prototype%`), runs `InitializeInstanceElements` and the body; DERIVED leaves `this` uninitialized until `super()`. Result: if the body returns an **object**, it wins; otherwise BASE returns the created `this`; DERIVED with a non-`undefined` return → `TypeError`; with `undefined` returns the `this` binding (which throws `ReferenceError` if `super()` was never called **[inference]**). Example: `new F()` with `return 1` ignores the primitive **[inference]**.
- `OrdinaryFunctionCreate`: default `[[Call]]` **without** `[[Construct]]`; `[[ThisMode]]` LEXICAL for arrow, STRICT if strict, otherwise GLOBAL (Spec p.208). `MakeConstructor` installs `[[Construct]]`, creates the `prototype` object with `constructor` (non-enumerable, configurable) and defines `F.prototype` as **non-enumerable and non-configurable**, `writable` according to the parameter (default true) (Spec p.209). `MakeClassConstructor` marks `[[IsClassConstructor]]` (Spec p.209).
- `AddRestrictedFunctionProperties` defines `"caller"` and `"arguments"` as accessors with `%ThrowTypeError%` (non-enumerable, configurable) (Spec p.208–209). `%ThrowTypeError%` is one per realm, non-extensible, with non-configurable `length` and `name` (Spec p.209).
- `DefineMethodProperty`: a method with a private key becomes a PrivateElement; otherwise `{writable: true, enumerable: <param>, configurable: true}`; it only fails for a static method named `"prototype"` (Spec p.210). `SetFunctionLength`: `length` `{writable: false, enumerable: false, configurable: true}` (Spec p.211).

### 14.2 FunctionDeclarationInstantiation (effects)
- Without initializers in the parameters, the body's declarations stay in the **same** environment as the parameters; with initializers (default values) a **second environment** is created for the body, so that closures in the parameters do not see the body's declarations (Spec p.211–212).
- The `arguments` object is created, except in arrows, when a parameter is named `arguments`, or (without parameter expressions) when a declared function or lexical binding is named `arguments` (Spec p.211–212).
- `arguments` is **unmapped** if the function is strict or has non-simple parameters (rest, defaults, destructuring); **mapped** only in non-strict with simple parameters. In strict the `arguments` binding is immutable (Spec p.212).
- Duplicate parameter names only occur (by early errors) in non-strict functions without defaults/rest (Spec p.212).
- Non-strict functions use a separate environment for top-level lexical declarations, so that direct `eval` detects conflicts with `var` (Spec p.213). **[DATED]** as to sloppy `eval`.
- `let`/`const`/`class` are created uninitialized; declared functions are instantiated and assigned at the start (Spec p.213).

### 14.3 Built-in function
- Ordinary object with `[[Realm]]`, `[[InitialName]]`, `[[Async]]`; initial `[[Prototype]]` `%Function.prototype%`; always has `[[Call]]`; `[[Construct]]` only if described as a constructor (Spec p.214). Creates a context with the function's realm and null `ScriptOrModule`; in `[[Construct]]` the result must be an object (Spec p.214). `[[Async]]` true returns a Promise (Spec p.215).
- Built-in functions are created by `CreateBuiltinFunction` with initial `length` and `name` (Spec p.215–216).

### 14.4 Bound function (exotic)
- Slots `[[BoundTargetFunction]]`, `[[BoundThis]]`, `[[BoundArguments]]` (Spec p.216). `[[Call]]` calls the target with `this = [[BoundThis]]` and bound arguments + new ones. `[[Construct]]` ignores `[[BoundThis]]` and, if `newTarget` is the bound function itself, replaces it with the target (Spec p.216–217). The bound function's `[[Prototype]]` is that of the target; it only has `[[Construct]]` if the target is a constructor (Spec p.217). Association with `bind` is an **[inference]**.

---

## 15. Exotic objects

They use the ordinary methods except where indicated (Spec p.216).

### 15.1 Array
- `length` is **non-configurable**, a non-negative integer and **< 2^32**; it is greater than every own array index; creating index `i` sets `length` to `i + 1`; reducing `length` deletes the index properties with index ≥ the new `length` (Spec p.217). Applies only to own properties.
- `[[DefineOwnProperty]]`: `"length"` goes to `ArraySetLength`; index ≥ `length` with non-writable `length` → `false`; creating an index updates `length` (Spec p.217–218).
- `ArrayCreate`: `length > 2^32 − 1` → `RangeError`; `length` ends up `{writable: true, enumerable: false, configurable: false}` (Spec p.218).
- `ArraySpeciesCreate`: if `originalArray` is not an array → `ArrayCreate`. Reads `constructor`; if it belongs to **another realm** and is that realm's `%Array%`, treats it as `undefined` (browser compatibility); reads `C[Symbol.species]` (`null` → `undefined`); `undefined` → `ArrayCreate`; non-constructor → `TypeError`; otherwise `new C(length)`, with no guarantee of being an Array (Spec p.218). Basis of `map`/`filter` etc. **[inference]**.
- `ArraySetLength` (Spec p.219): value converted by `ToUint32` and `ToNumber`; if they differ → `RangeError` (negative, fractional, NaN, ≥ 2^32). Reducing: non-writable `length` → `false`; deletes from back to front; if a **non-configurable** element prevents it, `length` stays at index + 1 and returns `false`; a requested `writable: false` is applied only at the end. If the value is an object, `valueOf` is called **twice** (legacy since the 2nd edition, according to the Spec) (Spec p.219). **[DATED]**

### 15.2 String
- Encapsulates `[[StringData]]` and exposes virtual data properties per code unit, plus `length`, all **non-writable and non-configurable** (Spec p.219). `StringGetOwnProperty` serves only keys that are canonical numeric strings of non-negative integers (not `-0`) smaller than the length, with `{writable: false, enumerable: true, configurable: false}` (Spec p.221).
- `[[DefineOwnProperty]]` on a string index only accepts a descriptor compatible with the current value (Spec p.220).
- `[[OwnPropertyKeys]]`: indices `0..len-1`; then other own array indices (≥ len) in numeric order; then other Strings by creation; finally Symbols (Spec p.220).
- Consequences **[inference]**: `new String("abc")[0]` reads `"a"`, but assigning fails; `Object.keys(new String("ab"))` includes `"0"` and `"1"` (enumerable).

### 15.3 Immutable prototype
Only `%Object.prototype%` and host objects **[HOST]** (Spec p.234). `[[SetPrototypeOf]]` delegates to `SetImmutablePrototype`: returns `true` if V is the current prototype (SameValue), otherwise `false` (Spec p.234). The caller decides whether this becomes `TypeError` **[extrapolation]**.

### 15.4 Arguments
- Ordinary (unmapped) or exotic (mapped) (Spec p.221).
- **Unmapped**: prototype `%Object.prototype%`; `length` `{writable: true, enumerable: false, configurable: true}`; `Symbol.iterator` = `Array.prototype.values`; `callee` as an accessor that throws `TypeError` (`%ThrowTypeError%`, **non-configurable**) (Spec p.221–222, 224).
- **Mapped** (only for functions without rest, without patterns, without initializers; may have duplicate names): `callee` is the function itself; indices < number of parameters and < arguments passed share their value with the bindings; with duplicate names only the **last** is mapped; parameters with no corresponding argument are **not** linked **[inference]** (Spec p.221, 224).
- The link breaks if the property is deleted and redefined or becomes an accessor; `[[DefineOwnProperty]]` with `writable: false` fixes the value and removes the mapping; a successful `[[Delete]]` removes the mapping (Spec p.221–223).
- Derived example: `function f(a){ arguments[0] = 9; return a; }` non-strict, simple parameters: `f(1)` returns 9; in strict or with a default it returns 1 **[inference]**.
- **[VERSION-DEPENDENT]**: before ES2017 the Spec required a `"caller"` that throws on ordinary arguments objects; ES2017 removed the requirement (Spec p.222).

### 15.5 TypedArray
- Handles String keys that are "canonical numeric strings": if they are a valid integer index they address elements; the other numeric ones are **absent without walking the prototype chain** (Spec p.225). Extra slots: `[[ViewedArrayBuffer]]`, `[[TypedArrayName]]`, `[[ContentType]]`, `[[ByteLength]]`, `[[ByteOffset]]`, `[[ArrayLength]]` (may be `AUTO` for views of a resizable buffer) (Spec p.225, 228–229).

| Method | For a canonical numeric key | Page |
|---|---|---|
| `[[GetOwnProperty]]` | invalid index → `undefined`; otherwise `{value, writable: true, enumerable: true, configurable: true}` | Spec p.225–226 |
| `[[HasProperty]]` | result of `IsValidIntegerIndex`, without prototypes | Spec p.226 |
| `[[DefineOwnProperty]]` | refuses invalid index, `configurable: false`, `enumerable: false`, accessor or `writable: false`; with `value` it writes (may throw on conversion) | Spec p.226 |
| `[[Get]]` | element or `undefined`, without prototypes | Spec p.226 |
| `[[Set]]` | `this` is itself: writes and `true`; Receiver another and invalid index: `true` with no effect; otherwise ordinary | Spec p.226–227 |
| `[[Delete]]` | `true` if invalid, `false` if valid | Spec p.227 |
| `[[OwnPropertyKeys]]` | indices `0..length-1` (if not out of bounds), non-index Strings, Symbols | Spec p.227 |
| `[[PreventExtensions]]` | `false` if the view does not have a fixed length (resizable buffer) | Spec p.225 |

- A valid index fails if the buffer is detached, the index is not an integer, is `-0` or negative, the view is out of bounds, or index ≥ length (Spec p.229). Writing converts first (`ToBigInt` or `ToNumber`, may throw) and only writes if valid; past the end or on a detached buffer it has no effect (Spec p.230). An invalid read → `undefined` (Spec p.229).
- Length: `TypedArrayLength` with `AUTO` = `floor((bufferSize − byteOffset) / elementSize)`; a view of length 0 with `byteOffset` equal to the buffer size is **not** out of bounds (Spec p.228–229).
- Keys such as `"1.5"`, `"-0"`, `"Infinity"` are canonical numeric: assigning does not create a property and reading gives `undefined` even if the prototype has the key **[inference]**.

### 15.6 Module namespace
- Own String properties = exported names (including `export *`), each `{writable: true, enumerable: true, configurable: false}`; **non-extensible** object (Spec p.230). Slots `[[Module]]`, `[[Exports]]` (sorted by code units) (Spec p.231).

| Method | Behavior | Page |
|---|---|---|
| `[[GetPrototypeOf]]` | `null` | Spec p.231 |
| `[[SetPrototypeOf]]` | immutable prototype | Spec p.231 |
| `[[IsExtensible]]` / `[[PreventExtensions]]` | `false` / `true` | Spec p.231 |
| `[[GetOwnProperty]]` (String) | `undefined` if not exported; otherwise the current value (may throw `ReferenceError` if uninitialized) | Spec p.231 |
| `[[DefineOwnProperty]]` | `false` if the name does not exist or the descriptor asks for `configurable: true`, `enumerable: false`, accessor or `writable: false`; with `value` only if equal | Spec p.232 |
| `[[HasProperty]]` | true if exported | Spec p.232 |
| `[[Get]]` | live binding; `ReferenceError` if the target's environment is not initialized (e.g., circular dependency); not exported → `undefined` | Spec p.232 |
| `[[Set]]` | always `false` | Spec p.233 |
| `[[Delete]]` | `false` if exported; `true` if not | Spec p.233 |
| `[[OwnPropertyKeys]]` | exported ones sorted, then Symbols | Spec p.233 |

---

## 16. Proxy (start of 10.5)

This section covers only Spec p.234–243 (the other parts of Proxy/Reflect are in other files).

- Proxy is exotic with `[[ProxyHandler]]` and `[[ProxyTarget]]` (object or `null`) (Spec p.234). Each trap corresponds to an internal method: `getPrototypeOf`, `setPrototypeOf`, `isExtensible`, `preventExtensions`, `getOwnPropertyDescriptor`, `defineProperty`, `has`, `get`, `set`, `deleteProperty`, `ownKeys`, `apply`, `construct` (Spec p.234–235).
- Without the trap, the operation goes to the target (Spec p.235). Default for traps: validates not revoked; `GetMethod` on the handler; trap `undefined` delegates; otherwise calls it with `this = handler` and the target as the first argument; validates the result against the target (Spec p.235). A detected violation → `TypeError`, at the time of the operation, not at creation.
- **Revoked**: both slots become `null`; any internal method afterwards throws `TypeError` (Spec p.235, 243).
- Boolean results of traps go through `ToBoolean` (Spec p.236–241).

**Invariants checked**

| Trap | Error (`TypeError`) when | Page |
|---|---|---|
| `getPrototypeOf` | result is neither an object nor `null`; or target non-extensible and value ≠ real prototype | Spec p.235 |
| `setPrototypeOf` | trap truthy, target non-extensible and V ≠ current prototype | Spec p.236 |
| `isExtensible` | result ≠ real state of the target | Spec p.236 |
| `preventExtensions` | trap `true` but target still extensible | Spec p.237 |
| `getOwnPropertyDescriptor` | does not return object/`undefined`; `undefined` for a non-configurable property of the target or a property of a non-extensible target; incompatible descriptor; "non-configurable" with no corresponding configurable one on the target; "non-configurable and non-writable" when the target is writable | Spec p.237–238 |
| `defineProperty` | trap truthy but: target non-extensible and new property; `configurable: false` with no corresponding one; incompatible; target configurable; target writable and `writable: false` requested | Spec p.238–239 |
| `has` | trap `false` but target has a non-configurable own property, or is non-extensible and has it (the opposite direction is not checked) | Spec p.239 |
| `get` | non-configurable non-writable data with a different value (SameValue); non-configurable accessor without a getter and value ≠ `undefined` | Spec p.240 |
| `set` | trap truthy with non-configurable non-writable data of a different value; non-configurable accessor without a setter | Spec p.240 |
| `deleteProperty` | trap truthy but a non-configurable one exists, or it exists on a non-extensible target | Spec p.241 |
| `ownKeys` | duplicates; elements that are not String/Symbol; a non-configurable key of the target is missing; non-extensible target without exactly the same keys | Spec p.241–242 |
| `construct` | result is not an object | Spec p.242–243 |

- `apply`: arguments become a real array; `[[Call]]` only exists if the target was callable; no check of the return (Spec p.242). `construct` only exists if the target was a constructor (Spec p.242).
- `ProxyCreate`: `target` or `handler` that are not objects → `TypeError` (for example `new Proxy(1, {})` **[inference]**) (Spec p.243).
- Pitfall **[inference]**: a `set` that forgets to return `true` returns falsy, and in strict the caller turns `false` into `TypeError` (conversion in PutValue, Spec p.81).

---

## 17. Points of attention across excerpts

This file uses only the Spec; there is no divergence between sources on this subject. Points where the Spec text itself requires care when reading:
- **host-defined vs implementation-defined**: the list of terms (Spec p.30) presents "host-defined" as equivalent to implementation-defined, while clause 4.2 distinguishes them (Spec p.27). The editorial distinction of 4.2 prevails.
- **`NaN ** 0`**: the extracted text shows no explicit statement; checked in the steps, exponent 0 is checked before base NaN, so the result is 1 (Spec p.57).
- **AssignmentTargetType** of `f().x`/`f()[x]`: the page break (Spec p.158–159) makes the grouping unclear; the reading adopted is SIMPLE for dot/bracket access over a call, and bare `f()` is WEB-COMPAT/INVALID (Spec p.159).
- The classification of `with`, `Symbol.unscopables`, sloppy `eval` and Annex B as legacy does not appear as a label on these pages; it comes from the "Legacy" concept of conformance (Spec p.25) **[extrapolation]**.

---

## 18. Do not reproduce

Extraction failures of the source PDF; do not copy them as if they were Spec text:
- Flattened exponents and symbols: "253 - 1" = 2^53 − 1 (Spec p.50, 85, 97), "232" = 2^32 (Spec p.92, 217–218), "231" = 2^31 (Spec p.93), counts and `2^1024` (Spec p.55–56), `radix^(k−1)` (Spec p.62).
- Table 2 of numeric operations broken into loose lines: a cell "a throw completion" appears glued to `Number::unsignedRightShift`, but belongs to `BigInt::unsignedRightShift` (Spec p.54, 65).
- Section titles appear at the end of each page; in 4.4 the definitions appear without the term (the association follows the order of the numbers) (Spec p.30–35).
- Figure 1 extracted as loose labels (Spec p.29); tables 24–28 with broken cells (Spec p.190, 216, 227).
- `opt` subscripts glued to the productions (Spec p.89–90, 119, 124, 138).

---

## 19. Gaps

- **Truncated excerpts in the sources**: the expansion of `NonZeroDigit :: one of …` is cut off at the end of Spec p.41; the definition of `TopLevelVarScopedDeclarations` starts at Spec p.136 and continues on Spec p.137 without the section title; the body of `SetImmutablePrototype` starts at Spec p.233 (only the introduction of 10.4.7) and continues on Spec p.234.
- **Outside the scope of this file** (they exist in the Spec, but in other reference files): syntax and semantics of expressions and statements (clauses 11–15 onward), `eval`/`Function` functions, classes, generators, async/await, Promise, modules (linking), Reflect, and the rest of Proxy from 10.5 on.
- **Not in the sources (after searching)**: edition in which each feature entered (except ES2015 for `class`, removal of `caller` on arguments in ES2017 and double `valueOf` in `ArraySetLength` since the 2nd edition); version in which `Float16Array` and `Iterator` entered: version not stated in the sources.
- **Not detailed in the pages read**: the exact moment of function hoisting (GlobalDeclarationInstantiation and block instantiation), the exact class of the `RequireObjectCoercible` error in destructuring (`TypeError` is an inference), `break;` without a label outside a loop, the error type when mixing BigInt and Number, the detailed rules of `Number::toString` (algorithm omitted) and the memory model (clause 29).
- **Spec examples absent**: the iframe example for realms and the relationship between `HostEnqueueTimeoutJob` and `setTimeout` are not in the Spec text (they are **[extrapolation]**).
