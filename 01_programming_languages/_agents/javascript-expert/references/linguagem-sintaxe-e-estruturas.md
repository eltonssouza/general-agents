# JavaScript language: syntax and structures according to the Spec

How to use this file: it is a lookup reference on the syntax and observable semantics of the language, organized by construct. Source: Spec = ECMA-262, 17th edition (ECMAScript 2026), cited as `(Spec p.N)` with the PDF page. The Spec is normative, but it almost never says in which edition a feature entered; when that happens, the text says "version not stated in the sources". Each construct carries, where applicable: form, observable semantics, errors (early errors are `SyntaxError`s detected before execution; the others are runtime exceptions) and edge cases. Internal algorithms were omitted on purpose. Labels: **[inference]** (connection made here from the text), **[extrapolation]** (knowledge not confirmed in the sources read), **[DATED]** (legacy, according to the source itself), **[VERSION-DEPENDENT]**, **[HOST]** (defined by the environment). Grep the `##`/`###` headings to navigate.

## Table of contents

1. Proxy: traps and invariants
2. Source code, code types and strict mode
3. Lexical grammar
4. Automatic semicolon insertion (ASI)
5. Identifiers and primary expressions
6. Left-hand-side expressions: member, call, new, super, spread, optional chaining, tagged template, meta-properties
7. Operators
8. Assignment and destructuring
9. Evaluation order (cross-cutting summary)
10. Statements and declarations
11. Functions
12. Classes
13. Scripts and modules
14. Divergences, inconsistencies in the sources and passages not to reproduce
15. Gaps

---

## 1. Proxy: traps and invariants

### 1.1 Overview
- A Proxy is an exotic object whose essential internal methods are partly implemented by ECMAScript code. It keeps two slots: `[[ProxyHandler]]` and `[[ProxyTarget]]` (Spec p.234).
- Correspondence between trap and internal method (Table 29, Spec p.234–235): `getPrototypeOf`, `setPrototypeOf`, `isExtensible`, `preventExtensions`, `getOwnPropertyDescriptor`, `defineProperty`, `has`, `get`, `set`, `deleteProperty`, `ownKeys`, `apply` (call) and `construct`.
- The handler receives the target as a parameter. If the handler does not define the trap, the operation is forwarded to the target (Spec p.235).
- Revocation: on revoking, both slots become `null` and any later operation throws `TypeError` (Spec p.235, p.243).
- Since the handler is arbitrary code, it may try to violate object invariants; the Spec explicitly checks the essential ones and a violation raises `TypeError` at the time of the operation, never at proxy creation (Spec p.235).
- Pattern of all traps (single summary): check that the proxy has not been revoked, look up the trap on the handler, delegate to the target if absent, otherwise call the trap with `this` equal to the handler and the target as first argument, and validate the result against the target.
- Boolean traps (`set`, `deleteProperty`, `defineProperty`, `has`, `isExtensible`, `preventExtensions`, `setPrototypeOf`) pass the result through `ToBoolean`; any truthy value counts as success (Spec p.236–241).
- `ProxyCreate` throws `TypeError` if the target or handler are not objects. The proxy is only callable if the target was callable and only a constructor if the target was a constructor (Spec p.243). Example **[inference]**: `new Proxy(1, {})` and `new Proxy({}, null)` fail with `TypeError`.

### 1.2 Table of traps, invariants and errors

| Trap | Error (`TypeError`) when | Page |
|---|---|---|
| `getPrototypeOf` | the return is neither an object nor `null`; or the target is non-extensible and the return differs from the real prototype | Spec p.235 |
| `setPrototypeOf` | truthy trap, non-extensible target and `V` differs from the current prototype | Spec p.236 |
| `isExtensible` | the boolean result differs from `IsExtensible(target)` | Spec p.236 |
| `preventExtensions` | the trap returns `true` but the target is still extensible | Spec p.237 |
| `getOwnPropertyDescriptor` | the return is neither an object nor `undefined`; see 1.3 | Spec p.237–238 |
| `defineProperty` | truthy trap but a violation; see 1.3 | Spec p.238–239 |
| `has` | the trap returns `false` but the target has the non-configurable own property, or the target is non-extensible and has it | Spec p.239 |
| `get` | the target has a non-configurable, non-writable data property and the trap's value is not SameValue; or a non-configurable accessor without `[[Get]]` and a return different from `undefined` | Spec p.240 |
| `set` | truthy trap, target with a non-configurable, non-writable data property and `V` different from the value; or a non-configurable accessor without `[[Set]]` | Spec p.240 |
| `deleteProperty` | truthy trap but the property exists on the target as non-configurable, or exists and the target is non-extensible | Spec p.241 |
| `ownKeys` | duplicates; an element that is not a string/symbol; a non-configurable key of the target is missing; non-extensible target and the list not equal to the target's keys | Spec p.241–242 |
| `apply` | no invariant checks on the return | Spec p.242 |
| `construct` | the return is not an object | Spec p.242–243 |

### 1.3 Detailed edge cases
- `getOwnPropertyDescriptor` (Spec p.237–238): it is an error to return `undefined` for a non-configurable property of the target, or for any existing property of a non-extensible target; it is an error to report an absent property as existing on a non-extensible target; it is an error to report `configurable: false` if the target lacks the property or has it as configurable; it is an error to report non-configurable and non-writable if on the target it is still writable; the completed descriptor must be compatible with the target's.
- `defineProperty` (Spec p.238–239): after a truthy result, it is an error (a) for the property not to exist on the non-extensible target, (b) to request `configurable: false` without a configurable counterpart on the target, (c) for the descriptor to be incompatible with the existing one, (d) to request `writable: false` when the target keeps a non-configurable, writable data property. Applying the descriptor to the target cannot throw.
- `has`: there is no check in the opposite direction; a trap returning `true` for a nonexistent property is accepted **[inference]** (Spec p.239).
- `deleteProperty`: if the target does not have the property, the operation returns `true` (Spec p.241).
- `set`: a trap that forgets to return truthy makes the internal operation return `false`; in strict code the caller turns that into an error **[inference]** (Spec p.240; the conversion by the caller is in 8.1, Spec p.317).
- `ownKeys`: the result is converted from an array-like into a list of keys; the extensibility check requires the same list (neither more nor less) as the target's (Spec p.241–242).
- `apply`: the arguments reach the trap as a real array (Spec p.242). `construct`: without a trap, it constructs the target with the received `newTarget` (Spec p.242).

### 1.4 Immutable prototype
- Immutable-prototype objects exist only in `%Object.prototype%` and in host objects. `[[SetPrototypeOf]](V)` returns `true` only if `V` is the current prototype (the same value), otherwise `false` (Spec p.234). Whether `false` becomes an exception is up to the caller **[extrapolation]**.

---

## 2. Source code, code types and strict mode

### 2.1 Source text
- Code is a sequence of Unicode code points (U+0000 to U+10FFFF); the external encoding is irrelevant and there is no normalization: combining sequences are individual code points (Spec p.243).
- Unicode escapes are valid in strings, regexes, templates and identifiers. In comments the escape is never interpreted. Unlike Java, a line-break escape does not end a comment or a string (Spec p.244).
- `ParseText` returns a node or a non-empty list of `SyntaxError`s; the quantity and order of reported errors are implementation-defined, but there must be at least one (Spec p.245). **[HOST]** as to which error appears first; two-pass analyzers may report the late error without the early one.

### 2.2 Four kinds of code (Spec p.246)
- Global: text treated as a Script, excluding nested functions, classes and similar.
- Eval: text passed to the built-in `eval` when the argument is a String.
- Function: what feeds `[[ECMAScriptCode]]` and `[[FormalParameters]]`, including the `BindingIdentifier` of the function's own name; it also comes from `Function`, `GeneratorFunction`, `AsyncFunction` and `AsyncGeneratorFunction`.
- Module: the `ModuleBody`.
- Practical consequence: strict-mode rules apply to the name of a function whose body has `"use strict"`, even if the surrounding code is not strict (Spec p.246).

### 2.3 Directive prologue and `"use strict"`
- Directive prologue: the longest initial sequence of expression statements (in `FunctionBody`, `ScriptBody` or `ModuleBody`) made only of a string literal followed by `;` (explicit or via ASI). It may be empty (Spec p.246–247).
- Use Strict Directive: exactly the literal `"use strict"` or `'use strict'`, with no escape or line continuation inside (Spec p.247).
- There can be more than one; the prologue statements are evaluated normally; implementations may give meaning to other directives **[HOST]** (Spec p.247).
- Trap: strict mode applies retroactively to the prologue; a string with an octal escape before `"use strict"` makes the code a syntax error (Spec example: a function with `"\7"` and then `"use strict"`) (Spec p.263).
- A `"use strict"` directive in a function with a non-simple parameter list is a `SyntaxError` (see 11.1).

### 2.4 What counts as strict code (Spec p.247)
- Global code that begins with the directive; **a module is always strict**; **every part of a class** (declaration or expression); eval that begins with the directive or that is a direct `eval` inside strict code; a function inside strict code or whose body begins with the directive; functions created by `Function`/`GeneratorFunction`/`AsyncFunction`/`AsyncGeneratorFunction` if the body (last argument) begins with the directive.
- Built-in functions: it is unobservable whether a function is built-in or written in ECMAScript (Spec p.247). **[HOST]**

### 2.5 Effects of strict mode spread across the Spec (index)
| Effect | Where |
|---|---|
| `arguments`/`eval` as `BindingIdentifier` are `SyntaxError` | 5.2; Spec p.274 |
| `implements interface let package private protected public static yield` as `Identifier` are `SyntaxError` | 5.2; Spec p.275 |
| Legacy octal and `\8`/`\9` are `SyntaxError` | 3.7, 3.8; Spec p.257–263 |
| `with` is `SyntaxError` | 10.9; Spec p.347 |
| `delete identifier` is `SyntaxError` | 7.2; Spec p.304 |
| A failing `delete` becomes `TypeError` | 7.2; Spec p.304 |
| Assignment to an unresolvable reference throws `ReferenceError`; to a read-only/setterless/non-extensible object throws `TypeError` | 8.1; Spec p.317 |
| Tail calls only in strict code | 11.10; Spec p.392 |
| Duplicates in parameters only allowed outside strict and in a simple list | 11.1; Spec p.355 |

---

## 3. Lexical grammar

### 3.1 Input elements and lexical goals
- The text becomes tokens, line terminators, comments and whitespace, read from left to right always taking the longest possible sequence (Spec p.248).
- There are several lexical goal symbols because `/` (division) and `/.../` (regex) are ambiguous (Spec p.248–249): `InputElementHashbangOrRegExp` (start of Script or Module), `InputElementRegExpOrTemplateTail`, `InputElementRegExp`, `InputElementTemplateTail` and `InputElementDiv` (other contexts).
- There is no syntactic context in which division and regex are both valid. If the next line starts with `/` and the context allows division, no `;` is inserted: `a = b` followed by `/hi/g.exec(c).map(d)` is read as `a = b / hi / g.exec(c).map(d)` (Spec p.248).

### 3.2 Format-control characters and whitespace
- Format-control characters (category Cf) may appear in comments, strings, templates and regexes. U+FEFF outside those contexts is whitespace, which accommodates a BOM in the middle of concatenated files (Spec p.249).
- Whitespace (Table 30, Spec p.250): TAB (U+0009), VT (U+000B), FF (U+000C), ZWNBSP (U+FEFF) and any code point of the `Space_Separator` category (includes U+0020 and U+00A0). The Spec deliberately excludes code points with the `White_Space` property that are not `Space_Separator` (Spec p.250).
- Whitespace is insignificant, except inside strings, regexes, templates and comments (Spec p.249).

### 3.3 Line terminators
- Unlike whitespace, they influence the syntactic grammar (ASI and restricted productions). Table 31 (Spec p.250): LF (U+000A), CR (U+000D), LS (U+2028), PS (U+2029); only these. `CR LF` counts as one break for line numbering (Spec p.251).
- There cannot be a terminator inside a token, except `StringLiteral`, `Template` and `TemplateSubstitutionTail`; and in strings, LF and CR only as part of a line continuation (Spec p.250).

### 3.4 Comments and hashbang
- A `/* */` comment does not nest. A `//` comment runs to the end of the line without including the terminator, which remains in the stream and therefore does not affect ASI (Spec p.251).
- For the syntactic grammar, a multiline comment containing at least one line terminator counts as a `LineTerminator`; thus `return /* a⏎b */ x` triggers ASI **[inference]** (Spec p.251).
- Hashbang: `#!` to the end of the line, only at the start of a Script or Module, discarded as a comment (Spec p.252).
- There are alternative comment definitions in Annex B (B.1.1) (Spec p.252). **[DATED]**

### 3.5 Tokens and punctuators
- `CommonToken`: `IdentifierName`, `PrivateIdentifier`, `Punctuator`, `NumericLiteral`, `StringLiteral`, `Template`; `DivPunctuator`, regex, `RightBracePunctuator` and `TemplateSubstitutionTail` depend on the lexical goal (Spec p.252).
- `?.` is only a punctuator if **not** followed by a decimal digit, so that `a?.5:b` remains a conditional (Spec p.256).
- Punctuators (Spec p.256): `{ ( ) [ ] . ... ; , < > <= >= == != === !== + - * % ** ++ -- << >> >>> & | ^ ! ~ && || ?? ? : = += -= *= %= **= <<= >>= >>>= &= |= ^= &&= ||= ??= =>`; `/` and `/=` are `DivPunctuator`.

### 3.6 Identifiers and reserved words
- Syntax follows Unicode Annex #31 with small modifications; `$` and `_` are valid in any position (Spec p.252–253). `IdentifierStart` = ID_Start, `$`, `_` or an escape; `IdentifierPart` = ID_Continue, `$` or an escape (Spec p.253). `PrivateIdentifier` = `#` + `IdentifierName`.
- Implementations use the Unicode categories of the most recent version and may accept code points defined later (Spec p.252). **[HOST]**
- A `\uXXXX`/`\u{...}` escape in an identifier contributes one code point; the code point must be valid for the position (start or part), otherwise `SyntaxError` (Spec p.253–254).
- Identifier equality: canonically equivalent sequences with distinct code points are **not** equal; there is no normalization (Spec p.254).
- Escapes do not allow writing a reserved word as an identifier: `els\u{65}` does not declare `else`, because the StringValue already normalizes the escape and the early error rejects it (Spec p.255–256, p.275).
- Five categories (Spec p.255):
  1. always allowed and not keywords (`Math`, `toString`, `_`);
  2. never allowed: the `ReservedWord`s except `await` and `yield`;
  3. allowed depending on context: `await`, `yield`;
  4. forbidden in strict mode: `let static implements interface package private protected public`;
  5. always allowed as identifiers, but keywords in certain productions: `as async from get meta of set target`.
- `ReservedWord` (Spec p.255): `await break case catch class const continue debugger default delete do else enum export extends false finally for function if import in instanceof new null return super switch this throw true try typeof var void while with yield`. **Not** on the list: `let`, `static`, `async`, `of`, `get`, `set`.
- `await` is reserved only in async functions and in modules; `async` can be a variable or a label; `enum` is a future reserved word; `arguments` and `eval` are not keywords but have restrictions in strict mode (Spec p.255–256).

### 3.7 Numeric literals
- Forms (Spec p.256–258): decimal (`123`, `1.5`, `.5`, `1e3`, `1.5e-3`), binary `0b`/`0B`, octal `0o`/`0O`, hexadecimal `0x`/`0X`, and BigInt with the `n` suffix (`10n`, `0xFFn`).
- Numeric separator `_`: only **between digits**, in decimal, binary, octal and hexadecimal, in the integer part, fractional part and exponent. `1__0`, `1_` and `0_1` are not valid **[inference]** (Spec p.257–258).
- BigInt: never with a dot or exponent, nor with the legacy octal form or "octal-like" decimal (Spec p.257).
- Legacy octal (`017`) and decimal with a leading zero containing 8 or 9 (`089`): legacy syntax, `SyntaxError` in strict code (Spec p.257–259). **[DATED]**
- Termination rule: the character immediately after the literal cannot be an `IdentifierStart` or a digit; `3in` is an error, not `3` and `in` (Spec p.258).
- Values: decimals rounded to the nearest Number; non-decimal integers become the Number of the mathematical value; with `n`, an exact BigInt; `_` does not enter the computation (Spec p.259–260). Examples: `1_000_000` is 1000000; `0b1010` is 10.

### 3.8 String literals
- Between single or double quotes; a code point outside the BMP becomes two UTF-16 units (Spec p.261).
- Literally forbidden: the closing quote, `\`, CR and LF. **LS and PS are allowed** (Spec p.261–263).
- Line continuation (`\` + terminator) contributes an empty string and is the only way to have LF/CR in the literal's source text (Spec p.262).
- Simple escapes (Spec p.263): `\b \t \n \v \f \r \" \' \\`. `\0` only if not followed by a digit (Spec p.261). `\xHH`, `\uHHHH`, `\u{...}` (up to 0x10FFFF) (Spec p.262, p.264). Any other escaped character produces itself, except digits, `x` and `u` (Spec p.262).
- Legacy octal (`\1`, `\07`, `\377`) and `\8`/`\9`: `SyntaxError` in strict mode (Spec p.262–264). **[DATED]** Values: `\8` and `\9` produce the characters 8 and 9 (Spec p.264).

### 3.9 Regular expression literals
- Each evaluation creates a **new** RegExp object; two identical literals are never `===` (Spec p.264).
- Two phases: the lexer finds the end (body and flags); then both are re-parsed by the strict regex grammar. Implementations may extend the regex grammar, but not the lexical productions (Spec p.264).
- The first character of the body cannot be `*`, `\`, `/` or `[`; inside `[...]` the slash `/` is allowed without escaping; flags are `IdentifierPartChar` (Spec p.265). `//` starts a comment; the empty regex is written `/(?:)/` (Spec p.265).
- Early error: `SyntaxError` if the flags are not `d g i m s u v y`, if a flag is repeated or if the body does not satisfy `ParsePattern`. Without `u` or `v`, the body is read in 16-bit units (Spec p.284). Examples: `/a/gg` and `/a/x` are errors.

### 3.10 Template literals (lexical)
- Tokens: `NoSubstitutionTemplate`, `TemplateHead` (`` `...${ ``), `TemplateMiddle` (`` }...${ ``), `TemplateTail` (`` }...` ``) (Spec p.266).
- Unlike strings, real line terminators are allowed (Spec p.266).
- Allowed escapes: simple ones, `\0` with no following digit, `\xHH`, `\uHHHH`, `\u{...}`. Legacy octal and `\8`/`\9` are **not** allowed (Spec p.266).
- `NotEscapeSequence` (for example `\01`, an incomplete `\x`, an unclosed `\u{` or above 0x10FFFF) (Spec p.267): in an untagged template it is a `SyntaxError`; in a tagged one the cooked value is `undefined` and the raw one is preserved (Spec p.267, p.285–286).
- TV (cooked value): escapes become code units, line continuation becomes empty, terminators normalize to LF. TRV (raw value): escapes kept as written, line continuation keeps the backslash and the terminator, `CR` and `CR LF` become LF, LS and PS preserved (Spec p.267–269). For a literal CR in the value, an explicit escape is required (Spec p.269).

---

## 4. Automatic semicolon insertion (ASI)

### 4.1 The three rules (Spec p.269)
1. **Offending token**: when the parser meets a token that no production allows, it inserts `;` before it if (a) there is at least one line terminator between it and the previous token, or (b) the offending token is `}`, or (c) the previous token is `)` and the inserted `;` would be the end of a `do-while`.
2. **End of input**: if the input ends without forming a single instance of the goal symbol, it inserts `;` at the end.
3. **Restricted productions**: if a token is allowed but is the first after `[no LineTerminator here]` and there is a line break before it, it inserts `;` before that token.
- Overlap: a `;` that would be parsed as an empty statement is never inserted, nor either of the two `;` in the header of a `for` (Spec p.269).

### 4.2 List of restricted productions (Spec p.269–270)
| Production | Effect with a line break |
|---|---|
| operand `++`/`--` (postfix) | `;` before the operator; it becomes a prefix on the next line |
| `continue`/`break` + label | `;` right after the word; the label is not part of it |
| `return` + expression; `throw` + expression | `;` after the word (`return` returns `undefined`) |
| `yield` + expression and `yield *` | same |
| arrow parameters + `=>` | `;` inserted and `=>` causes `SyntaxError` |
| `async` before `function`, a method name, an identifier `=>` or parameters | `;` inserted; `async` is left alone |
| `async` before `*` | `;` inserted and the punctuator causes `SyntaxError` |

Spec advice (Spec p.271): postfix `++`/`--` on the same line as the operand; the `return`/`throw`/`yield` expression starting on the line of the word; label on the same line; end of the arrow parameters and `=>` on the same line; `async` on the same line as the next token.

### 4.3 Official examples (Spec p.271–272)
- `{ 1 2 } 3` is invalid even with ASI; with a line break between `1` and `2` (and `}` and `3`) it becomes `{ 1 ;2 ;} 3;`, valid (Spec p.271).
- In `for (a; b⏎)`, the header's `;` is not inserted (Spec p.271).
- `return⏎a + b` becomes `return;` and `a + b;`; the sum is not returned (Spec p.271–272).
- `a = b⏎++c` becomes `a = b;` and `++c;` (Spec p.272).
- `if (a > b)⏎else c = d`: no `;` is inserted before `else` (it would be an empty statement), so it is an error (Spec p.272).
- `a = b + c⏎(d + e).print()` gets no ASI and becomes `a = b + c(d + e).print()` (Spec p.272).

### 4.4 Cases that require `;` on the previous line (Spec p.273)
If the next line starts with: `(` (becomes a call), `[` (becomes an access), a backtick (becomes a tagged template), unary `+` or `-` (becomes binary), or a RegExp literal (may be read as division). The Spec acknowledges that one can write with few `;`, but ASI does not occur at every line break and future syntax may change lines that depend on it (Spec p.273).

---

## 5. Identifiers and primary expressions

### 5.1 References and labels
- `IdentifierReference`, `BindingIdentifier` and `LabelIdentifier` accept `Identifier` and also `yield`/`await` depending on `[Yield]`/`[Await]`; the grammar accepts them and static semantics forbids them, to avoid unwanted ASI (Spec p.274).

### 5.2 Early errors for identifiers (Spec p.274–275)
- `arguments`/`eval` as `BindingIdentifier` in strict mode.
- `yield` as a reference, binding or label in strict mode; inside a generator (`[Yield]`) as a binding or `Identifier`.
- `await` as a reference, binding or label in a Module; inside an `[Await]` context.
- In strict mode, an `Identifier` equal to `implements interface let package private protected public static yield`.
- Any `Identifier` whose StringValue is a `ReservedWord`; the StringValue normalizes escapes (Spec p.275).
- Evaluating `IdentifierReference` produces a Reference via `ResolveBinding` (Spec p.276); a nonexistent variable throws `ReferenceError` when read **[extrapolation]**. In non-strict code `yield` is an ordinary identifier (Spec p.276).

### 5.3 `this`, literals and parentheses
- `this` evaluates to the `this` of the current execution context (Spec p.277).
- Literals: `null`, `true`, `false`, numeric and string literals evaluate to the value itself (Spec p.277).
- Parentheses: evaluates the inner expression **without** GetValue; the result may remain a Reference, which allows `delete` and `typeof` on parenthesized expressions (Spec p.289). Example **[inference]**: `typeof (undeclared)` still returns `"undefined"`.
- Cover grammar: `( ... )` can be grouping or arrow parameters (`()`, `(expr,)`, `(...x)`, `(a, ...b)` etc.); as an expression, only `( Expression )` is valid, so a trailing comma, `()` and rest give errors (Spec p.276–277).

### 5.4 Array literal
- Elements are evaluated on each evaluation of the literal (Spec p.278).
- Elision (a comma without an expression) creates a hole that counts toward `length` and does not define the property. A trailing elision does not contribute: `[1,2,]` has length 2, `[1,2,,]` has 3 **[inference]** (Spec p.278).
- Spread `...expr` uses a synchronous iterator and appends each value; a non-iterable fails in `GetIterator` (typically `TypeError`, **[extrapolation]**) (Spec p.279).
- Elements are created with `CreateDataPropertyOrThrow`, so setters or read-only properties inherited from `Array.prototype` do not interfere (Spec p.279). A `length` beyond 2^32−1 throws (Spec p.278).

### 5.5 Object literal
- Forms (Spec p.280): `{}`, with a list, with a trailing comma. `PropertyDefinition`: shorthand `a`, `name: value`, method, `...spread`, and `CoverInitializedName` (`a = 1`). The key can be an identifier, string, numeric or computed `[expr]`.
- `CoverInitializedName` is only valid when the literal is reinterpreted as a destructuring pattern; in a "real" object, `({a = 1})` is a `SyntaxError` (Spec p.281).
- Early errors (Spec p.281): a method with a direct `super(...)` or with private identifiers; two or more `__proto__: value` (not shorthand, not computed, not a method) is a `SyntaxError`, except in `ParseJSON`. So `{ __proto__: a, __proto__: b }` is an error, but `{ __proto__: a, ["__proto__"]: b }` is allowed.
- Evaluation (Spec p.282–284): in writing order; a numeric key becomes `ToString(number)` (`{1.0: 'x'}` creates `"1"`); a computed one goes through `ToPropertyKey` (may call `toString`/`Symbol.toPrimitive` and throw); `...expr` copies own enumerable properties via `CopyDataProperties`; properties are created with `CreateDataPropertyOrThrow` (own, writable, enumerable, configurable).
- A literal `__proto__: v` (not computed, not shorthand): if `v` is an object or `null`, it sets the new object's **prototype**; any other type is ignored. Shorthand `{ __proto__ }` and computed ones create an ordinary property (Spec p.283–284).
- An anonymous function or class as the value gets the key's name (except in the case of the `__proto__` setter) (Spec p.283–284).

### 5.6 Template literal (semantics)
- Untagged: without substitutions it is the TV; with substitutions it concatenates the head, the `ToString` of each expression and the following parts, from left to right. The conversion is that of `String.prototype.concat`, **not** that of the `+` operator (Spec p.288). A Symbol in `${}` throws `TypeError` **[inference]**. Example: `` `a${1+1}b` `` is `"a2b"`.
- Early errors: `NotEscapeSequence` in an untagged template; more than 2^32−1 elements (Spec p.285).
- Template object (Spec p.286–287): for each code location and per Realm, a frozen array with the cooked strings and a `raw` property (non-enumerable, non-writable, non-configurable) also frozen. The same identity is reused on each evaluation of the same code point; two identical templates in different places get different objects **[inference]**. Lazy or eager creation is unobservable.

---

## 6. Left-hand-side expressions

### 6.1 Hierarchy
- `MemberExpression` (`[ ]`, `.`, tagged template, `super.x`, meta-properties, `new X(args)`, `.#private`), `NewExpression`, `CallExpression` (includes `super(...)` and `import(...)`), `OptionalExpression` (Spec p.289–290). Arguments allow a trailing comma and spread (Spec p.290).

### 6.2 Member access (Spec p.291–293)
- `a.name` is equivalent to `a["name"]`. Order: evaluates the base, applies GetValue, evaluates the key; the result is a Reference.
- `ToPropertyKey` of the key does **not** happen right after evaluating the key: in `a[b] = c`, the conversion only happens after evaluating `c` (Spec p.293). Observable if `b` is an object with a side-effecting `toString`.
- `a.#x` produces a private reference (Spec p.292).

### 6.3 `new`
- Evaluates the constructor, then the arguments (`new X` is equivalent to an empty list), and only then checks whether it is a constructor; if not, `TypeError`. The check happens **after** evaluating the arguments (Spec p.293).

### 6.4 Calls
- Direct eval: a call whose callee is the identifier `eval` (not a property) and whose value is the intrinsic `%eval%`. With no arguments it returns `undefined`; otherwise it executes the first argument inheriting the caller's strict mode (Spec p.294).
- `this`: in `obj.f()` it is the base object; for a variable coming from a `with` environment, it is the `with` object; without a Reference, it is `undefined` (Spec p.294). `(0, obj.f)()` loses `this` because the comma returns a value, not a Reference **[inference]** (Spec p.324).
- A non-object or non-callable value: `TypeError`, after evaluating the arguments (Spec p.294).
- Tail position: see 11.10 **[VERSION-DEPENDENT]**.

### 6.5 `super`
- `super.x` and `super[expr]` require `this` to be already bound; the Reference has as its base the prototype of the home object and the current `this`. In `super[b] = c`, the key is only converted after evaluating `c`. Before `super()` in a derived constructor, reading `this` fails (probably `ReferenceError`, **[inference]**) (Spec p.295–296).
- `super(...)`: uses `new.target`, looks up the parent constructor as the prototype of the active function, evaluates arguments, `TypeError` if the parent is not a constructor, constructs with the same `new.target`, binds `this` to the result (error if already bound, so `super()` twice fails) and initializes the instance fields (Spec p.295).
- `delete super.x` throws `ReferenceError` (Spec p.304).

### 6.6 Arguments and spread
- Evaluated from left to right; `...x` uses a synchronous iterator; a non-iterable fails in `GetIterator` (Spec p.296). In a tagged template, the list is the template object followed by the values of the substitutions (Spec p.296–297).

### 6.7 Optional chaining `?.`
- Form: after `?.` can come `(args)`, `[expr]`, `.name`, `.#private` (Spec p.290).
- If the value to the left of `?.` is `undefined` or `null`, **the whole chain** results in `undefined` and the rest is not evaluated; only those two values trigger the short-circuit (`0`, `""`, `false` continue) (Spec p.297–298).
- `a?.b()` preserves `this` equal to `a` (Spec p.298).
- Early errors: `?.` followed by a template literal is a `SyntaxError`, to avoid strange ASI (Spec p.291). `delete this.#x` in an optional chain too (Spec p.304).

### 6.8 Tagged template
- A call whose arguments derive from the template (template object and values). It uses the same call logic; a non-callable tag raises `TypeError`. Accepts `MemberExpression` and `CallExpression` as the tag (Spec p.300–301).

### 6.9 `new.target` and `import.meta`
- `new.target` returns the NewTarget of the current function (Spec p.301). In a Script, `new.target` is only accepted in direct `eval`; in a module it is always a `SyntaxError` (Spec p.398, p.402).
- `import.meta`: only with the Module goal, otherwise `SyntaxError` (Spec p.291). Object created once per module, with prototype `null`, empty by default, filled by the host (Spec p.301, p.423). **[HOST]**

### 6.10 Dynamic `import()`
- Always returns a Promise. Failures converting the specifier and options **reject** the promise; they do not throw synchronously (Spec p.299).
- Second argument: if it is neither `undefined` nor an object, it rejects with `TypeError`; reads `options.with`, which if present must be an object; each attribute value must be a string; an attribute not supported by the host rejects with `TypeError` (Spec p.299).
- Resolves with the module's namespace object; any load, link or evaluation failure rejects (Spec p.300). Loading is host-defined **[HOST]**. Use `await` with `try/catch` or `.catch` **[inference]**.

---

## 7. Operators

### 7.1 Update `++` and `--`
- Postfix (no line break before the operator) and prefix. `SyntaxError` if the target is not a valid assignment target (Spec p.302).
- Converts with `ToNumeric`, adds or subtracts 1 (or `1n` for BigInt), writes back. Postfix returns the old value **already converted** (`x = "5"; x++` returns the number 5); prefix returns the new one (Spec p.302–303).
- A "web-compat" target (for example a function call in hosts that tolerate it) throws `ReferenceError` at runtime **[HOST]** (Spec p.302–303).

### 7.2 Unary (Spec p.303–306)
| Operator | Observable semantics |
|---|---|
| `delete` | an operand that is not a Reference or is unresolvable returns `true`; `delete super.x` throws `ReferenceError`; the base goes through `ToObject`, the key through `ToPropertyKey`, calls `[[Delete]]`; if it returns `false`, in strict it throws `TypeError` (non-configurable property), in sloppy it returns `false` (Spec p.304) |
| `void` | evaluates with GetValue (effects occur) and returns `undefined` (Spec p.305) |
| `typeof` | `undefined`, `object` (includes `null`), `string`, `symbol`, `boolean`, `number`, `bigint`, `function` (object with `[[Call]]`), `object`; an unresolvable reference returns `"undefined"` without throwing (Spec p.305) |
| `+` | `ToNumber`; BigInt throws an error **[inference]** (Spec p.305) |
| `-` | `ToNumeric`, preserves the type; negates `+0` to `-0` (Spec p.305–306) |
| `~` | `ToNumeric`, bitwise NOT according to Number or BigInt (Spec p.306) |
| `!` | inverted `ToBoolean`, always a boolean (Spec p.306) |
| `await` | only with `[+Await]` (Spec p.303) |

- Early errors of `delete` in strict: applying it to a simple identifier or a private field (`delete this.#x`), including through parentheses (`delete (((foo)))`) (Spec p.304).
- `typeof` in hosts with the `[[IsHTMLDDA]]` slot returns `"undefined"` for that object (optional normative step) **[HOST]** (Spec p.305). `typeof null` is `"object"` (Spec p.305).

### 7.3 Exponentiation, multiplicative, additive, shifts
- `**`: the left side is `UpdateExpression`, not `UnaryExpression`; so `-2 ** 2` requires parentheses **[inference]**, and right recursion makes `a ** b ** c` group as `a ** (b ** c)` **[inference]** (Spec p.306).
- `*`, `/`, `%` and `-` delegate to the generic binary evaluator (Spec p.307).
- `+` concatenates or adds (rules in 7.4). `<<`, `>>` (fills with the sign), `>>>` (fills with zeros); `>>>` with BigInt throws an error (probably `TypeError`, **[inference]**) (Spec p.308, p.317).

### 7.4 Common rules of binary operators (Spec p.317–318)
1. Only `+`: converts both with `ToPrimitive` without a hint; if either results in a string, converts both with `ToString` and concatenates.
2. Other cases (and `+` without a string): `ToNumeric` on both.
3. Different types (Number versus BigInt): `TypeError`.
4. BigInt: `**`, `/`, `%` and `>>>` may throw (division by zero, negative exponent; the exact error type is not on this page).
- `ToPrimitive` without a hint treats it as `number`, except `Date`, which treats it as `string` (Spec p.318). Example **[inference]**: `date + 1` concatenates, `({valueOf(){return 1}}) + 1` adds.
- Concatenation uses "or" (one string is enough); relational string comparison uses "and" (both) (Spec p.318).
- The left is evaluated (with GetValue) before the right (Spec p.318).

### 7.5 Relational (Spec p.308–310)
- The result is always a boolean. The `[In]` parameter prevents confusing the relational `in` with that of `for (x in obj)` (Spec p.309).
- `<`, `>`, `<=`, `>=` evaluate left then right; the order of `ToPrimitive` follows the writing order, even in `>` and `<=` (operands swapped internally). An undefined result (for example `NaN`) gives `false` in all four operators; therefore `NaN <= NaN` is `false` **[inference]** (Spec p.309).
- `instanceof` (Spec p.310): non-object target, `TypeError`; uses the `Symbol.hasInstance` method if it exists (result via `ToBoolean`); otherwise, a non-callable target raises `TypeError`; otherwise compares via the prototype chain through `prototype`. The final step exists for compatibility with editions without `Symbol.hasInstance`.
- `in` (Spec p.310): non-object right side, `TypeError` (`"a" in "str"` fails **[inference]**); considers own and inherited properties.
- `#field in object`: non-object right side, `TypeError`; returns `true` if the object has the private element; requires being inside a class that declares the name (Spec p.310).

### 7.6 Equality (Spec p.310–312)
- The result is a boolean. `==`/`!=` use abstract equality; `===`/`!==` the strict one. Invariants: `A != B` is equivalent to `!(A == B)`; `A == B` is equivalent to `B == A`, except for evaluation order (Spec p.311).
- Not transitive: `new String("a") == "a"` and `"a" == new String("a")` are `true`, but `new String("a") == new String("a")` is `false` (Spec p.312).
- Strings compare by UTF-16 code units, without canonical equivalence (Spec p.312).

### 7.7 Bitwise, logical, conditional, comma
- `&` (highest precedence), `^`, `|` (lowest) (Spec p.312).
- `&&` and `||` always return the value of one of the operands (not necessarily a boolean): `&&` returns the left if falsy; `||` returns the left if truthy. `??` returns the left if it is neither `undefined` nor `null` (Spec p.313). `0 || "x"` gives `"x"`; `0 ?? "x"` gives `0` **[inference]**.
- Grammar: `??` does not mix with `&&`/`||` without parentheses **[inference]** (Spec p.313).
- Conditional `?:`: evaluates only the chosen branch; both branches are `AssignmentExpression` (Spec p.314).
- Comma: evaluates the left with GetValue, discards it, returns the right already resolved (Spec p.324).

---

## 8. Assignment and destructuring

### 8.1 Assignment operators
- Forms: `=`, compound (`*= /= %= += -= <<= >>= >>>= &= ^= |= **=`) and short-circuit `&&= ||= ??=` (Spec p.314).
- Early errors (Spec p.314–315): in `=`, an object or array literal on the left side must be reinterpretable as an AssignmentPattern; otherwise, an invalid target is a `SyntaxError`. In compound operators, an invalid target is a `SyntaxError`. In `&&= ||= ??=`, a non-simple target is a `SyntaxError` (destructuring does not apply).
- Simple `=`: evaluates the left Reference first, then the right, then writes; returns the right value (Spec p.315). With a pattern on the left, evaluates the right side first (Spec p.315).
- Function naming: an anonymous function or class on the right gets the name of the identifier on the left; does not apply to `obj.prop = function(){}` **[inference]** (Spec p.315).
- Compound: reads the left value **before** evaluating the right (Spec p.315). In `x += f()`, if `f` changes `x`, the old value is used **[inference]**.
- Short-circuit (Spec p.316): `a &&= b` neither writes nor evaluates `b` if `a` is falsy; `a ||= b`, if `a` is truthy; `a ??= b`, if `a` is not nullish. In those cases setters and proxies are not triggered, unlike `a = a && b` **[inference]**. Function naming works with an identifier target.
- Strict mode (Spec p.317): an unresolvable reference raises `ReferenceError`; a data property with `writable: false`, an accessor without `set` or a new property on a non-extensible object raise `TypeError`.
- A web-compat target throws `ReferenceError` **[HOST]** (Spec p.315).

### 8.2 Early errors of assignment patterns (Spec p.318–319)
- The shorthand `{ a = 1 }` requires the identifier to be a simple target; `...target` in an object pattern cannot be another array/object literal; a non-literal target must be simple.
- Pattern grammar: `ObjectAssignmentPattern` and `ArrayAssignmentPattern`, with initializers, elisions and `...rest` (Spec p.318–319).

### 8.3 Destructuring semantics (assignment)
- Object pattern (Spec p.319–323): starts with `RequireObjectCoercible`; `null` or `undefined` on the right throw `TypeError`, **even with an empty pattern `{}`**. Each property is read with `GetV` (works on primitives); the initializer only fires when the value read is `undefined` (not `null`). `key: target` evaluates the key and writes to the target. Object rest creates a plain object and copies own properties except the keys already used.
- Array pattern (Spec p.320–323): obtains a **synchronous** iterator; a non-iterable source fails in `GetIterator`; an empty `[]` still opens and closes the iterator. Elision advances without keeping; an exhausted element becomes `undefined` and fires the initializer; rest consumes the remaining iterator into a new array.
- Closing: if the iterator did not finish at the end, or if there was an error in the middle, it calls `IteratorClose` (the `return` method); if it already finished, it does not close (Spec p.320–321).
- Order: for targets that are not nested patterns, the target's reference is evaluated before accessing the iterator or the initializer (Spec p.323).
- Examples **[inference]**: `[a, b] = [b, a]` swaps; `({x = 5} = {})` uses the default 5.
- Return of the assignment expression with a pattern: the right-hand side's value (Spec p.315).

---

## 9. Evaluation order (cross-cutting summary)

| Situation | Observable order | Page |
|---|---|---|
| Generic binary | left (GetValue), then right | Spec p.318 |
| `a[b] = c` | base, key, `c`, only then `ToPropertyKey(b)` | Spec p.293 |
| Simple `=` | left Reference, right, write | Spec p.315 |
| `=` with a pattern | right first, then the pattern | Spec p.315 |
| Compound `op=` | reads left, evaluates right, applies, writes | Spec p.315–316 |
| `new X(args)` | constructor, arguments, then checks whether it is a constructor (`TypeError`) | Spec p.293 |
| Call | callee, arguments, then checks whether it is callable (`TypeError`) | Spec p.294 |
| Arguments and arrays | left to right | Spec p.278, p.296 |
| Relational | `ToPrimitive` follows the writing order | Spec p.309 |
| Object literal | definitions in order; key before value | Spec p.282–283 |
| Template | substitutions from left to right | Spec p.287–288 |
| Destructuring of a simple target | target reference before the iterator/initializer | Spec p.323 |
| `for (let ...)` | new environment per iteration created before the increment | Spec p.337 |

---

## 10. Statements and declarations

### 10.1 Overview (Spec p.324–325)
- `Statement`: block, `var`, empty, expression, `if`, loops and `switch`, `continue`, `break`, `return` (only inside a function), `with`, label, `throw`, `try`, `debugger`. `Declaration`: functions (ordinary, generator, async, async generator), class, `let`/`const`.
- Generator, async and async generator declarations, when "executed" in sequence, return empty: they were already instantiated at the start of the scope (Spec p.325).

### 10.2 Block `{ }`
- Creates a new declarative lexical environment, instantiates the block's declarations in it and **always** restores the previous environment, whatever the exit (Spec p.326).
- Early errors (Spec p.326): duplicate lexically declared names; a lexical name also declared with `var` in the same block. Web-compat exception: in a browser (or a host with that semantics), non-strict code, duplicates coming only from `function` are not an error. **[HOST]/[DATED]**
- Instantiation (Spec p.326–327): `const` creates an immutable binding; `let`, `class` mutable and **uninitialized** (TDZ); functions are instantiated and initialized on block entry (hoisting inside the block). There is web-compat variation for functions in blocks (Spec p.327). **[HOST]**
- Value of a statement list: that of the last item that produces a value; `eval("1;;;;;")`, `eval("1;{}")` and `eval("1;var a;")` return 1 (Spec p.326).

### 10.3 `let` and `const`
- The variables are created when the environment is instantiated, but **cannot be accessed** until the `LexicalBinding` is evaluated (temporal dead zone, TDZ). The initializer's value is assigned when the binding is evaluated. `let x;` without an initializer receives `undefined` on evaluation (Spec p.327).
- Form: an identifier with an optional initializer, or a destructuring pattern with a mandatory initializer (Spec p.328).
- Early errors: a bound name equal to `"let"`; duplicate names in the same declaration; `const` without an initializer (Spec p.328).
- An anonymous initializer function gets the binding's name (Spec p.328). Reading `x` before `let x = 1` throws `ReferenceError` **[inference]** (Spec p.327 only describes the inaccessibility).

### 10.4 `var`
- Belongs to the `VariableEnvironment` of the execution context, created at instantiation and initialized with `undefined`; several declarations of the same name in the same scope define a single variable. The initializer is assigned when the declaration is executed (Spec p.328). `var x;` without an initializer does nothing at runtime (Spec p.329).
- Inside `with`, a `var` with the same name as a property of the `with` object assigns to the property (Spec p.329). **[DATED]**

### 10.5 Binding patterns
- Object `{ a, b: c, ...rest }` and array `[a, , b, ...rest]`; elements with a name, nested pattern and initializer; object rest requires an identifier, array rest accepts an identifier or a pattern (Spec p.330).
- The default value only fires with `undefined`; an anonymous default function gets the target's name (Spec p.331–332). A `null`/`undefined` source in an object pattern fails as in destructuring (8.3); the binding text is outside the excerpt read **[inference]**.
- `environment = undefined` means use `PutValue` (occurs in `var` and in parameters of non-strict functions) (Spec p.331, p.340).

### 10.6 Empty statement and expression statement
- `;` does nothing (Spec p.332).
- An expression statement **cannot start** with `{`, `function`, `async function` (with no line break between the two), `class`, nor with the sequence `let [` (Spec p.332). For an IIFE or an object literal at the start of a statement, use parentheses **[inference]**.

### 10.7 `if`
- `else` associates with the innermost `if` (Spec p.333). Evaluates `ToBoolean`; the statement's value is that of the branch or `undefined` (visible via `eval`) (Spec p.333).
- A body that is a labelled function: `SyntaxError` only if extension B.3.1 is implemented (Spec p.333). **[DATED]**

### 10.8 Loops
- `LoopContinues` (Spec p.334): `continue` without a label, or with a label belonging to the loop's label set, continues; other cases exit and propagate. `continue label` jumps to the correct outer loop **[inference]**.
- `do-while`: the body runs at least once; the production ends with `;` (with a special ASI rule, see 4.1(c)). `while`: tests before each iteration. Loop value: the last non-empty value of the body, starting at `undefined` (Spec p.334–335).
- Classic `for` (Spec p.336–337): three forms (expression, `var`, lexical declaration). The initial expression cannot start with `let [` and uses `[~In]`. Early error: the lexical declaration's name also `var` in the body. With `let`, each iteration has its own copy of the bindings: `CreatePerIterationEnvironment` copies the last value to a new environment **before** the increment. Closures in `for (let i...)` capture one `i` per iteration and do not see the later `i++` **[inference]**; with `var` there is only one variable. With `const` the per-iteration list is empty.
- `for-in`, `for-of`, `for-await-of` (Spec p.338–343):
  - Target: LHS expression (includes pattern), `var ForBinding` or `let/const ForBinding`. `for-in` takes `Expression`; `for-of` and `for-await` take `AssignmentExpression` (no bare comma) **[inference]**.
  - Lookahead: in `for-in` the LHS does not start with `let [`; in `for-of`, not with `let` nor `async of`; in `for await`, not with `let`. `for await` only with `[+Await]` (Spec p.338).
  - Early errors: a literal LHS must be reinterpretable as a pattern; in a lexical declaration, the name `"let"`, a name also `var` in the body, duplicate names (Spec p.339).
  - Evaluation of the right side of a lexical declaration occurs in an environment with the names uninitialized: `for (let x of x)` fails due to TDZ **[inference]** (Spec p.341).
  - `for-in`: a value of `undefined` or `null` ends the loop without an error; otherwise it converts to an object (primitives become wrappers) (Spec p.341–342). `for-of` uses a synchronous iterator; `for await` an asynchronous one; a non-object `next` result throws `TypeError` (Spec p.342).
  - Lexical binding: new environment per iteration; closures in `for (const x of list)` capture the value of that iteration **[inference]** (Spec p.342–343).
  - Closing: if the assignment fails or the body exits in a way that does not continue the loop (`break`, `return`, `throw`, external `continue`), `of`/`await of` call `IteratorClose`/`AsyncIteratorClose`; `for-in` only propagates (Spec p.343).
  - Annex B.3.5 extends these productions (Spec p.338, p.340–341). **[DATED]**, content not detailed in the sources read.

### 10.9 `for-in`: what is enumerated
- Only string keys (never symbols); properties deleted before being visited are ignored; those added during enumeration may not be visited; each name appears at most once; includes inherited ones going up the chain; a prototype property with the same name as one already processed is ignored **even if the object's one were non-enumerable** (Spec p.343).
- Deterministic order (behaving like `CreateForInIterator`) if neither the object nor the chain is a Proxy, TypedArray, module namespace or host exotic object, until there is: a `[[Prototype]]` change, property removal, an addition to an object of the prototype chain or an `enumerable` change (Spec p.343–344). The order of integers and strings comes from `[[OwnPropertyKeys]]`, outside the excerpt read.
- To get only own properties you must filter **[inference]**. The for-in iterator is never accessible to code (Spec p.344–345).

### 10.10 `continue` and `break`
- `continue` generates a CONTINUE completion (with or without a label); it must be inside a loop, without crossing a function or a class static block; `continue` inside a `switch` outside a loop is a `SyntaxError` (Spec p.346).
- `break` accepts a loop or `switch`; same function/static block limit (Spec p.346).
- No line break before the label in either (Spec p.346). A nonexistent or duplicate label is a static error (Spec p.360, p.377).
- A loop or `switch` converts a target-less BREAK into a normal completion; a labelled statement converts a BREAK with its label (Spec p.351–352). Example **[inference]**: `outer: for (...) { for (...) { continue outer; } }`.

### 10.11 `return`
- Without an expression returns `undefined`; no line break between `return` and the expression (Spec p.347). In an async generator, the value goes through `await` before returning (Spec p.347).
- Inside `try`, the `return` can be replaced by the `finally` completion: `try { return 1 } finally { return 2 }` results in 2 **[inference]** (Spec p.347, p.354).

### 10.12 `with` [DATED]
- The Spec marks `with` as legacy and discourages its use, suggesting alternatives valid in strict, such as destructuring (Spec p.347).
- Adds an Object Environment Record based on `ToObject(expression)` (`null`/`undefined` throw), executes and **always** restores the environment (Spec p.347–348).
- `SyntaxError` in strict code (therefore in modules and classes) (Spec p.347, p.376). Labelled-function body: error only with B.3.1 (Spec p.347–348).
- Result: that of the inner statement, with empty replaced by `undefined` (Spec p.348).

### 10.13 `switch`
- Evaluates the discriminant once and compares it with each `case` **in code order** by strict equality; the `case` expressions are only evaluated up to the first match (Spec p.349–350). `'1'` does not match `1` **[inference]**.
- After the match, it executes and **continues** through the following ones (fall-through) until an abrupt completion (Spec p.349).
- `default` in any position: first tests the `case`s before it, then the later ones; if none matches, it executes `default` and falls through the following ones (Spec p.349–350).
- The body is **a single scope**: `let x` in two `case`s is a `SyntaxError` (duplicate) (Spec p.348, p.350). Early errors: duplicate lexicals; lexical equal to `var`; legacy web exception for functions (Spec p.348). **[HOST]/[DATED]**
- Value: the last non-empty value produced (Spec p.349).

### 10.14 Labels
- Labels serve only `break`/`continue`; **ECMAScript has no `goto`** (Spec p.351). They can be stacked; the set makes up the current label set (Spec p.351).
- A labelled function declaration is a `SyntaxError`, except in non-strict code in a browser (or a host with "Labelled Function Declarations") (Spec p.351). **[HOST]/[DATED]**

### 10.15 `throw`
- Evaluates the expression and produces a throw completion; no line break between `throw` and the expression (Spec p.352–353). Any value can be thrown **[inference]**.

### 10.16 `try`
- Forms: `try…catch`, `try…finally`, `try…catch…finally`. The `catch` parameter can be omitted (`catch { }`) or be an identifier or a destructuring pattern (Spec p.353).
- Early errors: duplicate names in the parameter; a name equal to a lexical declaration of the block; equal to a `var` of the block (tolerated only for a simple identifier in a browser/host with VariableStatements in catch blocks) (Spec p.353). **[HOST]/[DATED]**
- The `catch` creates a new scope with the mutable name(s); if the parameter's destructuring throws, it restores the environment and propagates (Spec p.353–354).
- `finally` always runs. Ending normally, the result of the `try`/`catch` prevails; ending abruptly (`return`, `throw`, `break`, `continue`), it **replaces** the previous one, swallowing the exception or return (Spec p.354). Empty becomes `undefined`.
- Example **[inference]**: `try { f() } catch ({ message }) { log(message) }`.

### 10.17 `debugger`
- Triggers the environment's debugging facility, if one exists; otherwise it has no observable effect (Spec p.354–355). **[HOST]**

---

## 11. Functions

Overview: ECMAScript functions are created by several language elements; evaluation starts from the internal method `[[Call]]` (Spec p.355).

### 11.1 Parameters
- The list can be empty, only `...rest`, normal ones, or normal ones followed by `...rest`. Each element is a simple name, one with a default value, or a destructuring pattern (Spec p.355–357).
- Duplicates: `UniqueFormalParameters` (methods, arrows, setters) forbids them. In ordinary `FormalParameters`, duplicates are only allowed if the list is simple **and** the function is not strict (Spec p.355). **[DATED]** in the sense of sloppy legacy.
- **Simple** list (`IsSimpleParameterList`): only names, no defaults, no destructuring, no rest; an empty list is simple (Spec p.357–358).
- `ContainsExpression`: true if there is a default value or a computed key in a pattern (Spec p.356–357).
- Expected count (basis of `length` **[inference]**): counts the parameters to the left of the first one with a default or rest; parameters without a default after one with a default are optional (value `undefined`) but do not count; a single-identifier arrow counts 1; a setter with a default counts 0 (Spec p.359). Example **[inference]**: `function f(a, b = 1, c) {}` has count 1.
- `"use strict"` in the body of a function with a non-simple list is a `SyntaxError` (Spec p.360; analogous in methods p.365, generators p.369, async generators p.373, async p.388).

### 11.2 Function declaration and expression
- Forms: `function name(params) { body }` and `function [name](params) { body }` (expression). An anonymous declaration only exists in `export default` (Spec p.360–361).
- Early errors (Spec p.360): `UniqueFormalParameters` rules if the parameters are strict; the name `eval`/`arguments` in strict; `"use strict"` with non-simple parameters; a parameter repeated as a lexical declaration (`let`/`const`/`class`) of the body (`var` and `function` do not count); `super` (property or call) forbidden in ordinary functions; duplicate lexicals or ones conflicting with `var`; duplicate labels; nonexistent `break`/`continue` targets.
- Reaching the end without `return` returns `undefined`; an empty body too (Spec p.361, p.363).
- Ordinary functions have their own `this`, are constructors and receive an automatic `prototype`, even if never used as a constructor (Spec p.361–363).
- **Named** function expression: the name creates an extra environment with an immutable binding, visible only inside the body (recursion), without affecting the outer scope; an anonymous expression gets the name of the context or empty (Spec p.362).
- Function declarations have empty evaluation (instantiated at hoisting); declarations in blocks have an alternative web-compat mechanism (Spec p.362). **[HOST]/[DATED]**

### 11.3 Arrow functions
- Form: `params => body`; a single parameter as an identifier or a parenthesized list; expression body (cannot start with `{`) or block (Spec p.363). No line break before `=>` (Spec p.363).
- Parameters follow `UniqueFormalParameters` (no duplicates). Early errors: `yield`/`await` in the parameters; `"use strict"` with non-simple parameters; conflict with lexicals of the body (Spec p.363).
- An expression body returns the expression's value (Spec p.364–365).
- It has no own bindings for `arguments`, `super`, `this`, `new.target`; it resolves them in the outer lexical environment. Even when referencing `super`, the arrow does not become a method (Spec p.364).
- It does not receive a `prototype` and is not a constructor **[inference]** (Spec p.364, in contrast with p.361–362).
- To return an implicit object literal, parentheses are required **[inference]** (Spec p.363). Example: `const double = x => x * 2;`.

### 11.4 Methods, getters and setters
- Forms: normal, generator `*`, `async`, `async *`, `get`, `set` (Spec p.365).
- Getter: no parameters. Setter: exactly one formal parameter (Spec p.365).
- Early errors: `"use strict"` with non-simple parameters; conflict of parameters with lexicals of the body; duplicate names in the setter (Spec p.365). `super()` only in the `constructor` of a class with inheritance (Spec p.365–366, p.376).
- Methods receive a "home object", which enables `super.prop` (Spec p.366–367). They are defined as configurable; getters/setters via `DefinePropertyOrThrow`; private getters and setters become private elements of the accessor kind (Spec p.367).
- Methods are not constructors **[inference]** (Spec p.366–368). Generators and async generators get a writable, non-enumerable, non-configurable `prototype` (Spec p.367–368). Async methods have the prototype of `AsyncFunction` (Spec p.368).

### 11.5 Generators (`function*`)
- The body allows `yield` (without a value, with a value, or `yield*`). No line break between `yield` and the operand (Spec p.368).
- `yield` **cannot** appear in the parameters, because the parameter expressions are evaluated before the generator is in a resumable state (Spec p.369). Other early errors are analogous to those of ordinary functions; a generator method cannot have `super()` (Spec p.369).
- **Calling** a generator does not execute the body: it instantiates the parameters, creates the generator object suspended at the start and returns it (Spec p.369). Only the first `next()` runs code.
- `prototype` non-enumerable, writable, non-configurable; generators are not ordinary constructors (Spec p.370). Named expression: name visible only inside the body (Spec p.370–371). A bare `yield` produces `undefined` (Spec p.371).
- `yield*` (Spec p.371–372): obtains the operand's iterator (synchronous or asynchronous depending on the generator kind), forwards values received by `next` and returns the final value of the inner iterator. A non-object inner result: `TypeError`. On `throw()`: if the inner one has no `throw`, it closes the inner one and throws `TypeError`. On `return()`: if the inner one has no `return`, it forwards the completion (with `await` in the async case); otherwise it calls the inner `return` and requires an object in the result.
- Example **[inference]**: `function* g() { yield 1; yield* [2, 3]; }`.

### 11.6 Async generators (`async function*`)
- They allow `yield` and `await`. No line break between `async` and `function`. `yield` and `await` forbidden in the parameters (Spec p.372–373).
- Calling creates an async generator object in the initial suspended state, with an internal request queue, and returns it (Spec p.373). `prototype` non-enumerable, writable, non-configurable; an anonymous declaration only in `export default` (Spec p.374). Named expression: local name (Spec p.374–375).

### 11.7 Async functions (`async function`)
- `await` is a keyword when `[Await]` is present: in the body of an async function and in modules; in a Script, outside that, it can still be an identifier (Spec p.387). No line break between `async` and `function` (Spec p.387).
- `await` requires an operand (unlike `yield`) (Spec p.388). `await` in the parameters is a `SyntaxError` (Spec p.387–388).
- Calling always returns a **Promise**; if instantiating the parameters throws (for example, an error in a default value), the promise is **rejected**, there is no synchronous exception (Spec p.389). Not a constructor **[inference]** (Spec p.388–389).
- `await expr` evaluates and suspends until resolution (Spec p.390). Example **[inference]**: `async function f() { return await g(); }`.

### 11.8 Async arrows
- `async x => ...` or `async (a, b) => ...`; expression body or block. No line break between `async` and the parameters, nor before `=>` (Spec p.390).
- Parameters without `yield`/`await`; conflicts and `"use strict"` with non-simple ones are errors. They return a Promise (rejected if the parameters fail) and have lexical `this` (Spec p.390–391).

### 11.9 Comparative summary
| Form | Own `this` | Constructor | `prototype` | Call return |
|---|---|---|---|---|
| `function` | yes | yes | yes | value or `undefined` |
| arrow | no (lexical) | no | no | value |
| method | yes | no | no | value |
| `function*` | yes | no | yes (own) | generator object |
| `async function` | yes | no | no | Promise |
| `async function*` | yes | no | yes (own) | async generator object |
| `async` arrow | no (lexical) | no | no | Promise |

Pages: Spec p.361–364, p.366–368, p.370, p.374, p.388–391. Cells marked "no" for constructor and `prototype` of methods/async/arrows derive from the absence of `MakeConstructor` **[inference]**.

### 11.10 Tail-position calls [VERSION-DEPENDENT]
- The Spec defines when a call is a tail call; version not stated in the sources read, and the excerpt does not say whether engines implement it. **[HOST]** as to practice (Spec p.392).
- Only in **strict code**; only in a function/arrow body; never in generators, async, async generators and async arrows (Spec p.392). The reason: a non-standard extension that allows observing the chain of callers (Spec p.392).
- Tail positions (Spec p.392–397): the `return` expression; both branches of `if…else` (without `else`, no); the body of `with` and of a label; `case`/`default` lists; only the `catch` in `try…catch`; only the `finally` when it exists; the last operand of the comma; both branches of `?:`; only the right operand of `&&`, `||`, `??`; a normal call, with a template or parenthesized; in an optional chain, the last call.
- Not tail: loops, binary/unary operators, `++`/`--`, `**`, `delete/void/typeof/await`, assignments, `yield`, accesses, `new`, literals etc. (Spec p.393–396). Examples **[inference]**: `return 1 + f(x)` is not tail; `return await f()` is not; a call inside `try { return f() }` is not; in sloppy never.
- `PrepareForTailCall` requires releasing or reusing the transient resources of the current function (Spec p.397). The final note says that a tail call should only increase the stack by the difference in record sizes (Spec p.398); it does not claim that every engine complies.

---

## 12. Classes

### 12.1 Form
- `class Name [extends Expr] { elements }`. Elements: methods, `static` methods, fields (`name = value;`), `static` fields, `static { ... }` blocks and a stray `;`. Names can be private identifiers (`#x`) (Spec p.375–376). `extends` accepts `LeftHandSideExpression` (Spec p.375).
- **Every class definition is strict code** (Spec p.376).
- Static block: `await` and `yield` disabled as an expression, `return` not allowed (Spec p.376).

### 12.2 Early errors (Spec p.376–377)
- `super(...)` in the `constructor` of a class without `extends`; more than one `constructor`; a `constructor` getter/setter/generator/async; `super()` in a non-constructor method.
- Duplicate private names, except a getter and setter pair of the same name, both static or both non-static; `#constructor` forbidden.
- A `static` method named `prototype`; a field named `constructor`; a `static` field named `prototype` or `constructor`.
- A field initializer cannot reference `arguments` nor contain `super()`.
- Static block: duplicate/conflicting lexicals, labels, and it forbids `arguments`, `super()`, `await`.
- Every `#name` used (`obj.#x`, `obj?.#x`, `#x in obj`) must be declared in an enclosing class, otherwise a syntax error **[inference]** (Spec p.379–380).

### 12.3 Definition evaluation (observable effect)
- Class name: an immutable binding inside the class, initialized only after all elements are defined **[inference]**; each `#name` becomes a unique Private Name per class evaluation (Spec p.384–385).
- `extends` (Spec p.384): evaluated in the class environment (with the outer private environment); `null` gives a parent prototype `null` and parent constructor `Function.prototype`; a value that is not a constructor raises `TypeError`; a `superclass.prototype` that is neither an object nor `null` raises `TypeError`.
- Default constructor (Spec p.384–385): throws `TypeError` if called without `new`; in a derived class it behaves like `constructor(...args){ super(...args) }` without using the array iterator in an observable way; in a base class, it creates the object from `NewTarget` and initializes the fields. An explicit constructor is marked as a *class constructor*, which cannot be called without `new`, and receives the class name (Spec p.385).
- The class's `prototype` is the created proto object; `proto.constructor` is non-enumerable (Spec p.385).
- Order (Spec p.385–386): (1) non-constructor elements evaluated in code order (computed keys evaluated there); instance methods go to the proto, static ones to the class; (2) private methods/accessors collected, with a private getter and setter of the same name combined; (3) instance fields stored in `[[Fields]]`, static fields and blocks in a list; (4) if anything throws, it restores environments and propagates; (5) initializes the class name and adds static private methods; (6) executes static fields and blocks **in code order**, with the class as `this`.
- Static fields and blocks become inaccessible internal functions, with their own `this` (Spec p.382–383).
- An object has all or none of the private methods/accessors of a class, but may have only some of the private fields, since initializers can throw (Spec p.383–384).

### 12.4 Declaration versus expression (Spec p.386)
- `class Name {}` binds `Name` in the current environment after evaluating the class (TDZ until then, **[inference]**). An anonymous `class {}` only in `export default`, with the name `"default"`. An expression without a name has the name `""`; with a name, visible only inside the class.

### 12.5 Pitfalls
- `extends` of a non-constructor value or with an invalid `prototype`: `TypeError`. Calling a class without `new`: `TypeError` (explicit, via the *class constructor* mark, **[inference]**). `arguments` in a field initializer: `SyntaxError` (Spec p.377, p.384). `super()` twice: fails when binding `this` (6.5).
- Example **[inference]**: `class B extends A { x = 1; static y = 2; #z; }`.

---

## 13. Scripts and modules

### 13.1 Script
- `Script` is an optional `ScriptBody`, without `yield`, `await` or `return` at the top level (Spec p.398).
- Early errors: duplicate lexicals; a lexical also `var`; `super` and `new.target` (except in direct `eval`); duplicate labels; `break`/`continue` without a target; invalid private identifiers (except in direct `eval`) (Spec p.398).
- A Script is strict if the prologue has a Use Strict Directive (Spec p.398).
- `ParseScript`: syntax errors can only be reported when the script is loaded, even if the implementation finds them earlier (Spec p.399). `ScriptEvaluation` creates the global context, runs `GlobalDeclarationInstantiation` and only then evaluates; if instantiation throws, the body does not execute (Spec p.399–400).

### 13.2 Global declarations (conflicts between scripts)
- `var` and functions become properties of the global object; `let`/`const`/`class` stay in the global lexical declarations record, in TDZ (Spec p.400–401).
- `SyntaxError` if the new script's lexical name is already a global lexical or collides with a restricted global property (non-configurable global `var`/function); `SyntaxError` if the new script's `var`/function name is already a global lexical (Spec p.400). `TypeError` if it is not possible to declare the function or `var` globally (Spec p.400).
- Conflicts between scripts only appear at runtime; if there is an error, no binding of the script is created. Example **[inference]**: script 1 with `let v` and script 2 with `var v` throws `SyntaxError` on instantiating the second (Spec p.400–401).
- A property created directly (`globalThis.x = 1`) can be hidden by `let`/`const`/`class`, unlike `var`/function (Spec p.401).
- With a Proxy global object, tests may be unreliable and leave declarations partially instantiated; the script is not evaluated (Spec p.401).
- **[HOST]/[DATED]**: web semantics of functions in blocks (optional normative step): in a non-strict script, functions declared in blocks/`case` get a global `var` binding if there is no conflict (Spec p.400–401).

### 13.3 Module: grammar and early errors
- `Module` is an optional `ModuleBody`; items: `ImportDeclaration`, `ExportDeclaration`, `StatementListItem`. At the top level, `+Await` (top-level await) and `~Return`, `~Yield` apply (Spec p.402). `ModuleExportName` can be `IdentifierName` or `StringLiteral` (Spec p.402).
- Early errors (Spec p.402): duplicate lexicals; a lexical also `var`; duplicate exported names (therefore more than one `export default`); exporting a nonexistent local name; `super` and `new.target` (no eval exception); labels and targets; invalid privates; a string `ModuleExportName` with a lone surrogate.
- A module is always strict (Spec p.247). Other conflicts are checked at linking; if there is an error, the module is not evaluated (Spec p.402).

### 13.4 `import`
- Forms (Spec p.435–436): `import clause from "x" [with {...}];` and `import "x" [with {...}];`. Clause: default; `* as ns`; list `{ a, b as c }` (trailing comma and empty `{}` allowed); default followed by a namespace or list. The imported name can be a string literal (`"a b" as x`); the local one is always `ImportedBinding`. The specifier is a `StringLiteral`.
- `with { key: "value" }`: the key is `IdentifierName` or a string; the value must be a string literal; trailing comma optional (Spec p.436).
- Early errors: duplicate bound names; two `with` entries with the same key (Spec p.436).
- `import "x"` creates no binding but creates a request: the module is loaded and evaluated (Spec p.404, p.424, p.436).
- Mapping (Spec p.424): `import v from` is importName `"default"`; `import * as ns` is namespace; `import {x as v}` is importName `x`, local `v`.
- Imported bindings are **live** (they point to the source module's binding, they do not copy the value) **[inference]** (Spec p.428–429). `import * as ns` creates an immutable binding with the namespace (Spec p.429).

### 13.5 `export`
- Forms (Spec p.438–439): `export * [as name] from "x" [with ...]`, `export { a, b as c } [from "x"]`, `export var/let/const/function/class`, `export default` of a declaration (function, generator, async, class; the name may be omitted) and `export default AssignmentExpression;` (cannot start with `function`, `async function` or `class`, which would be declarations).
- Early errors in `export { ... }` without `from` (Spec p.439): referencing a string literal is a `SyntaxError`; each name is treated as an `IdentifierReference` (reserved words and `implements interface let package private protected public static` are errors). `export {a as "b c"}` is allowed; `export {"x"} from "m"` too **[inference]**.
- Informative mapping (Spec p.425): `export default 42` and `export default function(){}` use the synthetic name `"*default*"`; `export {v as x}` exports `x` with local `v`; `export * from` has importName ALL-BUT-DEFAULT (does not re-export `default`); `export * as ns from` has importName ALL.
- Rewriting: `export {x}` where `x` was imported becomes an indirect re-export, avoiding false ambiguity in `export *` (Spec p.425–426).
- Evaluation: `export ... from` and `export {...}` do nothing at runtime; `export var/declaration` evaluates the declaration; an anonymous `export default class` initializes `"*default*"` (Spec p.444).

### 13.6 Export resolution
- `ResolveExport` searches: local exports, indirect ones (`export * as ns` returns the namespace), `"default"` never comes from `export *`, then the `export *`s. Two `export *` with the same name pointing to different modules or bindings give `AMBIGUOUS`; the same binding is not ambiguous. A circular import returns `null` (Spec p.427–428).
- An ambiguous name only causes an error when imported explicitly. In the namespace (`import * as ns`), ambiguous names are simply left out, without an error **[inference]** (Spec p.434).
- `GetExportedNames` neither filters nor throws on ambiguity (Spec p.427).

### 13.7 Lifecycle: load, link, evaluate
| Phase | What it does | Failure | Repeatable | Pages |
|---|---|---|---|---|
| Load | `HostLoadImportedModule` fetches and parses each dependency, without duplicates per (specifier, attributes) | the module stays `NEW`; `SyntaxError` if an attribute is unsupported; the host may allow a retry | yes | Spec p.410–411, p.418 |
| Link | creates environments, resolves imports | `SyntaxError` if an import or indirect export does not resolve (nonexistent or ambiguous); modules go back to `UNLINKED` | yes (no effects) | Spec p.411–412, p.428 |
| Evaluate | executes dependencies first, in textual order, depth first | the error is memoized and rethrown on new attempts | **once** | Spec p.413–414, p.417 |

- Status: NEW, UNLINKED, LINKING, LINKED, EVALUATING, EVALUATING-ASYNC, EVALUATED (Spec p.408).
- Evaluation has side effects, so it only happens once, remembering the error; linking is repeatable; loading depends on the host (Spec p.418).
- Requests: `import x from "a"` and `import y from "a" with {type:"json"}` are different requests **[inference]** (Spec p.403).
- Link error: A->B->C with B failing leaves A and B `UNLINKED` and C `LINKED`. Evaluation error: A.Evaluate() rejects; A and B keep the error, C stays `EVALUATED` without an error (Spec p.417).
- Cycles: the second visit is a no-op; strongly connected components go together to `LINKED` (Spec p.418). `[[CycleRoot]]` holds the cycle's promise and error (Spec p.408).

### 13.8 Top-level await
- A module with `await` in the body has `[[HasTLA]]` true; it executes as the body of an async function; importers wait for it (Spec p.426, p.429–430). An async dependency does not make the importer `HasTLA`, but delays its execution (Spec p.408).
- Asynchronous execution: pending-dependency counters and `[[AsyncEvaluationOrder]]` define the order of **start** (not of finish); an error in a module with TLA rejects the promise of all those that depend on it, directly or indirectly (Spec p.414–416, p.420).
- Without top-level await, evaluation is synchronous.

### 13.9 Synthetic modules (JSON)
- A module defined by the specification, with fixed export names; no imports. JSON modules export only `default` **[inference]** (Spec p.430). If there is a `type` attribute equal to `"json"`, the host must return the result of `ParseJSONModule` or throw; the Spec does not forbid hosts from accepting JSON without the attribute (Spec p.433).

### 13.10 Host-defined points [HOST]
- Specifier resolution (path, package, extension), I/O, normalization, which attribute keys exist (default: empty list, so a non-empty `with` is an error) and the content of `import.meta` (Spec p.301, p.433–434).
- Context with no active script/module (for example `onclick="import('./foo.mjs')"`): the referrer is the Realm (Spec p.432).
- Hosts must handle the rejection of `Evaluate()` and rethrow the error (Spec p.406).

---

## 14. Divergences, inconsistencies in the sources and passages not to reproduce

### 14.1 Divergences between sources
- There was no cross-check against EJ1 and EJpt in this file, whose content was extracted only from the Spec. Where the EJ1 text (1st edition, `var`, no `let`/`const`/`class`/arrow/Promise) diverges, the Spec prevails, and everything in EJ1 is **[DATED]**.

### 14.2 Internal inconsistencies of the Spec (recorded by the extraction)
- `ScriptIsStrict` for an empty `Script` appears returning `undefined` in an algorithm declared as Boolean; it looks like a slip in the source (expected: false) (Spec p.398).
- `[[EvaluationError]]` in the Cyclic Module Record table: the description says "undefined" when there is no exception, but the algorithm uses EMPTY (Spec p.408, p.413). No practical effect.
- The note on the second labelled-function rule in `with` appears split by a page break (Spec p.347–348).

### 14.3 Truncated or noisy passages: do not reproduce
- The excerpt of 13.2.9 (grouping operator) ends in a heading at the end of p.288; use the rule in 5.3 (Spec p.289).
- The list in 12.10.3.2.1 (optional operands with `[no LineTerminator here]`) is truncated on p.273 and does not mention arrows; the complete list of restricted productions is on p.269–270 (use 4.2).
- On p.384–385, the creation of the class name's immutable binding and its late initialization are in separate steps; that this causes an internal TDZ is an inference, not a Spec statement.
- Tables 43–51 and figures 2–5 (p.417–422) lost values in extraction; the order 1, 3, 4 of `[[AsyncEvaluationOrder]]` comes from the prose on p.419 and the value 2 is not made explicit. Do not reproduce counter numbers from that example.
- Formulas with lost superscripts (p.259, p.264, p.278, p.285–286): "232 − 1" is 2^32 − 1.
- The label "NORMATIVE OPTIONAL" (p.305, p.327, p.400) marks steps that only apply in browsers/hosts: treat as **[HOST]**.

---

## 15. Gaps

- Conversion and comparison operations (`ToPrimitive`, `ToNumeric`, `IsLessThan`, abstract equality, `ToPropertyKey`), `CopyDataProperties`, `GetIterator`, `IteratorClose` and the order of `[[OwnPropertyKeys]]` were not detailed; only the edge effects cited.
- The error name (`TypeError` or `ReferenceError`) is not always stated on the pages read: `this` before `super()`, reading in TDZ, unary `+` with BigInt, `>>>` with BigInt, spread of a non-iterable. They are marked as **[inference]**.
- Not covered: Annex B (B.1.1, B.3.1, B.3.5), the details of direct `eval` (19.2.1.1) and the `Function` constructors.
- Versions: the Spec sources read do not date any feature (version not stated in the sources for `let`/`const`, classes, modules, top-level await, import attributes, optional chaining, `??`, private fields, static blocks, tail calls). To date them, consult Annex F (incompatibilities by edition) and EJpt.
- Iterator/generator objects (`next`, `throw`, `return` of generators), Promises and the namespace object (`ModuleNamespaceCreate`) are in other chapters of the Spec.
- EJ1 and EJpt were not consulted for this file; practical usage examples and didactic explanations should come from them.
