# Validation report - general-agents-orchestrator v1.0.0

Date: 2026-10-31. Environment: Windows 11, Python 3.13.15, Claude Code 2.1.316. English translation of the package: 2026-11-01 (see the last section).

## What was run
| Check | Command | Result |
|---|---|---|
| Catalog up to date | `python -I scripts/build_catalog.py --check` | OK, 60 agents (61 on 2026-11-01; 74 after the roles and the audit pipeline) |
| Automated tests | `python -I tests/run_script_tests.py` (also from the copy in `_agents_tests/`) | 84 PASS, 0 FAIL; the 60 reachable agents (on 2026-11-01: 106 PASS, 65 agents in 12 domains; after the English translation: 211 PASS, 74 agents in 13 domains) |
| Mutation proof | turn off the negative-clause protection / loosen the prefix | 3 FAIL / 1 FAIL (detected) |
| Plugin manifest | `claude plugin validate <PKG>` | Validation passed (directory warnings: LICENSE and icon missing) |
| E2E multi-domain | `claude -p --agent general-agents-orchestrator` + 2 specialist `--plugin-dir` | PASS (fallback), USD 1.82 |
| E2E single domain | same with `python-expert` | PASS (named delegation), USD 0.19 |

## E2E observations
- **E01:** the orchestrator ran `route.py` per subtask and `--show` on the two candidates and launched the two delegations in the same message (parallel). In the integration, it preserved `[from source]`/`[inference]`/`[extrapolation]`/POINTER ONLY with page, exposed the conflict "limit/offset (APIGEE p.50) vs OFFSET cost" with the trade-off and listed the gaps as NOT COVERED. It did not change files and stated that it did not validate for lack of database access.
- **E02:** direct delegation to `python-expert:python-expert`, no written plan; answer with labels and "Specialist:" at the end.

## Findings in the specialists (fixed on 2026-10-31, at the user's request)
1. **`plugin.json` files rejected by Claude Code.** 55 had `author` as a string (`author: Invalid input: expected object, received string`); the original value became `{"name": "..."}`. After that, the validator revealed 7 more with invalid `skills` (objects or paths without `./`, some pointing to `.py` scripts). The field was removed: Claude Code already scans `skills/` by default, and the scripts are documented in each package's README and prompt. The unknown field `entrypoint` (ignored by Claude Code) left 7 manifests. Result: `claude plugin validate` passes on 61/61, and a headless session with csharp, relational-dbms-internals and web-api-rest loaded the 3 plugins with no `plugin_errors`, with named agents and skills. E01 above ran before the fix, so it used the fallback.
2. **29 `.md` files cited `10_ai_and_llm/`**; the real folder is `09_ai_and_llm/`. The 34 occurrences were replaced. Two of them cite source PDFs (`DL-Deep-Learning-Goodfellow.pdf`, `Data-Platform-Engineering-Handbook-2022.pdf`) that are not in the repository.
3. **License and icon** (required only by the official plugin directory). By the user's choice: MIT license (`LICENSE` at the collection root, with a note that cited works follow their authors' terms) and `"license": "MIT"` in the 61 manifests. Each package received `.claude-plugin/icon.png`, a 512 px PNG per domain (number + acronym).
4. **Marketplace installation** (advice from the validator in the `directory` profile). Created `general-agents/.claude-plugin/marketplace.json` (local marketplace `general-agents`, 61 plugins with relative source); `claude plugin validate .` passes. Each README gained a line: `/plugin marketplace add /path/to/general-agents` and `/plugin install <name>@general-agents`. Tested with an isolated config directory: the marketplace was added and csharp-expert and the orchestrator were installed and enabled. Result of `claude plugin validate --profile directory` on the 61 packages: "nothing to report", no advice.
5. **Specialist suites.** Four runners failed when the source text was not in the collection (`scratch/...` and PDFs), unlike the convention of the others (go, rust, infosec, modern-deep-learning, python-web-frameworks), which mark SKIP. Adjusted to SKIP only when the **default** source is absent; with an explicit, invalid `--src` they still fail: google-engineering-craftsmanship (the existing detection only recognized "PyMuPDF missing"), aws-lambda-serverless, graphql and node-backend-frameworks (copies in `_agents_tests/` synchronized). Test HY-1 of go-expert, which requires every file to be UTF-8 text, now ignores `.png` (the icon), as it already ignored `.pyc`. Result: the 54 executable suites pass. The standalone `verify_citations.py`/`audit_claims.py` that require `--src` still depend on the source texts.

## Not run
- Codex and GitHub Copilot: no such clients in this environment. The adapters follow the official documentation checked on 2026-10-31 (`references/plataformas.md`).
- Blind execution by an independent model.

## Update 2026-11-01: `clean-code-expert` (04) joins
- Catalog regenerated: 61 agents in 11 domains; new routing case ("review this function by Clean Code..." → `clean-code-expert` 1st).
- C02 now compares the catalog with the agents on disk, instead of the fixed number 60; A04 uses `--top 999`. The orchestrator descriptions stopped citing the count.
- `fronteiras.md`: tie-breaker *Clean Code* (whole book) vs `design-patterns-expert` (sample of Ch. 1) vs `clean-architecture-ddd-expert` (SOLID as an acronym, layers).
- Checked that the new agent does not capture requests from its neighbors (Clean Architecture, SOLID).

## Fix of the `route.py` ordering (2026-11-01)
- **Problem:** generic terms in an agent's name (weight 3) beat the agent that covered the whole request. "GoF Strategy or State pattern" went to `infosec-strategy-threat-modeling-expert`/`ml-engineering-strategy-expert` ("strategy" in the name) and "how does Google do code review" went to `owasp-asvs-code-review-expert` ("code review" in the name).
- **Fix:** the order now uses `score = strength x coverage²`, where coverage is the fraction of the request terms, IDF-weighted, that the agent matches (coordination factor). The `strength` (raw match) still decides `MIN_SCORE`/`STRONG_SCORE`, so "NO SPECIALIST" and "clear specialist" did not change. The JSON carries both fields.
- **Calibration:** exponent 1 solved the Strategy case but not the Google one; 1.5 and 2 solved both without breaking any case. It stayed at 2, the largest margin. Using coverage in the threshold too was discarded: it dropped correct cases (knapsack, PITR, MLFQ) to NO SPECIALIST.
- **Verification:** 90 PASS, 0 FAIL, with four new regression cases (R52-R55) and A05. With the old ordering, R52-R54 fail (mutation proof). No specialist description needed to change.

## Role agents of folder 12 (2026-11-01)
- Origin: the 16 agents of `relay-harness/packages/coding-agent/resources/agents` (MIT). 4 joined, with no equivalent specialist in the collection: `product-owner`, `product-designer`, `tech-lead`, `principal-engineer`. The other 12 were considered duplicates (domain already covered by a specialist; cross-cutting work belongs to the orchestrator); the table is in `references/fronteiras.md`.
- Catalog: 65 agents in 12 domains. C02 now compares agents **and domains** with the disk. Cases R56-R60 (four roles and the boundary with the accessibility specialist). Result: 95 PASS, 0 FAIL.
- The orchestrator prompt and the adapters now distinguish specialists (source and page) from roles (`[practice]`, no page) and preserve `[practice]` in the integration.

## Management of role agents by the orchestrator (2026-11-01)
- **Catalog:** `build_catalog.py` writes `kind` (`role` for `*_roles` domains; `specialist` for the rest); `catalogo.md` shows the total per kind and marks the roles domain. (Values were `papel`/`especialista` until the English translation.)
- **Router:** `route.py` shows `kind` in `--json`, in the candidate list, in `--list` and in `--show`; the `--show` of a role reminds that the return is `[practice]`, with no page, and that grounding comes from the specialist.
- **Canonical prompt:** classification (b2) for role deliverables; role vs specialist and combination rules (specialists first, grounding with citations in the role brief; chain `product-owner` → `product-designer` → `tech-lead`; `principal-engineer` across teams); role brief without a page; attribution and role vs specialist conflict in the integration; routing per agent (specialist or role) in the delivery.
- **Protocol:** proportionality rows for roles, variant 2.1 of the brief, attribution rule `[from collection: <agent>]` and a full example (PIX). Codex/Copilot adapters, skill `orq-route`, `INDEX.md` and README updated.
- **Tests:** C07, S04-S06, F05-F06 new; 101 PASS, 0 FAIL (also on the copy in `_agents_tests/`). Mutation proof: with the role suffix changed, C07, S04 and S06 fail.
- **End to end (E03, Sonnet, USD 0.57):** the orchestrator ran the OWASP specialist first, then `product-owner` and `tech-lead` in sequence with the ASVS requirements cited in the brief; integrated with the roles labeled `[practice]`, the ASVS citations preserved with page and payments/PIX declared NO SPECIALIST; no user file changed. The `product-owner` ran its own story validator.
- **Finding outside the orchestrator:** the `owasp-asvs-code-review-expert` (an older specialist) looks for its scripts by relative path and did not find them in plugin mode on the 1st attempt; the orchestrator passed the path. The new packages (clean-code and roles) use `${CLAUDE_PLUGIN_ROOT}`; the older specialists were not changed.

## Agent models (2026-11-01)
- **Policy** in `scripts/models.json`, from the models allowed by the relay-harness (`model-eligibility.ts`, `docs/laya.md`) and the price-tier rule within the provider: `fast` = Haiku / gpt-6-luna; `balanced` = Sonnet / gpt-6.1-sol; `strong` = Opus / gpt-5.6-terra; `frontier` = Opus / gpt-6-astra. Copilot IDs from the `github-copilot.json` catalog.
- **Assignment:** specialists and roles in `balanced` (evidence: end-to-end tests with Sonnet); orchestrator and `principal-engineer` in `strong`. `fast` and `frontier` mapped, no agent by default.
- **Application:** `apply_models.py` wrote 187 files in 66 packages (frontmatter `model` in Claude Code and Copilot; a block in `AGENTS.md`). The 11 agents that already had `model: sonnet` matched the policy.
- **Regressions:** baseline of 59 collection suites, all green before; after the application, 6 broke on a rigid frontmatter regex (go-expert HY-7, clean-code-expert and the 4 roles). Fixed: go-expert now accepts an optional `model:`; the new packages now require a valid `model:`. Result: 59/59 green.
- **Does a plugin respect `model`?** The Claude Code documentation does not say; test E04: with the main session in Haiku, `principal-engineer` answered in `claude-opus-5-5` and `clean-code-expert` in `claude-sonnet-5-5` (`resolvedModel`).
- **Tests:** M01-M05; 106 PASS, 0 FAIL.

## English translation and bilingual routing (2026-11-01)
- **Scope:** the whole package was translated in place (prompt, adapters, README, plugin.json, skills, scripts, tests, references; `catalog.json` and `catalogo.md` regenerated from the 75 packages, whose descriptions are now English).
- **Kinds and keys:** `kind` values are now `specialist`/`role`; JSON keys of `route.py --json` (`candidates`, `strength`, `terms`, `exclusion_alert`, `clear_specialist`), the catalog `model` object (`tier`, `claude_policy`) and `models.json` (`tiers`, `default`, `exceptions`, `use`, `rationale`) are English. File names, the `model:` frontmatter, the `<!-- modelo:inicio/fim -->` markers and the `AGENTS.md` model block are unchanged.
- **Bilingual routing:** the lexical triage uses IDF-weighted terms of the English descriptions. English negative-clause patterns replaced the Portuguese ones ("Do not use for...", "Does not cover...", "NOT COVERED", "Out of scope"), plural/singular matching was added, and `scripts/vocab_pt.json` maps Portuguese words and phrases to English terms (deterministic, no network). Every routing case now exists in English (`R##`) and Portuguese (`RP##`) and must reach the same agent.
- **Adapted case:** "code review de segurança: injeção SQL e XSS" no longer reached `owasp-asvs-code-review-expert` in the top 1 with the English descriptions (the WSTG description carries "SQL injection" and "XSS"); the case is now "secure code review checklist: SQL injection and XSS" / "checklist de code review seguro: injeção SQL e XSS", top 2.
- **Result:** 211 PASS, 0 FAIL (baseline of the Portuguese package: 118 PASS).
