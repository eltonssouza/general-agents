# Reference index — javascript-expert

Load **only** the file you need. Every claim cites `(Spec p.N)`, `(EJpt p.N)` or `(EJ1 p.N)`, with the **PDF** page (not the page number printed in the footer).

| Abbreviation | Work | Nature | Caution |
|---|---|---|---|
| Spec | *ECMA-262*, 17th edition (ECMAScript 2026, 876 PDF pages) | official language standard | **almost never states which edition each feature entered** (except for occasional notes and Annexes E and F, p.865–869); p.813–842 (end of the memory model and Annex A, grammar summary) are not distilled here |
| EJpt | *Eloquent JavaScript* in Portuguese (504 PDF pages) | modern book; says it uses "a versão 2024 do JavaScript" (the 2024 version of JavaScript) (EJpt p.9) | the exact edition (4th) is not stated in the text (**[inference]**); it only explicitly dates `class`, `Symbol`, arrow functions and ES modules to 2015, and `var`/CommonJS/IIFE as pre-2015 |
| EJ1 | *Eloquent JavaScript* (file `EN-3ed`, 247 PDF pages) | **1st edition** (2007, revised through Nov 2013; EJ1 p.247) | **everything is [DATED]** (only `var`, no `let`/`const`/arrow/`class`/`Promise`/modules/`JSON.parse`/`Object.create`); the functions `print`, `show`, `load`, `attach` belong to the book's console (**[HOST][DATED]**) |

**Golden rule:**
1. **Hierarchy:** for language semantics, the **Spec prevails**; **EJpt** gives the modern explanation and environment examples (`[HOST]`: browser, DOM, `fetch`, Node.js); **EJ1** is **[DATED]** historical testimony, useful for recognizing legacy code and contrasting it with modern code.
2. **Versions:** being in the 2026 Spec only proves the feature exists in ES2026 (Spec p.25). If neither the Spec (notes, Annex E p.865, Annex F p.867–869) nor the books state the edition in which a feature entered (`?.`, `??`, `#private`, `async`/`await` as syntax, `at`, `toSorted`, `Object.hasOwn`, `Object.groupBy`, `Promise.any`, `Promise.allSettled`, `Promise.withResolvers`, `Float16Array`, `Set.prototype.union`, Iterator helpers, `Uint8Array.fromBase64`, etc.), write **"version not stated in the sources"** — never fill it in with "since ES20XX" from memory without labeling it **[extrapolation]**.
3. **Language vs `[HOST]`:** the Spec does not define input/output, DOM, `window`, `document`, `fetch`, `localStorage`, `setTimeout`, `console.log`, `process`, `node:fs`, `node:http`, CommonJS (`require`/`module.exports`) or NPM (Spec p.26–28, p.863–864; EJpt p.33–34, p.222–229, p.239, p.293, p.459). Mark all of these as **[HOST]**.
4. **Out of scope:** TypeScript (only a passing mention in EJpt p.171), UI/backend frameworks (React, Vue, Angular, Express, Next.js…), specific bundlers/linters, `structuredClone`, `queueMicrotask`, `AbortController`, detailed `Intl` (Spec p.25 only refers to ECMA-402) and `Temporal`.

## Page convention and map

Every citation `(Spec p.N)`, `(EJpt p.N)`, `(EJ1 p.N)` uses the **PDF page** (the N-th page of the file, counting from 1). The source PDFs are in `01_programming_languages/` (one level above `_agents/`):

| Abbreviation | File | Pages | Printed page |
|---|---|---|---|
| Spec | `JavaScript-ECMA-262-Spec.pdf` | 876 | printed = PDF − 24 (p.25 of the PDF prints "1"; p.1–24 are the cover and table of contents). Section titles usually appear in the footer of the page before the algorithm body: when checking a rule, also look at the following page |
| EJpt | `JavaScript-Eloquent-JS-PTBR.pdf` | 504 | the PDF prints no page numbers; only the PDF page exists |
| EJ1 | `JavaScript-Eloquent-JS-EN-3ed.pdf` (it is the 1st edition) | 247 | the PDF prints no page numbers; only the PDF page exists |

Map by topic, at chapter level (PDF pages; the start of each chapter was read in the PDF itself; within a chapter, confirm the term on the page before citing):

| Topic | Spec (clause: pages) | EJpt (chapter: pages) | EJ1 [DATED] (chapter: pages) |
|---|---|---|---|
| Conformance and host | 2–4: p.25–35; Annex D: p.863–864 | 1–2 (environment): p.28–35 | 1: p.1–8 |
| Types, values, coercion, equality | 6–7: p.49–117 | 1: p.13–27 | 2: p.9–29 |
| Grammar, ASI, expressions, statements | 11–14: p.243–354 | 2: p.28–49 | 2: p.9–29 |
| Scope, functions, closures, `this` | 8–9 and 15: p.118–195, p.355–397 | 2–3: p.28–72; 6: p.125–151 | 3: p.30–41 |
| Objects, prototypes, classes | 10, 15 (classes) and 20: p.196–242, p.376–386, p.461–486 | 4: p.73–105; 6: p.125–151 | 4: p.42–67; 8: p.125–166 |
| Arrays and higher-order functions | 23: p.615–674 | 4–5: p.73–124 | 4: p.42–67; 6: p.76–101 |
| Strings and RegExp | 22: p.538–614 | 9: p.188–218 | 10: p.177–184 |
| Numbers, Date, Math, JSON | 21 and 25.5: p.487–537, p.734–745 | 1: p.13–27; 4: p.99–100; 9: p.197–198 | 2: p.9–29 (numbers); 4: p.42–67 (Date, p.57–58); 14: p.230–247 (JSON, p.234) |
| Map, Set and collections | 24: p.675–697 | 6: p.125–151 | (no equivalent) |
| Errors and debugging | 20.5: p.482–487 | 8: p.167–187 | 5: p.68–75 |
| Modules | 16: p.398–444 | 10: p.219–235 | 9: p.167–176 (by convention) |
| Iteration, Promise, `async` | 27 and Jobs: p.186–189, p.749–798 | 6: p.125–151; 11: p.236–263 | (no equivalent) |
| Memory and concurrency | 26 and 29: p.745–748, p.802–814 | (no equivalent) | (no equivalent) |
| Annexes B, C, E, F (legacy, editions) | p.843–862, p.865–869 | p.9, p.32, p.198 | p.6, p.34 |
| [HOST] browser | (outside the standard) | 13–19: p.282–457 | 11–14: p.185–247 |
| [HOST] Node.js and NPM | (outside the standard) | 10 (NPM): p.224–235; 20–21: p.458–504 | (no equivalent) |

Distilled coverage (pages cited in `references/`, not counting this index): Spec 792 of 876 (not cited: p.1–24, cover and table of contents; p.38–40, p.572–574, p.652–655; p.813–842, memory and Annex A; p.871–876, bibliography, colophon and license; plus isolated pages), EJpt 466 of 504 (not cited: p.1–3, p.6–8, p.10–13, p.72–74, p.341–343 and isolated ones) and EJ1 204 of 247 (not cited: p.59–61, p.83–92, p.135–140, p.147–149, p.154–158, p.174–176 and isolated ones). Details and audit: `tests/relatorio-de-fidelidade.md`.

**Practice nomenclature:** TDZ, hoisting, microtask and bubbling are practice vocabulary that does not appear by name in the sources (see `glossario.md`, section 18); use them as a nomenclature **[extrapolation]**, pointing to the page of the mechanism (for example, uninitialized binding in Spec p.167–168, Job in Spec p.186–189).

**Recorded page tolerance:** when a line cites a page and the term sought only appears on the neighboring page (±1), the text was kept if the continuation of the algorithm is on the next page (title in the footer of the previous one). `tests/audit_tokens.py` lists these occurrences as PROXIMA (neighboring page); they are not failures, but they are not an exact check either.

## When to open each file

| Question / task | File |
|---|---|
| "What is X?" (term, concept, Spec jargon, iteration protocol, Job, Realm, `[HOST]`) | `glossario.md` |
| "Which construct should I choose?" (`let`/`const`/`var`, `===`/`==`/`Object.is`, function vs arrow, `class` vs literal vs `Map`, `for-of` vs array methods, `Promise` vs `async/await`, `||` vs `??`, ESM vs CommonJS) | `frameworks.md` |
| "How do I do it step by step?" (debug, write tests, copy without mutating, build a regex, dates, Promises/async, modules, Node `fs`/`http`, DOM/events/canvas) | `procedimentos.md` |
| "Why do I get this error / odd behavior?" / anti-patterns / Annex B / errors in the books themselves | `casos-e-antipadroes.md` |
| Language and Spec types, coercions (`ToPrimitive`, `ToNumber`, `ToBoolean`), equality (`==`, `===`, `SameValue`, `SameValueZero`), scope, hoisting, TDZ, Environment Records, Realms, Jobs, ordinary/exotic objects | `linguagem-valores-e-execucao.md` |
| Lexical grammar, ASI (automatic semicolon insertion), expressions, operators, destructuring, statements, functions, generators, classes, ES modules, Proxy (traps and invariants) | `linguagem-sintaxe-e-estruturas.md` |
| Global objects and general built-ins (`Object`, `Function`, `Boolean`, `Symbol`, `Error` and native types, `Number`, `BigInt`, `Math`, `Date`, `JSON`, `WeakRef`, `FinalizationRegistry`, `Atomics`, `DataView`, `Iterator`, `Promise`, `Reflect`, `Proxy`) | `builtins-objetos.md` |
| Text, collections and buffers (`String`, `RegExp`, `Array`, `TypedArray`, `Uint8Array` base64/hex, `Map`, `Set` and set algebra, `WeakMap`, `WeakSet`, `ArrayBuffer`, `SharedArrayBuffer`) | `builtins-texto-colecoes.md` |
| "Since which version does X exist?", Spec Annexes B/C/E/F, what is `[DATED]` vs modern (EJ1 × EJpt), what is `[HOST]` | `versoes-e-datado.md` (and the skill `js-version-features`) |
| "In which Spec clause/page is X?" | skill `js-spec-lookup` (`scripts/spec_lookup.py`) |

## How to read large files

List the sections with `Grep` (pattern `^#{2,3} `) and read only the relevant section with `Read` (`offset`/`limit`). Before saying that something is "not in the sources", `Grep` the term in **all** files of `references/` and consult `js-spec-lookup`.

## Marking conventions

- **[from source]** claim backed by the cited page (`Spec p.N`, `EJpt p.N`, `EJ1 p.N`). In these references, **a claim with a cited page and no other label counts as [from source]**; everything else is labeled.
- **[DATED]** EJ1 content (1st ed., 2007/2013), `var` as the default, `with`, `__proto__`, legacy octals, Spec Annex B.
- **[VERSION-DEPENDENT]** feature or change that the source ties to a specific edition (e.g., ES2015, ES2017, ES2018, ES2019).
- **[HOST]** defined by the host environment (browser, DOM, Node.js, timers, `fetch`, `console`), not by the ECMAScript standard.
- **[inference]** conclusion obtained by crossing pages or applying a Spec algorithm to a concrete case without the page stating the ready-made sentence (list the base pages).
- **[extrapolation]** knowledge external to the three sources (label it explicitly and recommend confirming in the environment/engine documentation).
- Quotation marks only for short literal quotes from the source (or the exact name of a Spec production/operation); translation, paraphrase and text copied from `references/*.md` go **without quotation marks**.
