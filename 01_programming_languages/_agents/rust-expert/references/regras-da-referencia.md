# Rust Reference rules: map, pitfalls, editions, UB and source limits

Lookup base for the Rust specialist agent, distilled mainly from "The Rust Reference" (Ref). All cited pages are PDF pages, with the source prefix: (Ref p.N), (Book p.N) or (RBE p.N). Points where the original text does not allow a conclusion are marked **[NOT VERIFIED IN THE PDF]**; connections made by this consolidation, and not by the source, carry **[inference]**.

## Contents

1. How to use this file
2. (a) "Where to look" map (topic → pages)
3. (b) Subtle rules and pitfalls by topic
   - 3.1 Lexical and literals
   - 3.2 Macros (macro_rules, hygiene, follow-set, proc macros)
   - 3.3 Items, traits, coherence, dyn compatibility
   - 3.4 Attributes, lints, cfg
   - 3.5 Expressions (evaluation, temporaries, operators, casts)
   - 3.6 Patterns
   - 3.7 Closures
   - 3.8 Types, layout and repr
   - 3.9 Lifetimes, variance, elision, HRTB, coercions
   - 3.10 Drop order and temporaries
   - 3.11 Names, paths, visibility
   - 3.12 Const eval
   - 3.13 Unsafe, UB, FFI, unwinding, inline asm
4. (c) Differences by edition
5. (d) Undefined behavior and guarantees
6. (e) Source limitations and dated content

---

## 1. How to use this file

- The Reference describes the most recent edition in the main text and isolates the differences in "Edition differences" blocks (Ref p.3). That is why section 4 gathers everything in a single table.
- It treats the program as a black box: optimizations are not specified, only the observable behavior must be respected (Ref p.2). When the compiler and the text diverge, the Reference itself asks for an issue; the text is not absolute truth (Ref p.1).
- Almost no rule id (`lex.token...`, `items.traits...`) survived the extraction; always cite by page.

## 2. (a) "Where to look" map

### Reference (Ref)

| Topic | Ref pages |
|---|---|
| Introduction, conventions, rule ids | 1–4 |
| Grammar notation (hard cut `^`) | 5–7 |
| Input format (UTF-8, BOM, CRLF, shebang) | 9–11 |
| Keywords (strict/reserved/weak); list of unused reserved ones | 12–15; 677–679 |
| Identifiers and raw identifiers | 16–17 |
| Comments and doc comments | 18–21 |
| Tokens, suffixes, char/string/raw/byte/C literals | 23–34; semantics in 270–281 |
| Numeric literals, tuple index, float | 34–39 |
| Lifetimes/labels, punctuation, reserved tokens | 39–44 |
| Macro invocation, macros by example | 46–53 |
| Macro scope, `macro_use`, `macro_export` | 53–62 |
| Hygiene and `$crate` | 62–65 |
| Follow-set (summary / formal detail) | 65–66 / 687–695 |
| Proc macros | 67–75 |
| Crates, `main`, `no_main`, `crate_name` | 76–79 |
| Conditional compilation (`cfg`, `cfg_attr`, `cfg!`, `cfg_select!`) | 80–91 |
| Items: modules, extern crate, use | 92–111 |
| Functions (ABI, unwinding by ABI, async) | 112–121 |
| Type aliases, structs, enums | 122–133 |
| Unions | 134–138 |
| Const items, static items | 139–145 |
| Traits (dyn compat, supertraits, unsafe traits) | 146–153 |
| Implementations (orphan, constraining parameters) | 154–159 |
| External blocks (ABI, `link`, `link_name`, `link_ordinal`) | 160–171 |
| Generics, const generics, where clauses | 172–178 |
| Associated items, GATs, associated consts | 179–188 |
| Attributes (syntax, built-ins, index) | 190–197 |
| `test`/`ignore`/`should_panic`, `derive` | 198–205 |
| Lints, `deprecated`, `must_use`, `#[diagnostic]` | 206–221 |
| `inline`/`cold`/`naked`, `target_feature` (tables 228–238), `track_caller`, `instruction_set` | 222–243 |
| `recursion_limit`, `non_exhaustive`, debugger attrs | 244–255 |
| Statements and expressions (precedence, place/value) | 257–269 |
| Blocks, async, const, unsafe blocks | 283–290 |
| Operators (overflow, borrow, deref, `?`) | 291–302 |
| `as` | 302–311 (+319) |
| Assignment | 312–318 |
| Array, index, tuple, struct expr, calls, methods, fields | 320–337 |
| Closures (expression) | 338–340 |
| Loops, labels, ranges, `if` | 341–356 |
| let chains, `match`, `return`, `.await`, `_` | 357–367 |
| Patterns | 368–391 |
| Types (list, primitives, compound, closures, pointers, trait objects, impl Trait, DST) | 393–448 |
| Layout and `repr` | 449–463 |
| Interior mutability, subtyping/variance, bounds/HRTB | 464–473 |
| Coercions, divergence/fallback | 474–483 |
| Destructors, drop scopes, lifetime extension | 484–497 |
| Lifetime elision | 498–502 |
| Special types and traits | 503–507 |
| Names, namespaces, preludes, `no_std` | 508–527 |
| Paths | 529–539 |
| Name resolution (imports, globs, macros, ambiguities) | 540–552 |
| Visibility and privacy | 554–560 |
| Memory model | 561–563 |
| Panic | 564–567 |
| Linkage | 569–575 |
| Inline assembly | 576–619 (registers 586–598; options 603–608; rules 608–612) |
| Unsafety | 620–623 |
| Undefined behavior / not considered unsafe | 624–631 |
| Constant evaluation | 632–637 |
| ABI (`used`, `no_mangle`, `link_section`, `export_name`), runtime | 638–643 |
| Appendices: grammar 645–676; syntax index 677–686; follow-set 687–695; tests 697–701; glossary 702–710 | see items |

Shortcuts: operators and symbols in Ref p.679–681; register class tables and allowed types in Ref p.587–596; guaranteed assembler directives in Ref p.616–619; definitions of blanket impl, fundamental, uncovered, turbofish, ZST and DST in Ref p.702–710.

### Rust by Example (RBE), page map only

Hello/comments 3–5; formatting 6–18; primitives 19–27; custom types 28–39; bindings 40–44; casting/inference/alias 45–51; conversions 52–58; expressions 59; control flow (`match`, `if let`, `let-else`, `while let`) 60–87; functions and closures 88–111; modules 112–124; crates 125–127; Cargo 128–136; attributes/`cfg` 137–142; generics 143–165; scope, RAII, ownership, borrowing 166–180; lifetimes 181–194; traits 195–220; `macro_rules!` 221–231; errors 232–269; std types 270–298; std misc (threads, channels, fs, processes) 299–326; FFI 327–329; tests 330–342; `unsafe` 343–344; `asm!` 345–356; raw identifiers 357–358; rustdoc 359–364. In this material only the page map was distilled (RBE p.3–364); the rules come from the Reference. Exception: the RBE criteria for error types and for multiple error types (RBE p.257–269) are recorded in procedimentos.md, section 12.

---

## 3. (b) Subtle rules and pitfalls by topic

### 3.1 Lexical and literals

**Grammar and input**
- The grammar is a PEG: ordered alternatives with backtracking; the `^` operator is a hard cut (once the left side has matched, the rest must match or the parse fails). Example: `c"\0"` fails as a C string because NUL is forbidden; without the cut it would be re-lexed as the identifier `c` followed by a string (Ref p.6–7).
- Source is UTF-8; an invalid file is an error (Ref p.9). Normalizations: BOM at the start, CRLF to LF (a single pass: "CR CR LF LF" still leaves CR+LF) and shebang removal (Ref p.9–10). A lone CR becomes whitespace (Ref p.10).

**Keywords and identifiers**
- Strict and reserved keywords cannot be used as the name of an item, variable, field, variant, parameter, label, macro, attribute or crate (Ref p.12–14). Weak ones (`'static`, `macro_rules`, `raw`, `safe`, `union`) only apply in context; `union` can still be a variable or method; `raw` is only a keyword in `&raw const/mut` (Ref p.14–15).
- `r#` frees a keyword to be used as an identifier, except `r#_`, `r#crate`, `r#self`, `r#Self`, `r#super` (Ref p.16–17). The `_` prefix only silences the "unused" warning; a lone `_` is a keyword (Ref p.12, 17).

**Comments**
- Outer doc: `///` with exactly 3 slashes and `/** */` with exactly 2 asterisks; `////` and `/***` are ordinary comments; `//!` and `/*!` are inner doc (Ref p.19–20). CR is forbidden in doc comments. A dangling `///` at the end of a module is an error (Ref p.21).
- When passing through macros, doc comments become `#[doc = "..."]` (Ref p.75).

**Literals**
- Escapes: `\x` in char/string goes up to `0x7F`; in byte/byte string up to `0xFF`; `\u{...}` accepts up to 6 hex digits with `_` and requires a valid scalar value, and does not exist in bytes (Ref p.24, 27–28, 30, 272). The `\`+LF continuation removes all following whitespace, including blank lines; avoid depending on it (Ref p.272–273). Substitution is left to right: `"\\x41"` stays a literal `\x41` (Ref p.275).
- Raw strings: up to 255 `#`; body without CR; raw byte string ASCII only (Ref p.28–31).
- C string (`c"..."`): bytes plus a final NUL; `\0`, `\x00` and `\u{0}` forbidden; Unicode above U+007F becomes UTF-8 and `\xHH` enters as a raw byte (`c"\xE6"` has 1 byte, `c"\u{E6}"` has 2). Edition 2021+ (Ref p.32–34, 277–278).
- Types: `&'static str`, `u8`, `&'static [u8; N]`, `&'static CStr`; none accepts a suffix as an expression (Ref p.274–278). Any literal with any suffix is a valid token and passes through macros (including `$l:literal`); rejection happens when it is used as an expression or pattern (Ref p.26).
- Numbers: `_` is free; hex/oct/bin require a digit after the prefix. The tokenizer rejects ambiguous forms (`0b0102`, `0x80.0`, `0b101e`, `2em`) instead of splitting (Ref p.35–37). `0x01_f32` is a hex integer and so is `0x01_e3`; an integer suffix cannot start with `e/E` (Ref p.35–36).
- `-1i8` is two tokens (negation applied to `1i8`); in `macro_rules` negation is never part of a literal token, whereas in proc macros a negative literal can be a single token (Ref p.36, 74–75, 279–280).
- Float: `2.` is valid but does not accept a suffix (`2.f64` would call a method); an exponent without digits is an error; `5f32` is an integer literal accepted as a float; `inf` and `NaN` are not literals; default `f64` (Ref p.38–39, 280–281). An unsuffixed integer infers its type; if under-constrained it falls back to `i32` (Ref p.278–279).
- Tuple index: decimal without leading zeros and without a suffix; `x.01`, `x.0b10`, `x.0usize`, `x.0_0` fail (Ref p.37–38, 324–326).
- Raw lifetime `'r#ident` frees a keyword (except `_ crate self Self super`) (Ref p.39–40). `'static` and `'_` cannot be declared (Ref p.173, 517).
- Reserved tokens: an arbitrary prefix glued to `#`, `'` or `"` (except `r b br c cr`); `a#foo`, `continue'foo`, `match"..."` break in 2021+ (Ref p.42–44). Reserved guards (`#"x"#`, `##`): error in 2024 (Ref p.44).

### 3.2 Macros

**Invocation and macro_rules**
- Invocation is valid in expression/statement, pattern, type, item (including associated), transcribers and extern blocks. Visibility never precedes an invocation; the `;` form is mandatory for an item/statement without braces (Ref p.46–47).
- The expander tries the rules in order and uses the first that matches; if the transcription of that rule errors, the following ones are not tried (Ref p.50).
- Matching does no lookahead: if the parser cannot decide, token by token, how to match the invocation, the result is a local ambiguity error. Ref example: with `($($i:ident)* $j:ident)`, the call `ambiguity!(error)` fails, even though looking at the next token (a `)`) would resolve it (Ref p.50). The outer delimiters of the matcher match any pair: `(())` matches `{()}` but not `{{}}`. A literal `$` is neither matchable nor transcribable (Ref p.50).
- Forwarding a `$e:expr` to another macro delivers an opaque AST that does not match literal tokens; only `ident`, `lifetime` and `tt` remain matchable. If you need to re-match, use `tt` (Ref p.50–51).
- Fragments: `block expr expr_2021 ident item lifetime literal meta pat pat_param path stmt tt ty vis`. `literal` accepts `-?` literal; `ident` does not match `_`, raw ident or `$crate`; `stmt` excludes the `;`; `vis` can be empty; `path` is TypePath (Ref p.49, 51–52).
- Repetitions `*`, `+`, `?` (the latter without a separator). In transcription, the metavariable must have the same number, kind and nesting of repetitions as in the matcher; each repetition must contain at least one metavariable, and all those in the same repetition have the same count (Ref p.53).

**Scope and export**
- Two scopes: textual (by order of appearance, enters child modules and files declared later) and path-based. An unqualified invocation looks up textual and then path-based; `self::m!` only path-based; the textual one shadows the path-based one (Ref p.53–55). Redefining is allowed; the most recent shadows the earlier one until the end of the scope (Ref p.55).
- `macro_rules` without `#[macro_export]` is `pub(crate)` and only gains path-based scope via re-export (`pub(crate) use m;`); `pub use` of a non-exported macro is an error. With `#[macro_export]` it is `pub` at the crate root; only the first occurrence of the attribute counts (Ref p.56–57, 60–61).
- `#[macro_use]` on a module extends the textual scope beyond it; on `extern crate` it imports the exported ones into the macro_use prelude, they can be used before the declaration and are shadowable. On a conflict between crates rustc currently prefers the last one imported: do not depend on it (Ref p.58–59). It does not apply to `extern crate self`.
- `local_inner_macros` prefixes `$crate::` on single-segment invocations; discouraged (Ref p.62, 65).

**Hygiene**
- `macro_rules` has mixed hygiene: labels and local variables resolve at the definition site; everything else (functions, items) at the invocation site. Variables and labels created in one expansion are not shared between invocations: `m!(define); m!(refer);` does not compile (Ref p.63).

**Follow-set** (summary in Ref p.65–66; Reference p.687–695 are the formal appendix, with the definitions of FIRST, LAST and FOLLOW, the matcher invariants and examples of valid and invalid matchers)
- Reason for the restriction (Ref p.65): the macro parser is deliberately limited to avoid ambiguity in the current and future versions. Besides the ambiguous-expansion rule, a fragment matched by a metavariable can only be followed by a token that has already been decided safe after that kind of fragment.
- Ref example: `$i:expr [ , ]` could be accepted today, because `[,]` is not part of any legal expression and the parse would always be unambiguous. It is rejected because `[` can start an expression suffix (indexing), so it cannot be discarded as a token that comes after an expression; if `[,]` became legal in a future version, the matcher would become ambiguous or would parse wrongly and break working code. `$i:expr,` and `$i:expr;` are legal because `,` and `;` are legitimate expression separators (Ref p.65). In other words: the error applies even when the matcher would be unambiguous today (future compatibility).
- Tokens allowed after each fragment (Ref p.65–66, 694): `expr`/`expr_2021`/`stmt` can only be followed by `=>`, `,`, `;`. In the appendix, `expr_2021` appears in the FOLLOW definition on p.694 (`FOLLOW(expr) = FOLLOW(expr_2021) = FOLLOW(stmt)`). `pat_param`: `=> , = | if in`. `pat`: `=> , = if in` (before 2021 also `|`). `path` and `ty`: `=> , = | ; : > >> [ { as where` or a `block` fragment metavariable. `vis` has its own rule (an identifier that is not a raw `priv`, a token that starts a type, or an `ident`/`ty`/`path` metavariable). The other fragments (`block ident tt item lifetime literal meta`) and the terminals have no restriction.
- End of the matcher (Ref p.689): the appendix's 1st invariant only applies to two successive sequences of token trees where the following one (`uu ...`) is non-empty. Hence a fragment at the end of the matcher has no follow restriction under this criterion (the prose explanation of the same invariant speaks of the token that comes after the matcher, "if any", on the same p.689). This is a reading of the formal statement; the text gives no example of a matcher ending in a restricted fragment.
- Repetitions (Ref p.66): the rules hold for every possible number of expansions, taking separators into account. (1) The separator, if any, must be able to follow the repetition's content. (2) If the repetition can occur several times (`*` or `+`), the content must be able to follow itself. (3) The content must be able to follow what comes before the repetition, and what comes after must be able to follow the content. (4) If it can match zero times (`*` or `?`), what comes after must be able to follow what comes before. Appendix examples: `($ty:ty < foo ,)` is illegal and `($ty:ty , foo <)` is legal; `($($ty:ty)-+)` is illegal because `-` cannot follow `ty` (Ref p.695).
- Appendix caveat: the third invariant (repetition without a separator, `*`/`+`, content must be able to follow itself) is described as not enforced today due to a historical oversight, and macros that violate it may become invalid in a future edition (Ref p.690). Yet the list of examples marks `($($e:expr)*)` as illegal (Ref p.695). There is also tension with the normative rule on p.66, which says that if the repetition can occur several times (`*` or `+`), the content must be able to follow itself, without restricting it to repetitions with a separator; the caveat on p.690 says the 3rd invariant, which deals with repetition without a separator, is not enforced today. The Reference does not clarify which statement describes the current rustc: **[NOT VERIFIED IN THE PDF]**. In new code, treat it as an error and use a separator.
- Practical way out of the two errors (local ambiguity from Ref p.50 and follow-set violation): reorder the matcher, that is, put the single ident or element before the repetition (`$j:ident $($i:ident)*` instead of a repetition followed by `$j:ident`), or put an allowed separator or terminal (`,`, `;`, `=>`) right after `expr`/`stmt`. **[inference]**: follows from the rules above (no lookahead, Ref p.50; allowed tokens and repetition rules, Ref p.65–66), but the Reference does not prescribe this recipe.

**Proc macros**
- They live at the root of a `proc-macro` crate (`[lib] proc-macro = true`), are only usable by another crate, compile for the host and run with the compiler's privileges (same concerns as build scripts). They can return syntax, panic (compile error) or hang the compiler (Ref p.67, 570).
- They are not hygienic: use absolute paths (`::std::option::Option`) and names unlikely to collide (Ref p.68).

### 3.3 Items, traits, coherence, dyn compatibility

**Crates, modules, use**
- `main`: no arguments, no bounds or `where`; the return implements `Termination` (`()`, `!`, `Infallible`, `ExitCode`, `Result<T,E>` with `E: Debug`). It can be an import (`use foo::bar as main`). Foreign unwinding escaping `main` ends with a safe abort, with no guarantee of `Drop` (Ref p.77–78).
- `crate_name`: non-empty, Unicode alphanumeric or `_` only; Cargo replaces `-` with `_` (Ref p.78–79, 99).
- `extern crate`: at the root it enters the extern prelude; `self as name` requires `as`; `as _` links without a name; `#[no_link]` avoids linking (Ref p.98–100).

**Functions**
- Without a return it is `()`; parameters are irrefutable patterns; without a body only in a trait or extern; default ABI "Rust", `extern fn` without a string is "C" (Ref p.113–116).
- `async fn`: calling does not execute, it only captures the arguments (including unused ones) in a future; 2018+. `async unsafe fn`: calling requires `unsafe`, awaiting does not (Ref p.117–119).

**Type aliases, structs, enums, unions**
- Discriminant: under repr Rust it is seen as `isize`, but the compiler may use less; explicit only if unit-only or with a primitive repr; implicit is previous+1; duplicates and overflow are errors; no generics of the enum (Ref p.128–130). `as` only on enums without tuple/struct variants; with a primitive repr the discriminant is read via pointer cast in `unsafe` (Ref p.130–132). An enum with zero variants is equivalent to never but does not coerce to other types (Ref p.132). Visibility on a variant passes syntax and falls to validation (Ref p.132–133).

**Const and static**
- `const` is inlined at each use: no fixed address; two references to the same const may differ; destructors run at each use; `const _: T = ...` can repeat; free consts are always evaluated at compile time, even in an unused generic function (Ref p.139–141). A reference to a const is `'static` only if the value is promotable; otherwise it creates a temporary (Ref p.139).
- `static` is a single allocation, lives for the whole program and does not drop; `Sync` type (except `static mut`); an immutable static without interior mutability may go to read-only memory; in a generic scope there is only one instance, not one per monomorphization. Access to `static mut` is `unsafe`; use `&raw mut` to avoid creating a reference (Ref p.142–144). Prefer `const`, except for large data, a single address or interior mutability (Ref p.145).

**Traits and dyn compatibility** (formerly "object safety")
- Associated items: functions, types and consts. Associated types have no value in the definition; trait functions cannot be `const`; `Self` is implicit (Ref p.146–147).
- Dyn compatible requires: compatible supertraits; no `Self: Sized`; no associated consts; no GATs; every function dispatchable or marked `where Self: Sized`. Dispatchable: no type parameters (lifetimes ok), `Self` only in the receiver, receiver `&Self`, `&mut Self`, `Box<Self>`, `Rc<Self>`, `Arc<Self>` or `Pin<P>` of these, no opaque return (neither `async fn` nor `-> impl Trait`). `Rc<Box<Self>>` does not dispatch; `AsyncFn*` is not compatible; `trait W: Super<Self>` neither (Ref p.147–150).
- Methods: `self` accepts `Self`, `&Self`, `&mut Self`, `Box`, `Rc`, `Arc`, `Pin<P>` and nestings, also through an alias (Ref p.181).
- Associated consts are only evaluated when referenced; generic ones, after monomorphization (`const PANIC: () = panic!()` only breaks if used) (Ref p.187–188).

**Implementations and coherence**
- Coherence: incoherent if the orphan rule fails or there is overlap (Ref p.157). Orphan: the trait is local, or at least one type of `T0..Tn` is local and no uncovered parameter appears before the first local one. Fundamental types (`&`, `&mut`, `Box`, `Pin`) leave `Box<Local>` local; `Vec<Foo>` is not local; an alias does not change locality; `Fn*` and `Sized` are fundamental, and adding an impl of them is a breaking change (Ref p.157, 703–705). A blanket impl `impl<T> Foo for T` has an uncovered type (Ref p.703).
- Impl parameters: type and const parameters must always constrain the impl (appear in the trait, in the implementing type, or as an associated type in a bound of a type that contains another constraining parameter); lifetimes only if used in an associated type. Errors: `impl<T> Struct {}`, `impl<const N: usize> Struct {}`, `impl<'a> HasAssocType for Struct { type Ty = &'a Struct; }` (Ref p.158–159).

**Generics**
- Lifetimes come first; const generics accept only integers, `char` and `bool`; in a type or array repetition the parameter appears alone (`N` or `{N}`), never `N * 2`; type vs const ambiguity resolves as type and `{ N }` forces const (Ref p.172–176).
- `impl Bar for Foo<true>` plus `Foo<false>` does not satisfy a generic `Foo<B>: Bar`: exhaustiveness of const values does not count (Ref p.177).

**External blocks** (see also 3.13)
- `unsafe extern` mandatory in 2024. Functions without a body, parameters `IDENT` or `_`, qualifiers only `safe`/`unsafe`; implicitly unsafe. Statics without an initializer, unsafe access unless `safe` (Ref p.160–161).

### 3.4 Attributes, lints, cfg

**Syntax**
- `unsafe(...)` is mandatory on `export_name`, `link_section`, `naked`, `no_mangle` (e.g. `#[unsafe(no_mangle)]`) and asserts unchecked obligations (Ref p.191).

**Tests and derive**
- `derive` only on struct/enum/union and generates bounds on the type parameters (`impl<T: PartialEq>`). Built-ins: Clone, Copy, Debug, Default, Eq, Hash, Ord, PartialEq, PartialOrd (Ref p.203–204).

**Lints**
- `#[diagnostic]` are hints without a guarantee; `on_unimplemented` with `message/label/note`; `do_not_recommend` omits an impl from the messages (Ref p.217–220).

**Code generation**
- `recursion_limit` (default 128) affects macro expansion and auto-deref; `type_length_limit` only with a nightly flag (Ref p.244–245).
- `collapse_debuginfo` only on `macro_rules!`; `debugger_visualizer` on a module or the root (Ref p.251–255).

**Conditional compilation**
- Predicates: option, `all()` (empty is true), `any()` (empty is false), `not()`, `true`, `false`; keys can repeat; an option cannot be turned on from inside the code, only via `--cfg` or the environment (Ref p.80–82).
- `#[cfg(false)]`: removes the item; true removes only the attribute. At crate level it removes the following content but keeps earlier crate attributes (a `#![no_std]` before it stays) (Ref p.88). `cfg_attr` expands to zero, one or several attributes, nests, but does not apply to `crate_type`/`crate_name` (Ref p.89).

### 3.5 Expressions

**Statements and evaluation**
- An item inside a block does not capture generics, parameters or locals of the outer function (Ref p.257–258). `let` without `else` requires an irrefutable pattern; with `else` the block must diverge, and the initializer cannot be a lazy-boolean nor end in `}` (Ref p.258–259).
- A block-like expression (`if`, `match`, block, loop) without `;` in statement position is parsed in isolation: `if ... {} [1];` does not index; without `;` the type must be `()` (Ref p.259–260).
- Precedence, strongest to weakest: paths; method/field; call/index; `?`; unary; `as`; `* / %`; `+ -`; `<< >>`; `&`; `^`; `|`; comparisons (do not chain); `&&`; `||`; `..` `..=` (do not chain); `=` and compound (right→left); `return`/`break`/closures (Ref p.262–263).
- The super-macros `format_args!` and `pin!` treat arguments as super operands (temporary extended if the call is extending); when `format_args!` creates internal temporaries it is unspecified (Ref p.267–268). Attributes on expressions: only on expression statements, array/tuple/call elements and the final expression of a block (Ref p.269).

**Blocks**
- A block with no tail and not diverging has the value `()`; with no tail and diverging, `!`; `fn f() -> ! { loop {}; () }` is an error (Ref p.283–284). A block is a value expression: `(&{ s }).borrow_self()` moves `s` (Ref p.285–286).

**Operators**
- Integer overflow panics in debug mode (`-C overflow-checks`). Counted: `+ - *`, `-` on signed minimum, `<<`/`>>` with a count ≥ bits or negative; `/` and `%` of MIN by `-1` always panic; `-128_i8` does not panic (Ref p.291–292). Integer division by zero is a panic; truncates toward zero; the remainder has the sign of the dividend; `>>` is arithmetic on signed (Ref p.299–300). `!` is bitwise on integers (Ref p.298).
- `?` is equivalent to `match Try::branch(e)` with `Continue(v)=>v` and `Break(r)=>return FromResidual::from_residual(r)`; `Try` is unstable. On `Result`, `Err(e)` returns `Err(From::from(e))`; it also holds for `Option`, `ControlFlow`, `Poll<Result>` and `Poll<Option<Result>>` (Ref p.296–297).
- Comparisons do not chain and take operands by implicit `&` (do not move); `&&`/`||` evaluate the right side only if necessary (Ref p.300–302).

**Cast `as`** (table Ref p.303)
- Allowed: numeric↔numeric; enum→integer; bool/char→integer; only `u8`→`char`; pointer↔pointer; Sized pointer↔integer; `&[T;n]`→`*T`; function→pointer/integer; non-capturing closure→fn pointer (Ref p.303, 319).
- Enum→integer: only unit-only and never with `Drop` (Ref p.305–306). Pointer→integer may truncate, use `usize`; integer→pointer depends on a memory model still evolving (Ref p.306–307).

**Assignment**
- Compound assignment: if both types are primitives known before monomorphization, the RHS is evaluated first; otherwise it is sugar for the trait method, LHS first. A generic `T` is not primitive even when instantiated with `u8`; do not depend on the order (Ref p.316–318). `x += x` compiles with `AddAssign + Copy`, but hand-desugared forms do not (Ref p.318).

**Aggregates, calls, fields**
- Calling a field that is a function requires `(s.f)(x)`; `s.f(x)` is a method (Ref p.320, 336).
- Struct expression: tuple struct constructors are value functions; functional update `..base` requires the same type and all fields visible, only the used fields of the base are accessed; it cannot be at the head of `if`/`while`/`for` nor as a scrutinee without parentheses (Ref p.327–329).
- Method lookup (Ref p.333–335): candidates = the receiver type repeatedly dereferenced (plus array unsize at the end); for each `T`, `T`, `&T`, `&mut T` enter in that order; at each candidate, inherent first, then visible traits. With an inherent `&mut self` and a trait `&self`, `f.bar()` picks the trait's. Mutability, lifetime and `unsafe` do not enter the lookup; more than one candidate is an error. On a trait object, an inherent method of the same name makes the dot call an error; only the qualified form calls the trait's.

**Loops and `if`**
- `while let` is equivalent to `loop { match e { pat => body, _ => break } }`; `for` is equivalent to `match IntoIterator::into_iter(e)` with `loop` and `Iterator::next(&mut iter)`, and that outer `match` keeps the temporaries of `e` alive until the end of the loop (Ref p.343–345).
- Labels follow hygiene and shadowing; `'_` is invalid; a labeled block requires a label on every `break` (Ref p.346–348).
- Let chains (`if let A = x && let B = y && cond`): the Reference requires that there be no loose `||` if there is a `let` (use parentheses) (Ref p.357, 363). Let chains in `if` only exist from edition 2024 (Ref p.357, "Edition differences" block, checked directly in the PDF). For `while`, the PDF read does not state the edition: **[NOT VERIFIED IN THE PDF]**.
- `.await` only in async context; since 2018; `_` as an expression only on the left of an assignment (`_ = f();` discards and avoids `unused_must_use`: example in Ref p.217) (Ref p.365–367).

### 3.6 Patterns

- A plain `let` requires an irrefutable pattern (Ref p.370). Function parameters too (Ref p.113).
- **Central pitfall**: a path pattern takes precedence over an identifier pattern. A single-segment identifier that resolves to a constant in scope is a path pattern; if the const is not in scope (missing import, typo), it becomes a binding that matches everything. `ref`/`ref mut` on an identifier that shadows a const is an error (Ref p.372–373).
- `e @ 1..=5` binds the matched value; `ref` only makes the binding a reference and is needed because `&field` is not valid in a subpattern (Ref p.372).
- Binding modes (match ergonomics): matching a reference against a non-reference pattern dereferences and changes the mode (move→`ref` for `&`; `&mut`→`ref mut`, unless already `ref`), repeating (Ref p.373–374). **2024**: explicit `ref`, `ref mut`, `mut` and reference patterns are only allowed with the default "move" mode; `let [mut x] = &[()];`, `let [ref x] = &[()];`, `let [&x] = &[&()];` are rejected (Ref p.374).
- Range patterns must be non-empty: `10..=0`, `10..0`, `10..10`, `..MIN` are errors, `10..=10` is valid; bounds are literals (including negative) or paths to a char/integer/float const, same type, float without NaN. `0u8..=255u8` is irrefutable; for `char`, the set excludes surrogates. `a...b` was removed in 2021 (Ref p.379–382). `&0..=5` is ambiguous: write `&(0..=5)` (Ref p.387).
- Constant patterns require `T: PartialEq` and recursive structural equality: integers, `str`, `bool`, `char`, tuples/arrays/slices/references of structural components, struct/enum only with `#[derive(PartialEq)]` (a manual impl does not work), raw pointer only if an integer constant, non-NaN float. The value must be known before monomorphization and cannot reference `static mut`, statics with interior mutability nor `extern` statics (Ref p.389–390). A `&CStr` literal as a pattern gives a type error (Ref p.371).
- Or-patterns are valid anywhere in a Pattern, except at the top of `let` and of parameters (use parentheses: `let (Ok(x) | Err(x)) = ...`). All alternatives have the same set of bindings, types and binding modes, without coercions; `x @ A(..) | B(..)` is an error because of precedence (Ref p.360, 390–391, 493).
- `match`: a place expression scrutinee generates no temporary and a by-value binding can move from the place; the scrutinee is not a temporary scope, details in the contrast block of 3.10 (Ref p.359, 490). The type is the LUB of the arms; without arms, `!` (Ref p.360). If the guard fails, the next pattern (including other `|` alternatives of the same arm) is tested, so a guard with a side effect may run several times; before the guard a shared reference to the matched part is taken and the value is only moved if the guard passes (Ref p.361–362). Guard with `if let` and `&&` (guard chains): **[NOT VERIFIED IN THE PDF]** from which edition it exists (Ref p.362–363).

### 3.7 Closures

- With `->` the body must be a block; each closure has a unique anonymous type; `move` serves to obtain `'static`; `Send`/`Sync` if all captured values are. `async |..|` returns a `Future`, 2018+ (Ref p.338–340).
- Modes in increasing order: ImmBorrow < UniqueImmBorrow < MutBorrow < ByValue. Each place is captured by the first mode compatible with the use in the body, independent of the surrounding code; a moved `Copy` is captured by ImmBorrow (Ref p.415–416).
- Precise capture by path (variable plus projections); ancestor and descendant both captured: the greater mode applies (Ref p.416–417). Truncations: deref of a shared `&` truncates at the rightmost deref; `move` captures the prefix up to before the first reference deref; deref of a raw pointer, prefix before the deref; a union field captures the whole union; `repr(packed)` captures up to before the first field access; arrays and slices never capture partially; `Box` captures only the field if by reference (and the whole Box if there is a move of the content), `Rc` captures the whole `Rc` (Ref p.417–426).
- UniqueImmBorrow arises when modifying the referent of a captured `&mut` with a non-`mut` variable; creating `&x` while the closure lives violates uniqueness (Ref p.427).
- Traits: `FnOnce` always; `FnMut` if it does not move out of the captured value; `Fn` if it neither mutates nor moves; depends on the body, not on the capture, and `move` closures can be `Fn` (Ref p.427–428). "Lending" async closures implement only `FnOnce`: `async move || x + 2` with `x: &i32` is not `Fn`, `*x + 2` is (Ref p.428–429).
- **2018 and earlier**: captures the whole variable, which changes the closure's type, conflicting borrows and drop; the way out was to borrow the field into a local beforehand (`let vec = &mut self.vec;`). `move` captures everything by move/copy even when a borrow would suffice (Ref p.431–432).

### 3.8 Types, layout and repr

- `bool`: size/alignment 1; `0x00`/`0x01`; any other pattern is UB; `transmute::<bool,u8>` is sound, the inverse is not. `char`: scalar value (0..=0xD7FF and 0xE000..=0x10FFFF), anything else is immediate UB; same layout as `u32`. `str` has the layout of `[u8]`; non-UTF-8 bytes in `str` methods can cause UB now or in the future (Ref p.397–403).
- `usize`/`isize` have the pointer's width (≥16 bits); the object limit is `isize::MAX`; pointer→`usize` is not necessarily reversible (provenance) (Ref p.400–401). `!` only appears as a function return and coerces to any type (Ref p.404). Recursion in types requires indirection; `type Rec = &'static [Rec]` is not valid (Ref p.395).
- Struct: layout undefined by default (reordering allowed). Union: no active field, reading is `unsafe` (Ref p.409–411).
- Raw pointers compare by address (plus metadata for DST); transmuting a pointer to a non-pointer has undecided semantics (Ref p.434–435).
- `impl Trait` in an argument is equivalent to an anonymous generic without turbofish (swapping one for the other is a breaking change); in a return, all paths must give the same concrete type. Lifetime capture: **2024** captures all parameters in scope; before, in free functions and inherent impls, lifetimes not mentioned in the bounds were not captured. `use<..>`: one per list, includes all types/consts in scope and the named lifetimes, lifetimes before types. `impl Trait` is not valid in `let`, a field, a type alias nor `extern` (Ref p.442–445).
- DST: parameters are `Sized` by default (`?Sized` relaxes it); in traits `Self: ?Sized` is the default; DST only as the last field (Ref p.448).
- FFI: a fieldless `repr(C)` enum has the size of the C enum of the ABI; a Rust enum can only hold declared discriminants, any other value is UB, so modeling a C enum or bitflags this way is usually wrong. An enum with fields `repr(C)` is a tag struct plus a union of payloads (Ref p.456–457).
- `UnsafeCell<T>` is the only way to relax the requirement that the value pointed to by `&` not change; several aliased `&mut UnsafeCell<T>` are UB (Ref p.464).

### 3.9 Lifetimes, variance, elision, HRTB, coercions

- Variance (table Ref p.466): `&'a T` covariant in both; `&'a mut T` covariant in `'a` and **invariant in `T`**; `*const T` covariant; `*mut T` invariant; `[T]`, `[T;n]`, `fn() -> T` covariant; `fn(T)` **contravariant**; `UnsafeCell<T>` invariant; `PhantomData<T>` covariant; `dyn Trait<T> + 'a` covariant in `'a`, invariant in `T`. Struct/enum/union derive from the fields and mixed positions give invariance (Ref p.466–467).
- HRTB: `for<'a> F: Fn(&'a i32)` is needed when the passed reference is local and lives shorter than any lifetime of the function (Ref p.471).
- Elision: each elided lifetime in the input is distinct; if exactly one lifetime appears in the parameters, it goes to all elided output ones; with `&self`/`&mut self`, that of `self` goes to the output; the rest is an error (`fn get_str() -> &str`, `frob(s:&str,t:&str)->&str`) (Ref p.498–499). For elision and `'static` in the RBE, see RBE p.186–194.
- Default object lifetime: container first (`&'a dyn T` ⇒ `+ 'a`; `Box<dyn T>` ⇒ `+ 'static`), otherwise the trait's bounds, otherwise inferred in expressions and `'static` outside. The innermost defines: `&'a Box<dyn Foo>` is still `Box<dyn Foo + 'static>`; two bounds on the container require an annotation. `const`/`static` with a reference have an implicit `'static` (Ref p.500–502).
- Coercion only at coercion sites: `let` with a type, `static`/`const`, call arguments, fields of struct/union/variant, function result, assigned value; propagates through arrays, tuples, parentheses and blocks (Ref p.474–476). Allowed: subtype, `&mut T`→`&T`, `*mut T`→`*const T`, `&T`→`*const T`, `&mut T`→`*mut T`, deref coercion, unsized, fn item→fn pointer, non-capturing closure→fn pointer, `!`→`T`; transitivity is not yet fully supported (Ref p.476–477). Unsize: `[T;n]`→`[T]`; `T`→`dyn U` if `T: U + Sized` and dyn compatible; `dyn T`→`dyn U` if `U` is a supertrait (Ref p.478).

### 3.10 Drop order and temporaries

- Assignment drops the previous value if initialized; assigning to an uninitialized variable does not drop; a partially moved variable drops only the remainder (Ref p.484–485).
- Order: the type's `Drop::drop` and then fields (struct in declaration order; enum, fields of the active variant; tuple in order; array/slice from first to last); move captures in a closure in unspecified order; a trait object runs the destructor of the underlying type (Ref p.484).
- Variables: reverse order of declaration; temporaries: reverse of creation; leaving several scopes from the inside out (Ref p.485–486). In a pattern: reverse; in an or-pattern the order of the first subpattern applies (Ref p.488–489). Parameters stay in the body's scope and are dropped last, each after the bindings of its pattern (Ref p.486–487). `let` variables belong to the block; those of `match`, to the arm's scope (Ref p.487).
- The temporary scope is the smallest among: function; statement; body of if/while/loop; else block; condition without a pattern of if/while or guard; guard with a pattern plus the arm's body; each operand of `&&`/`||`; in **2024**, also conditions with a pattern and the consequent of if, the body and condition of `while let`, and the whole tail of the block (Ref p.489–490).
- **2024**: temporaries of the `if let` scrutinee are dropped before the `else` (Ref p.490, example on p.491); temporaries of the block tail are dropped right after the tail, before the locals (Ref p.490). It affects `Mutex`/`RefCell` guards **[inference]** (the source only states the general effect) (Ref p.490).
- **Contrast `if let` x `match` x `else` (single reference block):** the `match` scrutinee is not its own temporary scope, so its temporaries may be dropped after the `match` expression; the Reference illustrates with the temporary of `match 1 { ref mut z => z };`, which lives until the end of the enclosing statement (Ref p.490). The `else` block of an `if`, on the other hand, is its own temporary scope (Ref p.489). Practical result: in 2024, the `if let` scrutinee dies before the `else`, whereas that of `match` stays alive until the end of the statement (Ref p.489–490). The mentions of the `match` scrutinee in section 3.6 and in the editions table (section 4) point to this bullet.
- Already evaluated operands are dropped in reverse order if another operand does `break`/`return`/panic (Ref p.492).
- Promotion to `'static`: expression evaluable at compile time, without interior mutability or destructors, decided by value (`&None` is `'static`) (Ref p.492).
- Lifetime extension (rules subject to change): `let x = &temp();` extends to the block; in `const`/`static`, to the program. Extending pattern: `ref`/`ref mut`, or struct/tuple/slice/or with an extending subpattern. Extending expression: initializer, operand of an extending borrow/array/cast/struct/tuple, arguments of a tuple struct/variant constructor, block tail (except async), `unsafe`/`const`, if/else branches, match arms, "super" operands of macros. They do NOT extend: arguments of an ordinary call (`identity(&temp())`), method receiver, match scrutinee, tail of `async {}`/closure, operand of `break` (Ref p.492–496).
- Destructors are not guaranteed: `mem::forget` and `ManuallyDrop` are safe; `exit`, `abort` and `panic=abort` do not run destructors; soundness must not depend on them. Panic crossing a non-unwinding ABI: either none or all up to the boundary run (Ref p.496–497).

### 3.11 Names, paths, visibility

**Namespaces and scopes**
- Namespaces: types, values, macros (bang and attribute are sub-namespaces), lifetimes and labels. `struct Foo(u32)` occupies type and value; a `use` duplicating a name in the module is an error even in different sub-namespaces (E0252) (Ref p.511–513).
- Names of outer modules do not enter a nested module; items inside `fn` do not see generics of the outer fn; pattern bindings shadow almost everything, except consts, statics and constructors (error) (Ref p.514–517).
- Preludes are not module members; order: extern > tool > macro_use > std > language. 2015 requires `extern crate`; 2018+ does not, but `alloc` and `test` still do. `#![no_std]` does not prevent `std` from being linked through a dependency; `#![no_implicit_prelude]` removes the std/extern/macro_use/tool preludes (Ref p.519–527).

**Paths**
- Turbofish is mandatory in an expression, optional in a type; `S::f()` prefers the inherent method, `<S as T>::f()` disambiguates. Leading `::`: crate root in 2015, extern prelude in 2018+ (Ref p.531–533).
- `Self` only as the first segment, without generics; `super` only leading and repeatable; `$crate` only in transcribers (Ref p.534–537).

**Name resolution** (Ref p.540–552)
- `use` resolves entirely at expansion and does not traverse types: `use m::E::V` (variant) works, `use m::A::V` (alias) and `use m::E::C` (associated const) are errors; as expressions they work (Ref p.542).
- Globs accept conflicting names and only error on use; non-glob imports and local items shadow them. In an expansion, a candidate defined within it that would shadow an external one is ambiguous, and the order of definitions matters (Ref p.543–551). rustc currently accepts a user glob with `core::panic!`/`std::panic!` against the prelude; do not depend on it (Ref p.545–546).

**Visibility**
- Everything is private by default, except associated items of a public trait and variants of a public enum. A private item is accessible in the current module and descendants; a public item is accessible from outside if all ancestors are. A child module `test` sees the parent's private items (Ref p.554–557).
- `pub(in path)`: a path that resolves to an ancestor module (each identifier must be a module, not a `use` name); `pub(super)` is `pub(in super)`; `pub(self)` is private. 2018+: starts with `crate`, `self` or `super`; 2015 also accepts `::` (Ref p.558). `pub(...)` only restricts; `pub use` short-circuits the privacy chain (`implementation::api::f` is a violation, `api::f` is not) (Ref p.560).

### 3.12 Const eval

- In a const context evaluation is always at compile time; outside it, it may or may not be. OOB and overflow are errors when evaluated at compile time, otherwise a warning and a probable runtime panic (Ref p.632).
- Allowed: literals, const params, paths to fn/const (recursive const is forbidden), tuples/arrays/structs, blocks, irrefutable `let`, assignment, indexing with `usize`, non-capturing closures, native operators, casts (except pointer→address and fn-pointer→address), `const fn`, `loop`/`while`/`if`/`match`. No `Drop::drop` (Ref p.632–636).
- Pitfall (issue #143129): `const C: () = { let _: &'static mut [u8] = &mut []; };` compiles (empty array promoted, no lifetime extension), but `const C: &[u8] = &mut [];` fails (tail, with extension) (Ref p.635).

### 3.13 Unsafe, UB, FFI, unwinding, inline asm

**Unsafe**
- These require `unsafe`: dereferencing a raw pointer; reading/writing `static mut` or an extern static; reading a union field (assigning is safe); calling `unsafe fn`; calling a safe function with `target_feature` without the same features in the context; implementing an `unsafe trait`; declaring an `extern` block; applying an unsafe attribute (Ref p.620).
- `unsafe` creates an obligation (`unsafe fn`, `unsafe trait`) or discharges it (`unsafe {}`, `unsafe impl`, `unsafe extern`, `#[unsafe(attr)]`). `unsafe extern` asserts correct signatures (Ref p.621–623).
- **Body of `unsafe fn` (two sources that differ in emphasis):** the Reference says the body of an `unsafe fn` is considered an `unsafe` block by default and that this can be changed by enabling the `unsafe_op_in_unsafe_fn` lint; an `unsafe fn` can only be called inside an `unsafe` block or inside another `unsafe fn` without that lint (Ref p.621–622). The Book, in turn, states that to perform unsafe operations in the body of an `unsafe fn`, an `unsafe` block is still needed, as in an ordinary function, and that the compiler warns if you forget (Book p.596); the counter listing (`unsafe fn add_to_count`) writes the explicit `unsafe { COUNTER += inc; }` inside the function (Book p.602). The edition from which the lint warns by default **does not appear** in the PDFs read: **[NOT VERIFIED IN THE PDF]**. Practical recommendation: always write a small, explicit `unsafe {}` inside `unsafe fn`; it works under both regimes and keeps each dangerous operation visible.

**FFI: exported symbols and default ABI**
- `no_mangle` can be used on any item and turns off the default name encoding: the symbol becomes the identifier itself. In addition, the item is publicly exported from the produced library or object file, similarly to `used` (Ref p.639). The attribute is unsafe because an unmangled symbol can collide with another one of the same name (or with a well-known symbol), leading to UB (Ref p.639).
- `link_section` (object section in which the function or static is placed) and `export_name` (name of the exported symbol on a function or static) follow the same requirement: in 2024 they must be written as `#[unsafe(link_section = "...")]` and `#[unsafe(export_name = "...")]`; before 2024 it was allowed without `unsafe` (Ref p.639–641). Reasons for unsafe: `link_section` allows putting data or code in sections that do not expect them, such as mutable data in a read-only area (Ref p.640); `export_name` can collide with another symbol (Ref p.641). Only the first occurrence of `link_section`/`export_name` on an item counts (Ref p.640–641). Other unsafe attributes: `naked` (Ref p.191).
- Default ABI: a function without `extern` has the `"Rust"` ABI (Ref p.115). `extern fn` with the ABI string omitted uses `"C"`, and `extern fn new_i32()` is equivalent to `extern "C" fn new_i32()` (Ref p.115–116). In an `extern` block, an omitted string also means `"C"`, but the Reference warns that the syntax without an explicit ABI is being phased out and recommends always writing the ABI (Ref p.162). Recommendation: always spell out `"C"` (or `"system"`, `"C-unwind"`) on `extern` functions and blocks. The Book calls `"C"` the most common ABI, which follows the C language ABI (Book p.600).
- Typical combination to expose Rust to C in 2024: `#[unsafe(no_mangle)] pub extern "C" fn name()`. In this use `unsafe` is required only on the attribute, not on an `extern` block (Book p.601).

**Panic and unwinding**
- UB in FFI: a foreign exception entering Rust through a non-unwinding ABI (`"C"`, `"system"`); a Rust `"C-unwind"` function called from non-unwinding code. Catching foreign unwinding with `catch_unwind`/`join`/exit from `main`: unspecified between aborting and an opaque `Err` (Ref p.567).

**Inline asm** (Ref p.576–619)
- UB in asm: a register not declared as an output being altered; SP not restored; unwinding out; `pure` with an effect or non-determinism; DF flag set; x87 stack altered; falling off the end with `noreturn` or `naked_asm!`; callee-saved altered in naked. The compiler treats asm as a black box and may duplicate it. Following the rules is necessary, not sufficient: the compiler does not validate the assembly (Ref p.608–615). Guaranteed directives in Ref p.616–619.

---

## 4. (c) Differences by edition

| Topic | Before (**[inference]**: the Ref describes the new rule; the old behavior is only a source when stated) | From | Ref pages |
|---|---|---|---|
| `async`, `await`, `dyn` | identifiers (`dyn` contextual in 2015) | 2018: strict keywords | 13, 15 |
| `try` | free | 2018: reserved | 14 |
| `gen` | free | 2024: reserved | 14 |
| `async fn`, async blocks, `.await`, async closures | unavailable | 2018 | 118, 287, 339–340, 365 |
| Paths in `use` | 2015: relative to the crate root | 2018: relative to the current scope; `::` points to the extern prelude | 103–105, 110, 533 |
| External crate in `use` | 2015 requires `extern crate` | 2018 dispenses with it (`alloc`, `test` still require it) | 104, 523–524 |
| `use *;` and `use ::{self as root}` | valid in 2015 | error in 2018+ | 108, 110 |
| Injection of `std`/`core` at the root | until 2017 | 2018+ does not inject | 525 |
| `no_implicit_prelude` and macro_use prelude | 2015 not affected | 2018+ removes | 527, 549 |
| Std prelude | `rust_2015`/`rust_2018` = `v1` | 2021 and 2024 have their own | 522 |
| Anonymous parameters in a trait (`fn f(i32);`) | allowed in 2015 | error since 2018 | 152, 182 |
| Parameter patterns in a trait fn with a body | 2015: only `IDENT`, `mut IDENT`, `_`, `&IDENT`, `&&IDENT` | 2018: any irrefutable | 152 |
| `dyn` | optional before 2021; in 2015 `dyn ::path` read as a path | 2021 mandatory | 438–439 |
| C string `c""` and `cr""` | lexed as `c` + `""` | 2021 | 33–34 |
| Raw lifetimes `'r#x` | lexed as `'r # x` | 2021 | 40 |
| Reserved prefixes (`a#foo`) | multi-token | 2021: lexer error | 43 |
| Reserved guards (`#"x"#`, `##`) | multi-token | 2024: error | 44 |
| Fragment `pat` | = `pat_param` | 2021 accepts or-pattern at the top | 52 |
| Follow-set of `pat` | could be followed by `\|` | 2021 forbids | 65–66 |
| Fragment `expr` | does not match `_` nor `const {}` at the top | 2024 matches; `expr_2021` preserves the old one (edition in force at the definition of the `macro_rules!`) | 52 |
| Array receiver and `IntoIterator` in method lookup | ignored before 2021 | 2021 (edition of the method name's token) | 335 |
| Capture in closures | ≤2018: whole variable (the Ref says "edition 2018 and before", p.431) | by disjoint path. The Ref does not name "2021" in the passage read; that association comes from the Edition Guide/external knowledge, **[inference]** | 430–432 |
| `extern` block | `unsafe` optional; `safe`/`unsafe` on items only in an `unsafe` block | 2024: `unsafe extern` mandatory | 160, 171, 620, 623 |
| `no_mangle`, `link_section`, `export_name` | plain attribute | 2024: `#[unsafe(...)]` | 639–641 |
| Binding modes (`ref`, `ref mut`, `mut`, `&pat` with non-move mode) | allowed | 2024 forbids | 374 |
| `impl Trait` in return | only mentioned lifetimes | 2024: captures all lifetimes in scope | 444 |
| Divergence fallback | `()` | 2024: `!` | 482–483 |
| Temporaries | **[inference]** (the Ref does not describe the previous behavior): the `if let` scrutinee lived beyond the `else`; block tail after locals | 2024 added two rules: the `if let` temporaries are dropped before the `else` block, and those of the block tail are dropped right after the tail, before the locals. Example: the scrutinee is dropped after the consequent and before the `else` (Ref p.491). Contrast with `match` and the `else` as its own scope: see 3.10 | 489–491 |
| `panic!` | before 2021 `core::panic!` and `std::panic!` differ | 2021+ identical | 545 |
| `pub(in path)` | 2015 accepts `::` and root modules | 2018+ requires `crate`/`self`/`super` | 558 |
| Range pattern `a...b` | accepted | removed in 2021 | 382 |
| Let chains in `if` | not supported | 2024: supported (checked in the PDF: before 2024 the LetChain grammar is not allowed in `if`) | 357 |

Without an `edition` key in `Cargo.toml`, 2015 applies (Book p.711). In 2015 `try` was not a keyword (Book p.693–694).

---

## 5. (d) Undefined behavior and guarantees

The Reference's list is non-exhaustive and may grow or shrink; there is no formal model of the semantics of what is allowed in unsafe code, so there may be other behaviors treated as UB, and the Reference reserves the right to define some items currently listed in the future (Ref p.624). The Reference itself tells you to read the Rustonomicon before writing unsafe code (Ref p.624); the Rustonomicon is not part of the PDF read, so what it contains was not checked here. `unsafe` does not relax any language rule: code in `unsafe` blocks and functions is still forbidden from causing UB; it just becomes the programmer's task to avoid it (Ref p.624). Unsafe code that does not allow UB to any safe client is sound; if safe code can abuse it to cause UB, it is unsound (Ref p.624). UB affects the whole program: UB in C called via FFI contaminates the Rust code and vice versa (Ref p.626).

### Explicit UB

- **Aliasing** (model not yet defined): `&T` does not see mutation while alive, except in `UnsafeCell`; `&mut T` is only accessed through derived pointers; mutating immutable bytes (promoted, immutable `static`, everything pointed to by `&T`), even when writing the same value (Ref p.624–625). Several aliased `&mut UnsafeCell<T>` (Ref p.464).
- Data race; dangling or misaligned place; place projection outside in-bounds limits; misused intrinsic; wrong ABI; unwinding through a frame that does not allow it; incorrect asm; violating runtime assumptions (e.g. `longjmp` skipping destructors) (Ref p.624–626).
- **Dangling pointer** (Ref p.627): a reference or pointer is dangling if not all bytes it points to are part of the same live allocation (and, of course, of some allocation). If the pointed-to size is 0, the pointer is never dangling, not even if null. The pointed-to bytes are determined by the pointer's value and the size of the pointed-to type (`size_of_val`) (Ref p.626). A DST points to the whole range, so the size metadata can never be too large; the dynamic size of a value cannot exceed `isize::MAX` (Ref p.627).
- **Alignment** (Ref p.626–627): a place is based on a misaligned pointer when the last `*` in the place computation was applied to a pointer not aligned for its type. The alignment requirement comes from the type of the dereferenced pointer, not the accessed field: with `ptr: *const S` and `S` of alignment 8, `(*ptr).f` requires `ptr` aligned to 8 even if `f` is `u8`. Only reading or writing (load/store) that place is UB; `&raw const`/`&raw mut` on it is allowed. `&`/`&mut` require the alignment of the field's type (otherwise it would produce an invalid value); with `repr(packed)`, creating the reference is a compile error (Ref p.293–294, 462, 626–627).
- **`read_unaligned`/`write_unaligned` and misaligned pointer:** to access a possibly misaligned field, the way is to create the raw pointer with `&raw const`/`&raw mut` (allowed, Ref p.627) and read/write with the unaligned methods instead of dereferencing the pointer directly; the `repr(packed)` text gives this example with `read_unaligned` and `write_unaligned` (Ref p.463). The borrow operator example creates `&raw const packed.f2` on a `u16` field of a packed struct and reads with `read_unaligned`, noting that `&packed.f2` would create a misaligned reference, therefore UB (Ref p.294). Pages 626–627 define the place based on a misaligned pointer and allow `&raw`, but do not mention `read_unaligned`.
- **Invalid values** (Ref p.627–628): the compiler assumes every produced value is valid, and producing an invalid one is immediate UB. To produce is to assign to, read from, pass to or return from a place or operation (Ref p.625). `bool` ≠ 0/1; null `fn` pointer; `char` surrogate or > `char::MAX`; any `!` value; uninitialized integer, float or raw pointer; uninitialized `str`; enum with an invalid discriminant; struct/tuple/array with an invalid field; null, misaligned, dangling reference or `Box`, or one to an invalid value (this last point under debate); invalid metadata (vtable, slice > `isize::MAX`); outside the range of `NonNull`/`NonZero`. For `union` the exact validity has not yet been decided (Ref p.397, 402, 457, 627–628).
- **Uninitialized memory** (Ref p.629): it is implicitly invalid for any type with a restricted set of valid values; the only cases where reading uninitialized memory is allowed are inside a `union` and in padding (gaps between fields).
- In const: pure integer data cannot have provenance, so reinterpreting a pointer as an integer is UB (Ref p.628–629).
- Union: reading a field with bits invalid for the type (e.g. `3` as `bool`) (Ref p.135).
- Non-UTF-8 bytes in `str` methods (Ref p.403).
- FFI and unwinding: native unwind crossing a non-unwinding ABI; foreign exception in Rust via a non-unwinding ABI; `C-unwind` called from non-unwinding code; potentially unwinding artifact with a crate outside the `unwind` strategy (Ref p.116–117, 567, 574).
- Asm: see 3.13 (undeclared register altered, SP not restored, impure `pure`, DF set, x87 altered, falling off the end in `noreturn`/`naked_asm!`, `nomem` with external access) (Ref p.606–613).

### Not considered unsafe (Ref p.630–631)

Deadlocks, leaks, exiting without destructors, leaking the randomized base address, overflow and logic errors. Overflow with `debug_assert!` enabled must panic; otherwise panic or wrap (two's complement), at the implementation's choice (`wrapping_*`, `Wrapping<T>` for explicit intent). Violating `Hash` consistency with `Eq` or mutating a key of `HashMap`/`BTreeMap`/`BinaryHeap` is not UB, but is unspecified (panic, wrong result, abort, non-termination).

### Unspecified or without guarantee

- Layout of repr(Rust), of closures and of async blocks; size of pointers to DST; alignment of primitives per platform; discriminant under repr Rust (Ref p.125, 128, 286, 449–452).
- Whether `const {}` outside the execution path is evaluated (Ref p.289); address of `const` (Ref p.139).
- `inline`, `cold`, `track_caller`, `#[diagnostic]` are hints (Ref p.217, 223, 241).
- Whether destructors run on an abort at a non-unwinding ABI boundary (Ref p.78, 117, 497).
- Catching foreign unwinding: abort or opaque `Err` (Ref p.567). Which macro wins in a `#[macro_use]` conflict between crates (Ref p.59). Visit order of macro scopes (Ref p.549). Semantics of transmuting a pointer to a non-pointer (Ref p.434–435). High bits in asm operands smaller than the register (Ref p.593–594).
- Lifetime extension rules subject to change; coercion transitivity and LUB informal (Ref p.476, 480, 492).
- Incomplete memory and aliasing model (Ref p.561, 624). Which concrete type `lib` produces and which format (rlib/dylib) each dependency receives (Ref p.569, 572).

### Explicit guarantees

- Static: all references point to the same allocation; no drop at program end; single in a generic context (Ref p.142–143). Free consts evaluated at compile time (Ref p.141). `const {}` executed at runtime is evaluated at compile time; const fn in the target's environment (Ref p.289, 637).
- `MIN / -1` and integer division by zero always panic; out-of-bounds index is a panic; saturating float→int with `NaN→0` (Ref p.292, 300, 304, 323).
- `size_of` a multiple of the alignment; array layout; `char` ≅ `u32`; `&str` ≅ `&[u8]`; pointers and refs with the same layout (Ref p.449–451).
- `repr(C)` with a defined algorithm; `repr(transparent)` inherits layout and ABI; discriminants with a primitive repr can be read via pointer cast; `repr(C)` union reads like `transmute` (Ref p.131–132, 135, 454–463).
- Writing to a union field is safe and does not drop (Ref p.135–136). `target_has_atomic` implies the full atomic API at that width (Ref p.85).
- A `Box` allocation is not reallocated on move (Ref p.562). Unwinding drops the live values in the traversed frames (Ref p.566). ZST is never dangling (Ref p.627).
- Asm: operands evaluated and outputs written left to right; `clobber_abi` follows new registers (Ref p.585, 603).
- Destructors are NOT guaranteed; soundness cannot depend on them (Ref p.497).

---

## 6. (e) Source limitations and dated content

### 6.1 Claims to verify

- **[VERIFIED IN THE PDF]** Let chains in `if` requiring edition 2024: Reference p.357 says that before 2024 the LetChain grammar is not allowed in `if`. Two intermediate notes diverged (one said only 2024, the other said not annotated); checking the source text resolved it in favor of the first. For `while`, the edition was not confirmed.
- **[NOT VERIFIED IN THE PDF]** Guard-let in `match` (`if let` with `&&` in a guard): the Reference does not say from which edition it exists; check the compiler version (Ref p.362–363).
- **[NOT VERIFIED IN THE PDF]** In Book p.65 a compiler message says that `let` is only accepted directly in `if` and `while` conditions; the block does not explain the feature.
- The list of type starts in the follow-set of `vis` and macro invariant 3 may be out of date (Ref p.690, 694). Several rules are marked by the Reference itself as subject to change: macro scope order (Ref p.549), GAT rule (Ref p.186), lifetime extension (Ref p.492), glob ambiguity restriction (Ref p.548).
- **[inference]** The effect of the 2024 temporaries on `Mutex`/`RefCell` guards is a connection made by this consolidation; the source only describes the drop rule (Ref p.490).

### 6.2 Reference coverage

- Details not distilled: the full grammar (Ref p.645–676), syntax index (Ref p.677–686, except reserved keywords and operators), test summary (Ref p.697–701), influences (Ref p.696), `target_feature` feature tables (Ref p.228–238), register class tables (Ref p.587–596), list of assembler directives (Ref p.616–619) and most of the glossary (Ref p.702–710). Consult the pages directly.
- Primary and type-relative name resolution appears only as a placeholder (Ref p.552–553). Associated items: the initial block ends at "Methods" (Ref p.180), and the rest comes from the next block (Ref p.181 onward).
- Sections without content in the notes: Whitespace (Ref p.22) and attributes on functions and parameters (pages not indicated in the notes; see Ref p.112–121). The unwinding-by-ABI table and the variance, `bool` truth and size tables came linearized and were reconstructed by reading order and checked against the surrounding text.
- Rule ids (`lex.token...`, `items.traits...`) almost did not survive extraction; only four were seen: `input.encoding.utf8` (Ref p.4, as an example of an id), `lex.token.literal.char-escape.unicode` (Ref p.45), `cfg.attr.crate-level-attrs` (Ref p.88) and `items.traits.params.patterns-with-body` (Ref p.152). Use pages as the reference.
- Rust by Example: only the page map was distilled; there are no RBE rules in this file (the exception, handling of multiple error types in RBE p.257–269, is in procedimentos.md, section 12). The map covers RBE p.3–364. RBE listings came with mixed line numbers, truncated or disordered code (RBE p.30–31, 90–91, 95–96, 118).
- No code was compiled or tested; the cited examples come from the notes.

### 6.3 Dated or version-dependent content (Book)

- The Book assumes Rust 1.90.0 (2025-09-18) or later and `edition = "2024"` (Book p.1). Compiler and Cargo outputs (`Finished dev profile`, `help:` messages) change between versions (Book p.30, 125, 131, 169, 214).
- `rand 0.8.5` pinned: `thread_rng` and `gen_range` belong to that series and other versions may break the examples (Book p.30, 181, 402). `ripgrep v14.1.1` and `resolver = "3"` are illustrative (Book p.399, 406). Logging in to crates.io requires a GitHub account at the time of writing (Book p.394).
- Async: `trpl` is a support crate of the book that re-exports types from the `futures` and `tokio` crates and may rename or wrap APIs; the book says Tokio is the most widely used async runtime, especially in web applications, that there are other runtimes perhaps better suited to each case, and that `trpl` uses Tokio underneath because it is well tested and widely used (Book p.491). The book does not compare runtimes nor performance. `Stream` and `StreamExt` were not yet in std at the time of writing (Book p.491, 518, 530–531). Benchmarks only on nightly at the time (Book p.278). Procedural macros require, at the time of writing, a separate crate (Book p.636, 638).
- `unsafe extern`, `safe fn`, `#[unsafe(no_mangle)]`, `&raw const/mut` and the `static_mut_refs` lint (deny by default) appear in the Book, which assumes edition 2024 (Book p.1, 594, 599–602); the Book does not say from which edition the lint is deny (**[extrapolation]**: in an earlier edition it may be only a warning). Miri requires nightly and its output varies with the version (Book p.604–605). The `mod.rs` style is the older style, still supported (Book p.185–186).

### 6.4 Truncated or missing passages (Book)

- **Boundaries of the distillation blocks (not gaps in the book).** The Book was distilled in 8 blocks of ~90 pages, cut by size, not by chapter. When a section crosses the boundary, the annotation may say "ends in the middle of X", but the subject continues in the next block and is covered: lifetime elision (start at p.269, rules at p.270–273), closures/`FnMut` and iterators (p.358–379), trait objects, dyn compatibility and the State pattern (p.543–561), Function Pointers and returned closures (p.629–632), list of `Copy` types and ownership with functions/slices (p.94–133). If a query falls on one of these seams, read the pages on both sides of the boundary before concluding the book does not cover the point.
- Details of `Vec<T>` are in the Rustonomicon (Book p.191); `unsafe` is not exhausted in the Book (Book p.606). Std does not offer grapheme clusters (Book p.202).
- Book page 719 appears empty or with only a marker; the summary (Book p.690) and Appendix F (translations) have no operational content.

### 6.5 PDF extraction problems

- Figures and diagrams became loose, illegible text (Book Figures 4-1 to 4-7, 15-1 to 15-4, 17-1 to 17-9); the meaning was recovered from the adjacent text (Book p.83–89, 99, 110, 414, 416, 430, 449).
- Listings with lines out of order or displaced to the end of the page (Book p.108, 113–114, 151, 270); captions before the code (Book p.529); truncated E0277 error message (Book p.128); Arabic text with lost ordering (Book p.196).
- Linearized tables (variance, `bool` truth, sizes) and code blocks with mixed line numbers, which were discarded (Ref p.466; RBE p.30–31, 90–91, 95–96, 118).
- No reader-directed text was found in the source notes; the content was treated only as data.
