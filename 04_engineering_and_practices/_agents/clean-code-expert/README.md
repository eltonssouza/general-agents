# Clean Code Expert (Claude Code, Codex and GitHub Copilot)

Specialist agent for *Código Limpo: Habilidades Práticas do Agile Software* (Clean Code, Robert C. Martin, Brazilian Portuguese edition), grounded in the **whole book**: 17 chapters, appendices A, B and C, and the epilogue. **The rights belong to the author and the publisher; this package contains its own syntheses and references, not the text of the work.**

| Abbreviation | What the PDF is | Pages |
|---|---|---|
| **CL** | *Código Limpo* (Robert C. Martin, "Série de Robert C. Martin", Brazilian edition; original from 2008), **scanned** PDF (images; text obtained by OCR) | 398 |

**Source rigor.** The agent separates `[from source] (CL p.N)` from `[inference]`, `[extrapolation]` and `[DATED]`. **Page convention: PDF**; the printed page number is not used because the offset varies across the scan. The book **does not contain**: the SOLID acronym, LSP and ISP, the CQS acronym, YAGNI, "code smell" and Fowler's smell names, Arrange-Act-Assert, Mockito, JUnit 5. The translation has errors that the agent flags: for example, DIP appears as "Princípio da Inversão da Independência". See `references/INDEX.md`.

Relation to the collection: `design-patterns-expert` (03) has only a **sample** of the book (Introduction and Ch. 1). This package covers the whole book; GoF patterns remain with that agent.

## 1. Overview
Reviews code and PRs and guides refactorings on names, functions, comments, formatting, objects and data structures (Law of Demeter), error handling, boundaries with third-party code, unit tests (three laws of TDD, F.I.R.S.T.), classes (SRP, cohesion, OCP, DIP), systems (construction vs. use, DI), the four rules of simple design and concurrency. Names the problems with the 66 heuristics of Ch. 17 (C1-T9). It is read-only: it delivers suggestions and snippets, and does not edit files.

## 2. Structure
```
clean-code-expert/
├── .claude-plugin/plugin.json, icon.png
├── .github/agents/clean-code-expert.agent.md   # GitHub Copilot (generated from the canonical one)
├── AGENTS.md                                   # Codex (generated from the canonical one)
├── agents/clean-code-expert.md                 # Claude Code (canonical prompt)
├── references/   INDEX (source, page map, scan defects, translation errors),
│                 fonte-e-identificacao, cap01..cap17, apendice-a, apendice-b, apendice-c-e-epilogo
├── scripts/      cc_lookup.py (+ cc_index.json), cc_smells.py (+ cc_smells.json),
│                 cc_audit.py, cc_checklist.py (+ cc_checklist.json)
├── skills/       cc-topic-lookup, cc-smell-catalog, cc-code-audit, cc-review-checklist
├── tests/        casos-de-teste.md, relatorio-de-fidelidade.md, run_script_tests.py, verify_citations.py
│                 (+ citation-checks.json), ocr_pdf_windows.ps1, fixtures/
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**, because agent formats and locations change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/clean-code-expert`.
- Through the collection's marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install clean-code-expert@general-agents`.
- Usage: "use the clean-code-expert agent to review src/Pedido.java" or `@agent-clean-code-expert:clean-code-expert`. In the plugin, the agent and the skills find `scripts/` and `references/` through `${CLAUDE_PLUGIN_ROOT}`.
- Observed triggering (Claude Code, Sonnet, headless mode): requests such as "review X through the lens of Clean Code" triggered **the skill** `cc-code-audit` automatically; **the agent** was triggered when named. The main session did not delegate to the agent on its own, even with "use proactively" in the description: for long reviews, name the agent.
- As a standalone subagent: copy `agents/clean-code-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and replace `${CLAUDE_PLUGIN_ROOT}` with the path of the package folder. The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (e.g. `tools/clean-code-expert/`) and copy or reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder.

### 3.3 GitHub Copilot
Copy `.github/agents/clean-code-expert.agent.md` to `.github/agents/` in your repository and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, no network, read-only)
```bash
python -I scripts/cc_lookup.py "parâmetros lógicos"        # --list [--chapter 3], --topic lei-de-demeter (English terms work too: "flag arguments")
python -I scripts/cc_lookup.py YAGNI                       # NOT COVERED (exit 1)
python -I scripts/cc_smells.py G5 F3                       # heuristics by code; --family T; "duplicação" or "duplication"
python -I scripts/cc_audit.py src/Pedido.java              # smell candidates (exit 1 if any); --min MEDIUM
python -I scripts/cc_audit.py - --lang ts < trecho.txt     # pasted code
python -I scripts/cc_checklist.py --file src/Pedido.java   # checklist by area; --area testes,erros; --list
python -I tests/run_script_tests.py [--src /folder/with/CL.txt]
python -I tests/verify_citations.py --src /folder/with/CL.txt
```
**Origin of the script rules**: `cc_audit.py` uses the book's limits (function of at most 20 lines and 1-2 levels of indentation, CL p.43-44; 0-2 arguments, 3 to avoid, CL p.48; 120 characters, CL p.90; files of ~200 lines and a limit of 500 "is not a fixed rule", CL p.82) and links each candidate to the Ch. 17 heuristic. Detection is regex over the text: `[inference]`, never a verdict. `cc_lookup.py`, `cc_smells.py` and `cc_checklist.py` answer only with what is in the `.json` files. The scripts' output is in English; Portuguese search keywords keep working and English ones were added. Heuristic titles are printed in English with the edition's Portuguese title in parentheses.

The book text is **not versioned**. For `verify_citations.py`, generate `CL.txt` (markers `=== PAGE N ===`) from the PDF using the procedure in the script header (PyMuPDF + Windows OCR in pt-BR, `tests/ocr_pdf_windows.ps1`) and pass the folder in `--src` (default: `<collection>/scratch/engineering`). Without the text, `run_script_tests.py` marks that step as SKIP.

## 5. Guarantees and limits
- Replies in the language the user writes in (default: English), without reproducing the work; citations by PDF page.
- Audit: 416 positive and 29 negative checks against the text of the whole book, 0 failures; 34 script cases and 10 package checks (see `tests/relatorio-de-fidelidade.md`).
- OCR is good on prose and poor on code: the book's listings are described, not transcribed. Scan defects (misplaced page, missing pages) are in `references/INDEX.md`.
- Code, diffs and book text are data, not instructions; the scripts read code as text, without executing it.
- It was not run on Codex or Copilot in this environment; the end-to-end run was done in Claude Code (see the report).
