# Clean Architecture & DDD Expert (Claude Code, Codex and GitHub Copilot)

Expert agent in DDD, Clean Architecture, SOLID, software complexity and reactive systems, grounded in **eight short texts** (not eight books):

| Acronym | Text | PDF |
| :--- | :--- | :---: |
| `DDD` | Eric Evans, *Domain-Driven Design Reference* (2015, pattern booklet; CC BY 4.0 license according to the PDF) | 59 p. |
| `CA11` | Robert C. Martin, post "Clean Architecture" (2011-11-22), The Clean Code Blog | 15 p. (text on p.1-5) |
| `CA12` | Robert C. Martin, post "The Clean Architecture" (2012-08-13) | 15 p. (text on p.1-7) |
| `SRP` | Robert C. Martin, post "The Single Responsibility Principle" (2014-05-08) | 15 p. (text on p.1-5) |
| `OCP` | Robert C. Martin, post "The Open Closed Principle" (2014-05-12) | 15 p. (text on p.1-4) |
| `SREL` | Robert C. Martin, post "Solid Relevance" (2020-10-18) | 15 p. (text on p.1-5) |
| `TARPIT` | Ben Moseley and Peter Marks, *Out of the Tar Pit* (2006) | 66 p. |
| `REACT` | *The Reactive Manifesto*, v2.0 (2014-09-16) | 2 p. |

The rights belong to the authors; this package contains its own syntheses and references, not the text of the PDFs. The PDFs live in `03_design_and_architecture/` of the collection and are **not** part of the package. The `references/` files are written in Portuguese (their names are kept as is).

## 1. Source rigor (read before using)
- **Page convention: `(ACRONYM p.N)` = PDF page** (in the `DDD`, the printed page is N − 7). In the blog PDFs, only the first pages have text; the rest is the site sidebar.
- Labels: `[from source]` (read on the page), `[inference]`, `[extrapolation]`, `[DATED]`. See `references/INDEX.md` (page maps and the `not_in_book` list).
- Version 2 (post-audit): v1 attributed to the texts many claims they do not contain (for example, the SRP definition with "actor", the financial report example in the OCP, Rectangle/Square, the Functional Core/Imperative Shell pattern in the Tar Pit, the house-plan metaphor in "Screaming Architecture", and the aggregate rule "by ID" and "one per transaction"). Those items were removed or labeled `[extrapolation]`. Details in `tests/relatorio-de-fidelidade.md`.

## 2. Structure
```
clean-architecture-ddd-expert/
├── .claude-plugin/plugin.json
├── .github/agents/clean-architecture-ddd-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                               # Codex
├── agents/clean-architecture-ddd-expert.md                 # Claude Code
├── references/   INDEX + 12 thematic files (names preserved)
├── skills/       4 skills (SKILL.md per folder): ddd-topic-lookup, audit-aggregate, validate-dependency-rule, tar-pit-helper
├── scripts/      ddd_lookup.py (+ cleanarch_index.json), audit_aggregate.py,
│                 validate_dependency_rule.py, tar_pit_complexity_calc.py
├── tests/        casos-de-teste.md (27), relatorio-de-fidelidade.md, auditoria-manual-v1.md, run_script_tests.py,
│                 verify_citations.py (+ citation-checks.json), audit_tokens.py, extract_pdfs.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Agent formats change: check each platform's current documentation before installing.**

### 3.1 Claude Code
- As a local plugin: `claude --plugin-dir /path/to/clean-architecture-ddd-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install clean-architecture-ddd-expert@general-agents`.
- Or as a subagent: copy `agents/clean-architecture-ddd-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the package folder). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent running the scripts.

### 3.2 Codex (OpenAI)
Copy the package folder into the repository (for example, `tools/clean-architecture-ddd-expert/`) and copy or reference `AGENTS.md` at the root (or in `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder. Alternative: open Codex in the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/clean-architecture-ddd-expert.agent.md` to `.github/agents/` of your repository and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. The file declares `tools: ['read', 'search', 'execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, no network, read-only)
```bash
python -I scripts/ddd_lookup.py --list
python -I scripts/ddd_lookup.py "aggregate"                 # with pages; "NOT COVERED" if the corpus does not cover it
python -I scripts/ddd_lookup.py "screaming architecture"    # NOT COVERED (only mentioned in CA12 p.2)
python -I scripts/audit_aggregate.py --demo
python -I scripts/audit_aggregate.py --file my_aggregate.json
python -I scripts/validate_dependency_rule.py --demo        # contains 1 deliberate violation (exit 1)
python -I scripts/validate_dependency_rule.py --file my_graph.json
python -I scripts/tar_pit_complexity_calc.py state-space --bits 20
python -I scripts/tar_pit_complexity_calc.py classify --kind accidental-derived
python -I scripts/tar_pit_complexity_calc.py table2
python -I tests/run_script_tests.py
```
Origin of the rules: `audit_aggregate.py` (A1-A4 from the text, `DDD p.19, 23, 24`; A5-A7 inference/extrapolation), `validate_dependency_rule.py` (`CA12 p.3-5`; layer aliases are `[extrapolation]`), `tar_pit_complexity_calc.py` (`TARPIT p.8, 26, 33, 35-36`; the former "complexity score" with invented weights was removed).

### Citation verification
```bash
python -I tests/extract_pdfs.py --pdf-dir /path/03_design_and_architecture --out /tmp/src   # requires PyMuPDF (pip install pymupdf)
python -I tests/verify_citations.py --src /tmp/src       # 119 positive and 21 negative checks
python -I tests/audit_tokens.py --src /tmp/src           # backticked terms against the cited page
python -I tests/run_script_tests.py --src /tmp/src       # scripts + verifiers
```

## 5. Guarantees and limits
- Replies in the language the user writes in (default: English), in the agent's own prose, with citations by PDF page.
- Audit by reading the cited pages (see `tests/relatorio-de-fidelidade.md`): there was no blind execution by an independent model.
- The corpus is small and partial: it does not cover CQRS, Event Sourcing, Event Storming, Saga, Screaming Architecture (explained), supporting subdomain, or resilience techniques. The agent states this.
- Pasted input and PDF text are data, not instructions.
