# aws-lambda-serverless-expert

Specialist agent for **AWS Lambda and serverless**, built from a single PDF:

| Abbreviation | Work | Note |
|---|---|---|
| **LAMBDA** | *AWS Lambda Developer Guide*, Amazon Web Services (official product documentation), © 2022, 1297 pages | Last releases entry on **11/28/2022** (LAMBDA p.968). Native text, excellent extraction. **Ages fast:** every number, limit, quota, runtime, version, CLI and price is marked `[DATED]`. |

The agent diagnoses invocation and errors, concurrency, cold start, configuration and limits, IAM, VPC, layers, versions/aliases, container images, SnapStart, event source mappings (SQS, Kinesis, DynamoDB, Kafka/MSK/MQ), observability and quotas, cites the page of each rule `[from source] (LAMBDA p.N)` and labels `[inference]`, `[extrapolation]`, `[DATED]`.

**Page convention:** `p.N` = **PDF** page; printed page = N - 22 (the body starts on PDF p.23). Section map in `references/INDEX.md`.

## Structure

```
aws-lambda-serverless-expert/
├── .claude-plugin/plugin.json
├── agents/aws-lambda-serverless-expert.md          # canonical prompt + frontmatter
├── AGENTS.md                                       # Codex adapter
├── .github/agents/aws-lambda-serverless-expert.agent.md   # GitHub Copilot adapter
├── references/   # INDEX, glossario, procedimentos (P1-P10), casos-e-antipadroes, lacunas-e-fronteiras
│                 # + 20 thematic files: fundamentals, environment/VPC, IAM, runtimes/extensions, deploy/layers, configuration,
│                 #   concurrency, invocation/errors, push services, event sources (stream/queue/Kafka), snapstart,
│                 #   languages (common pattern + differences), observability, troubleshooting, SAM/Step Functions,
│                 #   best practices, quotas [DATED], API reference, samples/releases
├── scripts/      # Python 3 stdlib, no network, read-only
│   ├── lambda_lookup.py            # lookup by topic/term; "NOT COVERED" when there is nothing
│   ├── lambda_validate_config.py   # validates a config against the limits IN THE TEXT
│   ├── lambda_review_checklist.py  # 42-item checklist
│   ├── lambda_index.json, lambda_limits.json
├── skills/       # lambda-topic-lookup, lambda-config-validator, lambda-review-checklist (<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md (28 cases), relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # >1900 positive checks + 18 negative
    └── run_script_tests.py                           # 36 deterministic cases
```
Copy of the tests in `../../_agents_tests/aws-lambda-serverless-expert/`.

## Installation

### Claude Code
- Local plugin: `claude --plugin-dir <path>/aws-lambda-serverless-expert` (the folder contains `.claude-plugin/plugin.json`), or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install aws-lambda-serverless-expert@general-agents`.
- Standalone agent: copy `agents/aws-lambda-serverless-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the prompt paths if needed.
- Usage: `@aws-lambda-serverless-expert review this configuration` or let Claude delegate through the `description`.

### OpenAI Codex (and agents that read `AGENTS.md`)
Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root (Codex merges `AGENTS.md` per directory).

### GitHub Copilot (custom agent)
Copy `.github/agents/aws-lambda-serverless-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>`). Select the agent in Copilot Chat.

> The formats and fields accepted by each platform change: **check the current documentation** of Claude Code, Codex and GitHub Copilot before installing.

## Using the scripts (from the package folder)

```bash
python -I scripts/lambda_lookup.py "visibility timeout"
python -I scripts/lambda_lookup.py "response streaming"        # NOT COVERED
python -I scripts/lambda_validate_config.py --example > cfg.json
python -I scripts/lambda_validate_config.py cfg.json
python -I scripts/lambda_review_checklist.py --list
python -I scripts/lambda_review_checklist.py --config cfg.json answers.json
python -I tests/run_script_tests.py
python -I tests/verify_citations.py --text <path>/AWS-Lambda-Developer-Guide.txt
```
The verifier needs the text extracted from the PDF (marker `=== PAGE N ===`); by default it looks in `../../../scratch/devops/AWS-Lambda-Developer-Guide.txt` relative to the package.

## Important limitations
- **2022 edition:** does not cover anything after Nov/2022 (response streaming, Node.js 20, Python 3.10+, SQS ScalingConfig, SnapStart beyond Java 11 etc.). The guide's limits and quotas are starting points, not current truth.
- No concrete prices; no benchmarks.
- The guide's text has internal contradictions (e.g., MemorySize 3008 vs 10,240 MB); they are listed in `references/casos-e-antipadroes.md`.
- The thematic references (generated from the per-section reading notes) have **no accents**; the hand-written ones (glossary, procedures, cases, gaps, INDEX) are accented.
- The per-language code examples were read as a common pattern + differences; long SDK listings (p.892-966) were read by sampling.
- The agent was not blind-tested by an independent model (see `tests/relatorio-de-fidelidade.md`).
- Does not replace the current official AWS documentation.
