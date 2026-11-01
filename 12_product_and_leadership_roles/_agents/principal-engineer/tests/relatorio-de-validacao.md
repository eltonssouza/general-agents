# Validation report: principal-engineer v1.0.0

Date: 2026-11-01. Environment: Windows 11, Python 3.13.15, Claude Code 2.1.316.

## Origin and decision
Adapted from `relay-harness/packages/coding-agent/resources/agents/principal-engineer.md` (MIT, Elton Souza): translated, `{{...}}` placeholders replaced by "expected inputs", constraints with their rationale, honesty labels (`[practice]`, `[from collection: <agent>]`, `[inference]`, `[assumption]`), hand-off to the collection's specialists and templates in `references/`. It entered the collection because no specialist covers this role; 12 of the 16 agents in the origin were left out as duplicates (see `00_orchestration/.../references/fronteiras.md`).

## Package
| Check | Result |
|---|---|
| `python -I tests/run_script_tests.py` | 6 checks, **0 failures** |
| `claude plugin validate --profile directory` | Validation passed; "These checks found nothing to report" |
| Collection marketplace | entry added; the marketplace's `claude plugin validate` passes (66 plugins) |
| Orchestrator | catalog with 65 agents in 12 domains; own routing case; 95 PASS / 0 FAIL |

## End-to-end run (Claude Code, headless, Sonnet model)
| # | Request | Result | Cost |
|---|---|---|---|
| R4 | "4 deploy tools across 8 teams: short RFC" (`--agent principal-engineer:principal-engineer`) | PASS: the 5 sections of the RFC; root cause labeled `[inference]`; verifiable guardrails; matrix with 4 alternatives (including doing nothing); pilot and waves; no invented source | US$ 0.04 |

Note: it used `[inference]`/`[assumption]` and not `[practice]`; the essential (not attributing to books) was met.

## Not run
Codex and GitHub Copilot (clients absent in this environment); models other than Sonnet; independent blind evaluation.
