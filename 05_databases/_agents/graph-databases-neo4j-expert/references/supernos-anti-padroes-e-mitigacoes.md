# Supernodes (dense nodes): what the book does NOT cover and what is related

Source: NEO4J. Pages = **PDF** (printed = N − 18).

## 1. Central warning
The book **does not use the terms "supernode" or "dense node" as a topic** and does not discuss supernodes, lock contention on popular nodes or mitigations. Verification by searching the extracted text: no occurrence. The v1 of this package attributed to the book a chapter on "supernodes" (including the e-mail case and the time tree as a solution); that was **false** and was removed. The book's e-mail case deals with relationships that lose information (see `casos-e-antipadroes.md`).

## 2. What the book says that is related
- The node record has an `extra` byte for flags; one of them identifies **densely connected nodes** (the book explains no more than that) [from source] (NEO4J p.172).
- Choosing another relationship means walking the node's linked list of relationships until a candidate is found (by type or property value) [from source] (NEO4J p.173).
- Differentiating by relationship name eliminates large portions of the graph in the traversal (see `diretrizes-de-modelagem-em-grafo.md`) [from source] (NEO4J p.85).
- If "everyone is a friend of Bob", the query for Bob's friends ends up considering the entire set [from source] (NEO4J p.36).
- Contention: an operation that competes for exclusive access (writes) to a part of the graph can have latency so high that it looks unavailable; in the graph, access patterns tend to be more distributed when queries are graph-local, starting from meaningful domain nodes [from source] (NEO4J p.183).
- Queries of a recommendation application need the "local" graph (they start from identifiable points and explore the neighborhood) [from source] (NEO4J p.126).
- Low-cardinality data: the book gives no rule about "not creating gender/status nodes". That is an [inference] from the guideline to use properties for attributes (NEO4J p.85).

## 3. Common mitigations (all [extrapolation])
- Introduce intermediate nodes to partition the fan-out (by type, period or region).
- Prefer specific relationship types and filter by type and direction in the query.
- Avoid traversals that pass through the popular node when one of the sides is enough.
- Later Neo4j versions handle dense nodes with their own structures (grouping relationships by type/direction); the exact optimization depends on the version: check the current documentation.
- Always record the measurement (relationship count per node) before deciding to refactor.

Verification example (Neo4j 2.x syntax from the book, only to count): `MATCH (n:Categoria) RETURN n.nome, size((n)--()) AS grau ORDER BY grau DESC LIMIT 10` is [extrapolation]; in current versions prefer `COUNT { (n)--() }`.

## 4. Thresholds
The numbers "50,000" and "5,000" relationships from the v1 script (`graph_advisor.py`) **do not come from the book**; the v2 script receives them as declared parameters [extrapolation].
