# product-designer delivery templates

`[practice]` Templates in common use in product design; they do not come from a bibliographic source in the collection. Numeric accessibility values are `[WCAG 2.2]`, with the criterion number.

## Journey and flow
| Step | User intent | Screen/state | System feedback | Possible error and recovery |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

## Usability heuristics (quick check)
Visibility of system status; match with the real world; user control and freedom (undo, exit); consistency and standards; error prevention; recognition rather than recall; flexibility and efficiency (shortcuts); aesthetic and minimalist design; help recognize, diagnose and recover from errors; help and documentation.

## Tokens
```
cor.primaria.500 = #1A73E8      (measure against the backgrounds with contrast.py)
cor.texto.padrao = #202124
cor.status.erro  = #C5221F      (always with an icon or text, never color alone)
tipo.corpo       = 16px / 24px
espaco.1..8      = 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px
elevacao.1..3    = card, menu and modal shadows
```

## Component states (fill in for each component)
| State | Visual | Behavior | Accessibility |
|---|---|---|---|
| Default | | | accessible name |
| Hover | | | not the only indicator |
| Focus | visible ring | logical tab order | ring contrast >= 3:1 (1.4.11) |
| Active | | | |
| Disabled | | no action | reason explained, when useful |
| Loading | skeleton/spinner | blocks double submission | announced to screen readers |
| Empty | message + action | | |
| Error | message + how to fix | keeps what the user typed | icon/text, not color alone |

## Accessibility checklist [WCAG 2.2]
- [ ] Normal text >= 4.5:1; large text (18 pt, or 14 pt bold) >= 3:1 (1.4.3, AA) — measured with `contrast.py`.
- [ ] Components, icons and focus ring >= 3:1 against the adjacent color (1.4.11, AA).
- [ ] Touch target >= 24x24 CSS px (2.5.8, AA); 44x44 if the goal is AAA (2.5.5).
- [ ] State and meaning do not depend on color alone.
- [ ] All states (empty, loading, error) specified.
