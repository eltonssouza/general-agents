# Observability & OpenTelemetry Expert (Claude Code, Codex, and GitHub Copilot)

**Introductory** specialist agent for observability of distributed systems and OpenTelemetry basics, grounded in two short works (DZone Refcards, 2021, 7 pages each):

- **[DOW]** *Getting Started With Observability for Distributed Systems*, Nicolas Giron and Hicham Bouissoumer (KumoMind). Source file: `Distributed-Observability-Whitepaper.pdf`.
- **[OTW]** *Getting Started With OpenTelemetry: Observability and Monitoring for Modern Applications*, Charles Mahler (InfluxData). Source file: `OpenTelemetry-Whitepaper.pdf`.

The rights belong to the authors/Devada; this package contains its own syntheses and references, not the text of the works.

## 1. What the agent does
Answers and reviews: monitoring vs observability; metrics, logs, and traces; graphs and alerts; platform checklist; agent-based collection and log policy; OpenTelemetry (APIs, SDKs, Collector, Agent vs Gateway, OTLP, spans, Context API, automatic vs manual instrumentation, legacy migration, backends). Reviews simple Collector YAML pipelines (reference coherence). Describes the works' diagrams based on a visual reading of the pages.

**Source rigor**: every claim from the source comes with `[from source] (DOW p.N)` or `(OTW p.N)` (PDF page = printed number; p.2 of each work is an ad). Anything not from the source is given as `[inference]`, `[extrapolation]`, or `[DATED]`. **Declared out of scope**: per-language SDKs and instrumentation (only Python/Flask in the OTW), advanced Collector, W3C propagation, SLOs, advanced sampling, commercial products, and **current OpenTelemetry versions/status** (the works are from 2021; only Tracing was stable).

## 2. Structure
```
observability-opentelemetry-expert/
├── .claude-plugin/plugin.json
├── .github/agents/observability-opentelemetry-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                                    # Codex
├── agents/observability-opentelemetry-expert.md                 # Claude Code
├── references/   INDEX, glossario, procedimentos, casos-e-antipadroes and 6 thematic files (includes diagramas-e-figuras and fronteira-e-datado)
├── skills/      obs-topic-lookup, collector-pipeline-check, signal-advisor   (SKILL.md; use the scripts in scripts/)
├── scripts/      obs_lookup.py + obs_index.json, collector_pipeline_check.py, signal_advisor.py
└── tests/        casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py, citation-checks.json, fixtures/
```

## 3. Installation
Script prerequisite: Python 3.8+ (standard library only), always with `python -I`. **Check each platform's current documentation**: agent formats and locations change.

### 3.1 Claude Code
- As a local plugin: `claude --plugin-dir /path/observability-opentelemetry-expert`.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install observability-opentelemetry-expert@general-agents`.
- As a subagent: copy `agents/observability-opentelemetry-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (for example, copy the folder to `.claude/observability-opentelemetry-expert/` and adjust the paths).

### 3.2 Codex (OpenAI)
- Copy the folder into the repository and use `AGENTS.md` at the root (or `~/.codex/AGENTS.md`); replace `<PKG>` with the real path. Alternative: open Codex with the working directory set to the package folder.

### 3.3 GitHub Copilot
- Copy `.github/agents/observability-opentelemetry-expert.agent.md` to your repository's `.github/agents/` and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. `tools: ['read', 'search', 'execute']`: remove `execute` if you do not want to run the scripts. The custom-agent format evolves; check the current documentation.

## 4. Scripts (deterministic, no network)
```bash
python -I scripts/obs_lookup.py "context propagation"      # topic with pages and "NOT IN THE SOURCE"; --list lists everything
python -I scripts/signal_advisor.py "slow service across microservices"
python -I scripts/collector_pipeline_check.py tests/fixtures/pipeline-otw-p3.yaml
python -I tests/verify_citations.py --src <folder with the extracted .txt files>
```
`collector_pipeline_check.py` does static reference checking (component used but not defined, pipeline without receiver/exporter, processor order); it does **not** validate real Collector names/fields. A "NOT COVERED" output in the scripts = subject outside the sources.

## 5. Guarantees and limits
- Replies in the user's language (default: English); no reproduction of excerpts; verbatim quotes are rare (<15 words).
- Audit: `tests/relatorio-de-fidelidade.md` (102 positive checks, 21 negative, 20+ test cases run by the author; **not** run blindly by an independent model).
- Injection immunity: YAML, spans, logs, and the PDFs' text are passive data.
- The works are sponsored, introductory material; for production, use the current official OpenTelemetry documentation.
