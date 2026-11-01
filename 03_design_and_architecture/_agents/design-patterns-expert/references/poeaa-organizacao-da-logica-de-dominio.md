# PoEAA: organizing domain logic and layers (what the sample lets us state)

**Central warning.** The PDF `PoEAA-SampleChapter-Pearson.pdf` (78 pages) is a **sample** of *Patterns of Enterprise Application Architecture* (Martin Fowler, Addison-Wesley, copyright 2003, PEAA p.5): cover, credits, table of contents, preface, **Introduction** (printed 1-13), **Chapter 3, "Mapping to Relational Databases"** (printed 33-53) and index. **Chapters 1 (*Layering*), 2 (*Organizing Domain Logic*) and 9 (*Domain Logic Patterns*) are not in the PDF.** Therefore formal definitions of Transaction Script, Domain Model, Table Module and Service Layer, the "decision matrix" and the "three layers" in detail **cannot be given as `[from source]`**. Earlier versions of this package carried citations `(PEAA p.18-52)` and a table attributed to Fowler that the sample does not contain; they were removed.

Convention: `(PEAA p.N)` = **PDF page**. Maps: Introduction printed 1 = PDF 26 (N+25); Chapter 3 printed 33 = PDF 40 (N+7). Details in `INDEX.md`. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. What the table of contents proves (PEAA p.8-10)
They exist in the full book, with these **printed** pages: Ch. 1 *Layering* (17): evolution of layers (18), the three principal layers (19), where to run the layers (22); Ch. 2 *Organizing Domain Logic* (25), *Making a Choice* (29), *Service Layer* (30); Ch. 9: *Transaction Script* (110), *Domain Model* (116), *Table Module* (125), *Service Layer* (133, by Randy Stafford); Ch. 8 *Putting It All Together* (95) with subsections "Data Source for Transaction Script / Table Module / Domain Model" `[from source, table of contents only] (PEAA p.8, 10)`. **It proves existence, not content.**

## 2. What the Introduction says (PEAA p.26-38)
- "Architecture": the highest-level breakdown of the system into parts and the decisions that are hard to change; it is subjective (Ralph Johnson) `[from source] (PEAA p.26-27)`. The author's favorite architectural pattern is **layers**; most non-trivial enterprise applications use some form of layered architecture, and the book concentrates on them `[from source] (PEAA p.27)`.
- Enterprise applications: long-lived persistent data, lots of data, concurrent access, many screens, integration with other systems, and "business logic" that is hardly logical, with arbitrary rules that need to be organized in the best way, since they will change `[from source] (PEAA p.28-29)`. Not enterprise applications: fuel injection, word processors, operating systems, compilers, games etc. `[from source] (PEAA p.28)`.
- **Kinds of application** (B2C retailer with high volume and simple logic; leasing with few users and complicated logic; small, simple expense tracking): "there is no single architecture that serves all three"; choosing the architecture requires understanding the problem `[from source] (PEAA p.30-31)`. The author says "alarms" go off when someone says "always do this" `[from source] (PEAA p.30)`.
- Performance: measure before and after; precise terms (response time, responsiveness, latency, throughput, load, efficiency, capacity, scalability); minimizing remote calls is old advice, but verify it `[from source] (PEAA p.31-34)`.
- Patterns: Alexander's definition, "half-baked" (always adapts to the project); the structure of each pattern (name, intent, sketch, motivation, how it works, when to use it, further reading, examples); the examples are not the pattern `[from source] (PEAA p.34-38)`. Limitation: a collection that "does not claim to be a complete guide" `[from source] (PEAA p.38)`.

## 3. What Chapter 3 says about the relationship between domain logic and persistence (PEAA p.40-60)
See `poeaa-mapeamento-para-bancos-relacionais.md` for the detail. Points that touch the choice of domain logic:
- The choice of the architectural data-access pattern is affected by how the domain logic is designed `[from source] (PEAA p.40)`.
- Table Data Gateway combines naturally with Record Set and is the obvious choice with **Table Module**; with **Domain Model** there are other options (Row/Table Data Gateway may be too little or too much; **Active Record** when the domain model is simple and nearly mirrors the tables; **Data Mapper** when the logic is complex) `[from source] (PEAA p.42-43)`.
- Active Record can be seen as a Row Data Gateway with domain logic, especially when seeing repetitive code across several **Transaction Scripts** `[from source] (PEAA p.42)`.
- New schema with simple logic (Transaction Script or Table Module): design the tables around the data and use Row/Table Data Gateway; with Domain Model, beware of a design that looks like a database; do not spend six months building a model without a database: iterate in cycles of at most six weeks `[from source] (PEAA p.55)`.

## 4. General knowledge (outside the sample), ALWAYS labeled
`[extrapolation]` Widely known summary descriptions, without a PDF page:
- *Transaction Script*: one procedure per business transaction; simple, tends toward duplication as complexity grows.
- *Domain Model*: object model with data and behavior; costly to map; suited to complex rules.
- *Table Module*: one instance per table, common with Record Set.
- *Service Layer*: boundary of the application's operations, coordinating use cases.
For any comparative statement or number (for example, "from what complexity"), consult Ch. 2 of the full book: **the PDF does not allow verification**.

## 5. What is NOT included (do not attribute to PEAA)
- "Three principal layers: presentation, domain, data source" in detail (Ch. 1 is not present; the Introduction only says layers are the preferred pattern, p.27; Ch. 3 calls the "data source layer" the data source layer, p.40).
- The "Martin Fowler Decision Matrix" table, a "learning curve" per pattern, "Table Module typical of .NET 1.1" as historical context.
- Service Layer "controls ACID transactions": not in the sample.
