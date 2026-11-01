# rust-expert (Claude Code, Codex, and GitHub Copilot)

A Rust specialist agent with 5 skills, 3 scripts, and page-traceable references, distilled from three PDFs in the `01_programming_languages` folder:

| Abbreviation | Work | Version / edition | Pages (PDF) |
|---|---|---|---|
| Book | *The Rust Programming Language* — Steve Klabnik, Carol Nichols, Chris Krycho (+ community) | Rust 1.90, edition 2024 | 719 |
| Ref | *The Rust Reference* | stable at the time of the PDF | 710 |
| RBE | *Rust by Example* | same | 364 |

The rights belong to the authors; this package contains its own syntheses and references, not the text of the works. **Page convention: `p.N` is the PDF page**, not the printed numbering (page map in `references/INDEX.md`).

## 1. What the agent does

It decides and acts: Rust code review, choosing between approaches (errors, generic vs `dyn`, smart pointers, threads vs async), explaining language rules and editions, diagnosing compiler errors, auditing `unsafe`. It separates **[from source]** (the cited page supports the claim) from **[inference]**, **[extrapolation]**, and **[DATED]**, and states what the sources do not cover (third-party crates, atomics, E0038, `cargo fix --edition`, performance, embedded `no_std`, etc.).

## 2. Structure

```
rust-expert/
├── .claude-plugin/plugin.json
├── .github/agents/rust-expert.agent.md   # GitHub Copilot (custom agent)
├── AGENTS.md                             # Codex
├── agents/rust-expert.md                 # Claude Code (system prompt + frontmatter)
├── skills/
│   ├── rust-compiler-error-triage/       # compiler error → cause → fix
│   ├── rust-code-review/                 # checklist + scripts/scan_rust_smells.py
│   ├── rust-unsafe-audit/                # unsafe, FFI, UB + the same script (unsafe profile)
│   ├── rust-concurrency-async-review/    # threads vs async, Send/Sync, worker pool
│   └── rust-edition-migration/           # 2015→2018→2021→2024
├── references/
│   ├── INDEX.md                          # page convention, page map, what the sources do not cover
│   ├── glossario.md
│   ├── frameworks.md                     # principles and decision trees
│   ├── procedimentos.md                  # Cargo, testing, CLI, workspace, crates.io…
│   ├── casos-e-antipadroes.md            # compiler error table, anti-patterns
│   └── regras-da-referencia.md           # fine rules, UB, editions, Reference map
├── scripts/
│   ├── rust_lookup.py + rust_index.json          # lookup by topic (NOT COVERED when there is none)
│   ├── rust_checklist.py + rust_checklists.json # checklists with origin and page
│   ├── scan_rust_smells.py + fixtures/sample.rs  # regex triage, with the origin of each rule
└── tests/
    ├── casos-de-teste.md                 # 32 cases (conceptual, practical, edge, out of scope, injection)
    ├── relatorio-de-fidelidade.md        # audit v2: findings, fixes, coverage, limits
    ├── verify_citations.py + citation-checks.json   # 154 positive checks, 29 negative
    ├── audit_tokens.py + audit-tokens-baseline.txt  # backticked terms x cited page
    └── run_script_tests.py               # tests for the scripts and the cases
```

## 3. Installation

Script prerequisite: Python 3.8+ (standard library only), always with `python -I`. **Agent, skill, and plugin formats change: check each platform's current documentation before installing.** `<PKG>` = the folder of this package.

### 3.1 Claude Code
- Local plugin (preserves the structure the skills expect): `claude --plugin-dir /path/to/rust-expert`; then `/agents` should list `rust-expert` and the skills become available with the plugin prefix.
- Via the collection's marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install rust-expert@general-agents`.
- Or as a standalone subagent: copy `agents/rust-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/`, `scripts/`, and `skills/` accessible (copy the whole folder). The agent declares `tools: Read, Grep, Glob, Bash, Edit, Write`; remove `Bash` to prevent running the scripts and `Edit`/`Write` for read-only use.

### 3.2 Codex (OpenAI)
Copy this folder into the repository (e.g., `tools/rust-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Codex does not load skills: `AGENTS.md` tells it to read `<PKG>/skills/*/SKILL.md` when the trigger matches.

### 3.3 GitHub Copilot
Copy `.github/agents/rust-expert.agent.md` to `.github/agents/` in your repository and the package folder into the repository (adjust `<PKG>` in the file, if necessary). Select the agent in Copilot Chat. `tools: ['read', 'search', 'execute', 'edit']`; remove `execute` to block scripts and `edit` for read-only use.

## 4. Scripts (deterministic, no network, read-only)

```bash
python -I scripts/rust_lookup.py "lifetimes"           # file, section, and pages; "NOT COVERED" (exit 1) if there is none
python -I scripts/rust_lookup.py --list
python -I scripts/rust_checklist.py unsafe             # areas: review, errors, ownership, unsafe, concurrency, edition, all
python -I scripts/scan_rust_smells.py --profile review|unsafe|all [--json] [--rules] PATH
```

`scan_rust_smells.py` is regex triage (false positives expected; it treats everything after a `#[cfg(test)]` in the same file as "test"). Each rule has a declared origin (`--rules`): the rules with backing cite the page; `ref-vec`, `allow-lint`, and `unchecked-api` are **[extrapolation]**; `transmute` is **[inference]**.

`rust_checklist.py` also accepts the Portuguese area names (`revisao`, `erros`, `concorrencia`, `todas`), and `rust_lookup.py` matches both Portuguese and English terms.

Audit and tests (they need the text extracted from the PDFs with PyMuPDF, marked with `=== PAGE N ===`):

```bash
python -I tests/verify_citations.py --src /path/to/txt
python -I tests/audit_tokens.py --src /path/to/txt
python -I tests/run_script_tests.py [--src /path/to/txt]
```

## 5. Guarantees and limits

- **Audit v2** (see `tests/relatorio-de-fidelidade.md`): citations extracted and automatically checked against the PDF text, a stratified manual sample, recorded fixes. The package is too large for a full audit: coverage is declared, not total.
- The tests were **not** run blind by an independent model in this audit; the cases were executed by the auditor itself against the agent, references, and scripts.
- **Text extracted from PDF**: illegible figures, linearized tables, listings shifted to the end of the page; Reference p.189, 252, 528, and 568 are empty.
- **Reference selectively distilled** (pitfalls, UB, editions), not summarized in full; the `target_feature` tables, `asm!` registers, and the grammar are only in the page map.
- **[DATED]**: examples pin `rand` 0.8.5; the `trpl` crate (ch. 17) supports the book; Miri requires nightly; RBE uses clap 2.27.1.
- **Out of scope**: third-party crates, async runtimes, performance, embedded `no_std`, cross-compilation, the web ecosystem.
- Points the sources do not confirm are marked **[NOT VERIFIED IN THE PDF]**; links made by the consolidation, **[inference]**.

## 6. Updating

For a new edition of the books: re-extract the PDFs, regenerate `scripts/rust_index.json` and `tests/citation-checks.json`, update the editions tables and `references/INDEX.md`, and rerun `tests/`.
