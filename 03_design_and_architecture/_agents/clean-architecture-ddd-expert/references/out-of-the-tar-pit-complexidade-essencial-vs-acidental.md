# Out of the Tar Pit: complexity, state, control and the "avoid and separate" split

Source: Ben Moseley and Peter Marks, *Out of the Tar Pit*, February 6, 2006 (acronym `TARPIT`, 66 PDF pages). **Convention**: `(TARPIT p.N)` = PDF page; in this PDF the printed page coincides with the PDF page (p.1 = 1). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

> **Corrections relative to the previous version of the package.** (1) The paper does **not** describe the metaphor of mammoths and saber-toothed tigers: "tar pit" appears only in the question in the conclusion ("what is the way out of the tar pit?", p.64); the Brooks work that appears in the references is the essay No Silver Bullet (reprinted in The Mythical Man-Month) `[from source] (TARPIT p.64)`. (2) The text does **not** "prove mathematically" anything: the arguments are conceptual. (3) The quoted sentence attributed to p.4, "complexity is the only root cause...", was invented text; what is on p.2 is the thesis that complexity is the root cause of most problems. (4) "Deadlocks", "race conditions", "mutex" and "semaphores" do **not** appear; the text speaks of concurrency with shared state and of non-repeatable tests (p.10). (5) Dead code and "complexity breeds complexity" are on **p.11**, not on p.18-20.

---

## 1. The thesis and the roadmap of the paper

- Abstract and introduction (p.1): complexity is the main difficulty in developing large-scale systems; following Brooks, they distinguish accidental from essential difficulty, but **disagree** that most of the remaining complexity is essential. The software crisis was identified in 1968 and has deepened `[from source] (TARPIT p.1)`. For the authors, the biggest contributor to complexity is the **handling of state**; other nearby contributors are the **volume of code** and the explicit concern with **control flow** `[from source] (TARPIT p.1)`.
- The paper is divided into two halves: the first on complexity (sections 2-7) and the second on a possible approach (sections 8-12) `[from source] (TARPIT p.2)`.
- Brooks pointed out four properties that make software hard: Complexity, Conformity, Changeability and Invisibility; the authors consider only complexity significant, and the others to be forms of it or problematic only because of it `[from source] (TARPIT p.2)`. Complexity is the root of most problems (unreliability, delay, insecurity, sometimes even performance) because understanding the system is a prerequisite to avoiding them `[from source] (TARPIT p.2)`.
- "Complexity" here is what makes systems hard to understand; it is **not** computational complexity theory `[from source] (TARPIT p.4)`.

## 2. How we understand systems: testing and informal reasoning

- Two ways to understand: **testing** (from outside, as a black box) and **informal reasoning** (from inside). Informal reasoning is by far the more important, because testing has inherent limits and because improving it reduces errors created, whereas improving testing only detects more errors `[from source] (TARPIT p.4)`.
- The central problem of testing: a test with one set of inputs says nothing about behavior with another set; tests only show the presence of bugs, never their absence (Dijkstra, cited) `[from source] (TARPIT p.5)`.
- Since every means of understanding has limits, **simplicity** is more important than testing or reasoning; between investing in testing or in simplicity, the latter may be the better choice `[from source] (TARPIT p.5)`.

## 3. Causes of complexity

1. **State** (4.1, p.6-8). By "state" the authors mean **mutable state** (footnote, p.6). Effects:
   - Testing: a test in one state says nothing about behavior in another state; the number of possible states usually exceeds that of inputs `[from source] (TARPIT p.6-7)`.
   - Informal reasoning: the number of scenarios grows; "with each additional bit of state, the total number of possible states doubles" `[from source] (TARPIT p.8)`; and there is **contamination**: a stateless procedure that uses (even indirectly) a stateful procedure can only be understood in the context of the state `[from source] (TARPIT p.8)`.
   - Conclusion: state is the biggest remaining cause of complexity `[from source] (TARPIT p.8)`.
2. **Control** (4.2, p.8-10): control is the order in which things happen; traditional languages force this concern, obliging one to specify *how* and to **over-specify** the problem (example of the three independent assignments, p.9) `[from source] (TARPIT p.8-9)`. Concurrency with shared state adds scenarios to consider and makes tests **non-repeatable**: the same test with the same input and the same initial state can give a different result `[from source] (TARPIT p.10)`.
3. **Code volume** (4.3, p.10-11): it is a largely secondary cause (much code serves to manage state and control); it is easy to measure; complexity grows non-linearly with size in most current systems, which makes it vital to reduce code to a minimum; with good handling of state and control, it is no longer clear that the growth is non-linear `[from source] (TARPIT p.10-11)`.
4. **Other causes** (4.4, p.11-12): duplicated code, never-used code ("dead code"), unnecessary abstraction, missing abstraction, poor modularity, poor documentation. They boil down to three principles: **complexity breeds complexity** (duplication as an example, especially under time pressure); **simplicity is hard**; **power corrupts** (without guarantees enforced by the language, errors and abuses happen; hence GC is good and languages that *permit* state should be viewed with caution) `[from source] (TARPIT p.11-12)`.

## 4. Classic approaches (summary)

- **OOP** (5.1, p.12-14): it is essentially imperative; encapsulation allows integrity constraints to be enforced by methods, but constraints involving several objects are awkward (it is not clear where they reside) `[from source] (TARPIT p.13)`. Object identity comes from state (intensional identity); *Value Objects* try to reintroduce extensional identity and may violate the notion of equivalence relation (for example, transitivity) `[from source] (TARPIT p.13-14)`. Conclusion: OOP suffers from state and control; it is not an adequate foundation for avoiding complexity `[from source] (TARPIT p.14)`. (Compare with `DDD p.19`, which prescribes immutable VOs: see the note in `ddd-tatico-e-agregados.md`.)
- **Functional programming** (5.2, p.15-18): rooted in lambda calculus; pure functions have **referential transparency**, which eliminates one of the two weaknesses of testing and improves reasoning `[from source] (TARPIT p.15)`. State can be simulated by passing extra parameters, but if a single pool parameter carries everything, a set of global variables is recreated and the ease of reasoning is lost `[from source] (TARPIT p.16-17)`. Weakness: real systems need to maintain state `[from source] (TARPIT p.18)`; monads help, but can be abused `[from source] (TARPIT p.18)`.
- **Logic programming** (5.3, p.19-21): promises to escape the complexity caused by control `[from source] (TARPIT p.21)`.

## 5. Essential vs. accidental (section 6)

- **Essential Complexity**: inherent to the problem, **as seen by the users**. **Accidental Complexity**: everything else, that which the team would not have to deal with in an ideal world (e.g., complexity from performance, suboptimal language and infrastructure) `[from source] (TARPIT p.21)`.
- The definition of "essential" is deliberately **stricter** than common usage: essential to the users' problem, not to a specific system nor to software in general; bits, bytes, transistors and computers are not essential `[from source] (TARPIT p.21)`. Essential = that which the team would have to worry about even in the ideal world; if there is a way for the team to produce something the users consider correct without dealing with that complexity, it is not essential `[from source] (TARPIT p.21-22)`. If the user does not even know what it is (thread pool, loop counter), it is not essential `[from source] (TARPIT p.22)`.
- The authors **disagree** with Brooks and Booch that software complexity is an essential property; much existing complexity is not essential; the goal of software engineering is to eliminate as much of the accidental as possible and to **assist** with handling the essential `[from source] (TARPIT p.22)`.

## 6. Ideal world and recommendations (section 7)

- **Ideal world** (7.1, p.23-27): one starts from informal requirements, formalized without concern for execution; executing them directly would be "absolute simplicity", the essence of declarative programming (the what, not the how) `[from source] (TARPIT p.23-24)`. Data classification (**Table 1**, p.26): essential input data -> essential state; immutable derived -> **accidental** state; mutable derived -> accidental; accidental derived -> accidental `[from source] (TARPIT p.24-26)`. "There are no caches or storage of derived calculations" in the ideal world `[from source] (TARPIT p.27)`. **Control** is almost entirely accidental; concurrency also, normally `[from source] (TARPIT p.27)`.
- **Limitations** (7.2, p.28-31): in practice, accidental complexity is needed for **performance** (the most common) and for **ease of expression** `[from source] (TARPIT p.30-31)`; reintroducing accidental state exposes one to the risk of inconsistent state `[from source] (TARPIT p.31)`.
- **Recommendations** (7.3, p.31-36): **Avoid** and **Separate**. Avoid state and control where they are not really essential; separate the essential complexity and the useful accidental complexity from the logic `[from source] (TARPIT p.31)`. **Table 2** (p.33): essential logic and essential state -> separate; useful accidental complexity (state/control) -> separate; useless accidental -> **avoid** `[from source] (TARPIT p.33)`. The system must remain correct if the "useful accidental" parts are removed, even if perhaps unacceptably slow `[from source] (TARPIT p.34)`. Each component may use a different, **restricted** language (the weaker the language, the simpler it is to reason) `[from source] (TARPIT p.34)`.
- **Reference restrictions between components** (p.35-36): essential state cannot refer to the others; essential logic refers to essential state, but not to accidental; accidental state/control may refer to the other two; changes in the accidental never require changing the essential logic `[from source] (TARPIT p.35-36)`.
- Caution about "designing for performance": optimizing a simple system is far easier than removing complexity from a complex system designed to be fast `[from source] (TARPIT p.36-37)`.

## 7. What the paper does not say (avoid attributing)

- Formulas for "percentage of essential/accidental complexity", weights per mutable variable, "purity" indices and thresholds such as "60% = bogged down": **do not exist**; the old script `tar_pit_complexity_calc.py` used invented weights (it was rewritten, see `scripts/`).
- "Almost all of the complexity is purely accidental" as a thesis: the text says much of it is accidental and disagrees with Brooks about the majority being essential, but does not claim "almost all" `[inference]` limited to "much" (p.22).
- 2^10 = 1,024 states as a numerical example from the paper: the text states the principle (doubles per bit, p.8); the number is arithmetic `[inference]`.
- Deadlocks/race conditions/mutex: see correction above.
- The "Functional Core, Imperative Shell" pattern (Gary Bernhardt) is **not in** the paper; see `programacao-funcional-relacional-frp.md`.
