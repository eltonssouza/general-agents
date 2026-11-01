# Test doubles: real, fake, stub and interaction (SWE-G ch. 13; MOCK p.4)

Convention: `(SWE-G p.N)` and `(MOCK p.N)` = PDF page. Ch. 13 = SWE-G p.184-201. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. The book's vocabulary (SWE-G) and what is NOT in it
- `[from source]` **Test double** is an object or function that replaces a real implementation in the test; the chapter avoids using "mocking" as a synonym because the term also designates more specific aspects (SWE-G p.184).
- `[from source]` Instead of a list of types, the chapter organizes three **techniques**: **faking**, **stubbing** and **interaction testing** (SWE-G p.188-189), and puts the **real implementation** first (SWE-G p.189).
- `[from source]` Mock = "a test double whose behavior is specified inline in the test", created by a *mocking framework* (Mockito in Java, googlemock in C++, `unittest.mock` in Python) (SWE-G p.187). "Interaction testing" is sometimes called "mocking" (SWE-G p.189).
- `[extrapolation]` **Gerard Meszaros's taxonomy** (*xUnit Test Patterns*, 2007): Dummy, Stub, Spy, Mock and Fake. **Neither SWE-G (no "Dummy" or "Spy", no mention of Meszaros) nor MOCK contains these five types.** v1 attributed the definitions of Dummy and Spy to "MOCK p.2" and "SWE-G p.241-243"; those pages do not say that (MOCK p.2 is the table of contents; SWE-G p.241 is outside the testing chapters, which end on p.221).
- `[from source]` MOCK uses another vocabulary, from tool marketing: **stub** (a minimal version of the service with predictable data, often handwritten), **mock** (verifies outputs against expectations, focuses on interactions and usually has state, e.g. counting calls) and **virtual service** (a stand-in created from a definition such as OAS or from recorded traffic, remotely accessible and shared across teams) (MOCK p.4).
- `[inference]` The two books use "mock" with different meanings (inline in a unit test vs. a simulated service). When answering, state which meaning is in use.

## 2. The impact of doubles and Google's stance
- `[from source]` Three concerns when using doubles: **testability** (the code must allow swapping), **applicability** (misuse produces brittle, complex tests; in many cases the real implementation should be preferred) and **fidelity** (how close the double is to the real one) (SWE-G p.184-185).
- `[from source]` Perfect fidelity is not always possible; tests with doubles need to be complemented by larger-scope tests that exercise the real implementation (SWE-G p.185).
- `[from source]` Google learned "the hard way" the danger of abusing mocking frameworks: tests easy to write, costly to maintain, that rarely found bugs; the pendulum now swings toward more realistic tests (SWE-G p.185).
- `[from source]` Seams and dependency injection: the dependency is passed to the object, not instantiated by it, which allows replacing it in the test (SWE-G p.186-187). In dynamic languages, individual functions can be swapped (SWE-G p.187).
- `[from source]` **Classical** style (prefer real implementations) vs. **mockist** (prefer mocking frameworks): Google considers the mockist style hard to scale (SWE-G p.189-190).

## 3. Prefer realism to isolation
- `[from source]` The real implementation is the first choice; it gives more fidelity and avoids boilerplate code that goes out of sync with the real one (SWE-G p.189).
- `[from source]` A bug in the real implementation that breaks the test is desirable: it is the signal that the code would fail in production (SWE-G p.190).
- `[from source]` `@DoNotMock` annotation (ErrorProne): lets the API owner declare that a type must not be mocked; scattered mocks limit the API's evolution and can violate the contract (e.g. returning null where it never would) (SWE-G p.190-191).
- `[from source]` When to use the real one: if it is fast, deterministic and has simple dependencies (e.g. value objects); criteria: execution time, determinism (clock, network, threads), cost of building the dependencies (SWE-G p.191-192).

## 4. Fakes
- `[from source]` **Fake** = a lightweight implementation of the API that behaves like the real one but is not suitable for production (e.g. in-memory database) (SWE-G p.188). If the real one is not viable, the fake is usually the best option (SWE-G p.192-193).
- `[from source]` The **owner** team of the real implementation should write and maintain the fake; create the fake at the root of what cannot be used in tests (e.g. the database API), not in each calling class (SWE-G p.193).
- `[from source]` The fake's fidelity is measured against the **API contract**: same input, same output and same state changes; latency and resource consumption may differ; rare functionality may fail fast (SWE-G p.194).
- `[from source]` Fakes must have their own tests; one way is to write tests against the public interface and run them against the real one and the fake (the book's "contract tests") (SWE-G p.194).
- `[from source]` With no fake available: ask the owners; if there is none, wrap the API calls in a class and make a fake of that class; or use the real one; or another technique (SWE-G p.194-195).
- `[from source]` The fake can be seen as an optimization: it only pays off if the gain exceeds the cost of creating and maintaining it (SWE-G p.195).

## 5. Stubbing
- `[from source]` Giving behavior (return values) to a function, typically via a framework (`when(...).thenReturn(...)` in the example) (SWE-G p.188-189).
- `[from source]` Dangers of excess: **unclear** tests, **brittle** tests (leak implementation details) and **less effective** tests (duplicate the contract with no guarantee of fidelity; do not keep state) (SWE-G p.195-196).
- `[from source]` Appropriate for getting the system to a state, simulating returns or errors that the real one or the fake do not produce; each stubbed function should be directly related to the assertions, with few stubbed functions (SWE-G p.197).

## 6. Interaction testing
- `[from source]` Validates **how** a function is called (not at all, too many times, wrong arguments) without running the implementation, via `verify(...)` (SWE-G p.189).
- `[from source]` Prefer **state testing**; interaction testing does not prove the system works, only that it called something, and it leaks details; tests that abuse it are informally called **change-detector tests** (SWE-G p.197-198).
- `[from source]` Legitimate cases: neither a real one nor a fake can be used (fallback), or the number/order of calls matters (e.g. verifying that a cache reduces calls to the database) (SWE-G p.198).
- `[from source]` Best practices: do interaction testing only of functions that **change state** in the outside world (e.g. `sendEmail()`, `saveRecord()`), not those that only query (`getUser()`); avoid over-specifying arguments and verified functions (SWE-G p.198-200).
- `[from source]` Chapter TL;DR: prefer the real one; a fake is usually ideal when the real one does not fit; excessive stubbing and interaction testing should be avoided when possible (SWE-G p.200-201).

## 7. Risk note in ch. 14
- `[from source]` "Unfaithful doubles": whoever writes the mock rarely wrote the thing being mocked and may have misunderstood the contract; mocks go stale if the owner changes the implementation; if teams provide fakes of their own services, the concern diminishes (SWE-G p.203).

## 8. v1 items without backing
| Claim | Status |
|---|---|
| Dummy/Stub/Spy/Mock/Fake taxonomy "from the book" | `[extrapolation]` (Meszaros), not in SWE-G or in MOCK |
| `ConcurrentHashMap` as an example of a fake | The book's example is `FakeFileSystem` with a `HashMap` (SWE-G p.192-193) |
| `verify(paymentGateway, times(1)).chargeCreditCard(...)` as the book's example | The book uses `verify(mockAuthorizationService).lookupUser(USER_ID)` (SWE-G p.189) and `chargeCreditCard` in a stub (p.187) |
| "Golden rule" and "common conformance test suite" | The book recommends owner + fake tests run against the real one and the fake (SWE-G p.193-194); "golden rule" is v1 rhetoric |
| Mocks only for side effects or I/O failures | Approximation of p.197-199; the book also admits the fallback when there is neither a real one nor a fake |
