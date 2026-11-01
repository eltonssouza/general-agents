# API mocking and contract testing (MOCK; SWE-G p.203, p.209-210)

**Nature of the source.** MOCK is a SmartBear marketing e-book (MOCK p.6, p.10-11); it treats the subject at an introductory level and with a vendor bias. Convention: `(MOCK p.N)` = PDF page (= printed). Useful content: p.3-10; p.11 is advertising; p.12 is blank.

## 1. What it is and why use it
- `[from source]` Mocking lets developers and testers build sandbox environments and simulate the behavior of services (MOCK p.3).
- `[from source]` Three terms: **stub**, **mock** and **virtual service** (see definitions in `taxonomia-de-test-doubles-fakes-vs-mocks.md`, section 1; MOCK p.4).
- `[from source]` Virtual services are used mostly in system tests; stubs and mocks in unit/module/acceptance tests; virtual services are usually deployed in an environment shared by several teams, while stubs are per-team instances (MOCK p.4).
- `[from source]` Reasons to simulate: the system is unavailable for security, performance, ownership or maintenance reasons, does not exist yet, or is external with no sandbox or with a per-request cost (MOCK p.4, p.9).

## 2. When to mock
- `[from source]` SmartBear recommends mocking when the service has not been developed yet or when dependencies (system calls, database) are not available (MOCK p.6).
- `[from source]` Scenarios cited: external dependencies and unexpected third-party behavior, isolated development, early functional testing, customer evaluation, avoiding dependencies on future or unavailable APIs (MOCK p.10).
- `[from source]` Geolocation example with Google Maps: a mock returns known results and preserves the external API's usage quota (MOCK p.9).
- `[from source]` Problems with calling real services in tests: connectivity failures, slow suites because of the network, third-party rate limits and lack of a sandbox (MOCK p.9).
- `[from source]` Design phase: the mock is updated every time the API is saved and lets the front end start before the backend; it allows collaborating with stakeholders without waiting for a deploy; it allows demonstrating the API without giving access to the product (MOCK p.8).
- `[from source]` Case study (no numbers): a company with microservices and OAS-based APIs that developed both sides in parallel thanks to mocks (MOCK p.8).
- `[from source]` Outside MOCK, SWE-G recommends **not** using a real third-party API in automated tests and treating that boundary as a point to split tests (SWE-G p.209).
- `[inference]` "Simulate HTTP 500/503/429/malformed payload" is a reasonable application, but MOCK only mentions rate limits as a *problem* of using the real service (p.9); SWE-G recommends testing failures (injecting errors and latency, SWE-G p.157). Do not attribute the list of codes to MOCK.

## 3. Mocking vs. contract testing
- `[from source]` **Contract testing** tests an integration point by checking each application in isolation against a shared understanding documented in a "contract" (the HTTP or queue messages) (MOCK p.5).
- `[from source]` Common form (as Pact does): check that calls to the test double return the same thing that would come from the real application (MOCK p.5).
- `[from source]` It applies where two services communicate; it pays off most with many services in parallel (microservices); it avoids "version hell". The text calls it the "killer app" of microservice development, which is the vendor's opinion (MOCK p.5).
- `[from source]` **Mock drift**: mocks and real services diverge because of rapid changes; contract testing helps keep track and reduces the need to update mocks per microservice layer, which can be updated in less frequent integration tests (MOCK p.7).
- `[from source]` It suggests validating that the recorded mock has not diverged by incorporating contract testing against it (MOCK p.10).
- `[from source]` SWE-G: consumer-driven contract tests define a contract between client and provider; tools cited: Pact and Spring Cloud Contracts; Google, because it uses protocol buffers, does not use them internally (SWE-G p.210).
- `[from source]` SWE-G: the double may not be faithful to the real one's contract; mocks go stale with no signal to the author of the real implementation (SWE-G p.203; p.209).
- `[extrapolation]` The "Pact in CI with a broker" flow, contract versioning and "can-i-deploy" are not in any of the sources.

## 4. Recording and replay
- `[from source]` MOCK: record HTTP/HTTPS traffic from an existing API and create a virtual service from the requests and responses; or record a live interaction and replay it in tests (MOCK p.9). The virtual service can be configured to forward requests to the real API and create virtual operations (MOCK p.10).
- `[from source]` SWE-G: Google uses a larger test in "Record Mode" (runs continuously post-submit) that generates traffic logs and a smaller test in "Replay Mode" for development and pre-submit; requests are matched by *matchers* because of nondeterminism; changing the client requires re-recording (SWE-G p.210).

## 5. What MOCK does not contain
Classification of "static vs. dynamic mocks" (v1, cited as "MOCK p.8-10"), in-memory CRUD with `POST`/`GET` (v1, "MOCK p.9-11"), payment gateway/SMS costs (v1, "MOCK p.7"), credit bureaus, OpenAPI as the "single source of truth" for both sides (the text speaks of OAS as a contract and of SwaggerHub, MOCK p.7-8). These were unsupported v1 claims: treat as `[extrapolation]`.
