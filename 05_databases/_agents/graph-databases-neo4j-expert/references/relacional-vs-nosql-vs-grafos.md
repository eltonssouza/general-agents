# Relational vs. aggregate NoSQL vs. graphs

Source: NEO4J ch. 2 and Appendix A. Pages = **PDF** (printed = N − 18).

## 1. Relational databases "have no relationships"
- In relational vocabulary, relationships exist only at modeling time, as a means of joining tables; they do not distinguish semantics or weight [from source] (NEO4J p.29).
- The book acknowledges that relational databases were built for paper forms and tabular structures, and that they do this very well [from source] (NEO4J p.29).
- As data complexity grows, the relational model becomes loaded with join tables, sparse rows and null checks; more connectivity means more joins [from source] (NEO4J p.29).
- Points listed: join tables mix business data with foreign key metadata; FK constraints require effort; nullable columns require checking in code; finding out what a customer bought requires several expensive joins [from source] (NEO4J p.30).
- Reciprocal queries ("which customers bought this product?") are more expensive; an index helps, but recursive queries get more expensive with depth [from source] (NEO4J p.30-31).
- Examples 2-1 to 2-3 (SQL): "Bob's friends" is cheap because it filters rows; the reciprocal scans the whole `PersonFriend` table; friends-of-friends requires recursive joins. Oracle has `CONNECT BY`, which simplifies the syntax, not the computational complexity [from source] (NEO4J p.31-32).
- Queries of four, five or six degrees "deteriorate significantly" due to the time and space complexity of recursive joins [from source] (NEO4J p.32).
- The schema is at once rigid and brittle; migration requires care [from source] (NEO4J p.32).

## 2. Aggregate NoSQL has no relationships either
- Key-value, document and columnar stores hold sets of disconnected documents/values/columns [from source] (NEO4J p.33).
- The usual strategy is to embed the identifier of one aggregate in another (foreign keys in effect), which forces joining aggregates in the application and becomes prohibitive; the app must maintain consistent references or it will accumulate dangling references [from source] (NEO4J p.33-34).
- Riak: *link walking* via map-reduce, relatively high-latency, serves simple programming and not general graph algorithms [from source] (NEO4J p.34).
- Without reverse pointers, questions like "who bought this product" require exporting the set (e.g., Hadoop) or inserting reverse references retroactively [from source] (NEO4J p.34).
- Aggregate stores do not maintain the consistency of connected data nor do they have IFA [from source] (NEO4J p.34).
- O notation: the book explains O(1), O(n), O(log n) and O(m log n); scanning everything is O(n) [from source] (NEO4J p.35-36).
- Adding a reverse friendship property (denormalization) costs write latency and disk, and the traversal remains expensive because it requires an index lookup at each hop [from source] (NEO4J p.36).

## 3. Graphs embrace relationships
- In the graph world "connected data is stored as connected data" [from source] (NEO4J p.36-37).
- A domain with variable structure and dense connectivity resists a single schema; the graph grows with new nodes and relationships without migrating data (example with `LOVES`, `COLLEAGUE_OF`, `BOSS_OF`, `MARRIED_TO`, `DISLIKES`) [from source] (NEO4J p.37-38).
- Patterns that are hard in SQL and laborious in aggregate stores: the example "ice cream flavors liked by people who like espresso, dislike Brussels sprouts and live in a neighborhood" [from source] (NEO4J p.40-42).
- For complex, variable-structure, densely connected data, the book concludes that the graph database is the best technology [from source] (NEO4J p.42).

## 4. Where relational and aggregate stores remain adequate
- They have a "good technological pedigree" for what they do well and fail on connected data when going beyond shallow traversals [from source] (NEO4J p.39).
- Set operations of modest size go well in both [from source] (NEO4J p.39).

## 5. Appendix A: ACID vs BASE and quadrants
See `nosql-apendice-e-modelos-de-grafo.md`.

## 6. What the book does NOT say
- It provides no comparative table "full ACID vs BASE" by product category; it discusses ACID vs BASE in Appendix A (NEO4J p.212-214). The v1 table was [inference] and was removed.
- It does not cite `WITH RECURSIVE`/recursive CTEs; it mentions "recursive joins" and `CONNECT BY`. Citing a recursive CTE is [extrapolation].
- It does not say the graph is "better" for ERP or accounting nor that NoSQL is "better for massive writes"; the book's point is connectivity.
