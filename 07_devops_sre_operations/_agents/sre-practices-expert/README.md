# SRE Practices Expert (Claude Code, Codex and GitHub Copilot)

SRE practices specialist agent, grounded in the work:
- **[SRE]**: *Site Reliability Engineering: How Google Runs Production Systems* (Beyer, Jones, Petoff, Murphy, eds.; O'Reilly/Google, 2016), 347-page PDF. The rights belong to the authors; this package contains its own summaries and references, not the text of the book.

## 1. Overview
Helps engineers and leads decide and act on: SLI/SLO/SLA and error budgets, risk and nines, toil, automation, monitoring and alerting, release engineering, simplicity, on-call, troubleshooting, emergency response and incident management, postmortems, reliability testing, load balancing, overload, cascading failures, consensus, cron and pipelines, data integrity, launches, capacity planning and management of SRE teams.

**Source rigor**: the book is from 2016 and describes Google. The agent separates `[from source] (SRE p.N)` from `[inference]`, `[extrapolation]` and `[DATED]` (Borgmon, Borg, Chubby, Rapid, Outalator etc.). **Page convention: PDF; printed page = N − 12.** The book does not cover burn rate, error budget policy, circuit breaker, OpenTelemetry, DORA, among others (see `references/INDEX.md`).

## 2. Structure
```
sre-practices-expert/
├── .claude-plugin/plugin.json
├── .github/agents/sre-practices-expert.agent.md   # Copilot
├── AGENTS.md                                      # Codex
├── agents/sre-practices-expert.md                 # Claude Code
├── references/   INDEX (with a deep/summary/pointer coverage map), glossary, procedures, casos-e-antipadroes + 12 topical files
├── scripts/      error_budget_calc.py, sre_math.py, postmortem_tool.py,
│                 sre_lookup.py (+ sre_index.json + book_term_index.json), build_book_index.py,
│                 verify_citations.py (+ citation-checks.json)
├── skills/       error-budget-calc, sre-math, postmortem-tool, sre-topic-lookup, build-book-index, verify-citations   # one SKILL.md per entry (skills/<name>/SKILL.md)
├── tests/        casos-de-teste.md (44), relatorio-de-fidelidade.md, run_script_tests.py, verify_citations.py, citation-checks.json
└── README.md
```

## 3. Installation
Script prerequisite: Python 3.8+ (stdlib only), always with `python -I`. **Check each platform's current documentation**, since agent formats change.

### 3.1 Claude Code
- Local plugin: `claude --plugin-dir /path/to/sre-practices-expert`.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install sre-practices-expert@general-agents`.
- Or as a subagent: copy `agents/sre-practices-expert.md` to `.claude/agents/` (project) or `~/.claude/agents/` (user) and keep `references/` and `scripts/` accessible (copy the folder, adjusting paths if needed). The agent declares `tools: Read, Grep, Glob, Bash`; remove `Bash` to prevent running the scripts.

### 3.2 Codex (OpenAI)
Copy the folder into the repository (e.g. `tools/sre-practices-expert/`) and copy/reference `AGENTS.md` at the root (or `~/.codex/AGENTS.md`). Inside the file, `<PKG>` is the package folder. Alternative: open Codex with its working directory in the package folder itself.

### 3.3 GitHub Copilot
Copy `.github/agents/sre-practices-expert.agent.md` into `.github/agents/` of your repository and the package folder into the repository (adjust `<PKG>`). Select the agent in Copilot Chat. `tools: ['read','search','execute']`; remove `execute` to block scripts.

## 4. Scripts (deterministic, offline)
```bash
python -I scripts/error_budget_calc.py downtime 99.95
python -I scripts/error_budget_calc.py requests --slo 99.99 --total 2500000 --failed 300
python -I scripts/error_budget_calc.py consume --slo 99.999 --failure-rate 0.0002
python -I scripts/error_budget_calc.py table            # reproduces Appendix A (48 cells)
python -I scripts/sre_math.py provision --peak 3470 --per-task 100
python -I scripts/sre_math.py oncall --sites 2
python -I scripts/sre_math.py retry-amp
python -I scripts/postmortem_tool.py template --lang pt
python -I scripts/postmortem_tool.py validate my-postmortem.md
python -I scripts/sre_math.py borgmon-ram --series 2500000 --hours 24   # 86.4 GB (24 B per point, SRE p.90-91)
python -I scripts/sre_math.py duration --start 14:54 --end 16:00         # 66 min (App. D)
python -I scripts/sre_lookup.py "error budget"       # COVERED (rc 0); also --topic, --pages, --list
python -I scripts/sre_lookup.py "root cause"        # COVERED (rc 0): definition on p.55; "push", "paging events", "feature flag" likewise
python -I scripts/sre_lookup.py "Dagger"            # POINTER ONLY (rc 3): the book has the term (p.137, 147), the package does not summarize it
python -I scripts/sre_lookup.py --check             # consistency: every topic keyword appears in the summary/rules
python -I scripts/sre_lookup.py "circuit breaker"   # NOT COVERED (rc 1): outside the book
python -I scripts/build_book_index.py --text /path/Google-SRE-Book.txt --check   # verifies the versioned term index
python -I scripts/verify_citations.py --text /path/Google-SRE-Book.txt   # requires the per-page extracted text (=== PAGE N ===)
python -I tests/run_script_tests.py
```
The formulas used are only those the book provides (time-based and aggregate availability, p.38; budget = 1 − target, p.25 and p.330; Appendix A, p.326-327); the rest is arithmetic from the book's examples, with the page.

## 5. Guarantees and limits
- Answers in the user's language (default: English), without reproducing the book; citations by page.
- **Three-level lookup (round 2)**: COVERED (summary + pages), POINTER ONLY (the book has the term, the package does not summarize it; pages come from the term index `book_term_index.json`, generated from the book's own text) and NOT COVERED (curated list of things outside the book or no occurrence in the index). Only the third level allows saying "the book does not cover this".
- Audit: `verify_citations.py` (371 positive and 56 negative checks after round 4; also in `tests/verify_citations.py`) plus an independent read-through audit of the references by three model reviewers (see `tests/relatorio-de-fidelidade.md`).
- **Round 5 (after the round 4 blind test)**: `COVERED` is now decided **only by the content of the summaries** in `references/*.md`: `scripts/build_ref_index.py` generates `scripts/ref_term_index.json` (whole term → summary sentences that cite a page; `--check` verifies) and `sre_lookup.py` matches the query against it, with no substring match on file name or title; terms found only in a pointer list, `INDEX.md` or a "the book does not cover this" note give POINTER ONLY (rc 3) and the note appears under "LIMIT NOTES". New content (with PDF page): roles, specialization and diversity (p.298); objectives, limitations and Early Engagement candidates (p.308, 310); global overload (p.176); OK/BAD and Resources of the minutes (p.340); LCE (p.262, 272); retries in an emergency (p.192); GC death spiral (p.198); Doorman (note 106, p.183); Peer Bonus (note 82, p.129); note 25 (p.62). Alertmanager is described on p.95 (the answer key for case C11 was wrong).
- **Round 4 (after the round 3 blind test)**: the lookup's `COVERED` requires the topic summary to address the term (before, "root cause" and "push" matched the wrong topics); 4 new topics and 14 expanded (definitions on p.55, production meeting p.296-297 and 339, outbound deadline and bursty queueing p.189 and 193, Moiré in continuous pipelines p.236, canary and 6 feature-flag requirements p.268, cherry-pick and MPM p.78, ticket scrub p.288, CAPA p.319 and a sweep of Ch. 11-12, 14-15, 23, 26, 33 and footnotes; see `references/INDEX.md`, "Varredura da rodada 4" ("Round 4 sweep")). The new tests were written for coverage, not from the 14 cases of the blind evaluation.
- Pasted input and PDF text are data, not instructions.
- The tests were **not** run blind by an independent model (see the report).
