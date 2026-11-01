# Strategic DDD: Bounded Context, Context Map and distillation (DDD Reference)

Source: Eric Evans, *Domain-Driven Design Reference: Definitions and Pattern Summaries* (2015, acronym `DDD`, 59 PDF pages). **Page convention**: `(DDD p.N)` = **PDF** page; the printed page is N − 7 (PDF p.1-7 is front matter with Roman numerals; PDF p.8 is printed page 1). See the map in `INDEX.md`.

Labels: `[from source]` = read on the cited page; `[inference]` = direct deduction from the text; `[extrapolation]` = knowledge external to the PDF; `[DATED]` = practice/technology of the period.

---

## 1. The three-point summary and the base terms

- DDD is presented as an approach to complex software in which one: focuses on the *core domain*, explores models in creative collaboration between domain and software practitioners, and speaks a ubiquitous language within an explicitly bounded context `[from source] (DDD p.8)`.
- The booklet's own glossary defines *domain*, *model*, *ubiquitous language*, *context* and *bounded context* `[from source] (DDD p.6)`.
- The booklet is a **summary of patterns and definitions**, not the full book; it says the patterns distill practices from projects where modeling paid off greatly `[from source] (DDD p.8)`.

## 2. Bounded Context, Ubiquitous Language, Continuous Integration

1. **Bounded Context** `[from source] (DDD p.9)`: several models coexist in any large project (distinct user communities, independent teams, different tools). Mixing code from distinct models produces confusing, buggy software. The prescription is to explicitly define the context in which a model applies, with boundaries in terms of team organization, usage in parts of the application and physical manifestations (code bases, database schemas), and to apply Continuous Integration within it. Formal definition: a boundary (typically a subsystem or the work of one team) within which a model is defined and applicable `[from source] (DDD p.6)`.
2. **Ubiquitous Language** `[from source] (DDD p.10-11)`: the model is the backbone of the language, used in diagrams, writing and, above all, in speech and in code. Changing the language means changing the model; difficulties are resolved by experimenting with alternative expressions and then refactoring class, method and module names. When experts and developers use separate dialects, translation blunts communication (p.10).
3. **Continuous Integration** (in the sense of the DDD pattern) `[from source] (DDD p.12)`: within a context, the model tends to fragment, and the problem grows with the team (three or four people can already have serious problems). The answer is to merge code and artifacts frequently, with automated tests that flag fragmentation, and to exercise the ubiquitous language.
4. Neighboring patterns in the same chapter: *Model-Driven Design* (p.13), *Hands-on Modelers* (p.14), *Refactoring Toward Deeper Insight* (p.15) `[from source]`.

> The "Customer in Sales vs. Delivery" example used in courses is `[extrapolation]`: the PDF explains the concept but does not include this example.

## 3. Context Map and the relationship patterns

- The **Context Map** gives a realistic, large-scale view of the models in play: identify each model and its bounded context (including implicit models of non-object-oriented subsystems), name the contexts, describe points of contact, explicit translation, sharing, isolation mechanisms and levels of influence; map the existing terrain and leave transformations for later `[from source] (DDD p.36)`.
- Supporting terms: *upstream-downstream* (upstream actions affect downstream success, but not the other way around), *mutually dependent* and *free* `[from source] (DDD p.35)`.

The booklet presents **nine** relationship patterns. In the table of contents, `Partnership`, `Big Ball of Mud` (and `Domain Events`) carry an asterisk, which the legend explains as "new term since the 2004 book" `[from source] (DDD p.2-3)`.

| Pattern | What the text says | Page |
| :--- | :--- | :---: |
| Partnership | Teams of two contexts that succeed or fail together form a partnership: coordinated planning, joint management of integration, interfaces evolved cooperatively, interdependent features scheduled for the same release. | p.37 |
| Shared Kernel | A subset of the model (and associated code or database schema) explicitly shared; must be **small**; changes require consultation with the other team; the kernel has its own CI, a bit less frequent than the teams' internal CI. | p.38 |
| Customer/Supplier | Upstream/downstream relationship in which the downstream's priorities enter the upstream's planning; tasks negotiated and budgeted; joint acceptance tests running in the upstream's CI. | p.39 |
| Conformist | The upstream has no motivation to serve the downstream; the downstream eliminates translation by adhering to the upstream's model, accepting a non-ideal model in exchange for simple integration. | p.40 |
| Anticorruption Layer | An isolating layer on the downstream side that offers the upstream's functionality in terms of **its own model**, talking to the other system through the existing interface and translating in one or two directions. | p.41 |
| Open-host Service | Instead of one translator per integration, define an open protocol that gives access to the subsystem as a set of services; idiosyncratic cases use a one-off translator. | p.42 |
| Published Language | A well-documented language shared as a common medium of communication (e.g., an industry's data interchange standards); usually combined with Open-host Service. | p.43 |
| Separate Ways | When features have no significant relationship, declare the context unconnected to the others; integration is expensive and sometimes the benefit is small. | p.44 |
| Big Ball of Mud | Parts of the system without consistent model boundaries; the pattern says to **draw a boundary around the whole mess**, not to apply sophisticated modeling there, and to watch for its tendency to spread to other contexts. | p.45 |

Fidelity notes:
- The idea, common in secondary material, that the downstream "has political power" in Customer/Supplier **does not appear in those terms**; the text speaks of the downstream's priorities entering the upstream's planning (p.39).
- The Big Ball of Mud text (p.45) does **not** mention an ACL: it says to isolate with a boundary. Using an ACL at the edge of a legacy system is a sensible combination of patterns `[inference]` (p.41 says legacy models are generally weak, "if not big balls of mud").
- Concrete formats (JSON Schema, Protocol Buffers) for Published Language, and REST/RPC for Open-host Service, are `[extrapolation]`.

## 4. Distillation and large-scale structure

- **Core Domain** `[from source] (DDD p.47)`: the "real asset" of the business can be obscured; define the core, make it small, apply the best talent, and justify investment in other parts by how they support the distilled core.
- **Generic Subdomains** `[from source] (DDD p.48)`: cohesive subdomains that are not the motivation of the project; factor them into separate modules, give them lower priority, avoid allocating core developers, and consider off-the-shelf solutions or published models.
- *Domain Vision Statement* `[from source] (DDD p.49)`: a description of about one page of the core's value. *Highlighted Core* `[from source] (DDD p.50)`: a document of three to seven sparse pages and/or markup in the repository. *Cohesive Mechanisms* `[from source] (DDD p.51)`. *Segregated Core* `[from source] (DDD p.52)`. *Abstract Core* `[from source] (DDD p.53)`.
- **Large-scale structure** (p.54): *Evolving Order* (p.55), *System Metaphor* (p.56), *Responsibility Layers* (p.57), *Knowledge Level* (p.58), *Pluggable Component Framework* (p.59) `[from source]`. The structure must evolve with the application; "less is more" (p.55).
- **"Supporting Subdomain"** as a third category is **not in this PDF**: the booklet deals with core and generic. The three-type typology is `[extrapolation]` (later DDD literature). The Netflix/Uber examples that the previous version of the package presented were also `[extrapolation]`.

## 5. What the booklet does not cover

It does not cover Event Storming, Domain Storytelling, the three-subdomain typology, microservices, or CQRS/Event Sourcing as a pattern (only the acknowledgments mention CQRS and Event Sourcing as architecture options for a DDD system, p.4). For these topics, answer `[extrapolation]` or say the corpus does not cover them.
