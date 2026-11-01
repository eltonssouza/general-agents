# Functional Relational Programming (FRP) in Out of the Tar Pit

Source: Moseley and Marks, *Out of the Tar Pit* (`TARPIT`), sections 8-12 (p.37-64). **Convention**: `(TARPIT p.N)` = PDF page (= printed page). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

> **Warning about the name.** In the paper, **FRP = Functional Relational Programming** (functional + relational model). The text itself warns, in a footnote, not to confuse it with *functional reactive programming*, which has some similarities but no intrinsic focus on relations `[from source] (TARPIT p.42)`. Also **not** in the paper is the expression "Functional Core, Imperative Shell", from the speaker Gary Bernhardt: the correspondence below is `[extrapolation]`.

> **FRP is hypothetical.** The paper states that FRP is "purely hypothetical", unproven in practice, although based on widely proven principles; the authors only created experimental, symbolic implementations of FRP infrastructures `[from source] (TARPIT p.42)`. A prototype of the essential state and logic in about 1500 lines of Scheme is cited (p.49). The conclusion is cautious: "it may not be FRP, but there is no doubt that it is simplicity" `[from source] (TARPIT p.64)`.

---

## 1. The relational model (section 8, p.37-42)

- The relational model, according to the authors, has **nothing intrinsically tied to databases**: it is a way of structuring data, manipulating it and maintaining integrity; it applies to state in any context `[from source] (TARPIT p.37)`.
- Four aspects: **structure** (relations), **manipulation** (specifying derived data), **integrity** (inviolable constraints) and **data independence** (logical/physical separation) `[from source] (TARPIT p.37)`.
- Warning from the text: SQL does not accurately reflect the relational model; do not equate the two `[from source] (TARPIT p.37)`.
- Relational algebra (restrict, project, join etc.) and extensions (general computations, aggregations, grouping, renaming) `[from source] (TARPIT p.41-42)`. The algebra is **not** Turing-complete `[from source] (TARPIT p.42)`.

## 2. The components of an FRP system (section 9.1, p.43-49)

The system is built with **separate specifications** for four components `[from source] (TARPIT p.43)`:

| Component | Content | Note | Page |
| :--- | :--- | :--- | :---: |
| **Essential State** ("State") | Relational definition of the state: names and types of the *base relvars*; all state is stored in relations, without exception | Only data entered directly by users should be essential state | p.44 |
| **Essential Logic** ("Behaviour") | Definitions of derived relations (relational algebra), integrity constraints (boolean expressions that are always true) and user-defined pure functions | No performance considerations here; "denormalizing for performance" makes no sense at this level | p.44-45 |
| **Accidental State and Control** ("Performance") | A series of declarative, isolated *hints* (they do not reference each other) to the infrastructure: store a derived relvar, physical storage strategies, indexes, parallel evaluation, eager/lazy | A change here never requires changing the essential logic | p.45-46 |
| **Other** (interfaces) | Feeders (input -> relational assignments to the essential state) and Observers (output/effects from changes in derived relvars) | Must be minimal; may be imperative; observers must not replace integrity constraints nor update the essential state directly | p.46-47 |

- The infrastructure that executes the FRP specification (storing relvars, manipulation language, evaluating algebra, enforcing integrity, physical storage mechanisms) is described on p.47-49; according to the text, **no real FRP infrastructures existed** at the time `[from source] (TARPIT p.49)` `[DATED]`.
- **Claimed benefits** `[from source] (TARPIT p.50-53)`: avoids useless accidental state and the risk of "bad state" (derived data is normally not stored), reduces code volume and eases distributed implementations (no pointers or access paths).
- **Data abstraction**: section 9.2.4 argues that unnecessary data abstraction (grouping items into composite types with hidden content) is another common and serious cause of complexity, because the grouping is subjective and heavy encapsulation erodes referential transparency; FRP discourages *data hiding* and offers neither nested relations nor product types `[from source] (TARPIT p.52-53)`. This **contrasts** with DDD's emphasis on rich, encapsulated models `[inference]`; the two texts have different premises (a hypothetical relational system vs. object-oriented modeling).
- **Example** (section 10, p.54-63): a real estate agency system (properties, offers, decisions, commissions) with relvars and derived relations in pseudocode; 10.4 deals with accidental state (p.62) and 10.5 with feeders/observers (p.63) `[from source] (TARPIT p.54-63)`. **Related work** (section 11) is in `[from source] (TARPIT p.63)`.

## 3. Relationship with the "Recommended Architecture" of section 7

- The same three blocks (essential state, essential logic, accidental state and control) are in **Figure 1** with static reference arrows: essential state does not depend on the others; essential logic depends on the essential state; the accidental depends on both `[from source] (TARPIT p.35-36)`. **Figure 2** (p.43) shows the dynamic data flow of FRP.
- For the Clean Architecture reader: the arrow "the essential does not reference the accidental" recalls the Dependency Rule `[inference]`: both are rules of **reference direction** that protect the core. But they are distinct models: in `TARPIT` the split is state/logic/accidental, in `CA12` it is entities/use cases/adapters/frameworks `[inference]`. The paper does not make this comparison.

## 4. "Functional Core, Imperative Shell" (extrapolation)

`[extrapolation]` Bernhardt's pattern (a core of pure functions with an imperative shell at the edge) is **inspired by ideas similar to** those of the paper (separating pure logic from effects), but is not described in it. Useful points, labeled:
- Pure functions and immutable data in the core, effects at the edge: consistent with the recommendation to separate essential logic from accidental state and control `[inference]` (TARPIT p.31-36) and with referential transparency (p.15).
- "Testable without mocks": a consequence of referential transparency, which removes a weakness of testing (p.15) `[inference]`.
- Statements such as "never accesses the clock" and "thin shell" are prescriptions of Bernhardt's pattern `[extrapolation]`.

## 5. What the paper does not cover

CQRS, Event Sourcing, NoSQL databases, specific modern languages (Haskell appears only as an example of a pure language, p.15), microservices architecture and any empirical evidence for FRP.
