# Linux Shell Administration Expert

Specialist agent in **shell fundamentals and Linux administration**, built from a single PDF:

| Abbreviation | Work | Note |
|---|---|---|
| **TLDP** | Machtelt Garrels, *Introduction to Linux: A Hands on Guide*, edition 1.27 (06/06/2008), The Linux Documentation Project, 223 pages | Native text (no OCR). **A 2008 book**: the agent marks `[DATED]` what has changed (SysV init, legacy GRUB, old RPM/yum, ifconfig, XFree86...). |

The agent reasons like a command-line practitioner (diagnoses PATH, permissions, processes, scheduling, redirection, backup, SSH/basic networking, basic security), **reviews** scripts, crontabs and file modes with the package tools, and cites a page on every rule: `[from source] (TLDP p.N)`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

**Page convention**: `p.N` = **PDF** page number; the printed page is **PDF − 8** (e.g. PDF 70 = printed 62).

**Boundary**: OS internals (scheduling, virtual memory, concurrency, FS internals) are left to the **`os-internals`** agent (*OSTEP* base); this agent forwards them. The book does **not** cover systemd, containers, SELinux, ACLs, `set -e`/`trap`, `ss`, ext4/XFS etc. (list verified in `tests/citation-checks.json`).

## Structure

```
linux-shell-administration-expert/
├── .claude-plugin/plugin.json                     # manifest (Claude Code)
├── agents/linux-shell-administration-expert.md    # canonical prompt + frontmatter
├── AGENTS.md                                      # Codex adapter
├── .github/agents/linux-shell-administration-expert.agent.md   # GitHub Copilot adapter
├── references/                                    # on-demand loading (19 files)
│   ├── INDEX.md (page convention, chapter map, triggers)
│   ├── glossario.md, procedimentos.md, casos-e-antipadroes.md
│   ├── ajuda-e-documentacao-do-sistema.md
│   ├── filesystem-hierarquia-particoes-e-inodes.md
│   ├── arquivos-links-e-busca-de-arquivos.md
│   ├── permissoes-propriedade-e-modos-especiais.md
│   ├── processos-jobs-sinais-e-desempenho-basico.md
│   ├── boot-init-runlevels-e-shutdown-datado.md
│   ├── agendamento-at-cron-e-tarefas-periodicas.md
│   ├── redirecionamento-pipes-e-filtros.md
│   ├── ambiente-do-shell-variaveis-e-scripts.md
│   ├── instalacao-de-software-e-pacotes-datado.md
│   ├── backup-compressao-e-criptografia.md
│   ├── redes-servicos-e-acesso-remoto.md
│   ├── seguranca-e-resposta-a-incidentes-basica.md
│   ├── x-window-impressao-editores-e-audio.md
│   └── fronteira-conteudo-datado-e-encaminhamento.md
├── skills/                                        # linux-topic-lookup, shell-script-linter, chmod-calculator (SKILL.md per folder)
├── scripts/                                       # Python 3, stdlib, no network, read-only
│   ├── linux_index.json                           # index: 40 topics, 170 commands, the book's glossary
│   ├── linux_lookup.py                            # index lookup ("NOT COVERED" when there is none)
│   ├── shell_lint.py                              # minimal static checker for shell scripts and crontabs
│   └── chmod_calc.py                              # octal/symbolic/ls -l/umask/special modes
└── tests/
    ├── casos-de-teste.md (31 cases) · casos.json · run_cases.py
    ├── relatorio-de-fidelidade.md
    ├── citation-checks.json + verify_citations.py # audit of the citations against the extracted text
    └── fixtures/ (exemplo-com-problemas.sh, exemplo-limpo.sh, exemplo-crontab.txt)
```

A copy of the tests is also in `../../_agents_tests/linux-shell-administration-expert/`.

## Installation

> Check each platform's current documentation: formats, frontmatter fields, paths and tool names change between versions.

### Claude Code
- **As a plugin**: point to this folder (which contains `.claude-plugin/plugin.json`) as a local plugin, for example `claude --plugin-dir <path>/linux-shell-administration-expert`, or publish it in your own marketplace.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install linux-shell-administration-expert@general-agents`.
- **As a standalone agent**: copy `agents/linux-shell-administration-expert.md` to `~/.claude/agents/` (or `.claude/agents/` in the project) and copy `references/` and `scripts/` to an accessible location, adjusting the `references/...` and `scripts/...` paths in the prompt if the agent does not sit next to those folders.
- Usage: `@linux-shell-administration-expert review this crontab` or let Claude delegate through the `description` field. The requested tools are minimal (Read, Grep, Glob, Bash to run the scripts).

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `references/` and `scripts/` to the repository root (or to the working subfolder; Codex combines `AGENTS.md` per directory). Also copy `agents/` if you want the canonical prompt referenced by AGENTS.md.

### GitHub Copilot (custom agent)
- Copy `.github/agents/linux-shell-administration-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the repository root (or adjust the `<PKG>` prefix).
- Select the agent in the Copilot Chat agent picker. The frontmatter follows the custom agents convention (`description`, `tools`); validate the supported fields in the current documentation.

## Using the scripts (from the package folder; Python 3, `-I`)

```bash
python -I scripts/linux_lookup.py inode                  # topic, pages, "NOT IN THE SOURCE"
python -I scripts/linux_lookup.py cmd tar                # pages where the command appears + glossary
python -I scripts/linux_lookup.py page 70                # PDF 70 = printed 62
python -I scripts/linux_lookup.py --not-in-book          # what the book does not cover
python -I scripts/shell_lint.py tests/fixtures/exemplo-com-problemas.sh
python -I scripts/shell_lint.py --crontab tests/fixtures/exemplo-crontab.txt --system
python -I scripts/shell_lint.py --list-rules             # rules, origin and pages
python -I scripts/chmod_calc.py octal 4755
python -I scripts/chmod_calc.py symbolic "u+rwx,go-rwx" --from 664
python -I scripts/chmod_calc.py umask 033                # the book's subtraction vs bitwise
python -I scripts/chmod_calc.py common                   # the book's table 3-9
python -I tests/verify_citations.py --src <folder with Linux-Introduction-to-Linux-TLDP.txt>
python -I tests/run_cases.py --src <folder with Linux-Introduction-to-Linux-TLDP.txt>
```

In Git Bash/Windows, set `MSYS_NO_PATHCONV=1` when passing arguments that start with `/`.

## Important limitations
- **A 2008, introductory book**: the agent does not replace current documentation; systems with systemd, UEFI, ext4/XFS, `ss`, nftables, SELinux stay as `[extrapolation]` or outside the collection.
- **Scripting**: the book devotes ~3 pages to shell scripts (p.129-131) and Appendix C (p.208-211). `shell_lint.py` is a MINIMAL checker (19 shell rules + 7 crontab rules); many are `[extrapolation]` and this is declared in each finding. No findings does not prove correctness; also use `shellcheck` (which the book does not mention).
- **Command citations**: `linux_lookup.py cmd` lists pages where the word appears (computed by text search), not necessarily the explanation of the command; open the page before citing.
- **Tests**: run by the package author against agent + references + scripts; there was **no** blind round by an independent model (see `tests/relatorio-de-fidelidade.md`).
- The PDF text was extracted with PyMuPDF (no OCR); the printed page where a chapter starts differs from the PDF by 8.
- Copyright: the references are paraphrases and operational syntheses, with rare, short verbatim quotes (< 15 words). The book is distributed under a BSD-like license (section 7 of the Introduction, TLDP p.11-12).
