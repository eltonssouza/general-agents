# Fidelity report — java-expert (v2, after audit)

Replaces the v1 report, which mainly validated page ranges and rounds of subagents from the same model family. This version records what the audit read on the PDF pages, what it found, what it fixed and what it did **not** audit.

## 1. Sources and page convention

| Abbreviation | Work | PDF | Package convention | Consistent? |
|---|---|---|---|---|
| Think | *Think Java* 6.1.3 | 291 p. | PDF page; printed = PDF − 18 | yes: 218 pages with a chapter header checked, difference 18 in all |
| Adv | *Advanced Java* (Java Code Geeks) | 124 p. | PDF page; footer "N / 113" = PDF − 11 | yes: 113 footers checked, difference 11 in all |
| JVM | *JVM Troubleshooting Handbook* | 127 p. | PDF page; footer "N of 127" = PDF | yes: 93 footers checked, difference 0 |
| RN | OpenJDK 11, 17, 21, 22, 26 release notes | 3 p. each | `(RN JDK N)`, no page | yes |

v1 already used the PDF page, but only stated the Think difference; the exact map for the three books was added to `references/INDEX.md` ("Mapa de páginas", i.e. the page map), to the agent prompt (rule 6), to the README and to the adapters.

## 2. Automatic audit

| Check | Result |
|---|---|
| `(Think/Adv/JVM p.N…)` citations with page range checked (all .md, .py, .json files of the package) | 1,637 (includes the test files and this report); 0 outside the PDF (in v1: 1,580, also 0) |
| Backticked tokens against the cited page (`tests/audit_tokens.py`), v1 | 1,139 terms: 50 FAIL and 17 NEAR |
| Same, v2 | 1,147 terms: 0 failures, 0 near; 55 hand-reviewed terms are in `tests/audit-allowlist.json` with the reason |
| `tests/verify_citations.py` + `citation-checks.json` | 136 positives, 29 negatives, 123 topic-index anchors: 0 failures |
| Mutation test of the verifier | changing a passage of the source text (inserting "Spring" in Adv; altering the JRockit sentence) makes exactly the expected items fail (N16 and P091) |
| JEP table (68 rows) against the 5 release notes | identical: number, title, mark; GA dates, JSR, schedule and LTS checked; `jdk_features.json` identical to the extracted list |

Preliminary scan (heuristic of numbers and terms of any kind, before the verifier existed): 1,580 citations, 969 with verifiable terms, 245 with some missing term; triage of the 245 resulted in the findings of section 4 and in false positives (translation, package "§" section, numbers without units).

## 3. Manual audit (sample)

I read the 7 files in `references/`, the 4 `SKILL.md`, the agent prompt, the 4 scripts and the test cases, and checked on the cited page **673 pairs (claim, page)**, with 1,187 terms, chosen for: numbers and units (GB, %, 256 MB, 98%/2%, 30K classes), names (classes, flags, APIs), tables, comparisons between sources, versions, sentences with always/never/mandatory and the prompt's claims (Think version, Adv era, handbook, LTS in the release notes). Coverage per file (full reading, sample checking): `casos-e-antipadroes.md` (Parts 1 to 4), `frameworks.md` (all 19 sections), `glossario.md` (all sections), `procedimentos.md` (all 16 sections), `jvm-troubleshooting.md` (sections 2 to 6), `versoes-e-datado.md` (tables and §6; the JEP table 100% by script), the 4 SKILL.md (symptom and cause tables).

Result: of the 673 pairs, **663 were OK and 10 had a problem**; reading the scripts and data found 4 more; the automatic checks pointed to 11 problems outside the sample, all confirmed by reading the page. Total: **25 distinct problems**, classified as follows:

| Class | No. of distinct problems | Examples |
|---|---|---|
| Wrong or imprecise page | 13 | `import java.util.Scanner;` cited at Think p.54, is on p.53; labels `PSOldGen`/`PSPermGen` cited at JVM p.36 and p.45, are on p.37, 43 and 46; JSR-222 and JSR-353 cited at Adv p.93–95, are on Adv p.89; Javadoc checklist cited at Adv p.64, the text is on p.62–63; `equals(Card that)` (Think p.212) was not cited |
| Claim without support | 4 | `WorkerThread1`/`WorkerThread2` as classes of the deadlock experiment (JVM p.80–81): the code on p.81 uses `Task.executeTask1/2`; the name `WorkerThread2` only exists in a stack frame on p.84; the package called "internal `sun.*` and `com.sun.tools.javac` classes" what Adv only shows as `JCCompilationUnit`/`TreeTranslator` (p.117): the package name `com.sun.tools.javac` appears on no page; "guard clause" (Think p.90–91) is the package's name, not the book's; "empty array has `length` 0" cited as Think p.142 (the page only says zero elements is allowed) |
| Overstatement | 4 | "never `==` with `double`" (Think p.280 says "probably never"), in 3 files; "never with magic number" (Think p.146 only replaces the 3 with `a.length`); JRockit "hundreds of MB" larger (JVM p.8: "a couple of hundred MB"); `nextInt` as an example of `InputMismatchException` (the book's example, p.91, uses `nextDouble`) |
| Scripts and data without origin | 4 | threshold of 20 repetitions and the reading "last Caused by = root cause" in `parse_stacktrace.py`; threshold of 3 threads in `summarize_thread_dump.py`; `lts_stated: true` for JDK 11 in `jdk_features.json`, although the JDK 11 page does not mention LTS |

I found no invented page citation or wrong JEP number: the v1 package already came hedged ([inference]/[extrapolation] labels, the books' own errors listed). The problems above are, for the most part, about page precision and degree of certainty.

Points checked that **were right** and deserve a record: claims of absence (no `var`, records, lambdas, streams, modules, `instanceof`, hashCode in Think; no G1, CMS, jcmd, JFR in the handbook; no PermGen/Metaspace and no LTS in the 11, 22 and 26 RN), handbook numbers (2 GB/32-bit, 3–4 GB/64-bit, 50% in the 64-bit example, 256 MB, 98%/2%, 30K classes, 2000/1920 file descriptors, 672 s versus 600 s), the Think's own errors recorded in Part 4 (`second` as `double` and `int` accessors, `StackOverflowException`, `int[] array = new Point[5]`, `shuffle` against the pseudocode, negative `score()`, `intersection`), JEP table and dates.

## 4. What was fixed

- **Text**: 13 pages adjusted, 4 claims rewritten or downgraded to [inference], 4 overstatements brought to the source's degree; files `casos-e-antipadroes.md`, `frameworks.md`, `glossario.md`, `jvm-troubleshooting.md`, `procedimentos.md`, `versoes-e-datado.md` and `skills/java-exception-triage/SKILL.md`.
- **Scripts and data**: thresholds and heuristics of the scripts labeled [extrapolation] in the output and in the docstring; `jdk_features.json` with `lts_stated` false for JDK 11 and a new field `lts_called_by_later_page`; CRLF normalized to LF.
- **Structure**: prompt with a page-convention rule and a section of real scripts; `references/INDEX.md` with a page map; README with installation on the 3 platforms and a warning to check current documentation (the old one had an absolute user path); new `AGENTS.md` (Codex) and `.github/agents/java-expert.agent.md` (Copilot); `plugin.json` 0.2.0.
- **New scripts**: `scripts/java_lookup.py` + `java_index.json` (47 topics, 14 declared "NOT COVERED" topics; each topic has term and page anchors checked by `verify_citations.py`).
- **New tests**: `verify_citations.py`, `citation-checks.json`, `audit_tokens.py`, `audit-allowlist.json`, `run_script_tests.py` (48 tests of the 5 scripts, including input with an embedded instruction and avoided false positives).
- Backup of the original package in `scratch/audit/java-expert/v1_backup/`.

## 5. Test cases

`tests/casos-de-teste.md` has 26 cases (conceptual 1, 2, 24; practical 3 to 10, 20, 21; version 11, 12, 13, 15; dated 14; edge 22, 23, 25; out of scope 16, 17; false premise 18; injection 19, 26). Cases 20 to 23 were **actually executed** (commands run and output checked against the criteria); the others were walked through by the auditor against the prompt, the references and the scripts, checking that each criterion has support on the cited page (by sample, section 3). **There was no blind execution by an independent model**: what v1 called independent rounds were subagents from the same model family and the results (9 PASS, 10 PARTIAL, 0 FAIL in 19 cases) were not repeated here. Nothing in this report measures the quality of a model's answers; it measures the fidelity of the supporting material.

## 6. What was NOT audited (coverage)

- The PDF pages the package does not cite: the package covers the books selectively and this audit did not verify **omissions** (what the books say and the package left out), nor order or emphasis.
- Each individual claim: of the ~1,600 citations, 673 pairs were read on the page and the rest only went through the automatic checks (page range and backticked terms). Terms outside backticks and verbs (for example "the book recommends") were only checked in the manual sample.
- Figures, screenshots and tables that text extraction did not bring (JVM p.29, 65, 67, 68; outputs on p.38–39, 57–58; Adv exception tables); the extracted text also loses backslashes and accents in some passages (`\u0000` appears as `u0000`).
- Test cases 1 to 19: the citations pass through page range and terms; the prose criteria were reread by sample, not all.
- In the files in `references/` the checking is by sample (the proportion varies: it was lower in the case studies of `jvm-troubleshooting.md` §3 and §5 and in the long tables of `procedimentos.md` §11 to §15).
- The 5 release notes were read in full (they are 1 page of content each); the rest of the site pages (side menus, such as "Loom" and "JDK 9" in the menus) was not treated as content.
- Real behavior of current Java/JVM: nothing was verified outside the sources; `[extrapolation]` remains without verified support.
- Scripts: run with fixtures and synthetic inputs; not tested with production dumps/traces or with modern Java code (records, sealed), which the regex linter does not understand.

## 7. Pending items

- Blind execution by an independent model (including from another family) of the 26 cases, with evaluation by reading the pages.
- Omission audit: compare each book's table of contents with what the package covers and list chapters without coverage.
- Re-extract the JVM figures (p.29, 65, 67, 68) and the outputs on p.38–39 with OCR, if the content is needed.
