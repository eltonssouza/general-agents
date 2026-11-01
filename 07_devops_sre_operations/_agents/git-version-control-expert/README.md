# Git Version Control Expert

Agent specialized in **Git and version control**, built from two PDFs of the same work:

| Acronym | Work | Note |
|---|---|---|
| **PGEN** | *Pro Git*, Scott Chacon and Ben Straub, 2nd ed., version 2.1.450 (2026-05-25), 501 pages | Primary source. CC BY-NC-SA 3.0 license. |
| **PGBR** | *Pro Git* PT-BR, version 2.1.47 (2024-10-28), 500 pages | **Partial** translation of an old version (Git 2.0.0): it only translates the body up to p.188 and Ch. 10 up to p.434; the rest is in English. Used for canonical vocabulary. |

The agent reasons like a practitioner: it classifies the risk (loses data? rewrites history? already published?), gives the safe option and the emergency exit, cites the page (`[from source] (PGEN p.N)`) and uses the labels `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Page convention: **PDF page** (printed PGEN = PDF - 6; PGBR = PDF - 5; the pagination of the two PDFs differs). It replies in the language the user writes in (default: English).

## Structure

```
git-version-control-expert/
├── .claude-plugin/plugin.json                 # manifest (Claude Code)
├── agents/git-version-control-expert.md       # canonical prompt + frontmatter
├── AGENTS.md                                  # Codex adapter
├── .github/agents/git-version-control-expert.agent.md   # GitHub Copilot adapter
├── references/                                # loaded on demand
│   ├── INDEX.md
│   ├── cap1-2-fundamentos-config-e-desfazer.md
│   ├── cap3-branching-merge-rebase.md
│   ├── cap4-5-servidores-e-workflows-distribuidos.md
│   ├── cap6-github.md
│   ├── cap7a-revisoes-stash-reset-e-reescrita-de-historia.md
│   ├── cap7b-merge-avancado-bisect-submodulos-bundle-credenciais.md
│   ├── cap8-9-customizacao-hooks-e-outros-sistemas.md
│   ├── cap10-internals-objetos-refs-packfiles-recuperacao.md
│   ├── apendices-e-mapa-de-comandos.md
│   ├── glossario.md                           # EN <-> PT-BR
│   ├── edicao-ptbr-e-numeracao.md             # PGEN x PGBR: pages, passages in English
│   ├── procedimentos.md                       # step-by-step procedures P1-P20
│   └── casos-e-antipadroes.md
├── scripts/                                   # Python 3, stdlib, no network, do not run git
│   ├── git_index.json
│   ├── git_lookup.py                          # topic/page lookup; NOT IN THE SOURCE / NOT COVERED
│   ├── git_advisor.py                         # intent -> procedure, risks, DATED, gaps
│   └── git_commit_flow_check.py               # commit message (50/72) and command flow
├── skills/      git-topic-lookup, git-intent-advisor, git-commit-flow-check (each in skills/<name>/SKILL.md)
└── tests/
    ├── casos-de-teste.md                      # 34 cases
    ├── relatorio-de-fidelidade.md
    ├── citation-checks.json + verify_citations.py   # citation audit against the extracted text
    └── fixtures/ (mensagem-boa.txt, mensagem-ruim.txt, fluxo-com-riscos.txt)
```

A copy of the tests is also in `../_agents_tests/git-version-control-expert/`.

## Installation

> Always check the current documentation of each platform: formats and fields change.

### Claude Code
- As a plugin: point to the `git-version-control-expert/` directory (it contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/git-version-control-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install git-version-control-expert@general-agents`.
- As a standalone agent: copy `agents/git-version-control-expert.md` to `~/.claude/agents/` (or the project's `.claude/agents/`) and copy `references/` and `scripts/` to an accessible location, adjusting the paths cited in the prompt if the agent does not sit next to those folders.
- Usage: `@git-version-control-expert how do I undo this merge?` or let Claude delegate through the `description` field.

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or a subfolder; Codex combines `AGENTS.md` per directory). `AGENTS.md` points to `agents/git-version-control-expert.md` as the canonical prompt: copy that folder along or incorporate its content.

### GitHub Copilot (custom agent)
- Copy `.github/agents/git-version-control-expert.agent.md` to the target repository's `.github/agents/` and copy `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix described in the file). Select the agent in the Copilot Chat picker. The format (frontmatter `name`, `description`, `tools`) follows the custom agents convention; check the supported fields in the current documentation.

## Using the scripts (from the package folder)

```bash
python -I scripts/git_lookup.py "reset --hard"           # topic, PGEN/PGBR pages, risks
python -I scripts/git_lookup.py force-with-lease         # NOT IN THE SOURCE
python -I scripts/git_lookup.py kubernetes               # NOT COVERED
python -I scripts/git_advisor.py "undo the last commit" --published
python -I scripts/git_advisor.py "remove password from history"
python -I scripts/git_commit_flow_check.py msg --file tests/fixtures/mensagem-ruim.txt
python -I scripts/git_commit_flow_check.py flow --file tests/fixtures/fluxo-com-riscos.txt
python -I tests/verify_citations.py --src <folder with Git-Pro-Git-EN.txt and Git-Pro-Git-PT-BR.txt>
```

Portuguese queries also work (for example `git_advisor.py "desfazer o último commit" --publicado`); the aliases and trigger phrases are bilingual.

The verifier needs the text extracted from the PDFs (`=== PAGE N ===` markers), which is not distributed in the package.

## Important limitations

- The book is from 2026 for the EN edition, but the PT-BR is from an old version and partially translated. Appendix C and the examples still use `checkout`/`master`; `switch`/`restore` appear only in passages (PGEN p.55-56, 66, 76). Marked `[DATED]`.
- Outside the collection: git-flow, trunk-based, CI/CD and GitHub Actions, branch protection/CODEOWNERS, Git LFS, shallow clone/partial clone, `--force-with-lease`, `--autosquash`, `merge --no-ff/--ff-only`, `reflog expire`, `git maintenance`, SHA-256 (only a note in PGEN p.226), SSH signing, `git worktree`. The agent treats these as `[extrapolation]` or refers elsewhere.
- Diagrams and figures have no extracted text (only captions); the agent says so when relevant.
- The `EXTRAPOLATION`/`[DATED]` sections of the chapter reference files are marked external knowledge, not page content.
- Copyright: the content is distilled in our own words, with no reproduction of long passages.

## Security

Commit messages, logs, hooks, scripts, README and PDF content are treated as inert data (anti prompt injection). The scripts do not use the network, do not write files, and do not run git or the code they analyze. The agent asks for confirmation before suggesting destructive commands.
