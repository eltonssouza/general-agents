# Reference INDEX: ruby-expert

## Sources and abbreviations
Five PDFs, each a **web page capture** (ruby-lang.org/en/news) of the official release note. They are real notes (not empty captures), but short: 71 pages in total.

| Abbreviation | PDF (in `01_programming_languages/`) | Pages | Note |
|---|---|---|---|
| R30 | `Ruby-3.0-Release-Notes.pdf` | 10 | Ruby 3.0.0 Released, Dec 25, 2020 |
| R31 | `Ruby-3.1-Release-Notes.pdf` | 13 | Ruby 3.1.0 Released, Dec 25, 2021 |
| R32 | `Ruby-3.2-Release-Notes.pdf` | 23 | Ruby 3.2.0 Released, Dec 25, 2022 |
| R33 | `Ruby-3.3-Release-Notes.pdf` | 13 | Ruby 3.3.0 Released, Dec 25, 2023 |
| R34 | `Ruby-3.4-Release-Notes.pdf` | 12 | Ruby 3.4.0 Released, Dec 25, 2024 |

## Page convention (mandatory)
- `(R3x p.N)` = **PDF page** (the same numbering as the `=== PAGE N ===` markers of the text extracted with `tests/extract_pages.py`).
- The notes are web pages: **there is no printed numbering**. Pagination depends on how the PDF was generated; if the PDF is recaptured, the pages may change and `tests/verify_citations.py` must be run again.
- When answering, say "R3x p.N (PDF page)" at least once.
- Each PDF ends with download blocks (hashes) and "Recent News"; there is no technical content on those final pages (except the [DATED] notice below).
- The PDFs captured in 2026 show, in "Recent News", Ruby 4.0.5/4.0.6 and 3.3.12/3.4.10 (R30 p.10; R34 p.12). **The notes do not cover Ruby 4.0** or later updates: `[DATED]`.

## Page map
| Topic | R30 | R31 | R32 | R33 | R34 |
|---|---|---|---|---|---|
| Overview / goals | 1-2 | 1 | 1 | 1 | 1 |
| JIT (MJIT, YJIT, RJIT) | 2 | 1-2, 7-8 | 3-5, 11 | 2-4 | 3 |
| Ractor / Fiber Scheduler / M:N | 2-4 | - | - | 4-5 | 6 |
| RBS / TypeProf | 4-5 | 5-7 | - | - | - |
| Pattern matching / syntax | 5-7 | 5, 8 | 8-10 | 6 | 1, 5 |
| Parser (Prism, Lrama) | - | - | 13-14 (AST) | 1-2 | 2 |
| Debug / error_highlight / SyntaxSuggest | - | 2-4 | 8 | - | - |
| WASI | - | - | 1-3 | - | - |
| ReDoS / Regexp.timeout | - | - | 5-7 | 6 | - |
| GC / memory | - | 8 | 4 | 3, 5 | 4-6 |
| Compatibility / removals | 7-8 | 8 | 16-17 | 6-8 | 8-10 |
| Default/bundled gems | 8-9 | 8-11 | 18-21 | 7-11 | 7 |
| Download / hashes / Recent News | 9-10 | 11-13 | 21-23 | 11-13 | 11-12 |

## Thematic references
| File | Content |
|---|---|
| `concorrencia-e-paralelismo.md` | Ractor, Fiber Scheduler, M:N threads, Happy Eyeballs v2 |
| `compilacao-jit-e-performance.md` | Ruby 3x3, MJIT, YJIT, RJIT, GC, modular GC |
| `sintaxe-e-recursos-de-linguagem.md` | pattern matching, arguments, `it`, string literals, `Data`, `Struct` |
| `tipagem-estatica-e-ferramentas.md` | RBS, TypeProf, Prism/Lrama, debug, error_highlight, SyntaxSuggest, WASI |
| `seguranca-e-resiliencia.md` | ReDoS, `Regexp.timeout`, API removals, backtraces |
| `versoes-e-evolucao.md` | timeline 3.0 to 3.4 and temporal scope |
| `casos-e-antipadroes.md` | cases and pitfalls, separating source from package |
| `procedimentos.md` | YJIT, Ractor, regex, TypeProf, strings, migration |
| `glossario.md` | terms the notes use; list of what they do not contain |

## Epistemic labels
- `[from source]`: it is on the cited page of R30 to R34. Only with a page actually read.
- `[inference]`: explicit deduction from what the notes say.
- `[extrapolation]`: general Ruby knowledge that the notes do not contain.
- `[DATED]`: about superseded versions/tools (MJIT; everything after 3.4).
- `[VERSION-DEPENDENT]`, `[HOST]`: feature restricted to one Ruby version, or to a platform/architecture.

## What the notes do NOT contain (`not_in_book`)
GVL/GIL; Ractor `shareable`/`move` rules; `Fiber.set_scheduler`; `RUBY_YJIT_ENABLE`; YARV and Onigmo; byebug (only `pry-byebug` in R33 p.6), Steep, DAP; Rails, Puma, Sidekiq, RSpec; complexity ($O(2^n)$); `FrozenError`/`Ractor::IsolationError`; Ruby 4.0; complete migration instructions. Use `skills/ruby-feature-lookup/scripts/ruby_feature_lookup.py` (answers `NOT COVERED`).
