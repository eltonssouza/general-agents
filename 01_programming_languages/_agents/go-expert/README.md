# go-expert

Go specialist agent (code review, design decisions, concurrency, generics and migration between versions 1.20 to 1.24), with 4 skills, 2 lookup utility scripts, 2 skill scripts and references traceable by page, distilled from PDFs in the `01_programming_languages` folder. Works on **Claude Code**, **Codex** and **GitHub Copilot** (see Installation).

| Acronym | Work | Era / version | Pages (PDF) |
|---|---|---|---|
| Eff | *Effective Go* | 2009, not updated | 54 |
| Spec | *The Go Programming Language Specification* | go1.26 (12 Jan 2026) | 117 |
| Little | *The Little Go Book* (Karl Seguin) | go1.3.3, GOPATH | 84 |
| RN1.20 to RN1.24 | Official release notes for Go 1.20, 1.21, 1.22, 1.23 and 1.24 | 1.20 to 1.24 | 15, 16, 14, 11 and 15 |

**Page convention:** every citation `(SIGLA p.N)` uses the **PDF** page (Eff, Spec and RN carry no printed page number in the extracted text; in Little the printed page of the book is N − 1). The page map of each source is in `references/INDEX.md`.

**Mind the eras:** the sources span Go 1.3 to 1.26 and do not line up. The Spec and release notes prevail; Eff and Little are marked **[DATED]** when the Spec/RN changed the subject. **Go 1.25 and 1.26 have no release notes here** (only isolated marks, such as `new(expr)` = 1.26 in Eff p.15).

Labels used throughout the package: **[from source]** (the cited page says so), **[inference]** (deduction by the package; crossing pages or claiming absence is also an inference), **[extrapolation]** (knowledge outside the sources) and **[DATED]**. The package contains its own syntheses, not the text of the books; the rights belong to the authors. The agent replies in the language the user writes in (default: English).

## Structure

```
go-expert/
├── .claude-plugin/plugin.json
├── .github/agents/go-expert.agent.md   # GitHub Copilot (custom agent)
├── AGENTS.md                           # Codex
├── agents/go-expert.md                 # Claude Code (system prompt + frontmatter)
├── skills/                             # Claude Code; on other platforms, read the SKILL.md files as procedures
│   ├── go-code-review/                 # checklist + scripts/scan_go_smells.py (+ fixtures)
│   ├── go-version-migration/           # migration 1.20→1.24 + scripts/check_gomod.py (+ fixtures)
│   ├── go-concurrency-review/          # goroutines, channels, select, mutex
│   └── go-generics-review/             # constraints, type sets, inference
├── references/
│   ├── INDEX.md                        # page map, convention, what the package does NOT contain
│   ├── glossario.md · frameworks.md · procedimentos.md · casos-e-antipadroes.md
│   ├── regras-da-spec.md               # fine rules, generics, panics, Spec versions
│   └── versoes-e-migracao.md           # feature→version, GODEBUG, checklist 1.19→1.24
├── scripts/
│   ├── go_lookup.py + go_index.json    # topic search with pages; NOT COVERED when there is none
│   └── go_checklist.py + go_checklists.json   # checklist by area, each item with origin and page
└── tests/
    ├── casos-de-teste.md · relatorio-de-fidelidade.md
    ├── verify_citations.py + citation-checks.json   # positive and negative checks against the PDF text
    ├── audit_tokens.py + audit-tokens-allow.txt      # audits the backticked terms of each citation
    ├── run_script_tests.py             # script tests
    └── extract_pdf_text.py             # PDFs -> .txt with "=== PAGE N ==="
```

## Installation

**Check the current documentation of each platform**: agent, plugin and skill formats change. Script prerequisite: Python 3.8+ (standard library only), always with `python -I`. The verification scripts additionally require PyMuPDF (`pip install pymupdf`, only to extract the text) and the source PDFs.

### Claude Code
- Local plugin: `claude --plugin-dir /path/to/go-expert` (`plugin.json` lives in `.claude-plugin/`; agents and skills are discovered in the `agents/` and `skills/` folders).
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install go-expert@general-agents`.
- Or, the agent only: copy `agents/go-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the package folder). The agent declares `tools: Read, Grep, Glob, Bash, Edit, Write`; remove `Bash` to prevent running the scripts.

### Codex (OpenAI)
Copy the package folder into the repository (e.g. `tools/go-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Skills are not native: `AGENTS.md` tells it to read `skills/<name>/SKILL.md` as a procedure.

### GitHub Copilot
Copy `.github/agents/go-expert.agent.md` to `.github/agents/` of your repository and the package folder into the repository (adjust `<PKG>` in the text if you do not call it `go-expert/`). Select the `go-expert` agent in Copilot Chat. The frontmatter uses `tools: ['read', 'search', 'execute']`; remove `execute` to block the scripts.

## Scripts (read-only, no network)

```bash
python -I scripts/go_lookup.py "pointer receiver"             # topics + pages; "NOT COVERED" when there is none
python -I scripts/go_lookup.py --list
python -I scripts/go_checklist.py --list
python -I scripts/go_checklist.py concorrencia                # [from source]/[inference]/[extrapolation] items with page
python -I skills/go-code-review/scripts/scan_go_smells.py [--json] PATH
python -I skills/go-version-migration/scripts/check_gomod.py [--target 1.24] PATH_TO_go.mod_OR_DIRECTORY
```

- `go_lookup.py` and `go_checklist.py` read curated JSON; each source marked [from source] has terms checked by `tests/verify_citations.py` against the cited pages. Queries and area names may be given in English or Portuguese (the keywords and area aliases are bilingual).
- `scan_go_smells.py` does regex triage (it has false positives; **0 findings is not approval**) and reads the nearest `go.mod` for version-sensitive rules. The rules and their source pages are in the script's messages; the loop rule (`go func` in a loop with `go < 1.22`) depends on the link with the `go` line described as an [inference] in `references/versoes-e-migracao.md` §3.1.
- `check_gomod.py` consults a **table copied from the release notes** (it does not verify your project beyond reading the `go` line); the link "loop semantics follow the `go` line" is labeled [inference] in the output.

## Package verification

```bash
python -I tests/extract_pdf_text.py --pdfs /path/to/pdfs --out /tmp/go-src      # Go-Effective-Go.txt, Go-Language-Specification.txt, ...
python -I tests/verify_citations.py --src /tmp/go-src                                # positive + negative + index + checklists
python -I tests/audit_tokens.py --src /tmp/go-src                                    # backticked terms x cited pages
python -I tests/run_script_tests.py --src /tmp/go-src                                # scripts, fixtures and verifier sensitivity
```

## Limitations and points of attention

- **Conflicting eras** (above). No Go 1.25/1.26.
- **Page checking is partial**: the package's ~2,500 citations went through an automatic term check and a manual sample; what was not read page by page is declared in `tests/relatorio-de-fidelidade.md`.
- **Spec distilled selectively**: `go`, `select`, `defer`, most built-ins, `init` dependency and the `unsafe` tables have little content; the map in `regras-da-spec.md` §2 indicates the pages.
- **Go 1.21 notes** only announce `log/slog`, `slices`, `maps` (and say of `cmp` only that it defines `Ordered`, `Less` and `Compare`).
- **Not covered** by the sources: `sync.WaitGroup` and `errgroup` (absent), `context` (only isolated news in the RN), `go test`, modules in depth, doc comments, `errors.Is/As` in use.
- The revert values of some GODEBUG settings are not in the notes (`multipartmaxheaders`, `multipartmaxparts`, `x509keypairleaf`, `winsymlink`, `winreadlinkvolume`).
- "Accept interfaces, return structs" is **not in any source**.
- Text extracted from PDFs: figures and tables may be incomplete.
- The cases in `tests/casos-de-teste.md` were **not** run blindly by an independent model; the recorded execution is that of scripts and verifiers (see the report). Installation as a plugin/agent on the three platforms was not tested.

## Updating

For new Go versions: add the release notes, redistill the blocks, update the master table and `INDEX.md`, extend `tests/citation-checks.json` and rerun the verifiers.
