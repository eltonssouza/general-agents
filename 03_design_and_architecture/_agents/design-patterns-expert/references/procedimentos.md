# Procedures (step-by-step guides derived from the sources)

Each step says where it comes from. Decision guides that combine sources are `[inference]`; numeric parameters that the book does not give are `[extrapolation]`. Pages = PDF (see `INDEX.md`).

## 1. Choose a catalog pattern by intent `[inference]` over the RG intents
The intents come from the catalog `[from source] (RG p.10-16)`; the tree is an organization made by this package.
1. **Object creation**
   - Families of compatible products without concrete classes: Abstract Factory `[from source] (RG p.17, 26)`.
   - A subclass decides the product type; or reuse objects through a pool: Factory Method `[from source] (RG p.45, 52-54)`.
   - Complex object in steps, many optional parameters (telescoping constructor): Builder `[from source] (RG p.30, 40)`.
   - Copy without depending on the class, or cloneable presets: Prototype `[from source] (RG p.58, 66-67)`.
   - Single instance with global access: Singleton, **with strong caveats** (RG p.75-76; GPP p.77-91).
2. **Structure**
   - Incompatible interfaces: Adapter `[from source] (RG p.78, 85)`; hierarchies that vary in two dimensions: Bridge `[from source] (RG p.89, 97)`; part-whole trees: Composite `[from source] (RG p.101, 108-109)`; layered behavior at runtime: Decorator `[from source] (RG p.112, 122)`; simple interface for a subsystem: Facade `[from source] (RG p.127, 131)`; many similar objects and little RAM: Flyweight `[from source] (RG p.135, 143)`; access control, lazy, cache, log: Proxy `[from source] (RG p.147, 153-154)`.
3. **Behavior**
   - Chain of checks: Chain of Responsibility `[from source] (RG p.157, 167)`; request as an object (queue, history, undo): Command `[from source] (RG p.172, 183)`; traversal without exposing the collection: Iterator `[from source] (RG p.187, 196)`; reduce dependencies between components: Mediator `[from source] (RG p.199, 206-207)`; snapshot/undo without breaking encapsulation: Memento `[from source] (RG p.211, 219-220)`; notify dynamic interested parties: Observer `[from source] (RG p.223, 231)`; behavior changes with state: State `[from source] (RG p.235, 244)`; interchangeable algorithms: Strategy `[from source] (RG p.248, 254-255)`; algorithm skeleton with extensible steps: Template Method `[from source] (RG p.258, 265)`; new operation over a structure without altering the classes: Visitor `[from source] (RG p.268, 276-277)`.
4. **Before applying**: does the pattern solve a real problem or is it overkill? `[from source] (RG p.8-9; GPP p.12, 17)`. Ask "what if I use a function/lambda?" (Strategy can be an anonymous function, RG p.256; Command can be a closure, GPP p.31-32).

## 2. Implement the Game Loop with a fixed step (GPP p.138-141)
1. Choose `MS_PER_UPDATE` (simulation granularity); it must be larger than the time of one `update()` on the slowest machine; the smaller it is, the more faithful on fast machines and the costlier to catch up to real time `[from source] (GPP p.139)`. Numeric value: `[extrapolation]` (60 Hz = 16.67 ms is common).
2. On each turn: measure the elapsed time, add it to `lag`, process input without blocking, while `lag >= MS_PER_UPDATE` call `update()` and subtract, then `render(lag / MS_PER_UPDATE)` `[from source] (GPP p.138-141)`.
3. Protect the inner loop with a maximum number of iterations so the game slows down instead of freezing `[from source] (GPP p.139)`; the value of the maximum and the choice to discard the excess `lag` are `[extrapolation]`.
4. The renderer uses the value between 0 and 1 to estimate the position of objects between two states (the computation with velocity is shown in GPP p.141); the exact form is the renderer's decision.
5. If the platform has its own loop (browser), the event loop drives the game `[from source] (GPP p.134, 141)`.

## 3. Refactor state conditionals into State (RG p.244-245; GPP p.92-110)
1. Identify the context and the methods with conditionals by state `[from source] (RG p.245)`.
2. If there are conflicting boolean flags, first replace them with an `enum` with a single state field, inverting the order of the branching (by state first) `[from source] (GPP p.97-98)`.
3. Create the state interface with only the methods that vary by state; one class per state; move the code and data exclusive to the state `[from source] (RG p.245; GPP p.99-101)`.
4. The context keeps the reference to the state and delegates; decide where the instances live: static (no fields) or created at each transition (with data) `[from source] (GPP p.101-103)`.
5. Consider entry/exit actions to consolidate what happens when entering the state `[from source] (GPP p.103-105)`.
6. If the states explode: concurrent, hierarchical machines or a pushdown automaton `[from source] (GPP p.105-110)`.

## 4. Implement Undo/Redo with Command (RG p.179-184; GPP p.27-30)
1. Command interface with `execute()` and `undo()` `[from source] (GPP p.28-29)`.
2. The movement command stores what changed (previous position), not a snapshot of the whole object (alternative: Memento, which GPP found costly, and RG cites the RAM cost) `[from source] (GPP p.29; RG p.183)`.
3. Keep a list of commands with a "current" pointer; when executing a new command after undo, discard what comes after `[from source] (GPP p.30)`.
4. Ensure that every data change goes through commands `[from source] (GPP p.30)`.

## 5. Create an Object Pool (GPP p.307-317)
1. Confirm the conditions: frequent creation/destruction, objects of similar size, slow or fragmenting allocation `[from source] (GPP p.309)`.
2. Allocate the set at the start, mark all as "not in use"; ask the object whether it is in use (or keep a flag) `[from source] (GPP p.309, 313)`.
3. To create in O(1), chain the free ones into a **free list** that reuses the memory of dead objects `[from source] (GPP p.314-317)`.
4. Decide what to do when the pool is exhausted (prevent, do not create, kill an existing one, grow) `[from source] (GPP p.310-311)`.
5. Fully clean/initialize the reused object and the references it retains `[from source] (GPP p.311-312)`.

## 6. Split a monolithic class into components (GPP p.214-223)
1. Slice by domain (input, physics, graphics) into component classes; leave in the entity only the "pan-domain" state (position, velocity) `[from source] (GPP p.216-219)`.
2. Hide each component behind an interface to allow swapping (e.g., demo mode) `[from source] (GPP p.219-221)`.
3. Decide the communication between components: container state, direct references or messages; combine them, starting simple `[from source] (GPP p.224-228)`.
4. If performance matters, components in contiguous arrays (Data Locality) `[from source] (GPP p.214, 277-279)`.

## 7. Choose the persistence strategy (PEAA Ch. 3)
1. Simple domain logic (Transaction Script or Table Module): tables around the data + Row/Table Data Gateway `[from source] (PEAA p.55)`.
2. Simple domain whose classes mirror the tables: Active Record `[from source] (PEAA p.42, 55)`.
3. Rich domain: Data Mapper and Unit of Work/Identity Map; consider an O/R mapping tool `[from source] (PEAA p.43, 45-46)`.
4. Inheritance: Single Table Inheritance as the author's first choice, with the trade-offs of joins x duplication `[from source] (PEAA p.52-54)`.
5. Iterate in short cycles, integrating the model with the database `[from source] (PEAA p.55)`.
6. What **cannot** be said: numeric criteria for "when to use Transaction Script/Domain Model" (Ch. 2 absent).
