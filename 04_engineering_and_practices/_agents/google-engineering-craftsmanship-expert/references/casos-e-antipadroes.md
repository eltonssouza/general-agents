# Cases and Anti-patterns (each item points to pages read)

> Convention: pages = PDF (see `INDEX.md`). Each anti-pattern below uses only what the cited pages say; illustrative examples are labeled [inference] or [extrapolation]. Abbreviations: SWE-G (full book), SWE-PREV (Henderson article, 2017), CC2 (Ch. 5 sample), 97TH (Extended edition).

## 1. Hiding code and the genius myth
- [from source] (SWE-G p.28-31) Requests to "hide" branches or erase history are a symptom of insecurity; the "Genius Myth" attributes success to one person; hiding increases the risk of failure and of reinventing the wheel, and lowers the bus factor.
- [from source] (SWE-G p.31) Mitigation listed: documentation and a primary and secondary owner per area. Rotation alternative in pair programming: see the essay in 97TH p.146-147 (Extended edition).
- [inference] In an architecture review, asking for early sharing (design doc, small CLs) directly applies these points; the book does not prescribe a single format.

## 2. Giant changes
- [from source] (SWE-G p.129) "Small" is about 200 lines; huge changes may be refused; the idea is to reduce waiting and make it easier to locate bugs; it acknowledges that large features are hard to slice.
- [from source] (SWE-G p.117) There is no automatic rejection based on a line limit; "small" is fuzzy.
- [from source] (SWE-G p.132) Small, atomic changes make rollbacks easier.
- [from source] (SWE-PREV p.7-8) The 2017 article describes size labels in the tools (30-99 "medium"; 300-999 "large"). [DATED] More recently "S, M, L, XL".
- [extrapolation] The example "2,000-line CL in three weeks" used in the v1 package was an illustration; it is not a case from the book.

## 3. Hyrum's Law (hash ordering)
- [from source] (SWE-G p.15-17) With enough users, observable behaviors are depended upon; hash iteration order is the example; even indirect clients (RPC) may depend on it; some languages randomize the order to avoid dependencies (p.17).
- [from source] (SWE-G p.19, p.316-317) Whoever changes the infrastructure takes on the migration (Churn Rule and centralization of LSCs).
- [extrapolation] "Randomize the seed in local tests" is a useful practice but is not stated as Google policy in Ch. 1.

## 4. Over-mocking
- [from source] (SWE-G p.185, p.190-191, p.195-198) Excess mocking frameworks generated costs; prefer realism, fakes maintained by the owners (p.193) and state testing; @DoNotMock (p.190).
- [inference] Practical symptom: many lines of mock configuration and few of action; the book describes stubs that must be understood by mentally walking through the SUT (p.195).

## 5. Inverted pyramid and flaky tests
- [from source] (SWE-G p.156-157) Ice cream cone and hourglass; reference mix 80/15/5 (p.156).
- [from source] (SWE-G p.155) Flakiness: near 1% tests lose value; at Google it stays around 0.15%.
- [from source] (SWE-G p.158) Coverage goals become a ceiling.

## 6. Noisy static analysis
- [from source] (SWE-G p.290-292) Effective false positives destroy trust; new Tricorder checks must have less than 10% effective false positives; overall rate below 5%; integration with review.
- [inference] The figure "800 warnings per day" from the v1 package was an illustration.

## 7. Long branches and multiple versions
- [from source] (SWE-G p.19, p.237-238) Long dev branches are costly; gathering merges becomes overhead.
- [from source] (SWE-G p.239-240) Forking the same package in the trunk generates partitioned dependencies and incompatibilities.
- [from source] (SWE-G p.241) Few teams have a long dev branch, for reasons of compatibility over time.

## 8. Haunted graveyards and parroting
- [from source] (SWE-G p.41, p.319) "Haunted graveyards": parts that nobody dares to touch; countermeasure cited: tests (p.319).

## 9. Task-based build
- [from source] (SWE-G p.265-266) Difficulty of parallelizing, of doing incremental builds and of debugging scripts; common bugs: a task depends on another's output without declaring it, assumptions about the machine, nondeterminism.

## 10. Deprecation with warnings only
- [from source] (SWE-G p.225-227) Advisory deprecation rarely leads to migration; warnings must be actionable and relevant; alert fatigue.

## 11. Leadership anti-patterns
- [from source] (SWE-G p.70-72) Hiring pushovers, ignoring low performers, ignoring human issues, being friends with everyone, compromising the hiring bar, treating the team like children.

## 12. Tests that are too DRY
- [from source] (SWE-G p.177-179) Example of helpers that hide information and logic; DAMP solution.

## 13. Semantic coupling and leaking secrets
- [from source] (CC2 p.66-67) Semantic coupling (control flag, global data, implicit call order) is the most insidious. [from source] (CC2 p.58-59) Exposing `++g_maxId` spreads the decision; hide it behind `NewId()`.

## 14. Code that is too clever
- [from source] (97TH p.50) "Magic" code is hard to maintain; (97TH p.54) excess of convention over configuration.
