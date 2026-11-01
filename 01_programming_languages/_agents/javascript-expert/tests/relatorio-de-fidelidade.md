# Fidelity and audit report: javascript-expert

Date: 2026-10-26. Target: `01_programming_languages/_agents/javascript-expert` (version 0.2.0 after the audit). This report **replaces** the previous one, which mostly validated page ranges and claimed "19 blind tests, 100% accuracy". Those blind runs cannot be re-verified (there are no transcripts in the package) and the "100% accuracy" did not hold up: the audit below found wrong pages, unsupported claims and exaggerations.

## 1. Sources and page convention

| Abbreviation | File | Pages | Convention |
|---|---|---|---|
| Spec | `JavaScript-ECMA-262-Spec.pdf` (ECMA-262, 17th ed., ES2026) | 876 | PDF page; printed = PDF − 24 |
| EJpt | `JavaScript-Eloquent-JS-PTBR.pdf` | **504** (the package said 505) | PDF page; the PDF prints no numbering |
| EJ1 | `JavaScript-Eloquent-JS-EN-3ed.pdf` (actually the 1st edition, 2007/2013) | 247 | PDF page; the PDF prints no numbering |

The convention (PDF page) was already in use and **is consistent**: 0 citations outside the page range among 4,903 citations. The page map, the printed-page convention and the ±1 tolerance are now in `references/INDEX.md`.

## 2. Method

1. Extraction of the text of the 3 PDFs with PyMuPDF, with `=== PAGE N ===` markers (`tests/extract_pages.py`).
2. **Automatic layer**, over **all** citations in the package (agent, references, skills, README and JSON data): (a) page range; (b) terms between backticks in the passage preceding each citation must appear on the cited page (`tests/audit_tokens.py`; ±1 page only as NEAR, recorded); (c) search for quoted passages attributed to the sources; (d) numbers; (e) check of the 2,224 titles of the `spec_toc.json` index against the indicated page; (f) 115 curated positive and 24 negative checks (`tests/verify_citations.py` + `citation-checks.json`).
3. **Manual layer**: reading of the cited pages for a sample of **101 entries** (about 150 atomic claims, since some entries group several), prioritizing the agent prompt, "always/never", numbers, comparisons between sources, tables, versions and claims of absence. The complete list was left in the audit notes (`scratch/audit/javascript-expert/notes/amostra_manual.tsv`, outside the package).
4. Correction, script tests (`tests/run_script_tests.py`), test cases (`tests/casos-de-teste.md`).

## 3. Results of the automatic layer

| Check | Before (v1) | After (v2) |
|---|---|---|
| Citations in the package (Spec / EJpt / EJ1) | 4,926 (2,906 / 1,518 / 502) | 4,903 (2,889 / 1,517 / 497; includes README, adapters and tests) |
| Pages outside the PDF | 0 | 0 |
| Backtick terms checked | 3,999 | 4,127 |
| Term only on a neighboring page (NEAR, ±1) | 57 | 56 (tolerance recorded in `references/INDEX.md`) |
| Term absent from the cited page and from the rest of the line | 191 | 223 reviewed by hand and recorded in `tests/audit-tokens-baseline.txt` (includes 32 repetitions in the `AGENTS.md` and Copilot adapters) |
| `spec_toc.json` titles on the indicated page | 2,224 of 2,224 | 2,224 of 2,224 |
| Quoted passages attributed to the sources and not literally locatable | 97 of 284 | 51 of 238 (the rest is code, a package label or a user question) |
| `verify_citations.py` | (did not exist) | 115 positive + 24 negative, 0 failures |
| `run_script_tests.py --src` | (did not exist) | 37 tests, 0 failures |

Honest reading of the "191/223": these are backtick terms that do not appear **literally** on the cited page. Reviewing the whole list by reading classified them as (i) illustrative code or a name the PDF writes differently (`%Symbol.x%`, flattened exponents, `Picture.draw` written as `draw(`), (ii) a term from another source cited on the same table row, (iii) a claim of absence ("EJpt does not carry X") or (iv) a header page with the algorithm on the next one. About 40 of them were checked page by page; the real findings are in section 4. **The 223 were not all read page by page**: the baseline records review, not proof of each item.

## 4. Manual layer: 101 entries

| Result | Entries |
|---|---|
| OK (page matches and the claim appears) | 84 |
| Wrong page | 5 |
| Claim unsupported by the cited source | 5 |
| Exaggeration (the source says less than the package) | 2 |
| Inadequate label or attribution | 4 |
| ±1 tolerance (title on the cited page, body on the next) | 1 |

Examples of what was wrong or unsupported (all corrected):

1. **Unsupported**: "p.813–842 absent from the extraction" (agent, README, INDEX, cases, glossary, versions, skill: 11 passages). The pages exist: p.813–814 close the memory model and p.815–842 are Annex A (grammar summary). The gap is one of distillation, not of extraction.
2. **Unsupported**: quoted claim "JS has no built-in module system (EJ1 p.167)". Page 167 and the following ones organize modules by convention and do not state this (2 passages).
3. **Unsupported**: "EJpt with 505 pages" (the PDF has 504; 5 passages).
4. **Unsupported**: the glossary said that "hoisting" and "bubbling" are not used in the books; "bubble" appears in EJ1 (p.208–213) and "hoisting" in the Spec (p.450, p.812). TDZ, hoisting, microtask and bubbling are now declared as practice nomenclature **[extrapolation]**.
5. **Unsupported**: `builtins-texto-colecoes.md` said the `CanBeHeldWeakly` algorithm does not appear in the sources; it is in Spec p.196 (clause 9.13).
6. **Exaggeration**: "`forEach` with `await` does not wait" cited to EJpt p.249–259 (agent, `frameworks.md`, `js-code-review` skill, message of `scan_js_smells.py`). EJpt does not cover `forEach` with `await`; it shows the `list +=` bug inside `map(async ...)` (p.258–259). Downgraded to **[inference]**, with Spec p.627.
7. **Exaggeration**: "`fetch` only rejects on network failure" (EJpt p.407, p.498). The book says the promise resolves with an error code and may reject on a network error; it does not say "only", and `response.ok` does not appear in EJpt (**[extrapolation]**).
8. **Wrong page**: `Array(len)` with `RangeError` cited to Spec p.614 (it is p.615); clause 20.5 (Error Objects) cited from p.481 (it starts on p.482); `Symbol.keyFor` on p.478 (it is p.479); modules "strict by definition" cited to Spec p.398 and EJpt p.221 and p.229 (the correct pages are Spec p.247 and p.178, EJpt p.169).
9. **Label**: `eval` attributed to EJpt p.228, which only covers the `Function` constructor (`eval` is in EJ1, p.168 and p.234); `module.exports` and the acronym IIFE treated as EJpt terms (the book uses `exports` and describes the IIFE in full); 46 translations or paraphrases presented in quotation marks as if they were literal quotes (quotation marks removed).

What was correct and preserved: the version claims (`class`, `Symbol`, arrow, ES modules, CommonJS and `var` as 2015/pre-2015; Annexes E and F; ES2017 and `caller`), the **[HOST]** boundary, the catalogued errors of the books (square root, `{,4}`, `self.content`, `String(err)`, `getMonth`), the 12 Promise rows, the table of well-known symbols, the Node and DOM sections of EJpt and the `spec_toc.json` index.

## 5. What was corrected (counts)

- Unsupported claims corrected: 5 entries, in 20 passages. Exaggerations: 2 entries, in 6 passages. Wrong pages: 5 entries, in 8 passages. Labels and attributions: 4 entries, in about 53 passages (46 of them quotation marks).
- Scripts: the 10-frame threshold of `parse_js_stack.py` is now labeled **[extrapolation]** (it is not from the book) and its note uses Spec p.482–487; messages of `scan_js_smells.py` for async `forEach` and `eval` with origin and label; `js_version_data.json` (module pages, `module.exports` note, 504 p.).
- Structure: page convention, map by topic, distilled coverage, ±1 tolerance and practice nomenclature in `references/INDEX.md`; agent prompt with the real list of scripts, the page convention and the nomenclature rule; README with installation on the 3 platforms; `AGENTS.md` and the Copilot agent generated from the prompt.

## 6. Files created or changed

Created: `AGENTS.md`, `.github/agents/javascript-expert.agent.md`, `scripts/js_topic_lookup.py`, `scripts/js_topic_index.json`, `tests/verify_citations.py`, `tests/citation-checks.json`, `tests/audit_tokens.py`, `tests/audit-tokens-baseline.txt`, `tests/extract_pages.py`, `tests/run_script_tests.py`, `tests/fixtures/` (3 files). Rewritten: `README.md`, `tests/casos-de-teste.md` (33 cases), this report, `.claude-plugin/plugin.json` (0.2.0). Changed: `agents/javascript-expert.md`, the 9 files in `references/`, the 4 `SKILL.md`, `scan_js_smells.py`, `parse_js_stack.py`, `js_version_data.json`. The original package is in `scratch/audit/javascript-expert/v1_backup/` (outside the package). The old files had no BOM or mojibake; the new and changed ones are UTF-8 without BOM and without user absolute paths.

## 7. Verifiers and tests (how to re-run)

```bash
python -I tests/extract_pages.py <PDF folder> <output>             # requires PyMuPDF
python -I tests/verify_citations.py --src <output>                   # 115 positive, 24 negative
python -I tests/audit_tokens.py --src <output>                       # all citations; exit 0 = no new failure
python -I tests/run_script_tests.py --src <output>                   # 37 tests (scripts + verifiers + self-test)
python -I scripts/js_topic_lookup.py --check                         # index up to date with references/
```

The 4 existing scripts were actually run (fixtures, output checked, injection in a comment and in a stack trace treated as data, nonexistent path, empty input). Each rule of `scan_js_smells.py` cites a valid page (20 pages checked against the size of the PDFs); the rules that do not come from the book are labeled. `spec_lookup.py` and `spec_toc.json` were validated title by title. `run_script_tests.py` without `--src` runs 33 of the 37 tests (the others need the PDF text).

## 8. Audit coverage (what was NOT audited)

- **Spec (876 pages, 2,889 citations)**: all went through the automatic range and backtick-term test, but only the manual sample read the pages. The sample covered clauses 2–4, 6–7, 9, 12–17, 19–25 (20 only in Error and Symbol), 27 and Annexes B, C, D, E and F. **Not or very little sampled**: clauses 5, 8, 10 (only occasionally), 18, 26 (WeakRef and FinalizationRegistry), 28 (Reflect and Proxy) and 29 (memory model); the full TypedArray, DataView and Atomics table; the detailed RegExp syntax; the details of B.1.2. The references cite 792 of the 876 pages (the uncited ones are in `references/INDEX.md`); Annex A (p.815–842) was not distilled.
- **EJpt (504 pages, 1,517 citations)**: manual sample in the introduction and in 14 of the 21 chapters (1, 2, 3, 4, 6, 8, 9, 10, 11, 13, 14, 18, 20 and 21); chapters 5, 7, 12, 15, 16, 17 and 19 (includes all the projects and exercises) only by the automatic layer.
- **EJ1 (247 pages, 497 citations)**: sample in chapters 1, 2, 3, 8, 9, 10, 11, 13 and 14; chapters 4, 5, 6, 7 and 12 only by the automatic layer.
- The check of **numbers** was approximate: PyMuPDF flattens exponents ("253 - 1" for 2^53 − 1) and symbols (∞, 𝔽). Of the 104 numbers "not found" in the first pass, those I read were formatting noise or code examples; no exhaustive check was done.
- Not audited semantically: each glossary definition (only the entries in the sample), the exercise procedures, and the false positive and false negative rate of `scan_js_smells.py` (it is a lexical regex, not an AST).
- `js_topic_index.json` is derived from the references: it inherits any error they still have, and the pages of the `[section]` entries are the union of the section's citations, not just of the topic.

## 9. Blind execution by an independent model

**There was none.** The 33 cases were run by whoever audits (cases 20 to 33 with real commands; cases 1 to 19 by documentary verification of the answer key against the PDF and against the references). No independent model answered questions blind using only the package. The behavior rules of the prompt (warn about injection, label, decline out-of-scope) were checked by reading and by the scripts, not observed in model answers.

## 10. Pending items

- Run the 33 cases blind with an independent model, with access only to the package folder, and record the answers.
- Widen the manual sample in Spec clauses 26, 28 and 29, in the EJpt project chapters and in EJ1 chapters 4 to 7.
- Decide whether Annex A (grammar summary, p.815–842) and EJ1 pages p.83–92, p.135–140 and p.154–158 should be distilled.
- Review page by page the 223 items of the `audit_tokens.py` baseline (today: list review and check of about 40).
- Run `js_topic_lookup.py --rebuild` and regenerate the baseline whenever the references change (the `--check` test flags the outdated index).
