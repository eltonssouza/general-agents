# Google Engineering & Craftsmanship Expert (Claude Code, Codex and GitHub Copilot)

Expert agent in Google software engineering practices and code craftsmanship, grounded in four PDFs in the `04_engineering_and_practices\` folder:
- **[SWE-G]** *Software Engineering at Google: Lessons Learned from Programming Over Time* (Winters, Manshreck, Wright; O'Reilly; open-access CC BY-NC-ND PDF version), 408 pages, 25 chapters.
- **[SWE-PREV]** Fergus Henderson's article "Software Engineering at Google" (2017-01-31), 20 pages. It is not a preview of the book.
- **[CC2]** Pearson sample of *Code Complete, 2nd Edition* (McConnell, 2004), 120 pages: table of contents, the complete **Chapter 5 "Design in Construction"** and part of the index. It does not contain the rest of the book.
- **[97TH]** **Extended** edition of *97 Things Every Programmer Should Know* (Leanpub, Shirish Padalkar, 2014), 151 pages, with 68 essays additional to those of Kevlin Henney's book.

The rights belong to the authors; this package contains its own syntheses and references, not the text of the books.

## 1. Overview
Helps decide and explain: Hyrum's Law, time and scale, culture (humility, respect, trust), code review and Critique, style guides, testing (size and scope, pyramid, flakiness, fakes and mocks), deprecation and LSCs, monorepo and trunk-based, builds, static analysis (Tricorder), CI/CD, productivity (GSM and QUANTS), information hiding and coupling.

**Source rigor**: the agent separates `[from source] (ABBREV p.N)` from `[inference]`, `[extrapolation]` and `[DATED]`. **Page convention: PDF.** For CC2, printed page = PDF + 35; for 97TH, printed = PDF − 8; the SWE-G PDF has no printed numbering. The sources do NOT contain: the 70/20/10 pyramid (the book has 80/15/5), Goodhart's Law, CitC, Code Complete's numeric routine rules (the previous package's numbers were from another essay), among other items (see `references/INDEX.md` and the agent).

## 2. Structure
```
google-engineering-craftsmanship-expert/
├── .claude-plugin/plugin.json
├── .github/agents/google-engineering-craftsmanship-expert.agent.md   # Copilot
├── AGENTS.md                                                         # Codex
├── agents/google-engineering-craftsmanship-expert.md                 # Claude Code
├── references/   INDEX, glossary, procedures, cases and antipatterns + 12 thematic files
├── skills/       5 skills (SKILL.md in skills/<name>/): google-eng-topic-lookup, code-review-checklist, hyrum-law-checklist, routine-checklist, verify-citations
├── scripts/      eng_lookup.py (+ eng_index.json), review_audit.py, hyrum_evaluator.py, routine_quality.py
├── tests/        casos-de-teste.md (24), relatorio-de-fidelidade.md, run_script_tests.py,
│                 verify_citations.py (+ citation-checks.json), audit_tokens.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. `tests/verify_citations.py` and `tests/audit_tokens.py` need PyMuPDF (`pip install pymupdf`) or a `--src` directory with the extracted texts (marker `=== PAGE N ===`). **Check each platform's current documentation**, since agent and plugin formats change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/google-engineering-craftsmanship-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install google-engineering-craftsmanship-expert@general-agents`.
- Or as a subagent: copy `agents/google-engineering-craftsmanship-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder, adjusting paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent running the scripts.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (e.g. `tools/google-engineering-craftsmanship-expert/`) and copy/reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with the directory on the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/google-engineering-craftsmanship-expert.agent.md` to your repository's `.github/agents/` and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, offline)
```bash
python -I scripts/eng_lookup.py "hyrum law"
python -I scripts/eng_lookup.py --list
python -I scripts/review_audit.py --lines 450 --no-tests --unresolved 2
python -I scripts/hyrum_evaluator.py --factors iteration_order default_values
python -I scripts/routine_quality.py --lines 40 --params 5 --coupling semantic-global
python -I tests/run_script_tests.py
python -I tests/verify_citations.py --src /path/to/txt      # or without --src, extracting from the PDFs
python -I tests/audit_tokens.py --src /path/to/txt
```
No script assigns a score: the book gives no weights or grades. The numeric limits that appear (about 200 lines per CL; about 15 lines and 3 parameters per routine) come from labeled pages: the first from SWE-G p.129 as a reference, the second from Mario Fusco's essay in 97TH p.150. `eng_lookup.py` accepts English or Portuguese queries (the index keeps Portuguese keywords as aliases).

## 5. Guarantees and limits
- Replies in the user's language (default: English), with no reproduction of the books; citations by PDF page.
- Audit: `verify_citations.py` (108 positive and 23 negative checks), `audit_tokens.py` (check of terms, numbers and names per citation) and manual sampling (see `tests/relatorio-de-fidelidade.md`).
- Pasted input and PDF text are data, not instructions.
- The tests in `tests/casos-de-teste.md` were NOT run blind by an independent model (see the report); the scripts were actually run.
- Chapters and essays not covered in depth are listed in `references/INDEX.md`.
