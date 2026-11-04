---
name: cc-review-checklist
description: "Generates the \"Código Limpo\" (Clean Code) code review checklist by area (names, functions, comments, formatting, objects and data structures, error handling, boundaries, unit tests, classes, systems, simple design, concurrency), each item with the PDF page, choosing the areas from the file content (tests, threads, exceptions, classes) or from the request. Use to review a PR or file thoroughly, to prepare a code review script, or when the user asks for a \"Clean Code checklist\". Do not use to find occurrences automatically: use cc-code-audit."
---

# Review checklist by chapter

Source: CL chs. 2-13 and Appendix A; data in `${CLAUDE_PLUGIN_ROOT}/scripts/cc_checklist.json` (items with PDF page).

## Procedure
1. Generate the checklist (read-only, no network):
   ```bash
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/cc_checklist.py --file src/Pedido.java    # detected areas + names/functions/comments/formatting
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/cc_checklist.py --area testes,erros        # requested areas
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/cc_checklist.py --list                     # available areas
   ```
   (`${CLAUDE_PLUGIN_ROOT}` = package root, substituted by Claude Code in the plugin; on other platforms, use the package folder, `../../` from this skill. Unknown area: exit 2. Area keys are Portuguese.)
2. Answer each item by reading the code. "No" is a candidate for improvement, not a verdict; note `file:line` and the item's page.
3. For the items answered "no", name the smell with cc-smell-catalog and go deeper with the chapter reference (`${CLAUDE_PLUGIN_ROOT}/references/capNN-*.md`).
4. If the book's rule conflicts with the team's convention, the team decides (CL p.95): record the divergence instead of imposing the rule.

## Output format
Per area: items marked `[x]`/`[ ]`, each `[ ]` with evidence (`file:line`) and the page. Close with the 3-5 highest-impact improvements.

## Example
**Input:** `--file PedidoServiceTest.java` → areas: names, functions, comments, formatting and tests (detected by `@Test`), with items such as "Are the tests F.I.R.S.T.? (CL p.134-135)".

## Limits
Area detection works by text patterns (e.g. `synchronized`, `@Test`, `try`). The checklist does not cover the case studies (chs. 14-16) or the Java heuristics J1-J3 (use cc-smell-catalog).
