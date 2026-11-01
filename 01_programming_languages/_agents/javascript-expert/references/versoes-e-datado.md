# Versions, eras and dated data in JavaScript

This file collects everything the three sources say about version and era: in which ECMAScript edition a feature was introduced (when the source says), what each source considers legacy or browser-specific, what belongs to the environment (host) and not to the language, and how to answer questions like "since which version?" and "is this safe for old browsers?". Use it before asserting anything about versions: Grep for the section title or the feature name, check the corresponding table and only then answer. Abbreviations: Spec = ECMA-262, 17th edition (ECMAScript 2026); EJ1 = *Eloquent JavaScript*, 1st edition (file "3ed"); EJpt = *Eloquent JavaScript* in Portuguese, modern edition. Every cited page is the PDF page, not the printed one. Labels: **[DATED]**, **[VERSION-DEPENDENT]**, **[HOST]**, **[inference]**, **[extrapolation]**. When a source does not state the edition of a feature, the text writes "version not stated in the sources" and never fills it in with a "since ES20XX" from memory.

## Contents

1. Nature of the three sources and rules of use
2. Features that the sources date (feature-by-source table)
3. Spec Annex E: ES2015 corrections with compatibility impact
4. Spec Annex F: incompatibilities between editions (full table)
5. Annex B and legacy or browser features
6. What is [HOST] (not part of the language)
7. Features listed in the Spec with no edition stated
8. EJ1 versus EJpt: old and modern practices
9. Disagreements between the sources
10. Errors and truncated passages in the sources (do not reproduce)
11. Answer procedure
12. Gaps

## 1. Nature of the three sources and rules of use

### 1.1 Spec: complete standard, almost no dating

The Spec is the 17th edition, which defines the ECMAScript 2026 programming language (Spec p.25). It is the standard: when it conflicts with the books, it prevails. The crucial point for this file: **the Spec describes the current state of the language and almost never says in which edition each feature was introduced.** It only talks about editions in three kinds of places:

- occasional notes in the body of the text (for example: class syntax from ECMAScript 2015, Spec p.29; `caller` requirement removed in ES2017, Spec p.222; change from Edition 3 in the handling of `thisArg`, Spec p.473; `valueOf` behavior on Array `length` in force since the 2nd edition, Spec p.219);
- Annex E (ES2015 corrections, Spec p.865) and Annex F (incompatibilities by edition, Spec p.867–869), both informative and reproduced in sections 3 and 4;
- Annex B (legacy browser features, Spec p.843–859), which marks what is legacy, but without saying since when it exists.

Practical consequence: for almost any method, syntax or object in the Spec (for example `at`, `findLast`, `toSorted`, `with`, `Array.fromAsync`, `Float16Array`, Spec p.644 onward), the correct answer to "since which version?" is **version not stated in the sources**. Being in the 2026 Spec only proves that the feature exists in this edition.

The Spec also defines conformance categories that work as era labels (Spec p.25): **Normative Optional** (the implementation may or may not have it; if it has part, it must have everything in the clause; browsers generally need to implement it) and **Legacy** (must be implemented, unless it is also Normative Optional; has undesirable characteristics, is not part of the core, and programmers should not use it or assume its existence in new code). The header examples of these categories are on Spec p.26.

The numbering of editions cited by the Spec: "Edition 3" (Spec p.473), "2nd Edition" (Spec p.219), "Edition 5 and 5.1" (Spec p.865), "ECMAScript 2015", "2016", "2017", "2018", "2019" (Annexes E and F). The current notation for well-known symbols is `%Symbol.name%`; earlier editions used `@@name` (Spec p.52), without saying which edition changed the notation.

### 1.2 EJ1: 1st edition, all [DATED]

The file called "3ed" is actually the **1st edition** of the book, written in 2007 and revised until November 2013 (EJ1 p.247, footer). All of the content is **[DATED]**: only `var`, no `let`, `const`, arrow functions, `class`, Promise, native modules, `Symbol`, `JSON.parse`/`JSON.stringify`, `Object.create`, `querySelector` or `"use strict"` (none of these appears in the text). The examples use the book's own console functions (`print`, `show`, `viewHTML`, `load`, `attach`, `detach`, `inPlacePrinter`), which are the book's **[HOST]** and not the language's (EJ1 p.17; EJ1 p.146; EJ1 p.168; EJ1 p.191).

What the EJ1 says about versions:

- ECMAScript is the document written to describe the language precisely when other browsers started to support it; the author treats JavaScript as ECMAScript plus tools for pages and windows (EJ1 p.5–6).
- It states that ECMAScript 5 has already come out, is compatible with what the book describes and adds as native methods some features that the book implements by hand; it cites "ECMAScript Harmony" as a more radical extension being standardized in 2011 (EJ1 p.6). It gives no edition number beyond "ECMAScript 5".
- It mentions `let` only as a future promise of Harmony, for block variables (EJ1 p.34).
- Browsers compatible with the book's console: Internet Explorer 6+, Firefox 1.5+, Opera 9+, Safari 3+, Chrome (EJ1 p.6). The quirks dealt with are from early 2007 (EJ1 p.195).

Rule of use: never present a claim from the EJ1 as current practice. Cite it as "the EJ1 (1st edition) says..." and add the modern EJpt equivalent (section 8). Claims about performance, cross-browser compatibility and IE bugs are 2007–2013 data.

### 1.3 EJpt: modern edition

The EJpt uses let/const, arrow functions, classes, Promises, async/await, ES modules, `??`, `?.`, private fields. The text declares it uses "a versão 2024 do JavaScript" [the 2024 version of JavaScript] (EJpt p.9). The exact edition is not declared; the book has date examples in 2023–2024 (EJpt p.197, p.402), cites Node.js 18 or higher (EJpt p.459) and "mais de três milhões de pacotes" [more than three million packages] on NPM (EJpt p.224). **[inference]** These clues suggest the 4th edition; this is not stated by the text. In an answer, say "the EJpt, which declares it uses 2024 JavaScript".

What the EJpt says about versions (EJpt p.9): ECMAScript 3 was widely supported from roughly 2000 to 2010; version 4, ambitious, was abandoned in 2008 due to political difficulty; version 5, modest, came out in 2009; version 6 came out in 2015, with ideas that came from 4, and since then there have been small annual updates. The designers avoid changes that break existing programs, so new browsers run old code, but old browsers may not support new features (EJpt p.9).

Within the EJpt, only a few features get an explicit year: `class` (2015 edition, EJpt p.132), symbols (2015, EJpt p.141), arrow functions (2015, EJpt p.56), ES modules ("desde o ECMAScript 2015" [since ECMAScript 2015], EJpt p.221) and the "before 2015" contrast for improvised module systems (EJpt p.225) and for `var` (EJpt p.31–32, p.52–53). Everything else (`?.`, `??`, `#private`, class fields, `Object.hasOwn`, `padStart`, rest/spread, destructuring, `async`/`await`, `matchAll`, flags `y` and `u`, `\p{...}`) appears without a version: "version not stated in the sources" (EJpt p.98, p.138, p.93–95, p.97–98, p.209–210, p.192–193, p.207–209, p.212–213).

### 1.4 Combined rules of use

1. The Spec prevails over the two books on semantics; EJpt is the modern explanation; EJ1 is historical testimony.
2. To date a feature, look first in section 2 (what the sources date). If it is not there, apply section 7 (listed but with no edition) or answer "version not stated in the sources".
3. For "is this legacy?", look in section 5; the Spec labels as Legacy and Normative Optional what it considers legacy (Spec p.25).
4. For "is this the language or the environment?", use section 6.
5. Release dates of browsers, of Node.js and of per-engine support are **not in** the sources, except the few cited in the text (for example Node 18+ in EJpt p.459).

## 2. Features that the sources date (feature-by-source table)

The "Spec" column summarizes what the standard says; "EJ1" and "EJpt" what each book says. "n/a" = not found in the text of the sources after searching.

| Feature | Spec | EJ1 [DATED] | EJpt | Label |
|---|---|---|---|---|
| `class` syntax | From ECMAScript 2015 on there are syntactic class definitions that express the constructor + prototype + methods pattern concisely (Spec p.29); the language remains fundamentally not class-based (Spec p.28) | n/a; uses constructor functions, `new` and `prototype` (EJ1 p.126–129) | Introduced in the 2015 edition; before, a plain function and `prototype` manipulation were used (EJpt p.132); a `class` constructor cannot be called without `new` (EJpt p.131, p.170) | [VERSION-DEPENDENT] ES2015 |
| Symbols (`Symbol` type) | Language type, unique and immutable values used as property keys (Spec p.51); well-known symbols (Spec p.52–53); the Spec does not say in which edition they appeared | n/a | Added in 2015 (EJpt p.141); `Symbol("description")` returns a unique value (EJpt p.141–142) | [VERSION-DEPENDENT] ES2015 (EJpt only) |
| ES modules (`import`/`export`) | Modules are language units, with the grammar goal `Module` in addition to `Script` (Spec p.28, p.36); loading delegated to the host (Spec p.432–433); edition of entry: version not stated in the sources | n/a; the modularity chapter organizes programs by convention, with files loaded by `<script>`, its own `load` and objects as namespaces (EJ1 p.167–172); that the language has no native module system is an **[inference]** (p.167 does not state it) | "Since ECMAScript 2015" there are two kinds of program, scripts and modules (EJpt p.221) | [VERSION-DEPENDENT] ES2015 (EJpt only) |
| CommonJS modules and the IIFE pattern | n/a | Module pattern with a function and `provide` (EJ1 p.171–172), homemade `load`/`require` (EJ1 p.168–169) | CommonJS is the improvised system "before 2015" (EJpt p.225); IIFE with a global variable (EJpt p.225–226); there is no reason to write new programs in CommonJS (EJpt p.229) | [DATED] |
| Arrow functions `=>` | The Spec describes functions (chapter 15, Spec p.355–397) without giving the edition in which arrow functions entered: version not stated in the sources | n/a | Added in 2015 to write small functions less verbosely (EJpt p.56) | [VERSION-DEPENDENT] ES2015 (EJpt only) |
| `let` and `const` | Annex F records that in ES2015 a statement list starting with `let` followed by a line break and an identifier begins a LexicalDeclaration, and so does `let [` (Spec p.867) | `let` cited only as a future feature of "Harmony" (EJ1 p.34); blocks do not create scope (EJ1 p.34) | `var` is the "pre-2015" form, when `let` did not exist (EJpt p.31–32, p.52–53) | [VERSION-DEPENDENT] ES2015 |
| `var` | n/a as a dated feature | The only way to declare a variable (EJ1 p.15) | Pre-2015 form, function scope, "behaves strangely" (EJpt p.31–32, p.52–53) | [DATED] |
| Tail position calls (tail calls) | Rules of `IsInTailPosition` (strict code only, outside async and generators) and `PrepareForTailCall` (Spec p.392–397); the preparation appears when calling (Spec p.294); the Spec does not say which engines implement it nor the edition | n/a | n/a | Version not stated in the sources; [HOST] as to engines |
| `caller` on ordinary arguments | Before ES2017 the Spec required a `"caller"` property that throws on `arguments` objects; implementations no longer have it and ES2017 removed the requirement (Spec p.222) | n/a | n/a | [VERSION-DEPENDENT] ES2017 |
| `thisArg` handling of `apply`/`call` | `thisArg` is passed unmodified; change from Edition 3, which replaced `undefined`/`null` with the global object; non-strict functions still do the replacement on entry (Spec p.473) | n/a (uses `apply`/`call`, EJ1 p.126) | `this` is `undefined` in a strict function called without a receiver (EJpt p.169) | [VERSION-DEPENDENT] Edition 3 (Spec) |
| `Function.prototype` being a function | For compatibility with pre-ES2015 code (Spec p.472–473) | n/a | n/a | [VERSION-DEPENDENT] ES2015 |
| `Array.prototype` being an Array | For compatibility with pre-ES2015 code (Spec p.619) | n/a | n/a | [VERSION-DEPENDENT] ES2015 |
| Names in `@@unscopables` of `Array.prototype` | Names that were not standard properties before ES2015, hidden from the `with` binding so as not to break old code (Spec p.644) | n/a | n/a | [VERSION-DEPENDENT] ES2015 |
| `source`, `global`, `ignoreCase`, `multiline` of RegExp | Before ES2015 they were data properties of the instances; now they are accessors on the prototype (Spec p.613) | n/a | n/a | [VERSION-DEPENDENT] ES2015 |
| Dynamic lookup of `exec` in RegExp | There is a compatibility path for code written for earlier editions without dynamic lookup (Spec p.609); unnumbered editions | n/a | n/a | [VERSION-DEPENDENT] unnumbered edition |
| `instanceof` and `Symbol.hasInstance` | Compatibility steps with earlier editions that did not use `%Symbol.hasInstance%` (Spec p.310) | `instanceof` described without `Symbol.hasInstance` (EJ1 p.163) | `instanceof` (EJpt p.147) | [VERSION-DEPENDENT] unnumbered edition |
| Internal tag `[[Class]]` and `Object.prototype.toString` | The definition preserves compatibility with legacy code that used `toString` to detect the type of built-in objects; it is not a reliable type test (Spec p.468) | n/a | n/a | [DATED] |
| Order of steps of `hasOwnProperty` and `isPrototypeOf` | Order chosen to preserve exceptions thrown by earlier editions when `this` is `undefined` or `null` (Spec p.466) | `hasOwnProperty` with `call` and failure points in IE8 (EJ1 p.130–131) | `Object.hasOwn(obj, name)` (EJpt p.138) | [VERSION-DEPENDENT] unnumbered edition |
| Double `valueOf` in `ArraySetLength` | Legacy behavior specified since the 2nd edition (Spec p.219) | n/a | n/a | [DATED] |
| Edition 3 (ES3) | n/a as a feature | Era's list of reserved words (EJ1 p.21) | ES3 widely supported from about 2000 to 2010 (EJpt p.9) | [DATED] |
| ES5 | "Edition 5 and 5.1" appears in Annex E (Spec p.865) | ECMAScript 5 has already come out (EJ1 p.6) | Version 5 came out in 2009 (EJpt p.9) | [VERSION-DEPENDENT] |
| ES6 / ES2015 | Main reference of Annexes E and F (Spec p.865, p.867–869) | n/a | Version 6 came out in 2015; annual updates afterwards (EJpt p.9) | [VERSION-DEPENDENT] |
| ECMAScript 2024 | n/a (the Spec is ES2026, p.25) | n/a | Version that the book declares it uses (EJpt p.9) | EJpt information |
| Top-level await, import attributes, JSON modules | The top-level module grammar allows `await` (Spec p.402); supported import attributes depend on the host (Spec p.434); edition: version not stated in the sources | n/a | n/a | Version not stated in the sources; [HOST] as to attributes |
| `async`/`await` | Described in clause 27 (Spec p.764–807 in general); Annex F records that in ES2019 the number of Jobs queued by `await` was reduced, with a possible observable difference in order between `then()` and `await` (Spec p.869) | n/a | `async` functions and `await` (EJpt p.249–250, p.252); edition: version not stated in the sources | [VERSION-DEPENDENT] ES2019 (only the Jobs reduction) |
| `Atomics.wake` to `Atomics.notify` | Renamed in ES2019 (Spec p.869) | n/a | n/a | [VERSION-DEPENDENT] ES2019 |
| Template objects (tagged templates) | Canonicalized by Parse Node (location in the source code) from ES2018, instead of by all occurrences of the same literal in the Realm (Spec p.867) | n/a | n/a | [VERSION-DEPENDENT] ES2018 |
| Unicode version requirement | ES2015 required 5.1; ES2016 requires 8.0.0 or higher; ES2017 started requiring the latest version (Spec p.867) | n/a | n/a | [VERSION-DEPENDENT] ES2016, ES2017 |
| Initializer in `for (var x = ... in ...)` | ES2015 forbade it with ForBinding; ES2017 allows it only in non-strict code (Spec p.868); Annex B.3.5 (Spec p.857–858) | n/a | n/a | [VERSION-DEPENDENT] ES2015, ES2017; [DATED] |
| Labelled function declarations and functions in blocks | ES2015 started allowing them in the grammar and forbidding them by early error; Annex B suppresses this in non-strict code (Spec p.855) | n/a | n/a | [DATED] Annex B |

Reading the table: the rows marked "EJpt only" mean that the Spec describes the feature but does not state the edition; the edition comes from the modern book.

## 3. Spec Annex E: ES2015 corrections with compatibility impact

Annex E is informative and is titled "Corrections and Clarifications in ECMAScript 2015 with Possible Compatibility Impact" (title at the end of Spec p.865). All items are **[VERSION-DEPENDENT]**: they describe differences between ES5/5.1 and ES2015.

| Clause | What changed | Page |
|---|---|---|
| 9.1.1.4.14–17 | Editions 5 and 5.1 tested for the existence of a property (including inherited) on the global object to decide whether a global declaration already existed; ES2015 tests for an **own** property, which matches what browsers mostly implemented | Spec p.865 |
| 10.4.2.1 (Array) | The 5th edition captured the length before converting the index or the new `length`, and the value could become invalid by side effect; ES2015 captures it **after** | Spec p.865 |
| 21.4.1.31 (TimeClip) | Earlier editions allowed `+0` or `-0` for time zero; ES2015 always returns `+0`, so the time value of a Date is never observably `-0` | Spec p.865 |
| 21.4.1.32 (date format) | Without a UTC offset, the **local** time zone is used; Edition 5.1 incorrectly said that the absence of a time zone would be interpreted as "Z" | Spec p.865 |
| 21.4.4.36 | If the year cannot be represented in the date and time format, it throws `RangeError`; earlier editions did not specify | Spec p.865 |
| 21.4.4.41 | `Date.prototype.toString` with time value `NaN` returns `"Invalid Date"`; before, it was not specified | Spec p.865 |
| 22.2.4.1 and 22.2.6.13.1 (RegExp `source`) | Any line terminator in the `source` value must be written with an escape sequence; Edition 5.1 only required escaping `/` | Spec p.865 |
| 22.2.6.8 and 22.2.6.11 (`match`, `replace` with global RegExp) | Earlier editions were wrong in saying that, if `lastIndex` did not change, it should be incremented by 1; the correct behavior is to increment by 1 **only if the pattern matched the empty string** | Spec p.865 |
| 23.1.3.30 (`Array.prototype.sort`) | `NaN` returned by the comparator is treated as `+0`; ToNumber is applied to the comparator's result; before, the effect of a non-numeric result was implementation-defined (in practice implementations called ToNumber) | Spec p.865 |

## 4. Spec Annex F: incompatibilities between editions (full table)

Annex F is informative: "Additions and Changes That Introduce Incompatibilities with Prior Editions" (title at the end of Spec p.867). The "Edition" column is the one the text itself indicates. All items are **[VERSION-DEPENDENT]**. The clause is the numbering of the 2026 Spec.

| Clause | Change | Edition | Page |
|---|---|---|---|
| 6.2.5 | Function calls cannot return a Reference Record | ES2015 | Spec p.867 |
| 7.1.4.1 | ToNumber of String recognizes binary and octal integer literals (`0b..`, `0o..`) in strings; before they gave `NaN` | ES2015 | Spec p.867 |
| 9.3 | Template objects (template literals and tagged templates) canonicalized by Parse Node (location in the source code), and not by all occurrences of the same literal in the Realm | ES2018 | Spec p.867 |
| 12.2 | Unicode 8.0.0 or higher required (ES2015 required 5.1); `U+180E` (Mongolian vowel separator) moved from Zs to Cf and stopped being whitespace: `"᠎".trim().length` was 0 before and becomes 1; ES2017 started always requiring the latest version of Unicode | ES2016; ES2017 | Spec p.867 |
| 12.7 | Valid code points of IdentifierName defined by `ID_Start` and `ID_Continue`; before, Unicode categories were enumerated | ES2015 | Spec p.867 |
| 12.10.1 | Automatic semicolon insertion adds `;` at the end of `do-while` if missing, aligning the Spec with most implementations | ES2015 | Spec p.867 |
| 13.2.5.1 | Duplicate property names in object initializers are no longer an early error | ES2015 | Spec p.867 |
| 13.15.1 | In strict mode, assigning to an immutable binding (such as the name of a FunctionExpression) is no longer an early error and becomes a runtime error | ES2015 | Spec p.867 |
| 14.2 | A statement list starting with `let`, a line break and an Identifier now begins a LexicalDeclaration; before, ASI inserted `;` before the identifier | ES2015 | Spec p.867 |
| 14.5 | An item starting with `let` followed by `[` is the start of a LexicalDeclaration; before it was an ExpressionStatement | ES2015 | Spec p.867 |
| 14.6.2 | The normal result of `if` is never EMPTY: if no part is evaluated or the result is EMPTY, the result is `undefined` | ES2015 | Spec p.867 |
| 14.7 (for) | In `for (let [`, the `let` is the start of a LexicalDeclaration; before it would be the start of an Expression | ES2015 | Spec p.867 |
| 14.7 (for-in) | In `for (let [` in a for-in, the `let` is the start of a ForDeclaration; before, of a LeftHandSideExpression | ES2015 | Spec p.867 |
| 14.7 | Before ES2015 there could be an initializer in the VariableDeclaration before `in`; ES2015 does not allow it with ForBinding; ES2017 allows it only in non-strict code | ES2015; ES2017 | Spec p.868 |
| 14.7 | The result of IterationStatement is never normal with an EMPTY value: it becomes `undefined` | ES2015 | Spec p.868 |
| 14.11.2 | The result of `with` is never EMPTY; it becomes `undefined` | ES2015 | Spec p.868 |
| 14.12.4 | The result of `switch` is never EMPTY; it becomes `undefined` | ES2015 | Spec p.868 |
| 14.15 | In ES2015 it is an early error for `catch` to contain a `var` with the same name as the parameter; before, the `var` was instantiated in the enclosing environment and the initializer assigned to the catch parameter (Annex B.3.4 allows it again in non-strict code, Spec p.857) | ES2015 | Spec p.868 |
| 14.15 and 19.2.1.3 | In ES2015, throws `SyntaxError` at runtime if the `catch` evaluates a non-strict direct `eval` whose code has a `var` or FunctionDeclaration binding the same name as the catch parameter | ES2015 | Spec p.868 |
| 14.15.3 | The result of TryStatement is never EMPTY (becomes `undefined` in the cases described) | ES2015 | Spec p.868 |
| 15.4.5 | Functions created as `[[Get]]` or `[[Set]]` of accessors in object literals are not constructors and have no `prototype`; before they were constructors and had one | ES2015 | Spec p.868 |
| 20.1.2.6 `Object.freeze` | A non-object argument is treated as an ordinary non-extensible object with no own properties; before it was always `TypeError` | ES2015 | Spec p.868 |
| 20.1.2.8 `Object.getOwnPropertyDescriptor` | A non-object argument goes through ToObject if possible; before it was always `TypeError` | ES2015 | Spec p.868 |
| 20.1.2.10 `Object.getOwnPropertyNames` | Same: ToObject | ES2015 | Spec p.868 |
| 20.1.2.12 `Object.getPrototypeOf` | Same: ToObject | ES2015 | Spec p.868 |
| 20.1.2.16 `Object.isExtensible` | A non-object is treated as an ordinary non-extensible object with no own properties; before `TypeError` | ES2015 | Spec p.868 |
| 20.1.2.17 `Object.isFrozen` | Same treatment; before `TypeError` | ES2015 | Spec p.869 |
| 20.1.2.18 `Object.isSealed` | Same | ES2015 | Spec p.869 |
| 20.1.2.19 `Object.keys` | A non-object: tries ToObject; before `TypeError` | ES2015 | Spec p.869 |
| 20.1.2.20 `Object.preventExtensions` | A non-object is treated as non-extensible with no properties; before `TypeError` | ES2015 | Spec p.869 |
| 20.1.2.22 `Object.seal` | Same | ES2015 | Spec p.869 |
| 20.2.3.2 (`bind`) | The `[[Prototype]]` of the bound function is the `[[GetPrototypeOf]]` of the target function; before it was always `%Function.prototype%` | ES2015 | Spec p.869 |
| 20.2.4.1 | The `length` property of functions becomes configurable; before it was non-configurable | ES2015 | Spec p.869 |
| 20.5.6.2 | The `[[Prototype]]` of the NativeError constructor becomes the `Error` constructor; before it was the Function prototype | ES2015 | Spec p.869 |
| 21.4.4 | The Date prototype is not an instance of Date; before it was an instance with TimeValue `NaN` | ES2015 | Spec p.869 |
| 22.1.3.12 `localeCompare` | Strings that are canonically equivalent under Unicode must be treated as identical; before there could be a bit-by-bit comparison | ES2015 | Spec p.869 |
| 22.1.3.28 and 22.1.3.30 (`toLowerCase`, `toUpperCase`) | Conversion operates on code points; before on code units; the only ones affected: the Unicode Deseret block | ES2015 | Spec p.869 |
| 22.1.3.32 `trim` | Recognizes whitespace outside the BMP, although from Unicode 7 on no such code points exist | ES2015 | Spec p.869 |
| 22.2.4.1 (RegExp constructor) | If `pattern` is a RegExp and `flags` is not `undefined`, creates a new instance with the flags replaced; before `TypeError` | ES2015 | Spec p.869 |
| 22.2.6 (prototype) | The RegExp prototype is not an instance of RegExp; before it was a RegExp with an empty pattern | ES2015 | Spec p.869 |
| 22.2.6 (accessors) | `source`, `global`, `ignoreCase`, `multiline` are accessors on the prototype; before they were data properties of the instances | ES2015 | Spec p.869 |
| 25.4.15 | `Atomics.wake` renamed `Atomics.notify` to avoid confusion with `Atomics.wait` | ES2019 | Spec p.869 |
| 27.1.5.4 and 27.6.3.6 | The number of Jobs queued by `await` was reduced, which may change the observable resolution order between `then()` and `await` | ES2019 | Spec p.869 |

Practical consequences of Annex F, all derived from the rows above:

- Code that passes a primitive to `Object.keys`, `Object.getPrototypeOf` and similar stops throwing `TypeError` from ES2015 on (Spec p.868–869); `null` and `undefined` still have no possible ToObject **[inference]**.
- `new` on the function of an object-literal getter or setter fails, since they stopped being constructors (Spec p.868) **[inference]**.
- `Number("0b101")` and `Number("0o17")` convert to a value instead of `NaN` (Spec p.867).
- Code that depended on the exact number of ticks between `await` and `then` may change behavior between engines before and after ES2019 (Spec p.869).
- Completion values (`if`, loops, `with`, `switch`, `try`) become `undefined` instead of EMPTY; this is only observed via `eval` and consoles that show the completion value (Spec p.867–868) **[inference]**.

## 5. Annex B and legacy or browser features

### 5.1 Nature of Annex B

Annex B is normative, but optional if the host is not a browser; browsers are required to support everything (Spec p.843). Some features are in the annex, others in the body of the Spec, marked with the "Normative Optional" box and guarded by the condition that the host supports them (Spec p.843). The Spec itself says that all the features in the annex have undesirable characteristics and would be removed were it not for legacy use; they are not part of the core; programmers should not use them or assume their existence in new code; implementations outside browsers are discouraged from implementing them (Spec p.843). In **strict code** the extensions B.3.1, B.3.2, B.3.3 and B.3.5 cannot be supported, and when parsing with the `Module` goal the lexical extensions of B.1.1 cannot be supported (Spec p.446). The whole annex is **[DATED]** and **[HOST]**.

### 5.2 Table of Annex B features

| Feature | What it is (summary) | Page |
|---|---|---|
| HTML-style comments (B.1.1) | `<!--` comments to the end of the line; `-->` is only valid at the start of a line (preceded by whitespace and single-line block comments); not allowed in `Module` | Spec p.843–844 |
| Legacy RegExp patterns (B.1.2) | Alternative grammar without the `u`/`v` flags: lookahead `(?=` and `(?!` can take a quantifier; a lone `{` is a literal; `\` + digits is a backreference only if the group exists, otherwise a legacy octal escape; `\c` in classes accepts a digit and `_`; in `[\d-x]` the `-` becomes a literal instead of an error; `{n}` without a target is a SyntaxError | Spec p.844–849 |
| `escape` and `unescape` (B.2.1) | Global functions that encode UTF-16 code units as `%XX` or `%uXXXX`; they keep letters, digits, `_` and `@ * + - . /`; based on RFC 1738, they do not reflect RFC 3986 | Spec p.849–851 |
| `String.prototype.substr` (B.2.2) | Substring by position and length; a negative start counts from the end | Spec p.851 |
| String HTML methods (B.2.2) | `anchor`, `big`, `blink`, `bold`, `fixed`, `fontcolor`, `fontsize`, `italics`, `link`, `small`, `strike`, `sub`, `sup`; via `CreateHTML`, which only escapes double quotes of the attribute value | Spec p.851–853 |
| `trimLeft` and `trimRight` (B.2.2) | Alternative names: the same function object as `trimStart` and `trimEnd`; the Spec recommends the new names | Spec p.853–854 |
| `getYear`, `setYear`, `toGMTString` (B.2.3) | `getYear` returns the local year minus 1900; `setYear` sets the year; `toGMTString` is the same object as `toUTCString`; the Spec prefers `getFullYear`, `setFullYear`, `toUTCString` | Spec p.854 |
| `RegExp.prototype.compile` (B.2.4) | Reinitializes an existing RegExp with a new pattern and flags; `TypeError` if `pattern` is a RegExp and `flags` is not `undefined` | Spec p.855 |
| Labelled function declarations (B.3.1) | ES2015 started allowing them in the grammar, but an early error rule generates SyntaxError; Annex B suppresses the error in non-strict code | Spec p.855 |
| Web semantics of functions in blocks (B.3.2) | Functions declared in blocks also get a `var` binding in the outer function, in non-strict code, when this would not cause an early error; the value is copied when the declaration is evaluated | Spec p.855–856; see also Spec p.213 and p.400–401 |
| `function` in `if` clauses (B.3.3) | In non-strict code, `if (c) function f(){}` is accepted as if it were the only item of a block | Spec p.856–857 |
| `var` in `catch` with the parameter name (B.3.4) | The `var` of the `catch` block may have the same name as the parameter; the initializer assigns to the catch parameter, not to the outer variable | Spec p.857 |
| Initializer in `for-in` with `var` (B.3.5) | `for (var x = expr in obj)` accepted in non-strict code | Spec p.857–858 |
| Slot `[[IsHTMLDDA]]` (B.3.6) | Host objects with this slot behave as `undefined` in ToBoolean, `==` and `typeof` (the example is `document.all`) | Spec p.858 |
| Browser host hooks (B.3.7, B.3.8) | `HostMakeJobCallback` and `HostEnsureCanAddPrivateElement` with browser-specific behavior | Spec p.858–859 |
| Function call as an assignment target (B.3.9) | In non-strict code, `f() = 1` throws `ReferenceError` at runtime, not an early error; does not apply to `??=`, `&&=`, `||=`; see also the WEB-COMPAT mark (Spec p.159) | Spec p.859 |

### 5.3 Other legacy features marked in the sources outside Annex B

- **`with`**: the Spec marks it as LEGACY and discourages its use in new code; it is a SyntaxError in strict code (Spec p.347, p.861). The Object Environment Records clause (which exists for `with`) is **[DATED]** (Spec p.163, p.169–171). `Symbol.unscopables` serves this environment (Spec p.53). The EJ1 presents `with` as a statement that the author never used in a real program but has seen in other people's code (EJ1 p.241). The EJpt says strict mode removes the `with` declaration, described as "tão errada" [so wrong] that the book no longer discusses it (EJpt p.170).
- **`__proto__` and legacy accessor methods**: `__proto__` is an accessor marked "Normative Optional, Legacy" (Spec p.468); `__defineGetter__`, `__defineSetter__`, `__lookupGetter__` and `__lookupSetter__` too (Spec p.469). The EJ1 describes `__proto__` as a hidden property of Gecko-family browsers, considered a bad idea by the author (EJ1 p.131). The EJpt presents `Object.getPrototypeOf` and `Object.create` (EJpt p.129–130).
- **Legacy octal**: legacy octal literals (`LegacyOctalIntegerLiteral`) and decimals with a leading zero containing 8 or 9 (`NonOctalDecimalIntegerLiteral`) are called "legacy" by the Spec (Spec p.259); octal string escapes, `\8` and `\9` too (Spec p.262); all are forbidden in strict code (Spec p.861). Templates cannot contain legacy octal escapes (Spec p.446).
- **Legacy `eval` dependencies**: recreating a deletable binding in non-strict mode (Spec p.167–168) is treated as an `eval` legacy; in strict code it throws `ReferenceError`.
- **Strict mode (Annex C, informative)**: list of strict mode restrictions (Spec p.861): `implements`, `interface`, `let`, `package`, `private`, `protected`, `public`, `static` and `yield` reserved; legacy octal and octal escapes forbidden; assignment to an unresolvable identifier throws `ReferenceError`; `eval` and `arguments` cannot be assigned to or used as a binding name; `callee` of the strict `arguments` object throws `TypeError`; `this` is not coerced to an object; `delete` of a direct binding is a SyntaxError; `with` is a SyntaxError; duplicate parameters are a SyntaxError. Usage detail in the EJpt: effects of strict mode (EJpt p.168–170); code inside classes and modules is strict automatically (EJpt p.169).
- **Constructor function called without `new`**: in non-strict mode, `this.name = name` creates a global binding and the call returns `undefined`; in strict mode, it throws `TypeError` (EJpt p.169–170).
- **Pre-ES2015 module patterns**: IIFE and CommonJS (EJpt p.225–226); homemade `load`/`require` (EJ1 p.168–169).
- **`getYear`**: the EJpt mentions it, saying it returns the year minus 1900 and is "em grande parte inútil" [largely useless] (EJpt p.198), in line with Annex B.2.3 (Spec p.854).
- **Timers by string**: in the EJ1, the first argument of `setTimeout` and `setInterval` can be a function or a string of code (EJ1 p.145); the string form is **[DATED]** (and **[HOST]**).
- **Reading JSON with `eval`**: EJ1 practice (EJ1 p.234); today the EJpt uses `JSON.parse` and `JSON.stringify` (EJpt p.99–100).

## 6. What is [HOST] (not part of the language)

### 6.1 According to the Spec

- The Spec does not provide for data input or output: the host environment supplies specific objects whose behavior is outside the scope of the standard (Spec p.26). Examples cited by the Spec for the browser: windows, menus, pop-ups, dialog boxes, text areas, anchors, frames, history, cookies and I/O, and events such as focus, load, error, selection, form submission and mouse (Spec p.27). For the web server: objects for requests, clients and files (Spec p.27).
- Terminology: **host** is an external source that defines the facilities of Annex D (for example, browsers, which follow WHATWG HTML); **host-defined** is a deferred definition without qualification; a **host hook** is an abstract operation defined by the host and must at least return a normal completion or a throw; a **host environment** usually includes objects and functions for input and output as properties of the global object (Spec p.27–28).
- Annex D (Spec p.863–864): list of host hooks (for example `HostEnqueuePromiseJob`, `HostEnqueueTimeoutJob`, `HostLoadImportedModule`, `HostEnqueueGenericJob`, `HostPromiseRejectionTracker`, `HostEnsureCanCompileStrings`, `HostResizeArrayBuffer`, `HostGrowSharedArrayBuffer`, `InitializeHostDefinedRealm`), host-defined fields (`[[HostDefined]]`, `[[HostSynchronizesWith]]`, `[[IsHTMLDDA]]`), the global object (Spec p.864) and job execution (Spec p.864).
- Consequences already described in the Spec: the queuing of Promise reactions uses `HostEnqueuePromiseJob` (Spec p.189, p.768); the minimum wait "timeout" is a contract of `HostEnqueueTimeoutJob` (Spec p.189); the Spec does not define `setTimeout`, and the link between the two is an **[extrapolation]**; hosts need not treat Jobs uniformly, and browsers and Node.js give Promise Jobs higher priority (Spec p.187); module loading is delegated to the host (Spec p.300, p.432–433); supported import attributes depend on the host (Spec p.434); the value of the global `this` can be any object supplied by the host (Spec p.174); `document.all` is the only known example of an object with `[[IsHTMLDDA]]` (Spec p.858).
- What the Spec defines and is **not** host: `globalThis` as a global property (Spec p.448), `Math`, `JSON`, `Promise`, `Intl` only if the implementation offers an internationalization API (the Spec only requires that, if it does, it follow ECMA-402; Spec p.25).

### 6.2 According to the EJ1 [DATED]

- The book's console functions, which are not the language's: `print`, `show`, `viewHTML`, `load`, `attach`, `detach`, `inPlacePrinter`, `recluseFile`, `heightAt`, `showRoute`, `BinaryHeap` (EJ1 p.17; EJ1 p.146; EJ1 p.168; EJ1 p.191).
- `alert`, `confirm`, `prompt`, `setTimeout`, `setInterval`, `window`, `navigator`, `document`, `XMLHttpRequest`, `ActiveXObject` and events are the browser's environment (EJ1 p.16–17, p.145, p.170, p.194–195, p.231).
- Chapters 11 to 14 (Web, DOM, events, HTTP) are almost entirely **[HOST]** (EJ1 p.186–238).

### 6.3 According to the EJpt

- The environment is the collection of existing bindings; at startup it is never empty and generally includes bindings to interact with the surrounding system (EJpt p.33). `prompt` (EJpt p.33–34) and `console.log` (EJpt p.34) belong to the host.
- `setTimeout` (EJpt p.239), the event loop (EJpt p.257), detection of unhandled promise rejection (EJpt p.245), the browser sandbox (EJpt p.290), the DOM (EJpt p.293–310), name resolution in `import` (browser as web addresses, Node.js as files, EJpt p.222), file reading and `readFile` (EJpt p.228), NPM (EJpt p.224), `fetch` and CORS (EJpt p.406–409), `localStorage` and `sessionStorage` (EJpt p.423, p.425), `FileReader` (EJpt p.422), web workers and timers (EJpt p.334–336), canvas (EJpt p.372 onward), events and `window.addEventListener` (EJpt p.318–319), and all of Node.js (modules `node:fs`, `node:http`, global `fetch`, EJpt p.459–494).
- Environment-dependent outputs: time zone and date in the `Date` examples (EJpt p.197).

## 7. Features listed in the Spec with no edition stated

All of these features appear in the 2026 Spec and the text of the sources **does not state the edition in which they were introduced**: use "version not stated in the sources". The EJpt does not date them either, except the few in section 2.

| Feature | Where it is in the Spec | Note |
|---|---|---|
| `Float16Array` | Global constructor (Spec p.458); list of Typed Arrays (Spec p.75); 16-bit FLOAT16 type (clause 23.2) | Version not stated in the sources |
| `Math.f16round` | Spec p.503 | Version not stated in the sources |
| `Math.sumPrecise` | Sum of an iterable of Numbers with precision; `TypeError` if not a Number (Spec p.507–508) | Version not stated in the sources |
| Iterator helpers (`drop`, `every`, `filter`, `find`, `flatMap`, `forEach`, `map`, `reduce`, `some`, `take`, `toArray`) | Spec p.756–761 | Version not stated in the sources |
| `Iterator`, `Iterator.from`, `Iterator.concat` | Subclassable constructor (Spec p.753); `Iterator.from` and `Iterator.concat` (Spec p.754) | Version not stated in the sources |
| `Set` set algebra (`union`, `intersection`, `difference`, `symmetricDifference`, `isSubsetOf`, `isSupersetOf`, `isDisjointFrom`) | Spec p.685–690 | Version not stated in the sources |
| `Object.groupBy` | Spec p.464 | Version not stated in the sources |
| `Map.groupBy` | Spec p.677 | Version not stated in the sources |
| `Map.prototype.getOrInsert`, `getOrInsertComputed` (and equivalents in WeakMap) | Spec p.679–680 (Map); Spec p.693–695 (invalid keys on write) | Version not stated in the sources |
| `Array.fromAsync` | Spec p.617–618 | Version not stated in the sources |
| Non-mutating Array methods: `toReversed`, `toSorted`, `toSpliced`, `with` | Spec p.640–643 | Version not stated in the sources |
| `Array.prototype.at`, `findLast`, `findLastIndex` | `at` (Spec p.619); `findLast` and `findLastIndex` (Spec p.624–625) | Version not stated in the sources |
| `Object.hasOwn` | Spec p.464; the EJpt uses it (EJpt p.138, p.281) | Version not stated in the sources |
| `RegExp.escape` | Spec p.600 | Version not stated in the sources |
| Regular expression modifiers `(?i:...)` | Allowed letters `i`, `m`, `s`; Spec p.559; also in Annex B.1.2 (Spec p.845) | Version not stated in the sources |
| Flags `d` (hasIndices), `v` (unicodeSets), `s`, `y`, `u` | Flag getters (Spec p.602); `u` and `v` together are a SyntaxError (Spec p.598–599, p.849); in the EJpt `y` (p.207–209) and `u` (p.212–213) | Version not stated in the sources |
| `JSON.rawJSON`, `JSON.isRawJSON` | Spec p.734, p.739 | Version not stated in the sources |
| Resizable `ArrayBuffer` (`resize`, `resizable`, `maxByteLength`) and `transfer` | Spec p.698, p.705–707 | Version not stated in the sources |
| Growable `SharedArrayBuffer` (`grow`) | Spec clause 25.2 (summary in the sources); hook `HostGrowSharedArrayBuffer` (Spec p.863) | Version not stated in the sources |
| `Uint8Array.fromBase64`, `fromHex`, `prototype.toBase64`, `toHex` | Spec p.670–672 | Version not stated in the sources |
| `String.prototype.isWellFormed`, `toWellFormed` | `isWellFormed` (Spec p.543); `toWellFormed` (Spec p.555) | Version not stated in the sources |
| `Promise.try`, `Promise.withResolvers`, `Promise.any`, `Promise.allSettled` | `allSettled` (Spec p.773–774), `any` (Spec p.774–775), `try` and `withResolvers` (Spec p.777) | Version not stated in the sources |
| `Atomics.waitAsync` | Spec p.733 (asynchronous DoWait Spec p.727–728) | Version not stated in the sources |
| Top-level `await` in the module; import attributes; JSON modules | Spec p.402; Spec p.434 | Version not stated in the sources |
| Operators `??`, `??=`, `&&=`, `||=`, `**`, `?.` | Punctuators (Spec p.256); optional chain (Spec p.290–291); in the EJpt `?.` (p.98) and `??` appears without a year | Version not stated in the sources |
| BigInt, numeric separators `_` | BigInt literal (Spec p.257); BigInt type (Spec p.33, p.53–55); separators (Spec p.259–260) | Version not stated in the sources |
| Private fields `#x` | `PrivateIdentifier` (Spec p.253); in the EJpt p.133–134 | Version not stated in the sources |
| Hashbang comment | Spec p.252 | Version not stated in the sources |
| `WeakRef`, `FinalizationRegistry` | Spec p.746 and clause 26 | Version not stated in the sources |
| `Reflect`, `Proxy` | Spec clauses 28.1 and 28.2 | Version not stated in the sources |

Important note: the Spec puts old and recent features side by side without signaling their age. Therefore "it is in the Spec" is never enough to answer "is it safe in old browsers?" (see section 11).

## 8. EJ1 versus EJpt: old and modern practices

The table shows the EJ1 practice [DATED] and the equivalent EJpt practice, with pages from both. Where the EJ1 has no equivalent, it says "n/a".

| Topic | EJ1 (1st edition, 2007/2013) [DATED] | EJpt (modern, "2024 version") |
|---|---|---|
| Variable declaration | `var name = expr;` (EJ1 p.15); blocks do not create scope, only functions do (EJ1 p.34); repeated `var` in the same scope passes without comment (EJ1 p.53) | `let` and `const` with block scope; `var` is pre-2015 and rarely used (EJpt p.31–32, p.52–53) |
| Block scope | Cited as a future feature (`let`, "Harmony") (EJ1 p.34) | `let` and `const` have block scope (EJpt p.52–53) |
| Reserved words | Era's list with `char`, `class` and others (EJ1 p.21) | List with `enum`, `yield`, `let` and others (EJpt p.32) |
| Functions | Function declaration and expression with `function` (EJ1 p.39–40); hoisting of declarations without using the term (EJ1 p.39) | Declaration, expression and arrow functions `=>` (EJpt p.55–56); hoisting (EJpt p.55) |
| Variable arguments | `arguments` object, almost an array, without `push` (EJ1 p.64) | Rest parameters `...numbers` and spread (EJpt p.93–95) |
| Parameter default values | `if (arguments.length < 2) howmuch = 1` (EJ1 p.64) | Parameter default value appears without a year (EJpt p.58–59 for optional arguments) |
| Constructor functions versus `class` | Constructors with `new`, `this`, `prototype`, `constructor` (EJ1 p.126–129); inheritance with helpers `inherit`, `method`, `create`, `extend` (EJ1 p.160–163) | `class` with `constructor`, methods, fields, `#private`, `static`, inheritance (EJpt p.130–147); `class` is from 2015 (EJpt p.132) |
| Object as a dictionary | `hasOwnProperty` with `call`, `forEachIn`, `Dictionary` (EJ1 p.129–131) | `Map`, `Object.create(null)`, `Object.hasOwn`, `Object.keys` (EJpt p.136–138) |
| Property enumeration | `for (var x in obj)` (EJ1 p.53–54) | `for...of` and `Object.keys` (EJpt p.87, p.138) |
| Higher-order functions | `forEach`, `map`, `reduce` reimplemented by hand (EJ1 p.78, p.80, p.82) | `filter`, `map`, `reduce` as array methods (EJpt p.112–115) |
| Destructuring and `?.` | n/a | Destructuring (EJpt p.97–98), optional access `?.` (EJpt p.98) |
| Errors and `try/catch` | `throw`, `try/catch/finally`, throwing strings discouraged (EJ1 p.70–75) | `try/catch/finally`, propagation, selective catching, strict mode (EJpt p.176–184, p.168–170) |
| Strict mode | n/a | `"use strict"` at the top of a file or function; automatic in classes and modules (EJpt p.168–170) |
| Callbacks versus Promise | `onreadystatechange` with `readyState == 4` and callbacks (EJ1 p.233) | Callbacks (EJpt p.238–240), Promises (EJpt p.240–243), rejection and `catch` (EJpt p.243–245) |
| `async`/`await` | n/a | `async` functions and `await` (EJpt p.249–250, p.252) |
| HTTP requests | `XMLHttpRequest`, with `ActiveXObject` for old IE (EJ1 p.231); synchronous freezes the browser (EJ1 p.233) | `fetch` returns a promise of `Response` (EJpt p.406–408) |
| JSON | `eval("(" + json + ")")` (EJ1 p.234) | `JSON.parse` and `JSON.stringify` (EJpt p.99–100) |
| Modules | No native system; one file per module, homemade `load`/`require` and IIFE with `provide` (EJ1 p.167–173) | ES modules `import`/`export` (EJpt p.220–223); CommonJS is legacy (EJpt p.225–229); `type="module"` on `<script>` (EJpt p.289) |
| Packaging | n/a | Packages and NPM (EJpt p.223–225); compilation, bundlers, minifiers (EJpt p.229–230) |
| DOM: finding nodes | `getElementById`, `getElementsByTagName`, the `$` function (EJ1 p.199) | The same plus `getElementsByClassName`, `querySelector` and `querySelectorAll` (EJpt p.299–300, p.309–310) |
| Events | `attachEvent` in IE and `addEventListener` in the others; global `event` in IE; IE's `srcElement` and `cancelBubble` (EJ1 p.209–211, p.214–215) | `addEventListener` (EJpt p.318–319) |
| IE quirks | `typeof` of `alert` is `"object"` (EJ1 p.80); IE8 and overwriting of built-in properties (EJ1 p.131); `className`/`htmlFor` attributes (EJ1 p.200); `tbody` mandatory in tables (EJ1 p.203); memory leak in DOM–object cycles (EJ1 p.227–228); browser detection (EJ1 p.194–195) | Compatibility: recent versions behave fairly uniformly (EJpt p.292); browser wars (EJpt p.291–292) |
| Dates | `new Date(...)`, months 0 to 11, `getFullYear` (EJ1 p.56–58) | `Date`, months from 0; `getYear` "em grande parte inútil" [largely useless] (EJpt p.197–198) |
| Regular expressions | Literal, `i`, `g`, `match`, `replace`, `$1`, `new RegExp` (EJ1 p.177–184) | Also `\p{...}` with `u`, `y`, `matchAll`, `u` and code units (EJpt p.192–193, p.207–213) |
| Strings | `charAt`, `slice`, `indexOf`, `split` (EJ1 p.49–52) | The same plus `codePointAt` (EJpt p.119), `padStart` (EJpt p.93) and UTF-16 (EJpt p.117–119) |
| Recursion performance | Recursion about ten times slower than a loop (EJ1 p.36) | About three times slower (EJpt p.62) |
| Timers | `setTimeout` and `setInterval` accept a string of code (EJ1 p.145) | `setTimeout` with a function (EJpt p.239) |
| Console | The book's `print`, `show` (EJ1 p.17) | The host's `console.log` (EJpt p.34) |

## 9. Disagreements between the sources

Each item says what each source states and which prevails (the Spec is the standard; the EJpt is the modern explanation; the EJ1 is dated).

1. **Block scope.** EJ1: blocks do not create scope, only functions do, and `let` appears only as a future promise (EJ1 p.34). EJpt: `let` and `const` have block scope; `var` respects only function scope (EJpt p.52–53). Spec: LexicalDeclaration syntax consolidated since ES2015 (Spec p.867). The EJpt/Spec **prevails**; the EJ1 only holds for `var`.
2. **`catch` with a `var` of the same name.** Spec Annex F: in ES2015 it is an early error (Spec p.868). Spec Annex B.3.4: in non-strict code, the `var` is allowed and the initializer assigns to the catch parameter (Spec p.857). Both statements coexist: the body rule (error) holds in strict mode and the Annex B rule (allowed) in non-strict browser mode. **[VERSION-DEPENDENT]** and **[HOST]**.
3. **Initializer in `for-in`.** Annex F: ES2015 forbade it and ES2017 allows it in non-strict code (Spec p.868); Annex B.3.5 describes the semantics (Spec p.857–858). No conflict, just two angles on the same rule.
4. **`matchAll`.** The EJpt describes `matchAll` as returning "um array de arrays" [an array of arrays] (EJpt p.210), but the example walks through it with `for...of`. Spec: it returns an iterator (Spec p.546). The Spec **prevails**.
5. **Recursion and performance.** EJ1: about ten times slower than a loop (EJ1 p.36). EJpt: about three times (EJpt p.62). They are measurements from different eras; do not use either as a current rule.
6. **EJpt edition.** The text does not declare the edition; probably the 4th edition is an **[inference]**, supported by dates in 2023–2024 (EJpt p.197, p.402) and by the declaration of using the 2024 version (EJpt p.9). A categorical statement of the edition (3rd or 4th) is not supported by the text.
7. **EJ1 "3ed".** The file name suggests the 3rd edition, but the content is the 1st (2007, revised in 2013; EJ1 p.247). The content prevails.
8. **Reserved words.** EJ1 p.21 lists terms such as `abstract`, `boolean`, `byte`, `char`, `double`, `final`, `float`, `goto`, `int`, `long`, `native`, `short`, `synchronized`; EJpt p.32 lists another set, without those terms and with `let`, `yield`, `enum`, `static`. The Spec deals with future reserved words in clause 12.7.2 (cited in Spec p.25) and lists those reserved only in strict mode in Annex C (Spec p.861). The Spec **prevails**; the books' lists are illustrative.
9. **Automatic strict mode.** EJpt: class and module code is strict (EJpt p.169); Spec: a class definition is always strict code (Spec p.376). They agree.
10. **`{,4}` in regex.** The EJ1 states that `{,4}` means four or fewer (EJ1 p.179); the Spec lists the quantifiers `{n}`, `{n,}` and `{n,m}` (Spec p.558–559, p.582); the form `{,4}` is not in the Spec, and a quantifier in braces without a target is a SyntaxError in legacy mode (Spec p.845–846). The Spec **prevails**; see section 10.
11. **`thisArg` and non-strict functions.** Spec: `thisArg` is passed unmodified since Edition 3, but non-strict functions still replace `undefined`/`null` with the global on entry (Spec p.473). EJpt: in a non-strict function called without a receiver, `this` is the global object; in strict it is `undefined` (EJpt p.169). They agree.

## 10. Errors and truncated passages in the sources (do not reproduce)

Items that must not be repeated as if they were correct:

- **EJ1 p.17**: the example prints the square of the number, but the text talks about "raiz quadrada" [square root]. A book error; do not reproduce the description.
- **EJ1 p.179**: `{,4}` described as four or fewer; **[DATED]** and doubtful; do not reproduce as valid ECMAScript RegExp syntax (Spec p.558–559 only lists `{n}`, `{n,}`, `{n,m}`).
- **EJ1 p.234**: `evalJSON` based on `eval`; presented only as period practice, not as a recommendation (the book itself warns about the risk, EJ1 p.234).
- **EJ1 p.80**: the claim that `alert` is not a real function in IE and has no `apply` is an IE quirk of the time **[HOST][DATED]**; do not generalize to the language.
- **EJpt p.210**: `matchAll` described as "um array de arrays" [an array of arrays]; contradicts the example; treat as iterable (Spec p.546).
- **EJpt p.227**: the date formatting code with `M(MMM)?` only accepts `M` or `MMMM` and does not handle `MM`/`MMM`.
- **EJpt p.474**: the text talks about installing "uma versão específica de mime" [a specific version of mime], but the command's package is `mime-types`.
- **Spec p.808–810**: mathematical symbols appear glued together and there is a duplication "execution execution" in NOTE 1 of Spec p.808; extraction noise with no semantic effect.
- **Spec p.849**: the text says the entries of Table 1 are added to Table 6 but the table is labelled "Table B.1"; numbering noise.
- **Spec p.865**: the item for 21.4.4.36 cites only the section, without naming the function; do not attribute it to a specific method without checking the standard.
- **Spec p.868**: the `Object.isExtensible` row says a non-object is treated as an ordinary non-extensible object, without stating the return; the returned value (`false`) is an **[inference]**.
- **Spec p.813–842**: they exist in the PDF (end of the memory model and Annex A, grammar summary), but were not distilled; nothing was inferred for them (see Gaps).
- **Spec p.860, p.862, p.866, p.870**: pages with no text in the PDF (blank or title only); the title of Annex C appears at the end of p.861.
- **Section titles at the end of each page** (PDF pattern): the numbering of clauses may look shifted; confirm using the clause cited in the Annex F row itself.

## 11. Answer procedure

### 11.1 "Since which version X?"

1. Normalize the feature name (for example `Array.prototype.at`, `class`, `Symbol`, `import`).
2. Look in section 2 (dated features) and in Annexes E and F (sections 3 and 4). If there is a year, answer with it, the source and the page. Example wording: "The EJpt states that `class` was introduced in the 2015 edition (EJpt p.132); the Spec also records that class syntax comes from ES2015 (Spec p.29)."
3. If the feature is in section 7, or is described by the Spec without an edition, answer: "version not stated in the sources", plus the page where the Spec defines it. Add that being in the 2026 Spec only proves it exists in ES2026 (Spec p.25).
4. If the question is about ES5 or ES6 as generic labels, use EJpt p.9 (ES3 around 2000–2010, v4 abandoned in 2008, v5 in 2009, v6 in 2015) and EJ1 p.6 (ES5 already released).
5. If the feature belongs to the browser or Node (DOM, timers, `fetch`), say it is not part of the language **[HOST]** and that the sources give no version (section 6).
6. Never invent "since ES20XX". If the user insists, offer checking in an external source as an **[extrapolation]**, clearly separated from what the sources say.

### 11.2 "Is this safe for old browsers?"

1. Classify the feature:
   - **From the EJ1 (1st edition)**: all [DATED]; it holds in engines of the era (2007–2013), but contains IE quirks (section 8). Do not use as a current reference.
   - **From Annex B**: it exists in browsers by obligation (Spec p.843), but it is legacy: do not assume it in new code and it does not exist in modules nor, in general, in strict mode (Spec p.446).
   - **Dated as ES2015 or later**: the EJpt says old browsers may not support new features (EJpt p.9) and that many packages are compiled to an earlier version (EJpt p.229). The Spec does not list per-browser support. Answer that the sources give no support table and refer to the compilation (transpilation) cited in EJpt p.229–230.
   - **With no edition stated** (section 7): "version not stated in the sources"; assert neither safety nor unsafety.
   - **[HOST]**: depends on the environment; the Spec only requires the host to fulfill the hooks (Spec p.863).
2. Check whether the code is in a module or in strict mode: in both, the legacy behavior of Annex B does not apply (Spec p.446, p.861; EJpt p.169).
3. Answer in two parts: "what the sources guarantee" (with page) and "what the sources do not cover" (per-browser support, release year of each engine). The second block can only be completed with external information, marked as an **[extrapolation]**.
4. Recommend, at most, the alternatives that the sources themselves point to: `trimStart`/`trimEnd` instead of `trimLeft`/`trimRight`, `getFullYear` instead of `getYear`, `toUTCString` instead of `toGMTString` (Spec p.853–854), `encodeURIComponent` in place of `escape` (**[extrapolation]**, not named in the Spec's Annex B).

### 11.3 Short examples

- Question: "Which version is `Object.groupBy` from?" Model answer: version not stated in the sources; the 2026 Spec defines it (Spec p.464).
- Question: "Does `let` work in an old browser?" Model answer: the EJ1 cites `let` only as a future feature (EJ1 p.34); the EJpt says `var` is the pre-2015 form (EJpt p.31–32); the Spec records the ASI change with `let` in ES2015 (Spec p.867); per-browser support is not in the sources.
- Question: "Can `escape()` be used?" Model answer: it is an Annex B legacy feature, mandatory in browsers and optional elsewhere (Spec p.843, p.849–851); the Spec discourages it in new code (Spec p.843).

## 12. Gaps

What the sources do not cover or leave incomplete:

- **Systematic dating of features**: the Spec does not state the edition of entry for most features; only Annexes E and F and a few notes date anything. There is no table of features by edition (ES2016 to ES2026) in any of the three sources.
- **Support per browser and engine**: there is no compatibility table (Chrome, Firefox, Safari, Edge, Node). Only the browsers of the EJ1 console (EJ1 p.6), the EJpt compatibility narrative (EJpt p.291–292) and Node 18+ (EJpt p.459) are present.
- **Exact EJpt edition**: not declared by the text; only the "2024 version" (EJpt p.9).
- **Release dates** of ES3, ES5 and ES6: given only approximately by the EJpt (p.9); editions ES2016 to ES2026 have no dates in the sources beyond the years in the names.
- **Spec p.813–842**: not covered in the consolidated material. The PDF has there the end of the memory model (p.813–814) and Annex A, grammar summary (A.1 to A.8, p.815–842), before Annex B (p.843); the index `spec_toc.json` locates these sections, but the content was not distilled.
- **Spec p.860, p.862, p.866, p.870**: pages with no text in the PDF (blank or title only); it was not checked whether there are images.
- **Details of B.1.2**: the legacy regex details on p.844–849 were summarized; the algorithms were not transcribed; B.3.7 and B.3.8 carry only the names of the hooks (Spec p.858–859).
- **Annex A** (grammar summary) and the other annexes are not in the consolidated material.
- **EJ1**: does not mention `Symbol`, `Promise`, `JSON.parse`, `Object.create`, `querySelector` or `"use strict"`; any question about them needs the EJpt or the Spec.
- **EJpt**: hardly dates the modern features; only `class`, symbols, arrow functions, ES modules and `var` receive 2015 or "pre-2015".
- **Tail calls**: the Spec describes the rules (Spec p.392–397), but the sources do not say which engines implement them nor since when.
- **`Intl` and `Temporal`**: `Intl` is only cited as conditional (Spec p.25); `Temporal` is not in the sources consulted.
