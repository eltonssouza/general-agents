# Cypher: fundamentals and query patterns

Source: NEO4J ch. 3. Pages = **PDF** (printed = N − 18). **Syntax version**: the book's examples are Neo4j 2.x (2.2, with 2.3 "coming soon", according to the preface, NEO4J p.14). Parameters appear as `{name}`, not `$name`; see `versoes-e-conteudo-datado.md`.

## 1. Philosophy
- Cypher is a declarative, compact query language; at the time of the book it was specific to Neo4j [from source] (NEO4J p.45).
- The book describes Cypher as "easy to learn" and aimed at developers, DBAs and stakeholders; the query is an ASCII drawing of the pattern sought ("find things like this") [from source] (NEO4J p.46).
- Other query languages cited: SPARQL and Gremlin (imperative, path-based) [from source] (NEO4J p.45).
- Identifiers allow referring to the same node more than once in the pattern; the pattern of three mutual friends is `(emil)<-[:KNOWS]-(jim)-[:KNOWS]->(ian)-[:KNOWS]->(emil)` [from source] (NEO4J p.46).

## 2. Anchors and specification by example
- To bind the pattern to real data, label and properties are used, e.g. `(emil:Person {name:'Emil'})`; Cypher anchors parts of the pattern and "flexes" the rest around them [from source] (NEO4J p.47).
- The anchor points are determined by labels and predicates; Cypher uses metadata from indexes, constraints and predicates, and it is sometimes useful to give additional hints [from source] (NEO4J p.47).
- Minimal query: `MATCH` followed by `RETURN`; nodes in parentheses, relationships with `-->`/`<--`, name in brackets after a colon, properties in braces [from source] (NEO4J p.47-48).
- The anchor can also be expressed in `WHERE` (same result) [from source] (NEO4J p.48).
- `RETURN` defines what goes back to the client; each matched node is bound to the identifier *lazily* while the client iterates [from source] (NEO4J p.48-49).

## 3. Clauses cited by the book
List on p.49 [from source] (NEO4J p.49): `WHERE`, `CREATE` and `CREATE UNIQUE`, `MERGE`, `DELETE`, `SET`, `FOREACH`, `UNION`, `WITH` and `START` (the latter "deprecated in favor of anchors in `MATCH`").
- `CREATE` builds entire structures in a single transaction; if it fails, nothing stays in the database [from source] (NEO4J p.63).
- `MERGE` ensures the subgraph exists, reusing what matches and creating what is missing; the book uses `CREATE` when adding without caring about duplication and `MERGE` when the domain does not allow duplication [from source] (NEO4J p.64).
- Identifiers exist only in the scope of the query; for durable names, create an index by label and property [from source] (NEO4J p.64).
- `WHERE` can require the presence or absence of paths, labels, relationship names, properties and general predicates [from source] (NEO4J p.67).
- `RETURN` can aggregate, sort, filter and limit; `DISTINCT`, `count`, `ORDER BY` and `collect` are used [from source] (NEO4J p.68-69).
- `WITH` chains parts of the query, passing results forward as in a Unix pipe; it also separates read clauses from `SET` and helps split complex queries [from source] (NEO4J p.49, p.69-70).

## 3.1 Book example (WITH)
`MATCH (bard:Author {lastname:'Shakespeare'})-[w:WROTE_PLAY]->(play) WITH play ORDER BY w.year DESC RETURN collect(play.title) AS plays` [from source] (NEO4J p.69).

## 4. Indexes and constraints
- Indexes optimize locating starting nodes; Cypher allows indexes per label and property combination, and uniqueness constraints for unique values [from source] (NEO4J p.65).
- Syntax of the time: `CREATE INDEX ON :Venue(name)` and `CREATE CONSTRAINT ON (c:Country) ASSERT c.name IS UNIQUE` [from source] (NEO4J p.65).
- On an existing database, indexes are populated in the background and become available when ready; the query works without an index, just slower: without an index Neo4j scans and filters all nodes of the label [from source] (NEO4J p.66).
- For import, the index trades O(n) cost for O(log n) in the existence check; it can be removed afterwards with `DROP INDEX ON :Movie(title)` if it only served the import [from source] (NEO4J p.120-121).

## 5. Parameters
- The book's examples pass values as parameters (`{name}`, `{adminName}`, `{interests}`) in application queries [from source] (NEO4J p.132, p.144, p.135).
- The book does **not** explain plan reuse/plan caching or Cypher injection. Recommending parameters for those reasons is [extrapolation] (general practice and Neo4j documentation; `$param` in current syntax).

## 6. What the book does NOT say
- It does not mention `EXPLAIN`, `PROFILE`, plan operators (`AllNodesScan`, `NodeIndexSeek`), `OPTIONAL MATCH`, `SKIP`, `allShortestPaths`, `CALL {}`, nor `LIMIT` as a rule. Any use is [extrapolation].
- It does not say that the starting node should "always" be labeled: it says the label plus property anchor the query and enable an index (NEO4J p.47, p.65).
