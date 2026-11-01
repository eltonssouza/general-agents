# Testing fundamentals and the pyramid (SWE-G, ch. 11 and 12)

Convention: `(SWE-G p.N)` = page of the 408-page **PDF** (no printed numbering). Ch. 11 = p.149-164; ch. 12 = p.165-183. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Why test
- `[from source]` Automated tests are not only for finding bugs: they sustain the ability to **change** software with confidence (refactor, add features, redesign) (SWE-G p.149).
- `[from source]` Writing tests improves design: the test is the code's first client and reveals excessive coupling, an insufficient API and edge cases (SWE-G p.149; p.153).
- `[from source]` The value of a suite comes from the confidence engineers place in it; a bad suite can be worse than none (SWE-G p.150).
- `[from source]` The GWS story: the policy of continuous automated testing, instituted in 2005, cut emergency pushes in half within a year (SWE-G p.150). The book is inconsistent about the date (2005 on p.150 and p.160; "2003" on p.205). Do not generalize the numbers to other teams `[inference]`.
- `[from source]` Benefits cited: less debugging, more confidence in changes, tests as executable documentation, simpler reviews, better design, fast releases (SWE-G p.152-153).
- `[from source]` What to do when a test breaks: fixing it within minutes preserves confidence; letting broken tests pile up nullifies the value (SWE-G p.152).

## 2. Size and scope (two distinct dimensions)
- `[from source]` **Size** = resources the test requires (memory, processes, time); **scope** = how many lines of code it verifies. Google classifies every test by size and always encourages the smallest possible (SWE-G p.153).
- `[from source]` Small: runs in **one process** (in many languages, one thread), with no `sleep`, no I/O, no blocking calls, no network or disk; uses test doubles for anything heavy (SWE-G p.154).
- `[from source]` Medium: may use several processes, threads and blocking calls, but only to `localhost` (a single machine) (SWE-G p.154).
- `[from source]` Large: without the `localhost` restriction, may span several machines; reserved for end-to-end configuration and for legacy components with no way to use doubles (SWE-G p.155).
- `[from source]` Footnote: Google in practice has a fourth size, "enormous", whose difference from large is historical (SWE-G p.163).
- `[from source]` Scope: narrow (unit), medium (integration between a few components), broad (functional/E2E/system). A broad-scope test can be small if it uses doubles for out-of-process dependencies (SWE-G p.156).
- `[from source]` Google defines small/medium/large as constraints that the infrastructure can **enforce** (e.g. a security manager in Java tests makes a small test that opens a network connection fail) (SWE-G p.153, p.156).

## 3. The pyramid: 80/15/5 (not 70/20/10)
- `[from source]` Google's approximate guide: about **80%** narrow-scope unit tests, **15%** integration and **5%** end-to-end, by count of cases; each team's mix varies (SWE-G p.156).
- `[from source]` In ch. 12 the rule of thumb is "about 80% unit and 20% of broader scope" (SWE-G p.165).
- `[from source]` Anti-patterns: **ice cream cone** (many E2E, few integration/unit tests; slow and unreliable) and **hourglass** (many E2E and unit tests, few integration tests; occurs when coupling prevents instantiating isolated dependencies) (SWE-G p.156-157).
- `[from source]` The book recommends fitting the mix to the local architectural and organizational reality; unit tests do not verify contracts between systems of different teams (SWE-G p.157).
- `[from source]` The ice cream cone usually arises when the code starts as a prototype with manual tests and nobody pays off the testing debt (SWE-G p.156; p.206).
- `[extrapolation]` The 70/20/10 ratio circulates in blogs and presentations; it is **not in these chapters** and must not be cited as from the book.

## 4. Flaky tests
- `[from source]` Flaky test = fails nondeterministically; sources of nondeterminism: clock, thread scheduling, network latency (SWE-G p.154-155).
- `[from source]` The book's numeric example: with a 0.1% chance of spurious failure per test and 10,000 tests per day, that is 10 investigations per day. Near 1% flakiness, tests start to lose value; Google's rate is around 0.15% (SWE-G p.155).
- `[from source]` Automatically rerunning trades CPU for engineering time; it only postpones the root cause (SWE-G p.155).
- `[from source]` Every test should be **hermetic**: contain the information to set up, run and tear down the environment, without depending on execution order or on a shared database (SWE-G p.155).
- `[from source]` `sleep()` and `setTimeout()` in tests are naive heuristics; prefer polling for the state transition with a safety timeout (SWE-G p.159, p.219).
- `[inference]` "Immediate quarantine" of flaky tests is not a prescription from the book: the book talks about fixing broken tests quickly (p.152) and about eliminating nondeterminism at Test Certified level 5 (p.161).

## 5. Other rules from ch. 11
- `[from source]` Beyoncé Rule: if a property matters, write a test for it (including performance, security, accessibility and failure handling) (SWE-G p.157).
- `[from source]` Test failure: simulate exceptions in unit tests and inject RPC errors or latency in integration/E2E tests (SWE-G p.157).
- `[from source]` Code coverage measures executed lines, not what was verified; targets such as 80% become a ceiling; the book suggests measuring coverage of small tests only and thinking in terms of behaviors (SWE-G p.157-158).
- `[from source]` Brittle tests (that over-specify or have boilerplate) resist change; abusive use of mocks is cited among the worst cases (SWE-G p.159).
- `[from source]` Treat tests as production code: performance goals, refactoring the slow ones, incentives (SWE-G p.159).
- `[from source]` Limits of automated testing: human evaluation for search/audio/video quality; exploratory testing and, after finding the defect, an automated test to prevent regression (SWE-G p.162).
- `[from source]` Avoid flow control (conditionals and loops) in tests (SWE-G p.155; p.175-176).

## 6. Good unit tests (ch. 12)
- `[from source]` Goals: tests that do not need to change when the system is refactored, gains a feature or gets a bug fix; only behavior changes require touching the test (SWE-G p.166-167).
- `[from source]` **Test through the public API**: invoke the system as the user would, do not call private methods (SWE-G p.167-169); note 2 (printed on p.183) calls this the "front door" principle (SWE-G p.183).
- `[from source]` **State, not interaction**: interaction tests are more brittle; prefer verifying the resulting state (SWE-G p.169-170).
- `[from source]` **Complete and concise** tests; **behaviors, not methods**; given/when/then structure (the book notes it is also called "arrange, act, assert"); the test name describes the action and the expected result; a single "when" action in most tests (SWE-G p.171-175; p.183 note 6).
- `[from source]` No logic in the test; clear failure messages with expected versus actual (SWE-G p.175-177).
- `[from source]` **DAMP, not DRY**: a bit of duplication is acceptable if it makes the test more descriptive; DAMP complements DRY, it does not replace it (SWE-G p.177-179).
- `[from source]` Shared values: prefer helpers/builders that define only what the test cares about over ambiguous constants; shared setup is for building the object under test, not for values the test depends on (SWE-G p.179-181).
- `[from source]` Shared test infrastructure must have its own tests; standardize libraries early (Google started requiring Mockito in new Java tests) (SWE-G p.182).
- `[inference]` "AAA structure" is just another name for given/when/then cited in a note; the book does not treat it as a separate rule.

## 7. Numbers and terms that v1 said were from the book, but are not
| v1 claim | Status |
|---|---|
| 70/20/10 | **No**: the book says 80/15/5 (p.156) and 80/20 (p.165) |
| "mathematical certainty" that behavior is preserved | Exaggeration; the book speaks of confidence |
| Hyrum's Law as the cause of ordering flakiness | The book cites Hyrum's Law in ch. 14 (p.204, 214), not as a cause of flakiness here |
| Run in "< 50 ms" | No number in the book |
| `FakeClock` | Does not appear; the book says to use a double with a fixed time in place of the system clock (p.192) |
