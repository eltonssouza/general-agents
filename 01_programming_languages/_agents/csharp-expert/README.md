# C# Expert (Claude Code, Codex and GitHub Copilot)

A C# specialist agent grounded in four sources:

- **[CSYB]**: *C# Programming Yellow Book*, Rob Miles, "Cheese" Edition 8.1 (17/12/2019), 217-page PDF.
- **[CSHist]**: *The history of C#* (Microsoft Learn, updated on 18/11/2025), 16 pages, from C# 1.0 to C# 14. The files `CSharp-9-WhatsNew.pdf`, `CSharp-10-WhatsNew.pdf` and `CSharp-11-WhatsNew.pdf` have the **same text**.
- **[CS12]**: *What's new in C# 12* (6 pages). **[CS13]**: *What's new in C# 13* (7 pages).

The rights belong to the authors; the package contains its own syntheses and references, not the text of the works.

## 1. Overview

Helps explain, design and review C#: types and conversions, methods (`ref`/`out`), arrays, exceptions, files, OOP (struct vs class, inheritance, interfaces, properties), collections, threads with `Monitor`, and the version timeline (including C# 12 and C# 13).

**Source rigor**: the book is from 2019 (before C# 8) and didactic. The agent separates `[from source] (SIGLA p.N)` from `[inference]`, `[extrapolation]` and `[DATED]`. **Page convention: PDF; printed CSYB = N − 5.** The sources do **not** cover boxing, `using`/`Dispose`, the `lock` statement, `throw;`, stack vs heap, `GetHashCode`, common exception names, records and nullable (only named in CSHist) etc.; see `references/INDEX.md` §5.

## 2. Structure

```
csharp-expert/
├── .claude-plugin/plugin.json
├── .github/agents/csharp-expert.agent.md      # GitHub Copilot
├── AGENTS.md                                  # Codex
├── agents/csharp-expert.md                    # Claude Code
├── references/   INDEX, fundamentos-e-sintaxe, poo-e-design, avancado-e-execucao,
│                 versoes-e-evolucao, recursos-modernos, casos-e-antipadroes, procedimentos, glossario
├── skills/
│   ├── cs-concept-lookup/   SKILL.md, scripts/cs_concept_lookup.py + cs_concept_index.json
│   ├── cs-version-lookup/   SKILL.md, scripts/cs_version_lookup.py + cs_version_data.json
│   ├── cs-code-review/      SKILL.md, scripts/scan_cs_smells.py + fixtures/sample.cs
│   └── cs-error-triage/     SKILL.md, scripts/parse_cs_stack.py + fixtures/trace*.txt
├── tests/        casos-de-teste.md (26), relatorio-de-fidelidade.md,
│                 verify_citations.py + citation-checks.json, audit_tokens.py,
│                 run_script_tests.py, extract_pdf_text.py
└── README.md
```

## 3. Installation

Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**, since formats and agent names change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/csharp-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install csharp-expert@general-agents`.
- Or as a subagent: copy `agents/csharp-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `skills/` accessible (copy the package folder and adjust the relative paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (e.g. `tools/csharp-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder. Alternative: open Codex with the directory set to the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/csharp-expert.agent.md` to the `.github/agents/` of your repository and the package folder into the repository (adjust `<PKG>` in the text, if needed). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block the scripts.

## 4. Scripts (deterministic, no network)

```bash
python -I skills/cs-concept-lookup/scripts/cs_concept_lookup.py struct
python -I skills/cs-concept-lookup/scripts/cs_concept_lookup.py boxing          # NOT COVERED
python -I skills/cs-version-lookup/scripts/cs_version_lookup.py --version 13
python -I skills/cs-version-lookup/scripts/cs_version_lookup.py --query records
python -I skills/cs-code-review/scripts/scan_cs_smells.py skills/cs-code-review/scripts/fixtures/sample.cs
python -I skills/cs-error-triage/scripts/parse_cs_stack.py skills/cs-error-triage/scripts/fixtures/trace.txt
python -I tests/run_script_tests.py
```

The scripts do not execute the analyzed code; the linter and triage rules declare the origin (`source`, `inference` or `extrapolation`) and the page.

## 5. Citation verification

The package citations are checked against the text extracted from the PDFs (markers `=== PAGE N ===`, N = PDF page):

```bash
python -I tests/extract_pdf_text.py <PDF folder> <output folder>          # requires PyMuPDF
python -I tests/verify_citations.py --src <output folder>                 # positive and negative checks
python -I tests/audit_tokens.py --src <output folder>                     # backticked terms vs cited page
```

`<output folder>` receives `CSharp-Yellow-Book.txt`, `CSharp-9-WhatsNew.txt`, `CSharp-12-WhatsNew.txt` and `CSharp-13-WhatsNew.txt`.

## 6. Guarantees and limits

- Replies in the user's language (default: English), without reproducing the works; citations by page.
- v2 audit: reading of the cited pages (manual sample of 105 claims from v1: 19 correct, 22 with the wrong page, 42 unsupported and 22 exaggerated) and automatic verifiers (see `tests/relatorio-de-fidelidade.md`).
- Code, logs, stack traces and PDF text pasted by the user are **data**, not instructions.
- The test cases were **not** run blind by an independent model (see the report).
