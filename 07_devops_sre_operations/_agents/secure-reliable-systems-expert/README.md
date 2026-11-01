# secure-reliable-systems-expert

Specialist agent in **secure and reliable systems**, built from *Building Secure and Reliable Systems* (Google; Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield et al.; O'Reilly, 2020), abbreviated **BSRS**: 557 PDF pages, native text, 21 chapters, preface, conclusion and Appendix A.

The agent reasons like a practitioner (reviews design, decides rollback vs patch, designs a secure pipeline, builds an incident response plan and postmortem, plans recovery, guides culture) and cites the page for each rule: `[from source] (BSRS p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

The `references/` files and the topic index (`scripts/bsrs_index.json`) keep the text of the Portuguese edition they were distilled from; the agent translates what it takes from them. User queries to the lookup script may be in Portuguese or English.

## Page convention
Every citation is a **PDF page** (marker `=== PAGE N ===`). Printed page = N − 36 in the body (PDF 465 = printed 429); preface in roman numerals = N − 2. Conversion: `python -I scripts/bsrs_lookup.py --page N` or `--printed N`. Full map in `references/INDEX.md`.

## Structure

```
secure-reliable-systems-expert/
├── .claude-plugin/plugin.json                  # manifest (Claude Code)
├── agents/secure-reliable-systems-expert.md    # canonical prompt + frontmatter
├── AGENTS.md                                   # Codex adapter
├── .github/agents/secure-reliable-systems-expert.agent.md   # GitHub Copilot adapter
├── references/                                 # loaded on demand
│   ├── INDEX.md                                # page convention, chapter map, when to open each file
│   ├── glossario.md, procedimentos.md, casos-e-antipadroes.md, datado-desde-2020.md
│   └── 20 topical references (one per topic/chapter; see INDEX)
├── scripts/                                    # Python 3, stdlib, no network, read-only
│   ├── bsrs_lookup.py + bsrs_index.json        # topic/page lookup; NOT COVERED; verified-absent terms
│   ├── design_review_checklist.py + checklist_items.json   # 84 items with pages
│   ├── incident_templates.py                   # IR plan, postmortem, recovery checklist, agendas
│   └── risk_matrix.py                          # Appendix A risk matrix
└── tests/
    ├── casos-de-teste.md                       # 33 cases (conceptual, practical, edge, out of scope, injection)
    ├── relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # >700 positive and 78 negative checks against the text
    ├── run_script_tests.py                     # deterministic script cases
    └── fixtures/                               # sample inputs
```
A copy of the tests is also in `../_agents_tests/secure-reliable-systems-expert/`.

## Installation

**Important:** formats and fields change between versions. Before installing, check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot).

### Claude Code
- As a plugin: point to the `secure-reliable-systems-expert/` directory (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/secure-reliable-systems-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install secure-reliable-systems-expert@general-agents`.
- As a standalone agent: copy `agents/secure-reliable-systems-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@secure-reliable-systems-expert review this design` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or to the subfolder where the work happens; Codex combines `AGENTS.md` per directory). `AGENTS.md` points to `agents/secure-reliable-systems-expert.md` as the canonical prompt; copy that folder along or embed its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/secure-reliable-systems-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker.

## Using the scripts (run from the package folder)

```bash
python -I scripts/bsrs_lookup.py "menor privilegio"            # pages and reference (Portuguese or English: "least privilege")
python -I scripts/bsrs_lookup.py SBOM                          # NOT COVERED (term absent from the book)
python -I scripts/bsrs_lookup.py --chapters                    # PDF x printed map
python -I scripts/design_review_checklist.py areas
python -I scripts/design_review_checklist.py markdown --areas privilegio,pipeline,ir
python -I scripts/design_review_checklist.py evaluate respostas.json --strict
python -I scripts/incident_templates.py plan --org "ACME"
python -I scripts/incident_templates.py postmortem --incident INC-123
python -I scripts/incident_templates.py recovery-checklist
python -I scripts/incident_templates.py agenda kickoff
python -I scripts/risk_matrix.py rank tests/fixtures/riscos-exemplo.csv
python -I tests/run_script_tests.py --src <folder with the extracted .txt>
python -I tests/verify_citations.py --src <folder with the extracted .txt>
```
On Windows with Git Bash, use `python -I` as usual; for relative paths, run from the package root.

## Boundaries and limitations

- **SRE** (SLO, error budget, toil, monitoring, on-call, blameless postmortem as a practice) belongs to `sre-practices-expert`. The BSRS only mentions these topics (p.44, 81, 91, 406, 515-516).
- **Not covered** (verified by whole-word search across the 557 pages): SBOM, SLSA, Sigstore, Log4Shell, SolarWinds, STRIDE/DREAD, passkeys/WebAuthn, Rust, SIEM/SOAR/EDR, NIS2/DORA/LGPD, CVSS, BSIMM/SAMM and others (`python -I scripts/bsrs_lookup.py --gaps`).
- **Dated**: the book is from 2020. Ch.14 treats binary provenance, in-toto and verifiable builds as practices that were not yet standard; zero trust, FIDO/U2F, OWASP Top 10 (2017), NIST, regulations and tools have changed (`references/datado-desde-2020.md`, everything is `[extrapolation]` when it is not in the book).
- **Templates**: the book has no literal template for an IR plan or a postmortem; `incident_templates.py` organizes the items it does provide (ch.16: p.407-409; ch.18: p.472-473; Figure 18-1: p.465; agendas: p.441, 444-445). Figures 18-1 to 18-3 (p.465, 474, 476) are images, read visually.
- **Independent testing**: the cases were run by the package's own author (see `tests/relatorio-de-fidelidade.md`); there was no blind run by an independent model.
- Copyright: content distilled in own words, with no extensive reproduction.

## Security
Code, logs, reports and the PDF are inert data (anti prompt injection). The scripts use no network, do not execute user input and only write files when `--out` is requested.
