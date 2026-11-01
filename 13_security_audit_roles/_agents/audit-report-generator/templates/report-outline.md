# Security Audit Report — {{PROJECT}}

**Revision analyzed:** {{REVISION}} | **Date:** {{DATE}} | **Scope:** {{SCOPE}}  
**Audit state:** COMPLETE WITHIN SCOPE / PARTIAL (choose according to coverage)

## 1. Executive summary
- **Confirmed** vulnerabilities: {{CONFIRMED_TOTAL}}; by severity {{BREAKDOWN}}.
- Potential: {{POTENTIAL_TOTAL}}; requires validation: {{PENDING_TOTAL}}.
- Greatest verified risks and priority actions.
- Scope actually analyzed and main gaps.

## 2. Architecture and threat
Stack, surfaces, diagram, trust boundaries and applicability criteria for the 20 domains.

## 3. Coverage matrix
| Domain | Inventoried | Examined | Not verified | Not applicable | Limiting factors |
|---|---:|---:|---:|---:|---|

## 4. Strengths
**Verified** controls with evidence, scope and caveats.

## 5. Confirmed findings
By severity → domain → file:line, redacted evidence, conditions, impact and remediation.

## 6. Suspicions and pending investigation
Potential, requires validation, discarded false positives (triage summary).

## 7. Malicious code
Confirmed behaviors, highly suspicious, sensitive but legitimate, indeterminate; without inferring intent.

## 8. Privacy and technical compliance
Applicable requirements, sources, evidence, external gaps, legal review needed. **It is not equivalent to certification.**

## 9. Roadmap P0–P3
Root cause, impact, urgency, fix, suggested owners by function, acceptance criteria and tests.

## 10. Methodology and limitations
Tools and versions actually used, revision, steps, coverage and gaps.

## 11. ISSUES FOR GITHUB
Complete texts, delimited by `--- ISSUE n ---` and `--- END ISSUE n ---`.

## 12. Appendices
List of assets, technical/normative references, generator and artifact integrity.

**PDF design:** A4, ~2 cm margins, header/footer, page number, donut and bar charts, colors by severity: critical `#B91C1C`; high `#EA580C`; medium `#D97706`; low `#2563EB`; positive `#059669`.
