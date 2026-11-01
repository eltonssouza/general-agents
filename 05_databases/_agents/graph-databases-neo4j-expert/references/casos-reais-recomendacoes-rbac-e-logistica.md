# Real cases from the book: recommendations (Talent.net), access control (TeleGraph) and logistics (Global Post)

Source: NEO4J ch. 5. Pages = **PDF** (printed = N − 18). The company names are fictitious (the book warns that names, context, models and queries were altered) [from source] (NEO4J p.123, p.129).

## 1. Why organizations choose graph databases
Four reasons: performance "from minutes to milliseconds"; much faster development cycles (less impedance mismatch); extreme business responsiveness (a schemaless model evolves); "enterprise ready" (ACID, high availability, read scaling, billions of entities) [from source] (NEO4J p.123-124).

## 2. Common use cases cited
- Social (explicit vs implicit); recommendations (inductive, not deductive); geo (Euler and the bridges of Königsberg; R-trees); MDM; network and data center management (top-down and bottom-up impact analysis); authorization and access control (millisecond queries over structures with billions of parts) [from source] (NEO4J p.124-129).
- The book says graphs "do not necessarily" deliver a complete MDM solution [from source] (NEO4J p.127).

## 3. Talent.net (professional network)
- Model: `User` connects to the company through `WORKS_FOR`, to topics through `INTERESTED_IN` and to projects through `WORKED_ON`; the social ties are **inferred**, not declared [from source] (NEO4J p.129-130).
- Query 1, colleagues with interests in common: matches `WORKS_FOR` and `INTERESTED_IN`, counts interests as `score` and collects the names with `collect`; orders by `score` [from source] (NEO4J p.132-133).
- Variant: remove the same-company requirement and include the company in the `RETURN` [from source] (NEO4J p.133-134).
- Query 2, colleagues and colleagues-of-colleagues with certain interests: path `(subject)-[:WORKED_ON]->(:Project)-[:WORKED_ON*0..2]-(:Project)<-[:WORKED_ON]-(person:User)-[:INTERESTED_IN]->(interest:Topic)`; `WITH person, interest, min(length(p)) as pathLength` filters redundant paths; the distance is `(pathLength - 1)/2`; the book warns that long variable-length paths are relatively inefficient and that they should be restricted [from source] (NEO4J p.135-136).
- Result ordered by `score`, not by distance (Arnold, 2 hops away, beats Charlie, 1 hop away) [from source] (NEO4J p.137).
- Optimization: precomputed `WORKED_WITH` relationship (shortcut) for the site's most frequent pattern; it is updated asynchronously by a queue with a single *writer thread* using `CREATE UNIQUE`; direction ignored in queries [from source] (NEO4J p.139-140).
- Book note: the graph traverses relationships in both directions at the same low cost; reciprocity must be decided by the domain [from source] (NEO4J p.139).
- Time "under 10 ms" and "nightly MapReduce batch" (v1): are **not** in the book.

## 4. TeleGraph (access control)
- Problem: relational system with recursive joins and stored procedures; generating the view of what an administrator manages takes many minutes [from source] (NEO4J p.141).
- Model: administrators in groups; groups linked to organizational units by `ALLOWED_INHERIT`, `ALLOWED_DO_NOT_INHERIT` and `DENIED`; `DENIED` takes precedence over `ALLOWED_INHERIT`, but is subordinate to `ALLOWED_DO_NOT_INHERIT` [from source] (NEO4J p.142-143).
- They tested two models (fine-grained types vs a single `PERMISSION` type with properties); the fine-grained types were almost twice as fast [from source] (NEO4J p.143).
- Query "everything the administrator accesses": two queries joined by `UNION` (`ALLOWED_INHERIT` minus `DENIED`, then `ALLOWED_DO_NOT_INHERIT`), with `[:CHILD_OF*0..3]` [from source] (NEO4J p.144-145).
- Checking access to a resource: label employees and accounts as `Resource` and count paths (`accessCount`); the Java client tests whether any value is greater than zero [from source] (NEO4J p.147-148).
- "Bottom-up" view: given a resource, who administers it [from source] (NEO4J p.148-149).
- The v1 query `MEMBRO_DE*0..` / `POSSUI_PAPEL` / `CONCEDE_ACESSO` was [extrapolation] and is **not** the TeleGraph model.

## 5. Global Post (logistics)
- Requirements: 1 to 3 thousand parcels per second enter the network; the route must be computed in milliseconds before the sorting machine decides; routes change by period; the model must allow significant evolution for 10+ years [from source] (NEO4J p.150).
- Model: ~25 national parcel centers and ~2 million delivery units; parcel centers linked to delivery bases, which cover areas, divided into segments; delivery units stay outside the graph and are indexed by segment [from source] (NEO4J p.150, p.153).
- Relationships `CONNECTED_TO` (upper part) and `DELIVERY_ROUTE` (lower) partition the graph and give efficient traversals; both have `start_date` and `end_date` [from source] (NEO4J p.153).
- Route in three legs: go up from the start and from the end to the bases (trees) and cross the upper part by weighted shortest path [from source] (NEO4J p.154-156).
- Cypher: four subqueries with `WITH`, `all(...)` for the period, `reduce` summing `cost`, `ORDER BY score ASC LIMIT 1` [from source] (NEO4J p.157-159).
- Alternative implementation with the Traversal Framework: `PathExpander` for the interval; depth-first search with `Evaluator` to find the bases; `GraphAlgoFactory.dijkstra` for the upper leg; adopted because every millisecond affects the cluster size [from source] (NEO4J p.160-164).
- The v1 "Campinas → Recife" example is invented. Dijkstra is **not** executed "natively in Cypher" in the book: it comes from the Java algorithms library.

## 6. What the book does NOT say
- It provides no millisecond benchmarks for these systems beyond the general claims of "minutes to milliseconds" (NEO4J p.123).
- It does not use the terms RBAC/GBAC (the case is "authorization and access control").
