# Test Doubles: Fakes, Stubs and Interaction Testing (SWE-G Ch. 13)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`, Ch. 13 "Test Doubles" (PDF p.184-200, Andrew Trenk and Dillon Bly).

## 1. Concepts
- [from source] (SWE-G p.184) A test double is an object or function that replaces a real implementation in a test. The chapter avoids the term "mocking" because it is ambiguous. Its use brings three implications: testability, applicability and fidelity.
- [from source] (SWE-G p.185) Google's experience: mocking frameworks seemed like "a hammer for every nail"; after years and many tests, the cost was realized (constant maintenance, little value in finding bugs). The "pendulum" is now swinging the other way (less use of mock frameworks). The book admits that the application varies a lot between teams.
- [from source] (SWE-G p.186) Seam: a point that allows different dependencies to be used in the test; dependency injection is a common technique. Guice and Dagger are cited (p.187). In dynamic languages (Python, JavaScript) it is possible to replace functions dynamically (p.187).
- [from source] (SWE-G p.187) Mocking framework: a library that makes it easier to create doubles; Mockito (Java), googlemock (C++) and unittest.mock (Python) are cited.
- [from source] (SWE-G p.188-189) Three techniques: faking (a lightweight implementation that behaves like the real one, for example an in-memory database), stubbing (giving behavior to a function, hardcoding returns) and interaction testing (validating how a function is called, without executing its implementation).
- Fidelity note: the v1 package used the taxonomy "Fake, Stub, Mock, Spy, Dummy" and attributed it to Meszaros in Ch. 13 (p.184-188). That five-item taxonomy does NOT appear in the chapter; it uses the three techniques above.

## 2. Prefer realism over isolation
- [from source] (SWE-G p.189) The first choice is the real implementation of the dependencies; the style is called "classical testing", as opposed to "mockist testing". Google found the mockist style hard to scale.
- [from source] (SWE-G p.190) Realistic tests give more confidence; a bug in a real implementation may break many tests and this is considered good (it indicates the code would not work in production). `@DoNotMock` case (Error Prone): it lets the API owner declare that a type must not be mocked; mocks duplicate API behavior and restrict its evolution (p.190-191).
- [from source] (SWE-G p.191-192) When to use the real implementation: if it is fast, deterministic and has simple dependencies (value objects such as money, dates, lists). Factors: execution time, determinism (non-hermetic code, system clock) and construction of dependencies.

## 3. Fakes
- [from source] (SWE-G p.192) If the real implementation is not viable, the best option is usually a fake, preferred over other techniques because the SUT should not be able to distinguish between real and fake.
- [from source] (SWE-G p.193) Who should write it: "the team that owns the real implementation should write and maintain the fake". There is a cost trade-off (few users may not justify it). Create fakes at the root of what is not viable to use in a test (for example, the database API, not each class that calls it).
- [from source] (SWE-G p.194) Fidelity: the fake must maintain fidelity to the API contract (same output and same state changes) from the test's point of view; fail fast for unsupported paths; fakes must have their own tests, for example contract tests run against the real implementation and the fake.
- [from source] (SWE-G p.194-195) With no fake available: ask the API owner; wrap the API in a class and fake that class; or use the real one. A fake can be seen as an optimization.

## 4. Stubbing and interaction testing
- [from source] (SWE-G p.195-196) Excess stubbing makes tests unclear, brittle and less effective (there is no way to ensure fidelity to the real contract; no state).
- [from source] (SWE-G p.197) Stubbing is appropriate when a function must return a specific value to drive the SUT into a state, including errors that are hard to provoke with a real or fake; each stubbed function must have a direct relation to the assertions. Real or fake are still preferred.
- [from source] (SWE-G p.197-198) Prefer state testing to interaction testing; excessive interaction tests are jokingly called "change-detector tests".
- [from source] (SWE-G p.198) When interaction testing is appropriate: when state testing cannot be done (as a last resort) or when the number/order of calls matters (for example, verifying that a cache reduces calls to the database). It must be complemented by larger-scope tests.
- [from source] (SWE-G p.198-200) Best practices: interaction testing only for functions that change state (sendEmail, saveRecord); avoid overspecification (verify only what is needed for the behavior under test).
- [from source] (SWE-G p.200) TL;DR: prefer the real implementation to doubles; a fake is usually the ideal solution if the real one cannot be used; excess stubbing generates unclear and brittle tests.

## 5. What the chapter does NOT say
- It does not say "avoid mocking frameworks whenever possible" as a literal quote; the v1 package presented that sentence in quotes. What the book says is that excess use causes costs and that the pendulum swings toward more realistic tests (p.185).
- It does not say that mocks should be used "exclusively" for I/O timeouts; it says stubbing can simulate values and errors that are hard to provoke (p.197).
- It does not contain the code `verify(dao).findById(10); verify(cache).put(10, user);` nor the story of the `NullPointerException` in staging. Those examples were v1 illustrations. [inference] They may be used as the agent's own examples, without a page.
