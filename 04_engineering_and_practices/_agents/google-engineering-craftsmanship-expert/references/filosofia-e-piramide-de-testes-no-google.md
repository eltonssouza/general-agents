# Testing Philosophy, Size and Scope, Pyramid and Unit Tests (SWE-G Ch. 11, 12 and 14)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`. Ch. 11 "Testing Overview" (PDF p.149-163, Adam Bender), Ch. 12 "Unit Testing" (p.165-183, Erik Kuefler), Ch. 14 "Larger Testing" (p.202-221, Joseph Graves; overview only).

## 1. Why test (Ch. 11)
- [from source] (SWE-G p.149) Automated tests prevent bugs in production (the later the bug is found, the more expensive it is) and, just as important, support the ability to change; writing tests also improves design, since the test is the first client of the code.
- [from source] (SWE-G p.150) Tests derive value from the confidence engineers place in them; "a bad suite can be worse than none". Google Web Server case (2005): at the time, more than 80% of pushes to production contained user-visible bugs; after requiring tests on every change and running them continuously, the number of emergency pushes dropped by half in a year.
- [from source] (SWE-G p.150) Example of a 100-person team in which each person introduces one bug per month generates five new bugs per working day.
- [from source] (SWE-G p.151-152) Write, run and react; the essential thing is to fix broken tests quickly to maintain confidence. Benefits (p.152-153): less debugging, more confidence in changes, better documentation, simpler reviews, more thoughtful design, fast quality releases.

## 2. Size and scope
- [from source] (SWE-G p.153) Two distinct axes: size (resources required: memory, processes, time) and scope (code paths verified). The book prefers classifying by size (small, medium, large) rather than "unit/integration", because the most desired qualities are speed and determinism.
- [from source] (SWE-G p.154) Small: runs in a single process (in many languages, a single thread), with no sleep, no I/O, no other blocking calls (no network or disk); uses test doubles for heavy dependencies. Footnote (p.163): there is a small allowance, since tests may access a file system if it is hermetic and in memory.
- [from source] (SWE-G p.154) Medium: may have multiple processes, threads and blocking calls, including network, but only to localhost (a single machine).
- [from source] (SWE-G p.155) Large: no localhost restriction; used mainly for end-to-end configuration tests and for legacy components where doubles are impossible. The book also mentions that an "enormous" size exists at Google (footnote 4, p.163).
- [from source] (SWE-G p.155) "All tests should strive to be hermetic": contain all the information to set up, execute and tear down the environment and assume as little as possible about the outside (for example, the execution order). This applies to all sizes, not only small. "A test should be obvious by inspection"; the book discourages conditionals and loops in tests.
- [from source] (SWE-G p.156) Scope: narrow (unit), medium (integration), large (functional, end-to-end, system). The book says it prefers to keep real dependencies when feasible.

## 3. The proportion of the pyramid
- [from source] (SWE-G p.156) "As a good rough guideline" Google aims for about 80% narrow-scoped (unit) tests, 15% medium-scoped (integration) and 5% end-to-end, measured by number of test cases; "each team's mix will be a little different" (caption of Fig. 11-3).
- [from source] (SWE-G p.165) In Ch. 12 another formulation appears: a rule of thumb of about 80% unit tests and 20% tests of broader scope.
- Critical fidelity note: the v1 package stated "70/20/10 pyramid (p.150-154)". Those numbers are NOT in the book. The book's numbers are 80/15/5 (p.156) and 80/20 (p.165), and always as approximate guidance.
- [from source] (SWE-G p.156-157) Anti-patterns: "ice cream cone" (many end-to-end tests, few integration and unit tests) and "hourglass" (many unit and end-to-end tests, few integration tests; linked to tight coupling). The recommended mix serves the goals of productivity and confidence in the product (p.157).

## 4. Rules and metrics
- [from source] (SWE-G p.157) Beyoncé Rule: "test everything that you don't want to break"; includes performance, accessibility, security and failure handling. Testing failures (injecting RPC errors and latency; chaos engineering).
- [from source] (SWE-G p.157-158) Code coverage measures only whether a line was executed, not what happened. An 80% goal tends to become a ceiling and not a floor. The book recommends measuring coverage only from small tests and thinking about behaviors tested.
- [from source] (SWE-G p.155) Flakiness: with a 0.1% chance of spurious failure and 10,000 tests per day, that is 10 investigations per day; rerunning trades CPU for engineering time; "near 1% flakiness tests start to lose value"; at Google the rate stays around 0.15% (thousands of flakes per day). Most flakes come from nondeterminism in the tests themselves (clock, thread scheduling, network latency).
- Fidelity note: the v1 package said flaky tests are "immediately removed from the critical path and quarantined (p.158)"; that policy is not on those pages. [inference] Quarantine is common practice, but it is not attributed to the book here.
- [from source] (SWE-G p.158) Scale: a monorepo with more than two billion lines and about 25 million lines changed per week (half by automated systems); almost no team uses branches; the CI system includes the TAP, described in the book as "Test Automated Platform" (p.158).

## 5. Sustainable unit tests (Ch. 12)
- [from source] (SWE-G p.166) Two problems: brittle tests (they break from a harmless change) and unclear tests.
- [from source] (SWE-G p.166-167) The ideal test is unchanging: pure refactorings, new features and bug fixes should not require changing existing tests; only behavior changes should.
- [from source] (SWE-G p.167-169) Test through the public API (the "front door"); defining "unit" is "more art than science", with three rules of thumb about helpers, free-use packages and support libraries.
- [from source] (SWE-G p.169-170) Test state and not interactions; interaction tests are more brittle; the book prefers real objects to mocks when they are fast and deterministic.
- [from source] (SWE-G p.171-172) Complete and concise tests; it is worth violating DRY if it improves clarity.
- [from source] (SWE-G p.172-174) Test behaviors, not methods; given/when/then structure ("given", "when", "then"); the book mentions in note 6 (p.183) that these components are sometimes called "arrange, act, assert". Name the test after the behavior (starting with "should" is a trick, p.175).
- [from source] (SWE-G p.175-176) Do not put logic in tests; write clear failure messages (p.176-177).
- [from source] (SWE-G p.177-179) DAMP ("Descriptive And Meaningful Phrases") instead of DRY for test code; DAMP is complementary to DRY, not a replacement (p.179). Shared values, shared setup and helpers (p.179-182); test infrastructure must have its own tests (p.182); Google standardized Mockito as the single mock framework in new Java tests (p.182).
- Fidelity note: "understand from top to bottom in under 30 seconds" is NOT in the book. [extrapolation] It can serve as a review heuristic, as long as it is labeled.
- [from source] (SWE-G p.183) TL;DR: unchanging tests; public API; state, not interactions; complete and concise; behaviors, not methods; structure that emphasizes behaviors; names by behavior; no logic; clear failure messages; DAMP over DRY.

## 6. Larger tests (Ch. 14), the essentials only
- [from source] (SWE-G p.221) TL;DR: large tests cover what unit tests do not; they are composed of SUT (system under test), data, action and verification; a good design includes a testing strategy that identifies risks; effort is needed so they do not generate friction in the developer workflow.
- [from source] (SWE-G p.204) Configuration changes are cited as the main cause of major outages at Google.
- [from source] (SWE-G p.208) Dimensions of the SUT: hermeticity and fidelity, among others; (p.209) Webdriver Torso case as an example of the risk of testing in production; (p.217) DiRT (disaster recovery exercise).

## 7. Outside the scope of this reference
- Specific test tools (JUnit, etc.) are in the PDFs of other packages (for example `JUnit-Tutorial.pdf`), not here.
