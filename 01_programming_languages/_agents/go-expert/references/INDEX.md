# Reference index — go-expert

Load **only** the file you need. Every claim cites `(Eff p.N)`, `(Spec p.N)`, `(Little p.N)` or `(RN1.xx p.N)`, with the **PDF** page (not the printed numbering).

| Abbreviation | Work | Era / version | Pages (PDF) | Caution |
|---|---|---|---|---|
| Eff | *Effective Go* | **2009**, not updated | 54 | does not cover generics or modules; the only recent marks are `new` with an expression "as of Go 1.26" (p.15) and the note on the loop before 1.22 (p.44) |
| Spec | *The Go Programming Language Specification* | **go1.26** (Jan 12, 2026) | 117 | newer than the covered RN; the version appendix ends at 1.24 (p.114-116) |
| Little | *The Little Go Book* (Karl Seguin) | **go1.3.3**, GOPATH | 84 | very dated; printed page = PDF page − 1 |
| RN1.20 … RN1.24 | official release notes | Go 1.20 to 1.24 | 15, 16, 14, 11, 15 | **no 1.25 or 1.26** |

**Golden rule:** Spec and RN prevail over Eff and Little when they diverge. Mark **[DATED]** whatever comes from the old sources.

## Page convention

- `(SIGLA p.N)` is always the **PDF** page in the `01_programming_languages` folder (`Go-Effective-Go.pdf`, `Go-Language-Specification.pdf`, `Go-The-Little-Go-Book.pdf`, `Go-1.20-Release-Notes.pdf` … `Go-1.24-Release-Notes.pdf`).
- **Little:** the PDF shows the printed number in the footer of each page, and it is the PDF number minus 1 (PDF page 43 shows "42"). The package **always** uses the PDF number; the printed page is N − 1. Tell the user so when citing Little.
- Eff, Spec and RN carry no printed page number in the extracted text (checked at the start and end of several pages): only the PDF page exists.
- Ranges: `p.N–M` or `p.N-M` = from page N to M. A citation with several pages does not mean the claim is on both: when the claim is on a single page, the package should cite only that one (the automatic check verifies the set).
- Verification: `tests/verify_citations.py` (positive/negative checks and the scripts' index), `tests/audit_tokens.py` (backticked terms against the cited page) and `tests/run_script_tests.py`; see `tests/relatorio-de-fidelidade.md` for what was and was not audited.

## When to open each file

| I need… | Open | Size |
|---|---|---|
| What a term means (type set, receiver, GODEBUG, iterator…) | [glossario.md](glossario.md) | ~4 thousand words |
| Deciding between approaches: pointer vs value, errors, interfaces, channels vs mutex, embedding | [frameworks.md](frameworks.md) | ~5.8 thousand |
| Step-by-step procedures and review checklists by area | [procedimentos.md](procedimentos.md) | ~3.2 thousand |
| Pitfalls, anti-patterns and examples | [casos-e-antipadroes.md](casos-e-antipadroes.md) | ~3.7 thousand |
| Fine language rules: assignability, conversions, constants, panics, **generics**, versions marked in the Spec | [regras-da-spec.md](regras-da-spec.md) | ~7.4 thousand |
| In which version X appeared, what changes when migrating, GODEBUG, 1.19→1.24 checklist | [versoes-e-migracao.md](versoes-e-migracao.md) | ~9.2 thousand |
| Quickly find the topic and pages (or learn that there is **no coverage**) | `python -I scripts/go_lookup.py "topic"` | — |
| Review checklist by area with the source and page of each item | `python -I scripts/go_checklist.py AREA` | — |

## Shortcuts by question

- "Which version introduced X?" → `versoes-e-migracao.md` §1 (master table); skill `go-version-migration`.
- "My test broke after bumping `go`" → `versoes-e-migracao.md` §3 (silent items) and §5 (GODEBUG).
- "Goroutine in a loop" → depends on the `go` line: `versoes-e-migracao.md` §3.1 + `casos-e-antipadroes.md` §2.6; skill `go-concurrency-review`.
- "`cannot infer T`, type set, `comparable`" → `regras-da-spec.md` §4; skill `go-generics-review`.
- "Slice/map/pointer behaves strangely" → `casos-e-antipadroes.md` and `regras-da-spec.md` §3.4 and §3.12.
- "Run-time panic" → `regras-da-spec.md` §5.
- "GOPATH, `go get`, `godoc`" → **[DATED]** in `procedimentos.md` §10; Go 1.22 changed `go get` in GOPATH mode (`versoes-e-migracao.md` §1.2).

## Page map (PDF)

The maps below were checked against the titles in the extracted text. The Spec map is in `regras-da-spec.md` §2.

**Eff (54 pp.):** p.1 table of contents and era notice · p.2-3 formatting, indentation, comments · p.3-5 names (package p.4, getters p.4, `-er` interfaces p.5, MixedCaps p.5) · p.5 semicolons · p.6-7 `if`, redeclaration · p.8 `for` · p.9-11 `switch`, type switch · p.11-13 functions, multiple returns, named results · p.13-14 `defer` · p.15-17 `new`, constructors, composite literals · p.17 `make`, arrays · p.18-19 slices · p.19-20 2D slices · p.20-22 maps · p.22-25 printing (`fmt`) · p.25-26 `append` · p.26-27 constants and `iota`, variables · p.28 `init`, methods · p.28-29 pointers vs values · p.29-33 interfaces, conversions, type assertion · p.33-36 interfaces and methods (`HandlerFunc`) · p.36-38 the `_` identifier · p.38-39 import for side effect, interface check · p.39-42 embedding · p.42-47 concurrency (goroutines p.42-43, channels p.43-45, parallelization p.46-47) · p.47-48 free list · p.48-49 errors · p.49-52 panic and recover · p.52-54 example web server.

**Little (84 pp.; printed = PDF − 1):** p.2-4 about the book · p.6-8 introduction · p.10-13 installation (GOPATH, go1.3.3 on p.11-12) · p.14-18 what Go is (compiled, typed, GC) · p.19-22 running code, `main`, imports, `godoc` · p.23-27 variables and functions · p.28-33 structs, constructors, `new` · p.35-36 composition · p.36 overloading · p.37-38 pointers vs values · p.41-46 arrays and slices · p.47-48 maps · p.49-50 pointers vs values (collections) · p.53-57 packages (cycles p.54, visibility p.56, `go get` p.56-57) · p.58-60 interfaces · p.63-64 errors · p.65 `defer` · p.67 `if` with initialization · p.68 empty interface, conversions · p.69 strings and bytes · p.70 function type · p.73-76 goroutines and synchronization · p.77-79 channels · p.79 buffer · p.80-81 `select` and timeout · p.84 conclusion.

**RN (each version):** language on p.1 (and p.1-3 in 1.21, with `panic(nil)` on p.3) · tools/`go` command p.2-3 (1.20: p.2-4; 1.21: p.3-4) · `vet` (1.20: p.4-5; 1.22: p.3; 1.23: p.2; 1.24: p.3) · runtime/compiler/linker (1.20: p.5-6; 1.21: p.4-5; 1.22: p.4-5; 1.23: p.3-4; 1.24: p.3-4) · standard library (1.20: p.6-15; 1.21: p.5-14; 1.22: p.5-12; 1.23: p.4-11; 1.24: p.4-14) · platforms (1.20: p.2, p.6, p.15; 1.21: p.15-16; 1.22: p.13-14; 1.23: p.11; 1.24: p.14-15). Specific points: telemetry RN1.23 p.2 · Timer/Ticker RN1.23 p.4 · iterators RN1.23 p.4-5 · `math/rand/v2` and `ServeMux` RN1.22 p.5-6 · `math/rand` RN1.20 p.11-12.

## What the package does NOT provide (do not treat as fact)

- **Go 1.25 and 1.26:** no release notes (only isolated marks: `new(expr)` = 1.26 per Eff p.15; future notices in RN1.24).
- **`sync.WaitGroup`, `errgroup`:** absent from all four sources. **`context`:** only isolated novelties in the RN (RN1.20 p.8; RN1.21 p.7).
- **Tests** (`go test`, benchmarks, `-race`), **linters**, **doc comments** (Eff points to "Go Doc Comments", which is not in the sources), **modules in depth**, `errors.Is/As` in use (the RN only mention `errors.Join` and multiple `%w`).
- **`log/slog`, `slices` and `maps` API from 1.21:** only announced (RN1.21 p.6); for `cmp` only `Ordered`, `Less` and `Compare` are listed.
- **"Accept interfaces, return structs", "when to use generics", the nil-in-interface trap (only a deduction from Spec p.12 + p.69), the "cannot infer T" text:** are not in any source.
- Reversion values for `multipartmaxheaders`, `multipartmaxparts`, `x509keypairleaf`, `winsymlink` and `winreadlinkvolume` are not in the notes.
- Performance, third-party libraries and frameworks, other languages.

## How to read large files

`regras-da-spec.md`, `versoes-e-migracao.md` and `frameworks.md` exceed the limit for reading at once. Do not read the whole file: list the sections with `Grep` (pattern `^#{2,3} `, with `-n`), pick the section and read only it with `Read` (`offset`/`limit`). Very long table lines come out truncated in Grep: use `Read` by offset. For a term or code, `Grep` across all files in `references/` before concluding that something is not covered.

## Marking conventions

- **[DATED]**: comes from an old source and may have been superseded by the Spec/RN.
- **[inference]**: link made during consolidation (deduction, cross-page reading or claim of absence), not stated by the source.
- **[extrapolation]**: knowledge outside the sources; must be labeled in the answer.
- **[NOT VERIFIED IN THE PDF]**: a point the sources do not confirm; valid only when the reference file itself carries it.

## Reading cautions

- The text was extracted from PDF: figures and tables may be incomplete.
- The Spec was distilled selectively (pitfalls, generics, panics, versions); `go`, `select`, `defer`, most built-ins, `init` dependency and the `unsafe` tables have little distilled content: use the page map and read the Spec.
- The Go 1.21 notes only **announce** `log/slog`, `slices` and `maps`, without listing the API; for `cmp` they say only that it defines `Ordered`, `Less` and `Compare` (RN1.21 p.6).
- Effective Go only describes the basics of comments and points to "Go Doc Comments", which is not in the sources.
- Check labels: the package has ~2,500 citations; automatic verification covers the backticked terms and the ~115 curated checks, not every sentence (see `tests/relatorio-de-fidelidade.md`).
