# Fidelity report — python-expert (audit v0.2.0)

Date: 2026-10-26. This report **replaces** the v0.1 one (2026-10-24), which validated the package with a battery of cases simulated by subagents and by checking page citations, without systematically verifying the statements against the text of the PDFs. Here the package was audited against the text extracted from the PDFs. **There was no blind execution by an independent model in this round.**

## 1. Sources, page convention and method

| Abbreviation | Work | PDF | Pages | Printed = PDF − |
|---|---|---|---|---|
| Tut | The Python Tutorial 3.14.0rc3 | `Python-3.14-Tutorial.pdf` | 167 | 6 |
| Ref | The Python Language Reference 3.14.0rc3 | `Python-3.14-Language-Reference.pdf` | 225 | 8 |
| Notes | Python Notes for Professionals (community) | `Python-Notes-for-Professionals.pdf` | 813 | 25 |
| Lib | The Python Library Reference 3.14.0rc3 (index only in the package) | `Python-3.14-Standard-Library.pdf` | 2,488 | 26 |
| — | Tutorials 3.10, 3.11, 3.12, 3.13 (not distilled) | `Python-3.1x-Tutorial.pdf` | 153 / 153 / 161 / 167 | 6 |

- The package always cites the **PDF** page, consistently. This was **measured** on all numbered pages (footer or header): 97.0% (Tut), 98.2% (Ref), 97.0% (Notes) and 98.8% (Lib) of the pages confirm the offset; the rest are pages without a number (covers, parts). v0.1 only declared Ref ≈ −8 and Tut ≈ −6; the full map is now in `references/INDEX.md`.
- Extraction: PyMuPDF (`page.get_text()`), one text per PDF with the marker `=== PAGE N ===` (N = PDF page). The texts were kept in `scratch/audit/python-expert/src/` (outside the package). Backup of the original package: `scratch/audit/python-expert/v1_backup/`.
- **The 3.10–3.13 Tutorials were not used by the agent.** The prompt said "release notes of versions 3.10–3.13 (not provided)". They now come in only as a **presence** index of 47 terms (`tutorial_versions.py`), with the caveat that presence in the Tutorial is not a version mark.
- Huge sources: the Library Reference (2,488 p.) only exists in the package as an index of the bookmarks; it was verified **in the part the package uses** (the index) and not in the body. The Notes (813 p.) were verified by declared stratified sampling (section 3).

## 2. Automatic audit (layer a)

Citations: 1,704 occurrences of `(Tut|Ref|Notes|Lib p.N…)` in the package (outside `tests/`: 817 Notes, 440 Tut, 399 Ref, 48 Lib), referring to 4,107 pages. Results of `tests/verify_citations.py` and `tests/audit_tokens.py`:

| Check | Result |
|---|---|
| Page range of all citations (4,107 pages) and number of pages of the 4 texts | 0 out of range |
| Page convention (PDF − 6/8/25/26) | 97–98.8% of numbered pages; see section 1 |
| 90 curated **positive** checks (package fact on the cited page) | 90/90 after correction (the 1st round had 9 failures, all due to a premise or page error of **mine**: e.g. Tut p.130 cites PEP 703 and Ref p.127 cites PEP 758; and Notes p.505 has a security warning, which became a scanner finding) |
| 18 **negative** checks (plausible claims that the source does not carry in that passage) | 18/18 after correction |
| Version marks of the master table (`versoes-e-datado.md` §1: Added/Changed/Deprecated/Removed) | 100 confirmed, 0 failures (the 1st strict version flagged 9 because of wording differences; all checked by hand: the text says "Changed … deprecated"). One row had an inexact mark (`__classcell__`, see §4) |
| Stdlib index × PDF | 293/293 modules and 1,744 sections with the title on the indicated page (2 registered exceptions: XPath section and license title, page break) |
| Presence index of the 3.10–3.14 Tutorials | 47 terms, 471 pages checked, 0 failures |
| `audit_tokens.py`: backticked terms × cited page | 2,248 terms checked in 1,634 citations; 24 on a neighboring page (±1, **registered** tolerance); 422 terms absent from the cited page, **triaged** and recorded in `audit_tokens_baseline.txt` (see below) |

**On the 422 "absent".** On the first run there were 485 (442 after ignoring the fix column of the tables). The triage: (i) I read the 136 occurrences in which the term exists ≤ 10 pages from the cited one and fixed those that were page errors (4); (ii) I read the 36 on a neighboring page (fixed 10 citations; 24 page breaks remained); (iii) I read in full the list of the 309 terms that **do not exist** in the source text: they are package forms (suggestions such as `[[] for _ in range(n)]`, identifiers with their own spelling, package examples) or lines with several citations in which the term belongs to the following citation. I did not read the page of each of the 309. The baseline serves to **detect regression** (a new failure fails), it does not prove each entry is correct.

## 3. Manual sample (layer b)

**114 statements** read against the cited page(s) (see `scratch/audit/python-expert/notes/manual_sample.tsv`). Declared stratification: by file (fontes-comunitarias 19, frameworks 18, glossary 17, rules 13, cases 12, scanner 7, procedures 7, skills 10, versions 4, prompt 4, others 3), by source (statements that cite each work, some cite more than one: Notes 59+, Ref 30, Tut 27) and by type, prioritizing the agent prompt, sentences with "always/never/only", numbers, versions, comparisons between sources, tables, security and "book errors" (claims that the PDF is wrong, which are the highest risk).

| Verdict | Count |
|---|---|
| OK | 92 |
| Wrong or incomplete page | 14 |
| Overstatement | 6 |
| Unsupported (contradicts or has no basis in the text) | 2 |
| Total | 114 |

Coverage by topic: the 4 sources and all files of `references/` were touched; of the claims in the `fontes-comunitarias.md` register about the book I read 19: 18 well-founded (e.g. the book calls `\r` form-feed, uses an undefined `line` in `readlines` and shows `isinstance(x, byte)`) and 1 overstated (SEG-1, below).

**Relevant examples of what was wrong or unsupported in v0.1:**

1. **Scanner, `eval-exec` rule**: the message said the Notes describe `eval`/`exec` "without a security warning". **False**: Notes p.505 says it is not possible to use `eval`/`exec` securely with untrusted user code. Fixed; new test.
2. **Scanner, `finally-flow` rule**: it flagged any `break`/`continue`/`return` inside `finally`, including those of an inner loop and a nested function (3 false positives in a clean file). Fixed (`fixtures/clean.py` = 0 findings).
3. **Coverage of the Notes**: "668 of 813 pages distilled, 37 chapters left out" (prompt, README, INDEX) had no basis. Measured: 588 pages cited and **58** of 202 chapters with no citation at all, including language topics (bitwise operators, precedence, `heapq`, `pass`). Replaced and listed in `references/INDEX.md`.
4. **`fontes-comunitarias.md` SEG-1**: it said the Notes present `pickle` "without a security warning"; the pickle chapter carries the warning (Notes p.535) and so does the Tutorial (Tut p.66). Rewritten for the examples on p.687 and 731.
5. **INDEX**: "Nothing in the sources says whether the free-threaded build is the default": the glossary (Tut p.124, 132) and the Lib (p.876, 1018, 2049) talk about "free-threaded builds". Rewritten without denying what is there.
6. **Namespace packages**: cited as Tut p.128 in 3 places; the text is on Tut p.134. Fixed (frameworks ×2, triage skill).
7. **`regras-da-linguagem.md`**: t-strings cited via the index (Ref p.224) instead of Ref p.26; `__slots__` cited via the glossary (Ref p.183) when the rules are on Ref p.57; and a Portuguese word in quotation marks attributed to the glossary.
8. **Overstatements**: "never `range(len(x))`" (the book says "Don't use index to loop over a sequence"), "always define `__repr__`" (the book says "consider implementing at least `__repr__`"), inexact mark "Changed 3.8" for `__classcell__` (Ref p.60 only says it gives a `RuntimeError` in 3.8).

## 4. Corrections made

- **Pages**: 14 page corrections (Ref p.26/57/53/96/109/117; Tut p.70/134; Notes p.256/273/374/497–498 and two repeated pairs), in `regras-da-linguagem`, `glossario`, `frameworks`, `casos-e-antipadroes`, `versoes-e-datado` and the triage skill. 3 other citations had their range widened (Ref p.147–148, Notes p.435–436, Tut p.95).
- **Statements**: 2 unsupported, 6 overstatements rewritten; 3 items of `fontes-comunitarias.md` and of the INDEX adjusted.
- **Scripts**: `scan_python_smells.py` gained an origin and label (official, community, inference, extrapolation) per rule and per finding, corrected messages, a corrected `finally-flow` rule; `stdlib_lookup.py` says **NOT COVERED** (before: "no module matched"); new `tutorial_versions.py` + `tutorial_index.json`; 3 fixtures (`clean.py`, `injection.py`) and `sample.py` kept.
- **Structure**: agent prompt expanded (from 86 to 108 lines): page convention, real scripts with paths, [DATED] content section, anti prompt-injection security section and revised boundary; `README.md` with installation on the 3 platforms and a notice to check the current documentation (the user's absolute path was removed); `AGENTS.md` (Codex) and `.github/agents/python-expert.agent.md` (Copilot) generated from the prompt; `plugin.json` 0.2.0; `references/INDEX.md` with page map, measured coverage, label convention and gaps.
- **Encoding**: no mojibake or BOM found; 11 files of v0.1 (10 .md and `stdlib_lookup.py`) had CRLF line endings and were normalized to LF; UTF-8 without BOM everywhere.

## 5. Scripts: audit and tests

- `scan_python_smells.py`: 27 rule entries (14 for Python 3 code, 12 for Python 2 and `syntax-error`). The origin of each rule was checked against the text: 12 of the 14 Python 3 ones have a book page, 1 is [inference] (`except-pass`), 1 is [extrapolation] (`weak-hash`); the Python 2 ones are [DATED] with a Notes page. Actually run on `sample.py`, `sample_py2.py`, `clean.py` and `injection.py`. **It runs on the available interpreter (3.13), not on 3.14**: on 3.13, `except A, B:` falls into the Python 2 branch (the rule's message warns about it).
- `stdlib_lookup.py` and `tutorial_versions.py`: run with present terms, absent terms and no argument.
- `tests/run_script_tests.py`: **25/25** tests (scanner: 14 rules, negatives, false positives, JSON, origin, injection, exit codes; lookup: csv, pathlib, NOT COVERED, JSON, `--list-chapters`; tutorials: presence, absence, NOT COVERED, inference).

## 6. Test cases

`casos-de-teste.md`: **32 cases** (19 original + 13 new: conceptual, practical, edge, out of scope, false premise, injection). Run with `tests/run_cases.py`: **104 mechanical checks passed, 0 failed** (grep in the references, execution of the scripts and checking the fact on the page of the PDF text). **This verifies that the package contains and retrieves the material; it does not evaluate a model's answers.** The new cases were written after finding the defects, which favors the result on them. The v0.1 defects (scanner and SEG-1) would make cases 20, 21 and 32 fail if reintroduced.

## 7. Audit coverage: what was NOT audited

- **Body of the Library Reference (2,488 p.)**: only the index and the modules the package cites.
- **Notes**: 817 citation occurrences, 59+ statements read by hand; the rest only went through the automatic checks (backticked terms, range, 90+18 curated checks). 225 pages of the Notes are not cited by the package and were not read.
- **Long-range citations** (≥ 10 pages, ~25 occurrences such as `Notes p.621–646`) are section pointers; the audit does not check them statement by statement.
- **`audit_tokens`**: it only checks backticked terms; a sentence without backticks was only checked if it fell in the manual sample. The 309 terms "absent from the source" were read as a list, not page by page.
- **Cases 1–19**: the criteria (answer key) were **not rewritten**; their pages were checked only by the `run_cases.py` checks (and an automatic pass that found 76 terms not found out of 259, usually Portuguese text or code with its own spelling; I did not review them one by one).
- The text was checked on the **text extraction** of the PDFs, not on the visual pages: code indentation, tables and figures may differ (the package already declared extraction losses in Tut p.60, 62, 96 and 122).
- **Not tested**: installation on the 3 platforms (Claude Code, Codex, Copilot) and real use of the skills; the scanner on Python 3.14.
- **No blind execution by an independent model.**

## 8. Known pending items and risks

1. The 58 chapters of the Notes without a citation (see `references/INDEX.md`) remain undistilled; if the user asks about them, the correct answer is "the package does not cover it".
2. The Standard Library remains index-only; the API is not described.
3. The presence index of the Tutorials covers 47 terms; extending it requires curation (each term needs page verification).
4. Release candidate: the final behavior of 3.14 may differ from the text.
5. Running a **blind** battery with an independent model (answer key outside the package) is the next validation step; it was not done.
