# Timeline: Ruby 3.0 to 3.4 according to the official notes

Convention: `(R3x p.N)` = PDF page of the note (see `INDEX.md`). All five notes were published on December 25 of the respective year, by naruse (cover of each note).

| Version | Date | Highlights (each detailed in the thematic files) |
|---|---|---|
| 3.0.0 | Dec 25, 2020 | Ruby 3x3 goal; Ractor (experimental); Fiber Scheduler; RBS and TypeProf; pattern matching leaves experimental (R30 p.1-7) |
| 3.1.0 | Dec 25, 2021 | YJIT (experimental); `debug` gem; `error_highlight`; hash value omission; pin `^` with expression (R31 p.1-5) |
| 3.2.0 | Dec 25, 2022 | WASI/WebAssembly; production-ready YJIT; ReDoS improvements and `Regexp.timeout`; `Data`; `SyntaxSuggest` (R32 p.1-12) |
| 3.3.0 | Dec 25, 2023 | Prism; Lrama; RJIT; faster YJIT with less memory; M:N threads; GC improvements (R33 p.1-5) |
| 3.4.0 | Dec 25, 2024 | `it`; Prism as the default parser; Happy Eyeballs v2; YJIT; modular GC; warning when mutating string literals (R34 p.1-5) |

## Ruby 3.0.0
- `[from source]` Goals: performance, concurrency, typing (R30 p.1). Ractor (R30 p.2-3), Fiber Scheduler (R30 p.3-4), RBS and TypeProf (R30 p.4-5).
- `[from source]` One-line pattern matching redesigned (experimental): `=>` as rightward assignment; `in` now returns true/false, where in 2.7 it raised `NoMatchingPatternError` (R30 p.5-6). Find pattern (experimental) (R30 p.6). "Endless" method definition `def square(x) = x * x` (R30 p.6). Native `Hash#except` (R30 p.6). Memory view, experimental C API (R30 p.6).
- `[from source]` Changes since 2.7: keyword arguments separated from the others; `...` now accepts leading arguments; `case`/`in` stops being experimental; `$SAFE` removed; backtrace order goes back to that of 2.4 (R30 p.7-8).
- `[from source]` No longer bundled gems or stdlib: sdbm, webrick, net-telnet, xmlrpc; rexml and rss become bundled gems (R30 p.8).

## Ruby 3.1.0
- `[from source]` Keeps compatibility with 3.0 (R31 p.1). Experimental YJIT (R31 p.1-2); debug.gem (R31 p.2-3); error_highlight (R31 p.3-4); IRB autocompletion (R31 p.4).
- `[from source]` Language: omitted values in Hash literals and keyword arguments (`{x:, y:}`, `foo(x:, y:)`); the pin `^` accepts an expression; optional parentheses in one-line pattern matching (R31 p.5). One-line pattern matching (`ary => [x, y, z]`) stops being experimental; the evaluation order of multiple assignment changes; Psych 4.0 (R31 p.8).
- `[from source]` Gems that move from default to bundled: net-ftp, net-imap, net-pop, net-smtp, matrix, prime, debug (R31 p.11). RBS: generic parameters with bounds, generic aliases, `rbs collection` (R31 p.5-6). Experimental TypeProf for IDE (R31 p.6-7).

## Ruby 3.2.0
- `[from source]` WASI (R32 p.1-3); production YJIT (R32 p.4-5); ReDoS (R32 p.5-7); SyntaxSuggest and ErrorHighlight for TypeError/ArgumentError (R32 p.8).
- `[from source]` Language: anonymous `*` and `**` can be forwarded; a proc with one positional parameter and keywords no longer autosplats; evaluation order of constant assignment; find pattern stops being experimental; `ruby2_keywords` mandatory to delegate keywords via `*args` (R32 p.8-10).
- `[from source]` `Data` (R32 p.11-12); built-in `Set` without `require "set"` (autoload via the constant `Set` or `Enumerable#to_set`) (R32 p.15); `Struct` accepts keyword initialization without `keyword_init: true` (R32 p.15); `Hash#shift` on an empty hash always returns `nil` (R32 p.12); Unicode 15.0 (R32 p.15). Removals (R32 p.16).
- `[from source]` Bundler 2.4 uses the PubGrub resolver; RubyGems continues with Molinillo (R32 p.11).

## Ruby 3.3.0
- `[from source]` Prism as a default gem and Lrama in place of Bison (R33 p.1-2); YJIT (R33 p.2-3); RJIT in place of MJIT (R33 p.4); M:N threads (R33 p.4-5); GC (R33 p.5); IRB (R33 p.5-6).
- `[from source]` Compatibility: `it` calls without arguments in a block without ordinary parameters are deprecated (it will be a reference to the first parameter in 3.4); `Regexp::new` with at most 2 arguments (R33 p.6); `ext/readline` retired in favor of `reline` (R33 p.7).
- `[from source]` RubyGems/Bundler warn when `require`-ing gems that will become bundled without declaring them in the Gemfile/gemspec: abbrev, base64, bigdecimal, csv, drb, getoptlong, mutex_m, nkf, observer, racc, resolv-replace, rinda, syslog (R33 p.7-8). racc is promoted to a bundled gem (R33 p.10).

## Ruby 3.4.0
- `[from source]` `it` (R34 p.1); Prism default (R34 p.2); Happy Eyeballs v2 (R34 p.2); YJIT (R34 p.3-4); modular GC (R34 p.4); string literals (R34 p.5); Ractor (R34 p.6).
- `[from source]` Compatibility: error messages/backtrace and `Hash#inspect` change (R34 p.8); `Kernel#Float()` and `String#to_f` accept "1." (R34 p.8-9); `Refinement#refined_class` removed (R34 p.9); old `Net::HTTP` constants removed (R34 p.9-10).
- `[from source]` Gems promoted to bundled: mutex_m, getoptlong, base64, bigdecimal, observer, abbrev, resolv-replace, rinda, drb, nkf, syslog, csv, repl_type_completor (R34 p.7).

## Temporal scope [DATED]
- `[from source]` The five captures were taken after 2026 and the "Recent News" section of the pages lists Ruby 4.0.5/4.0.6 and 3.3.12/3.4.10 as recent releases (R30 p.10; R34 p.12). The five notes cover only 3.0 to 3.4; **Ruby 4.0 and 3.x fixes later than .0.0 are not covered**: whatever the user needs about them is `[extrapolation]` and must be checked in the official documentation.
