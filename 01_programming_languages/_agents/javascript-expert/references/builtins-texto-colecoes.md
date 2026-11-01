# Text and collection built-ins: String, RegExp, Array, TypedArray, Map, Set, buffers

This file is a quick-lookup catalog, by member name, of the built-in text and collection objects defined by the Spec (ECMA-262, 17th edition, ECMAScript 2026): `String`, `RegExp`, `Array`, `TypedArray` (with `Uint8Array` base64/hex), `Map`, `Set`, `WeakMap`, `WeakSet`, `ArrayBuffer` and `SharedArrayBuffer`. Each object has a section with a six-column table (Member, Signature, What it does and edge cases, Error thrown, Page, Mark). To find a member, Grep for its name (for example `padStart`, `lastIndex`, `getOrInsert`) or for the section title (for example `## 3. RegExp`). All pages are pages of the Spec PDF and appear as `(Spec p.N)`. The Spec is normative, but it almost never says in which edition a feature appeared; when that happens, the table says "version not stated in the sources".

## Contents

1. Conventions and marks
2. String
   - 2.1 Constructor and static functions
   - 2.2 General prototype rules
   - 2.3 Character access and length
   - 2.4 Search and comparison
   - 2.5 Slicing, padding, repetition and splitting
   - 2.6 Methods that delegate to RegExp (match, replace, search...)
   - 2.7 Case, normalization, trim and Unicode well-formedness
   - 2.8 String iterator
   - 2.9 Legacy Annex B methods
3. RegExp
   - 3.1 Flags
   - 3.2 Pattern syntax
   - 3.3 Unicode properties (`\p`)
   - 3.4 Constructor and static functions (including `RegExp.escape`)
   - 3.5 Prototype: exec, test, flags, source, toString
   - 3.6 Symbol.match, matchAll, replace, search, split methods
   - 3.7 lastIndex and the exec algorithm
   - 3.8 Annex B and legacy
4. Array
   - 4.1 Constructor and statics
   - 4.2 Prototype: mutators, accessors, iteration, non-mutating
   - 4.3 Holes, genericity and species
5. TypedArray
6. Uint8Array: base64 and hex
7. Map
8. Set (including set algebra)
9. WeakMap
10. WeakSet
11. ArrayBuffer
12. SharedArrayBuffer
13. Divergences and points of attention between Spec passages
14. Do not reproduce (noise and truncated passages in the sources)
15. Gaps

## 1. Conventions and marks

- **Sources**: this file uses only the Spec. EJ1 and EJpt are not cited here.
- **Marks**: **[DATED]** for Annex B (legacy browser features, which the Spec itself says to replace with alternatives); **[HOST]** for behavior defined by the environment (for example `localeCompare` ordering, `toLocaleString` format); **[VERSION-DEPENDENT]** when the Spec attributes the change to an edition; **[inference]** and **[extrapolation]** for links that are not written in the Spec; "version not stated in the sources" when the text does not date the feature.
- **String indices**: the Spec indexes strings by UTF-16 code unit, not by full Unicode character (Spec p.540–541). An emoji outside the basic plane takes two positions.
- **`this` pattern**: most `String.prototype` methods do `RequireObjectCoercible(this)` and then `ToString(this)`, so `null` or `undefined` as `this` throws `TypeError` [inference from the convention described, Spec p.540–553]. `Array.prototype` methods are generic via `ToObject`; `TypedArray` ones are not (see sections 4 and 5).
- **The 2^53 − 1 limit**: in the PDF the exponent was lost and appears as "253 - 1"; this file writes 2^53 − 1 [inference, see section 14].

## 2. String

### 2.1 Constructor and static functions

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `String` | `String(value)` / `new String(value)` | With no argument gives the empty string. Called as a function it converts the value; if it is a Symbol, it returns the symbol's textual description instead of throwing. With `new`, it creates a String object (slot `[[StringData]]`) whose prototype comes from `NewTarget`. It can be extended with `extends`; the subclass must call `super` to create the slot. | With `new` and a Symbol the flow falls into ToString [inference: TypeError] | p.538 | — |
| `String.fromCharCode` | `(...codeUnits)` | Converts each argument with ToUint16 (reduces modulo 2^16, no error) and concatenates the code units. The function's `length` is 1. | — | p.538 | — |
| `String.fromCodePoint` | `(...codePoints)` | Converts each argument with ToNumber and encodes it in UTF-16 (may produce two units). The function's `length` is 1. Unlike `fromCharCode`, it does not reduce out-of-range values. | `RangeError` if the number is not an integer, is less than 0 or greater than 0x10FFFF (includes NaN) | p.538–539 | — |
| `String.raw` | `(template, ...substitutions)` | Designed as a template literal tag function. Converts `template` to an object, reads its `raw` property and the length of that; a length less than or equal to 0 gives the empty string; otherwise it interleaves the raw pieces with the substitutions converted by ToString. Pieces left over beyond the substitutions stay unsubstituted. | — | p.539 | — |
| `String.prototype` | data property | Prototype; not writable, not enumerable, not configurable. | — | p.539 | — |

### 2.2 General prototype rules

- `String.prototype` is itself a String exotic object, with `[[StringData]]` equal to the empty string, `length` 0 (not writable, not enumerable, not configurable) and prototype `Object.prototype` (Spec p.539).
- Unless stated otherwise, the methods require `this` to be a string or an object with `[[StringData]]`; however most are marked as intentionally generic and convert `this` by ToString (Spec p.539–540). `valueOf` and `toString` are **not** generic (see 2.7).
- Typical parameter conversions are `ToIntegerOrInfinity` (positions), `ToString` (texts), `ToLength` (padding sizes) and `ToUint32` (limits) [inference from the algorithms described on p.540–553].
- String instances have `length` (number of code units, immutable: not writable, not enumerable, not configurable) and enumerable properties with index names (Spec p.557). Assigning to `length` does not change the string [extrapolation: in strict mode the assignment would throw `TypeError`].
- `String.prototype.constructor` is `%String%` (Spec p.541).

### 2.3 Character access and length

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `at` | `at(index)` | ToIntegerOrInfinity on the index; negative counts from the end (`len + index`). Outside `[0, len)` returns `undefined`. Returns a string of one code unit. | — | p.540 | — |
| `charAt` | `charAt(pos)` | Outside the range returns the empty string (not `undefined`). Result is a primitive. Equivalent to `substring(pos, pos+1)` when `pos` is an integer. | — | p.540 | — |
| `charCodeAt` | `charCodeAt(pos)` | Returns the code unit value (0 to 65535); outside the range returns `NaN`. | — | p.540 | — |
| `codePointAt` | `codePointAt(pos)` | Returns the code point (up to 0x10FFFF) that starts at `pos`; if no valid surrogate pair starts there, returns the lone unit; outside the range returns `undefined`. | — | p.541 | — |
| `concat` | `concat(...args)` | Converts `this` and each argument by ToString and concatenates; returns a primitive. The function's `length` is 1. | — | p.541 | — |
| `length` (instance) | property | Number of code units; immutable. | — | p.557 | — |

Quick-lookup trap: for an invalid position, `at` and `codePointAt` return `undefined`, `charAt` returns `""` and `charCodeAt` returns `NaN` [inference by comparison, Spec p.540–541].

### 2.4 Search and comparison

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `includes` | `includes(searchString [, position])` | Returns a boolean; `position` defaults to 0 and is clamped to `[0, len]`. | `TypeError` if `searchString` is a RegExp (per IsRegExp) | p.542 | — |
| `indexOf` | `indexOf(searchString [, position])` | Converts `searchString` by ToString (a RegExp is accepted and becomes text); `position` clamped to `[0, len]`; returns the smallest index greater than or equal to `position`, or -1. | — | p.542–543 | — |
| `lastIndexOf` | `lastIndexOf(searchString [, position])` | Converts `position` with ToNumber; `NaN` (including absent) becomes +Infinity, that is, it searches everything; if the string is shorter than the search it returns -1; clamps `position` to `[0, len − searchLength]`; returns the largest index less than or equal to `position`, or -1. | — | p.543 | — |
| `startsWith` | `startsWith(searchString [, position])` | `position` defaults to 0, clamped to `[0, len]`; an empty search gives `true`; if start + length goes past the end it gives `false`. | `TypeError` if `searchString` is a RegExp | p.552–553 | — |
| `endsWith` | `endsWith(searchString [, endPosition])` | `endPosition` defaults to `len`, clamped to `[0, len]`; an empty search gives `true`; compares the same-sized segment ending at `endPosition`. | `TypeError` if `searchString` is a RegExp | p.541–542 | — |
| `localeCompare` | `localeCompare(that [, reserved1 [, reserved2]])` | Compares `this` and `that` (both by ToString) according to the environment's locale rule; returns a non-`NaN` number (negative, zero or positive). Requires a consistent total order and that strings canonically equivalent in Unicode give 0; it is recommended not to honor compatibility equivalence. With ECMA-402 present, it follows that specification. It does not work directly as a `sort` comparator without adaptation (it needs a two-argument function). | — | p.544–545 | [HOST] |

Shared error note: the Spec explains that the `TypeError` for RegExp in `includes`, `startsWith` and `endsWith` exists to leave room for future extensions (Spec p.542). See also `Annex F`, where `localeCompare` started treating canonical equivalents as identical (Spec p.869) [VERSION-DEPENDENT: ES2015].

### 2.5 Slicing, padding, repetition and splitting

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `slice` | `slice(start, end)` | Negatives count from the end (`len + value`, minimum 0); positives clamped to `len`; undefined `end` is `len`; if start is greater than or equal to end, empty string. | — | p.551 | — |
| `substring` | `substring(start, end)` | `NaN` or negative becomes 0; greater than `len` becomes `len`; if `start > end`, it **swaps** the two; undefined `end` is `len`. Does not treat negatives as a count from the end. | — | p.553 | — |
| `padStart` | `padStart(maxLength [, fillString])` | `maxLength` by ToLength; if less than or equal to the current length returns the original string; undefined `fillString` is a space; empty padding returns the original; repeats and **truncates** the padding until complete. Inserts at the start. | — | p.546–547 | — |
| `padEnd` | `padEnd(maxLength [, fillString])` | Same as `padStart`, but inserts at the end. | — | p.546–547 | — |
| `repeat` | `repeat(count)` | `count` by ToIntegerOrInfinity; 0 gives the empty string; result is a primitive. `NaN` becomes 0 and returns empty [extrapolation]. | `RangeError` if negative or +Infinity | p.547–548 | — |
| `split` | `split(separator, limit)` | If `separator` is an object with `Symbol.split`, delegates. Undefined `limit` is 2^32 − 1, otherwise ToUint32. `limit` 0 gives an empty array; undefined `separator` gives an array with the whole string; an empty separator generates one entry per **code unit** (breaks surrogate pairs); empty `this` with a non-empty separator gives `[""]`; the general case cuts at non-overlapping occurrences and stops on reaching `limit` elements. | — | p.551–552 | — |

Minimal example (direct consequence of the rules): `"5".padStart(3, "0")` gives `"005"` (Spec p.547). `"a,b".split(",", 1)` gives only `["a"]` (Spec p.551–552).

### 2.6 Methods that delegate to RegExp (match, replace, search...)

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `match` | `match(regexp)` | If `regexp` is an object with a `Symbol.match` method, delegates to it. Otherwise converts `this` to a string, creates a RegExp (no flags) from the argument and calls its `Symbol.match`. Without the `g` flag, returns only the first match (`Symbol.match` behavior). | — | p.545 | — |
| `matchAll` | `matchAll(regexp)` | Returns an **iterator** of results (each is an array with the segment and the captures); if it never matches, produces nothing. If `regexp` is an object and IsRegExp is true, reads `flags` and requires `g`. Delegates to `Symbol.matchAll` if it exists; otherwise creates a RegExp with `g`. | `TypeError` if the RegExp has no `g` | p.546 | — |
| `replace` | `replace(searchValue, replaceValue)` | An object with `Symbol.replace` receives the delegation (path of RegExps). With a search string, replaces only the **first** occurrence; if not found, returns the original. A function `replaceValue` receives `(matchedSegment, position, originalString)` and the return goes through ToString; otherwise the text goes through `GetSubstitution`. | — | p.548 | — |
| `replaceAll` | `replaceAll(searchValue, replaceValue)` | If `searchValue` is an object and IsRegExp, reads `flags` and requires `g`; then delegates to `Symbol.replace`. With a search string, replaces **all** non-overlapping occurrences from left to right, advancing at least 1; an empty search matches between all code units, including start and end. | `TypeError` if the RegExp has no `g` | p.550 | — |
| `search` | `search(regexp)` | Delegates to `Symbol.search`; otherwise creates a RegExp and calls its `Symbol.search`. Returns an index or -1. | — | p.550 | — |

**Replacement text (`GetSubstitution`)** used by `replace`/`replaceAll` when the second argument is not a function (Spec p.548–550):

| Sequence | Effect | Page |
|---|---|---|
| `$$` | a literal `$` | p.549 |
| `` $` `` | the part of the string before the match | p.549 |
| `$&` | the matched segment | p.549 |
| `$'` | the part after the match | p.549 |
| `$n`, `$nn` | capture number 1 to 99; with two digits and an index above the total, it is one digit plus a literal digit; 0 or an index above the total leaves the text literal; an `undefined` capture becomes empty | p.549 |
| `$<name>` | named group; only valid if named groups exist and there is a `>`; `undefined` becomes empty; otherwise `$<` stays literal | p.549 |
| other `$` | literal | p.549 |

Trap: with a **string** search there are no captures, so `$1` and `$<name>` remain literal [inference from the calls with an empty list, Spec p.548–549]. Minimal example: `"abc".replace("b", "[$&]")` gives `"a[b]c"` (Spec p.549).

### 2.7 Case, normalization, trim and Unicode well-formedness

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `toLowerCase` | `toLowerCase()` | Reads the string as UTF-16 code points and applies the standard Unicode conversion, using locale-insensitive mappings. The result length may change; `s.toUpperCase().toLowerCase()` is not necessarily `s.toLowerCase()`. | — | p.554 | — |
| `toUpperCase` | `toUpperCase()` | Same, using the uppercase algorithm. Example: `"ß".toUpperCase()` gives `"SS"` [extrapolation]. | — | p.555 | — |
| `toLocaleLowerCase`, `toLocaleUpperCase` | `([reserved1 [, reserved2]])` | With ECMA-402 they follow that specification; without it they behave like the locale-less versions, but are meant to respect the environment's locale; they differ in a few cases (Turkish). | — | p.553–554 | [HOST] |
| `normalize` | `normalize([form])` | `form` defaults to `"NFC"`; accepts only `"NFC"`, `"NFD"`, `"NFKC"`, `"NFKD"`. | `RangeError` for any other value | p.546 | — |
| `trim`, `trimStart`, `trimEnd` | `()` | Remove whitespace at the start and end, only at the start, only at the end (via `TrimString`). "Whitespace" is the union of `WhiteSpace` and `LineTerminator`. Generic. Example: `"  x ".trimEnd()` gives `"  x"`. | `TypeError` if `this` is `null`/`undefined` | p.555–556 | — |
| `isWellFormed` | `isWellFormed()` | Returns whether the string contains no lone surrogates, via `IsStringWellFormedUnicode`. | — | p.543 | version not stated in the sources |
| `toWellFormed` | `toWellFormed()` | Returns a copy in which every lone surrogate becomes U+FFFD; valid pairs and already well-formed strings stay the same. Example: `"a\uD800b".toWellFormed()` gives `"a" + U+FFFD + "b"` [extrapolation]. | `TypeError` if `this` is `null`/`undefined` | p.555 | version not stated in the sources |
| `valueOf` | `valueOf()` | Returns `ThisStringValue(this)`: the string, or the value of the `[[StringData]]` slot. **Not generic.** | `TypeError` if `this` is neither a string nor a String object | p.556 | — |
| `toString` | `toString()` | Same behavior via `ThisStringValue`. | `TypeError` if `this` is neither a string nor a String object [inference] | p.554 | — |

Other case rules in `Annex F`: case conversion started operating on code points (affecting only the Deseret block) and `trim` started recognizing whitespace outside the basic plane (Spec p.869) [VERSION-DEPENDENT: ES2015]. Also in Annex F, the Unicode update removed U+180E from the whitespace category (Spec p.867) [VERSION-DEPENDENT: ES2016, and ES2017 starts requiring the latest Unicode version].

### 2.8 String iterator

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `[Symbol.iterator]` | `[Symbol.iterator]()` | Iterates by **code points**, returning each as a string (a surrogate pair comes along as one element). The function's `name` is `"[Symbol.iterator]"`. Example: `[..."a😀"]` has 2 elements [extrapolation]. | `TypeError` if `this` is `null`/`undefined` | p.557 | — |
| `%StringIteratorPrototype%.next` | `next()` | Resumes the internal generator. The iterator's prototype is `%Iterator.prototype%`; `@@toStringTag` is `"String Iterator"` (not writable, not enumerable, configurable). | — | p.557–558 | — |

### 2.9 Legacy Annex B methods [DATED]

Annex B is normative for browsers, but the Spec itself says to prefer modern alternatives (Spec p.843, p.853–854).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `substr` | `substr(start, length)` | Substring by position and **length**. Negative `start` counts from the end (`max(len + start, 0)`; -Infinity becomes 0; positive clamped to `len`). Undefined `length` uses the rest; otherwise clamped to `[0, len]`. Result is a primitive; generic. | `TypeError` if `this` is `null`/`undefined` | p.851 | [DATED] |
| `anchor` | `anchor(name)` | Wraps the text in `<a name="...">...</a>`. Double quotes in the value become `&quot;`; `<`, `>` and `&` are **not** escaped, so it is not safe for untrusted HTML [inference]. | `TypeError` if `this` is `null`/`undefined` | p.851–852 | [DATED] |
| `big`, `blink`, `bold`, `fixed` | `()` | Wrap in `<big>`, `<blink>`, `<b>`, `<tt>`. | same | p.852 | [DATED] |
| `fontcolor`, `fontsize` | `(colour)`, `(size)` | Wrap in `<font color="...">` and `<font size="...">`. | same | p.852 | [DATED] |
| `italics`, `link`, `small`, `strike`, `sub`, `sup` | `()`; `link(url)` | Wrap in `<i>`, `<a href="...">`, `<small>`, `<strike>`, `<sub>`, `<sup>`. | same | p.853 | [DATED] |
| `trimLeft`, `trimRight` | properties | Alternative names: the initial value is the same function object as `trimStart` and `trimEnd`. Prefer the new names. | — | p.853–854 | [DATED] |

## 3. RegExp

A RegExp object holds a regular expression and its flags; the form and functionality are modeled on Perl 5 regular expressions (Spec p.558). If the pattern (text) cannot be parsed by the grammar, a `SyntaxError` occurs (Spec p.558, p.598).

### 3.1 Flags

Valid flags: `d g i m s u v y`. Any other letter, or a repetition, is a `SyntaxError`; `u` and `v` together as well (Spec p.598–599). Each flag has a getter on the prototype, with no setter.

| Flag | Getter | Effect | Page | Mark |
|---|---|---|---|---|
| `d` | `hasIndices` | The `exec` result gains the `indices` array with `[start, end]` pairs per capture (and its own `groups` when there are names); groups that did not participate are `undefined`. | p.611 | — |
| `g` | `global` | Finds all matches; `lastIndex` is used and updated. | p.603, p.610 | — |
| `i` | `ignoreCase` | Ignores case via `Canonicalize`. With `u`/`v` it uses Unicode simple case folding; without them it uses `toUppercase` (if the result does not have length 1, or if it maps non-ASCII to ASCII, the character stays). | p.586 | — |
| `m` | `multiline` | `^` and `$` also match at line boundaries. | p.578–579 | — |
| `s` | `dotAll` | The `.` also matches line terminators. | p.583 | — |
| `u` | `unicode` | Unicode mode: the pattern and the input are read by code points; enables `\p{...}` and `\u{...}`. | p.571 | — |
| `v` | `unicodeSets` | Extended Unicode mode: set operations in classes, `\q{...}` and properties of strings. Incompatible with `u`. | p.562–563, p.598–599 | version not stated in the sources |
| `y` | `sticky` | The match is only valid exactly at `lastIndex`; on failure, resets `lastIndex` and returns `null` without advancing. | p.610 | — |

Getter details (Spec p.602–603): `flags` requires `this` to be an object and builds the string by reading the properties through `Get` in the order `hasIndices`, `global`, `ignoreCase`, `multiline`, `dotAll`, `unicode`, `unicodeSets`, `sticky` (letters `d g i m s u v y`). The individual getters throw `TypeError` if `this` is not an object or if it is an object without a flags slot other than `%RegExp.prototype%`; on `%RegExp.prototype%` itself they return `undefined`.

Observable differences of `i` (Spec p.587–588): simple case folding never maps `ß` to `ss`, but may map from outside Basic Latin to inside it; so `/[a-z]/ui` matches U+017F (long s) and U+212A (Kelvin sign), but `/[a-z]/i` does not. In classes, the case of the range endpoints matters: `/[E-F]/i` matches only E, F, e, f; `/[E-f]/i` matches all basic Latin letters and also the characters `[`, `\`, `]`, `^`, `_` and the backtick.

### 3.2 Pattern syntax

The grammar parameters are `UnicodeMode`, `UnicodeSetsMode` and `NamedCaptureGroups` (Spec p.558).

| Construct | Meaning and edge cases | Page | Mark |
|---|---|---|---|
| `a\|b` | Disjunction: tries the left alternative; if it fails, the right one. Captures of a skipped alternative are `undefined`. `/a\|ab/.exec("abc")` matches `"a"`. | p.573–574 | — |
| `^`, `$` | Start and end of input; with `m`, also after/before a line terminator. With `y`, `^` is still only the start of the input (or of a line with `m`). | p.578–579 | — |
| `\b`, `\B` | Word boundary / non-boundary. Outside the input limits, that side counts as non-word. | p.579, p.581–582 | — |
| `(?=...)`, `(?!...)` | Positive and negative lookahead; zero width. **No backtracking into** the lookahead. Captures inside a negative lookahead are never visible outside. Example: `/(?=(a+))/.exec("baaabac")` gives `["","aaa"]`. | p.579–581 | — |
| `(?<=...)`, `(?<!...)` | Positive and negative lookbehind; the interior is matched **backwards** (right to left), which inverts the evaluation order of terms and captures. | p.574, p.581 | — |
| `*`, `+`, `?`, `{n}`, `{n,}`, `{n,m}` | Quantifiers: 0..∞, 1..∞, 0..1, n, n..∞, n..m. A `?` suffix makes them lazy. `{n,m}` with n greater than m is an error. | p.558–559, p.575–576, p.582 | — |
| Repetition and captures | Captures inside a repeated group are reset on each iteration: `/(z)((a+)?(b+)?(c))*/.exec("zaacbbbcac")` gives `["zaacbbbcac","z","ac","a",undefined,"c"]`. After the minimum is reached, an iteration that matches empty is rejected (avoids an infinite loop). | p.575, p.577 | — |
| `.` | Any character; without `s`, excludes line terminators. | p.583 | — |
| `[...]`, `[^...]` | Class and negated class. Range `a-z`; `-` is literal at the start, at the end, as a range endpoint or right after a range. Inside a class, `\b` is backspace. A range with a class endpoint (`\w`) or with a start greater than the end is an error. | p.561–562, p.587–589 | — |
| `\d \D \s \S \w \W` | Digits `0-9`; whitespace = `WhiteSpace` + `LineTerminator`; `\w` = ASCII `[A-Za-z0-9_]` (with `i` and Unicode mode, plus characters that canonicalize to that set); uppercase ones are complements. | p.589, p.592 | — |
| `\p{...}`, `\P{...}` | Unicode property and complement; only in `u` or `v` mode. See 3.3. | p.561, p.589–590 | — |
| `( ... )` | Capture group; records in `cap[n]`. `(?:...)` does not capture. | p.583–584 | — |
| `(?<name>...)` | Named group; becomes a property of `groups`. Repeated names are only allowed in different alternatives of a disjunction; otherwise `SyntaxError`. | p.559–560, p.563 | — |
| `(?i:...)`, `(?-i:...)` | Inline modifiers; allowed letters `i`, `m`, `s`; a repeated letter, the same letter in both sets or the empty form `(?-:...)` are `SyntaxError`. | p.559, p.563–564, p.584, p.587 | version not stated in the sources |
| `\N` | Numeric backreference; if the group is still `undefined`, it **matches empty** (success). N greater than the total number of groups is a `SyntaxError` in Unicode mode (see 3.8 for legacy mode). | p.564, p.584 | — |
| `\k<name>` | Reference to a named group; with duplicate names, uses the one that captured. A nonexistent name is a `SyntaxError`. | p.564, p.585–586 | — |
| `\n \t \v \f \r \0 \cX \xHH \uHHHH \u{...}` | Character escapes (`\u{...}` only in Unicode mode; `\0` only if not followed by a digit; `\cX` uses the letter modulo 32). In Unicode mode, `IdentityEscape` accepts only `SyntaxCharacter` or `/`. | p.559–560, p.567 | — |
| Classes in `v` mode | Union, intersection `&&`, subtraction `--`, nested classes `[...]` and `\q{abc\|d}` (disjunction of strings). Reserved double pairs (`&&`, `!!`, `##` etc.) cannot be literals. `\P{...}` or `[^...]` whose content can match strings is a `SyntaxError`. Example: `/[\p{L}--[a-z]]/v` [extrapolation]. | p.562–563, p.565, p.590–593 | version not stated in the sources |

`SyntaxCharacter`: `^ $ \ . * + ? ( ) [ ] { } |` (Spec p.559). A pattern with 2^32 − 1 or more capture groups is also an error (Spec p.563).

**BMP vs Unicode** (Spec p.571): without `u`/`v` the pattern is "BMP" and the string is treated as a sequence of 16-bit units (an emoji counts as two characters); with `u`/`v` it counts as one. Spec example: U+1D11E becomes two elements (0xD834, 0xDD1E) in BMP and a single one in Unicode.

### 3.3 Unicode properties (`\p`)

Rules (Spec p.564–565, p.590, p.593, p.597):
- Only names and aliases from the Spec tables are accepted; any other is a `SyntaxError`. The comparison is case-sensitive and does not ignore spaces, `-` or `_`. The UAX44 `Is` prefix is not supported.
- `\p{Name=Value}` form: `Name` must be non-binary: `General_Category` (`gc`), `Script` (`sc`) or `Script_Extensions` (`scx`) (Table 64, p.594). The value must exist in `PropertyValueAliases.txt`. Examples: `scx` is valid, `Scx` is not; `Xpeo` and `Old_Persian` are valid, `Old Persian` is not.
- "Lone" form `\p{X}`: tries first as a `General_Category` value (for example `\p{Lu}`); otherwise as a binary property (Table 65) or binary property of strings (Table 66).
- Binary ones (Table 65, p.594–596), among others: `ASCII`, `ASCII_Hex_Digit`, `Alphabetic`, `Any`, `Assigned`, `Bidi_Control`, `Bidi_Mirrored`, `Case_Ignorable`, `Cased`, the `Changes_When_*`, `Dash`, `Default_Ignorable_Code_Point`, `Deprecated`, `Diacritic`, `Emoji` and variants (`Emoji_Component`, `Emoji_Modifier`, `Emoji_Modifier_Base`, `Emoji_Presentation`, `Extended_Pictographic`), `Extender`, `Grapheme_Base`, `Grapheme_Extend`, `Hex_Digit`, `ID_Continue`, `ID_Start`, `Ideographic`, `Join_Control`, `Lowercase`, `Math`, `Noncharacter_Code_Point`, `Pattern_Syntax`, `Pattern_White_Space`, `Quotation_Mark`, `Regional_Indicator`, `Sentence_Terminal`, `Soft_Dotted`, `Terminal_Punctuation`, `Unified_Ideograph`, `Uppercase`, `Variation_Selector`, `White_Space`, `XID_Continue`, `XID_Start`.
- Binary properties of strings (Table 66, p.596), **only in `v` mode**: `Basic_Emoji`, `Emoji_Keycap_Sequence`, `RGI_Emoji_Modifier_Sequence`, `RGI_Emoji_Flag_Sequence`, `RGI_Emoji_Tag_Sequence`, `RGI_Emoji_ZWJ_Sequence`, `RGI_Emoji`. In `u` mode they are a `SyntaxError`; `\P{...}` with them as well.
- With `v` and `i` together, the set goes through simple case folding (Spec p.590, p.591).

### 3.4 Constructor and static functions

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `RegExp` | `RegExp(pattern, flags)` / `new RegExp(...)` | Can be called with or without `new`. Without `new`, if `pattern` is regexp-like, `flags` is `undefined` and `pattern.constructor` is `RegExp` itself, it returns the **same object** `pattern`. If `pattern` is a RegExp, it uses its `source` and, if `flags` is `undefined`, its original flags; if it is regexp-like without a slot, it reads `source` and `flags` by property. `pattern` and `flags` `undefined` become the empty string. In a string literal, `\` must be written `\\`. Can be extended; subclass calls `super`. With a RegExp and different `flags`, creates a new instance with the flags replaced. | `SyntaxError` for invalid pattern, invalid or repeated flag, `u` with `v`; `TypeError` if `lastIndex` is not writable | p.598–600, p.869 | [VERSION-DEPENDENT] (Annex F: in ES2015 it stopped being `TypeError`) |
| `RegExp.escape` | `RegExp.escape(S)` | Escapes a **string** for literal use inside a pattern. No coercion: a non-String throws an error. A first character that is a digit or ASCII letter becomes `\xHH`. `SyntaxCharacter` and `/` get a `\`; tab, LF, VT, FF, CR become `\t \n \v \f \r`; the characters `,-=<>#&!%:;@~'` plus double quote and backtick, whitespace, line terminators and lone surrogates become `\xHH` or `\uHHHH`; the rest stays the same. Not to be confused with `EscapeRegExpPattern`, which escapes a pattern to become `source`. | `TypeError` if `S` is not a String | p.600–601 | version not stated in the sources |
| `RegExp.prototype` | property | Not writable, not enumerable, not configurable. The prototype **is not** a RegExp instance; it inherits `valueOf` from Object. | — | p.601 | — |
| `RegExp[Symbol.species]` | getter | Returns `this`; `name` is `"get [Symbol.species]"`. Lets subclasses change the constructor used internally. | — | p.601 | — |

### 3.5 Prototype: exec, test, flags, source, toString

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `exec` | `exec(string)` | Converts by ToString and calls the internal algorithm; returns a result array or `null`. See 3.7. | `TypeError` if `this` has no `[[RegExpMatcher]]` | p.602, p.609–611 | — |
| `test` | `test(S)` | Does `RegExpExec`; returns `false` if `null`, otherwise `true`. With `g` or `y` it uses and updates `lastIndex`, so repeated calls on the same object can alternate `true`/`false` [inference]. | `TypeError` if `this` is not an object | p.608–610 | — |
| `source` | getter | Returns the pattern with `/` and line terminators escaped (`EscapeRegExpPattern`), so that `"/"+S+"/"+F` is an equivalent literal; an empty pattern becomes `"(?:)"`. On `%RegExp.prototype%` returns `"(?:)"`. | `TypeError` if `this` is not an object or is an object without a slot other than the prototype | p.606 | — |
| `flags` | getter | See 3.1. | `TypeError` if `this` is not an object | p.602 | — |
| `toString` | `toString()` | Returns `"/" + source + "/" + flags`, reading both by `Get`. | `TypeError` if `this` is not an object | p.609 | — |
| `constructor` | property | `%RegExp%`. | — | p.601 | — |

### 3.6 Symbol.match, matchAll, replace, search, split methods

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `[Symbol.match]` | `(string)` | Reads `flags`. Without `g`, returns the `RegExpExec` result. With `g`, resets `lastIndex` and collects only `result[0]` of each match in an array (`null` if none); on an empty match advances `lastIndex` (by code point with `u`/`v`). A truthy value in `Symbol.match` is what `IsRegExp` uses to recognize "regexp objects". | `TypeError` if `this` is not an object | p.603–604 | — |
| `[Symbol.matchAll]` | `(string)` | Creates a **new** regexp (`new C(R, flags)`, with `SpeciesConstructor`) and copies `lastIndex`; returns an iterator (`CreateRegExpStringIterator`). Because it clones, the original's `lastIndex` does not change [inference]. | `TypeError` if `this` is not an object | p.604 | — |
| `[Symbol.replace]` | `(string, replaceValue)` | A callable `replaceValue` uses functional mode: calls `(matched, ...captures, position, string[, groups])`; `groups` is only passed if not `undefined`; return by ToString. Otherwise `ToString` and `GetSubstitution`. With `g`, resets `lastIndex` and advances on an empty match. If the position goes backwards (a misbehaving subclass), the replacement is ignored. | `TypeError` if `this` is not an object | p.604–605 | — |
| `[Symbol.search]` | `(string)` | Saves `lastIndex`, forces 0, runs and restores; returns -1 or `result.index`. `lastIndex` and `global` are ignored. | `TypeError` if `this` is not an object | p.605–606 | — |
| `[Symbol.split]` | `(string, limit)` | Uses `SpeciesConstructor` and forces the `y` flag on a new regexp. Separators do not enter the result; captures (including `undefined`) do. An empty match is not valid at the start, at the end or right after the previous separator; with a regexp that matches empty the string is split by code units. Empty input: `[]` if the regexp matches empty, otherwise `[""]`. `limit` by ToUint32 (0 gives `[]`, default 2^32 − 1). Ignores the original's `global` and `sticky`. `/a*?/[Symbol.split]("ab")` gives `["a","b"]`. | `TypeError` if `this` is not an object | p.607–608 | — |

All have a `name` in the format `"[Symbol.xxx]"` (p.604–608).

### 3.7 lastIndex and the exec algorithm

- `lastIndex`: index where the next search starts; own property `{writable: true, enumerable: false, configurable: false}`; it is reset (to 0) on creation via `Set(..., true)` (Spec p.598, p.613).
- **Without `g` and without `y`, `lastIndex` is treated as 0** and is not updated. With `g` or `y`: success writes `lastIndex = end` (in code units); failure resets `lastIndex` and returns `null`; `lastIndex` greater than the input length also resets and returns `null` (Spec p.610).
- Without `y`, the search advances position by position with `AdvanceStringIndex` (1 unit, or one code point in Unicode mode). With `y`, failure at the starting position ends without advancing (Spec p.610–611).
- `RegExpExec` first looks up the object's `exec` property; if callable, calls it and requires an object or `null`; otherwise uses the internal algorithm (requires `[[RegExpMatcher]]`) (Spec p.609). The Spec says this preserves compatibility with code from earlier editions [VERSION-DEPENDENT: edition not numbered in the source].
- Success result: array with `length = n + 1`, properties `index` (start), `input`, `0` (matched segment), `1..n` (captures, `undefined` for non-participants) and `groups` (object with `null` prototype holding named groups, or `undefined` if there are no names). With `d`, also `indices` (Spec p.610–611).
- In Unicode mode, internal indices are in code points and are converted back to code units (`GetStringIndex`) (Spec p.610–611).

**matchAll iterator** (Spec p.613–614): `%RegExpStringIteratorPrototype%` inherits from `%Iterator.prototype%`; `next()` requires an object with the slots (otherwise `TypeError`); once exhausted it returns `{value: undefined, done: true}`; if the regexp is not global, it returns the single match and finishes; if it is global, it advances on an empty match. `@@toStringTag` is `"RegExp String Iterator"`. Example: `[..."a1b2".matchAll(/\d/g)]` gives two results [extrapolation].

Instances inherit from the prototype and have the slots `[[OriginalSource]]`, `[[OriginalFlags]]`, `[[RegExpRecord]]`, `[[RegExpMatcher]]` (Spec p.613). Before ES2015, `source`, `global`, `ignoreCase`, `multiline` were data properties of the instances; today they are accessors on the prototype (Spec p.613, p.869) [VERSION-DEPENDENT: ES2015].

### 3.8 Annex B and legacy

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| Legacy pattern grammar | without `u`/`v` | A lookahead may receive a quantifier (a lookbehind may not). Lone `]`, `{` and `}` are literals, but `{n}`/`{n,m}` with no target is an error. A `\N` reference is only valid if N is at most the number of groups; otherwise it becomes a legacy octal escape. `\c` without a letter matches the backslash itself. `\k` is only a named-group escape if the pattern has names. In classes, `[\d-x]` treats `-` as literal; in Unicode mode this is an error. `[z-a]` is still an error. | `SyntaxError` on a quantifier with no target | p.844–849 | [DATED] |
| `compile` | `RegExp.prototype.compile(pattern, flags)` | Reinitializes the RegExp itself with a new pattern and flags; if `pattern` is a RegExp, uses its source and original flags. | `TypeError` if `this` has no `[[RegExpMatcher]]` or if `pattern` is a RegExp and `flags` is not `undefined` | p.855 | [DATED] |

## 4. Array

### 4.1 Constructor and statics

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Array` | `Array(...args)` / `new Array(...args)` | Calling with or without `new` gives the same. 0 arguments: empty array. 1 **non-Number** argument: one-element array. 1 Number argument: it is the length (array with holes, no elements). 2 or more: array with those elements. `new Array(3)` is not `[3]`. The prototype comes from `NewTarget` (subclasses). The constructor's `length` is 1. | `RangeError` if the single Number is not a uint32 integer (1.5, -1, 2^32) | p.615–616 | — |
| `Array.from` | `from(items [, mapper [, thisArg]])` | Factory for an iterable or array-like. `mapper` receives only `(value, index)`. If `items` has `Symbol.iterator`, iterates; otherwise uses `ToObject` and `length`. Uses `new C()` if `this` is a constructor (generic). If `mapper` or the definition throws during iteration, the iterator is closed. Example: `Array.from({length: 3}, (_, i) => i * 2)` gives `[0,2,4]`. | `TypeError` if `mapper` is not callable; `TypeError` on reaching 2^53 − 1 elements; `Array.from(null)` throws [inference] | p.616–618 | — |
| `Array.fromAsync` | `fromAsync(items [, mapper [, thisArg]])` | Asynchronous version (async function, returns a promise). Prefers `Symbol.asyncIterator`, then an adapted `Symbol.iterator`, then array-like. Each `next()` result and each mapped value is awaited; on the array-like route each value read and the mapper result are awaited. Failures close the iterator. | `TypeError` (as a promise rejection [inference]) for an invalid `mapper`, a `next()` result that is not an object or 2^53 − 1 elements | p.617–618 | version not stated in the sources |
| `Array.isArray` | `isArray(arg)` | Returns `IsArray(arg)`. | may throw for a revoked Proxy [extrapolation] | p.618 | — |
| `Array.of` | `of(...items)` | Creates an array with the arguments; `Array.of(7)` gives `[7]`. Uses `new C(len)` if `this` is a constructor. | — | p.618 | — |
| `Array.prototype` | property | Not writable, not enumerable, not configurable. | — | p.618 | — |
| `Array[Symbol.species]` | getter | Returns `this`; `name` `"get [Symbol.species]"`. Subclasses redefine it to change the constructor used by the deriving methods. | — | p.619 | — |

`Array.prototype` is itself an Array exotic object with `length` +0 (writable, not enumerable, not configurable), for compatibility with pre-ES2015 code (Spec p.619). `Array.prototype.constructor` is `%Array%` (Spec p.620). There is no `Array.prototype.groupBy` in the Spec notes: grouping is done by `Object.groupBy` (object with no prototype holding arrays, Spec p.464) and `Map.groupBy` (see section 7).

### 4.2 Prototype

**Mutators (change the array itself)**

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `copyWithin` | `copyWithin(target, start [, end])` | Copies a segment of the array itself to another position without changing `length`; negatives count from the end; limits in `[0, len]`; handles overlap; deletes the destination when the source is a hole. Returns the object itself. | — | p.620–621 | — |
| `fill` | `fill(value [, start [, end]])` | Writes the same value into the range; `start` defaults to 0, `end` defaults to `length`; negatives from the end. Uses strict `Set`. Returns the object. | a failed `Set` (e.g.: frozen object) throws [inference] | p.622–623 | — |
| `pop` | `pop()` | Removes and returns the last; empty sets `length` 0 and returns `undefined`. | — | p.631 | — |
| `push` | `push(...items)` | Appends to the end and **returns the new length**; the function's `length` is 1. | `TypeError` if `len + n` exceeds 2^53 − 1 (before changing anything) | p.631–632 | — |
| `reverse` | `reverse()` | Reverses in place, handling holes (moves the value and deletes the other side); returns the object. | — | p.634 | — |
| `shift` | `shift()` | Removes and returns the first, shifting the rest; empty returns `undefined`. | — | p.634–635 | — |
| `unshift` | `unshift(...items)` | Inserts at the start preserving order; returns the new length; the function's `length` is 1. | `TypeError` if it exceeds 2^53 − 1 | p.642 | — |
| `sort` | `sort(comparator)` | Sorts in place and returns the object; **stable**. Collects existing values, sorts, rewrites from index 0 and deletes the rest (preserves the number of holes). `undefined` goes to the end, then the holes, without calling the comparator. **Without a comparator, compares as strings** (10 comes before 9). With a comparator, the return goes through ToNumber and `NaN` becomes 0. An inconsistent comparator leaves the order implementation-defined; if the comparator throws, sorting stops and the error propagates. | `TypeError` if `comparator` is neither `undefined` nor callable (checked before anything) | p.636–638 | — |
| `splice` | `splice(start, deleteCount, ...items)` | Removes `deleteCount` and inserts `items`; returns an array (via species) with the removed ones. Without `start`: nothing removed; `start` without `deleteCount`: removes to the end; `deleteCount` clamped to `[0, len − start]`; negative `start` counts from the end. Sets `length` explicitly. | `TypeError` if the new size exceeds 2^53 − 1 | p.638–640 | — |

**Accessors and search (do not change)**

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `at` | `at(index)` | Negative counts from the end; outside `[0, len)` returns `undefined`. | — | p.619 | — |
| `concat` | `concat(...args)` | New array (species) with the elements of `this` and of each spreadable argument. Spreads if the argument is an object and (`Symbol.isConcatSpreadable` is true, or, if undefined, `IsArray`). Holes remain holes; sets `length` at the end. The function's `length` is 1. `[1].concat([2,3], 4)` gives `[1,2,3,4]`. | `TypeError` if the total exceeds 2^53 − 1 | p.619–620 | — |
| `includes` | `includes(searchElement [, fromIndex])` | Uses **SameValueZero** (finds `NaN`); negative `fromIndex` counts from the end; computed index ≤ 0 searches everything; `fromIndex ≥ len` or empty gives `false`. **Does not skip holes** (reads them as `undefined`). | — | p.628 | — |
| `indexOf` | `indexOf(searchElement [, fromIndex])` | Uses strict equality (`NaN` is never found); returns the smallest index or -1; skips holes; `fromIndex ≥ len` gives -1. | — | p.628–629 | — |
| `lastIndexOf` | `lastIndexOf(searchElement [, fromIndex])` | Searches back to front; `fromIndex` defaults to `len − 1`; explicit `undefined` becomes 0 (distinguishes present from absent); computed index less than 0 gives -1. | — | p.630 | — |
| `join` | `join([separator])` | Separator `undefined` is `","`, otherwise ToString. `undefined`/`null` elements become empty. | — | p.629 | — |
| `slice` | `slice(start, end)` | Shallow copy of `[start, end)` via species; negatives from the end; preserves holes; sets `length`. | — | p.635 | — |
| `toString` | `toString()` | Gets `join`; if callable, calls it; otherwise uses `%Object.prototype.toString%`. | — | p.642 | — |
| `toLocaleString` | `toLocaleString([reserved1 [, reserved2]])` | Joins elements with a locale-dependent separator; `undefined`/`null` become empty; the others call the element's `toLocaleString`. With ECMA-402 it follows that specification. | — | p.640 | [HOST] |
| `entries`, `keys`, `values` | `()` | Create an Array Iterator (`[i, v]` pairs, indices, values). `Array.prototype[Symbol.iterator]` is the **same** function object as `values`. | — | p.621, p.629, p.643 | — |

**Iteration with callback**

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `every` | `every(callback [, thisArg])` | Calls `(value, index, object)` on present elements until one returns falsy (`false`); empty gives `true`. An omitted `thisArg` makes the callback's `this` `undefined`. | `TypeError` if `callback` is not callable | p.622 | — |
| `some` | `some(callback [, thisArg])` | Inverse: stops at the first truthy; empty gives `false`. | same | p.636 | — |
| `filter` | `filter(callback [, thisArg])` | New array (species, `ArraySpeciesCreate(O, 0)`) with only the approved ones; skips holes; compact result. | same | p.623–624 | — |
| `forEach` | `forEach(callback [, thisArg])` | Calls on present elements; returns `undefined`. | same | p.627 | — |
| `map` | `map(callback [, thisArg])` | New array of the same `length` via species; holes stay holes (the callback is not called for them). | same | p.630–631 | — |
| `reduce` | `reduce(callback [, initialValue])` | Callback `(accumulator, value, index, object)` with `this` `undefined`. Without `initialValue`, uses the first **present** element as the accumulator. Explicit `undefined` counts as a supplied initial value [inference]. | `TypeError` if the callback is invalid or if there are no elements (only holes) and no initial value | p.632–633 | — |
| `reduceRight` | `reduceRight(callback [, initialValue])` | Same logic from right to left. | same | p.633–634 | — |
| `find`, `findIndex` | `(predicate [, thisArg])` | First element / index (or `undefined` / -1) for which the predicate coerces to true. **Do not skip holes**: visit all indices reading with `Get` (holes arrive as `undefined`); deleted indices are still visited. Predicate receives `(value, index, object)`. Example: `[5,12,8].find(x => x > 9)` gives 12. | `TypeError` if the predicate is invalid | p.624–626 | — |
| `findLast`, `findLastIndex` | same | Same, in descending order. | same | p.624–626 | version not stated in the sources |
| `flat` | `flat([depth])` | Flattens sub-arrays; `depth` defaults to 1, by ToIntegerOrInfinity (negative becomes 0; Infinity flattens everything). Only flattens what `IsArray` approves; skips holes; species. | `TypeError` if it exceeds 2^53 − 1 | p.626–627 | version not stated in the sources |
| `flatMap` | `flatMap(mapperFunction [, thisArg])` | Maps with `(element, index, object)` and flattens **one level**. | `TypeError` if the mapper is not callable | p.626–627 | version not stated in the sources |

**Non-mutating versions** (new Array via `ArrayCreate`, **without species**; read holes as `undefined`)

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `toReversed` | `toReversed()` | Reversed copy. | — | p.640–641 | version not stated in the sources |
| `toSorted` | `toSorted(comparator)` | Validates the comparator **before** `ToObject`; sorts like `sort`, but with no holes in the result. | `TypeError` if the comparator is invalid | p.641 | version not stated in the sources |
| `toSpliced` | `toSpliced(start, skipCount, ...items)` | Non-mutating equivalent of `splice`; returns the resulting array (not the removed ones). | `TypeError` if the new size exceeds 2^53 − 1 | p.641–642 | version not stated in the sources |
| `with` | `with(index, value)` | Copy with the element replaced; negative counts from the end. Example: `[1,2,3].with(1, 9)` gives `[1,9,3]`. | `RangeError` if the index is outside `[0, len)` (unlike `at`) | p.643 | version not stated in the sources |

**`Array.prototype[Symbol.unscopables]`**: object with a null prototype with `true` for `at`, `copyWithin`, `entries`, `fill`, `find`, `findIndex`, `findLast`, `findLastIndex`, `flat`, `flatMap`, `includes`, `keys`, `toReversed`, `toSorted`, `toSpliced`, `values`. Attributes: not writable, not enumerable, configurable. Reason: they are names that were not standard properties before ES2015 and are ignored by the `with` statement [DATED] so as not to break old code (Spec p.643–644) [VERSION-DEPENDENT: ES2015 as a reference].

### 4.3 Holes, genericity and species

- **Generic**: almost all methods do `ToObject(this)` and `LengthOfArrayLike`, and can be transferred to array-like objects (notes say intentionally generic, Spec p.620–642).
- **Holes**: `forEach`, `map`, `filter`, `every`, `some`, `reduce`, `indexOf` only visit indices that exist (`HasProperty`). `includes`, `find*`, `join`, `at`, `with`, `toSorted`, `toReversed`, `toSpliced` read via `Get` and treat holes as `undefined` (Spec p.625, p.628, p.641).
- **Range fixed before the first call**: elements appended afterwards are not visited; changed values are seen with their current value; elements deleted before the visit are not visited in the methods with `HasProperty` (Spec p.622, p.623, p.627, p.630, p.632, p.636). `find*` are the exception (they visit deleted ones).
- **species**: `concat`, `filter`, `map`, `slice`, `splice`, `flat`, `flatMap` create the result via `ArraySpeciesCreate`, using `constructor`/`@@species` (Spec p.619–620, p.626–627).
- **`length`**: always greater than the index of every own configurable property; reducing `length` deletes the elements above; if there is a non-configurable element in the range, `length` ends up one above the largest non-configurable index (Spec p.644).
- **Array Iterator**: `next()` recomputes the length on every call (arrays that grow during iteration keep being traversed); an invalid `this` is `TypeError`; for an out-of-bounds TypedArray it is also `TypeError`; `@@toStringTag` is `"Array Iterator"` (Spec p.644–645).
- **Annex E** (ES2015): `Array.prototype.sort` started treating the comparator's `NaN` as +0 and applying ToNumber (before, implementation-defined) (Spec p.865) [VERSION-DEPENDENT].

## 5. TypedArray

A TypedArray is an array-like **view** over a binary buffer; there is one constructor per element type (Spec p.646).

| Constructor | Element type | Conversion | Page |
|---|---|---|---|
| `Int8Array` / `Uint8Array` | 8-bit signed / unsigned integer | ToInt8 / ToUint8 | p.646 |
| `Uint8ClampedArray` | 8-bit unsigned with **clamp** | ToUint8Clamp | p.646 |
| `Int16Array` / `Uint16Array` | 16 bits | ToInt16 / ToUint16 | p.646 |
| `Int32Array` / `Uint32Array` | 32 bits | ToInt32 / ToUint32 | p.646 |
| `BigInt64Array` / `BigUint64Array` | 64 bits (BigInt content) | ToBigInt64 / ToBigUint64 | p.646 |
| `Float16Array` | IEEE 16 bits (version not stated in the sources) | — | p.646 |
| `Float32Array` / `Float64Array` | IEEE 32 / 64 bits | — | p.646 |

The byte-size column of Table 70 was not extracted from the PDF; the sizes above come from the names (8/16/32/64 bits) (Spec p.646).

### 5.1 Concrete constructors and %TypedArray%

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `TypedArray` (concrete) | `new Int8Array()`, `new X(length)`, `new X(typedArray)`, `new X(buffer [, byteOffset [, length]])`, `new X(iterable/array-like)` | No arguments: empty. First argument not an object: `ToIndex` is the number of elements (new zeroed buffer). TypedArray: copies (same type clones the buffer; different types convert element by element). Buffer: a view; `byteOffset` and `length` by `ToIndex`. Other object: an iterable is read entirely into a list; otherwise array-like. A resizable buffer without `length` produces an AUTO length (tracks the buffer). Can be extended. | `TypeError` if called without `new`; `TypeError` if the source is out of bounds, the buffer is detached or the content types differ (Number versus BigInt); `RangeError` if `byteOffset` is not a multiple of the element size, if `offset` goes past the buffer or if `offset + length × size` goes past the buffer size; `RangeError` if the fixed buffer is not a multiple of the element size and `length` is omitted | p.665–668 | — |
| `BYTES_PER_ELEMENT` | property of the constructor and of the prototype | Not writable, not enumerable, not configurable. Each concrete constructor has `length` 3 and `[[Prototype]]` `%TypedArray%`. | — | p.669 | — |
| `%TypedArray%` | abstract intrinsic | Superclass with no global name; calling it or using it with `new` always throws. `length` 0, `name` `"TypedArray"`. | `TypeError` | p.647 | — |
| `%TypedArray%.from` | `from(source [, mapper [, thisArg]])` | `this` must be a constructor. If `source` is iterable, it **reads everything into a list first** before creating the target and assigns with `mapper(value, index)`; otherwise array-like. | `TypeError` if `this` is not a constructor or `mapper` is invalid | p.647–648 | — |
| `%TypedArray%.of` | `of(...items)` | Creates a TypedArray of the size of the arguments, converting each value to the type. | `TypeError` if `this` is not a constructor | p.648 | — |
| `%TypedArray%[Symbol.species]` | getter | Returns `this`. | — | p.648 | — |

### 5.2 Prototype (%TypedArray%.prototype)

General rule: the methods **are not generic**. `this` must have the `[[TypedArrayName]]` slot and goes through `ValidateTypedArray`, which throws `TypeError` if the slot is missing or if the array is **out of bounds** (detached buffer, or resizable that shrank) (Spec p.651, p.665). The prototype itself does not have the instance slots (Spec p.648–650, p.669).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `buffer`, `byteLength`, `byteOffset`, `length` | getters | `buffer` returns the viewed ArrayBuffer/SharedArrayBuffer. The three sizes return **0** (without throwing) when out of bounds or detached. | `TypeError` if `this` does not have the slot | p.649, p.656 | — |
| `at` | `at(index)` | As in Array, with validation. | `TypeError` | p.649 | — |
| `copyWithin` | `(target, start [, end])` | Copies **bytes**; revalidates after the conversions. | `TypeError` if it went out of bounds | p.650 | — |
| `entries`, `keys`, `values`, `[Symbol.iterator]` | `()` | Validate and create an Array Iterator; `[Symbol.iterator]` is the same as `values`. | `TypeError` | p.651, p.655, p.663 | — |
| `every`, `some`, `forEach`, `find`, `findIndex`, `findLast`, `findLastIndex` | `(callback [, thisArg])` | Same rules as Array, without holes (they use `Get`). | `TypeError` if the callback is invalid | p.651–653, p.660 | — |
| `fill` | `(value [, start [, end]])` | Converts `value` **first** (ToBigInt for BigInt64/BigUint64, ToNumber for the others), then computes indices and revalidates the size. | `TypeError` when passing a Number to a BigInt array [inference]; `TypeError` if it went out of bounds | p.651–652 | — |
| `filter` | `(callback [, thisArg])` | Collects the approved ones and creates the result with `TypedArraySpeciesCreate`. | same | p.652 | — |
| `includes`, `indexOf`, `lastIndexOf` | `(searchElement [, fromIndex])` | Same logic as Array (SameValueZero in `includes`; strict equality in the others). | `TypeError` | p.654–656 | — |
| `join` | `([separator])` | As Array; elements are never `null`. | `TypeError` | p.655 | — |
| `map` | `(callback [, thisArg])` | Creates the result **first** (`TypedArraySpeciesCreate(O, [len])`); each return is written with `Set` (undergoes the type conversion). | `TypeError` | p.656 | — |
| `reduce`, `reduceRight` | `(callback [, initialValue])` | As Array. | `TypeError` if empty without an initial value | p.656–657 | — |
| `reverse` | `()` | Reverses in place. | `TypeError` | p.657–658 | — |
| `set` | `set(source [, offset])` | Copies from an array-like or TypedArray; `offset` defaults to 0. If source and target share a buffer, it **clones** the source region first. Same type copies bytes; different types convert. | `RangeError` for negative `offset`, Infinity or `source.length + offset` above the target; `TypeError` if target/source out of bounds or different content types (BigInt versus Number) | p.658–659 | — |
| `slice` | `(start, end)` | **Copy** (does not share the buffer) via `TypedArraySpeciesCreate`; revalidates. | `TypeError` if it went out of bounds | p.659–660 | — |
| `sort` | `sort(comparator)` | **Numeric order** without a comparator: `NaN` last, `-0` before `+0`. With a comparator, ToNumber and `NaN` becomes 0. Example: `new Int8Array([10, 9, 1]).sort()` gives 1, 9, 10. | `TypeError` if the comparator is invalid (checked first) | p.661, p.665 | — |
| `subarray` | `(start, end)` | New TypedArray over the **same** buffer, without copying; created via species; negatives from the end. If the original is AUTO and `end` is `undefined`, the new one also tracks the buffer. Out of bounds: treats the length as 0, without throwing. Changing the subarray changes the original. | — | p.661–662 | — |
| `toLocaleString` | `([reserved1 [, reserved2]])` | Same algorithm as Array, with validation. | `TypeError` | p.662 | [HOST] |
| `toReversed`, `toSorted`, `with` | `()`, `(comparator)`, `(index, value)` | Non-mutating; create the result with `TypedArrayCreateSameType` (same type, **without** species). `with` converts `value` first and checks `IsValidIntegerIndex`. | `TypeError` (invalid comparator, validation); `RangeError` in `with` with an invalid index | p.662–663 | version not stated in the sources |
| `toString` | `()` | It is the same function object as `Array.prototype.toString`. | — | p.663 | — |
| `[Symbol.toStringTag]` | getter | Returns the type name (`"Uint8Array"` etc.); `undefined` if `this` is not a TypedArray. | — | p.663–664 | — |
| `constructor` | property | Initially `%TypedArray%`; on each concrete prototype, the concrete constructor. | — | p.650, p.669 | — |

Relevant internal operations: `TypedArraySpeciesCreate` validates that the result is a TypedArray of the **same content type** (Number versus BigInt), otherwise `TypeError`; `TypedArrayCreateSameType` ignores species; `CompareTypedArrayElements` defines the numeric order described above (Spec p.664–665).

## 6. Uint8Array: base64 and hex

`Uint8Array` is an ordinary TypedArray with additional methods on the constructor and on the prototype (Spec p.669). Version in which it entered: not stated in the sources (the whole block).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Uint8Array.fromBase64` | `fromBase64(string [, options])` | Decodes and returns a new `Uint8Array` of the exact size. `options.alphabet`: `"base64"` (default) or `"base64url"`. `options.lastChunkHandling`: `"loose"` (default), `"strict"` or `"stop-before-partial"`. | `TypeError` if `string` is not a String or an option is invalid; `SyntaxError` for invalid content | p.670 | version not stated in the sources |
| `Uint8Array.fromHex` | `fromHex(string)` | Decodes hexadecimal into a new `Uint8Array`. | `TypeError` if not a String; `SyntaxError` for invalid content | p.670 | version not stated in the sources |
| `setFromBase64` | `setFromBase64(string [, options])` | Decodes **into** the existing array from the start; stops when a full group no longer fits. Returns `{ read, written }` (characters consumed, bytes written). Valid bytes already decoded are written **even if an error comes later**: the `SyntaxError` is only thrown after writing. | `TypeError` if `this` is not exactly `Uint8Array`, if it is out of bounds or an option is invalid; `SyntaxError` | p.670–671 | version not stated in the sources |
| `setFromHex` | `setFromHex(string)` | Same structure, without `options`. | same | p.671 | version not stated in the sources |
| `toBase64` | `toBase64([options])` | Encodes the bytes. `alphabet` `"base64"` (default) or `"base64url"`; `omitPadding` by ToBoolean (true suppresses `=`). Follows RFC 4648 (section 4 or 5). | `TypeError` if out of bounds or `alphabet` is invalid | p.671–672 | version not stated in the sources |
| `toHex` | `toHex()` | Each byte becomes two **lowercase** hexadecimal digits, concatenated. | `TypeError` if out of bounds | p.671–672 | version not stated in the sources |

Base64 decoder rules (Spec p.672–675):
- ASCII whitespace between characters is ignored: only tab (0x09), LF (0x0A), FF (0x0C), CR (0x0D) and space (0x20); VT (0x0B) is **not**.
- Default alphabet: A–Z, a–z, 0–9, `+`, `/`. In `base64url`, `+` and `/` are an error and `-` and `_` are accepted.
- Partial final group: `"stop-before-partial"` stops before the group without error; `"strict"` gives `SyntaxError`; `"loose"` gives an error with 1 character and decodes with 2 or 3 (without requiring leftover bits to be zero). In `"strict"`, leftover bits must be zero.
- `=` padding: with fewer than 2 characters in the group it is an error; with 2 characters it requires the second `=` (whitespace between them allowed; without it, `"stop-before-partial"` stops without error and the other modes give an error). Any content after the padding is a `SyntaxError`.
- A character outside the alphabet is a `SyntaxError`.

Hex decoder rules (Spec p.675): odd length is an immediate `SyntaxError`; reads two at a time, accepts uppercase and lowercase; a character outside `0-9a-fA-F` interrupts with `SyntaxError`, but the previous pairs have already been decoded; does not tolerate whitespace [inference: it does not call the whitespace-skipping routine].

## 7. Map

Key equality: **SameValueZero** (`NaN` equals `NaN`; `-0` equals `+0`, and the stored key becomes `+0` via `CanonicalizeKeyedCollectionKey`) (Spec p.675, p.697). Iteration order is insertion order. Implementations must have sublinear access time on average; the list described in the Spec is only a semantics model (Spec p.675).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Map` | `new Map([iterable])` | Requires `new`. `undefined`/`null` gives an empty Map. Reads `this.set` (a `set` overridden in a subclass is used) and calls it for each item; each item must be a pair-like **object** (property `"0"` is the key, `"1"` the value; the read may trigger getters). An exception while reading/adding closes the iterator. Can be extended. Passing `[1, 2]` instead of pairs throws. | `TypeError` without `new`, if `set` is not callable or if an item is not an object | p.675–676 | — |
| `Map.groupBy` | `groupBy(items, callback)` | Calls `callback(element, index)` in order; the return is the Map key and the value is an array with the group's elements. Object keys preserve identity [inference]. | — | p.677 | version not stated in the sources |
| `Map[Symbol.species]` | getter | Returns `this`. | — | p.677 | — |
| `clear` | `clear()` | Empties; returns `undefined`. Internal list preserved for suspended iterators. | `TypeError` if `this` lacks `[[MapData]]` | p.677–678 | — |
| `delete` | `delete(key)` | `true` if it removed, `false` if it did not exist. | same | p.678 | — |
| `entries` | `entries()` | Iterator of `[key, value]`; it is also the value of `[Symbol.iterator]`. | same | p.678, p.681 | — |
| `forEach` | `forEach(callback [, thisArg])` | Calls `callback(value, key, map)` in insertion order. Removed and unvisited entries are skipped; **new entries added during traversal are visited**; a key removed after being visited and re-added will be visited again. Returns `undefined`. Always adding a new key inside the loop may not terminate [inference]. | `TypeError` if the callback is invalid | p.678–679 | — |
| `get` | `get(key)` | Value or `undefined`. | `TypeError` if `this` is invalid | p.679 | — |
| `getOrInsert` | `getOrInsert(key, value)` | If present, returns the current value; otherwise inserts `value` and returns it. | same | p.679 | version not stated in the sources |
| `getOrInsertComputed` | `getOrInsertComputed(key, callback)` | Checks `callback` before the lookup. If the key exists, returns without calling. Otherwise calls `callback(key)` (canonicalized key, `this` `undefined`); then **looks up again**: if the callback inserted the key, the value is overwritten by the return; if not, appends. | `TypeError` if the callback is not callable | p.679–680 | version not stated in the sources |
| `has` | `has(key)` | Boolean. | same | p.680 | — |
| `keys`, `values` | `()` | Iterators of keys / values. | same | p.680 | — |
| `set` | `set(key, value)` | Updates keeping the original position, or appends to the end. **Returns the Map itself** (chainable). | same | p.680 | — |
| `size` | getter | Entries not removed; no setter. | same | p.680 | — |
| `[Symbol.iterator]` | `()` | Initially the same object as `entries`. | — | p.681 | — |
| `[Symbol.toStringTag]` | property | `"Map"` (configurable). | — | p.681 | — |

Traps: object and Symbol keys compare by identity (Spec p.675). `%Map.prototype%` is an ordinary object without `[[MapData]]` (Spec p.677). **Map Iterator**: walks by index, skips removed ones, re-reads the length at each step (sees new items); `entries` generates a new array on each result; `@@toStringTag` `"Map Iterator"` (Spec p.681–682).

## 8. Set

Unique values by SameValueZero; same performance requirement as Map (Spec p.682).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `Set` | `new Set([iterable])` | Requires `new`. `undefined`/`null` gives an empty Set; otherwise reads `add` and calls it for each value; an exception closes the iterator. | `TypeError` without `new` or if `add` is not callable | p.683–684 | — |
| `Set[Symbol.species]` | getter | Returns `this`. | — | p.684 | — |
| `add` | `add(value)` | If it already exists (after canonicalizing -0), returns the Set unchanged; otherwise appends to the end. Returns the Set. | `TypeError` if `this` lacks `[[SetData]]` | p.684–685 | — |
| `clear` | `clear()` | Empties; `undefined`. | same | p.685 | — |
| `delete` | `delete(value)` | `true`/`false`. | same | p.685 | — |
| `entries` | `entries()` | Iterator of `[v, v]` pairs. | same | p.686 | — |
| `forEach` | `forEach(callback [, thisArg])` | `callback(v, v, set)`; same visiting rules as Map. | `TypeError` if the callback is invalid | p.686–687 | — |
| `has` | `has(value)` | Boolean. | `TypeError` if `this` is invalid | p.687 | — |
| `keys`, `values` | `()` | `keys` is the same function object as `values`; `[Symbol.iterator]` initially too. | same | p.689–690 | — |
| `size` | getter | Number of values. | same | p.689 | — |
| `[Symbol.toStringTag]` | property | `"Set"`. | — | p.690 | — |

**Set algebra** (version not stated in the sources). All validate `other` with `GetSetRecord`: `other` must be a "set-like" object with a numeric `size` (ToNumber; `NaN`, including `undefined`, is `TypeError`; negative is `RangeError`; infinite is accepted), a callable `has` and a callable `keys`. **An Array does not qualify** [inference]. Those that return a set create a plain **new Set**, without going through the subclass constructor or species (Spec p.682–683, p.686, p.688, p.690).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `union` | `union(other)` | Copy of `this` with the values of `other.keys()` appended without duplicating; those of `this` first. Example: `new Set([1,2]).union(new Set([2,3]))` gives 1, 2, 3 [extrapolation]. | `TypeError`/`RangeError` from `GetSetRecord` | p.690 | version not stated in the sources |
| `intersection` | `intersection(other)` | Elements present in both. If `this.size ≤ other.size`, walks `this` and uses `other.has`, preserving the order of `this`; otherwise walks `other.keys()` and the order follows that of `other`. No duplicates even if `keys()` repeats. | same | p.687–688 | version not stated in the sources |
| `difference` | `difference(other)` | Elements of `this` that are not in `other`. Starts from a copy of `this`; chooses the algorithm by the sizes, so the number of calls to `has`/`keys` of a custom `other` varies. | same | p.685–686 | version not stated in the sources |
| `symmetricDifference` | `symmetricDifference(other)` | Elements in exactly one of the two. Always walks `other.keys()`: if the value is in `this`, removes it from the result; otherwise appends it. | same | p.689–690 | version not stated in the sources |
| `isSubsetOf` | `isSubsetOf(other)` | If `this.size > other.size` returns `false` immediately; otherwise checks each element via `other.has`. | same | p.688–689 | version not stated in the sources |
| `isSupersetOf` | `isSupersetOf(other)` | If `this.size < other.size` returns `false`; otherwise walks `other.keys()` and closes the iterator on failure. | same | p.689 | version not stated in the sources |
| `isDisjointFrom` | `isDisjointFrom(other)` | `true` if there are no elements in common; same split by size; closes the iterator on finding a common one. | same | p.688 | version not stated in the sources |

**Set Iterator**: `entries` generates a new `[v, v]` array; items added during iteration appear; `@@toStringTag` `"Set Iterator"` (Spec p.691).

## 9. WeakMap

Keys must be holdable weakly: objects and Symbols not registered by `Symbol.for`, according to `CanBeHeldWeakly` (Spec p.196). There is no enumeration, `size` or `clear`; entries with an unreachable key may be collected (Spec p.692). **Reading with an invalid key is silent; writing throws** (Spec p.693–695).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `WeakMap` | `new WeakMap([iterable])` | Requires `new`; same steps as Map (reads `set`, `AddEntriesFromIterable`). | `TypeError` without `new` | p.692–693 | — |
| `delete` | `delete(key)` | An invalid key returns `false`; otherwise removes and returns `true`/`false`. | `TypeError` if `this` lacks `[[WeakMapData]]` | p.693 | — |
| `get` | `get(key)` | An invalid or absent key gives `undefined`. | same | p.694 | — |
| `has` | `has(key)` | An invalid key gives `false`. | same | p.694 | — |
| `set` | `set(key, value)` | Updates or appends; returns the WeakMap. Example: `wm.set(1, "x")` throws [inference]. | `TypeError` if the key cannot be held weakly | p.695 | — |
| `getOrInsert` | `getOrInsert(key, value)` | Present: returns it; otherwise inserts and returns `value`. | `TypeError` for an invalid key | p.694 | version not stated in the sources |
| `getOrInsertComputed` | `getOrInsertComputed(key, callback)` | As in Map: calls `callback(key)` only if absent and redoes the lookup before writing. | `TypeError` for an invalid key or a non-callable callback | p.694 | version not stated in the sources |
| `[Symbol.toStringTag]` | property | `"WeakMap"`. | — | p.695 | — |

## 10. WeakSet

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `WeakSet` | `new WeakSet([iterable])` | Requires `new`; reads `add` and calls it per item; an exception closes the iterator. | `TypeError` without `new` or non-callable `add` | p.695–696 | — |
| `add` | `add(value)` | Appends if absent; returns the set. | `TypeError` if the value cannot be held weakly | p.696 | — |
| `delete` | `delete(value)` | An invalid value gives `false`; otherwise `true`/`false`. | — | p.697 | — |
| `has` | `has(value)` | An invalid value gives `false`. | — | p.697 | — |
| `[Symbol.toStringTag]` | property | `"WeakSet"`. | — | p.697 | — |

WeakSet has no `size`, `forEach`, iterators or `clear` in the sources (Spec p.695–697).

## 11. ArrayBuffer

It can be fixed-length or resizable (created with `maxByteLength`) (Spec p.698). A **detached** buffer has `null` data and size 0, and data operations fail (Spec p.699–700, p.708).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `ArrayBuffer` | `new ArrayBuffer(length [, options])` | Requires `new`; `length` by `ToIndex`; `options.maxByteLength` (by `ToIndex`; `undefined` is equivalent to absent) creates a resizable buffer. Can be extended. Example: `new ArrayBuffer(8, { maxByteLength: 16 })`. | `TypeError` without `new`; `RangeError` if `length > maxByteLength` or if the maximum block cannot be allocated | p.698–700, p.704–705 | — |
| `ArrayBuffer.isView` | `isView(arg)` | `true` only if `arg` is an object with `[[ViewedArrayBuffer]]` (TypedArray; the page does not mention `DataView` [extrapolation]). | — | p.705 | — |
| `ArrayBuffer[Symbol.species]` | getter | Returns `this`; used by `slice`. | — | p.705 | — |
| `byteLength` | getter | Current size; detached gives 0. | `TypeError` if `this` lacks `[[ArrayBufferData]]` or is a SharedArrayBuffer | p.706 | — |
| `maxByteLength` | getter | Detached gives 0; fixed gives its own size; resizable gives the maximum. | same | p.706 | — |
| `resizable` | getter | `true` if resizable. | same | p.706 | — |
| `detached` | getter | Boolean. | same | p.706 | — |
| `resize` | `resize(newLength)` | `newLength` by `ToIndex`; the host may handle it [HOST]; otherwise swaps the block copying the minimum; returns `undefined`. Example: `buf.resize(12)` changes it; `buf.resize(32)` above the maximum throws. | `TypeError` if fixed, shared or detached; `RangeError` if above the maximum | p.706–707 | [HOST] (hook) |
| `slice` | `slice(start, end)` | Indices by ToIntegerOrInfinity (negatives from the end, clamped to `[0, len]`); creates the new buffer via `SpeciesConstructor` (default `%ArrayBuffer%`); the result must be a non-shared, non-detached ArrayBuffer, **different** from the original and with size ≥ the new length; revalidates and copies only what still exists. | `TypeError` if detached, shared or the result is invalid | p.707 | — |
| `transfer` | `transfer([newLength])` | Moves the content to a new ArrayBuffer **preserving resizability** and detaches the original (`ArrayBufferCopyAndDetach`). Undefined `newLength` keeps the size; otherwise `ToIndex`. | `TypeError` if not an ArrayBuffer, shared, already detached or with a detach key | p.699, p.707 | version not stated in the sources |
| `transferToFixedLength` | `transferToFixedLength([newLength])` | Same, but the result is always fixed-length. | same | p.708 | version not stated in the sources |
| `[Symbol.toStringTag]` | property | `"ArrayBuffer"`. | — | p.708 | — |

Additional points: after `transfer`, the original has `detached` true and `byteLength` 0, and TypedArrays that viewed it start behaving as out of bounds [inference] (Spec p.699–700, p.706, p.708). The detach key (`[[ArrayBufferDetachKey]]`) is only defined by the environment [HOST] (Spec p.708). `DetachArrayBuffer` with a different key throws `TypeError` (Spec p.700).

**Guidelines for resizable buffers** (Spec p.708–709): test in the target environment (memory varies a lot); choose the smallest possible `maxByteLength` and avoid going over 2^30 bytes (1 GiB); creating with a given maximum does not guarantee that future `resize` calls will succeed. For implementations in environments that reserve virtual memory, it is recommended to throw for maximums above a range of 1 to 1.5 GiB [HOST].

**Byte conversion** (Spec p.701–703): signed integers use two's complement; floats follow IEEE 754; the encoding of a written `NaN` is chosen by the implementation; rounding to float16/float32 is round-half-to-even; byte order uses the agent's `[[LittleEndian]]` field when not specified [HOST].

## 12. SharedArrayBuffer

The global property only exists if the environment offers concurrent access to SharedArrayBuffers; the host may omit it [HOST] (Spec p.711). It is never detached and its data is never `null` (Spec p.711, p.714). It can be fixed or **growable** (grows with `grow`, never shrinks) (Spec p.709).

| Member | Signature | What it does / edge cases | Error thrown | Page | Mark |
|---|---|---|---|---|---|
| `SharedArrayBuffer` | `new SharedArrayBuffer(length [, options])` | Requires `new`; `length` by `ToIndex`; `options.maxByteLength` creates a growable one (allocates the block of the maximum size plus 8 bytes for the current length). | `TypeError` without `new`; `RangeError` if `length > maxByteLength` | p.709–711 | [HOST] |
| `SharedArrayBuffer[Symbol.species]` | getter | Returns `this`. | — | p.711 | — |
| `byteLength` | getter | Size (synchronizing read). | `TypeError` if not shared | p.712 | — |
| `growable` | getter | `true` if growable. | same | p.713 | — |
| `maxByteLength` | getter | Fixed: current size; growable: the maximum. | same | p.713 | — |
| `grow` | `grow(newLength)` | `newLength` by `ToIndex`; the host may handle it [HOST]; otherwise a compare-and-exchange loop. A size equal to the current one does nothing. Concurrent calls are totally ordered: if `grow(20)` comes before `grow(10)`, the second throws `RangeError` instead of shrinking. Returns `undefined`. | `TypeError` if fixed or not shared; `RangeError` if smaller than the current, larger than the maximum or out of memory | p.712–713 | [HOST] (hook) |
| `slice` | `slice(start, end)` | Same index logic as ArrayBuffer; default species `%SharedArrayBuffer%`; the result must be a SharedArrayBuffer with different data and sufficient size. | `TypeError` if the result is invalid | p.713–714 | — |
| `[Symbol.toStringTag]` | property | `"SharedArrayBuffer"`. | — | p.714 | — |

Synchronization (Spec p.714): size reads through the `length`/`byteLength` getters (of SharedArrayBuffer, `%TypedArray%.prototype` and `DataView.prototype`) are synchronizing; the bounds check on indexed access (`u8[idx]`) is **not**. Being within bounds in one access does not guarantee being so in the next without explicit synchronization. The same `maxByteLength` guidance as for ArrayBuffer applies (smallest possible, up to 1 GiB).

## 13. Divergences and points of attention between Spec passages

In this part of the catalog there is only the Spec (EJ1 and EJpt are not included). The relevant divergences are between the body of the Spec and the annexes, or between old and current behavior:

- **`RegExp` constructor with `flags`**: the body (p.599) creates a new instance when `pattern` is a RegExp and `flags` is supplied; Annex B (`compile`, p.855) throws `TypeError` in that same case; Annex F (p.869) records that, before ES2015, the constructor also threw. The body prevails for the constructor and Annex B for `compile` [DATED].
- **`localeCompare`**: the body requires canonical equivalents to give 0 (p.544–545); Annex F (p.869) says that before, bit-by-bit comparison was enough. The body applies.
- **`Array.prototype.sort` and the comparator's `NaN`**: the body treats it as 0 (p.638); Annex E (p.865) records that before it was implementation-defined.
- **Annex E, item 8**: Annex E cites `String.prototype.match`/`replace` with a global RegExp, but the cited sections (22.2.6.8 and 22.2.6.11) are the `Symbol.match` and `Symbol.replace` methods of RegExp (p.865, p.603–605). The rule cited (advance `lastIndex` only on an empty match) is the one the body describes.
- **Equality in Map/Set**: the `delete` text uses `SameValue` after canonicalizing `-0`; the effect is equivalent to SameValueZero (p.678, p.685, p.697) [inference].

## 14. Do not reproduce (noise and truncated passages in the sources)

- **Lost exponents**: "2^32 − 1", "2^53 − 1", "2^31", "2^30" appear as "232 − 1", "253 - 1" etc. in the PDF (Spec p.563, p.610–611, p.616–620, p.631, p.639, p.641–642). Do not copy the flattened text.
- **Truncated `Symbol.split` example** (Spec p.607): the result list of the example `/<(\/)?([^<>]+)>/` ends at `"coded",` in the extracted text; the rest (`"/"`, `"CODE"`, `""`) is not available. Do not complete from memory.
- **Table 70 (sizes in bytes)** empty in the extracted PDF (Spec p.646); **Tables 64–66**: aliases separated from their names (e.g.: `Dep` on p.595, `NChar` on p.596).
- **Section headers at the end of the page**: the numbers 22.x/23.x/24.x/25.x appear at the end of each page; some notes of `at`, `charAt`, `charCodeAt`, `codePointAt` and `concat` appear mixed on p.540–541, and the body of `startsWith` is on p.552 with the note on p.553. The method-page association in this file follows the order of the titles.
- **`AllocateTypedArrayBuffer`** ends truncated on p.668.
- **Section start cut off on p.555**: the paragraph about `toUppercase` was attributed to `toUpperCase`.
- **Pattern grammar**: loose parentheses and parameter symbols rearranged by the extractor (Spec p.558–563); the grammar's indentation is not reliable.
- **Symbols 𝔽 and ℝ** stuck to the following text (e.g.: "+0𝔽and"): noise, with no semantic effect.

## 15. Gaps

- **ES versions**: the Spec dates almost none of the methods in this catalog (`at`, `findLast`, `toSorted`, `with`, `fromAsync`, `Float16Array`, base64/hex of `Uint8Array`, `Map.groupBy`, `getOrInsert*`, set algebra, `transfer`, `resize`, `grow`, `isWellFormed`, `RegExp.escape`, flag `v`, inline modifiers). All stay as "version not stated in the sources". Only ES2015 (Annex F/E), ES2016, ES2017 and ES2018 are cited in the annexes, for other items.
- **Not covered by the notes**: algorithms of `ToIndex`, `ToIntegerOrInfinity`, `ToLength`, `IsRegExp`, `SpeciesConstructor`, `CanBeHeldWeakly`, `GetSubstitution` in detail by group name, `ArraySpeciesCreate`, `IsStringWellFormedUnicode`; text of the Annex B RegExp productions beyond the summary; later TypedArray sections (properties of the concrete constructors beyond the p.669 summary); `DataView`, `Atomics` and other buffer objects; `Intl` and what ECMA-402 defines for `toLocale*`, `localeCompare` and `normalize`.
- **Tables**: complete values of Tables 64–66 (Unicode properties) and of the byte sizes (Table 70) are not fully available; the list of binary properties in section 3.3 is partial ("among others").
- **Host behavior**: formats of `toLocaleString`/`toLocaleDateString`, `localeCompare` order, time zone name and other [HOST] hooks depend on the environment and are not determined by the Spec.
- **EJ1 and EJpt**: this file uses no examples or explanations from the books; the didactic explanation of these objects stays outside this catalog.
