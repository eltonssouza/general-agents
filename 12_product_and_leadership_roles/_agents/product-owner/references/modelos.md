# product-owner delivery templates

`[practice]` Templates in common use in product work; they do not come from a bibliographic source in the collection.

## Ubiquitous language glossary
| Term | Definition (one sentence) | Forbidden synonyms |
|---|---|---|
| Order | Purchase confirmed by the customer, with items and address | "request", "purchase" (when ambiguous) |

## AS-IS / TO-BE flow
- **AS-IS**: numbered steps of the current process, who performs each one, where there is rework or waiting.
- **TO-BE**: steps of the desired process; for each step, happy path, alternatives and failure recovery.

## Story
```
### Story <id>: <short title, verb + object>
**As a** <persona>, **I want** <one capability>, **so that** <business outcome>.

**Scenario:** <happy path>
- **Given** <context with concrete values>
- **When** <user action or event>
- **Then** <observable result>

**Scenario:** <edge or validation>
- **Given** ...
- **When** ...
- **Then** ...
```
Check INVEST: Independent (delivers without depending on another one in progress), Negotiable (describes a need, not a solution), Valuable (explicit business outcome), Estimable (defined terms), Small (fits in one iteration; an "and" in the "I want" usually hides two), Testable (verifiable scenarios).

## Definition of Ready (DoR)
- [ ] Terms in the story are in the glossary.
- [ ] Persona and business outcome are explicit.
- [ ] There are scenarios for the happy path, the edges and the validations, with concrete values.
- [ ] Dependencies and test data are known.
- [ ] `story_check.py` reports no errors.

## Definition of Done (DoD)
- [ ] All scenarios verified by automated tests.
- [ ] Criteria demonstrated to the PO (or to the business owner).
- [ ] No open high-severity defect tied to the story.
- [ ] User or operations documentation updated, when applicable.

## Replacing vague terms (examples)
| Vague | Measurable |
|---|---|
| "fast" | "responds within 2 s at p95 with 100 concurrent users" |
| "intuitive" | "80% of new users complete the task without help in the usability test" |
| "secure" | concrete criterion (e.g. "only the order's owner sees it"); technical detail with the collection's security specialists |
