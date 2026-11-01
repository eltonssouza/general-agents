# Typing (RBS, TypeProf), the Prism parser and diagnostic tools

Convention: `(R3x p.N)` = PDF page of the note (see `INDEX.md`).

## 1. RBS
- `[from source]` RBS is a language for describing the types of Ruby programs; checkers such as TypeProf and other tools that support RBS understand the program better with these definitions (R30 p.4).
- `[from source]` It allows describing classes and modules: methods, instance variables and their types, inheritance and mix-ins. The goal is to support common Ruby patterns, with advanced types: unions, method overloading and generics; also duck typing with interface types (R30 p.4).
- `[from source]` Ruby 3.0 includes the `rbs` gem, which parses and processes the definitions (R30 p.4). The note's example shows `attr_reader name: String`, `Array[User | Bot]` and `def post: (String, from: User | Bot) -> Message` (R30 p.4).
- `[from source]` 3.1: generic parameters with bounds, generic aliases, and `rbs collection` to manage RBS for gems (R31 p.5); many signatures for built-in/standard libraries added (R31 p.6).
- `[from source]` RBS ships as a bundled gem: rbs 2.0.0 in 3.1 (R31 p.10), 2.8.2 in 3.2 (R32 p.21), 3.4.0 in 3.3 (R33 p.11).
- `[extrapolation]` Keeping `.rbs` files separate from `.rb` (like `.d.ts` or `.h`), and the use of Steep or IDEs to check types, are not in the notes (the note shows only the RBS syntax). What the 3.0 note says about philosophy is a sentence attributed to Matz: static checking "without type declarations" by abstract interpretation (R30 p.4).

## 2. TypeProf
- `[from source]` Type analysis tool bundled with Ruby; it works as type inference: reads Ruby code without annotations, analyzes which methods are defined and how they are used, and generates a prototype of signatures in RBS (R30 p.4-5).
- `[from source]` Usage shown: save `test.rb` and run `typeprof test.rb` (R30 p.5). At the time it was experimental and immature: only a subset of the language and limited detection of type errors (R30 p.5).
- `[from source]` 3.1: "TypeProf for IDE" (experimental), a VS Code extension that shows the estimated signature above each method, underlines possible name or type errors and suggests method names (R31 p.6-7). Bundled versions: typeprof 0.21.1 (R31 p.11), 0.21.3 (R32 p.21), 0.21.9 (R33 p.11).
- `[extrapolation]` Redirecting the output to `sig/app.rbs` and the exact content generated for any given code depend on the TypeProf version; only the note's example (class `User`) is from the source.

## 3. Prism and Lrama
- `[from source]` 3.3: Prism is introduced as a default gem; it is a portable, error-tolerant, easily maintained "recursive descent" parser, production-ready and actively maintained, which can be used instead of Ripper; it is a C library used internally by CRuby and a Ruby gem for tools (R33 p.1).
- `[from source]` Notable API: `Prism.parse(source)` (AST inside the result), `Prism.parse_comments(source)` and `Prism.parse_success?(source)` (R33 p.1-2).
- `[from source]` `ruby --parser=prism` (or `RUBYOPT="--parser=prism"`) is for trying out the Prism compiler; the note says the flag is only for debugging (R33 p.2). The Prism version bundled in 3.3 is 0.19.0 (R33 p.8).
- `[from source]` 3.3: Bison was replaced by the LALR parser generator Lrama (Feature #19637) (R33 p.2).
- `[from source]` 3.4: the default parser goes from `parse.y` to Prism (Feature #20564); it is an internal improvement with little visible change; to use the conventional parser, `--parser=parse.y` (R34 p.2).
- `[extrapolation]` Lines of code of `parse.y`, adoption by RuboCop/Solargraph and Language Server are not in the notes.

## 4. `debug`, `error_highlight` and `SyntaxSuggest`
- `[from source]` 3.1: the `debug` gem (debug.gem), a rewritten debugger, is now distributed with Ruby. Features: debugging without slowing down the application, remote debugging, rich front-ends (VS Code and the Chrome browser), multi-process/multi-thread, colored REPL, record and replay, tracing (R31 p.2). It replaces the old `lib/debug.rb` (R31 p.3). It moves from default gem to bundled in the same release (R31 p.11).
- `[from source]` 3.1: `error_highlight` shows the refined error location in the backtrace, with `^^^^^` under the snippet and a "Did you mean?" suggestion (example `1.time {}` with `NoMethodError`); at the time only `NameError` was supported (R31 p.3). Enabled by default; disabled with `--disable-error_highlight` (R31 p.4).
- `[from source]` 3.2: `ErrorHighlight` now points to the relevant argument in `TypeError` and `ArgumentError` (R32 p.8).
- `[from source]` 3.2: `syntax_suggest` (formerly `dead_end`) is integrated into Ruby and helps find the position of errors such as a missing or extra `end` (R32 p.8); the included version is 1.0.2 (R32 p.20).
- `[from source]` 3.2: `RubyVM::AbstractSyntaxTree.parse` gains `error_tolerant` and `keep_tokens` (R32 p.13-15).
- `[from source]` IRB: autocompletion and documentation (3.1, R31 p.4); debug integration commands (`debug`, `break`, `next`, `step`...) even without `gem "debug"` in the Gemfile (R32 p.18); `irb:rdbg` integration (R33 p.6).
- `[extrapolation]` "Replaces byebug" and "DAP protocol" are not in the notes.

## 5. WebAssembly/WASI (Ruby 3.2)
- `[from source]` Initial port of WebAssembly support based on WASI: it allows a CRuby binary in the browser, in an edge serverless environment or other WASI hosts; at the time it passed the basic and bootstrap suites that do not use the Thread API (R32 p.1).
- `[from source]` Context: WASI standardizes the interface with the operating system for Wasm; one use case is the TryRuby playground (R32 p.2). Technically, CRuby uses Asyncify to provide Fiber, exceptions and GC; and a VFS over WASI allows packaging Ruby apps into a single `.wasm` file (R32 p.3).
- `[extrapolation]` Specific runtimes (Wasmtime, Cloudflare Workers) are not in the notes.
