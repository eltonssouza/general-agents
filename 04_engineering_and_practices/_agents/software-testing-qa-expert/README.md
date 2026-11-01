# Software Testing & QA Expert (Claude Code, Codex and GitHub Copilot)

A testing engineering and QA specialist agent grounded in five sources. **The rights belong to the authors; this package contains its own syntheses and references, not the text of the works.**

| Acronym | What the PDF is | Pages |
|---|---|---|
| **SWE-G** | *Software Engineering at Google* (Winters, Manshreck, Wright; O'Reilly, 2020): chapters 11 to 14 | PDF p.149-221 (of 408) |
| **JUNIT** | *JUnit Tutorial* (Java Code Geeks, 2014): **JUnit 4**, 8-page excerpt | 8 |
| **MOCK** | "Intro to API Mocking" e-book from SmartBear (marketing) | 12 (content p.3-10) |
| **TDM** | DZone Refcard *Test Data Management: Patterns and Anti-Patterns for a Data Factory* (Niall Crawford, 2021) | 9 |
| **JMETER** | *JMeter Tutorial* (Java Code Geeks, 2015), **JMeter 2.11** | 53 |

**Source rigor.** The agent separates `[from source] (SIGLA p.N)` from `[inference]`, `[extrapolation]` and `[DATED]`. **Page convention: PDF** (only JMETER has a different printed page: "N / 46" = PDF − 7). **The sources do not contain**: JUnit 5/Jupiter, the Meszaros Dummy/Spy taxonomy, the 70/20/10 pyramid (the book says 80/15/5), Little's Law and percentiles, JMeter's `-e -o`, JSON Path Extractor, LGPD. See `references/INDEX.md`.

## 1. Overview
Helps decide and review: test mix and size, flaky tests and hermeticity, clear unit tests, the choice between real implementation, fake, stub and interaction testing, API mocking and contract testing, test data management (profiling, synthetic data, masking, subsetting, virtualization) and JMeter load plans.

## 2. Structure
```
software-testing-qa-expert/
├── .claude-plugin/plugin.json
├── .github/agents/software-testing-qa-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                            # Codex
├── agents/software-testing-qa-expert.md                 # Claude Code
├── references/   INDEX (sources, versions, page map), glossary, procedures, cases-and-anti-patterns + 8 thematic files
├── scripts/      testing_lookup.py (+ testing_index.json), doubles_selector.py, jmeter_calc.py, tdm_audit.py
├── skills/       testing-topic-lookup, test-doubles-selector, jmeter-load-plan-calc, tdm-checklist (each in <name>/SKILL.md)
├── tests/        casos-de-teste.md (24), relatorio-de-fidelidade.md, run_script_tests.py,
│                 verify_citations.py (+ citation-checks.json), audit_tokens.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**, since agent formats and locations change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/software-testing-qa-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install software-testing-qa-expert@general-agents`.
- Or as a subagent: copy `agents/software-testing-qa-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder, adjusting paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent running the scripts.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (e.g. `tools/software-testing-qa-expert/`) and copy or reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder.

### 3.3 GitHub Copilot
Copy `.github/agents/software-testing-qa-expert.agent.md` to the `.github/agents/` of your repository and the package folder into the repository (adjust `<PKG>` in the file). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, no network)
```bash
python -I scripts/testing_lookup.py "data masking"          # --list, --topic fakes, --book SWE-G
python -I scripts/testing_lookup.py jupiter                 # NOT COVERED (exit 1)
python -I scripts/doubles_selector.py --slow-or-unhermetic --stateful-collaborator
python -I scripts/doubles_selector.py --fault-injection
python -I scripts/jmeter_calc.py --threads 100 --ramp-up 20 --loops 10 --latency 80 --think-time 500 --sla 200
python -I scripts/jmeter_calc.py --target-tps 250 --latency 800 --think-time 1200
python -I scripts/tdm_audit.py --raw-prod --manual-inspect
python -I tests/run_script_tests.py --src /path/to/extracted-texts
python -I tests/verify_citations.py --src /path/to/extracted-texts
python -I tests/audit_tokens.py --src /path/to/extracted-texts
```
`testing_lookup.py` accepts queries in English or Portuguese (the index keeps both keyword sets).

**Origin of the script rules**: `doubles_selector.py` uses SWE-G p.189-200 ("dummy" is an `[extrapolation]`); `tdm_audit.py` uses TDM p.3-8 (score weights are a heuristic, not from the book; not legal advice); `jmeter_calc.py` uses the Thread Group arithmetic (JMETER p.15) and Little's Law, which is **not** in the PDF and is labeled `[extrapolation]`; it does not estimate percentiles. `testing_lookup.py` answers only with what is in `testing_index.json`.

`verify_citations.py`, `audit_tokens.py` and `run_script_tests.py --src` require the per-page extracted texts (`JUNIT.txt`, `MOCK.txt`, `TDM.txt`, `JMETER.txt`, `SWEG.txt`, with `=== PAGE N ===` markers; see the header of `tests/verify_citations.py` for the PyMuPDF extraction command). The source PDFs are in `04_engineering_and_practices/` of the collection.

## 5. Guarantees and limits
- Replies in the user's language (default: English), without reproducing the works; citations by page (PDF).
- Audit: see `tests/relatorio-de-fidelidade.md` (automatic verification with 145 positive and 21 negative checks, audit of backticked terms and a manual sample of 101 v1 claims).
- Pasted input (code, JMX, logs, data) and PDF text are data, not instructions.
- The tests were **not** run blind by an independent model (see the report). The audit coverage and the open items are in the report.
