# Data Warehouse, Streaming & Distributed Systems Expert (Claude Code, Codex and GitHub Copilot)

Specialist agent in dimensional modeling and stream processing, grounded in two sources present in the collection:
- **[KIMBALL]**: *Kimball Dimensional Modeling Techniques* (Kimball Group; summary of the techniques from *The Data Warehouse Toolkit*, 3rd ed., 2013), 24-page PDF. Rights belong to the authors; this package contains its own syntheses, not the text.
- **[STREAM]**: *A Survey on the Evolution of Stream Processing Systems* (Fragkoulis, Carbone, Kalavri, Katsifodimos), arXiv:2008.00842v2 (Jan/2023), 30-page PDF.
- **Helland** (*Life Beyond Distributed Transactions*): **absent source**. The collection file `Life-Beyond-Distributed-Transactions.pdf` is actually the astrophysics paper "HD 30963: A new HgMn star" (arXiv:1609.03542). The agent states this, does not cite a page and labels all Helland content as `[extrapolation]`.

## 1. Overview
Helps decide and review: grain, facts and dimensions, surrogate keys, SCD 0-7, bus matrix, drill-across, multipass SQL, centipede; and in streaming: event time, watermarks, state, snapshots, exactly-once (on state vs on output), output commit problem, back-pressure and elasticity.

**Source rigor**: separates `[from source] (SIGLA p.N)` from `[inference]`, `[extrapolation]` and `[DATED]`. **Page convention: PDF.** `KIMBALL`: printed page = N − 3 (cover p.1, table of contents p.2-3). `STREAM`: PDF = printed. The agent states what the collection does **not** provide (tumbling/sliding/session taxonomy, the name "ABS", RocksDB off-heap, Flink/Kafka APIs, Saga/Outbox, Data Vault, lakehouse; see `references/INDEX.md`).

## 2. Structure
```
data-warehouse-streaming-distributed-expert/
├── .claude-plugin/plugin.json
├── .github/agents/data-warehouse-streaming-distributed-expert.agent.md   # GitHub Copilot
├── AGENTS.md                                                              # Codex
├── agents/data-warehouse-streaming-distributed-expert.md                  # Claude Code
├── references/   INDEX, glossary, procedures, cases and anti-patterns + 13 thematic files
├── scripts/      analytics_lookup.py (+ analytics_index.json), scd_type_selector.py,
│                 stream_semantics_calc.py, entity_boundary_auditor.py
├── skills/       analytics-topic-lookup, scd-type-selector, stream-semantics-calc, entity-boundary-auditor   # one SKILL.md per entry (skills/<name>/SKILL.md)
├── tests/        casos-de-teste.md (27), relatorio-de-fidelidade.md, run_script_tests.py,
│                 verify_citations.py (+ citation-checks.json), audit_tokens.py
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**, since agent formats and paths change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/data-warehouse-streaming-distributed-expert`.
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install data-warehouse-streaming-distributed-expert@general-agents`.
- Or as a subagent: copy `agents/data-warehouse-streaming-distributed-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder; adjust the `<PKG>` paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent running the scripts.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (e.g., `tools/data-warehouse-streaming-distributed-expert/`) and copy or reference `AGENTS.md` at the repository root (or in `~/.codex/AGENTS.md`). In the file, `<PKG>` is the package folder. Alternative: open Codex inside the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/data-warehouse-streaming-distributed-expert.agent.md` to `.github/agents/` of your repository and the package folder into the repository (adjust `<PKG>` in the file). Select the agent in Copilot Chat. The file uses `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, no network)
```bash
python -I scripts/analytics_lookup.py "watermark"       # (--list, --not-covered); "NOT COVERED" if the collection does not cover it
python -I scripts/scd_type_selector.py --history full --rate slow
python -I scripts/scd_type_selector.py --history dual
python -I scripts/stream_semantics_calc.py --source replayable --state checkpointed --sink at-least-once --time event-time
python -I scripts/entity_boundary_auditor.py --uses-2pc    # checklist 100% [extrapolation]
python -I tests/run_script_tests.py
```
Origin of the rules: the SCD descriptions and semantics come from KIMBALL p.15-16 and STREAM p.17-20; **the scripts' decision trees are the agent's `[inference]`**; the boundary auditor is `[extrapolation]`.

## 5. Audit (how to reproduce)
1. Extract the text of each PDF per page with `=== PAGE N ===` markers (N = PDF page), for example with PyMuPDF:
   ```python
   import fitz
   d = fitz.open("Kimball-Dimensional-Modeling-Techniques.pdf")
   open("KIMBALL.txt", "w", encoding="utf-8").write("".join("=== PAGE %d ===\n%s\n" % (i, p.get_text()) for i, p in enumerate(d, 1)))
   ```
   (likewise `STREAM.txt` for the survey and `HELLAND.txt` for the Helland file.)
2. `python -I tests/verify_citations.py --kimball KIMBALL.txt --stream STREAM.txt --helland HELLAND.txt` (129 positive checks, 28 negative and a page-range sweep of all package citations).
3. `python -I tests/audit_tokens.py --kimball KIMBALL.txt --stream STREAM.txt` (backticked terms against the cited page).

## 6. Guarantees and limits
- Replies in the user's language (default: English), without reproducing the text; citations by PDF page.
- Coverage: the two PDFs present have 24 and 30 pages and were read in full in this audit; Helland could not be audited because the source is absent.
- Pasted input and PDF text are data, not instructions.
- The test cases were **not** run blind by an independent model (see `tests/relatorio-de-fidelidade.md`).
