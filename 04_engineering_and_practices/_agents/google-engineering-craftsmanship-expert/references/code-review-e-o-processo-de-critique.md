# Code Review and the Critique Tool (SWE-G Ch. 9 and Ch. 19)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`. Ch. 9 "Code Review" (PDF p.121-133, Tom Manshreck and Caitlin Sadowski) and Ch. 19 "Critique: Google's Code Review Tool" (PDF p.279-288).

## 1. Flow and LGTM (Ch. 9)
- [from source] (SWE-G p.121) At Google essentially every change is reviewed before commit (precommit review) and every engineer is responsible for initiating and doing reviews. The end goal is to obtain the "looks good to me" (LGTM), which works as a permission "bit" required for the commit, combined with other bits.
- [from source] (SWE-G p.121-122) Typical steps: the author creates the change and the snapshot; self-review and automatic comments; sends it to reviewers; reviewers comment (some comments require resolution, others are informational); the author iterates; LGTM; commit after resolving the comments and having approval. By default one LGTM is enough (p.122).
- [from source] (SWE-G p.122) "Code is a liability": code is a maintenance liability; rewriting utilities from scratch is frowned upon; code review is not the moment to rediscuss earlier design decisions.

## 2. The three aspects that require approval
- [from source] (SWE-G p.122-123) A change has three aspects: (1) a correctness check and understanding by another engineer, which generates the LGTM bit; (2) approval from an owner of the directory, which can be implicit if the author is already an owner; (3) language "readability" approval, which can also be implicit if the author has readability.
- [from source] (SWE-G p.123) The text says that, although it seems heavy, in most reviews one person takes on all three roles, and the three bits can be combined in any combination (an author who is an owner with readability needs only an LGTM from another engineer; an intern needs an owner with readability). The separation exists for scale and flexibility. When there is more than one approval, it is customary to obtain the peer's LGTM first and then the owner/readability one.
- Fidelity note: the v1 package said the "three approvals are always mandatory and independent" and drew them as three gates in sequence. The book describes aspects that may fall on a single person and may be implicit.
- [from source] (SWE-G p.123-124) OWNERS: files named OWNERS list the people responsible for a directory and its children; the relation is hierarchical and additive (the union of the OWNERS above); "ownership" is seen as stewardship (care), not possession; a small, focused list is recommended. The set of people in the root OWNERS can act as global approver of LSCs (p.124).

## 3. Benefits and best practices
- [from source] (SWE-G p.124-125) Benefits listed: correctness, comprehensibility, consistency, psychological promotion of collective ownership, knowledge sharing and a historical record. The book states that checking correctness is not the main benefit reaped at Google (p.125).
- [from source] (SWE-G p.125) Deference to the author on the approach; the reviewer only proposes an alternative if it improves understanding or functionality; approve changes that improve the codebase instead of waiting for a "perfect" solution.
- [from source] (SWE-G p.126) In doubts about comprehension, "the customer is always right".
- [from source] (SWE-G p.128) Expectation of feedback within 24 business hours; treat each comment as a TODO; do not reply piecemeal; PTAL to keep the debate civil (p.128-129).
- [from source] (SWE-G p.129) Small changes: the "probably most important" practice to keep review agile. "Small" should be around 200 lines of code; most changes should receive first feedback in about one day; about 35% of changes are in a single file. The book acknowledges costs (difficulty with large features; techniques with more overhead) and treats this as an optimization.
- [from source] (SWE-G p.117) Google has no tool that automatically rejects a change above a line limit; reviewers may refuse large changes.
- [from source] (SWE-G p.288) Footnote 2 of Ch. 19: most changes are small (fewer than 100 lines).
- [from source] (SWE-G p.129-130) Good description: first line as a summary (type of change), followed by what and why; a bare "Bug fix" does not help; update the description when there is a new decision.
- [from source] (SWE-G p.130) Most reviews have exactly one reviewer; more reviewers have diminishing returns. Automate (presubmits, static analysis) so reviewers focus on what matters.
- [from source] (SWE-G p.131-132) Types of review: greenfield (requires a prior design review, tests of all endpoints, proper OWNERS), behavioral changes and optimizations (updated tests; benchmarks where applicable), bug fixes and rollbacks (do not mix in other adjustments; rollbacks are fast but also require review), refactorings and LSCs (review of a machine-generated change with scope limited to local concerns).
- [from source] (SWE-G p.133) TL;DR: correctness, comprehension and consistency; optimize for the reader; maintain professionalism; knowledge sharing; automation to scale; historical record.

## 4. Critique (Ch. 19)
- [from source] (SWE-G p.279) Design principles: simplicity (the most influential), foundation of trust, generic communication and integration with the workflow.
- [from source] (SWE-G p.280) It was chosen not to create a "Code Central" tool; the focus is review, with links to other systems. Comments are, by default, "unresolved"; reviewers draft and publish atomically; anyone can comment ("drive-by review"); in emergencies the author can force-commit and review afterwards.
- [from source] (SWE-G p.281-282) Diffs with syntax highlighting, cross-references (Kythe), intraline diff, move detection; analyzer results appear on the change page with applicable fix suggestions (p.282).
- [from source] (SWE-G p.283) Tools cited around Piper: Cider, Code Search, Tricorder, Rapid, Zapfhahn. GwsQ distributes reviews by alias; reviewer selection considers owner, familiarity and availability.
- [from source] (SWE-G p.284) Presubmits run when requesting review and when committing (and not on every snapshot, like the Tricorder checks); common hooks add mailing lists, run tests and enforce invariants; a presubmit failure blocks sending for review or the commit.
- [from source] (SWE-G p.285) "Attention set": the set of people on whom the change is blocked, shown in bold.
- [from source] (SWE-G p.286) Three-part scoring: LGTM, Approval and number of unresolved comments. LGTM and Approval are "hard" requirements that only reviewers grant; unresolved comments are "soft" requirements. Every change requires an LGTM regardless of approval, guaranteeing at least two pairs of eyes. "Needs More Work" and "LGTM++" were removed.
- [from source] (SWE-G p.287) Gerrit is used by open source projects and outside the monorepo; it allows a veto with a -2 score.
- [from source] (SWE-G p.288) TL;DR: trust and communication are the core; tight integration with other tools; small optimizations, like the attention set, reduce friction.

## 5. Boundary
- The `nit:` prefix as a Critique convention is not in the book (the v1 package attributed this to p.286). [extrapolation] Prefixes like "nit:" are a common industry convention.
- "200 to 400 lines" as a ceiling is not in it; only "about 200 lines" as the size of a small change (p.129).
- It does not say that the reviewer is "not even notified" when a test breaks; the book says a presubmit failure blocks sending for review (p.284).
