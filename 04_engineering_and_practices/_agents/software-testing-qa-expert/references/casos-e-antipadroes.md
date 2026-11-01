# Anti-patterns in tests, mocks, data and load (with page)

Convention: `(SIGLA p.N)` = PDF page (JMETER printed = N − 7). Each item separates what is `[from source]` from what is `[inference]`/`[extrapolation]`. The "cases" are illustrative scenarios **written for this package**, not real cases described in the books.

## 1. Tests
**1.1 Ice cream cone.** Scenario: a prototype that became a product with only manual and E2E tests. `[from source]` The pattern has many E2E tests and few integration/unit tests, is slow and unreliable, and arises from prototypes that never paid off their testing debt (SWE-G p.156); the way out is to migrate to the pyramid in the first days, with unit tests, and then cover with automated integration (SWE-G p.206). `[from source]` Hourglass: many E2E and unit tests, few integration tests, because of coupling (SWE-G p.157).

**1.2 Over-mocking.** Scenario: every dependency becomes a mock with when/verify. `[from source]` Abuse of mocks produced tests that are easy to write, costly to maintain and that rarely found bugs (SWE-G p.185); verifying calls instead of state lets the test pass with a bug and fail on a valid refactoring (SWE-G p.170); prefer real, then fake (SWE-G p.200-201). `[inference]` Counting calls is only justified in the cases listed on p.198-199.

**1.3 Tolerated flaky test.** `[from source]` Rerunning only postpones the cause; near 1% flakiness tests lose value (SWE-G p.155); the typical cause is nondeterminism in the test itself (clock, threads, network) (SWE-G p.155). `[from source]` `sleep` in large tests is naive; prefer polling a state with a timeout, or using events (SWE-G p.219). `[inference]` Quarantining flaky tests is common practice, but it is not a prescription from the book.

**1.4 Coverage as a goal.** `[from source]` Targets such as 80% become a ceiling; coverage only measures execution, not verification (SWE-G p.157-158).

**1.5 Testing the implementation.** `[from source]` Testing private methods or the serialization format makes the test brittle; use the public API (SWE-G p.167-169).

**1.6 Logic and excessive DRY in the test.** `[from source]` Loops, conditionals and helpers that hide data hide bugs; prefer DAMP (SWE-G p.176-179).

**1.7 Stale mocks.** `[from source]` Whoever writes the mock rarely wrote the real one; with no change signal, the mock goes stale (SWE-G p.203); in API vocabulary, *mock drift* (MOCK p.7). Mitigation from the book: fakes maintained by the owners (SWE-G p.193-194; p.203) and contract testing (MOCK p.5; SWE-G p.210).

## 2. Data
**2.1 Production data in test environments.** Scenario: a dump copied to QA. `[from source]` TDM treats masking as the standard (copied data with PII obfuscated, in a non-reversible way) and the use of real data as a last-resort exception, with a request, documented risk and approval; promoting exceptions to standard practice is an anti-pattern (TDM p.6; p.8). `[inference]` A raw dump in QA contradicts both patterns. Specific legal consequences (LGPD, fines) are **not** in TDM; it cites GDPR, HIPAA and PCI (TDM p.6) `[extrapolation]` for the rest.

**2.2 Late data requirements.** `[from source]` Discovering data needs after provisioning the environments causes delays and rework (TDM p.3-4).

**2.3 Synthetic data in higher environments.** `[from source]` Fake data may not match the business rules and loses value in SIT/UAT/performance (TDM p.5).

**2.4 Masking too much or inconsistently.** `[from source]` Masking everything increases the risk of breaking integrity; masking "Simon" as "John" here and not there breaks integrity (TDM p.6).

**2.5 Manual inspection and data spreadsheets.** `[from source]` Validating PII manually is not reliable (TDM p.6-7); data lists age and attract everyone to the same set (TDM p.7); "the hero" and selective automation (TDM p.7).

**2.6 Loose subset.** `[from source]` Needed data goes missing and relationships are lost (TDM p.5).

## 3. Load and performance
**3.1 Too many listeners in the GUI.** `[from source]` Listeners consume a lot of resources and memory; use few; experienced users run in non-GUI (`-n -t -l`) (JMETER p.50). `[inference]` Measuring load with the GUI and open result trees can distort the measurement; the book does not quantify this.

**3.2 Duration Assertion with an unrealistic limit.** `[from source]` In the example, 100 ms produced failures and 2000 ms let almost everything pass (JMETER p.29-30); the limit must come from the requirement, not from the example `[inference]`.

**3.3 Duplicated samplers.** `[from source]` Use variables and loops in the same sampler instead of several nearly identical ones (JMETER p.50).

**3.4 Load without fidelity.** `[from source]` Load testing is an emergent property and must resemble production; when comparing versions, the environment must be equivalent (SWE-G p.213).
