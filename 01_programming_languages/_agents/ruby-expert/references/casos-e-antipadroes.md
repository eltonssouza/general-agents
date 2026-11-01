# Use cases and antipatterns (with the source of each)

Convention: `(R3x p.N)` = PDF page of the note. Here each case separates what is **from the source** (the notes) from what is a **package recommendation** (`[inference]`/`[extrapolation]`). No case states "always/never" beyond what the note says.

## 1. Mutating a string literal in Ruby 3.4
- Problem: `mensagem = "Olá, "; mensagem << nome` in a file without a `frozen_string_literal` comment.
- `[from source]` In such files, 3.4 emits a deprecation warning when the literal is mutated; turn the warnings on with `-W:deprecated` or `Warning[:deprecated] = true`; `--disable-frozen-string-literal` undoes the change (R34 p.5).
- `[extrapolation]` Common fixes: interpolation (`"Olá, #{nome}"`), `+"Olá, "` or `String.new`. They are not in the notes.

## 2. Regex with back-reference or look-around on untrusted input
- `[from source]` The memoization algorithm does not apply to regexes with back-references, look-around or huge fixed repetitions; for those cases there is `Regexp.timeout` (global) and `timeout:` in `Regexp.new` (R32 p.7).
- `[inference]` If your code matches regexes of that kind against third-party input, it is worth setting a timeout; the value depends on the case.
- `[extrapolation]` Handling `Regexp::TimeoutError` and responding with HTTP 4xx are application decisions.

## 3. Sharing state between Ractors
- `[from source]` Ractors cannot share normal objects; they communicate by messages (R30 p.2). There are syntax restrictions when there is more than one Ractor (R30 p.2).
- `[extrapolation]` The detailed rules (frozen objects are shareable, `move`, copy) are in `doc/ractor.md` (R30 p.3), not in the notes. For details, consult the documentation of the version.

## 4. Modeling an immutable value
- `[from source]` `Data.define` creates an immutable value class, similar to `Struct` with a leaner and stricter API (R32 p.11-12).
- `[inference]` For value objects, `Data` communicates the intent of immutability. Anyone who needs setters stays with `Struct`.

## 5. Pin `^` in pattern matching
- `[from source]` In 3.1 the pin accepts an expression, such as `^(n + 2)` (R31 p.5).
- `[extrapolation]` The classic problem of "the identifier captures and overwrites the variable" comes from the general semantics of pattern matching, not from the notes.

## 6. Blocking threads with I/O
- `[from source]` `Fiber#scheduler` intercepts blocking operations and gives lightweight concurrency without changing the code; the `async` gem provides an event loop (R30 p.3-4). `IO#select` was not supported (R30 p.3).
- `[extrapolation]` How many threads/descriptors are "too many" depends on the system.

## 7. Missing `end` in large files
- `[from source]` The `syntax_suggest` integrated in 3.2 helps find a missing or extra `end` (R32 p.8).

## 8. Choosing the wrong JIT
- `[from source]` 3.0 warns that the JIT (MJIT) was not yet suited to workloads such as Rails (R30 p.2); YJIT was created for Rails applications (R31 p.1) and stopped being experimental in 3.2 (R32 p.4); the 3.3 note says to keep using YJIT in production and that RJIT is experimental (R33 p.4).
- `[extrapolation]` The `--jit` flag and `RUBY_YJIT_ENABLE=1` do not appear in the notes; use `--yjit` (R31 p.2) or `RubyVM::YJIT.enable` (R33 p.3).

## 9. Short blocks
- `[from source]` In 3.4, `it` is the reference to the unnamed block parameter, behaving like `_1` (R34 p.1). In 3.3, `it` without arguments in a block without parameters is deprecated (R33 p.6).
- `[VERSION-DEPENDENT]` Do not use `it` in code that must run on Ruby < 3.4.

## 10. Types
- `[from source]` RBS describes types; TypeProf generates an RBS prototype from code without annotations (R30 p.4-5).
- `[extrapolation]` Keeping `.rbs` separate and using a checker (Steep) is an ecosystem practice; the note only presents the RBS language and TypeProf.

## 11. Expecting version changes when migrating (extra, only with backing)
- `[from source]` When moving up to 3.2, codebases that use `Fixnum`, `Bignum`, `File.exists?`, `Dir.exists?`, `taint`/`untaint` break (R32 p.16); for 3.4, `Refinement#refined_class` was removed and the error messages changed format (R34 p.8-9); libraries leave the stdlib for bundled gems (R33 p.7-8; R34 p.7).
- `[extrapolation]` The migration procedure (order, tools) belongs to the package, not to the notes.
