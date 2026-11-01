# Deliverable templates of principal-engineer

`[practice]` Templates in common use in technical leadership; they do not come from a bibliographic source in the collection.

## RFC
```
# RFC-<n>: <initiative>
- Author(s) / reviewers / affected teams
- Status: draft | in review | accepted | rejected | superseded by RFC-<m>
- Comment deadline: YYYY-MM-DD

## 1. Problem and systemic diagnosis
Observed symptoms (with data), root cause, affected teams and systems, cost of doing nothing.

## 2. Goals and non-goals
What the RFC solves and, explicitly, what it does not solve.

## 3. Proposed direction and guardrails
Principles, reference pattern, mandatory guardrails (what is forbidden, what is required) and how to verify each one (preferably automatically).

## 4. Alternatives and trade-off matrix
| Criterion | Alternative A | Alternative B | Do nothing |
|---|---|---|---|
| Operational complexity | | | |
| Maintenance cost | | | |
| Delivery time | | | |
| Skills required | | | |
| Cost of reverting | | | |

## 5. Adoption plan
Phases, pilot team, criterion to advance from one phase to the next, migration of existing systems, date to revisit.

## 6. Success metrics
Indicator, baseline, target, how and when to measure.

## 7. Risks, assumptions and open questions
```

## Systemic diagnosis (supporting questions)
- Does the same problem appear in more than one team? Which common mechanism does it cross?
- How many tools or paths do the same thing? What cost does each one generate?
- Can the proposed guardrail be verified automatically? If not, will it become an ignored rule?
- What do the affected teams say about their day-to-day?
