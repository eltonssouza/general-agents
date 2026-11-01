# Procedures (derived checklists; each step has an origin)

> Convention: pages = PDF (see `INDEX.md`). Labels per step: [from source] only when the page says so; otherwise [inference] (logical derivation from the cited pages) or [extrapolation] (general good practice, no page). These procedures are NOT sequences declared by the book; they are the agent's checklists.

## 1. Preparing a change for review
1. [from source] (SWE-G p.129) Keep the change small and focused on one subject (about 200 lines is the book's reference; it is not a hard limit, p.117).
2. [from source] (SWE-G p.129-130) Write the description: first line as a summary, then the what and the why; update it when there is a new decision.
3. [from source] (SWE-G p.131-132) Test: a bug fix must add the test that was missing; behavior changes alter tests; do not mix in other fixes.
4. [from source] (SWE-G p.284, p.294) Let the presubmits (formatting, tests, "DO NOT SUBMIT") pass before requesting review.
5. [from source] (SWE-G p.122-123) Check which aspects need approval: LGTM from a peer, owner and readability (they may be implicit if you already have them).
6. [from source] (SWE-G p.128) Treat each comment as a TODO; expect feedback within 24 business hours (reviewer expectation).

## 2. Assessing the risk of changing a widely used API
1. [from source] (SWE-G p.15-16) Start from Hyrum's Law: observable behavior (order, timing, error format) may have dependents.
2. [from source] (SWE-G p.228-229, p.323) Use code search and semantic analysis to find uses (Code Search, Kythe).
3. [from source] (SWE-G p.19) Run the CI tests; under the Beyoncé Rule, whatever has no test in CI does not count as a regression.
4. [from source] (SWE-G p.226) Temporary shutdowns of increasing duration reveal hidden dependencies (a technique cited for deprecation).
5. [from source] (SWE-G p.316-328) If clients are affected, use the LSC process (authorization, generation, shards, cleanup).
6. [extrapolation] Risk note: the v1 package had a numeric "risk score"; no backing. The script `hyrum_evaluator.py` now lists factors with the book page and does not compute a score.

## 3. Deprecating a system
1. [from source] (SWE-G p.223) Confirm that there is an equivalent replacement and that the system is in fact obsolete.
2. [from source] (SWE-G p.225-226) Decide between advisory and compulsory; for compulsory, define a deadline, an enforcement mechanism and the responsible team.
3. [from source] (SWE-G p.227) Use actionable and relevant warnings and limit them to newly changed lines.
4. [from source] (SWE-G p.229) Prevent backsliding (annotations such as `@deprecated` surfaced in review; visibility lists in the build).
5. [from source] (SWE-G p.227-228) Assign owners and incremental milestones.
6. [extrapolation] "Phases 1-3" of v1 (blocking, communication, removal) were an organization by the agent.

## 4. Designing a routine or class
1. [from source] (CC2 p.62) Ask "what does this class need to hide?".
2. [from source] (CC2 p.62-64) Identify, separate and isolate items likely to change.
3. [from source] (CC2 p.65-67) Assess coupling by size, visibility and flexibility; avoid semantic coupling.
4. [from source] (97TH p.150-151) Readability heuristics from an essay: short methods (about 15 lines according to the author), one responsibility, about 3 parameters.

## 5. What to do when the book does not say
- Declare "NOT COVERED" and, if general knowledge is useful, label it [extrapolation].
