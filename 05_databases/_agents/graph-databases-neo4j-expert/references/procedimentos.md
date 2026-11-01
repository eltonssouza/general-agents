# Procedures based on the book

Source: NEO4J. Pages = **PDF** (printed = N − 18). Only procedures the book actually describes are here; details in other files. Neo4j 2.x syntax: check the current documentation before running.

## P1. Model from questions
1. Write the user story and extract entities, relationships and the question [from source] (NEO4J p.84).
2. Rewrite the goals as questions; identify entities and relationships; translate to Cypher paths; express questions as patterns [from source] (NEO4J p.81).
3. Nouns become labels, verbs with an object become relationships, proper nouns become nodes with properties [from source] (NEO4J p.81).
4. Beware of "verbing": look for the hidden noun (e-mail, review) [from source] (NEO4J p.82).

## P2. Test the plausibility of a model
1. Read the graph as sentences from a starting node, following relationships and reading labels and names [from source] (NEO4J p.58).
2. Write the query for each use case (e.g., find assets with `status = 'down'` between the user and the application) [from source] (NEO4J p.58-59).
3. Write unit tests with small graphs for the normal and the exceptional case [from source] (NEO4J p.103-104).

## P3. Record events in a timeline tree
See `modelagem-temporal-time-trees-e-intervalos.md` (`MERGE` of `Year`, `Month`, `Day` and the event, starting from a `Timeline` node) [from source] (NEO4J p.91).

## P4. Choose a relationship type
1. Closed set of names: fine-grained types; open set (weights): property [from source] (NEO4J p.86).
2. Also needs "all": fine-grained types plus a generic one (e.g., `ADDRESS`) or a list of types in the query [from source] (NEO4J p.86).
3. Optimize the critical path: create a direct shortcut, such as `WORKED_WITH`, updated asynchronously by a queue [from source] (NEO4J p.92, p.139).

## P5. Data loading
- Initial: `neo4j-import` with CSVs [from source] (NEO4J p.117-118).
- Batch: `LOAD CSV` with `MERGE` in parts, an index on what `MERGE` looks up, and `USING PERIODIC COMMIT` [from source] (NEO4J p.119-121).
- Details in `arquitetura-testes-capacity-e-importacao.md`. [DATED]

## P6. Plan capacity
1. Build a representative dataset early [from source] (NEO4J p.112).
2. Estimate the on-disk store size with that dataset and compute memory: page cache (ideally the whole store) and modest heap [from source] (NEO4J p.112, p.115).
3. Redundancy: the number of failures tolerated determines instances (3 or 4 for 1; 5 for 2) [from source] (NEO4J p.116).
4. Load: `(1000 / average time in ms) × cores × machines` [from source] (NEO4J p.116).

## P7. Measure performance
Query tests: registered suite, in CI, one thread, random starting nodes; application tests: percentiles [from source] (NEO4J p.109-111).

## P8. Cluster (master-slave HA, DATED)
Writes to the master (replication via `ha.tx_push_factor`/`ha.tx_push_strategy`); two balancers (read and write) if using REST for Cypher; *read your own writes* with consistent routing [from source] (NEO4J p.99-102).

## P9. Mitigate a highly connected node
The book provides no procedure. See `supernos-anti-padroes-e-mitigacoes.md` ([extrapolation]).

## P10. Version changes
For any Neo4j version later than 2.x, label [DATED]/[extrapolation] and direct the user to check the current documentation (`versoes-e-conteudo-datado.md`).
