# Chapter 10 — Classes (with Jeff Langr)

Source: CL ch. 10, PDF p.136-151 (chapter opening on p.136; first heading "Organização das classes" — "Class Organization" — on p.137).

The chapter moves up from the level of lines and functions to the level of the class: member order, encapsulation,
size measured in responsibilities, cohesion, and how to organize classes to absorb change (OCP, DIP).

## Class organization (member order)
- Following the Java convention, a class begins with the list of variables: first the public static constants, then the private static variables, then the private instance variables (CL p.137).
- There is seldom a good reason for a public variable (CL p.137).
- Public functions come after the variables; the private functions called by a public one go right after it, following the top-down rule and reading like a newspaper article (CL p.137).
- [inference] The order follows the same logic as the stepdown/newspaper rule of the formatting chapter, applied to the class; the book calls this the standard Java convention, not a universal rule (CL p.137).

## Encapsulation
- Variables and functions should be private by default, but "we are not fanatics" ("não somos radicais") (CL p.137).
- If a test in the same package needs to access a function or variable, it can be protected or package-scoped: "tests rule" ("o teste tem prioridade") (CL p.137).
- Before that, look for a way to keep it private; loosening encapsulation is always the last resort (CL p.137).

## Classes should be small, measured by responsibilities
- First rule: classes should be small; second: they should be smaller than that (CL p.137).
- Functions are measured by physical lines; classes are measured by **responsibilities** (CL p.137).
- Extreme example: `SuperDashboard` with about 70 public methods, a "god class" (CL p.137).
- Even reduced to five methods, `SuperDashboard` still has too many responsibilities: few methods do not guarantee a small class (CL p.139).
- The class name should describe its responsibilities; if a concise name does not come out, the class is probably too big (CL p.139).
- Ambiguous names such as Processor, Manager, or Super indicate an accumulation of responsibilities (CL p.139).
- Description test: it should be possible to describe the class in about 25 words without using the conjunctions "if", "and", "or", "but"; an "and" in the description signals too many responsibilities (CL p.139).

## The Single Responsibility Principle (SRP)
- The book's statement: a class or module should have one, and only one, reason to change (CL p.139).
- The SRP gives both the definition of responsibility (a reason to change) and the guideline for class size (CL p.139).
- The five-method `SuperDashboard` has two reasons to change: version information and Swing component management; the solution is to extract the `Version` class (CL p.139-140).
- Identifying reasons to change helps recognize and create better abstractions (CL p.140).
- The SRP is one of the most important concepts in OO and one of the simplest, but it is the most ignored principle when creating classes (CL p.140).
- Cause: making the software work and making it clean are different activities; many stop when the program works and do not go back to split the overstuffed classes (CL p.140).
- Many small classes do not make the system harder to understand: the analogy is a toolbox with many labeled drawers versus a few drawers with everything mixed together (CL p.140).
- Goal: the system should be composed of many small classes, not a few large ones; each encapsulates one responsibility, has one reason to change, and collaborates with a few others (CL p.140-141).

## Cohesion
- Classes should have a small number of instance variables; each method should manipulate one or more of them (CL p.141).
- The more variables a method manipulates, the more cohesive it is to the class; a class in which every variable is used by every method is maximally cohesive (CL p.141).
- Maximal cohesion is neither advisable nor generally possible, but we want high cohesion: methods and variables that are codependent and form a logical whole (CL p.141).
- Warning sign: keeping functions small and argument lists short can bloat the class with instance variables used by only a few methods; this almost always indicates another class trying to get out of the larger one (CL p.141).
- Action rule: separate variables and methods into two or more more-cohesive classes (CL p.141).

## Maintaining cohesion results in many small classes
- When extracting part of a large function that uses four local variables, do not pass all four as arguments; promoting them to instance variables makes the extraction easier (CL p.142).
- This reduces the class's cohesion; if a few functions share certain variables, they form a class of their own: when classes lose cohesion, split them (CL p.142).
- Breaking large functions into small ones generally allows splitting the classes as well, giving better organization and a more transparent structure (CL p.142).
- The refactored program gets longer (from one to almost three pages) because of longer names, function/class declarations used as comments, and whitespace; the book treats this as acceptable (CL p.147).
- The refactoring was not a rewrite: tests pinned down the behavior of the original program and small changes were made one by one, running the tests after each step (CL p.147).

## Organizing for change (OCP)
- In a clean system, classes are organized to reduce the risk of each change (CL p.148).
- A class that must be opened to receive new functionality (e.g., `Sql` without `update`) violates the SRP if it has two reasons to change: a new type of statement and a change to an existing type (CL p.148).
- Private methods that serve only a subset of the class are a useful heuristic for seeing where to improve (CL p.148).
- The main trigger for acting is a real need for change: if the class is logically complete and no change is coming soon, leave it alone; when you need to open it, consider fixing the design (CL p.148).
- Solution shown: each operation becomes a subclass of an abstract `Sql`; common private behavior goes into utility classes (`Where`, `ColumnList`) (CL p.148-149).
- Gains: each class becomes simple, the risk of one function breaking another drops, tests become easier, and adding `update` does not change any existing class (CL p.150).
- OCP as the book states it: classes should be open for extension but closed for modification (CL p.150).
- Ideal: incorporate new features by extending the system, not by changing existing code (CL p.150).

## Isolating from change (DIP)
- Concrete classes contain details; abstract ones represent concepts; a client that depends on concrete details is at risk when they change. Interfaces and abstract classes isolate this impact (CL p.150).
- Depending on concrete details also makes testing harder (e.g., `Portfolio` dependent on a volatile stock exchange API) (CL p.150).
- Solution: a `StockExchange` interface with a single method, implemented by `TokyoStockExchange`; the `Portfolio` constructor receives the interface (CL p.150).
- In the test, a fixed-value stub replaces the real exchange, making the result deterministic (CL p.151).
- A system decoupled enough to be tested this way is also more flexible and reusable (CL p.151).
- DIP, as the book says: classes should depend on abstractions, not on concrete details (CL p.151).

## Examples from the book
- Listing 10-1: `SuperDashboard` with dozens of public methods (CL p.137-139).
- Listing 10-2: the same class reduced to five methods, still with two responsibilities (CL p.139).
- Listing 10-3: extracted `Version` class, with a single responsibility (CL p.140).
- Listing 10-4: `Stack`, example of a cohesive class (only `size()` does not use both variables) (CL p.141).
- Listing 10-5: `PrintPrimes`, Java translation of Knuth's program generated by the WEB tool, written as a single function (CL p.142-143).
- Listings 10-6 to 10-8: the same program split into `PrimePrinter` (execution environment), `RowColumnPagePrinter` (formatting), and `PrimeGenerator` (prime generation) (CL p.144-147).
- Listing 10-9: `Sql` class that must be opened for changes (CL p.148).
- Listing 10-10: hierarchy of closed subclasses of `Sql` (CL p.149).
- `Portfolio`/`StockExchange` and the `PortfolioTest` test with `FixedStockExchangeStub` (CL p.150-151).

## What the chapter does NOT say / common confusions
- It does not set a maximum number of lines or methods per class: the measure is responsibility (CL p.137, p.139).
- The book's SRP is defined by reason to change, not by doing only one thing (that is the function rule of ch. 3) (CL p.139).
- The translation calls the DIP "Princípio da Inversão da Independência" (literally "Independence Inversion Principle"); the book never uses "Inversão de Dependência" (Dependency Inversion) (CL p.151). When citing, explain that it is the Dependency Inversion Principle [inference].
- The chapter does not present the acronym SOLID, nor LSP or ISP; it cites only SRP, OCP, and DIP, referring to [PPP] (CL p.139, p.150-151).
- It does not tell you to split classes preemptively: without a need for change, the logically complete class may stay as it is (CL p.148).
- It does not forbid `protected`/package access for tests; it only makes it a last resort (CL p.137).
- It defines no formal cohesion metric (like LCOM); cohesion is described qualitatively (CL p.141).

## [DATED]
- Examples depend on Swing (`JFrame`) and on Java conventions of the time (CL p.137-140).
- The `Portfolio` test uses JUnit 4 (`@Before`, `Assert.assertEquals`) (CL p.151).
- The Knuth tool cited (WEB, 1992) is a historical reference (CL p.142).
