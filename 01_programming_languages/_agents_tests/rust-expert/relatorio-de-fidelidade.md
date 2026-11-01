# Fidelity report — rust-expert (audit v2)

Date: 2026-10-26. Sources: *The Rust Programming Language* (Book, Rust 1.90, edition 2024, 719 p.), *The Rust Reference* (Ref, 710 p.), *Rust by Example* (RBE, 364 p.). Page convention: **PDF** (the `=== PAGE N ===` marker of the text extracted with PyMuPDF), consistent throughout the package.

This report **replaces** the v1 one, which only claimed to validate page ranges and reported blind executions by subagents that this audit **did not reproduce** (see section 7).

## 1. What was done

1. **Inventory**: the three sources were extracted page by page. The package convention (PDF page) was confirmed: none of the 1,538 citations in v1 falls outside 1–719 (Book), 1–710 (Ref), or 1–364 (RBE), and the pages checked by reading match the PDF numbering. The package is too large to audit sentence by sentence (~230 KB of references, ~1,500 citations): the audit is by **declared stratified sampling** (section 5).
2. **Backup** of the original package before any change.
3. **Automatic layer** (`tests/audit_tokens.py`): reads all `(Book|Ref|RBE p.N...)` citations from all `.md` files in the package, extracts the backticked terms and the `E0xxx` codes from the cited passage, and looks for them (ignoring whitespace/case) in the cited pages, classifying them as OK / only in another citation on the same line / paraphrased notation / neighboring page / FAIL. A second pass (numeric check, not distributed) compared numbers in the text with the cited pages.
4. **Curated checks layer** (`tests/verify_citations.py` + `tests/citation-checks.json`): **154 positive checks** (terms that must be on the cited pages), **29 negative** (plausible claims the sources do not carry; whole-word search across all pages), and **202 script-data checks** (each entry of `rust_index.json` and each item of `rust_checklists.json` has its terms checked on the pages it cites; each section pointed to in the index exists).
5. **Manual sample**: 149 claims classified after reading the cited page (section 3), covering the 5 files in `references/`, the 5 skills, the index, and the script rules.
6. **Fixes** (section 4), **structure** (AGENTS.md, Copilot agent, README with 3 platforms, INDEX with page map, revised prompt), and **new scripts** (`rust_lookup.py`, `rust_checklist.py`, declared origin in `scan_rust_smells.py`).
7. **Tests** (`tests/casos-de-teste.md`, 32 cases; `tests/run_script_tests.py`).

## 2. Results of the automatic layer (v1 package, final tool)

| Measure | Value |
|---|---|
| Citations extracted (`.md` files of the v1 package) | 1,538 |
| Pages outside the PDF range | 0 |
| Technical terms checked | 2,644 |
| Present on the cited page | ≈ 2,284 |
| Only in another citation on the same line (passage with several citations) | 51 |
| Package notation whose words are all on the pages (e.g., `Arc<Mutex<T>>`) | 170 |
| Only on a neighboring page (±1) | 19 |
| Raw FAIL (not found on the cited pages) | 120 |

Triage by reading of the 120 FAIL and the 19 NEAR: most are **package notation in Portuguese or code abbreviations** (`nome.rs`, `[T; N]`, `for x in coleção`, `{:?}`), code that the PDF extraction does not preserve literally, or a **deliberate negative claim** (`E0038`, `fmt --check`); those items went into `tests/audit-tokens-baseline.txt`. The rest were **real page or backing errors** and were fixed (section 4; e.g., `HashSet` in RBE p.277–279 being RBE p.294–295; Miri in Book p.717 being p.604–605; "256 variants" without backing). The numeric check flagged 52 lines, almost all false positives of the method (a number that belongs to another citation on the same line); **1** was a number without backing (the 256).

Final state with the corrected package: `audit_tokens.py` → 0 FAIL (111 occurrences in 106 entries of the reviewed baseline, plus 176 of paraphrased notation); `verify_citations.py` → 154 positive, 29 negative, and 202 data checks, 0 failures.

## 3. Manual sample (149 claims, cited page read)

| Verdict | Count | Meaning |
|---|---|---|
| OK | 106 | the specific claim is on the cited page |
| Wrong or imprecise page | 25 | the content exists in the sources, but on another page (or the list omitted the right page) |
| No backing | 11 | the page does not carry the claim (number, rule, flag, recommendation) |
| Overstated | 7 | the page carries something more restricted than what the package claimed |

Distribution by file (errors = page + no backing + overstated): `regras-da-referencia.md` 47 (3 errors), `frameworks.md` 24 (1), `procedimentos.md` 23 (11), `casos-e-antipadroes.md` 18 (2), `glossario.md` 17 (9), skills 13 (11), `INDEX.md` 2 (1), `scan_rust_smells.py` 5 (5 rules without origin or with overstated text). Each line of the sample groups a claim and the cited page; some group several sentences from the same page.

**Relevant examples of what was without backing or overstated** (all fixed):

1. `procedimentos.md` 14.4: "`repr(C, u8)` limits to 256 variants (Ref p.454, 457–461)": the 256 is not on those pages; it became **[inference]**, and "`repr` on an enum without variants is an error" was restricted to the primitive representation (Ref p.459).
2. `procedimentos.md` 14.1: "`cfg!` compiles both branches (Ref p.89–90)": the Reference only says `cfg!` becomes `true`/`false`; it became **[inference]**.
3. `procedimentos.md` 14.1: "`#[must_use]` does not fire on tuple/`Some`/`if`/`match` (Ref p.216–217)": it omitted that the type-based check still applies.
4. `procedimentos.md` 14.6: "`transmute` from pointer to integer is UB (Ref p.628–629)": the page restricts it to the **const context** (provenance).
5. `INDEX.md`: "the API (`AtomicUsize`, `fetch_add`) is not in the sources": Ref p.143 uses `AtomicUsize::new` and `fetch_add` in a `static` example (without documenting the API); the negative was rewritten and gained check N01.
6. `skills/rust-code-review`: `cargo fmt --check` with "Book p.707–709": the flag is in no source (**[extrapolation]**; check N24); the same skill cited "`&[T]` instead of `&Vec<T>`" and "overflow" on wrong pages (Book p.133 and p.59/79–80, when the right ones are p.107–114 and p.54–55).
7. `glossario.md`: "poisoned (Book p.678, 680)" (p.680 does not cover this; correct: p.476, 678), "a release every six weeks (Book p.711)" (correct: p.715–716), `HashSet` in RBE p.277–279 (correct: p.294–295).
8. `scan_rust_smells.py`: no rule declared an origin; `ref-vec`, `allow-lint`, and `unchecked-api` are external conventions (**[extrapolation]**) and `transmute` follows from other rules (**[inference]**); the `static-mut` message ("in 2024 direct references are forbidden") was rewritten to what the Book says (the `static_mut_refs` lint, Book p.602).

What **was correct** and was kept: the bulk of the references is faithful to the pages (106 of 149 with no caveat); the numbers checked (benchmark 19.6/19.2 ms, `recursion_limit` 128, opt-level 0–3, six weeks, Rust 1.90.0 of 2025-09-18) match; the editions table rows that were checked (dyn, divergence fallback, preludes, array and `IntoIterator`, `panic!`, raw lifetimes, anonymous parameters, `a...b`, 2018/2024 keywords, let chains, `unsafe extern`, closure capture, binding modes) are correct; the Reference page map (53 section starts) and the RBE one (28 chapter starts) were checked.

## 4. Fixes applied

- **Pages** (25): glossary (poisoned, six weeks, `HashSet`, `From::from`, `filter`, `from_utf8_lossy`, `zip`, `{:#?}`), procedures (RUST_BACKTRACE, IGNORE_CASE, `output.txt`, Miri, `asm!` options), rules (`_ = f();`, id `input.encoding.utf8`), cases (`yield_now`, label "appendix D"), skills (r#, slices, overflow, `cargo check`, three async pages, `collect`), and test case 8 (`join_all`).
- **No backing, downgraded to [inference]/[extrapolation]** (11): examples 1, 2, and 6 above, `try_from`, `cargo fix` and drop order, alternatives to `static mut`, and the script's 4 rules.
- **Overstated, rewritten** (7): examples 3, 4, 5, and 8 above; headers of `frameworks.md` and `glossario.md` that said there was no Reference; `static_mut_refs` "of the 2024 phase".
- **Standardization**: `references/INDEX.md` with page convention, labels (incl. **[DATED]**), page map of the three PDFs, and a list of what the sources do not carry; `README.md` with installation on the 3 platforms; `AGENTS.md` (Codex); `.github/agents/rust-expert.agent.md` (Copilot); agent prompt with pages in the decision rules, a real scripts section, four labels, and an explicit boundary; `plugin.json` 0.2.0.
- **Scripts**: `rust_lookup.py` + `rust_index.json` (62 topics and 9 limits; "NOT COVERED" with exit 1), `rust_checklist.py` + `rust_checklists.json` (55 items with label and page), `scan_rust_smells.py` moved to `scripts/` with the origin of each rule and `--rules` (the two identical copies inside the skills were removed and the skills point to `<PKG>/scripts/`).
- **Encoding**: UTF-8 without BOM and LF in all text files; no absolute user paths.

## 5. Audit coverage

**Audited**: 100% of the citations for page range; 100% of the backticked terms and E0xxx codes against the cited page (automatic layer, with triage by reading); 154 curated claims and 29 negatives; 149 claims read and classified, distributed across all files in `references/`, all skills, the index, and the scripts, with emphasis on numbers, comparisons, "always/never", versions, editions tables, pattern names, and prompt rules.

**Not fully audited** (declared): sentence-by-sentence reading of `regras-da-referencia.md` (~8.4 thousand words), `frameworks.md`, `procedimentos.md`, `casos-e-antipadroes.md`, and `glossario.md`; sentences without backticks and without numbers were only covered by the manual sample; the linearized tables (variance, `bool`, sizes) were checked by sample; the acceptance criteria of cases 1–19 were checked against pages and terms, not re-executed blind; the extracted text was the source, with no systematic comparison against the rendered pages (visually verified only Book p.639).

## 6. Test execution

`python -I tests/run_script_tests.py --src <txt>`: 21 script tests (cases `CT-20` to `CT-28`, including JSON output, unknown area, and nonexistent path), compilation of the scripts, 51 coverage checks of cases 1–32 in the references, prompt, and skills, `verify_citations.py`, `audit_tokens.py`, and a **mutation self-test** (the verifier rejects a wrong citation and a false negative). Final result: 0 failures.

Cases 1–32 were **executed by the auditor itself** against the agent, references, and scripts (consult, run the script, check the page); cases 20–32 carry the "Execution (v2)" block with what was run. This does not replace a blind test.

## 7. Limits and pending items (read before trusting)

- **There was no blind execution by an independent model.** v1 reports 15 cases executed blind by subagents (4 re-executed after fixes, 19/19 PASS); that execution was not redone here and is not evidence for this audit. Cases 1–19 remain as an answer key derived from the PDF by v1.
- **Sample, not census**: 149 claims among thousands. Residual errors are likely, mainly in long sentences without backticked terms.
- **Text extracted from PDF**: illegible figures, linearized tables, listings shifted to the end of the page; Reference p.189, 252, 528, and 568 empty; Reference rule ids almost absent.
- **[DATED]**: `rand` 0.8.5, `trpl`, clap 2.27.1 (RBE p.130), compiler messages, Miri/nightly. Nothing was compiled or run with `cargo`.
- **Not tested**: installation as a plugin in Claude Code (`claude --plugin-dir`), in Codex, and in Copilot; the agent format of the three platforms may have changed (see the notice in the README).
- **Pending**: (a) the edition in which `unsafe_op_in_unsafe_fn` warns by default remains **[NOT VERIFIED IN THE PDF]**; (b) the conflict between Ref p.66/690 and p.695 on repetition without a separator in `macro_rules!` remains open; (c) `while` with let chains and guard-let have no confirmed edition; (d) an independent blind execution of the 32 cases is missing.

## Appendix: manual sample

The full list (149 lines: area, claim, citation, verdict, note) is in `scratch/audit/rust-expert/notes/manual_sample.tsv`, outside the package.
