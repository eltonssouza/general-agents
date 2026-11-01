# Deliverable templates of tech-lead

`[practice]` Templates in common use in technical leadership; they do not come from a bibliographic source in the collection.

## Vertical slice
| # | Slice (observable outcome) | Depends on | Risk it reduces | Complexity (S/M/L) | Test criterion |
|---|---|---|---|---|---|
| 1 | Prototype of the payment gateway integration | — | unknown external API | M | test call approved in the sandbox |
| 2 | ... | 1 | ... | ... | ... |
Rule: a slice delivers something testable end to end (data, logic, interface or API); "create the tables" alone is not a slice.

## Milestone quality standard
- [ ] Validation of all external input (type, format, size, range).
- [ ] Errors handled on every I/O call, with a timeout.
- [ ] Automated tests for each acceptance criterion; a broken build blocks merge.
- [ ] No secret in code or logs; authorization checked on the server.
- [ ] Structured logs and metrics for what matters to the milestone.
- [ ] Code review criteria agreed with the team.

## Technical debt register
| ID | Debt | Why it was accepted | Cost of carrying it | Remediation trigger | ADR | Owner |
|---|---|---|---|---|---|---|
| D1 | No queue: emails sent synchronously | milestone 1 deadline | checkout latency | > 500 orders/h or p95 > 2 s | ADR-007 | team X |

## ADR (Architecture Decision Record)
```
# ADR-<n>: <decision in one sentence>
- Status: proposed | accepted | superseded by ADR-<m>
- Date: YYYY-MM-DD
## Context
<forces at play, constraints, what motivated the decision>
## Decision
<what was decided>
## Alternatives considered
<each with pros and cons>
## Consequences
<what improves, what gets worse, cost of reverting, trigger to revisit>
```
