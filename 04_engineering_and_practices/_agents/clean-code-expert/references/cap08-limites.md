# Cap. 8 — Limites (Boundaries; by James Grenning)

Source: CL ch. 8, PDF p.117-123 (opening on p.117; bibliography on p.123).

## Premise
- The chapter is signed by James Grenning (CL p.117).
- We rarely control all the software in the system: purchased packages, open-source code, components from other teams. The chapter deals with integrating that external code cleanly and keeping the boundaries clean (CL p.117).

## Using third-party code
- There is a natural tension between the provider and the user of an interface. The provider seeks wide applicability, and the user wants an interface focused on their own needs. The tension causes problems at the boundaries (CL p.118).
- Example `java.util.Map` (Figure 8.1): the interface is too broad. Any holder can call `clear()` and erase everything, and `Map` does not restrict the types stored (CL p.118).
- Scattering `(Sensor) sensors.get(sensorId)` through the code leaves the cast to each client: it works, but it is neither clean nor expressive (CL p.118-119).
- Generics improve readability, but do not solve the excess capability of `Map` (CL p.119).
- Passing `Map` around the system multiplies the places to change if the interface changes. This already happened when generics entered Java 5, and some systems avoided generics because of the size of the change (CL p.119).
- Clean way: a `Sensors` class that holds the private `Map` and exposes `getById(id)`. The boundary interface is hidden, generics become an implementation detail, and the class can enforce design and business rules. The code is easier to understand and harder to misuse (CL p.119).
- It does not ask for encapsulating **every** use of `Map`. The advice is not to pass `Map`, or any boundary interface, around the whole system: keep it inside a class or a close family of classes and avoid returning it or accepting it as an argument in public APIs (CL p.119).

## Exploring and learning boundaries
- Testing third-party code is not our job, but it may be worth writing tests for the external code we use (CL p.119).
- Learning the API and integrating it at the same time doubles the difficulty, and we end up debugging without knowing whether the bug is ours or theirs (CL p.120).
- **Learning tests** (a name attributed to Jim Newkirk): tests that call the external API the way the application would. They are controlled experiments that verify our understanding and focus on what we want to know about the API (CL p.120).

## Learning log4j
- Narrative: the first test fails asking for an `Appender`. With an unconfigured `ConsoleAppender` there is no output stream. With `PatternLayout` and `ConsoleAppender.SYSTEM_OUT`, it works. The default constructor of `ConsoleAppender` comes "unconfigured", which looks like a bug or inconsistency (CL p.120-121).
- The knowledge becomes a series of unit tests (Listing 8-1, `LogTest`) and is then encapsulated in our own logging classes, isolating the application from the log4j boundary interface (CL p.121).

## Learning tests are better than free
- They cost nothing, because we would have to learn the API anyway. They are precise experiments (CL p.121-122).
- They pay off: with each new release of the external package, we run the tests and see whether the behavior changed. Each release brings new risk, and an incompatibility shows up immediately (CL p.122).
- Whether or not you need the learning, define a clear boundary with **boundary tests** that exercise the interface the way our code would. Without them, there is a temptation to keep the old version longer than we should, because nothing eases the migration (CL p.122).

## Using code that does not yet exist
- Another kind of boundary separates the known from the unknown (CL p.122).
- The radio system case: the "Transmitter" API did not yet exist. The team defined the interface they **wanted** to have, `Transmitter.transmit(frequência, fluxo)` (frequency, stream), and kept working (CL p.122).
- Advantage: we control that interface, and the client code (`CommunicationsController`) stays readable and focused on its own role (CL p.122).
- When the real API was defined, the `TransmitterAdapter` was created (ADAPTER pattern, with a cross-reference to [GOF]). It encapsulates the interaction with the API and is the only point to change if it evolves (CL p.122-123, Figure 8.2).
- The design offers a convenient **seam** for tests: with a `FakeTransmitter`, the `CommunicationsController` is tested, and once the real API is available, boundary tests are created (CL p.123).

## Clean boundaries
- Change is one of the things that happen at boundaries. Good designs accommodate change without large rework. With code outside our control, we must protect our investment (CL p.123).
- Boundary code needs clear separation and tests that define expectations. Avoid having much of the code know the particulars of the third party (CL p.123).
- "É melhor depender de algo que você controle" (It is better to depend on something you control) than on something that ends up controlling you (CL p.123).
- Manage external boundaries in **few places** that reference them: wrap them, as with `Map`, or use an ADAPTER, which converts the ideal interface into the provided one. The code communicates better, uses the boundary consistently and has few points of change (CL p.123).

## Examples from the book
- Figure 8.1: list of methods of `Map`, of `Map` and of `Object` (CL p.118).
- `Map sensors` with a cast, the generics version and the `Sensors` class encapsulating it (CL p.118-119).
- Tests `testLogCreate` and `testLogAddAppender` with log4j, and Listing 8-1 `LogTest` (CL p.120-121).
- Figure 8.2: `CommunicationsController`, `Transmitter` interface, `FakeTransmitter`, `TransmitterAdapter` and the Transmitter API (CL p.123).

## What the chapter does NOT say / common confusions
- It does not say we should exhaustively test third-party libraries. It says it is not our job to test them, but that learning tests and boundary tests are worth it (CL p.119, p.122).
- It does not order encapsulating every use of `Map` (CL p.119).
- The term "learning test" is attributed to Jim Newkirk, not to the chapter's author (CL p.120).
- It does not talk about "Anti-Corruption Layer", "Ports and Adapters" or "hexagonal architecture" [extrapolation: these are terms from other sources].
- It does not mention mocking frameworks. The test double in the example is a hand-written fake, `FakeTransmitter` (CL p.123).
- Code remark: the printed listing uses `Map<Sensor>`, but Java's `Map` requires two type parameters (CL p.119) [extrapolation].

## [DATED]
- log4j 1.x (`BasicConfigurator`, `ConsoleAppender`, `PatternLayout`) is the API in the example (CL p.120-121). log4j 1.x was discontinued and replaced by Log4j 2/SLF4J [DATED][extrapolation]. The lesson (learning tests) remains valid.
- The reference to the introduction of generics in Java 5 is historical (CL p.119) [DATED].
- JUnit 4-style tests (`@Test`, `@Before`) (CL p.120-121) [DATED].
