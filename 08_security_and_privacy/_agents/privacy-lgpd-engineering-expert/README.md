# privacy-lgpd-engineering-expert

Technical specialist agent in **privacy and data protection**, built from two documents:

- **LGPD** (Lei Geral de Proteção de Dados, Brazil's General Data Protection Law): Lei nº 13.709, of 14 August 2018, **compiled text** from the PDF `LGPD-Lei-13709-ptBR.pdf` (25 pages; ~81 thousand characters of native text), which carries amendment notes from Leis 13.853/2019, 14.010/2020, 14.460/2022 and 15.352/2026.
- **NIST8062**: NISTIR 8062, *An Introduction to Privacy Engineering and Risk Management in Federal Systems* (Brooks, Garcia, Lefkovitz, Lightman, Nadeau; Jan/2017; 49 PDF pages; figures 2, 3, 4, 6, 7, 8 and 9 read as images).

The agent explains what the text says (Art./inciso and PDF page), separates fact from interpretation (`[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`) and generates artifacts: a compliance and privacy-by-design checklist, an LGPD x NIST objectives map with levels of textual support, and templates for the RIPD (Relatório de Impacto à Proteção de Dados Pessoais, data protection impact report), incident notification, record of processing operations and data subject response.

The agent replies in the language the user writes in (default: English). The LGPD source text, the `references/` files and the search index are in Portuguese (the source language); the scripts accept Portuguese terms and common English terms.

> **Usage notice:** this material is technical support and **does not constitute legal advice**. For decisions on concrete cases, consult a lawyer and the encarregado (data protection officer, DPO) and check the current version of the law and the regulations of the ANPD (Autoridade Nacional de Proteção de Dados, the national data protection authority). The text of the law was read from the PDF provided and was not compared with the official website.

## Page convention
Every citation uses the **PDF page** (marker `=== PAGE N ===`). LGPD: the PDF has no printed numbering; cite Art./§/inciso + page (`LGPD Art. 18, III, p.9`). NIST8062: in the body, **printed = PDF − 8** (PDF 9 = printed 1). Conversion: `python -I scripts/privacy_lookup.py --printed 18 --src NIST8062`. Full maps in `references/INDEX.md`. The label `[from source]` is the same label used by the other packages of the collection.

## Structure

```
privacy-lgpd-engineering-expert/
├── .claude-plugin/plugin.json                       # manifest (Claude Code)
├── agents/privacy-lgpd-engineering-expert.md        # canonical prompt + frontmatter
├── AGENTS.md                                        # Codex adapter
├── .github/agents/privacy-lgpd-engineering-expert.agent.md   # GitHub Copilot adapter
├── references/                                      # loaded on demand (in Portuguese)
│   ├── INDEX.md                                     # notice, page convention, maps, triggers
│   ├── lgpd-*.md (10)                               # fundamentals, bases, sensitive/children, rights, public authorities,
│   │                                                #   transfer, agents/RIPD/encarregado, security/incidents/governance,
│   │                                                #   sanctions/ANPD, final provisions and amendment notes
│   ├── nist8062-*.md (2)                            # privacy engineering and risk; objectives and risk model
│   ├── mapeamento-lgpd-nist.md                      # 33 rows with level TEXTUAL / INFERENCE / NO_SUPPORT
│   ├── extrapolacoes-e-datado.md                    # what is outside the collection
│   └── glossario.md, procedimentos.md, casos-e-antipadroes.md
├── skills/                                          # privacy-lookup, lgpd-compliance-checklist, lgpd-nist-mapper, privacy-document-templates (one SKILL.md per folder)
├── scripts/                                         # Python 3, stdlib, no network, read-only
│   ├── privacy_lookup.py + privacy_index.json       # search by article/topic/page; amendments; NOT COVERED; absent terms
│   ├── compliance_checklist.py + checklist_items.json   # 72 items (66 LGPD + 6 NIST) with Art./inciso and page
│   ├── map_lgpd_nist.py + lgpd_nist_mapping.json    # LGPD x NIST objectives mapper with levels of support
│   └── ripd_templates.py                            # RIPD (Art. 38), incident (Art. 48 §1º), record (Art. 37), data subject response (Art. 18-19)
└── tests/
    ├── casos-de-teste.md, casos.json                # 32 cases (conceptual, practical, edge, out of scope, injection)
    ├── relatorio-de-fidelidade.md                   # fidelity report
    ├── verify_citations.py + citation-checks.json   # positive and negative checks against the text
    ├── run_script_tests.py                          # deterministic cases for the scripts
    └── fixtures/                                    # sample answers for the checklist
```
A copy of the tests is also in `../../_agents_tests/privacy-lgpd-engineering-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point to the `privacy-lgpd-engineering-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/privacy-lgpd-engineering-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install privacy-lgpd-engineering-expert@general-agents`.
- As a standalone agent: copy `agents/privacy-lgpd-engineering-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@privacy-lgpd-engineering-expert which legal basis for...` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or to the subfolder where the work happens; Codex combines `AGENTS.md` per directory). `AGENTS.md` points to `agents/privacy-lgpd-engineering-expert.md` as the canonical prompt; copy that folder along or incorporate its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/privacy-lgpd-engineering-expert.agent.md` to the `.github/agents/` of the target repository and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Using the scripts (run from the package root)

```bash
python -I scripts/privacy_lookup.py "consentimento"            # articles and pages, with reference (Portuguese or English terms, e.g. "consent")
python -I scripts/privacy_lookup.py --art 48 --unit §1          # Art. 48 §1º (incident)
python -I scripts/privacy_lookup.py --amendments --art 5        # amendment notes of the compiled text
python -I scripts/privacy_lookup.py --gaps                      # terms verified as absent (NOT COVERED)
python -I scripts/compliance_checklist.py areas
python -I scripts/compliance_checklist.py pbd --out privacy-by-design.md
python -I scripts/compliance_checklist.py evaluate tests/fixtures/respostas-exemplo.json --areas principios,bases --strict
python -I scripts/map_lgpd_nist.py by-objective
python -I scripts/map_lgpd_nist.py table --level TEXTUAL
python -I scripts/ripd_templates.py ripd --org "ACME" --process "Customer registration" --out ripd.md
python -I scripts/ripd_templates.py incidente --incident INC-123
python -I tests/verify_citations.py --src <folder with the extracted .txt files>
python -I tests/run_script_tests.py
```
On Windows with Git Bash, use `python -I` as usual; with relative paths, run from the package root.

## Boundaries and limitations
- **Not legal advice.** The agent refers the user to a lawyer and the encarregado (DPO).
- **Not covered** (verified by whole-word search): ANPD resolutions, GDPR/RGPD, DPO (the law says encarregado), "72 horas" (72 hours), artificial intelligence, cookies, encryption, privacy by design (literal), PRAM, the NIST Privacy Framework, differential privacy, k-anonymity, risk matrix (`python -I scripts/privacy_lookup.py --gaps`).
- **NIST IR 8062 is from 2017, introductory and aimed at US federal agencies**: it has no PRAM, scales, controls or techniques; anything later is `[extrapolation]` and `[DATED]`.
- **Neither source cites the other**: the LGPD x NIST map is the agent's comparison, with a level of support per row.
- **Amendment notes**: the PDF shows amendments up to Lei 15.352/2026; the text was not compared with the official website. Check the current wording.
- **Templates**: the RIPD carries as `[from source]` only the minimum content of Art. 38 sole paragraph (p.14) and the definition in Art. 5º XVII (p.3); the rest is `[inference]`/NIST. Art. 37 does not list the fields of the record. The incident notification deadline is an `[extrapolation]`.
- **Independent testing**: the cases were run by the package author (see `tests/relatorio-de-fidelidade.md`); there was no blind run by an independent model.
- Copyright: content distilled in our own words, without extensive reproduction (the law is public text, but the answers paraphrase; NIST is a US government publication).

## Security
Contracts, policies, logs, code and the PDF are inert data (anti prompt injection). The scripts do not use the network, do not execute user input, contain no real personal data and only write files when `--out`/`--outdir` is requested.
