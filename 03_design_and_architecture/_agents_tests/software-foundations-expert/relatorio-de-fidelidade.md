# Fidelity report: `software-foundations-expert` (audit v1 → v2)

**Scope**: agent `software-foundations-expert`, sources SICP, TAUP and CI (PDFs in `03_design_and_architecture/`). **Method**: extraction of the text of the three PDFs with PyMuPDF (markers `=== PAGE N ===`, N = PDF page); backup of the v1 package; automatic audit of all citations and terms; audit by reading the cited pages; correction; new verifiers; execution of test cases. **The old report only validated the page range and declared "100% fidelity"; that was not supported** (see section 3).

## 1. Inventory of the sources
| Acronym | File | Pages (PDF) | Complete? | Numbering |
|---|---|---|---|---|
| SICP | `SICP-Structure-and-Interpretation-of-Programs.pdf` | 634 | Yes (chs. 1-5, references, index); 6 pages with <200 characters (cover/blank) | No printed numbering; online edition (web sections) |
| TAUP | `The-Art-of-Unix-Programming.pdf` | 549 | Yes (chs. 1-20, appendices A-D, colophon) | Printed = PDF − 2 (footers checked on PDF p.27-549); table of contents on PDF p.3-11 uses printed numbers |
| CI | `Crafting-Interpreters-Nystrom.pdf` | 630 | **Almost**: **chapter 9 (Control Flow) is not included** (p.139 → p.140, from ch. 8 to ch. 10); opening pages of Parts II and III out of order (p.231-232) | No printed numbering; web edition capture |

All three are complete captures/editions with extractable text (they are not samples). The other PDFs in the folder belong to other agents. Figures (SICP frames, CI diagrams) do not appear in the text.

**Page convention in v1**: inconsistent. For SICP and CI it used numbers that generally do not match the PDF (SICP: "p.31" for the substitution model, which is on p.28-31; "p.397" for `amb`, on p.379-381; "p.476-485" for stop-and-copy, on p.489-494). In TAUP it used the **printed page** for the ch. 1 rules (PDF − 2) and the **PDF page** for the chapters (`Ch. 5 p.132-160`), without warning. **v2 convention**: PDF page for everything, with a map in `references/INDEX.md` and the TAUP conversion (printed = PDF − 2).

## 2. Audit counts
- **Citations in v1**: 269 instances `(SIGLA p.N[-M])` in .md, .py and .json; none outside the PDF page range (which is what the old report validated).
- **Curated sample**: 140 claim–page pairs from v1 (covering all 14 reference files, the prompt and the scripts), each checked by key terms against the cited page and, when it failed, searched across the whole book. Result in `scratch/audit/software-foundations-expert/notes/v1_manual_audit.md`:

| Class | Count | % |
|---|---|---|
| OK (terms on the cited page) | 55 | 39% |
| Wrong page (the content exists on another page) | 70 | 50% |
| No basis (the term/claim is not in the book) | 14 | 10% |
| Exaggeration (the book says less) | 1 | 1% |

  Some of the 55 "OK" match by coincidence with list pages or generic terms: the TAUP rules were on **printed** pages (PDF − 2), so under the PDF convention most of them point to the wrong page, even though the term is found on the neighboring page. The audit of backticked terms of v1 (`audit_tokens.py` adapted) gave 11 FAIL and 3 NEAR out of 46 terms checked.
- **Manual reading**: I read the real pages of all topics (SICP 1.1.5, 1.3, 2.1-2.5, 3.1-3.5, 4.1-4.3, 5.3-5.4; TAUP ch. 1, 5, 7, 8, excerpts of ch. 11 and 15; CI ch. 2, 4-6, 11, 14-15, 17, 21-22, 24-26, 30) to rewrite the references; I classified as "wrong page" when the content was on another page and "no basis" when it was on none.

### 2.1 Examples of what had no basis or was wrong in v1
1. **"Dynamic scope (TAUP p.364)"**: the expression does not exist in TAUP or SICP; only CI defines it (p.131, p.161). Corrected to CI p.131 and declared in `not_in_book`.
2. **"Closure (function) (SICP p.230)"**: SICP **rejects** that sense of "closure" (p.141, note 6). v1 attributed to the book a definition that it avoids.
3. **"Homoiconicity (SICP p.334)"** and **"Cheney's algorithm (SICP p.476-485)"**: neither term appears in SICP (Cheney only in CI p.533, in an exercise); stop-and-copy is in SICP p.489-494.
4. **"Bytecode is 10x to 50x faster than tree-walk" and "5x to 10x less memory" (CI p.233-278)**: these numbers do not exist. The book gives 72 s (jlox) vs 0.5 s (C) on `fib(40)` (CI p.232) and qualitative comparisons (p.233-235). They were also in the script `compiler_pipeline_audit.py`.
5. **"`*vm.ip++` is fast because of the L1 cache and prefetch (CI p.263)"**: the page does not say this; the book's justification is that dereferencing a pointer is faster than indexing (p.261).
6. **"Visitor: double dispatch and Open/Closed Principle (CI p.74)"**: the terms do not appear; the book presents the Visitor as an approximation of the functional style and ties it to the *expression problem* (p.70-72).
7. **"Processes: fault isolation (TAUP p.193) and copy-on-write (p.194)"**: not on those pages (copy-on-write is not in the book); the book discusses threads as a "performance hack" and a last resort (p.192, p.213-216).
8. **"Pratt formulated it in 1973 (CI p.300-305)"**: the book does not give the year; **"90% of cycles in 10% of the code (TAUP printed p.46)"**: the rule exists, but in ch. 15 (TAUP p.412), not in the Rule of Optimization.
9. **Wrong pages in bulk**: Resolver "CI p.187-214" (ch. 11 is p.163-186; p.187-214 is "Classes"); `amb` "p.397-405" (p.379-401); CI GC "p.506-534" ok, but NaN boxing "p.594-606" (p.601-604); abstraction barriers "SICP p.104" (p.94-96); mutex "p.292-294" etc.
10. **Our own examples and relations presented as the book's**: the `quaternion` column of the operation×type table, the idea that message passing is the "foundation of OO with actors/prototypes" (SICP p.189) and the closure property at "SICP p.118-120" (the text is on p.104 and p.141).
11. **Missing chapter**: v1 listed "CI Ch. 4-13 (p.39-232)" without noticing that ch. 9 is not in the PDF.

## 3. What was corrected
- **Rewrote 14 files in `references/`** (all names preserved) and created the page map in `INDEX.md` (convention, chapters, gaps, `not_in_book`). Removed `file:///C:/...` links with user paths.
- **Claims**: each bullet now says what the book says on the cited page, or is downgraded to `[inference]`/`[extrapolation]`, or removed. In the references and the prompt: 260 `[from source]` marks, 30 `[inference]`, 31 `[extrapolation]`, 10 `[DATED]`. Citations (same extraction as the verifier): 901 instances across the whole package.
- **Agent prompt** rewritten (the 40-line one was truncated: it had only guidelines and the script list): it now has frontmatter, scope and boundary, language and labels, page convention, anti prompt-injection, method, decision rules with pages, when to consult `references/` and `scripts/` (real files), response format, epistemic honesty, what the books do not cover and `[DATED]` (100 lines).
- **Scripts**:
  - `foundations_lookup.py`/`foundations_index.json`: index rebuilt (104 entries, all with `verify` terms checked against the pages; 48 → 104 entries); new `NOT COVERED` behavior, `not_in_book` boundary (13 items), `--list`, `--not-in-book`, `--json`.
  - `evaluator_trace.py`: declared origin; it now has a real mini-reducer (substitution, applicative/normal orders, reduction count) and simulations of `set!` and of the environment model with frames; before, it only printed fixed text.
  - `unix_philosophy_checker.py`: pages corrected (PDF); declares that questions, weights and scoring are `[extrapolation]`; `--set`/`--profile`/`--rules`.
  - `compiler_pipeline_audit.py`: unsupported numbers removed; each line has `origin` (`[from source]` with a page or `[inference]`); new topics `pipeline_phases` and `value_representation`.
- **New files**: `README.md` with installation in Claude Code, Codex and GitHub Copilot; `AGENTS.md`; `.github/agents/software-foundations-expert.agent.md`; `plugin.json` 2.0.0; `tests/verify_citations.py` and `citation-checks.json` (171 positive, 19 negative); `tests/audit_tokens.py`; `tests/run_script_tests.py`.

## 4. Verifier results (recorded execution)
- `python -I tests/verify_citations.py --src <folder>`: **171 positive, 19 negative, 104 index entries, 901 citations in range, 0 failures**. The first run found 5 problems, all ours: one citation with a term split by hyphenation, one incomplete page and **3 wrong negatives**: the rule "90% of the time in 10% of the code" **exists** in TAUP (p.412) and the term `webassembly` appears in CI p.18; the negatives were rewritten and the 90/10 rule became a positive. The reference files were also corrected (INDEX and `casos-e-antipadroes.md` said the book did not contain the 90/10 rule).
- `python -I tests/audit_tokens.py --src <folder>`: 298 backticked terms checked against the pages cited on the same line, 0 failures, 0 near (13 occurrences on lines that declare absence/inference are counted separately).
- `python -I tests/run_script_tests.py --src <folder>`: ST-01..ST-29, 0 failures (lookup, evaluator_trace, checker, pipeline, index, verifiers).
- Test cases CT-01..CT-33 (`tests/casos-de-teste.md`): 33 cases run against agent+references+scripts, all PASS by the criterion described in the file. Synchronized in `03_design_and_architecture/_agents_tests/software-foundations-expert/`.

## 5. Audit coverage (what was NOT audited)
- **Chapters of the books that the package does not cover** and that, therefore, were not audited against the agent: SICP 4.4 (logic programming, p.401-445) and 5.1-5.2, 5.4.1, 5.5 (register machines and compilation, p.446-545); TAUP chs. 2-4, 6, 9-10, 12-13 (except cited excerpts), 14-20 and appendices; CI chs. 3, 8 (only the environment), 12-13 (classes), 16, 18-19, 22-23, 27-29 and appendices.
- **Figures**: no claim that depends only on a diagram (SICP frames, CI trees) was verified. The descriptions of frames come from the text.
- **Terms vs claims**: `verify_citations.py` checks terms and numbers on the pages; it does not check reasoning. Nuances (for example, the exact form of a sentence) were checked by reading the cited pages at the points where I wrote; there is no full reading of the 1,813 pages.
- **CI chapter 9** is not in the PDF and could not be audited.
- **Scripts**: the mini-reducer supports only a subset (numbers, `+ - * /`, comparisons, `if`, `define` of procedures; no `set!`, `let`, lists); `unix_philosophy_checker.py` has our own heuristic scoring.
- **Blind execution**: **there was no blind execution by an independent model**; the 33 cases were run by the auditor itself with access to the answer key. The "PASS" result measures the package's consistency with the PDFs, not the performance of an unknown model.

## 6. Pending items
- Run `tests/casos-de-teste.md` blind with an independent model and compare with the answer keys.
- If the CI PDF is replaced by one with ch. 9, extend the references and index.
- Decide whether the package should cover SICP 4.4 and ch. 5 (logic, register machines, compilation) and TAUP chs. 9-12 and 14-15, which are currently out of scope.
- Periodically review the agent format of the three platforms (README warns to check the current documentation).
