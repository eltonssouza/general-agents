# INDEX: product-owner

## Nature
**Role** agent (folder 12 of the collection): delivers product specification. It has no bibliographic source in the collection; the guidelines are market practices labeled `[practice]`. Origin: `relay-harness/packages/coding-agent/resources/agents/product-owner.md` (MIT, Elton Souza), translated and adapted to the collection standard on 2026-11-01.

## Files
| File | Use |
|---|---|
| `modelos.md` | glossary, AS-IS/TO-BE, story with scenarios, DoR, DoD, replacing vague terms |
| `../scripts/story_check.py` | deterministic validation of stories (skill `po-story-check`) |

## Boundaries with the collection
| Topic | To whom |
|---|---|
| DDD theory (ubiquitous language, bounded contexts) with a citable source | `clean-architecture-ddd-expert` |
| Screens, interaction flows, design tokens, visual accessibility | `product-designer`; accessibility fundamentals: `web-accessibility-visual-design-expert` |
| Slicing technical execution, technical debt, risk sequencing | `tech-lead` |
| Testing strategy and automation of the criteria | `software-testing-qa-expert` |
| Security and privacy requirements (LGPD) | `owasp-asvs-code-review-expert`, `privacy-lgpd-engineering-expert` |

## What this agent does not do
Implement code; estimate in hours; prioritize by value without business data (it asks or records it as an assumption).
