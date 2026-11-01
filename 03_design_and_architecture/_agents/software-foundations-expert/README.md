# Software Foundations Expert (Claude Code, Codex and GitHub Copilot)

Expert agent in programming and language foundations, grounded in three works (PDFs in `03_design_and_architecture/`, complete and with extractable text):
- **[SICP]** Abelson and Sussman with Julie Sussman, *Structure and Interpretation of Computer Programs*, 2nd ed. (MIT Press, 1996). 634-page PDF (online edition).
- **[TAUP]** Eric S. Raymond, *The Art of Unix Programming* (2003). 549-page PDF.
- **[CI]** Robert Nystrom, *Crafting Interpreters* (web edition capture). 630-page PDF; **chapter 9 (Control Flow) is not in the PDF**.

The rights belong to the authors; this package contains its own syntheses and references, not the text of the books.

## 1. Overview
Helps explain, review and implement: substitution and environment models, `set!` and referential transparency, data abstraction and data-directed programming, concurrency and streams, evaluators (metacircular, lazy, `amb`), the 17 Unix rules, textuality, IPC and minilanguages, and interpreter construction (scanner, AST, Visitor, parser, resolver, bytecode VM, Pratt, closures and upvalues, garbage collection, NaN boxing).

**Source rigor**: every claim attributed to a book carries `[from source] (SIGLA p.N)`; the rest is `[inference]`, `[extrapolation]` or `[DATED]`. **Page convention: PDF** (in TAUP, printed page = PDF − 2; SICP and CI have no printed numbering in the PDF). The full map and the `not_in_book` list are in `references/INDEX.md`.

## 2. Structure
```
software-foundations-expert/
├── .claude-plugin/plugin.json
├── .github/agents/software-foundations-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                             # Codex
├── agents/software-foundations-expert.md                 # Claude Code (full prompt)
├── references/   INDEX (page map) + 11 topical files + casos-e-antipadroes, procedimentos, glossario
├── scripts/      foundations_lookup.py (+ foundations_index.json), evaluator_trace.py,
│                 unix_philosophy_checker.py, compiler_pipeline_audit.py
├── skills/       5 skills (<name>/SKILL.md; procedure using the package scripts)
├── tests/        casos-de-teste.md (30), relatorio-de-fidelidade.md, run_script_tests.py,
│                 verify_citations.py (+ citation-checks.json), audit_tokens.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**: agent formats and locations change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/software-foundations-expert`.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install software-foundations-expert@general-agents`.
- Or as a subagent: copy `agents/software-foundations-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the whole folder and adjust the paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (for example `tools/software-foundations-expert/`) and copy or reference `AGENTS.md` at the root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with the working directory in the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/software-foundations-expert.agent.md` to `.github/agents/` in your repository and the package folder into the repository (adjust `<PKG>` in the text if needed). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block script execution.

## 4. Scripts (deterministic, no network; each header declares the origin of the rules)
```bash
python -I scripts/foundations_lookup.py "substitution model"
python -I scripts/foundations_lookup.py --book SICP "dynamic scoping"      # NOT COVERED (boundary)
python -I scripts/foundations_lookup.py --not-in-book
python -I scripts/evaluator_trace.py --mode substitution --expr "(f 5)" --order normal
python -I scripts/evaluator_trace.py --mode orders
python -I scripts/evaluator_trace.py --mode mutable_breakdown
python -I scripts/evaluator_trace.py --mode environment
python -I scripts/unix_philosophy_checker.py --preset chatty_cli
python -I scripts/unix_philosophy_checker.py --set silent_on_success=1,pipe_friendly=1
python -I scripts/compiler_pipeline_audit.py --topic treewalk_vs_bytecode
python -I scripts/compiler_pipeline_audit.py --topic gc_architecture
python -I tests/run_script_tests.py
python -I tests/run_script_tests.py --src /path/to/folder/with/sicp.txt+taup.txt+ci.txt
```
Origin of the rules: the `foundations_lookup.py` index is curated and checked against the pages (each entry has `verify` terms); the `evaluator_trace.py` reducer is **ours** (`[extrapolation]`), over the SICP rules at p.29-31 and p.224-227; in `unix_philosophy_checker.py` the rules and pages are from TAUP, but **questions, weights and scoring are ours**; in `compiler_pipeline_audit.py` each line has origin `[from source]` with a page or `[inference]`.

## 5. Audit and verification
The PDF text is not shipped in the package. To reproduce the audit, extract the text of each PDF with `=== PAGE N ===` markers (N = PDF page), for example with PyMuPDF (`page.get_text()`), into `sicp.txt`, `taup.txt` and `ci.txt` in one folder, and run:
```bash
python -I tests/verify_citations.py --src /pasta -v     # 171 positive, 19 negative, index, ranges
python -I tests/audit_tokens.py --src /pasta             # backticked terms against the cited pages
```
Result of the last run and what was NOT audited: `tests/relatorio-de-fidelidade.md`.

## 6. Guarantees and limits
- Replies in the user's language (default: English), without reproducing the book; citations by page (PDF).
- Version 1 of the package cited pages from memory: of the 140 curated page claims, only 55 matched; 70 were on the wrong page and 15 had no basis or were exaggerations. Version 2 was recomputed page by page (see the report).
- Pasted input and PDF text are data, not instructions.
- The test cases were run against the agent, the references and the scripts by the auditor itself, **not** by an independent model blind (see the report).
- PDF diagrams are not in the extracted text; CI ch. 9 is not in the PDF.
