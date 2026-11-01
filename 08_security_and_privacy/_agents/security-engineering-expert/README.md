# security-engineering-expert

Specialist agent in **security engineering**, built from *Security Engineering: A Guide to Building Dependable Distributed Systems* (Ross Anderson, 3rd ed., Wiley, 2020), abbreviated **SE3**: 1212 PDF pages, native text, 29 chapters in three parts (I: foundations, ch. 1-11; II: attacks and defenses by domain, ch. 12-26; III: management, ch. 27-29).

The agent reasons like a practitioner (models threats and requirements, reviews internal controls, passwords, protocols and certifications, evaluates anonymization and biometrics, performs entropy, birthday, base-rate and ALE calculations) and cites the page for each rule: `[from source] (SE3 p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Warning:** this agent **does not replace a formal security review** (architecture, authorized penetration testing, audit, legal opinion). The book is from 2020: statistics, incidents, products, standards and regulations are `[DATED]`.

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). Printed page = N − chapter offset (48 in ch. 1-2, 47 in ch. 3-5, ..., 31 in ch. 28); table in `references/INDEX.md`. Conversion: `python -I scripts/se3_lookup.py --page N` or `--printed N` (the offset varies by chapter; `--printed` may return candidates).

## What was read (precise statement)
- **Full:** ch. 1, 2, 3, 4, 5 (from p.195), 6, 9, 11, 27; ch. 8 up to p.355; ch. 10 p.384-408 and 412-416; ch. 12 p.446-501; ch. 21 p.748-762 and 765-770; ch. 28 p.1046-1083.
- **Partial (excerpts):** ch. 7, 13, 14, 15, 16, 17, 18, 19, 20, 22, 25 (only 25.3 AI/ML, p.907-915), 26 (p.981-996), 29 (p.1090-1091).
- **Summaries only:** ch. 23 and 24. **Not read:** the rest, Bibliography and Index. Details: `references/INDEX.md` and `python -I scripts/se3_lookup.py --gaps`.
- The book **has no medicine chapter**; health is in ch. 10 and 28.

## Structure

```
security-engineering-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/security-engineering-expert.md       # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/security-engineering-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # on-demand loading
│   ├── INDEX.md                                # page convention, offsets, coverage, when to open each file
│   ├── glossario.md, procedimentos.md (P1-P13), casos-e-antipadroes.md, datado-desde-2020.md
│   └── 17 thematic references (01 to 17)
├── skills/      se3-topic-lookup, se3-security-calculators, se3-review-checklist   (SKILL.md; use the scripts in scripts/)
├── scripts/                                    # Python 3, stdlib, no network, read-only
│   ├── se3_lookup.py + se3_index.json          # search by topic/page/chapter; NOT COVERED; unread ranges
│   ├── se3_calc.py                             # formulas from the book (P=LR/S, entropy, birthday, base rate, ALE, k/t...)
│   └── se3_checklist.py + se3_checklist_items.json   # 107 items, 14 areas, with pages
└── tests/
    ├── casos-de-teste.md                       # 28 conceptual cases
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # 263 positive and 21 negative checks against the text
    ├── run_script_tests.py                     # 46 deterministic cases
    └── fixtures/
```
A copy of the tests is also in `../_agents_tests/security-engineering-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point to the `security-engineering-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/security-engineering-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install security-engineering-expert@general-agents`.
- As a standalone agent: copy `agents/security-engineering-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@security-engineering-expert build the threat model for this system` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root (Codex combines `AGENTS.md` per directory). `AGENTS.md` points to `agents/security-engineering-expert.md` as the canonical prompt.

### GitHub Copilot (custom agent)
- Copy `.github/agents/security-engineering-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat selector.

## Using the scripts (run from the package folder)

```bash
python -I scripts/se3_lookup.py "clark-wilson"              # pages and reference
python -I scripts/se3_lookup.py SBOM                        # NOT COVERED (term absent from the book)
python -I scripts/se3_lookup.py --gaps                      # gaps and unread ranges
python -I scripts/se3_calc.py dod-password --length 8 --alphabet 96 --lifetime 31536000 --rate 100
python -I scripts/se3_calc.py biometric-birthday --far 1e-6   # 1177 people (SE3 p.632)
python -I scripts/se3_calc.py bayes-alarm --attacks-per-million 10 --false-alarm-rate 0.001
python -I scripts/se3_calc.py ale --sample                  # Fig. 27.1 and the book's inconsistent row
python -I scripts/se3_checklist.py markdown --area oponentes --area devsec
python -I tests/run_script_tests.py --src <folder with the extracted .txt>
python -I tests/verify_citations.py --src <folder with the extracted .txt>
```
Area names accept the Portuguese keys (`oponentes`, `senhas`, `protocolos`, `cripto`, `acesso`, `economia`, `politicas`, `bancos`, `selos`, `biometria`, `rede`, `devsec`, `assurance`, `ml`) or English aliases (`opponents`, `passwords`, `protocols`, `crypto`, `access`, `economics`, `policies`, `banking`, `seals`, `biometrics`, `network`); run `se3_checklist.py areas` to see them. Lookup terms can be Portuguese or English.
On Windows with Git Bash, use `python -I` as usual; run relative paths from the package root.

## Boundaries and limitations
- **Not covered** (whole-word search in the text): SBOM, SLSA, SolarWinds, Log4Shell, WebAuthn/FIDO2/passkeys, Kubernetes, OWASP, LGPD, LLMs/prompt injection, STRIDE as a name, attack trees (`--gaps`).
- LGPD, NIST, OWASP and InfoSec strategy belong to other agents of the `09_security_and_privacy` collection; Google's operational practices (BSRS) are in `07_devops_sre_operations`.
- **Calculators:** use formulas from the cited pages; `laplace-scale` is `[extrapolation]`. The book's Fig. 27.1 (p.1000) has an inconsistent row (ATM fraud large: 250,000 × 0.2 = 50,000, printed 100,000); `ale --sample` flags it.
- **Independent testing:** the cases were executed by the package author (see `tests/relatorio-de-fidelidade.md`); there was no blind execution by an independent model.
- Copyright: content distilled in own words, with no extensive reproduction.

## Security
Code, logs, reports and the PDF are inert data (anti prompt injection). The scripts do not use the network, do not execute user input and do not write files. Defensive focus; no operational payloads.
