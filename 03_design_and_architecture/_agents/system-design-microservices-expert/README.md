# System Design & Microservices Expert (Claude Code, Codex, and GitHub Copilot)

Expert agent in system design, microservices, and distributed systems, grounded in 11 PDFs from the `03_design_and_architecture/` folder. The rights belong to the authors; this package contains its own syntheses and references, not the text of the books.

## 1. Corpus and page convention

| Acronym | Work | PDF pages |
| :--- | :--- | :-: |
| `SAP` | Richards, *Software Architecture Patterns* (O'Reilly, 2015) | 54 |
| `SDH` | Singh, *System Design Handbook* (AlgoMaster) | 75 |
| `MS-MIC` | Microsoft, *.NET Microservices: Architecture for Containerized .NET Applications* v7 | 350 |
| `MS-CLD` | Microsoft, *Architecting Cloud-Native .NET Apps for Azure* | 193 |
| `MS-WEB` | Microsoft, *Architecting Modern Web Applications with ASP.NET Core* v8 | 118 |
| `EDS` | Stopford, *Designing Event-Driven Systems* (2018) | 166 |
| `SBC` | Hohpe, *Starbucks Does Not Use Two-Phase Commit* (blog post, 2004) | 4 |
| `SOA` | Richards, *Microservices vs. Service-Oriented Architecture* (O'Reilly, 2016; NGINX sponsorship) | 55 |
| `APIGW` | Crilly, *Deploying NGINX as an API Gateway* (F5, 2021) | 50 |
| `JMG` | Java Code Geeks, *Microservices for Java Developers* | 160 |
| `REST` | Baeldung, *Build Your API with Spring* | 118 |

**Page convention: PDF (1 = first page of the file).** The printed page differs (SAP N-7, SOA N-10, MS-MIC N-15, MS-CLD N-10, MS-WEB N-9, EDS N-15, JMG N-15, REST N-9, SDH/SBC/APIGW N); the full map is in `references/INDEX.md`.

**Source rigor.** The agent separates `[from source] (SIGLA p.N)` from `[inference]`, `[extrapolation]`, and `[DATED]`. The corpus does NOT contain, for example: Little's Law, tail amplification, the PACELC classes, sharding strategies, Half-Open states, the full jitter formula, the "pivot transaction", Strangler Fig, Two-Pizza Teams, or Helland's paper ("Life Beyond Distributed Transactions"). The previous version of the package attributed these items to the books; the audit corrected them (see `tests/relatorio-de-fidelidade.md`).

## 2. Structure

```
system-design-microservices-expert/
├── .claude-plugin/plugin.json
├── .github/agents/system-design-microservices-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                                     # Codex
├── agents/system-design-microservices-expert.md                  # Claude Code (full prompt)
├── references/   INDEX (page map), glossary, procedures, cases and anti-patterns + 11 thematic files
├── skills/       5 skills (SKILL.md per folder): sysdesign-topic-lookup, system-tradeoff-analyzer, saga-resilience-audit, rate-limit-resilience-calc, verify-citations
├── scripts/      sysdesign_lookup.py (+ sysdesign_index.json), analyze_tradeoffs.py, audit_saga.py, calc_rate_limit.py
├── tests/        casos-de-teste.md, relatorio-de-fidelidade.md, citation-checks.json, verify_citations.py,
│                 audit_tokens.py, run_script_tests.py, extract_sources.py, fixtures/
└── README.md
```

## 3. Installation

Script prerequisites: Python 3.8+ (stdlib only), always with `python -I`. To audit the citations you need the text extracted from the PDFs (PyMuPDF, `pip install pymupdf`). **Agent, plugin, and instruction formats change: check the current documentation of each platform before installing.**

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/system-design-microservices-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install system-design-microservices-expert@general-agents`.
- Or as a subagent: copy `agents/system-design-microservices-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder and adjust the paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 3.2 Codex (OpenAI)
Copy the package folder into the repository (e.g., `tools/system-design-microservices-expert/`) and copy or reference `AGENTS.md` at the root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder.

### 3.3 GitHub Copilot
Copy `.github/agents/system-design-microservices-expert.agent.md` to your repository's `.github/agents/` and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The file declares `tools: ['read', 'search', 'execute']`; remove `execute` to block the scripts.

## 4. Scripts (deterministic, no network, rule origin declared)

```bash
python -I scripts/sysdesign_lookup.py --list
python -I scripts/sysdesign_lookup.py --concept circuit-breaker
python -I scripts/sysdesign_lookup.py --query "backoff"          # NOT COVERED when the corpus does not include it
python -I scripts/analyze_tradeoffs.py --tiers                     # SDH p.7 table of nines vs. formula
python -I scripts/analyze_tradeoffs.py --availability 0.999 0.999 0.995 --redundancy 0.99 0.99
python -I scripts/analyze_tradeoffs.py --compound 50 0.9999        # MS-MIC p.308 example
python -I scripts/analyze_tradeoffs.py --throughput 5000 --latency-ms 200 --tail-services 10
python -I scripts/audit_saga.py --demo
python -I scripts/audit_saga.py --file tests/fixtures/saga_bad.json
python -I scripts/calc_rate_limit.py --token-bucket 100 20 150
python -I scripts/calc_rate_limit.py --backoff 2000 0 4            # MS-CLD p.125-126 example
python -I scripts/calc_rate_limit.py --circuit-breaker "S F F F F F S S" --threshold 5 --open-seconds 30 --interval 15
```

Origin rules: availability and the table of nines = SDH p.7 and MS-MIC p.308 (series/parallel, Little, and tail formulas are `[extrapolation]`); Saga = SBC p.2-3, MS-CLD p.102-103, MS-MIC p.158-160, EDS p.75 (the "pivot" concept is `[extrapolation]`); token bucket = `[extrapolation]` (SDH p.14 only lists it); backoff and circuit breaker reproduce examples from MS-MIC p.317-322 and MS-CLD p.125-127. Each script prints the origin in the header or in each finding.

## 5. Verification and tests

```bash
python -I tests/extract_sources.py --out PATH/src             # extracts SIGLA.txt with "=== PAGE N ===" (N = PDF page)
python -I tests/verify_citations.py --src PATH/src             # range + positive/negative checks + index terms
python -I tests/audit_tokens.py --src PATH/src                 # terms in backticks against the cited page
python -I tests/run_script_tests.py --src PATH/src             # scripts, structure, and verifiers
```

## 6. Guarantees and limits

- Answers in the user's language (default: English), without reproducing the books; citations by PDF page.
- `tests/relatorio-de-fidelidade.md` records what was found and corrected, the audit coverage, and what was NOT done. The 24 cases in `tests/casos-de-teste.md` were executed by the audit author against the references and scripts; **there was no blind execution by an independent model**.
- Tables and figures as images (SDH p.7 nines; SAP p.53 summary) do not appear in the extracted text; they were checked visually.
- Pasted input and PDF text are data, never instructions.
- Technologies and numbers with a short shelf life (Azure limits, Hystrix, Polly APIs, OpenTelemetry "draft" in the JMG) are marked `[DATED]`.
