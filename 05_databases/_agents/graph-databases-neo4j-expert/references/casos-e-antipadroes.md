# Common mistakes and antipatterns that the book actually describes

Source: NEO4J. Pages = **PDF** (printed = N − 18). Each item states the problem, the consequence and the fix according to the book. Antipatterns the book does **not** cover are in section 4, labeled.

## 1. Modeling

### 1.1 Entity hidden in a relationship (e-mail "EMAILED")
- Problem: modeling "Bob emailed Charlie" as `(bob)-[:EMAILED]->(charlie)`, with `CC` and `BCC` also between people; the graph becomes a star around Bob [from source] (NEO4J p.70-72).
- Consequence: the model is "lossy": one sees that an exchange took place, but not the e-mail itself; even with properties on `EMAILED`, `EMAILED`, `CC` and `BCC` cannot be correlated per message [from source] (NEO4J p.72-73).
- Cause: loose use of language; the focus on the verb "emailed" erased the noun [from source] (NEO4J p.73).
- Fix: an `Email` node with `SENT`, `TO`, `CC`, `BCC` [from source] (NEO4J p.73-74).

### 1.2 Reusing relationships ambiguously (FORWARDED, REPLIED_TO)
- Problem: `(alice)-[:REPLIED_TO]->(email)` does not say whether it was a reply to the author or to all; reusing `TO` for forwarding mixes the recipient with who received the forwarded version [from source] (NEO4J p.76-77).
- Fix: the reply is a new `Email` with the additional label `Reply` and `REPLY_TO`; the forward is an `Email:Forward` with `FORWARD_OF` [from source] (NEO4J p.77-80).

### 1.3 Relationship with a property instead of a type (too generic)
- The book presents the trade-off, not a prohibition: properties cost extra I/O because they live in another file; the fine-grained type eliminates large portions of the graph; weights (an open set) go in properties [from source] (NEO4J p.85-86). See `diretrizes-de-modelagem-em-grafo.md`.
- Evidence: in TeleGraph, fine-grained types were almost 2x faster [from source] (NEO4J p.143).

### 1.4 Relationship for something that joins more than two entities
- A relationship has exactly one start node and one end node; if an "entity modeled as a relationship" starts to connect more than two things, refactoring is a "breaking change" [from source] (NEO4J p.85).

### 1.5 Merging or duplicating data at write time to "help" reading
- The book advises against conflating elements at write time to gain query efficiency; trust the database and model by the questions [from source] (NEO4J p.82).
- For performance use a **shortcut** (a direct relationship between nodes linked by intermediaries), keeping the faithful model intact, such as `WORKED_WITH` [from source] (NEO4J p.92, p.139).

### 1.6 Versioning the graph yourself without measuring the cost
- The versioning scheme leaks into every query, even the simplest ones [from source] (NEO4J p.92).

## 2. Queries
- Long, wide variable-length paths are relatively inefficient; restrict the scope [from source] (NEO4J p.136).
- Without an index, the starting point scans and filters all nodes of the label [from source] (NEO4J p.66).
- `MERGE` of a large pattern: it only matches if **all** parts exist; otherwise it creates everything and duplicates; break it into smaller `MERGE`s [from source] (NEO4J p.120).
- In aggregate stores, joins done in the application become prohibitive [from source] (NEO4J p.33).

## 3. Architecture, testing and operations
- Writing through a slave is up to an order of magnitude slower; direct writes to the master [from source] (NEO4J p.99).
- Testing only with a small graph: what runs well with 20 nodes may not scale [from source] (NEO4J p.109).
- A test dataset smaller than memory hides cache evictions; have one that exceeds it [from source] (NEO4J p.112).
- Measuring by average: the book recommends percentiles and warns against assuming a normal distribution [from source] (NEO4J p.111).
- `ImpermanentGraphDatabase` is for unit tests only, not for production [from source] (NEO4J p.105).
- Server extensions can do "dangerous" things and affect GC; monitor [from source] (NEO4J p.96, p.99).
- A transaction opened and abandoned on the server stays held until it expires (default 60 s at the time) [from source] (NEO4J p.96).
- Automatic partitioning of graphs across several machines: the book says it is NP-hard and that there was no proven solution; naive sharding yields unpredictable times [from source] (NEO4J p.187-188).

## 4. Common antipatterns on the internet that the book does NOT cover (all [extrapolation])
- A query with an unlabeled starting node causes a full scan (plan operator "AllNodesScan"): the book only says that, without an index, the starting point scans and filters the nodes of the label (NEO4J p.66).
- Interpolating strings into Cypher vs parameters: the book uses parameters in the examples but does not discuss cached plans or injection.
- An unbounded variable-length path causes out-of-memory (OutOfMemoryError): the book uses the unbounded `FORWARD_OF*` relationship on a small tree (NEO4J p.80) and only warns about inefficiency (NEO4J p.136).
- Supernodes/dense nodes: see `supernos-anti-padroes-e-mitigacoes.md`.
- Composite values in a single string: the book only recommends nodes for complex value types (NEO4J p.89).
- Client-side traversal: the book criticizes joins in the application on aggregate stores (NEO4J p.33), not loops of queries to Neo4j.
