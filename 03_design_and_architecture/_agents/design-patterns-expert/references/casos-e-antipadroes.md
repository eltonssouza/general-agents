# Practical cases and anti-patterns (only what the sources support)

Sources: RG (Refactoring.Guru catalog), GPP (Nystrom), CC (sample: Ch. 1 only), PEAA (sample: Introduction and Ch. 3). Pages = PDF (see `INDEX.md`). Each item says what the text asserts; what is an extension is labeled. Unsupported v1 items (Transaction Script "trap", Flag Argument "forbidden", "God Entity" with 5,000 lines attributed to p.232, GC of "100 to 300 ms") were removed or rewritten.

## 1. Singleton as a global variable
- GPP: the Singleton is global state encapsulated in a class; it is hostile to reasoning, encourages coupling (anyone can `#include` it and call it) and is hostile to concurrency `[from source] (GPP p.81-83)`. It solves two problems (a single instance and global access) even when only one of them is needed; the `Log` example shows the cost when the need for several arises `[from source] (GPP p.83-84)`.
- RG: violates SRP, can mask bad design, requires care in multithreading, makes testing harder `[from source] (RG p.75-76)`.
- Remedy (GPP): check whether the class is needed, pass the object as a parameter, get it from the base class, from something already global or from a Service Locator `[from source] (GPP p.85-91)`.

## 2. Boolean flags piling up in state code
- GPP: the heroine with `isJumping_`, `isDucking_`... generates bugs with every new action (jumping in the air, diving); "complex branching and mutable state" are error-prone kinds of code `[from source] (GPP p.92-95)`. Remedy: FSM with `enum`/`switch` and then State `[from source] (GPP p.96-101)`.
- Note: this is **not** the Clean Code "flag arguments" rule (which is only in the CC table of contents and index, without text: see `clean-code-nomes-e-funcoes.md`).

## 3. Subclass explosion (inheritance by combination)
- Bridge: `Shape` x colors yields 4 classes with 2 shapes and 2 colors, and grows with each new dimension `[from source] (RG p.90)`. Decorator: combined notification channels `[from source] (RG p.113-114)`. Command: button subclasses per action `[from source] (RG p.173)`. Factory Method: conditionals per transport type `[from source] (RG p.46)`. Type Object: one subclass per monster breed `[from source] (GPP p.191-194)`. Component: `Zone/Decoration/Prop` hierarchy and the "Deadly Diamond" `[from source] (GPP p.211-212)`.
- In common `[inference]`: replace inheritance with composition/data. Nystrom reminds us that one should not be dogmatic against inheritance either `[from source] (GPP p.155)`.

## 4. Monolithic class covering several domains
- GPP: the hero class with input, physics, graphics and sound becomes a 5,000-line file, with coupling like a "Gordian knot" and concurrency risks per domain `[from source] (GPP p.209-210)`. Remedy: Component `[from source] (GPP p.210-213)`. The "God Object" is also a risk of Mediator and Facade `[from source] (RG p.132, 208)`.

## 5. Observer: forgotten observer (lapsed listener) and ordering
- GPP: an observer that is not unregistered becomes a "zombie" retained by the subject's list; solution: unregistration discipline (the observer removes itself, the subject may send a final notification, or automatic unregistration in the base) `[from source] (GPP p.55-57)`. RG: subscribers are notified in random order `[from source] (RG p.232)`; for GPP there must be no order dependency between observers `[from source] (GPP p.52)`.
- Weak references as a remedy: `[extrapolation]` (not in GPP).

## 6. Game Loop with a variable step
- GPP: `update(elapsed)` makes the game non-deterministic and unstable (accumulated floating-point error on different machines; physics damping tuned for a fixed step) `[from source] (GPP p.136-138)`. Remedy: update with a fixed step using `lag` and render with the remainder `[from source] (GPP p.138-141)`.
- Iteration limit of the inner loop so the game does not freeze: cited without a number `[from source] (GPP p.139)`; the simulator's cap of "8" is `[extrapolation]`.

## 7. Cache of derived data without invalidation
- GPP (Dirty Flag): forgetting to mark the flag leads to stale data that is hard to trace; deferring too long causes pauses; if it fails before synchronizing, the work is lost (autosave) `[from source] (GPP p.297-298)`. Remedy: encapsulate every modification of the primary state `[from source] (GPP p.298)`.

## 8. Object allocation in the middle of the game
- GPP: memory fragmentation on consoles/mobile, soak tests; Object Pool with free list `[from source] (GPP p.307-317)`. Pool pitfalls: reused objects are not zeroed, exhausted pool, references retained with a garbage collector `[from source] (GPP p.310-312)`.

## 9. Event queue as a global variable and feedback loops
- GPP: a central queue is a global variable; the world changes between sending and processing; event cycles can flood the queue `[from source] (GPP p.236-237)`. Only use a queue to decouple in time `[from source] (GPP p.235)`.

## 10. Active Record that grew too large
- PEAA Ch. 3: with rich domain logic the 1:1 class-table mapping fails, the database does not handle inheritance and testing without the database becomes difficult; migrate to Data Mapper; do not mix primary persistence mechanisms `[from source] (PEAA p.42-43)`.
- Domain models built for six months without a database are risky `[from source] (PEAA p.55)`.

## 11. Hidden dependency: Service Locator
- GPP: the dependency is deferred to runtime, the service may not exist and does not know who calls it; prefer passing the object; use a null service for a failed lookup `[from source] (GPP p.252-257)`.

## 12. Applying a pattern without need
- RG: criticisms (kludge for weak languages, "literal" application, "if all you have is a hammer..."); `[from source] (RG p.8-9)`. Flyweight only under heavy RAM pressure `[from source] (RG p.143-144)`; Strategy/State/Builder have a cost in classes when the case is small `[from source] (RG p.42, 245, 255)`.
- GPP: YAGNI and the risk of speculative abstraction and extensibility `[from source] (GPP p.12, 17)`. Spatial Partition is not worth it with small n `[from source] (GPP p.324)`; Bytecode is the most complex pattern in the book `[from source] (GPP p.169)`.

## 13. Bad code and debt (Clean Code, Ch. 1)
- Bad code brings companies down; "later equals never"; team productivity tends to zero; "grand redesign in the sky"; lack of professionalism `[from source] (CC p.33-36)`. The Boy Scout rule as a continuous practice `[from source] (CC p.44)`.
