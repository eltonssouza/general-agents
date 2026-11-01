# Practical cases and antipatterns (with the textual basis of each)

Each item separates what the corpus says (`[from source]`) from the proposed diagnosis or remedy (`[inference]`/`[extrapolation]`). **Convention**: `(ACRONYM p.N)` = **PDF** page (DDD: printed = N − 7). The **names** of the antipatterns below are mostly from external literature; the PDF describes the problem without using the name.

---

## 1. Anemic domain model

- What the corpus says: when unrestricted queries and application code concentrate the logic, the domain logic leaves the model and "entities and value objects become mere data containers" `[from source] (DDD p.24)`. When UI, database and support code are written inside the business objects, the domain logic becomes diffuse and hard to reason about `[from source] (DDD p.17)`.
- Labels: the name "Anemic Domain Model" is Martin Fowler's `[extrapolation]`; the previous package attributed it to "Fowler and Evans" with a citation to `DDD p.16-17`, which does **not** address the topic. The example `order.setStatus("PAGO")` is illustrative `[extrapolation]`.
- Remedy `[inference]`: give behavior back to entities and VOs, expressing operations in the ubiquitous language (`DDD p.10-11`), and keep invariants under the responsibility of the aggregate root (`DDD p.23`).

## 2. UI, SQL and business rules mixed together

- `[from source] (DDD p.17)`: mixing makes things harder to understand and test; superficial UI changes can alter business logic. `[from source] (CA12 p.4)`: all SQL must be confined to the adapters layer, in the parts tied to the database; nothing inward of it should know about the database. `[from source] (SRP p.5)`: "that is why you don't put SQL in JSPs".
- Remedy `[inference]`: separate layers and move data access into adapters, using an interface in the inner circle (`CA12 p.6`).

## 3. Violation of the Dependency Rule

- `[from source] (CA12 p.3)`: source code dependencies point only inward; no **name** from an outer circle may be mentioned by an inner circle (functions, classes, variables). Data formats from outer circles must not be used inside either.
- Examples of symptoms `[extrapolation]`: a use case importing an HTTP request class; a use case directly instantiating a SQL repository.
- Remedy `[from source] (CA12 p.5-6)`: apply the DIP; the use case calls an interface (output port) declared in the inner circle; the outer layer implements it.

## 4. Data "cheating" at the boundaries

- `[from source] (CA12 p.6)`: what crosses boundaries are simple, isolated data structures; Entities or database rows must not be passed; the `RowStructure` example illustrates the violation.
- Additional risks (coupling the public JSON contract to the internal model, *mass assignment*) are `[extrapolation]`: the PDF does not mention them.

## 5. Mixed reasons for change (SRP)

- `Employee` with `calculatePay`, `reportHours` and `save` serves different organizations (finance, operations, technology) `[from source] (SRP p.3)`; a change requested by one group can break something another group values and did not ask to change `[from source] (SRP p.4)`.
- Remedy: separate the code by reason for change (`SRP p.5`). The concrete decomposition into classes such as `PayCalculator` and the Facade pattern are `[extrapolation]`.

## 6. Poorly delimited aggregates

- `[from source] (DDD p.23)`: external objects must hold references only to the root; consistency inside the boundary is synchronous and across aggregates is asynchronous; when boundary decisions are not well guided, reconsider the model. `[from source] (DDD p.24)`: repositories only for roots that need direct access; unrestricted queries that instantiate interior objects "ambush" the root.
- "Giant aggregate" (the `CustomerAggregate` example with all orders and invoices), "OptimisticLockException" and "hundreds of megabytes" are illustrations `[extrapolation]`; the PDF only states that cautious locks cause useless interference between users (p.23).
- Reference between aggregates by ID: widespread practice `[extrapolation]` (not in the booklet).

## 7. Big Ball of Mud and model contamination

- `[from source] (DDD p.45)`: without consistent model boundaries the system becomes a big ball of mud, where "dependencies criss-cross" and cause and effect are hard to trace; the pattern says to draw a boundary around it, not to apply sophisticated modeling there, and to watch for its tendency to spread. `[from source] (DDD p.41)`: an anticorruption layer protects the downstream model from a weak upstream.
- Combining the two ideas (isolating the BBoM and integrating via an ACL) is `[inference]`. "Within a few months the concepts leak" is an illustration `[extrapolation]`.

## 8. Dialects and the single corporate model

- `[from source] (DDD p.10)`: experts and technicians speaking different dialects "blunt" communication; `[from source] (DDD p.9)`: multiple models are inevitable, and mixing code from distinct models produces buggy software. The condemnation of the "single corporate model" as a "catastrophic illusion" is **not** a sentence from the PDF; the conclusion that a single universal model is not the prescription is an `[inference]` from p.9.

## 9. Mutable state, control and caches

- `[from source] (TARPIT p.6-8)`: state harms testing (a test in one state says nothing about another) and informal reasoning; the number of states doubles with each bit; there is contamination by stateful procedures. `[from source] (TARPIT p.8-10)`: control over-specifies the *how*; concurrency makes tests non-repeatable.
- Caches and stored derived values are **accidental state** in the ideal world `[from source] (TARPIT p.25-27)`; they may be necessary for performance, with the risk of inconsistent state `[from source] (TARPIT p.30-31)`.
- Remedy from the paper `[from source] (TARPIT p.31-36)`: avoid what is not essential and separate essential from accidental. The specific recommendation "immutable VOs" comes from `DDD p.19`; "pure functions" comes from referential transparency (`TARPIT p.15`). Combining the two is an `[inference]`.

## 10. Premature optimization

- `[from source] (TARPIT p.36-37)`: optimizing a simple system is easier than removing complexity from a complex system that was designed to be fast.

## 11. Synchronous coupling and cascading failure (reactive view)

- `[from source] (REACT p.1-2)`: resilience through replication, containment, isolation and delegation; asynchronous messaging with isolation and flow control through queues and back-pressure.
- Specific patterns (circuit breaker, bulkhead, retry with backoff, saga) are **not in** the corpus `[extrapolation]`.

## 12. Boundary of what each text solves

| Problem | Main source | Caution |
| :--- | :--- | :--- |
| Language and model boundaries | `DDD p.9-12, 36-45` | Booklet is a summary; no code |
| Dependency direction in code | `CA12 p.3-7` | Blog; diagram not legible in the PDF |
| Reasons for change | `SRP p.1-5`, `SREL p.2` | Does not use "actor" |
| Extension without modification, plugins | `OCP p.1-4` | No report example |
| State and control as complexity | `TARPIT p.6-11, 21-36` | 2006 paper; FRP is hypothetical |
| Resilient and elastic systems | `REACT p.1-2` | Short manifesto; no techniques |
