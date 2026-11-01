# Fidelity and audit report: cicd-build-automation-expert (v1 -> v2)

- **Agent**: `cicd-build-automation-expert`
- **Page convention**: `(SIGLA p.N)` = **PDF** page (GRADLE: printed = PDF − 8; SWE-G: 408-page PDF with no printed page number).
- **Source text used**: PyMuPDF 1.27, `=== PAGE N ===` markers (N = PDF page), in the files `CICD.txt`, `GRADLE.txt`, `GHA.txt` and `SWEG.txt` (outside the package, in `scratch/audit/cicd-build-automation-expert/src/`).
- **Important**: **there was no blind execution by an independent model.** The 26 test cases were executed by the auditor against the prompt, the references and the scripts; v1 claimed "19 of 19 PASS by independent automated validator" and that **had no backing** (the v1 criteria repeated the same wrong pages).

## 1. Source inventory
| Acronym | PDF | Real nature | Pages | Note |
|---|---|---|---|---|
| CICD | `CI-CD-DZone-Trend-Report-2021.pdf` | trend report (survey + articles + sponsors) | 67 | p.5-18 are a survey on TDD/BDD/SOLID/microservices; DORA only cited in p.16 |
| GRADLE | `Gradle-Cookbook-JavaCodeGeeks.pdf` | Gradle 2.3 tutorials (2016) | 78 | v1 called it "Handbook" and cited p.1-30 as if they were concepts; real content: p.7 preface, p.9-16 basics, p.17-24 properties, p.25-49 GWT/SourceSets, p.62-64 Wrapper |
| GHA | `GitHub-Actions-Guide.pdf` | 7-page refcard (Feb/2022) | 7 | it is an introductory refcard, not a complete GitHub Actions reference |
| SWE-G | `Software-Engineering-at-Google-completo.pdf` | complete book, 408 pages with no printed number | 408 | ch. 18 = p.260-277; ch. 22 = p.316-329; ch. 23 = p.330-346; ch. 24 = p.347-353 |

v1 convention: **inconsistent**. GRADLE/CICD/GHA used the PDF page, but many cited pages (for example, GRADLE p.26-30 for "incremental build") were about another subject; SWE-G used pages 369 to 495, **nonexistent or from other chapters** in this PDF (and chapter 22 was called "Chapter 20").

## 2. v1 findings (two-layer audit)
### 2.1 Automatic (`tests/audit_tokens.py` applied to v1)
- **262** `(SIGLA p.N)` citation groups (GHA 63, CICD 103, SWE-G 78, GRADLE 74).
- **57** groups with a page **outside the PDF** (all SWE-G, p.> 408); of the 78 SWE-G groups, **none** pointed to the chapters used (18, 23, 24).
- Verifiable terms (backticks, numbers, acronyms, names): 157 checked, **37 ok, 13 only on a neighboring page, 107 absent** from the cited page; **122 citations with problems** (invalid range or missing term).

### 2.2 Manual (84 v1 claims read against the cited pages and the real pages)
| Verdict | Count | Examples |
|---|---|---|
| OK | 9 | Event/Workflow/Job/Step/Runner (GHA p.3-4); GitHub Actions launched in 2019 (GHA p.1, 3); `.github/workflows/` (GHA p.4) |
| Wrong page (content exists on another page) | 15 | Task-based x artifact-based at "SWE-G p.369-375" (real: p.263-268); Delivery x Deployment rule at "CICD p.8-12" (real: p.22) |
| Unsupported | 50 | three Gradle phases and `settings.gradle` (GRADLE p.10-16); `implementation` vs `api`; DORA with ranges; SHA pinning and `permissions: contents: read` (CICD p.44-46); `cancel-in-progress`/`timeout-minutes`; secret masking and NaCl; "presubmit < 10 minutes"; SLO/1%/p95 canary; Trivy/Clair |
| Exaggeration (partly supported) | 10 | "ephemeral destroyed runners" (GHA p.4 says hosted or standalone); "immediate quarantine" of flaky tests (SWE-G p.337: temporarily remove from presubmit); incremental build by hash and cache (GRADLE p.26-30; real: only `UP-TO-DATE` in p.44-47 and `options.incremental` in p.33-34) |
Full list of the sample: `scratch/audit/cicd-build-automation-expert/notes/manual_sample.md`.

### 2.3 v1 numbers and scripts with no backing
- `dora_evaluator.py`: Elite/High/Medium/Low ranges (Elite lead time <= 1 h; CFR Elite <= 10%, High <= 20%, Medium <= 30%; MTTR by ranges; average "score") **do not come from any package source**. Comparison with the DORA 2024 report p.13 (audited package `dora-devops-delivery-expert`): Elite has lead time **< 1 day**, failure rate **5%** (High 20%, Medium 10%, Low 40%, values per cluster, not ranges), Elite recovery < 1 hour, High and Medium < 1 day, Low 1 week to 1 month; the report says the clusters are not a maturity model.
- `gha_linter.py`: invented scoring weights (30/25/15/10/5); pinning, `permissions`, `timeout`, `concurrency` rules attributed to CICD p.44-46, GHA p.4.
- `gradle_trace.py`: simulated "BUILD SUCCESSFUL" and marked tasks `UP-TO-DATE` with no basis; cited "GRADLE p.10-16" for phases that do not exist in the PDF.
- `cicd_index.json`: invalid SWE-G pages 369-495; CICD "IaC 51-55" and "security 56-60" imprecise (p.54 has no text; p.59-60 are an advertisement and a customer case).
- `plugin.json`/README: described GRADLE as a "Handbook" of concepts and SWE-G as "408 p. ch. 20"; README with no multi-platform installation.

## 3. Corrections made (v2)
- **Rewrote the 12 references** keeping the file names (links preserved) and **created** `references/lacunas-e-conteudo-datado.md`; `INDEX.md` now has the inventory, nature and date of the sources, page map and page convention.
- All citations now use the PDF page; SWE-G redone for p.260-277, 316-317, 330-353; CICD p.5-18 is no longer used for DORA/CD.
- Content that is not in the sources was **downgraded to `[extrapolation]`** (Gradle phases, `implementation`/`api`, input hashing, pinning, `permissions`, concurrency, secret masking, DORA) or **removed** (typosquatting, Trivy/Clair, "scanners capture tokens in seconds", unverified example SHAs, "10 minutes", "quarantine", 1% canary with p95/p99, "five pillars" for Elite).
- `[DATED]` content identified: Gradle 2.3 (`<<`, `compile`, `jcenter()`, `output.classesDir`), `@v2` and `openjdk:11`, 2020-2022 numbers.
- Prompt rewritten (98 lines) with sources and nature, page convention, scope and boundary, 4 labels, anti prompt-injection, backed decision rules, when to consult `references/` and `scripts/` (real files), response format and epistemic honesty; `AGENTS.md` (Codex) and `.github/agents/cicd-build-automation-expert.agent.md` (Copilot) created; `README.md` with installation on the 3 platforms and a reminder to check current documentation; `plugin.json` 2.0.0.
- **Scripts audited and rewritten**: `dora_evaluator.py` (no invented ranges: compares with DORA 2024 p.13 labeled `[extrapolation]`, with CICD p.34-35, no overall level); `gha_linter.py` (origin per rule, no score, check of `needs`/`runs-on`/secrets/injection); `gradle_trace.py` (no simulation; illustrative order; labeled task-body check); `cicd_lookup.py` + `cicd_index.json` (30 topics with PDF pages and 10 "NOT COVERED" groups).
- Encoding: files rewritten in UTF-8 without BOM; no user absolute paths in links (v1 had `claude plugin add c:\development\...` in the README).

## 4. Verifiers and results (v2)
| Verifier | Result |
|---|---|
| `tests/verify_citations.py --src <txt>` | **115 positive and 20 negative, 0 failures** (`citation-checks.json`; 4 sources; negatives cover DORA, three phases, `implementation`, pinning, `permissions`, `concurrency`, masking, quarantine, "10 minutes", SLO canary, Trivy/Clair, hermetic in ch. 18) |
| `tests/audit_tokens.py --src <txt>` | **404 citation groups; 0 invalid ranges; 276 terms checked, 276 ok, 0 failures, 0 on a neighboring page** (`[extrapolation]` passages, declared absences and v1 citations are skipped by a rule documented in the script) |
| `tests/run_script_tests.py --src <txt>` | **28 script cases + index validation + listing + the two verifiers: 0 failures** |
| `tests/casos-de-teste.md` | **26 cases** (C, P, B, F, I) executed by the auditor; 26 OK |

## 5. What was NOT audited (coverage)
- **GRADLE p.50-61 (OSGi/BNDTools) and p.65-71 (NetBeans)**: read by sampling; the package does not use them in claims.
- **SWE-G ch. 18**: p.260-273 read; p.274-277 (dependencies, transitive) read in excerpts; **ch. 22**: introduction only (p.316-317); the other SWE-G chapters are not part of the package.
- **CICD**: read in full, but the figures (pipeline diagrams, bar charts on p.7, 10-11, 14-17, 21-25) **were not inspected as images**; only the extracted text.
- The auditor's **`[extrapolation]` claims** (Gradle phases, `<<` removed, pinning, `permissions`, DORA) are general knowledge and were **not** checked against current documentation (no network); hence they carry the "check the current documentation" warning.
- The DORA 2024 table was **checked** against the text extracted from the report (p.13), but the report is not a source of this package.
- There was no independent model review nor blind execution of the test cases.

## 6. Pending
- Run a blind execution of the 26 cases with an independent model.
- Consider adding to the package a current GitHub Actions and Gradle source (the current documentation) to cover pinning, `permissions`, the Gradle phases and `implementation`/`api` with backing; today these topics are `[extrapolation]`.
- Visually inspect the CICD figures p.7-25 if any claim comes to depend on them.
