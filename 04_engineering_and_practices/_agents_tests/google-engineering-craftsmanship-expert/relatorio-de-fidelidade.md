# Fidelity Report: `google-engineering-craftsmanship-expert` (v2, audit of 2026-10-26)

This report replaces the previous one, which claimed "19/19 PASS, 100% page fidelity, 0 hallucinations" while validating only the page range. The audit below compared the v1 package with the text of the PDFs and found dozens of unsupported claims. **There was no blind run by an independent model**: the conceptual cases were verified by the auditor's trace; the scripts were actually run.

## 1. Source inventory and page convention
| Abbrev. | PDF | What it actually is | Pages | Convention |
| :-- | :-- | :-- | :-- | :-- |
| SWE-G | `Software-Engineering-at-Google-completo.pdf` | open book, 25 chapters + index | 408 | PDF pages; Ch. 1 on p.13; no printed numbering |
| SWE-PREV | `Software-Engineering-at-Google.pdf` | Fergus Henderson's article, 2017 (NOT a preview of the book) | 20 | printed = PDF |
| CC2 | `Code-Complete-SampleChapter-Pearson.pdf` | SAMPLE: full table of contents, full Ch. 5 (PDF p.38-88), part of the index | 120 | printed = PDF + 35 |
| 97TH | `97-Things-Every-Programmer-Should-Know.pdf` | Extended edition (Leanpub 2014): 68 ADDITIONAL essays | 151 | printed = PDF - 8 |

**v1 convention**: mixed and undeclared. SWE-G used PDF pages (chapter starts match), while CC2 and 97TH used printed pages. v2 standardized on PDF pages and declared the map in `references/INDEX.md`.
**Source identification errors in v1**: "97 Things (O'Reilly, Kevlin Henney, 151 p.)" is actually the Extended edition with 68 additional essays; "SWE-PREV = Winters et al. overview" is Henderson's article; "Code Complete (Selected Chapters)" is a sample with only Ch. 5; the authors of several SWE-G chapters were wrong (for example, Ch. 16 is not by Rachel Potvin).
Texts extracted with PyMuPDF (`python -I`) to `scratch/audit/google-eng/src/*.txt` with `=== PAGE N ===` markers; v1 backup in `scratch/audit/google-eng/v1_backup/`.

## 2. Automatic layer
**v1 (applying the same term auditor to the backup)**: 198 citations in the package; 77 checkable items (terms in backticks, numbers, names and quotes); **41 failures and 6 "near"** (SWE-G: 35 failures and 6 near in 70 items; CC2: 3 failures in 3 items; 97TH: 3 failures in 4 items). Part of the CC2 and 97TH failures stems from the use of printed pages (mixed convention); the rest is unsupported content.
**v2**:
- `tests/verify_citations.py`: **108 positive and 23 negative checks, 0 failures** (positives cover SWE-G, CC2, 97TH and SWE-PREV; negatives cover 70/20/10, Goodhart, CitC, `nit:`, HRT, 1% false positives, Meszaros, cyclomatic, quarantine, "30 seconds", Live at Head in Ch. 16, "hermetic" in Ch. 18, 95%, 10-15 minutes, 5xx/p99, 1% canary, Miller, cohesion types, Boy Scout in 97TH).
- `tests/audit_tokens.py`: **413 citations extracted from the package files; 223 items checked (terms in backticks, numbers, proper names and English quotes in double quotes); 0 failures, 0 near**. Every failure found during review was fixed (for example, a quoted phrase that was a paraphrase and page numbers in the wrong format).
- `tests/run_script_tests.py`: 16 script cases + the two verifiers, 0 failures (the English translation of the package added two Portuguese-query cases, CT-09b and CT-26b).
- The automatic layer checks the occurrence of terms and numbers on the cited pages; it does **not** prove that the whole claim is correct (for that, see the manual layer).

## 3. Manual layer: sample of 71 v1 claims read against the page
Verdict: **OK 14; wrong page 9; unsupported 33; exaggeration 15**. (Claims attributed to wrong authors or sources count as unsupported.)

| # | v1 citation | v1 claim | Verdict | Evidence |
| :-- | :-- | :-- | :-- | :-- |
| 1 | SWE-G p.13 | definition 'software engineering is programming integrated over time' | OK | internal Google saying, p.13 |
| 2 | SWE-G p.14-16 | 'three pillars' time, scale, trade-offs | exaggeration | Ch. 1 presents three differences/themes (p.13-14), without 'pillars' |
| 3 | SWE-G p.16 | statement of Hyrum's Law | wrong page | statement on p.15; p.16 has the hash example |
| 4 | SWE-G p.105 | Google randomizes the hash seed in tests | unsupported | p.17 says some languages randomize; p.105 is Ch. 8 (style) |
| 5 | SWE-G p.19, p.316 | the team that changes the API migrates the clients (Churn Rule/LSC) | OK | p.19 Churn Rule; p.317 centralization |
| 6 | SWE-G p.150-154 | 70/20/10 pyramid | unsupported | book: 80/15/5 (p.156) and 80/20 (p.165) |
| 7 | SWE-G p.151 | small tests with no network, disk or system clock | exaggeration | p.154: no sleep, I/O or blocking calls; the clock is not mentioned |
| 8 | SWE-G p.153 | large tests = 10% | unsupported | p.156: 5% end-to-end |
| 9 | SWE-G p.158 | flaky tests go to quarantine immediately | unsupported | policy not in the book |
| 10 | SWE-G p.168 | test readable in under 30 seconds | unsupported | number not in the book |
| 11 | SWE-G p.171 | canonical AAA structure | exaggeration | p.173: given/when/then; AAA only in a note (p.183) |
| 12 | SWE-G p.185 | quote 'Prefer real ones or Fakes. Avoid mocking frameworks whenever possible' | exaggeration | the quoted sentence does not exist; see p.185 and p.189-190 |
| 13 | SWE-G p.184-188 | Meszaros taxonomy (Fake, Stub, Mock, Spy, Dummy) | unsupported | the chapter uses faking, stubbing and interaction testing (p.188-189) |
| 14 | SWE-G p.195 | mocks exclusively for rare I/O failures | exaggeration | p.197: stubbing for unreachable values/errors; interaction testing in specific cases |
| 15 | SWE-G p.189 | a Fake belongs to the API maintainer | wrong page | correct idea; correct page is p.193 |
| 16 | SWE-G p.335 | TAP selects tests via the DAG | wrong page | p.341 (global dependency graph of Forge and Blaze) |
| 17 | SWE-G p.332 | hundreds of millions of tests | unsupported | number not in the book; p.339: 4 billion cases per day |
| 18 | SWE-G p.332-335 | most tests run in 10 to 15 minutes | unsupported | number not in the book; p.340: average wait ~11 min to submit |
| 19 | SWE-G p.350 | 1% canary with 5xx, p99 and CPU | unsupported | numbers and metrics not in the book |
| 20 | SWE-G p.351 | automatic rollback in seconds | exaggeration | p.341: automatic rollback with high confidence; 'seconds' is not in the book |
| 21 | SWE-G p.290 | above 10% false positives engineers disable the tool | exaggeration | p.292: 10% is the criterion for new Tricorder checks |
| 22 | SWE-G p.290 | check only authorized with FP below 1% | unsupported | 1% target not in the book |
| 23 | SWE-G p.292-294 | one-click quick fixes | OK | p.293: applicable fix suggestions in Critique |
| 24 | SWE-G p.121-124 | three mandatory independent approvals | exaggeration | p.123: they can fall on one person and be implicit |
| 25 | SWE-G p.126-128 | ideal CL <200 lines and ceiling of 400 | unsupported | p.129: about 200; 400 not in the book |
| 26 | SWE-G p.286 | nit: prefix does not block | unsupported | nit: not in the book |
| 27 | SWE-G p.284 | if a test breaks the reviewer is not even triggered | exaggeration | p.284: presubmit failure blocks sending/commit |
| 28 | SWE-G p.280 | Critique with minimalist design | wrong page | principles on p.279; p.280 covers Code Central |
| 29 | SWE-G p.30-34 | HRT as an acronym | unsupported | acronym does not appear; pillars on p.33 |
| 30 | SWE-G p.35-36 | dev who types an accidental command and blaming the system | unsupported | p.36 does not have this example |
| 31 | 97TH p.138 | truck factor and lone genius | exaggeration | the essay covers pair rotation (PDF p.146) |
| 32 | SWE-G p.65-72 | servant leadership | OK | p.67-68 |
| 33 | SWE-G p.68-69 | micromanagement and low performers as antipatterns | OK | p.70-72 |
| 34 | SWE-G p.83-88 | three 'commandments' of leadership at scale | OK | p.83-89 ('three Always') |
| 35 | SWE-G p.86 | Always Be Leaving = being away for a month of vacation | exaggeration | p.86-88 talk about being a SPOF and about an autonomous organization |
| 36 | SWE-G p.94-104 | GSM | OK | p.97-103 |
| 37 | SWE-G p.96 | Goodhart's Law | unsupported | not in the book |
| 38 | SWE-G p.95 | QUANTS | wrong page | p.98-99 |
| 39 | SWE-G p.107-111 | six principles of style rules | unsupported | p.106: five principles |
| 40 | SWE-G p.112-115 | guidelines cover 95% of cases | unsupported | not in the book |
| 41 | SWE-G p.111 | clang-format, gofmt, google-java-format via presubmit | wrong page | p.118 (google-java-format is not mentioned) |
| 42 | SWE-G p.224 | advisory deprecation usually fails | wrong page | p.225-226 |
| 43 | SWE-G p.226 | quote 'the team that introduces the new library funds the migration' | exaggeration | the quoted sentence does not exist; see p.19, p.317 |
| 44 | SWE-G p.318-326 | canonical LSC steps (proposal, automation, rosie, review, merge) | exaggeration | book: authorization, creation, shards, cleanup (p.324-325) |
| 45 | SWE-G p.322 | Rosie partitions by directory and maintainer | OK | p.323 and p.326 |
| 46 | SWE-G p.231-246 | Ch. 16 by Rachel Potvin | unsupported | author: Titus Winters |
| 47 | SWE-G p.235 | 5,000 consumers updated in one operation | unsupported | not in the book |
| 48 | SWE-G p.233 | CitC (Clients in the Cloud) | unsupported | does not appear in the PDF |
| 49 | SWE-G p.234, p.297 | Live at Head eliminates diamond dependencies | wrong page | p.303 (dependency model) |
| 50 | SWE-G p.237 | rejects long-lived feature branches | OK | p.237-238 |
| 51 | SWE-G p.260-278 | Blaze/Bazel based on DAG and artifacts | OK | p.266-268 |
| 52 | SWE-G p.266 | strict network/env/clock bans (hermeticity) | exaggeration | Ch. 18 does not use 'hermetic'; sandbox p.269; hermetic in SWE-PREV p.5 |
| 53 | SWE-G p.268 | cryptographic hash determines the artifact with 100% certainty | exaggeration | p.271 and p.269 (nothing prevents non-deterministic actions) |
| 54 | SWE-G p.270-274 | millions of processing hours saved per day | unsupported | not in the book |
| 55 | SWE-G p.202-221 | Ch. 14 = test doubles | unsupported | Ch. 14 = Larger Testing; doubles = Ch. 13 (p.184) |
| 56 | CC2 p.77 | 'Managing complexity is software's primary technical imperative' (literal) | wrong page | PDF p.43 (printed 78); the sentence is not literal |
| 57 | CC2 p.77 | Miller's 7 +- 2 rule | unsupported | Miller does not appear in the sample |
| 58 | CC2 p.80-82 | desirable design characteristics | OK | printed 80-81 = PDF 45-46 (mixed convention) |
| 59 | CC2 p.92-96 | Parnas information hiding | OK | printed 92-97 = PDF 57-62 |
| 60 | CC2 p.93 | secrets: data structure, device, business rule | OK | printed 93-98 (examples in PDF 58-63) |
| 61 | CC2 p.77-81 | functional/sequential/temporal/logical/coincidental cohesion | unsupported | taxonomy in Ch. 7, outside the sample |
| 62 | 97TH p.82 | Boy Scout Rule by Robert C. Martin | unsupported | the essay is 'Leave It in a Better State' by Patrick Kua (PDF p.90) |
| 63 | 97TH p.60 | Implicit Dependencies, by Steve Berczuk | unsupported | author: Klaus Marquardt (PDF p.68) |
| 64 | 97TH p.100 | Restrict Mutability by Henney and Udi Dahan | unsupported | author: Kevlin Henney (PDF p.108) |
| 65 | 97TH p.142 | Write Code for Humans, by Dave Thomas and Andy Hunt | unsupported | author: Mario Fusco (PDF p.150) |
| 66 | 97TH source | 97 Things (O'Reilly), 151 pages | unsupported | it is the Extended edition with 68 additional essays |
| 67 | SWE-PREV source | Winters et al., overview/preview | unsupported | it is Henderson's article (2017) |
| 68 | scripts/routine_quality | scoring by cohesion, <=4 parameters, <=50 lines | unsupported | no origin in CC2; the 97TH p.150 numbers are different |
| 69 | scripts/review_audit | points per rule, thresholds of 400 and 800 lines | unsupported | no origin in the book |
| 70 | scripts/hyrum_evaluator | weights 15-35 and multipliers by number of clients | unsupported | no origin in the book |
| 71 | SWE-G p.121 | LGTM as a seal of technical correctness | OK | p.121 and p.126 |

### Relevant examples of what was unsupported
1. **70/20/10 pyramid** (v1 in 3 files, glossary and test cases): the book says 80/15/5 (SWE-G p.156) and 80/20 (p.165). The "rigid 70/20/10 ratio" does not exist.
2. **Tricorder "false-positive rate < 1%"** and "above 10% engineers disable it": the book has a criterion of less than 10% for new checks and an average rate below 5% (SWE-G p.292).
3. **Numeric limits for CLs, lines and parameters**: "ceiling of 400 lines", "<= 4 parameters", "<= 50 lines" and cohesion scoring do not exist in the sources; the only CL number is "about 200 lines" (SWE-G p.129) and the book says there is no automatic rejection (p.117); routine numbers (about 15 lines, about 3 parameters) come from a 97TH essay (p.150), not from Code Complete.
4. **Invented literal quotes**: "Prefer real implementations or Fakes... avoid mocking frameworks whenever possible" (v1, p.185) and "the team that introduces the new library... funds the migration" (v1, p.226).
5. **Canary "1% of servers, 5xx, p99, rollback in seconds"** (v1, p.350-351): none of this is in the book; Henderson's article only describes canary servers (SWE-PREV p.10).
6. **Authors of the 97TH essays**: Boy Scout Rule (Robert C. Martin, p.82), Implicit Dependencies (Steve Berczuk, p.60), Restrict Mutability (Henney and Udi Dahan, p.100), Write Code for Humans (Thomas and Hunt, p.142). In the PDF the essays are by Patrick Kua, Klaus Marquardt, Kevlin Henney and Mario Fusco, and the "Boy Scout Rule" essay is not in it.
7. **Ch. 14 as "test doubles"** (SWE-G p.202-221): Ch. 14 is Larger Testing; doubles are in Ch. 13 (p.184).
8. **Scripts**: `routine_quality.py` (points for cohesion, size, parameters), `review_audit.py` (points, thresholds of 400 and 800 lines) and `hyrum_evaluator.py` (weights and multipliers by number of clients) encoded rules with no origin.
9. **Agent prompt (41 lines)**: it was truncated; it ended at the list of scripts, without a section on when to consult `references/`, response format, epistemic honesty, boundary and [DATED] content.

## 4. What was fixed
- **References**: the 15 files in `references/` were rewritten from the pages read (each fact with `[from source] (ABBREV p.N)` of the PDF) with a "Nota de fidelidade" ("fidelity note") section where v1 was wrong; `visao-geral-henderson-2017-software-engineering-at-google.md` was added (the 16th file). Files keep their original names (links preserved).
- **Sources**: table with convention and chapter map in `references/INDEX.md`; the HRT acronym is marked as not present in the PDF.
- **Agent**: complete 98-line prompt (scope and boundary, convention, labels, security, method, decision rules with pages, trigger table, format, epistemic honesty).
- **Scripts**: the four scripts now produce checklists with origin per rule and no scoring; `eng_lookup.py` gained a list of "what the book does NOT contain" and prints NOT COVERED; `eng_index.json` was regenerated (50 entries, 11 items without coverage).
- **Structure**: README with installation for Claude Code, Codex and GitHub Copilot; `AGENTS.md`; `.github/agents/google-engineering-craftsmanship-expert.agent.md`; `plugin.json` updated.
- **Tests**: 26 cases in `casos-de-teste.md`, `run_script_tests.py`, `verify_citations.py`, `citation-checks.json` and `audit_tokens.py`; cases and report synchronized with `_agents_tests/google-engineering-craftsmanship-expert/`.

## 5. Audit coverage (what was NOT audited)
- SWE-G read in full: Ch. 1, 2, 7, 8, 9, 12, 13, 15, 16, 19, 20, 22 and 24. Read partially: Ch. 3 (p.40-43, p.52-55), Ch. 5 (p.65-72; p.73-78 only by titles and TL;DR), Ch. 6 (p.83-91), Ch. 11 (p.149-158 and TL;DR of p.163), Ch. 18 (p.260-277), Ch. 21 (p.297, p.303, p.310-314), Ch. 23 (p.330-342). Only titles or overview: Ch. 14 and 17. **Not read**: Ch. 4, 10 (Documentation), 25 and the rest of Ch. 3, 17, 21 and 23.
- SWE-PREV: p.1-18 read.
- CC2: Ch. 5 read p.38-75 (heuristics); p.76-88 only by titles; table of contents and index not audited in detail.
- 97TH: 13 of the 68 essays read.
- "Unsupported" references in v1 were identified by a sample of 71 claims, not by an exhaustive examination of all 198 citations; the term auditor covers 223 items of v2 and 77 of v1.
- There was no blind run by an independent model; the conceptual cases were traced by the auditor.

## 6. Pending
- Audit the unread chapters (4, 10, 14 in depth, 17, 21, 23, 25) and the remaining 55 97TH essays.
- Obtain the text of the full Code Complete (Ch. 6, 7, 8, 24) to cover the cohesion taxonomy and routines, now outside the sample.
- Run the conceptual cases blind with an independent model.
