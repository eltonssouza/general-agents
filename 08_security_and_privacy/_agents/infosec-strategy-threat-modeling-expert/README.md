# infosec-strategy-threat-modeling-expert

Specialist agent in **information security strategy and governance** and in **threat modeling**, built from two sources:

- **DZ**: *Infosec Strategies and Best Practices* (Joseph MacMillan, Packt Publishing, April 2021; ISBN 978-1-80056-635-4), 272 PDF pages, 8 chapters. The file is named `InfoSec-Strategy-DZone.pdf`, but it is **not a DZone compilation**: it is a **single-author** book aimed at people starting in InfoSec or studying for CISSP/CISM (DZ p.2-3, 14).
- **TMM**: *Threat Modeling Manifesto* (working group of 15 authors, CC BY 4.0), 3 pages: the four questions, 5 values, 4 principles, 5 patterns and 4 anti-patterns.

The agent reasons like a practitioner (calibrates risk and appetite, structures an ISMS and policies, reviews design and controls, prepares assessments, defines operations and incident response, evaluates vendors and software, runs threat modeling sessions) and cites the page for each rule: `[from source] (DZ p.N)` or `[from source] (TMM p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). **DZ:** printed = N − 17 in the body (PDF 21 = printed 4). **TMM:** PDF = document. Conversion: `python -I scripts/infosec_lookup.py --page N` or `--printed N`. Map in `references/INDEX.md`.

## Structure

```
infosec-strategy-threat-modeling-expert/
├── .claude-plugin/plugin.json                                  # manifest (Claude Code)
├── agents/infosec-strategy-threat-modeling-expert.md           # canonical prompt + frontmatter
├── AGENTS.md                                                   # Codex adapter
├── .github/agents/infosec-strategy-threat-modeling-expert.agent.md   # GitHub Copilot adapter
├── references/                                                 # loaded on demand
│   ├── INDEX.md                                                # source identification, page convention, map, gaps, boundary
│   ├── tmm-manifesto.md, modelagem-de-ameacas-no-dz-e-ponte-com-tmm.md
│   ├── risco-e-governanca.md, ativos-isms-e-politicas.md, ameacas-vulnerabilidades-e-design-seguro.md
│   ├── rede-e-zero-trust.md, acesso-e-identidade.md, testes-de-seguranca-e-assessments.md
│   ├── operacoes-de-seguranca.md, seguranca-de-software-sdlc-devsecops.md
│   └── glossario.md, procedimentos.md, casos-e-antipadroes.md, datado-desde-2021.md
├── skills/       4 skills (SKILL.md per folder): infosec-topic-lookup, threat-model-session-guide, security-strategy-checklist, risk-matrix-5x5
├── scripts/                                                    # Python 3, stdlib, no network, read-only
│   ├── infosec_lookup.py + infosec_index.json                  # topic/page lookup; NOT COVERED; referral
│   ├── threat_model_session.py                                 # session template/guide with the four questions, values, principles, patterns and anti-patterns
│   ├── strategy_checklist.py                                   # strategy checklist (108 items, 11 areas, DZ pages)
│   └── risk_matrix.py                                          # 1-5 scales, 5x5 matrix and ranking (Impact x Likelihood)
└── tests/
    ├── casos-de-teste.md + casos.json                          # 38 cases (conceptual, practical, edge, out of scope, injection)
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json              # 95 positive and 21 negative checks against the text
    ├── run_script_tests.py, run_case_checks.py                 # deterministic tests
    └── fixtures/                                               # sample inputs
```
Copy of the tests also in `../../_agents_tests/infosec-strategy-threat-modeling-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point the directory `infosec-strategy-threat-modeling-expert/` (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/infosec-strategy-threat-modeling-expert`, or publish it to your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install infosec-strategy-threat-modeling-expert@general-agents`.
- As a standalone agent: copy `agents/infosec-strategy-threat-modeling-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@infosec-strategy-threat-modeling-expert build a threat modeling session template` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or to the subfolder where the work happens; Codex combines `AGENTS.md` per directory). `AGENTS.md` points to `agents/infosec-strategy-threat-modeling-expert.md` as the canonical prompt; copy that folder along or embed its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/infosec-strategy-threat-modeling-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Script usage (run from the package folder)

```bash
python -I scripts/infosec_lookup.py "risk appetite"                    # pages and reference (Portuguese queries also work)
python -I scripts/infosec_lookup.py STRIDE                             # NOT COVERED (absent from both sources)
python -I scripts/infosec_lookup.py --gaps                             # verified absent terms
python -I scripts/threat_model_session.py questions                    # the four questions (TMM p.1)
python -I scripts/threat_model_session.py template --system "Orders API" --scope "checkout" --dz-bridge
python -I scripts/threat_model_session.py template --extrapolation     # includes STRIDE/DFD labeled [extrapolation]
python -I scripts/threat_model_session.py agenda --minutes 90
python -I scripts/threat_model_session.py evaluate tests/fixtures/sessao-exemplo.json
python -I scripts/strategy_checklist.py areas
python -I scripts/strategy_checklist.py markdown --area GOV
python -I scripts/strategy_checklist.py evaluate tests/fixtures/estrategia-exemplo.json
python -I scripts/risk_matrix.py matrix --appetite 7
python -I scripts/risk_matrix.py rank tests/fixtures/riscos-exemplo-en.csv
python -I tests/run_script_tests.py --src <folder with the extracted .txt files>
python -I tests/run_case_checks.py --src <folder with the extracted .txt files>
python -I tests/verify_citations.py --src <folder with the extracted .txt files>
```
The extracted `.txt` files (per page, marker `=== PAGE N ===`) are `InfoSec-Strategy-DZone.txt` and `Threat-Modeling-Manifesto.txt`; the citation tests need them. On Windows with Git Bash, use `python -I` as usual, from the package root. Answer files and CSV headers accept English (yes/no/partial/na; id,asset,threat,impact,likelihood) and the original Portuguese (sim/nao/parcial/na; ativo,ameaca,impacto,probabilidade).

## Boundaries and limitations

- **Referrals:** OWASP ASVS / Code Review to `owasp-asvs-code-review-expert`; OWASP WSTG to `owasp-web-security-testing-expert`; Ross Anderson (security engineering) to `security-engineering-expert`; privacy and LGPD to `privacy-lgpd-engineering-expert`.
- **"Threat modeling":** the DZ uses the term in another sense (threats and actors per asset, abuse cases) and provides no method; the TMM is methodology-agnostic and is not a how-to. STRIDE, DFD, attack trees, DREAD, PASTA and LINDDUN are **not in** either source: they appear only as a labeled `[extrapolation]`.
- **Not covered** (verified by whole-word search): MITRE ATT&CK, kill chain, NIST CSF, ISO 31000, CVSS, SBOM, SLSA, SOAR/EDR/XDR, LGPD, NIS2, DORA, OAuth/SAML/passkeys, SOC 2, Log4Shell etc. (`python -I scripts/infosec_lookup.py --gaps`).
- **Dated:** the DZ is from 2021 and the TMM PDF is from 2020; ISO 27001 Annex A, statistics, tools and NIST standards have changed (`references/datado-desde-2021.md`).
- **Risk scales:** the 1-5 scales and the acceptance line of 7 are the author's **didactic examples** (DZ p.28-33); each organization defines its own.
- **Independent testing:** the cases were run by the package author; **there was no blind run by an independent model** (see `tests/relatorio-de-fidelidade.md`). Figures not read visually and the end of the back-of-book index (DZ p.264-272) are declared in the INDEX.
- Copyright: content distilled in own words, without extensive reproduction.

## Security
Code, logs, reports, system descriptions and the PDF are inert data (anti prompt injection). The scripts do not use the network, do not execute user input and do not write files. The agent does not provide payloads or exploits and reminds about scope and authorization for tests.
