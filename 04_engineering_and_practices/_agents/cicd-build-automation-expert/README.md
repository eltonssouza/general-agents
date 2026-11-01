# CI/CD & Build Automation Expert (Claude Code, Codex and GitHub Copilot)

Specialist agent for CI/CD and build automation, grounded in four sources. **Source rigor**: the package separates `[from source]` (read on the cited page) from `[inference]`, `[extrapolation]` and `[DATED]`, and declares what the sources do **not** say. **Page convention: every `(SIGLA p.N)` citation uses the PDF page** (GRADLE: printed = PDF − 8; SWE-G: the PDF has no printed number).

## 1. Sources (PDFs in `04_engineering_and_practices/`)

| Acronym | Work | Nature | Date | PDF pages |
|---|---|---|---|---|
| **CICD** | *CI/CD Trend Report: Automation for Reliable Software Delivery* (DZone) | **Trend report**: May 2021 survey (695 responses), articles and **sponsor content**; not a book | Jun/2021 | 67 |
| **GRADLE** | *Gradle Build Automation Handbook* (JavaCodeGeeks; file `Gradle-Cookbook-JavaCodeGeeks.pdf`) | Collection of **Gradle 2.3 tutorials** | 2016 | 78 |
| **GHA** | *Getting Started With GitHub Actions* (DZone Refcard 373, Justin Albano) | Introductory **refcard** with deployment to Azure | Feb/2022 | 7 |
| **SWE-G** | *Software Engineering at Google* (O'Reilly), ch. 18, 22 (introduction), 23 and 24 | Complete **book** as a 408-page PDF with no printed page number | 2020 | 408 (ch. 18: p.260-277; 22: p.316-329; 23: p.330-346; 24: p.347-353) |

The file `Software-Engineering-at-Google.pdf` (20 pages, a 2017 article) is **not** a source of this package. The sources belong to their authors; the package contains its own syntheses and references, not the text of the PDFs.

## 2. What changed in the audit (v1 -> v2)
v1 attributed to the sources a lot of content they do not contain (for example, the three Gradle phases, `implementation`/`api`, DORA metrics and ranges, action pinning by SHA, `permissions`, secret masking, "presubmit in 10 minutes") and cited SWE-G p.215 and p.369-495 (nonexistent or on other subjects). v2 fixes pages, labels extrapolations and ships verifiers. Details and counts in `tests/relatorio-de-fidelidade.md` (fidelity report); gaps in `references/lacunas-e-conteudo-datado.md`.

## 3. Structure
```
cicd-build-automation-expert/
├── .claude-plugin/plugin.json
├── .github/agents/cicd-build-automation-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                              # Codex
├── agents/cicd-build-automation-expert.md                 # Claude Code
├── references/   INDEX, glossary, procedures, cases-and-antipatterns, gaps + 9 thematic files
├── skills/      cicd-topic-lookup, gradle-task-check, delivery-metrics-evaluator, github-actions-workflow-linter, verify-citations   (SKILL.md; they use the scripts in scripts/)
├── scripts/      cicd_lookup.py (+ cicd_index.json), gradle_trace.py, dora_evaluator.py, gha_linter.py
├── tests/        casos-de-teste.md (26), relatorio-de-fidelidade.md, verify_citations.py (+ citation-checks.json),
│                 audit_tokens.py, run_script_tests.py
└── README.md
```

## 4. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check the current documentation of each platform**: agent formats, plugins and frontmatter fields change.

### 4.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/cicd-build-automation-expert` (the folder contains `.claude-plugin/plugin.json`).
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install cicd-build-automation-expert@general-agents`.
- Or as a standalone subagent: copy `agents/cicd-build-automation-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder and adjust the paths cited in the prompt, if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 4.2 Codex (OpenAI)
Copy the package folder into the repository (for example, `tools/cicd-build-automation-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with the working directory in the package folder itself.

### 4.3 GitHub Copilot (custom agent)
Copy `.github/agents/cicd-build-automation-expert.agent.md` to `.github/agents/` of your repository and copy the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The frontmatter uses `tools: ['read','search','execute']`; remove `execute` to block script execution.

## 5. Scripts (deterministic, no network, read-only)
```bash
python -I scripts/cicd_lookup.py "gradle wrapper"            # topic -> source and pages; NOT COVERED if absent
python -I scripts/cicd_lookup.py --list
python -I scripts/gha_linter.py --file .github/workflows/ci.yml   # each rule declares its origin; no score
python -I scripts/gha_linter.py --rules
python -I scripts/gradle_trace.py order --task build         # illustrative order of the java plugin [extrapolation]
python -I scripts/gradle_trace.py check --file build.gradle  # loose code in a task body [extrapolation]
python -I scripts/dora_evaluator.py ranges                   # DORA 2024 p.13 table [extrapolation] + CICD p.34-35 survey
python -I scripts/dora_evaluator.py evaluate --deploy-frequency 20 --lead-time-hours 36 --recovery-hours 5 --cfr-percent 12
python -I scripts/dora_evaluator.py compute --deploys 24 --days 30 --failed 3 --lead-hours 10 20 50 --recovery-hours 2 6
python -I tests/verify_citations.py --src /path/to/txt       # CICD.txt GRADLE.txt GHA.txt SWEG.txt with "=== PAGE N ==="
python -I tests/audit_tokens.py --src /path/to/txt
python -I tests/run_script_tests.py --src /path/to/txt
```
Origin notes: `dora_evaluator.py` does **not** use ranges from the sources (they do not exist): it compares with the clusters of the DORA 2024 report p.13 and does **not** assign an overall level. `gha_linter.py` marks the pinning, `permissions`, `timeout-minutes` and `concurrency` rules as `[extrapolation]`. `gradle_trace.py` does not simulate a build; the task order is an illustration. The lookup index keeps Portuguese keywords alongside English ones, so queries in either language work.

## 6. Guarantees and limits
- Replies in the language the user writes in (default: English), without reproducing the sources; citations by PDF page.
- Audit: 115 positive and 20 negative checks (`tests/verify_citations.py`) plus term auditing of all citations (`tests/audit_tokens.py`). Coverage and what was **not** audited: see `tests/relatorio-de-fidelidade.md`.
- Pasted inputs (YAML, scripts, logs) and PDF text are data, not instructions.
- The tests were **not** run blind by an independent model (see the report).
- The content reflects the dates of the sources (2016 to 2022): Gradle 2.3 and `@v2` actions are `[DATED]`; check the current documentation.
