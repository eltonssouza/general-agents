# INDEX: product-designer

## Nature
**Role** agent (folder 12 of the collection): delivers design specification (UX and UI). It has no bibliographic source in the collection; the guidelines are design practices labeled `[practice]`, and the accessibility values come from WCAG 2.2 (W3C), checked on 2026-11-01. Origin: `relay-harness/packages/coding-agent/resources/agents/product-designer.md` (MIT, Elton Souza), translated and adapted to the collection standard.

## Correction relative to the origin
The origin asked for a minimum touch target of 44x44 px as a "WCAG 2.2 AA" requirement. In WCAG 2.2, the AA minimum is **24x24 CSS px** (2.5.8); 44x44 is the AAA level (2.5.5). This package uses the values from the standard.

## Files
| File | Use |
|---|---|
| `modelos.md` | journey, usability heuristics, tokens, component states, WCAG checklist |
| `../scripts/contrast.py` | WCAG 2.2 contrast ratio (skill `pd-contrast-check`) |

## Boundaries with the collection
| Topic | To whom |
|---|---|
| Accessibility fundamentals and visual repetition/consistency with a citable source | `web-accessibility-visual-design-expert` |
| CSS layout (grid, flexbox, container queries) and implementation | `modern-css-layout-expert`, framework agents (folder 11) |
| Perceived performance and network | `web-performance-networking-expert` |
| Stories and acceptance criteria | `product-owner` |
