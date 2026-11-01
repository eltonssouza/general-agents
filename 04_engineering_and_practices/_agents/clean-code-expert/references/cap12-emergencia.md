# Chapter 12 — Emergence (by Jeff Langr)

Source: CL ch. 12, PDF p.168-173 (opening on p.168; list of the rules on p.169).

Chapter author: Jeff Langr (CL p.168). Thesis: four simple rules, followed during the work, make a
good design "emerge" and make it easier to apply principles such as SRP and DIP (CL p.168).

## Kent Beck's four rules of Simple Design
- The rules are attributed to Kent Beck (Simple Design, reference [XPE]) (CL p.168, p.173).
- According to Kent, a design is simple if it follows these rules, **in this order** (CL p.169):
  1. Runs all the tests;
  2. Contains no duplication;
  3. Expresses the intent of the programmer;
  4. Minimizes the number of classes and methods.
- The rules are in order of importance: the first weighs more than the second, and so on (CL p.169).
- Rule 4 is explicitly the lowest priority of the four (CL p.173).

## Rule 1: runs all the tests
- First of all, a design must produce a system that acts as intended; without a simple way to verify it, the design on paper is doubtful (CL p.169).
- A system that is thoroughly tested and passes all its tests is a testable system; a system that cannot be verified should not be deployed (CL p.169).
- Making the system testable pushes toward small, single-purpose classes: classes that follow the SRP are easier to test (CL p.169).
- Tight coupling makes testing difficult; the more tests, the more you use DIP, dependency injection, interfaces, and abstraction to reduce coupling (CL p.169).
- The book's conclusion: "Writing tests leads to better designs" (printed: "Criar testes leva a projetos melhores") (CL p.169).
- Following this rule aligns the system with the OO goals: low coupling and high cohesion (CL p.169).

## Rules 2 to 4: refactoring
- With tests, it is possible to keep code and classes clean by refactoring gradually; with each new line, reflect on whether the design got worse, clean it up, and run the tests (CL p.169).
- Tests eliminate the fear of breaking the code while cleaning it (CL p.169).
- In refactoring, any concept of good design applies: increase cohesion, reduce coupling, separate concerns, modularize, reduce classes and functions, improve names (CL p.169).
- The final three rules (eliminate duplication, ensure expressiveness, minimize classes and methods) are applied in this phase (CL p.169).

## No duplication
- Duplication is the primary enemy of a well-designed system: extra work, risk, and complexity (CL p.170).
- Identical lines are duplication; similar lines can be tweaked to look more alike to make refactoring easier (CL p.170).
- There is also duplication of implementation: `isEmpty()` can be implemented by calling `size()` instead of keeping a separate boolean (CL p.170).
- Eliminate duplication even of a few lines (CL p.170).
- Extracting similarities at a very low level reveals SRP violations; the extracted method can move to another class and be reused. This "small reuse" greatly reduces complexity (CL p.171).
- Template Method is a common technique for removing high-level duplication: the subclasses fill in only the step that varies (CL p.171-172).

## Expressiveness
- Most of the cost of a design is in long-term maintenance; understanding what the system does is crucial to changing it without breaking it (CL p.172).
- Code should clearly express the author's intent, reducing defects and maintenance cost (CL p.172).
- Means: good names (no surprise on discovering what a class or function does), small classes and functions, standard nomenclature (pattern names such as COMMAND or VISITOR), and well-written unit tests, which serve as documentation (CL p.172-173).
- The most important means is to try: do not move on to the next problem without making the code easier for others to read, and the next person is probably you (CL p.173).
- Take pride in your work and care for what you created (CL p.173).

## Minimal classes and methods
- Even eliminating duplication, expressiveness, and the SRP can be taken too far, producing tiny structures; hence the rule asks to keep the number of functions and classes minimal (CL p.173).
- Examples of dogmatism to avoid: an interface for every class; always separating fields and behaviors into data classes and behavior classes (CL p.173).
- Goal: a small overall system, with small classes and functions; but having tests, eliminating duplication, and expressing yourself is more important (CL p.173).

## Conclusion
- Simple practices do not replace experience, but they distill decades of the authors' experience and help adhere to good principles and patterns (CL p.173).

## Examples from the book
- `isEmpty()`/`size()`: duplication of implementation (CL p.170).
- `scaleToOneDimension` and `rotate`: small duplication removed by extracting `replaceImage` (CL p.170-171).
- `VacationPolicy`: vacation calculation for the US and EU refactored with Template Method (`accrueVacation` + abstract `alterForLegalMinimums`) (CL p.171-172).

## What the chapter does NOT say / common confusions
- The order is not negotiable in the book: tests > no duplication > expressiveness > few classes/methods (CL p.169, p.173). Popular versions that swap the order of duplication and expressiveness are not the book's [extrapolation].
- "Minimize classes and methods" does not authorize large classes: it is the lowest-priority rule and serves to contain dogmatism (CL p.173).
- The chapter does not use YAGNI nor state "passes the tests" as "write tests first"; the rule is to have tests and run them (CL p.169).
- The chapter's author is Jeff Langr; the rules are Kent Beck's (CL p.168).

## [DATED]
- Nothing substantial. The example uses `System.gc()` and `RenderedOp` (JAI), merely illustrative (CL p.170-171).
