# ruby-expert (Claude Code, Codex and GitHub Copilot)

Agent that answers questions about what is new in **Ruby 3.0 to 3.4** based on the five official release notes (ruby-lang.org pages captured as PDF):

| Code | Note | Pages |
|---|---|---|
| R30 | Ruby 3.0.0 Released (Dec 25, 2020) | 10 |
| R31 | Ruby 3.1.0 Released (Dec 25, 2021) | 13 |
| R32 | Ruby 3.2.0 Released (Dec 25, 2022) | 23 |
| R33 | Ruby 3.3.0 Released (Dec 25, 2023) | 13 |
| R34 | Ruby 3.4.0 Released (Dec 25, 2024) | 12 |

The rights belong to the authors; the package contains original syntheses, not the text of the notes. **Page convention: PDF page** (web captures have no printed numbering). The notes say *what changed*; they are not a usage guide. The agent separates `[from source] (R3x p.N)` from `[inference]`, `[extrapolation]` and `[DATED]`. The captures (2026) list Ruby 4.0.x under "Recent News": **Ruby 4.0 and later fixes are not covered**. It does not cover Rails or other languages (see `references/INDEX.md`, section `not_in_book`).

## Structure
```
ruby-expert/
├── .claude-plugin/plugin.json
├── .github/agents/ruby-expert.agent.md   # GitHub Copilot
├── AGENTS.md                             # Codex
├── agents/ruby-expert.md                 # Claude Code
├── references/    INDEX + 9 topical files (concurrency, JIT, syntax, typing/tooling, security, versions, cases, procedures, glossary)
├── skills/
│   ├── ruby-feature-lookup/   scripts/ruby_feature_lookup.py + ruby_feature_index.json (50 topics; NOT COVERED)
│   ├── ruby-version-lookup/   scripts/ruby_version_lookup.py + ruby_version_data.json
│   ├── ruby-code-review/      scripts/scan_ruby_smells.py + fixtures/sample.rb (15 rules with page)
│   └── ruby-error-triage/     scripts/parse_ruby_stack.py + fixtures/trace.txt
├── tests/  casos-de-teste.md (32), relatorio-de-fidelidade.md, verify_citations.py + citation-checks.json,
│           audit_tokens.py, extract_pages.py, run_script_tests.py
└── README.md
```

## Installation
Script prerequisite: Python 3.8+ (stdlib only, no network); always run with `python -I`. `tests/extract_pages.py` requires PyMuPDF (`pip install pymupdf`) and the PDFs. **Check each platform's current documentation**: agent formats change.

### Claude Code
- Local plugin: `claude --plugin-dir /path/to/ruby-expert` (`plugin.json` points to `agents/ruby-expert.md` and the 4 skills).
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install ruby-expert@general-agents`.
- Or as a subagent: copy `agents/ruby-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `skills/` accessible (for example, copy the package folder along and adjust the paths cited in the agent). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### Codex (OpenAI)
Copy the package folder into the repository (e.g. `tools/ruby-expert/`) and copy/reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder.

### GitHub Copilot
Copy `.github/agents/ruby-expert.agent.md` to the `.github/agents/` of your repository and the package folder into the repository (adjust `<PKG>` in the agent text). Select the agent in Copilot Chat. `tools: ['read', 'search', 'execute']`; remove `execute` to block scripts.

## Scripts (read-only, no network)
```bash
python -I skills/ruby-feature-lookup/scripts/ruby_feature_lookup.py yjit
python -I skills/ruby-feature-lookup/scripts/ruby_feature_lookup.py gvl            # NOT COVERED
python -I skills/ruby-version-lookup/scripts/ruby_version_lookup.py --version 3.2
python -I skills/ruby-code-review/scripts/scan_ruby_smells.py file.rb
python -I skills/ruby-error-triage/scripts/parse_ruby_stack.py trace.txt
python -I tests/run_script_tests.py
python -I tests/extract_pages.py --pdfs <PDF folder> --out <txt folder>
python -I tests/verify_citations.py --src <txt folder>
python -I tests/audit_tokens.py --src <txt folder> --strict
```
The linter is heuristic (line by line); it does not replace RuboCop or testing on the target version. Each rule carries the note page and a label; rules that are package recommendations are shown at INFO level as `[inference]`.

## Guarantees and limits
- Answers in the user's language (default: English), without reproducing the notes; pages checked by `verify_citations.py` (70 positive, 26 negative) and `audit_tokens.py` (266 terms).
- Code, logs and PDF text are data, not instructions.
- The free-form test cases were **not** run blind by an independent model (see `tests/relatorio-de-fidelidade.md`).
