# Advanced Cypher: variable-length paths, shortest path and composition

Source: NEO4J chs. 3-5. Pages = **PDF** (printed = N − 18). Neo4j 2.x syntax (see `versoes-e-conteudo-datado.md`).

## 1. Variable-length paths
- Data center example: `MATCH (user:User)-[*1..5]-(asset:Asset) WHERE user.name = 'User 3' AND asset.status = 'down' RETURN DISTINCT asset`. The path has 1 to 5 relationships, unnamed and undirected; `RETURN DISTINCT` avoids duplicates of assets matched by several paths [from source] (NEO4J p.58-59).
- `[:STREET|CITY*1..2]` combines alternative types (`|`) with variable depth, for addresses of variable granularity [from source] (NEO4J p.66).
- Chained replies: `MATCH p=(email:Email {id:'6'})<-[:REPLY_TO*1..4]-(:Reply)<-[:SENT]-(replier)` binds the path to the identifier `p` and computes `length(p) - 1` as the depth; the book limits the depth to four "here" [from source] (NEO4J p.78-79).
- To count forwards, it uses `[f:FORWARD_OF*]` **with no upper bound**, at any depth, and `count(f)` [from source] (NEO4J p.80-81). That is: the book does not forbid unbounded `*`; it uses it on a small tree structure.
- Book warning about efficiency: long variable-length paths "can be relatively inefficient"; they should be restricted to the smallest possible scope, using fixed-length relationships at the ends and a short variable stretch in the middle (`[:WORKED_ON*0..2]`) [from source] (NEO4J p.136).
- Organizational hierarchy with `[:CHILD_OF*0..3]` [from source] (NEO4J p.144).
- [extrapolation] "Unbounded `*` brings down the JVM with OutOfMemoryError" is **not** in the book. It is a plausible risk in dense graphs and stays as a general good practice, labeled.

## 2. Shortest path
- `shortestPath` appears in two queries: `MATCH p=shortestPath((first)-[*..4]-(second)) RETURN length(p) AS distance` (test of the social network example, which expects distance 4) [from source] (NEO4J p.106). In the server extension the same idea with the syntax `shortestPath(first-[*..4]-second)` [from source] (NEO4J p.97).
- The book does not say that `shortestPath` uses BFS, nor does it present `allShortestPaths`.
- **Weighted** shortest path: in the Global Post case the middle part of the route is chosen in Cypher by summing costs with `reduce` and ordering; in the Traversal Framework version `GraphAlgoFactory.dijkstra` from the Java algorithms library is used, not Cypher [from source] (NEO4J p.157-159, p.164).

## 3. Query composition
- `WITH` stitches subqueries together; in Global Post four subqueries form the complete route [from source] (NEO4J p.157-159).
- Predicates over paths: `all(r in relationships(upLeg) WHERE ...)`, `reduce(weight=0, r in relationships(topRoute) | weight+r.cost)`, `nodes(...)`, `tail(...)` [from source] (NEO4J p.157-158).
- `UNION` joins queries with projections of the same columns and removes duplicates; `UNION ALL` keeps duplicates [from source] (NEO4J p.144-145).
- Aggregations: `count`, `collect`, `min(length(p))`; `LIMIT {resultLimit}` appears as a parameter [from source] (NEO4J p.135-136).
- `WITH split(line.locations,";") ... UNWIND locations AS location` expands lists during import [from source] (NEO4J p.119).

## 4. The book's recommendation pattern (the real one)
- The book has no "FOAF" query. The closest recommendation pattern is Talent.net's: people who share interests, counting interests in common as `score` (see `casos-reais-recomendacoes-rbac-e-logistica.md`) [from source] (NEO4J p.132).
- The v1 example `(eu)-[:AMIGO_DE]->(amigo)-[:AMIGO_DE]->(candidato)` with `count(amigo)` is an [extrapolation] consistent with the book's reasoning about friends-of-friends, not a query from the book.
