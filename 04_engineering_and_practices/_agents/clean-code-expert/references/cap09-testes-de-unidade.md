# Cap. 9 — Testes de Unidade (Unit Tests)

Source: CL ch. 9, PDF p.124-135 (opening on p.124; conclusion and bibliography on p.135).

## Historical context
- In 1997 nobody talked about TDD. Tests were throwaway code, like the manual test of `Timer::ScheduleCommand` in C++, typing in a melody and checking it on the screen. The author threw the test code away (CL p.124-125).
- Today he would isolate the code from the operating system, simulate the time functions to control them completely, and check boolean flags as time advanced. The tests would live in the same package as the code and be runnable by anyone (CL p.125).
- In the rush to adopt tests, many forgot the subtle points of writing **good** tests (CL p.125).

## The three laws of TDD
Text of the Brazilian edition, checked on the image (CL p.125):
1. **First Law**: you may not write production code until you have written a failing unit test.
2. **Second Law**: you may not write more of a unit test than is sufficient to fail, "e não compilar é falhar" (and not compiling is failing).
3. **Third Law**: you may not write more production code than is sufficient to pass the currently failing test.
- Source in a footnote: *Professionalism and Test-Driven Development*, R. C. Martin, IEEE Software, May/June 2007 (CL p.125).
- The laws lock the programmer into a cycle of about **thirty seconds**, with the tests only a few seconds ahead of the code (CL p.126).
- Result: dozens of tests a day, hundreds a month, thousands a year, covering almost all the production code. The volume, which can rival that of production code, becomes a management problem (CL p.126).

## Keeping tests clean
- Real case: a team decided that the test code would not follow the quality standard of production (the motto was quick and dirty). Dirty tests are equivalent to having no tests, or are worse (CL p.126).
- Tests must change along with production. The dirtier they are, the harder it is to change them and the more time is spent fitting in new tests. The maintenance cost grew with every release until the team discarded the whole suite (CL p.126).
- Without a suite: defects increased, fear of change set in, cleaning of production code stopped and the code rotted (CL p.126).
- Moral: test code is as important as production code. It is not a second-class citizen and demands thought, design and care (CL p.127).

## Tests enable the -ilities
- It is the unit tests that keep the code flexible, maintainable and reusable, because with tests there is no fear of changing the code (CL p.127).
- The greater the coverage, the smaller the fear. With tests you can improve even a tangled architecture (CL p.127).
- Bad tests compromise the ability to change and to improve the structure. The worse the tests, the worse the code gets (CL p.127).

## Clean tests
- What makes a test clean: "legibilidade, legibilidade e legibilidade" (readability, readability and readability), perhaps even more than in production code. Readability comes from clarity, simplicity and density of expression (the translation's terms: clareza, simplicidade e consistência de expressão): saying a lot with as few expressions as possible (CL p.127).
- Listing 9-1 (FitNesse) has duplication [G5] in the calls to `addPage` and `assertSubString` and irrelevant details (`PathParser`, creating the responder, building the URL) that hide the intent (CL p.127-129).
- The refactoring in Listing 9-2 makes the **BUILD-OPERATE-CHECK** pattern obvious (CONSTRUIR-OPERAR-VERIFICAR in the Portuguese edition; the footnote points to TestPatterns) [extrapolation]. Each test has three parts: it builds the data, operates on it and checks the result (CL p.129).
- The tests go straight to the point and use only the types and functions they need (CL p.129).

## Domain-specific testing language
- Instead of using the system's manipulation APIs directly, build functions and utilities that form a specialized **test API**, a test DSL, to make the tests easier to write and read (CL p.130).
- This API is not born ready: it evolves from the continuous refactoring of tests polluted by details (CL p.130).

## A dual standard
- The test API code follows different engineering standards from production. It must be simple, succinct and expressive, but need not be as efficient, because it runs in a test environment (CL p.130).
- Listings 9-3 and 9-4: `assertTrue(hw.heaterState())` and the like become `wayTooCold()` followed by `assertEquals("HBchL", hw.getState())`. Uppercase means on and lowercase means off, in the order {heater, blower, cooler, hi-temp-alarm, lo-temp-alarm} (CL p.130-131).
- The encoded string comes close to violating the mental mapping rule, but here it seems appropriate (CL p.131).
- Listing 9-6: `getState()` concatenates `String` instead of using `StringBuffer`. It would be inefficient in a real-time embedded system, but is acceptable in the test (CL p.131-132).
- Nature of the dual standard: there are things that are unacceptable in production and perfectly acceptable in a test, usually tied to memory and CPU. "Mas nunca de clareza" (But never clarity) (CL p.132).

## One assert per test
- One school of thought defends a single `assert` per JUnit test function. The advantage shows in Listing 9-5, where each test reaches a single quick conclusion (CL p.132). The footnote about the school is cut off in the scan.
- Listing 9-7 splits the test of 9-2 into two, with names in **given-when-then** format (`givenPages`, `whenRequestIsIssued`, `thenResponseShouldBeXML`). This improves reading, but duplicates code (CL p.132-133).
- The duplication could be removed with Template Method or with a separate class using `@Before`, but it is too much work for too little. The author prefers the multiple assertions of Listing 9-2 (CL p.133).
- Conclusion: a single assert is a good guideline, not a law. The best is to **minimize** the number of assertions per test (CL p.133).

## Single concept per test
- Perhaps the best rule is a single concept per test function. Avoid long tests that test several things in sequence (CL p.133).
- Listing 9-8 (`testAddMonths` of `SerialDate`) tests three things and should become three tests. Separated, they reveal the general rule: when adding months, the day does not exceed the last day of the month. They also reveal a missing test, February 28 plus one month giving March 28 (CL p.133-134).
- The problem is not multiple assertions, but multiple concepts. Final rule: minimize assertions per concept and test **one concept per test function** (CL p.134).

## F.I.R.S.T.
Five rules, with a footnote crediting Object Mentor training materials (CL p.134). The acronym comes from English (Fast, Independent, Repeatable, Self-validating, Timely). The names in the translation:
- **F, Rapidez (Fast)**: fast tests. Slow tests are not run often, problems show up late and the code does not get cleaned (CL p.134).
- **I, Independência (Independent)**: one test does not set up conditions for the next. They must run in isolation and in any order. Dependency creates a domino effect of failures and hides defects (CL p.134).
- **R, Repetitividade (Repeatable)**: repeatable in any environment, be it production, QA or a laptop on a train with no network. Otherwise there will always be an excuse for the failures (CL p.134).
- **S, Autovalidação (Self-validating)**: boolean output, pass or fail. You do not read a log or compare files by hand. Without self-validation, failure becomes subjective (CL p.134).
- **T, Pontualidade (Timely)**: written in a timely way, immediately **before** the production code. Written afterwards, the production code may turn out hard to test or not be designed for testing (CL p.135).

## Chapter conclusion
- The subject deserves a whole book. Tests are as important to the health of the project as production code, perhaps more, since they preserve flexibility, maintainability and reuse (CL p.135).
- Keep the tests succinct and expressive, invent test APIs as a DSL, and do not let the tests rot, or the code rots along with them (CL p.135).

## Examples from the book
- `Timer::ScheduleCommand` in C++ with the manual melody test (CL p.124-125).
- Listings 9-1 and 9-2: `SerializedPageResponderTest` (FitNesse) before and after refactoring (CL p.127-129).
- Listings 9-3 to 9-6: `EnvironmentControllerTest` and `MockControlHardware.getState()` (CL p.130-132).
- Listing 9-7: the same test split, with one assert and given-when-then names (CL p.132).
- Listing 9-8: `testAddMonths` of `SerialDate`, with several concepts (CL p.133).

## What the chapter does NOT say / common confusions
- It does not impose "one assert per test" as a rigid rule: it calls it a good guideline and prefers multiple assertions in the case of 9-2. The recommended rule is **one concept per test** (CL p.133-134).
- The T of F.I.R.S.T. is "Pontualidade/Timely" (writing before the code), not "Thorough" nor "Testável" (testable) (CL p.134-135).
- The S is "Autovalidação" (Self-validating, boolean output), not "Small" nor "Simples" (simple) (CL p.134).
- It does not use the term "Arrange-Act-Assert". It uses CONSTRUIR-OPERAR-VERIFICAR (BUILD-OPERATE-CHECK) and the given-when-then convention (CL p.129, p.132-133).
- It does not cite Mockito or any other mocking framework. "Mock" appears only in the class name `MockControlHardware`, a hand-written test double (CL p.132).
- It does not set a numeric coverage target (CL p.127).
- The dual standard does **not** license dirty tests: the concession is only for efficiency, never for clarity (CL p.132).
- The three laws do not say "write all the tests first". They say to alternate in cycles of seconds (CL p.126).

## [DATED]
- `testXxx` names without annotation (JUnit 3 style) in Listings 9-1, 9-2 and 9-7, and `@Test`/`@Before` (JUnit 4) (CL p.127-133) [DATED]. In JUnit 5 they are `@BeforeEach`, `@DisplayName` and `assertAll` [extrapolation].
- `StringBuffer`: since Java 5 the usual choice is `StringBuilder`, and `+=` concatenation is optimized by the compiler in several cases (CL p.132) [DATED][extrapolation].
- The one-assert-per-JUnit-test rule is discussed in the context of the JUnit of the time (CL p.132) [DATED].
