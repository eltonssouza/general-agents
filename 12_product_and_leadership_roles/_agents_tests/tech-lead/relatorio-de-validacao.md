# Validation report: tech-lead v1.0.0

Date: 2026-11-01. Environment: Windows 11, Python 3.13.15, Claude Code 2.1.316.

## Origin and decision
Adapted from the harness's `tech-lead` role agent (MIT, Elton Souza): translated, `{{...}}` placeholders replaced by "expected inputs", constraints with their rationale, honesty labels (`[practice]`, `[from collection: <agent>]`, `[inference]`, `[assumption]`), hand-off to the collection's specialists and templates in `references/`. It entered the collection because no specialist covers this role; 12 of the 16 agents in the origin were left out as duplicates (see `00_orchestration/.../references/fronteiras.md`).

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
| R3 | "Plan the technical execution: PIX in an e-commerce, 4 devs, 6 weeks" (`--agent tech-lead:tech-lead`) | PASS: the 5 sections of the format; slices ordered by risk (PSP spike first), a test criterion per slice, technical debt with an ADR; explicit `[assumption]` (3x); no invented source | US$ 0.07 |

Note: it used `[assumption]` and not `[practice]`; the essential (not attributing to books) was met.

## Not run
Codex and GitHub Copilot (clients absent in this environment); models other than Sonnet; independent blind evaluation.
