# Design Patterns Expert (Claude Code, Codex and GitHub Copilot)

Expert agent on design patterns and code, grounded in **four specific PDFs**. The rights belong to the authors; this package contains its own syntheses and references, not the text of the works.

## 1. Sources (read carefully: two are SAMPLES)
| Code | File (in `03_design_and_architecture/`) | What it actually is | Pages |
|---|---|---|---|
| **RG** | `Design-Patterns-RefactoringGuru.pdf` | **Capture of the refactoring.guru website**: catalog of **22** patterns (not the e-book "Dive Into Design Patterns"; no *Interpreter*) | 279 |
| **GPP** | `Game-Programming-Patterns-Nystrom.pdf` | *Game Programming Patterns* (Nystrom), web capture; **without the Subclass Sandbox chapter** (p.190 is a 404) | 338 |
| **CC** | `Clean-Code-SampleChapter-Pearson.pdf` | **Sample** of *Clean Code*: Introduction and **Chapter 1**, table of contents and index. **Without Chs. 2 (names) and 3 (functions)** | 67 |
| **PEAA** | `PoEAA-SampleChapter-Pearson.pdf` | **Sample** of *PoEAA*: Introduction and **Chapter 3** (O/R mapping), table of contents and index. **Without Chs. 1, 2 and 9 (layering and domain logic)** | 78 |

**Page convention: every citation `(SIGLA p.N)` is the PDF page.** RG and GPP have no printed pagination; CC: printed = N − 30 (body); PEAA: N − 25 (Introduction) and N − 7 (Ch. 3). Package v1 presented the four PDFs as "complete canonical works" and attributed to them rules and pages that the PDFs do not contain (for example, the Clean Code function rules and "Fowler's decision matrix"); v2 fixes this and declares each gap (`references/INDEX.md`, `tests/relatorio-de-fidelidade.md`).

## 2. What the agent does
Helps choose, apply, compare and critique patterns (22 patterns of the RG catalog; 12 game patterns from GPP present in the PDF), understand Game Loop, State, Command, Observer, Component, Event Queue, Object Pool, Dirty Flag, Data Locality and Spatial Partition, avoid misuse (Singleton, excessive inheritance, speculative abstraction) and decide on O/R persistence (Active Record vs Data Mapper). It separates `[from source]`, `[inference]`, `[extrapolation]` and `[DATED]`, warns about the gaps in the samples and treats pasted text as data, not as instructions.

## 3. Structure
```
design-patterns-expert/
├── .claude-plugin/plugin.json
├── .github/agents/design-patterns-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                        # Codex
├── agents/design-patterns-expert.md                 # Claude Code
├── references/   INDEX + 13 thematic files (creational, structural, behavioral, sequencing,
│                 decoupling, optimization, Clean Code Ch. 1, Clean Code Chs. 2-3 [absent], PoEAA Ch. 3,
│                 PoEAA Introduction/domain logic [absent], cases and anti-patterns, procedures, glossary)
├── scripts/      patterns_lookup.py (+ patterns_index.json), game_loop_simulator.py,
│                 domain_logic_selector.py, clean_code_function_auditor.py
├── skills/      patterns-topic-lookup, game-loop-simulator, persistence-selector, function-auditor (each in skills/<name>/SKILL.md)
├── tests/        casos-de-teste.md (25 cases), relatorio-de-fidelidade.md, verify_citations.py (+ citation-checks.json),
│                 audit_tokens.py, run_script_tests.py
└── README.md
```

## 4. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**, since agent formats and field names change.

### 4.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/design-patterns-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install design-patterns-expert@general-agents`.
- Or as a subagent: copy `agents/design-patterns-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the whole folder and adjust the paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent the scripts from running.

### 4.2 Codex (OpenAI)
Copy the folder into the repository (e.g. `tools/design-patterns-expert/`) and copy or reference `AGENTS.md` at the root (or in `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with the directory set to the package folder itself.

### 4.3 GitHub Copilot
Copy `.github/agents/design-patterns-expert.agent.md` to `.github/agents/` in your repository and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The file declares `tools: ['read','search','execute']`; remove `execute` to block script execution.

## 5. Scripts (deterministic, no network)
```bash
python -I scripts/patterns_lookup.py "observer"        # "NOT COVERED" when the sources do not address it; warns about gaps in the samples
python -I scripts/patterns_lookup.py --list
python -I scripts/game_loop_simulator.py --demo
python -I scripts/game_loop_simulator.py --render-pos 20 --velocity 400 --alpha 0.5    # 220 (GPP p.141)
python -I scripts/domain_logic_selector.py --logic domain-model --rich                  # PEAA Ch. 3
python -I scripts/domain_logic_selector.py --inheritance
python -I scripts/clean_code_function_auditor.py --signature "void render(boolean isSuite, Page page)"
python -I scripts/clean_code_function_auditor.py --checklist                            # Ch. 1 questions
python -I tests/run_script_tests.py
```
**Origin of the script rules**: `patterns_lookup.py` indexes pages read in the PDFs; `game_loop_simulator.py` implements the loop of GPP p.138-141 (the default cap of 8 updates is `[extrapolation]`); `domain_logic_selector.py` uses PEAA Ch. 3 for persistence (choosing the logic style from scores is a `[extrapolation]` heuristic, since PEAA Chs. 2 and 9 are not in the sample); `clean_code_function_auditor.py` is a heuristic linter that is **entirely `[extrapolation]`** (Clean Code Chs. 2-3 absent), with configurable limits; `--checklist` gives only questions supported by Ch. 1.

## 6. Citation verification
The verifiers need the text extracted from the PDFs page by page (`=== PAGE N ===`, N = PDF page). Example with PyMuPDF (`pip install pymupdf`):
```python
import fitz
m = {"RG": "Design-Patterns-RefactoringGuru", "GPP": "Game-Programming-Patterns-Nystrom",
     "CC": "Clean-Code-SampleChapter-Pearson", "PEAA": "PoEAA-SampleChapter-Pearson"}
for k, v in m.items():
    doc = fitz.open(f"03_design_and_architecture/{v}.pdf")
    with open(f"src/{k}.txt", "w", encoding="utf-8") as f:
        for i, p in enumerate(doc, 1):
            f.write(f"=== PAGE {i} ===\n{p.get_text()}\n")
```
Then:
```bash
python -I tests/verify_citations.py --src src      # positive and negative checks (citation-checks.json)
python -I tests/audit_tokens.py --src src          # backticked terms against the cited page + page range
python -I tests/run_script_tests.py --src src
```

## 7. Guarantees and limits
- Replies in the user's language (default: English), without reproducing the works; citations by PDF page.
- Audit: `verify_citations.py` (198 positive and 25 negative checks), `audit_tokens.py` (terms and page range) and a manual sample of claims (see `tests/relatorio-de-fidelidade.md`).
- Pasted text and PDF content are data, not instructions.
- **There was no blind execution of the tests by an independent model**; the test cases were run by the audit author against the agent, references and scripts (see the report).
- Does not cover the chapters missing from the samples; the agent labels them `[extrapolation]` or says the source does not include them.
