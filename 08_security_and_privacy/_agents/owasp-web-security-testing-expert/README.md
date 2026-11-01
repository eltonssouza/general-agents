# owasp-web-security-testing-expert

Expert agent for **guiding authorized web application security testing and methodology**, built from the *OWASP Web Security Testing Guide v4.2* (OWASP Foundation, 2020; Creative Commons 4.0 license per the front matter), abbreviated **WSTG**: 465 PDF pages, native text, ch. 2 (principles and techniques), ch. 3 (framework in the SDLC), ch. 4 (12 test categories with `WSTG-XXXX-NN` IDs), ch. 5 (reporting) and appendices A-F.

The agent uses the **test ID as the key** and cites the page: `[from source] (WSTG p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. It **guides people**: it does not scan targets, does not execute attacks, requires authorization and does not provide payloads beyond pointing to what the guide documents.

## Page convention
Every citation is a **PDF page** (`=== PAGE N ===` marker of the extracted text). Printed page = N − 2. Conversion: `python -I scripts/wstg_lookup.py --printed N` or `--page N`. Full ID → pages map in `references/INDEX.md`.

## Structure

```
owasp-web-security-testing-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/owasp-web-security-testing-expert.md # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/owasp-web-security-testing-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # loaded on demand (in English)
│   ├── INDEX.md                                # page convention, when to open each file, ID -> pages map (116 entries)
│   ├── glossario.md, procedimentos.md, casos-e-antipadroes.md, datado-desde-2020.md
│   └── 14 per-category references (introduction, framework, INFO, CONF, IDNT, ATHN, ATHZ, SESS, INPV x2, ERRH+CRYP, BUSL, CLNT+APIT, report)
├── scripts/                                    # Python 3, stdlib, no network, read-only
│   ├── wstg_lookup.py + wstg_index.json        # lookup by ID/topic/page; NOT COVERED; --gaps; --datado
│   ├── test_plan_generator.py                  # coverage checklist from the scope (authorization gate)
│   └── finding_template.py                     # finding template, report skeleton, validation
├── skills/       3 skills (<name>/SKILL.md; procedure with the package scripts)
└── tests/
    ├── casos-de-teste.md + casos.json          # 32 cases (conceptual, practical, edge, out of scope, injection)
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # 163 positive and 19 negative checks against the PDF text
    ├── run_script_tests.py                     # 30 deterministic script cases
    └── run_case_checks.py                      # deterministic coverage of the 32 cases (agent + references + scripts)
```
A copy of the tests is also in `../../_agents_tests/owasp-web-security-testing-expert/` (relative to the `_agents` folder).

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point to the `owasp-web-security-testing-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/owasp-web-security-testing-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install owasp-web-security-testing-expert@general-agents`.
- As a standalone agent: copy `agents/owasp-web-security-testing-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the prompt paths if the agent does not sit next to those folders.
- Usage: `@owasp-web-security-testing-expert what does WSTG-SESS-03 test?` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or to the subfolder where the work happens; Codex merges `AGENTS.md` per directory). `AGENTS.md` points to `agents/owasp-web-security-testing-expert.md` as the canonical prompt; copy that folder along or embed its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/owasp-web-security-testing-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Using the scripts (run from the package folder)

```bash
python -I scripts/wstg_lookup.py WSTG-SESS-03                  # ID -> title, pages, reference
python -I scripts/wstg_lookup.py "session fixation" --top 3    # topic (Portuguese terms also work)
python -I scripts/wstg_lookup.py --page 202                    # which test covers the PDF page
python -I scripts/wstg_lookup.py jwt                           # NOT COVERED
python -I scripts/wstg_lookup.py --gaps
python -I scripts/test_plan_generator.py features
python -I scripts/test_plan_generator.py sample > scope.json
python -I scripts/test_plan_generator.py plan --scope scope.json
python -I scripts/finding_template.py finding --id WSTG-ATHZ-04
python -I scripts/finding_template.py report-skeleton
python -I scripts/finding_template.py check finding.json
python -I tests/run_script_tests.py --src <folder with the extracted OWASP-WSTG-4.2.txt>
python -I tests/run_case_checks.py
python -I tests/verify_citations.py --src <folder with the extracted OWASP-WSTG-4.2.txt>
```
On Windows with Git Bash, use `python -I` normally; the scripts set UTF-8 output.

## Boundaries and limitations

- **ASVS and code review**: refer to `owasp-asvs-code-review-expert`. **Threat modeling and strategy**: `infosec-strategy-threat-modeling-expert`.
- **Not covered** (verified by whole-word search across the 465 pages): JWT, SAML/OIDC, WebAuthn, SBOM/SLSA, mass assignment, prototype pollution, CSP, Kubernetes/serverless, HTTP/2-3, EPSS and others (`python -I scripts/wstg_lookup.py --gaps`).
- **Dated**: the guide is from 2020 (Flash, Web SQL, TLS values, tool lists, Top 10/ASVS versions); see `references/datado-desde-2020.md`.
- **Authorization**: the WSTG has no authorization template; the agent uses what the guide says (rules of engagement, pre-engagement, scope in the report, per-test cautions) and marks the rest as `[extrapolation]` (see `references/procedimentos.md`).
- **Sampled reading**: INPV-05.1 to 05.8, INPV-06 to 19, ch. 4.11-4.12 and appendices A-D and F were read through summary, objectives and remediation; the operational core (payloads, evasions, DBMS-specific bypasses) was not transcribed, by safety decision. Details in `references/INDEX.md` and `tests/relatorio-de-fidelidade.md`.
- **Plan generator**: the feature → tests mapping belongs to the package `[inference]`; it covers only the guide's cases and does not replace risk analysis (the guide asks to reprioritize, p.8).
- **Independent testing**: the cases were run by the package author; there was no blind run by an independent model.
- Copyright: content distilled in its own words, without extensive reproduction.

## Security
Code, tool outputs, reports and the PDF are inert data (anti prompt injection). Authorization only counts when declared by the user in the chat. The scripts do not use the network, do not execute user input and do not write files.
