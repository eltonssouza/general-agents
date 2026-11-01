# Glossary (v2, audited)

Convention: `(SIGLA p.N)` = **PDF** page (JMETER printed = N − 7; see `INDEX.md`). Each term carries the label: `[from source]` (checked on the page), `[inference]` or `[extrapolation]`. Definitions are in our own words; consult the source text for the original.

### A
- **A/B diff test**: a large test that sends the same traffic to the base and candidate versions and compares the responses; differences must be approved by a person `[from source]` (SWE-G p.214-215).
- **Assertion (JUnit 4)**: a method of `org.junit.Assert` that verifies an expected result `[from source]` (JUNIT p.3-4). **Assertion (JMeter)**: an element that validates a sampler's response `[from source]` (JMETER p.18).

### B
- **Beyoncé Rule**: "if you liked it, you should have put a test on it"; test everything you do not want to break `[from source]` (SWE-G p.157).
- **Brittle test**: a test that fails in the face of a harmless change to production code, with no real bug `[from source]` (SWE-G p.166).

### C
- **Canary analysis / prober**: checks in production; a prober runs read assertions against production, a canary compares metrics of the updated part with the baseline `[from source]` (SWE-G p.215-216).
- **Categories (JUnit 4)**: `@Category` with `@IncludeCategory`/`@ExcludeCategory` to filter tests `[from source]` (JUNIT p.7-8).
- **Change-detector test**: nickname given to tests that abuse interaction testing and break on any change `[from source]` (SWE-G p.198).
- **Classical vs. mockist testing**: preferring real implementations vs. preferring mocking frameworks `[from source]` (SWE-G p.189).
- **Contract testing**: testing each application in isolation against a shared contract of the messages `[from source]` (MOCK p.5); **consumer-driven**: the client defines the contract, the provider executes it; Pact and Spring Cloud Contracts are cited `[from source]` (SWE-G p.210).

### D
- **DAMP**: "Descriptive And Meaningful Phrases"; in tests, duplication is tolerated if the test becomes clearer; complements DRY `[from source]` (SWE-G p.177-179).
- **Data masking**: copying the dataset with PII/sensitive data obfuscated in a non-reversible way, keeping a production-like appearance `[from source]` (TDM p.6). **Data encryption**: reversible obfuscation by key `[from source]` (TDM p.6).
- **Data profiling**: automatic discovery of schema, relationships and PII risks `[from source]` (TDM p.4). **Data sub-setting**: reducing the data footprint by a repeatable criterion `[from source]` (TDM p.5). **Data virtualization**: a virtual copy based on deltas over the source `[from source]` (TDM p.5). **Data views**: locatable, reserved data pools `[from source]` (TDM p.7). **Data exemption**: exceptional use of production data with a recorded request, risk and window `[from source]` (TDM p.8).
- **Dependency injection**: passing the dependencies to the object instead of instantiating them in it; creates *seams* `[from source]` (SWE-G p.186).
- **Dummy** and **Spy**: types in Meszaros's taxonomy (a parameter that is never used; a wrapper that records calls) `[extrapolation]`; they **do not appear** in SWE-G or in MOCK.
- **Duration Assertion (JMeter)**: fails the sample if the response takes longer than a limit in ms; example with 100 ms and then 2000 ms `[from source]` (JMETER p.29-30).

### F
- **Fake**: a lightweight implementation of the API, similar to the real one, unsuitable for production (e.g. in-memory database) `[from source]` (SWE-G p.188).
- **Fidelity**: how close the double or test environment is to the real behavior `[from source]` (SWE-G p.184-185, p.202).
- **Flaky test**: a test that fails nondeterministically `[from source]` (SWE-G p.154-155).

### H
- **Hermetic**: contains everything it needs to set up, run and tear down its environment `[from source]` (SWE-G p.155); **hermetic SUT** is isolated from other components and from external traffic `[from source]` (SWE-G p.208).
- **Hourglass / ice cream cone**: anti-patterns of test mix `[from source]` (SWE-G p.156-157).
- **Hyrum's Law**: the effective API is all visible behavior, not only the declared contract `[from source]` (SWE-G p.204).

### I
- **Interaction testing**: verifying how a function was called; contrasts with **state testing**, which verifies the resulting state `[from source]` (SWE-G p.189, p.197).

### L
- **Larger tests**: tests without the small/medium constraints (can be slow, non-hermetic, nondeterministic) `[from source]` (SWE-G p.202).
- **Little's Law**: N = X × R `[extrapolation]` (queueing theory; not in JMETER).
- **Listener (JMeter)**: displays the results; only collects from samplers at its level or below `[from source]` (JMETER p.17). **Logic controller**: defines the order of the samplers `[from source]` (JMETER p.16-17).

### M
- **Mock (SWE-G)**: a test double whose behavior is specified inline by a mocking framework `[from source]` (SWE-G p.187). **Mock (MOCK)**: verifies outputs against expectations, focuses on interactions, usually has state `[from source]` (MOCK p.4).
- **Mock drift**: mocks and real services diverge because of rapid changes `[from source]` (MOCK p.7).
- **Small / medium / large**: one process / one machine (localhost) / no restriction `[from source]` (SWE-G p.153-155).

### P
- **PII**: personal data that identifies someone; TDM examples: full name, address, email, phone `[from source]` (TDM p.4).
- **80/15/5 pyramid**: Google's approximate mix of unit, integration and end-to-end tests `[from source]` (SWE-G p.156). It is not 70/20/10.

### R
- **Ramp-up period (JMeter)**: the time JMeter takes to start all the threads `[from source]` (JMETER p.15). **Loop count**: number of iterations `[from source]` (JMETER p.15).
- **Record/Replay**: recording the traffic of external services in a larger test and replaying it in smaller tests, with *matchers* `[from source]` (SWE-G p.210); also in MOCK p.9.
- **Rule (JUnit 4)**: `@Rule` on a `public` field changes how each test method runs (`ErrorCollector`, `ExpectedException`, `TestName`) `[from source]` (JUNIT p.7).

### S
- **Sampler (JMeter)**: an element that sends requests to servers `[from source]` (JMETER p.15). **Timer**: defines the wait between requests `[from source]` (JMETER p.18).
- **Seam**: a point that allows swapping dependencies in the test `[from source]` (SWE-G p.186).
- **Stub (SWE-G)**: giving behavior (return values) to a function `[from source]` (SWE-G p.188). **Stub (MOCK)**: a minimal version of a service with predictable data `[from source]` (MOCK p.4).
- **SUT (system under test)**: in a large test, the real system under test, from single-process to multi-machine `[from source]` (SWE-G p.207-208).
- **Suite (JUnit 4)**: `@RunWith(Suite.class)` + `@Suite.SuiteClasses` `[from source]` (JUNIT p.7).

### T
- **Test double**: an object or function that replaces a real implementation in a test `[from source]` (SWE-G p.184).
- **Test Data Management (TDM)**: managing test data for "data-ready" environments `[from source]` (TDM p.1). **Data factory**: a set of TDM methods `[from source]` (TDM p.3).
- **Thread Group (JMeter)**: root of the plan; defines threads, ramp-up, loop count and error behavior `[from source]` (JMETER p.15).
- **Test Certified**: Google's internal program of five levels of testing maturity `[from source]` (SWE-G p.160-161).
- **Size vs. scope**: resources required vs. code verified `[from source]` (SWE-G p.153, p.156).
