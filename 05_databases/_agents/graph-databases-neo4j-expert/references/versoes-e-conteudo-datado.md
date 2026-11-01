# Versions, dated syntax and what the collection does not cover

## 1. Version of the sources
- **NEO4J**: 2nd edition, copyright 2015 (NEO4J p.4); the preface says Neo4j was at version 2.2, with 2.3 coming soon, and that the Cypher examples were revised to the latest syntax of the time [from source] (NEO4J p.14). The record layout is from 2.2 [from source] (NEO4J p.171). The edition was distributed by Neo Technology (rights 2015) [from source] (NEO4J p.4).
- **NEO_START**: 4 pages of the Neo4j website (© 2026 on the page) with only topic titles, site menu and footer; it **has no technical content** (NEO_START p.1-4). It mentions "Embedding & Vector Indexes", composite database, real-time change capture, centrality algorithms, Graph Data Science and GraphAcademy as topics (NEO_START p.2) without explaining them.

## 2. Map of the book's syntax vs. current versions (all [extrapolation]/[DATED])
Check the current Neo4j documentation and the *Cypher manual* for your version.
| Book (2.x), with page | Current practice (to verify) |
|---|---|
| `{name}` as a parameter (NEO4J p.132) | `$name`; the `{name}` form was deprecated and removed in recent versions |
| `CREATE INDEX ON :Venue(name)` (NEO4J p.65) | `CREATE INDEX FOR (v:Venue) ON (v.name)` (with optional name) |
| `CREATE CONSTRAINT ON (c:Country) ASSERT c.name IS UNIQUE` (NEO4J p.65) | `CREATE CONSTRAINT ... FOR (c:Country) REQUIRE c.name IS UNIQUE` |
| `DROP INDEX ON :Movie(title)` (NEO4J p.121) | `DROP INDEX name` |
| `START` (NEO4J p.49, already deprecated in the book) | removed; use `MATCH` |
| `CREATE UNIQUE` (NEO4J p.139-140) | replaced by `MERGE` |
| `USING PERIODIC COMMIT` (NEO4J p.121) | `CALL { ... } IN TRANSACTIONS` |
| `neo4j-import` (NEO4J p.117) | `neo4j-admin database import` |
| Master-slave HA (NEO4J p.182) | Causal Clustering and, later, database-based clustering (primaries/secondaries) |
| REST API and JAX-RS extensions (NEO4J p.96-99) | Bolt and drivers; procedures in Java |
| Core API, Traversal Framework (NEO4J p.177-179) | procedures/embedded Java; Cypher is the default path |
| `shortestPath` (NEO4J p.106) | remains; also see `allShortestPaths` and the GDS library |

## 3. Topics the collection does **not** cover
Supernodes/dense nodes; time trees with hour; Raft/Causal Cluster; isolation levels; `EXPLAIN`/`PROFILE`; security and native Neo4j RBAC; Bolt; APOC; Graph Data Science; vectors; migration of relational data; multitenancy modeling; backup and restore; observability. When asked, say "the collection does not cover this" and, if you give an answer, label it [extrapolation].

## 4. Origin of the scripts' content
See `scripts/` and `INDEX.md`: linter and advisor rules that go beyond the book's text are [extrapolation] and are printed as such.
