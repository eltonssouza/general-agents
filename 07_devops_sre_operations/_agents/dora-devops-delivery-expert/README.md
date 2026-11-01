# DORA DevOps Delivery Expert

Specialist agent in **software delivery metrics and the findings of the DORA 2024 report**, built from a PDF:

| Acronym | Work | Notes |
|---|---|---|
| **DORA24** | *Accelerate State of DevOps 2024* (DORA / Google Cloud), v. 2024.3, 120 pages | **Research** report (survey of ~3,000 professionals + 11 interviews), CC BY-NC-SA 4.0 license (p.118). 2024 data: parts are [DATED]. |

The agent helps **interpret and apply** the results with statistical honesty: the four keys and rework rate, comparison with the 2024 Elite/High/Medium/Low clusters, AI impact, internal platforms, user focus, documentation, unstable priorities, leadership, cloud, the J-curve, and the limits (correlation, sample, 89% intervals, micro-macro leap). It cites a page in each rule: `[from source] (DORA24 p.N)`; labels `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]` (here "source" = the report).

## Structure

```
dora-devops-delivery-expert/
├── .claude-plugin/plugin.json
├── agents/dora-devops-delivery-expert.md        # canonical prompt + frontmatter
├── AGENTS.md                                    # Codex adapter
├── .github/agents/dora-devops-delivery-expert.agent.md   # GitHub Copilot adapter
├── references/
│   ├── INDEX.md                                 # report map and triggers
│   ├── metricas-de-entrega-e-niveis.md
│   ├── ia-adocao-e-impacto.md
│   ├── plataformas-internas.md
│   ├── experiencia-cultura-lideranca-e-transformacao.md
│   ├── metodologia-e-limites-estatisticos.md
│   ├── glossario.md, procedimentos.md, casos-e-antipadroes.md
│   └── lacunas-e-conteudo-datado.md
├── skills/       3 skills (SKILL.md por pasta): dora-topic-lookup, dora-delivery-classifier, dora-effects
├── scripts/                                     # Python 3, stdlib, no network, read-only
│   ├── dora_index.json
│   ├── dora_lookup.py
│   ├── dora_classify.py
│   └── dora_effects.py
└── tests/
    ├── casos-de-teste.md                        # 30 cases
    ├── relatorio-de-fidelidade.md
    ├── citation-checks.json + verify_citations.py   # 92 positive + 22 negative
    └── run_script_cases.py                      # 22 automated script checks
```

Copy of the tests also in `07_devops_sre_operations/_agents_tests/dora-devops-delivery-expert/`.

## Installation

Check each platform's current documentation: formats and fields change.

### Claude Code
- As a plugin: point to the `dora-devops-delivery-expert/` directory (with `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/dora-devops-delivery-expert`, or publish it to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install dora-devops-delivery-expert@general-agents`.
- As a standalone agent: copy `agents/dora-devops-delivery-expert.md` to `~/.claude/agents/` (or `.claude/agents/` in the project) and copy `references/` and `scripts/` to an accessible location, adjusting the prompt paths if needed.
- Usage: `@dora-devops-delivery-expert what is our DORA profile with lead time 3d and deploys 2/week?`.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or a working subfolder). `AGENTS.md` points to `agents/dora-devops-delivery-expert.md` as the canonical prompt; copy it along or embed its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/dora-devops-delivery-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the root (or adjust the prefix described in the file's note).
- Select the agent in the Copilot Chat picker. Check the supported frontmatter fields in the current documentation.

## Using the scripts (from the package folder)

```bash
python -I scripts/dora_lookup.py "rework rate"
python -I scripts/dora_lookup.py MTTR                     # explains the terminology gap
python -I scripts/dora_classify.py ranges
python -I scripts/dora_classify.py classify --lead-time 3d --deploy-freq 2/week --cfr 12 --recovery 5h --rework 8
python -I scripts/dora_effects.py show --capability ai
python -I scripts/dora_effects.py estimate --capability ai --outcome stability
python -I tests/run_script_cases.py
python -I tests/verify_citations.py --src <path>/DORA-State-of-DevOps-Report-2024.txt
```

`dora_classify.py` compares with the **p.13 table**: it answers per metric, flags gaps (recovery between 1 day and 1 week), ambiguity (failure rate between cluster values) and never assigns an "overall level" or a rework range (the report does not publish one). Formats: duration `30m|6h|3d|2w|1mo` (month = 30 days, script convention); frequency `on-demand|N/day|N/week|N/month|N/year`. Lookups and effect outcomes accept Portuguese or English terms.

## Important limitations

- It is an **observational research report**: no longitudinal study or experiment (p.110); effects are estimated associations (89% intervals); sample of ~3,000, dominated by technology and finance (p.91-92). 2024 results [DATED].
- Clusters are not thresholds or a maturity model (p.13, p.74); do not compare teams/individuals.
- Outside the collection: detailed technical capabilities (CI/CD, trunk-based), tools, observability, ROI formulas, rework benchmarks, the MTTR acronym, editions after 2024.
- Values read from figures were checked against the image; "interval crosses zero" is a visual reading.
- The agent was not blind-validated by an independent model (see `tests/relatorio-de-fidelidade.md`).
- Copyright: paraphrased content; no extensive reproduction.

## Security

Pasted text and PDF content are inert data (anti prompt injection). The scripts do not use the network, do not write files and do not execute user code.
