# Fidelity report: software-testing-qa-expert (v1 -> v2 audit)

The previous report (v1) said "19 of 19 PASS" in "blind tests" and only validated page ranges. This audit replaces it. **There was no blind execution by an independent model**: the 24 cases were executed by the audit author, who also wrote the package.

## 1. Sources and page convention
| Acronym | What the PDF is (verified in the text) | Pages |
|---|---|---|
| SWE-G | *Software Engineering at Google* (`-completo` PDF, running text without printed numbering); ch. 11-14 = PDF p.149-221 | 408 (76 used) |
| JUNIT | JUnit Tutorial (Java Code Geeks, 2014), **JUnit 4**, 8-page excerpt of the 26-page tutorial | 8 |
| MOCK | SmartBear marketing e-book (stub/mock/virtual service) | 12 |
| TDM | DZone Refcard by Niall Crawford (2021), patterns and anti-patterns | 9 |
| JMETER | JMeter Tutorial (2015), **JMeter 2.11**; printed "N / 46" = PDF − 7 | 53 |
The PDF `Software-Engineering-at-Google.pdf` (20 pp., an article by F. Henderson, 2017) is not a source of this agent. **Standardized convention: PDF page**, with maps in `references/INDEX.md`. In v1 two incompatible conventions coexisted: references with PDF pages (JMETER p.50, TDM p.6) and the agent/glossary/tests with pages that exist in no PDF (SWE-G p.213-255, JMETER p.46-47 etc.).

## 2. Method
1. **Extraction** with PyMuPDF (`python -I`) of all 6 PDFs (including the 20-page article) with `=== PAGE N ===` markers; backup of the original package in `scratch/audit/software-testing-qa-expert/v1_backup/`.
2. **Full reading** of the pages of the 4 small sources (JUNIT 1-8, MOCK 1-12, TDM 1-9, JMETER 1-53) and of SWE-G p.149-221 (ch. 11-14).
3. **Automatic, layer a** (`tests/`): `verify_citations.py` + `citation-checks.json` (145 positive, 21 negative); `audit_tokens.py` (292 citations on `[do livro]` lines, 74 backticked terms checked against the cited page); page range (529 citations in references, agent, adapters and index, 0 out of range).
4. **Manual, layer b**: a sample of **101 v1 claims** (agent, 11 references, glossary, scripts and tests) read against the cited page (full list in `scratch/audit/software-testing-qa-expert/notes/manual_sample_v1.md`). Covers all 5 sources and all themes (JUnit, doubles, mocking/contract, TDM, JMeter, pyramid/flaky/larger tests).
5. **Scripts**: audited (origin of the rules), rewritten and executed; `tests/run_script_tests.py`.

## 3. Result of the manual sample of v1 (101 claims)
| Class | Qty | Meaning |
|---|---|---|
| OK | 6 | page and content supported |
| Wrong page (PG) | 30 | content exists, but on another page (e.g. DAMP at "SWE-G p.220"; it is at p.177-179) |
| No basis (SL) | 47 | the source does not say it |
| Exaggeration (EX) | 18 | the source says something smaller or different |
Result: **only 6% of the sample was correct as written.** The dominant failure was source identity: v1 described JUNIT as a JUnit 5 refcard, MOCK as a DZone refcard with the Meszaros taxonomy and JMETER as a load guide with Little's Law and an HTML report; none of that content is in the PDFs.

### Relevant examples of what had no basis or was distorted
1. **JUnit 5/Jupiter** (`@BeforeEach`, `assertAll`, `assertThrows`, `@ParameterizedTest`, "Platform/Jupiter/Vintage") attributed to "JUNIT p.1-6": the PDF is a JUnit 4 tutorial; none of these terms appears (negative checks N07-N09).
2. **70/20/10 pyramid** "SWE-G p.213-217": the book says 80/15/5 (p.156) and 80/20 (p.165); p.213-217 are in larger tests (A/B diff, UAT) and do not discuss proportion.
3. **Meszaros Dummy/Stub/Spy/Mock/Fake taxonomy** "MOCK p.2; SWE-G p.241-247": MOCK p.2 is the table of contents and SWE-G p.241-247 is outside the testing chapters; "Dummy", "Spy" and "Meszaros" do not appear (N02, N11). The book organizes faking, stubbing and interaction testing (p.188-189).
4. **JMeter**: Little's Law, JSON Path Extractor, `-e -o` with dashboard and percentiles, "strict prohibition" of the GUI with "100% CPU" (JMETER p.46-47): none of this is in the PDF; p.50 only recommends non-GUI to experienced users (`-n -t -l`) and few listeners (N18-N21).
5. **TDM**: LGPD and fines, static/dynamic masking, Copy-on-Write, "10 TB", "12 to 24 hours", "2% to 5%", "90% of storage": absent (N14-N16); the refcard cites GDPR, HIPAA and PCI (p.6).
6. **Scripts**: `jmeter_calc.py` invented percentiles (p90 = 1.3 x latency "M/M/1") and `tdm_audit.py` attributed "LGPD violation" and score weights to the book; the README documented flags (`--tps`, `--rt`) that did not exist.
7. **Exaggeration of "mandatory"**: masking "mandatory" and "absolute mathematical irreversibility" (TDM p.6 says "ideally non-reversible"); mocks "solely" for side effects (SWE-G p.197-199 admits other cases).
8. **Report**: "19/19 PASS in blind tests" with no documented blind execution; CT-13 validated Little's Law as "JMETER p.9-10, p.14-16".

## 4. What was fixed
- **Agent** (`agents/software-testing-qa-expert.md`): rewritten with the real identity and versions of the sources, page convention (PDF), a table of when to consult REAL `references/` files and scripts, response format, epistemic honesty with the 4 labels and a list of what must never be attributed to the sources, boundary, `[DATED]` content and anti prompt-injection (70 lines).
- **References** (11 files, names preserved): the 10 thematic/general ones rewritten with checked pages; `INDEX.md` now carries the identity of the sources, the PDF↔printed map (JUNIT, JMETER, SWE-G) and "what the sources do not cover"; absolute user links (`file:///` with drive and personal folder) removed. Claims with no basis were removed or downgraded to `[extrapolation]` (JUnit 5 in its own map, Meszaros, Little's Law, `-e -o`, LGPD).
- **Scripts**: `testing_index.json` from 16 to 29 topics with `not_in_book` and an `uncovered` list (NOT COVERED); `testing_lookup.py` with `--book`, `--topic`, coverage note; `doubles_selector.py` with the rules of SWE-G p.189-200 and "dummy" as an `[extrapolation]`; `jmeter_calc.py` without percentiles, with labeled arithmetic and Little as an `[extrapolation]`; `tdm_audit.py` with 15 anti-patterns and 7 practices, each with a page, the score declared as a heuristic and a notice that it is not legal advice (LGPD absent from TDM).
- **Package**: `README.md` with installation for Claude Code, Codex and GitHub Copilot and a notice to check the current documentation; `AGENTS.md` (Codex); `.github/agents/software-testing-qa-expert.agent.md` (Copilot); `plugin.json` v2.0.0 without the JUnit 5 description.
- **Tests**: `tests/verify_citations.py`, `tests/citation-checks.json`, `tests/audit_tokens.py`, `tests/run_script_tests.py`, `tests/casos-de-teste.md` (24 cases) and this report; synchronized with `_agents_tests/software-testing-qa-expert/`.

### Failures that the automatic verification itself found in the new text (and were fixed)
| Verifier | Finding | Fix |
|---|---|---|
| verify_citations | "front door" cited at SWE-G p.168; it is note 2 of ch. 12, printed on p.183 | reference and check fixed |
| verify_citations | `ErrorCollector` broken in the PDF as "ErrorCol lector" | check term adjusted |
| verify_citations | negative `expected\s*=` matched `expected = expectedResult` (constructor on p.7) | regex replaced by `@Test(expected` |
| audit_tokens | `when/verify` in the scenario (not from the source) flagged as a p.185 term | removed from the backticks |
| reading | "SWE-G p.241 is from ch. 17" was incorrect (p.241 is about version control) | replaced by "outside the testing chapters, which end at p.221" |

## 5. Verifiers and tests (final result)
- `verify_citations.py`: 145 positive, 21 negative, **0 failures**.
- `audit_tokens.py`: 292 citations, 74 terms, **0 failures, 0 near**.
- `run_script_tests.py --src ...`: **25 checks OK, 0 failures** (21 script cases, index validity, page ranges, `verify_citations`, `audit_tokens`).
- 24 conceptual/practical/edge/out-of-scope/injection cases in `casos-de-teste.md`, all met by the package author (not blind).

## 6. Coverage: what was NOT audited
- **Figures and screenshots**: the extracted text does not contain the content of the figures (JMeter screens, SWE-G figures 11-2 to 11-4 and 14-1 to 14-6). They were neither rendered nor read; claims that depend on figures were not made.
- **SWE-G chapters outside 11-14** (e.g. CI at p.330, build, code review) and the 20-page article: outside the agent's scope and not audited.
- **Quality of the writing and of the synthesis** of the references was reviewed by the author, but not by a second reader.
- The **manual sample of 101 claims** is from v1; the new claims were verified by the automatic checks (145 + terms) and by the author's reading, without an independent second reading.
- **Blind execution by an independent model**: not done.

## 7. Open items
1. Run the 24 cases blind with another model, using only agent + references + scripts.
2. If the goal was to cover **JUnit 5/Jupiter** and a **JMeter guide with load and reports**, the right sources ("Core JUnit 5" refcard, a practical JMeter guide) are **not** in `04_engineering_and_practices/`; include those PDFs and re-audit. Meanwhile, the agent treats JUnit 5 and `-e -o` as an `[extrapolation]`.
3. Visually check the figures cited above, if any answer needs them.
