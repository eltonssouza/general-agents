# Reference index — rust-expert

Load **only** the file you need. Every claim cites `(Book p.N)`, `(Ref p.N)` or `(RBE p.N)`.

## Page convention (read first)

**`p.N` is always the PDF page** (the N-th page of the file, the same as the `=== PAGE N ===` markers of the extracted text), **not** the printed numbering. There is no fixed offset between the two: always check the PDF page. This convention was verified in this audit and is consistent across the whole package (no citation outside 1–719 in the Book, 1–710 in the Ref, 1–364 in the RBE).

| Sources | Abbreviation | PDF | Pages | Edition / version |
|---|---|---|---|---|
| *The Rust Programming Language* (Klabnik, Nichols, Krycho) | Book | `Rust-The-Rust-Programming-Language.pdf` | 719 | Rust 1.90.0, edition 2024 (Book p.1) |
| *The Rust Reference* | Ref | `Rust-Reference.pdf` | 710 | stable at the time of the PDF (describes the most recent edition, Ref p.3) |
| *Rust by Example* | RBE | `Rust-by-Example.pdf` | 364 | stable at the time of the PDF (dated examples, e.g. clap 2.27.1 in RBE p.130) |

## Labels used in the package

- **[from source]**: the cited page supports the specific claim.
- **[inference]**: a connection made by the package from the pages; they do not state it.
- **[extrapolation]**: knowledge external to the sources, useful but not attributable to them.
- **[DATED]**: depends on a version (Rust 1.90, `rand` 0.8.5, `trpl`, clap 2.27.1, compiler outputs, Miri/nightly).
- **[NOT VERIFIED IN THE PDF]**: a point the sources do not confirm; do not treat it as fact.
- **[VERIFIED IN THE PDF]**: a discrepancy between notes resolved by checking the source text.

## When to open each file

| I need… | Open | Size |
|---|---|---|
| What a term means (ownership, `Pin`, `dyn compatible`…) | [glossario.md](glossario.md) | ~3.6k words |
| Choosing between approaches: error handling, generic vs `dyn`, smart pointers, threads vs async, state, macros, modules | [frameworks.md](frameworks.md) | ~6.5k |
| Step by step: Cargo, tests, CLI "thin binary + lib", workspace, crates.io, derive macro, thread pool, review by area | [procedimentos.md](procedimentos.md) | ~5.5k |
| A compiler error, an antipattern, an illustrative example | [casos-e-antipadroes.md](casos-e-antipadroes.md) | ~6k |
| Fine-grained language rule: UB, layout, drop order, closures, macros, FFI, differences between editions, "where to look" in the Reference | [regras-da-referencia.md](regras-da-referencia.md) | ~8.4k |

Shortcut by topic, with pages: `python -I scripts/rust_lookup.py "<term>"` (see "Scripts" below).

## Page map (PDF)

### Book (719 p.)

| Part | Pages | Part | Pages |
|---|---|---|---|
| Preface and introduction | 1–7 | Ch. 12: I/O project (minigrep) | 315–351 |
| Ch. 1: getting started (rustup, Cargo) | 8–22 | Ch. 13: closures and iterators | 352–382 |
| Ch. 2: guessing game | 23–44 | Ch. 14: more about Cargo and crates.io | 383–407 |
| Ch. 3: common concepts | 45–81 | Ch. 15: smart pointers | 408–456 |
| Ch. 4: ownership | 82–115 | Ch. 16: concurrency | 457–484 |
| Ch. 5: structs | 116–138 | Ch. 17: async | 485–534 |
| Ch. 6: enums and `match` | 139–159 | Ch. 18: object-oriented programming | 535–562 |
| Ch. 7: packages, crates and modules | 160–186 | Ch. 19: patterns | 563–590 |
| Ch. 8: collections | 187–209 | Ch. 20: advanced features (unsafe, traits, macros) | 591–644 |
| Ch. 9: errors | 210–233 | Ch. 21: final project (web server) | 645–690 |
| Ch. 10: generics, traits, lifetimes | 234–274 | App. A keywords 692–695; B operators 696–702; C derivable traits 703–706 | |
| Ch. 11: tests | 275–314 | App. D tools 707–710; E editions 711–712; F translations 713; G Rust and nightly 714–718 | |

### Reference (710 p.)

Full "topic → pages" map in [regras-da-referencia.md](regras-da-referencia.md) (section 2). Summary: lexical 9–44; macros 46–75; crates and conditional compilation 76–91; items (modules, functions, structs, traits, impls, extern, generics) 92–188; attributes 190–255; statements and expressions 257–367; patterns 368–391; types 393–448; layout and `repr` 449–463; variance and coercions 464–483; destructors 484–497; elision 498–502; names, paths and visibility 508–560; memory model, panic and linkage 561–575; inline asm 576–619; unsafety and UB 620–631; const eval 632–637; ABI and runtime 638–643; appendices 645–710.

### Rust by Example (364 p.)

Hello and formatting 3–18; primitives 19–27; custom types 28–39; bindings 40–44; casting and inference 45–51; conversions 52–58; control flow 60–87; functions and closures 88–111; modules 112–124; crates and Cargo 125–136; attributes 137–142; generics 143–165; scope, RAII and ownership 166–180; lifetimes 181–194; traits 195–220; `macro_rules!` 221–231; errors 232–269; std types 270–298; std misc (threads, channels, fs) 299–326; FFI 327–329; tests 330–342; unsafe 343–344; asm 345–356; compatibility 357–358; rustdoc 359–364.

## Shortcuts by question

- "Why does the compiler say E0xxx?" → `casos-e-antipadroes.md` (Part 1, by topic); then the skill `rust-compiler-error-triage`.
- "What is the difference of edition 2021/2024 for this?" → `regras-da-referencia.md` (editions table); skill `rust-edition-migration`.
- "Is this `unsafe` safe?" → `regras-da-referencia.md` (UB, FFI) + skill `rust-unsafe-audit`.
- "Threads or async?" → `frameworks.md` (Concurrency) + skill `rust-concurrency-async-review`.
- "How to publish / organize / test?" → `procedimentos.md`.
- "Rc, Weak, cycles, parent-child tree, `weak_count`?" → `glossario.md` (smart pointers section) + `procedimentos.md` (recipe "Parent/child cycle without a leak") + `frameworks.md`.
- "Temporaries in `if let`/`match`, drop order by edition?" → `frameworks.md` (temporaries) and `regras-da-referencia.md` (editions table and drop order); read both.
- "`Mutex`, deadlock?" → `frameworks.md` (Concurrency) and `procedimentos.md`. Atomic types: the Book only mentions them as an alternative for simple counters (Book p.482); the Reference uses `AtomicUsize::new` and `fetch_add` only inside a `static` example (Ref p.143), without documenting the API. Explaining atomics (orderings, `compare_exchange`) is an **[extrapolation]**.

## What the sources do NOT contain (use `scripts/rust_lookup.py` to confirm)

Confirmed by searching the three extracted sources (whole word, see `tests/citation-checks.json`, negative checks N01–N29): the atomics API (`AtomicUsize`, `fetch_add`, `SeqCst`) in the Book; the error code `E0038`; `async-std`, `thiserror`, `anyhow`, `crossbeam`, `rayon`, `parking_lot`; `RwLock`, `Condvar`, `Barrier` and `thread::scope` in the Book; the `cargo fix --edition` flag; the `cargo fmt --check` flag; `no_std` in the Book; `cargo audit`/`cargo deny`; the Stacked/Tree Borrows aliasing models. Choice of crates, performance, cross-compilation and the web ecosystem are out of scope (see the `limites` field of `scripts/rust_index.json`).

## Scripts (standard Python 3, no network, read-only; use `python -I`)

- `scripts/rust_lookup.py "<term>"` (or `--topic ID`, `--list`): file, section and PDF pages; prints **NOT COVERED** (exit 1) when the index does not cover the term.
- `scripts/rust_checklist.py <area>` (`revisao`, `erros`, `ownership`, `unsafe`, `concorrencia`, `edition`, `todas`): checklist with the label and page of each item.
- `scripts/scan_rust_smells.py [--profile review|unsafe|all] [--rules] PATH`: regex triage of Rust code; each finding carries its origin (label and page).
- Data: `scripts/rust_index.json`, `scripts/rust_checklists.json`. Tests: `tests/verify_citations.py`, `tests/audit_tokens.py`, `tests/run_script_tests.py` (they need the extracted text of the PDFs).

## How to read large files

`regras-da-referencia.md`, `frameworks.md`, `casos-e-antipadroes.md` and `procedimentos.md` exceed the limit for reading at once. Do not read the whole file: list the sections with `Grep` (pattern `^#{2,3} `, with `-n`), pick the section and read only it with `Read` (`offset`/`limit`). For a term or error code, use `Grep` for the term across all files in `references/` (or `scripts/rust_lookup.py`) before concluding that something is not covered.

## Reading cautions

- The text was extracted from PDF: illegible figures, linearized tables, listings and example code displaced to the end of the page, Reference rule ids almost absent. In the Reference, pages 189, 252, 528 and 568 are empty and pages 8, 332, 392, 413 and 644 almost empty; in the Book, page 719.
- The Book was distilled in blocks cut by size; a section may cross the boundary (see "Block boundaries" in `regras-da-referencia.md`).
- The Reference was distilled selectively (pitfalls, UB, editions), **not** summarized in full. `target_feature` tables, `asm!` registers and grammar were left only in the page map.
- **[DATED]**: examples pin `rand` 0.8.5; the chapter 17 `trpl` crate is a support crate for the book; Miri requires nightly; the RBE uses clap 2.27.1; compiler outputs change between versions.
- Audit v2 coverage: see `tests/relatorio-de-fidelidade.md` (stratified sample; the package is too large for a full audit).
