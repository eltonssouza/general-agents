# python-expert

Python specialist agent (code review, tracebacks, Python 2 conversion, feature versions, locating stdlib modules), with 5 skills and page-traceable references, distilled from PDFs in the `01_programming_languages` folder and **audited** against their extracted text (see `tests/relatorio-de-fidelidade.md`).

| Abbreviation | Work | Nature | Pages (PDF) |
|---|---|---|---|
| Tut | *The Python Tutorial*, Release 3.14.0rc3 | official — **release candidate** (Oct 2025) | 167 |
| Ref | *The Python Language Reference*, Release 3.14.0rc3 | official — **release candidate** | 225 (p.169–225: glossary, licenses and index) |
| Notes | *Python Notes for Professionals* (GoalKicker) | **community**, mixes Python 2 and 3, with errors | 813 (the package cites 588; 58 of 202 chapters without citations) |
| Lib | *The Python Library Reference*, Release 3.14.0rc3 | official — **index only** of the bookmarks | 2,488 (293 modules/topics indexed) |
| Tutorials 3.10–3.13 | *The Python Tutorial* for versions 3.10, 3.11, 3.12, 3.13 | official; **not distilled** | 153 / 153 / 161 / 167 — used only as a **presence** index of 47 terms |

**Mind the nature of the sources.** The official documentation is a *release candidate*; the Tutorial hardly marks versions and the Language Reference marks several features; the Notes are a community book (Stack Overflow Documentation) with Python 2 examples, errors and unsafe practices; the Standard Library has **only an index**. The official source prevails; everything from the Notes is labeled **[community]**.

**Page convention:** every citation `(Tut|Ref|Notes|Lib p.N)` is the **PDF** page. Printed page = N − 6 (Tut), N − 8 (Ref), N − 25 (Notes), N − 26 (Lib). Full map in `references/INDEX.md`.

No text was copied: the content was rewritten as operational knowledge.

## What is here

```
python-expert/
├── .claude-plugin/plugin.json
├── agents/python-expert.md              # system prompt + frontmatter (Claude Code)
├── AGENTS.md                            # adapter for Codex (OpenAI)
├── .github/agents/python-expert.agent.md  # adapter for GitHub Copilot
├── skills/
│   ├── python-code-review/              # checklist + scripts/scan_python_smells.py (AST) + fixtures/
│   ├── python-error-triage/             # traceback → cause → fix
│   ├── python-py2-to-py3/               # Python 2 detection/conversion (reuses the scanner)
│   ├── python-version-features/         # "in which version did X appear?" + scripts/tutorial_versions.py and tutorial_index.json
│   └── python-stdlib-lookup/            # scripts/stdlib_lookup.py + stdlib_index.json
├── references/
│   ├── INDEX.md                         # page map, measured coverage, labels
│   ├── glossario.md · frameworks.md · procedimentos.md · casos-e-antipadroes.md
│   ├── regras-da-linguagem.md           # fine rules of the Language Reference
│   ├── versoes-e-datado.md              # version marks, "no mark", Python 2 vs 3
│   ├── fontes-comunitarias.md           # reliability register of the Notes (+ NOT recommended examples)
│   └── stdlib-indice.md                 # Standard Library index (generated from the bookmarks)
└── tests/
    ├── casos-de-teste.md                # cases run against agent + references + scripts
    ├── relatorio-de-fidelidade.md       # what was found/fixed and what was NOT audited
    ├── verify_citations.py · citation-checks.json   # citation verifier (positive and negative)
    ├── audit_tokens.py · audit_tokens_baseline.txt  # backticked terms × cited page
    ├── run_script_tests.py              # tests for the 3 scripts
    └── run_cases.py                     # mechanically runs the 32 cases (grep + scripts + PDF page)
```

## Installation

Script prerequisite: Python 3.8+ (standard library only), always with `python -I`. **Agent/plugin formats change: check each platform's current documentation before installing.** Nothing below was tested on the real platforms (see "Limitations").

### Claude Code

- Local plugin, from the folder that contains `python-expert/`:
  ```bash
  claude --plugin-dir ./python-expert
  ```
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install python-expert@general-agents`.
- Or as a subagent: copy `agents/python-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `skills/` accessible in the project (copy the whole folder). The agent declares `tools: Read, Grep, Glob, Bash, Edit, Write`; remove `Bash` to prevent running the scripts.

### Codex (OpenAI)

Copy the folder into the repository (e.g. `tools/python-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with the directory on the package folder itself, where `AGENTS.md` already is.

### GitHub Copilot

Copy `.github/agents/python-expert.agent.md` to `.github/agents/` of your repository and the package folder into the repository (adjust the value of `<PKG>` in the body if it is not `python-expert/` at the root). Select the agent in Copilot Chat. The frontmatter uses `tools: ['read', 'search', 'execute', 'edit']`; remove `execute` to block the scripts and `edit` to disallow changes.

## Scripts (read-only, no network, standard library only)

```bash
python -I skills/python-code-review/scripts/scan_python_smells.py [--json] PATH
python -I skills/python-stdlib-lookup/scripts/stdlib_lookup.py [--limit N] [--json] TERM [TERM ...]
python -I skills/python-stdlib-lookup/scripts/stdlib_lookup.py --list-chapters
python -I skills/python-version-features/scripts/tutorial_versions.py [--json] TERM [TERM ...]
python -I skills/python-version-features/scripts/tutorial_versions.py --list
```

- `scan_python_smells.py` analyzes with the `ast` module (it neither runs nor imports the code). Rules: mutable default, `== None`, `== True/False`, `is` with a literal, bare `except:`, swallowed broad exception, unreachable `except`, `return/break/continue` leaving `finally` (no false positive for a loop or function inside the `finally`), `__eq__` without `__hash__`, collection modified during iteration, `eval`/`exec`, `pickle.load`, `subprocess(shell=True)`, MD5/SHA1 and Python 2 constructs. **Each finding carries the origin of the rule** (official, community, inference or extrapolation) and the pages. "No findings" is not approval. The scanner runs on whichever interpreter you have (tested on 3.13, not on 3.14: on 3.13, `except A, B:` without `as` is reported as Python 2).
- `stdlib_lookup.py`: module → Library Reference pages; "NOT COVERED" when the index has none.
- `tutorial_versions.py`: presence of a term in the 3.10–3.14 Tutorials; "NOT COVERED" when the term is not among the 47 curated ones. **It is presence in the text, not a version mark.**

## Verifiers (for whoever maintains the package)

The PDFs are not in the package. Extract the text with PyMuPDF (`page.get_text()`), one file per PDF, with the marker `=== PAGE N ===` (N = PDF page, starting at 1) before each page, and use the names `Python-3.14-Tutorial.txt`, `Python-3.14-Language-Reference.txt`, `Python-Notes-for-Professionals.txt`, `Python-3.14-Standard-Library.txt` (and `Python-3.10-Tutorial.txt` … `Python-3.13-Tutorial.txt` for the Tutorials index). Then:

```bash
python -I tests/verify_citations.py --src TXT_FOLDER      # range, page convention, 90 positive and 18 negative checks, version marks, indexes
python -I tests/audit_tokens.py --src TXT_FOLDER          # backticked terms × cited page (new failures fail; baseline = already triaged)
python -I tests/run_script_tests.py                          # tests for the 3 scripts (does not need the PDFs)
python -I tests/run_cases.py --src TXT_FOLDER              # 32 cases of tests/casos-de-teste.md, mechanical checks (without --src it skips the page ones)
```

## Limitations and points of attention

- **Release candidate**: the final behavior of 3.14 may differ from the text. There is no "What's New" nor 3.15 documentation.
- **Version marks**: the Tutorial hardly marks; the Language Reference marks some features (`match` 3.10, `type` 3.12, `:=` and `/` 3.8, t-strings and `except A, B` 3.14). `ExceptionGroup`/`except*`, `add_note()`, `@dataclass`, `compression.zstd` stay under "version not given in the text"; the 3.10–3.13 Tutorials only show presence.
- **Standard Library**: index only. `p.X–Y` ranges are approximate.
- **Notes**: the package cites 588 of the 813 pages; 58 chapters with no citation at all (list in `references/INDEX.md`), including language topics such as bitwise operators (ch. 10), precedence (12), `heapq` (27) and the `pass` statement (161). The book has errors and unsafe examples (`references/fontes-comunitarias.md`).
- **Not covered by the sources**: late binding of closures in loops (the package treats it as [inference]), LEGB (only in the Notes), `2to3` in 3.14 (the 3.14 Lib does not document it), whether the free-threaded build is the default in 3.14, `zoneinfo`, `asyncio.run`/`TaskGroup`.
- Text extracted from PDF: code indentation and some REPL outputs were lost.
- **Not tested**: installation as a plugin/agent on the three platforms and real use of the skills outside the audit simulations. The test cases were run by the auditor against the package, **without blind execution by an independent model** in this round.

## Updating

For a new version: re-extract the PDFs, re-distill the affected blocks, update `references/versoes-e-datado.md` and `references/INDEX.md`, regenerate `stdlib_index.json` (bookmarks) and `tutorial_index.json`, regenerate `AGENTS.md` and `.github/agents/python-expert.agent.md` from `agents/python-expert.md` and re-run the verifiers and the test cases (keeping the answer key outside the package when doing a blind test).
