---
name: pd-contrast-check
description: "Use when defining a palette, design tokens or component states, or when asked \"does this gray pass contrast?\", \"are these colors accessible?\": calculates the WCAG 2.2 contrast ratio between color pairs (hex) and says whether it passes AA/AAA for normal text, large text and components (1.4.3, 1.4.6, 1.4.11), without rounding. Do not use to audit a whole page or for accessibility fundamentals with a citable source (web-accessibility-visual-design-expert)."
---

# WCAG 2.2 contrast check

## Procedure
1. Run the calculation (arithmetic only; no network):
   ```bash
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/contrast.py "#767676" "#FFFFFF"
   python -I ${CLAUDE_PLUGIN_ROOT}/scripts/contrast.py "#1A73E8/#FFFFFF" "#5F6368/#F1F3F4" --json
   ```
   (`${CLAUDE_PLUGIN_ROOT}` = the package root, substituted by Claude Code in the plugin; on other platforms, use the package folder, `../../` from this skill.)
2. For each pair: normal text needs 4.5:1 (AA); large text (18 pt, or 14 pt bold) and UI components/icons need 3:1 (AA). If it fails, darken or lighten the token and measure again; record the final ratio in the accessibility checklist.
3. Remember what the script does not measure: the actual font size, touch target size (24x24 CSS px at AA, 2.5.8) and state indicated by color alone.

## Output format
Table: token/pair — ratio — AA text — AA large text — AA components — proposed adjustment.

## Example
**Input:** `contrast.py "#777" "#fff"` → 4.48:1: fails AA for normal text, passes for large text. Adjustment: `#767676` (4.54:1) passes.

## Limits
Solid colors in hex; it does not compute transparency, gradients or text over images. Exit: 0 all pairs pass AA for normal text, 1 some pair fails, 2 usage error.
