---
name: cc-smell-catalog
description: "Catalog of the 66 heuristics of chapter 17 of \"Código Limpo\" (Clean Code; \"Odores e Heurísticas\", Smells and Heuristics: C1-C5 comments, E1-E2 environment, F1-F4 functions, G1-G36 general, J1-J3 Java, N1-N7 names, T1-T9 tests), with the title (English, plus the Brazilian edition's printed Portuguese title) and the PDF page. Use when the user cites a code (\"what is G5?\", \"does this violate F3?\"), asks for the heuristic for a problem (\"which heuristic covers duplication/magic numbers/transitive navigation?\") or when a review needs to name the smell. Do not use for rules that exist only in chapters 1-16 without a code: use cc-topic-lookup."
---

# Catalog of smells and heuristics (ch. 17)

Source: CL ch. 17, PDF p.280-309; data in `${CLAUDE_PLUGIN_ROOT}/scripts/cc_smells.json` (66 codes); family summary in `${CLAUDE_PLUGIN_ROOT}/references/cap17-odores-e-heuristicas.md`.

## Procedure
1. Run the query (read-only, no network):
   ```bash
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/cc_smells.py G5 F3 N1     # by code (accepts g5, G05)
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/cc_smells.py "duplication"  # by keyword (Portuguese works too: "duplicação")
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/cc_smells.py --family T     # whole family
   ```
   (`${CLAUDE_PLUGIN_ROOT}` = package root, substituted by Claude Code in the plugin; on other platforms, use the package folder, `../../` from this skill.)
2. Interpret:
   - Each entry shows the code, the English title with the edition's Portuguese title in parentheses, the family and `(CL p.N)`, a summary of our own, whether the smell has candidates detectable by script (`cc_audit.py`) or requires judgment, and the related codes.
   - **NOT COVERED** (exit 1): a code that does not exist in the book (e.g. G37, F5) or a word with no matching heuristic. Say so; do not invent a code.
3. Always cite the code and the page: "F3 Flag Arguments (CL p.283)". The related codes are `[inference]` by the package, except when the book explicitly links the codes.
4. Titles with problems in the edition: G34 is printed without its final word ("Funções devem descer apenas um nível de", missing "abstração"); mention it when citing.

## Response format
`CODE Title (CL p.N)` — what it is (1-2 sentences) — how it appears in the user's code — suggestion.

## Example
**Input:** "what is G25?" → `G25 Replace magic numbers with named constants (CL p.294)`: loose numbers become named constants; self-explanatory formulas and very well-known values may stay.

## Limits
"Smell" (odor) is the book's term; it does not use "code smell" or Fowler's names (Long Method, God Class...). The Appendix C page numbers ("17-292") do not apply to this edition.
