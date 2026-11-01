# Procedures (each step with its origin)

Convention: `(R3x p.N)` = PDF page of the note. The procedures below belong to the package; steps that follow from the notes carry the page, the others are labeled.

## 1. Enabling and inspecting YJIT
1. `[from source]` Enable it with the command-line option `--yjit` on `ruby` (R31 p.2). In builds from 3.3 on, it can also be enabled at run time with `RubyVM::YJIT.enable`, even only after the application has finished booting (R33 p.3). To use other YJIT options without turning it on at startup, `--yjit-disable` (R33 p.3).
2. `[from source]` To compile Ruby with YJIT, `rustc` 1.58.0 or higher is required before `./configure` (R32 p.4).
3. `[from source]` Statistics: `RubyVM::YJIT.runtime_stats`; `--yjit-stats` computes and prints them at some cost (R32 p.4). `--yjit-log` and `RubyVM::YJIT.log` (3.4) show the compilation log (R34 p.3).
4. `[from source]` Limits: `--yjit-exec-mem-size` (64 MiB by default in 3.2, R32 p.5) and, in 3.4, `--yjit-mem-size` with a default of 128 MiB (R34 p.3).
5. `[extrapolation]` Checking whether YJIT is active with `RubyVM::YJIT.enabled?`, using `RUBY_YJIT_ENABLE=1` and passing flags to Puma are **not** in the notes; consult the documentation of the Ruby in use.
6. `[HOST]` Supported platforms: x86-64 and arm64 on Linux, macOS, BSD and other Unix (R32 p.4).

## 2. First experience with Ractors
1. `[from source]` Create actors with `Ractor.new { ... }` and collect with `take`, as in the official example (R30 p.3). Expect the "experimental feature" warning on the first `Ractor.new` (R30 p.2).
2. `[from source]` Ractors do not share normal objects; use messages (R30 p.2). Consult `doc/ractor.md` for the rules (R30 p.3).
3. `[extrapolation]` Freezing objects with `.freeze` or `move: true`: a rule from `doc/ractor.md`, outside the notes.
4. `[from source]` Measure: the example shows 16.69 s parallel against 64.56 s sequential on 4 cores (R30 p.3).

## 3. Protecting a regex against ReDoS
1. `[from source]` Understand that 3.2 already improves matching (R32 p.5-6) but does not cover back-references, look-around and huge repetitions (R32 p.7).
2. `[from source]` Set `Regexp.timeout = 1.0` (global) or use `Regexp.new(padrao, timeout: x)`; `Float::INFINITY` for a regex without a limit (R32 p.7).
3. `[from source]` On overrun: `Regexp::TimeoutError` (R32 p.7).
4. `[extrapolation]` `rescue`, logging and HTTP response: application decisions.

## 4. Generating an RBS prototype with TypeProf
1. `[from source]` Save the code in `test.rb` and run `typeprof test.rb` (R30 p.5). The output is an RBS prototype with classes, `attr_reader` and `def initialize : (...) -> ...` (R30 p.5).
2. `[from source]` TypeProf is experimental/immature in 3.0 (R30 p.5); in 3.1 there is experimental IDE support (R31 p.6-7).
3. `[extrapolation]` Saving the output in `sig/` and integrating with Steep: ecosystem practice.

## 5. Preparing code for the 3.4 string warnings
1. `[from source]` Run with `-W:deprecated` (or `Warning[:deprecated] = true`) to see literal mutation warnings in files without a `frozen_string_literal` comment (R34 p.5).
2. `[from source]` `--disable-frozen-string-literal` undoes the behavior (R34 p.5).
3. `[extrapolation]` Fix with interpolation, `+""` or `String.new`, or add the magic comment to the file.

## 6. Migrating between versions (checklist with backing)
1. 2.7 to 3.0: separation of keyword arguments; `$SAFE` removed; libraries that left (webrick, net-telnet, xmlrpc, sdbm) (R30 p.7-8).
2. 3.1: `Psych.load` uses `safe_load` (R31 p.8); gems net-ftp/imap/pop/smtp, matrix, prime and debug become bundled (R31 p.11).
3. 3.2: removals (`Fixnum`, `Bignum`, `File.exists?`, `Dir.exists?`, `taint`...) (R32 p.16); `ruby2_keywords` mandatory for delegation via `*args` (R32 p.10).
4. 3.3: `Regexp::new` with at most 2 arguments; `it` without arguments deprecated (R33 p.6); warnings for `require` of gems that will become bundled (R33 p.7-8).
5. 3.4: error messages and `Hash#inspect` change (R34 p.8); block/keywords in index not allowed (R34 p.5); gems promoted to bundled (R34 p.7).
