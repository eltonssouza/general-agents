# Validation report: product-designer v1.0.0

Date: 2026-11-01. Environment: Windows 11, Python 3.13.15, Claude Code 2.1.316.

## Origin and decision
Adapted from the harness's `product-designer` role agent (MIT, Elton Souza): translated to English, `{{...}}` placeholders replaced by "expected inputs", constraints with the reason why, honesty labels (`[practice]`, `[from collection: <agent>]`, `[inference]`, `[assumption]`), hand-offs to the collection specialists and templates in `references/`. It entered the collection because no specialist covers this role; 12 of the 16 agents in the origin were left out as duplicates (see `00_orchestration/.../references/fronteiras.md`).

## Package
| Check | Result |
|---|---|
| `python -I tests/run_script_tests.py` | 13 checks, **0 failures** |
| `claude plugin validate --profile directory` | Validation passed; "These checks found nothing to report" |
| Collection marketplace | entry added; the marketplace's `claude plugin validate` passes (66 plugins) |
| Orchestrator | catalog with 65 agents in 12 domains; dedicated routing case; 95 PASS / 0 FAIL |

## End-to-end run (Claude Code, headless, Sonnet model)
| # | Request | Result | Cost |
|---|---|---|---|
| R2 | "Does #777 on white pass contrast? Minimum touch target at AA?" (`--agent product-designer:product-designer`) | PASS: ran `contrast.py`; 4.48:1 fails AA (1.4.3), suggests `#767676` (4.54:1); touch target **24x24 CSS px (2.5.8)**, 44x44 only at AAA (2.5.5) | US$ 0.03 |

The reply corrects the value the origin attributed to AA (44x44).

## Not run
Codex and GitHub Copilot (clients absent in this environment); models other than Sonnet; independent blind evaluation.
