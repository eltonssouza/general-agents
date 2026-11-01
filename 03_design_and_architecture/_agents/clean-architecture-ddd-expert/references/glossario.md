# Bilingual glossary (with PDF pages)

Corpus terms. **Convention**: `(ACRONYM p.N)` = **PDF** page (DDD: printed = N − 7). A term without a page is not in the PDF (`[extrapolation]`).

### A
- **Accidental Complexity (complexidade acidental)**: everything that is not essential; complexity the team would not have to deal with in the ideal world (for example, that which comes from performance and from suboptimal language and infrastructure) `[from source] (TARPIT p.21)`.
- **Aggregate (agregado)**: a set of entities and VOs with a boundary and a root; invariants enforced by the root; the boundary governs transactions and distribution `[from source] (DDD p.23)`.
- **Aggregate Root (raiz do agregado)**: the chosen entity; external objects hold references only to it `[from source] (DDD p.23)`.
- **Anticorruption Layer (ACL, camada anticorrupção)**: an isolating layer on the downstream side that expresses the upstream in terms of its own model `[from source] (DDD p.41)`.
- **Assertions (asserções)**: explicit postconditions and invariants (code or tests) `[from source] (DDD p.29)`.

### B
- **Back-pressure**: applied in queue management for flow control in message-driven systems `[from source] (REACT p.2)`.
- **Big Ball of Mud**: parts of the system without consistent model boundaries; delimit with a boundary and do not model sophisticatedly `[from source] (DDD p.45)`.
- **Bounded Context (contexto delimitado)**: a boundary within which a model is defined and applicable `[from source] (DDD p.6, 9)`.

### C
- **Clean Architecture**: name of the 2011 post (`CA11 p.1`) and of the 2012 one that presents the circles and the Dependency Rule `[from source] (CA12 p.3)`.
- **Conformist**: the downstream adheres to the upstream's model `[from source] (DDD p.40)`.
- **Context Map**: a view of the models and their contexts, with points of contact `[from source] (DDD p.36)`.
- **Control (controle)**: the order in which things happen; a cause of complexity when needlessly specified `[from source] (TARPIT p.8-9)`.
- **Core Domain (domínio central)**: the valuable core of the model, to be kept small and given the best talent `[from source] (DDD p.47)`.
- **Customer/Supplier**: a relationship in which the downstream's needs enter the upstream's planning `[from source] (DDD p.39)`.

### D
- **Dependency Inversion Principle (DIP)**: "depend in the direction of abstraction" `[from source] (SREL p.4-5)`; used to make dependencies oppose the flow of control `[from source] (CA12 p.5-6)`.
- **Dependency Rule (Regra de Dependência)**: source code dependencies can only point inward `[from source] (CA12 p.3)`.
- **Domain Event (evento de domínio)**: something that happened and that interests the experts; an immutable domain object `[from source] (DDD p.20)`.
- **Domain Service**: the text calls it only **Services** (a standalone operation when something is not the natural responsibility of an entity/VO) `[from source] (DDD p.21)`.

### E
- **Elastic (elástico)**: stays responsive under varying load `[from source] (REACT p.2)`.
- **Entity (entidade)**: an object defined by identity and continuity `[from source] (DDD p.18)`.
- **Entities (circle)**: enterprise business rules `[from source] (CA12 p.3)`.
- **Essential Complexity**: inherent to the problem, as seen by the users `[from source] (TARPIT p.21)`.
- **Essential State / Essential Logic**: FRP components (state in relations; relational logic and pure functions) `[from source] (TARPIT p.44-45)`.

### F
- **Factory (fábrica)**: encapsulates the creation of complex aggregates/VOs `[from source] (DDD p.25)`.
- **FRP (Functional Relational Programming)**: a hypothetical approach that unites functional programming and the relational model `[from source] (TARPIT p.42)`.
- **Functional Core, Imperative Shell**: a pattern by Gary Bernhardt `[extrapolation]`; it is **not** in the paper.

### G-I
- **Generic Subdomain**: a cohesive subdomain that is not the motivation of the project `[from source] (DDD p.48)`.
- **Interface Adapters**: adapters that convert data between use cases/entities and external agents `[from source] (CA12 p.4)`.
- **Interface Segregation Principle (ISP)**: keep interfaces small so that nobody depends on what they do not need `[from source] (SREL p.4)`.

### L-M
- **Liskov Substitution Principle (LSP)**: a program that uses an interface must not be confused by an implementation of it; it deals with subtyping `[from source] (SREL p.3-4)`.
- **Message Driven**: communication by asynchronous messages `[from source] (REACT p.2)`.
- **Module**: part of the model, not only of the code `[from source] (DDD p.22)`.

### O
- **Observers / Feeders (FRP)**: output and input components `[from source] (TARPIT p.46-47)`.
- **Open-Closed Principle (OCP)**: extend behavior without modifying the system `[from source] (OCP p.2)`.
- **Open-host Service**: an open protocol that gives access to the subsystem as services `[from source] (DDD p.42)`.

### P-R
- **Partnership**: a cooperative relationship between teams that succeed or fail together `[from source] (DDD p.37)`.
- **Published Language**: a shared, documented language `[from source] (DDD p.43)`.
- **Reactive Systems**: Responsive, Resilient, Elastic and Message Driven systems `[from source] (REACT p.1)`.
- **Referential Transparency (transparência referencial)**: given the same set of arguments, the function always returns the same result `[from source] (TARPIT p.15)`.
- **Repository**: a service with the illusion of an in-memory collection of the roots of a type `[from source] (DDD p.24)`.
- **Resilient**: stays responsive in the face of failures `[from source] (REACT p.1)`.
- **Responsive**: responds in a timely manner `[from source] (REACT p.1)`.

### S
- **Screaming Architecture**: title of an earlier post by the author, only **mentioned** in `CA12 p.2`; the explanation of the concept is not in the PDFs `[extrapolation]`.
- **Separate Ways**: a context without connection to the others `[from source] (DDD p.44)`.
- **Shared Kernel**: a small subset of the model shared by teams `[from source] (DDD p.38)`.
- **Single Responsibility Principle (SRP)**: one and only one reason to change `[from source] (SRP p.2)`; reasons for change come from people `[from source] (SRP p.4)`. "Actor" is a later term `[extrapolation]`.
- **State (estado)**: in the paper, mutable state `[from source] (TARPIT p.6)`.
- **Supple Design**: design that invites change `[from source] (DDD p.26)`.

### U-V
- **Ubiquitous Language**: a language structured around the model `[from source] (DDD p.6, 10-11)`.
- **Use Cases (circle)**: application-specific business rules `[from source] (CA12 p.3-4)`.
- **Value Object**: an object without conceptual identity, treated as immutable `[from source] (DDD p.19)`.
