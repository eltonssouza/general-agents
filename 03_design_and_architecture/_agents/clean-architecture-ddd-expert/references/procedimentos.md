# Procedures: work routines with the textual basis of each step

These routines are **practical syntheses** of the package. Each step has its basis in the corpus (`[from source]`, PDF page) or is marked `[inference]`/`[extrapolation]`. Code is **illustrative** (`[extrapolation]`): none of the PDFs contains example code beyond `Employee` (SRP p.3) and pseudocode in `TARPIT`. **Convention**: DDD printed = PDF − 7.

---

## 1. Model an aggregate

Basis: `DDD p.23-25`.
1. **List the invariants** that must hold consistently and define properties and invariants "for the aggregate as a whole" `[from source] (DDD p.23)`. Asking the experts which rules require immediate consistency is an `[inference]`.
2. **Choose the root**: one entity; external objects hold a reference only to the root; references to internal members only within an operation `[from source] (DDD p.23)`. The root (or designated mechanism) enforces the invariants `[from source] (DDD p.23)`.
3. **Draw the boundary using the transactional criterion as well**: inside, synchronous consistency; across aggregates, asynchronous updates `[from source] (DDD p.23)`. If the boundary does not help with transaction and distribution decisions, reconsider the model `[from source] (DDD p.23)`.
4. **Between aggregates**: the text speaks of a reference to the root; using identifiers instead of object pointers is widespread practice `[extrapolation]`; "one aggregate per transaction" is a reading `[inference]` of item 3 and must be labeled as such.
5. **Repository**: only for roots that need direct access, with the illusion of an in-memory collection and selection methods by domain criteria `[from source] (DDD p.24)`.
6. **Factory**, if creating the aggregate is complex: create the entire aggregate at once, enforcing invariants `[from source] (DDD p.25)`.
7. **Domain events** to communicate relevant changes: modeled as immutable domain objects `[from source] (DDD p.20)`; asynchronous propagation across aggregates `[from source] (DDD p.20, 23)`.
8. Check with `scripts/audit_aggregate.py` (rules labeled by origin).

## 2. Fix a Dependency Rule violation with a port and adapter

Basis: `CA12 p.3-7`.
1. **Identify** the name of an outer circle mentioned inside an inner one (web framework class, database driver class, database row format) `[from source] (CA12 p.3, 6)`.
2. **Declare an interface in the inner circle** that expresses what the use case needs (in the text: "Use Case Output Port") `[from source] (CA12 p.6)`. The name "port" and the signature are `[extrapolation]`.
3. **Make the use case depend only on the interface**; the outer circle implements it (dynamic polymorphism) `[from source] (CA12 p.6)`. How to inject the implementation (constructor, container) is not in the text `[extrapolation]`.
4. **Convert data** at the boundary into simple structures and into the form most convenient to the inner circle `[from source] (CA12 p.6-7)`.
5. **Compose at the application entry point** (instantiate the adapter and pass it to the use case) `[extrapolation]`.
6. **Validate** with `scripts/validate_dependency_rule.py` (describe modules/layers in JSON).

Illustrative sketch `[extrapolation]`:
```java
// use case circle
interface OrderOutputPort { void save(Order order); }
class CreateOrderUseCase {
    private final OrderOutputPort port;
    CreateOrderUseCase(OrderOutputPort port) { this.port = port; }
}
// adapters/frameworks circle
class SqlOrderAdapter implements OrderOutputPort { /* SQL here */ }
```

## 3. Separate essential logic from accidental state and control

Basis: `TARPIT p.31-36` (separate and avoid). The package does **not** propose a recipe from the paper for today's object-oriented code: the paper describes a hypothetical architecture (FRP). The steps below are adaptations `[extrapolation]` guided by principles of the text:
1. **Classify the data** as essential input, derived or accidental, according to Table 1 `[from source] (TARPIT p.26)`: derived data and caches are accidental state; consider recomputing instead of storing `[from source] (TARPIT p.25-27)`.
2. **Avoid** unnecessary state and control; **separate** what remains among essential logic, essential state and useful accidental `[from source] (TARPIT p.31-34)`.
3. **Do not let the essential logic reference the accidental** (the logic refers to essential state, not to accidental) `[from source] (TARPIT p.35-36)`.
4. **Pure functions in the logic** to obtain referential transparency `[from source] (TARPIT p.15)`; input and output effects at the edge via minimal components (feeders/observers, `TARPIT p.46-47`). The formulation "functional core, imperative shell" is `[extrapolation]`.
5. **Performance later**: optimizing a simple system is easier than simplifying an optimized one `[from source] (TARPIT p.36-37)`.
6. Estimate the state space with `scripts/tar_pit_complexity_calc.py` (only the arithmetic of p.8 and tables 1 and 2).

## 4. Adopt decoupling in a project with a framework (Rails/Spring/etc.)

Basis: `CA11 p.2-5`.
1. Controllers only unpack the request into a simple structure and hand it to an interactor; views only read the response structure `[from source] (CA11 p.2)`.
2. Take advantage of thin end-to-end slices without coupling (simple interim UI) `[from source] (CA11 p.3-4)`.
3. Framework conventions are not a reason to couple business rules; decoupling is "worth more" in the author's view `[from source] (CA11 p.4)`.
4. Think about the shape of the system for a few hours or a day or two, without BDUF `[from source] (CA11 p.5)`.
