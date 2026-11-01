# Fidelity report: clean-architecture-ddd-expert (audit v1 -> v2)

Audit date: 2026-10-26. Method: text extraction of the 8 PDFs with PyMuPDF (markers `=== PAGE N ===`, N = PDF page), automatic audit of citations and terms, manual reading of the cited pages for a sample of claims, correction, and re-run of the verifiers. **There was no blind execution by an independent model**: the test cases were resolved and checked by the auditor himself (see `casos-de-teste.md`). The old report ("19 blind tests, 100% PASS") validated only page ranges and has no basis for that claim.

## 1. Sources and page convention
| Acronym | PDF | Pages | Actual content |
| :--- | :--- | :---: | :--- |
| `DDD` | DDD-Reference-Evans | 59 | booklet of definitions and patterns (printed = PDF − 7) |
| `CA11` | Clean-Architecture-UncleBob-2011 | 15 | "Clean Architecture" post (2011-11-22): text on p.1-5, sidebar on p.6-15. **It is not "The Lost Years"** |
| `CA12` | The-Clean-Architecture-UncleBob-2012 | 15 | post (2012-08-13): text on p.1-7; diagram not legible |
| `SRP` | SOLID-SRP-UncleBob | 15 | post (2014-05-08): text on p.1-5 |
| `OCP` | SOLID-OCP-UncleBob | 15 | post (2014-05-12): text on p.1-4 |
| `SREL` | SOLID-Relevance-UncleBob | 15 | "Solid Relevance" post (2020-10-18): text on p.1-5 |
| `TARPIT` | Out-of-the-Tar-Pit | 66 | full paper |
| `REACT` | Reactive-Manifesto-2.0 | 2 | full manifesto; no author names |

The v1 declared no convention, mixed content pages with sidebar pages (the "15 pages" of each post) and, in the `DDD`, cited printed and PDF pages without distinction. The v2 uses the **PDF page everywhere**, with a map in `references/INDEX.md`.

## 2. Audit results
### 2.1 Automatic (v1)
- `audit_tokens.py` against the v1: **163 explicit "(ACRONYM p.N)" citations** checked; **51 failures**: 28 citations to pages that are only blog sidebar (for example `CA11 p.6-13`, `SRP p.9-12`, `OCP p.5-8`, `SREL p.7-15`) and 23 terms in backticks absent from the cited page (for example `Supporting Subdomain` at `DDD p.33`, `Functional Core`/`Imperative Shell` at `TARPIT p.45`, `CustomerId` at `DDD p.26`, `javax.persistence.*` at `CA12 p.4`). The full output was kept in the audit notes (outside the package).
- Index `cleanarch_index.json` (v1): snippets with tab garbage and table-of-contents pages (for example, "ubiquitous_language" pointing to the cover and table of contents of the `DDD`).

### 2.2 Manual (v1): 96 claims read on the cited page
| Verdict | Count |
| :--- | :---: |
| OK | 14 |
| Wrong page | 26 |
| Unsupported claim | 43 |
| Exaggeration | 13 |

Sample covering the 8 sources, the prompt, the scripts, the index and the old report (full list in `tests/auditoria-manual-v1.md`). Relevant examples of what had **no basis**:
1. **SRP "one module, one actor"** (`SRP p.3`) and the definition of "Actor": the post uses "one reason to change"; the word "actor" does not appear in the PDF. Also without basis: `regularHours`, merge conflicts, three classes and Facade (`SRP p.6-12`, sidebar pages).
2. **"Screaming Architecture" and "The Lost Years"** as content of `CA11 p.2-13`, with an invented quotation about the house plan/library: the PDF is the 2011 "Clean Architecture" post; p.6-15 are sidebar.
3. **Out of the Tar Pit**: mammoths and tigers metaphor (`TARPIT p.2-3`), quoted phrase "complexity is the only root cause" (p.4), "mathematically demonstrate", deadlocks and race conditions (p.14), and the "Functional Core, Imperative Shell" pattern attributed to `TARPIT p.45` (it is by Gary Bernhardt, absent from the paper).
4. **Aggregate rules**: "five inviolable rules", "strictly by-ID reference" and "one aggregate per transaction" (`DDD p.24-27`) are not in the booklet; the script `audit_aggregate.py` treated them as errors and cited wrong pages (`DDD p.36-43`, which are Context Map).
5. **OCP and SREL**: financial report case with `WebPresenter`/`PdfPresenter` (`OCP p.5-8`), formal Liskov definition, Rectangle/Square, DIP in two items, "SOLID in microservices = SRP+ISP" (`SREL p.13`; the text says the opposite on p.2) and "monads = DIP/OCP".
6. **Context Map**: "supporting subdomain" (`DDD p.33`), "Evans categorically instructs: never let a Big Ball of Mud contaminate..." (the text says to draw a boundary, p.45) and "political power" in Conformist/Customer-Supplier.
7. **`tar_pit_complexity_calc.py`**: "essential/accidental" percentage with invented weights 8/4/6/15 and a 60% threshold.
8. **Reactive Manifesto**: "Supervisor pattern of the Actor model", "without human intervention" and "enabling foundation" (readings by the package author, not from the PDF).

### 2.3 Audit of the v2
- `verify_citations.py`: **119 positive checks** (required terms on the cited pages, all 8 sources) and **21 negative** (plausible claims that the corpus does not contain: mammoths, deadlock, Functional Core, "actor" in the SRP, Facade, financial report, Rectangle/Square, Gateways, "supporting subdomain", "by ID", Akka, supervisor, circuit breaker, manifesto authors, among others): **0 failures**, also over the raw PDF extraction (`extract_pdfs.py`). Mutation test: changing the page of a check or inserting a term present in a negative one produces FAIL.
- `audit_tokens.py` on the v2: **359 citations** in agent, AGENTS.md, Copilot adapter, README, references and scripts; page range and blog content (no sidebar citations); **58 terms** in backticks or italics checked on the cited page; **0 failures, 0 near (±1)**. On the first pass 13 failures appeared; after adjusting the extractor (italic false positives in Portuguese) and fixing the text (citation to a sidebar page, `Domain Events` on a neighboring page, misspelled `upstream/downstream`, external titles without a page), it reached 0.
- `run_script_tests.py`: **22 script cases, 0 failures**, plus the two verifiers.

## 3. What was fixed
- **Agent** (`agents/clean-architecture-ddd-expert.md`): it was truncated at 45 lines (it ended at the script list, with no scope/boundary, response format, page convention, epistemic honesty or anti-injection). Rewritten in full (75 lines), with a realistic acronym table ("8 short texts", not 8 books), the required final sections and real `references/` and `scripts/` paths.
- **References** (12 files, names preserved): rewritten from the pages; citations in the format `[from source] (ACRONYM p.N)` only for what was read; the rest `[extrapolation]`/`[inference]`/`[DATED]`. Removed: invented quotations, blockquotes attributed to Uncle Bob, the tar pit metaphor, formulas without a source. `clean-architecture-e-the-lost-years.md` keeps its name for compatibility and carries a notice that `CA11` is not "The Lost Years".
- **Scripts**: `audit_aggregate.py` (rules A1-A7 with origin and label; error only for what the text says), `validate_dependency_rule.py` (levels from `CA12 p.3-5`; aliases `[extrapolation]`; unknown layer is reported), `tar_pit_complexity_calc.py` (no invented metric: 2^N from `TARPIT p.8`, Tables 1 and 2, reference constraints), `ddd_lookup.py` + `cleanarch_index.json` (58 curated topics, 28 `not_covered` topics, `NOT COVERED`).
- **Structure**: README with installation on the 3 platforms and a warning to check the current documentation; `AGENTS.md` (Codex); `.github/agents/clean-architecture-ddd-expert.agent.md` (Copilot); `plugin.json` updated (v2.0.0, real commands).
- **Tests**: `casos-de-teste.md` (27 cases), `verify_citations.py`/`citation-checks.json`, `audit_tokens.py`, `run_script_tests.py`, `extract_pdfs.py`, fixtures. Synchronized with `_agents_tests/clean-architecture-ddd-expert/`.
- **Encoding**: files written in UTF-8 without BOM; no absolute user paths.

## 4. Audit coverage (what was NOT audited or only partially)
- `TARPIT`: fully read p.1-18, 21-28, 30-31, 33-37, 42-49 and 64; read only in part p.50, 52 and 53 (benefits, data abstraction) and p.63 (end); **not read**: p.19-20 (logic programming), p.29 and 32, p.38-41 (relational model details), p.51, p.54-62 (example; only the section titles were checked) and the bibliography p.65-66. The references' claims about these pages are generic and limited to what was read.
- `DDD`: fully read p.1-3 (table of contents), 6 and 8-59; of p.4 (acknowledgments) only the beginning and the mention of CQRS/Event Sourcing; p.5 not read; p.7 (pattern overview) is a figure without extractable text.
- `CA12`: the circular diagram and the boundary diagram are images and were not audited.
- Term-based checks are necessary, not sufficient: they confirm the presence of terms on the page, not the interpretation. The manual sample of 96 items is from the v1; the v2 was written by reading the pages and then verified by the automatic checks, **without independent review**.
- Verification that each illustrative example (Java in `procedimentos.md`) compiles: not applicable (labeled `[extrapolation]`).

## 5. Pending
- Blind execution of the 27 cases by an independent model.
- Full re-reading of `TARPIT` p.19-20, 38-41 and 54-63 if the package ever cites those details.
- Decide whether it is worth reusing the Clean Architecture PDF (2017 book) or "The Lost Years" in the corpus: today the concepts "actor" and "Screaming Architecture" remain `[extrapolation]`/NOT COVERED.
