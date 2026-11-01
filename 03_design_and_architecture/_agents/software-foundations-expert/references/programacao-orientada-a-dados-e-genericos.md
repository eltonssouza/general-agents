# Data-directed programming and generic operations

Source: SICP 2.4 and 2.5 (PDF pages; see `INDEX.md`).

## 1. The problem of multiple representations (SICP 2.4)
- `[from source]` (SICP p.168): abstraction barriers isolate the representation, but there may be more than one useful representation for the same object, and systems are designed by many people over time, under changing requirements; it is not possible for everyone to agree on the representation in advance.
- `[from source]` (SICP p.169-171): complex numbers can be represented in **rectangular** form (real and imaginary parts) or **polar** form (magnitude and angle). Addition and subtraction are natural in terms of real/imaginary parts; multiplication and division, in terms of magnitude/angle (formulas and `add-complex`, `mul-complex` at SICP p.171). The book calls the example "simple but unrealistic" (SICP p.169); note 43 (p.182) says that in practice the rectangular form is usually preferable because of rounding errors.
- `[from source]` (SICP p.169): the complex-number system has two kinds of barrier: "horizontal" ones (as in figure 2.1) and a "vertical" one that allows designing and installing alternative representations separately.
- `[from source]` (SICP p.172): "principle of least commitment": the constructor/selector barrier allows postponing the choice of representation to the last moment.

## 2. Tagged data and explicit type dispatch (SICP 2.4.2-2.4.3)
- `[from source]` (SICP p.172-175): for two representations to coexist, each datum must be tagged (`attach-tag`, `type-tag`, `contents`); generic selectors (`real-part`, etc.) do *dispatching on type*; this discipline of attaching/stripping tags is organizational (SICP p.175).
- `[from source]` (SICP p.175-176): dispatch with `cond` has two weaknesses: (1) the implementer of the generic selectors must know all the representations and add a clause for each new one; (2) procedure names cannot collide across the whole system. The book summarizes: the technique is **not additive**.
- `[from source]` (SICP p.176): the problem "is real" in systems such as large database managers.

## 3. Data-directed programming (SICP p.176-182)
- `[from source]` (SICP p.176-177): key observation: a set of generic operations over a set of types forms a **two-dimensional table** (operations on one axis, types on the other); figure 2.22 shows this table. The procedures `put` and `get` install and look up entries indexed by operation and type (SICP p.177).
- `[from source]` (SICP p.177-178): each representation becomes a *package* (`install-rectangular-package`, `install-polar-package`) whose procedures are internal to the package (no name conflicts) and registered in the table with `put`.
- `[from source]` (SICP p.178-179): `apply-generic` looks up in the table the procedure for the operation and the argument types, applies it to the `contents`, or signals an error ("no method for these types"); the generic selectors become calls to `apply-generic` and **do not change** when a representation is added (SICP p.179).
- `[from source]` (SICP p.183): the generic arithmetic system is *additive*: packages can be designed separately and combined without modification.
- `[inference]` (from SICP p.176-179): "modular additivity" = installing a new package without touching existing code. The v1 table with a `quaternion` column is **our illustrative example**, not the book's.

## 4. Message passing (SICP p.181-182)
- `[from source]` (SICP p.181): instead of decomposing the table by *rows* (each operation does its own dispatch), it is decomposed by *columns*: "intelligent objects" that dispatch on the operation name; `make-from-real-imag` returns a `dispatch` procedure that responds to `'real-part`, `'imag-part`, `'magnitude`, `'angle`.
- `[from source]` (SICP p.182): the book says message passing is not a mathematical trick, but a useful technique for organizing systems with generic operations, and that it will be a tool for simulation in ch. 3; exercise 2.76 asks to compare the three strategies for adding types or operations.
- `[extrapolation]`: the v1 claim that the technique is "the conceptual foundation of object-oriented programming based on actors or prototypes" is **not** in SICP (p.181-182); remove as an attribution. The relation to OO is the reader's inference.

## 5. Systems with generic operations, coercion and hierarchies (SICP 2.5)
- `[from source]` (SICP p.188): operations across distinct types (for example, complex + ordinary number) could be handled with one procedure per type combination, which is laborious.
- `[from source]` (SICP p.189-190): alternative: **coercion**. Coercion procedures (`scheme-number->complex`) are installed in a coercion table; `apply-generic` tries the operation and, if there is no method, tries to coerce one argument to the type of the other. Advantage: one procedure per pair of types (possibly n² for n types) instead of one per combination of operation and types (SICP p.190). Limit: it may be necessary to convert both to a third type.
- `[from source]` (SICP p.190-191): **tower of types** (integer ⊂ rational ⊂ real ⊂ complex); each type provides a `raise` procedure that takes it one level up; the system "raises" the lower types until they match (exercises 2.83-2.84); the tower simplifies adding types and allows "inheritance" of operations from the supertype.
- `[from source]` (SICP p.192): hierarchies are not always towers: a type can have several subtypes and several supertypes (geometric figures, figure 2.26), and then there is no single way to "raise"; the book says dealing with many interrelated types while preserving modularity is very difficult and a research area.

## 6. What the book does not say
- It does not use "quaternion" in the example; it does not relate the technique to actors/prototypes; it does not define "additivity" beyond "adding without modifying" (SICP p.176).
