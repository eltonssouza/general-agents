# Temporal modeling: time trees, linked lists and intervals

Source: NEO4J ch. 4 ("Time" section) and the Global Post case (ch. 5). Pages = **PDF** (printed = N − 18). The book calls the pattern a *timeline tree*; "Time Tree" is the name used in the v1 package and in later texts.

## 1. Two time techniques
The book describes two techniques: timeline trees and linked lists; in some solutions it is worth combining them [from source] (NEO4J p.90).

## 2. Timeline tree
- Useful when you need to find all events in a period; each year has its month nodes and each month its day nodes; the example uses broadcast dates of episodes of a TV show (Figure 4-6) [from source] (NEO4J p.90-91).
- Nodes are inserted only when needed; assuming the root node is indexed (or reachable by traversal), a chained `MERGE` ensures year, month, day and the event: `MATCH (timeline:Timeline {name:{timelineName}})` followed by `MERGE` of `Episode`, `Year`, `Month`, `Day` and `BROADCAST_ON` [from source] (NEO4J p.91).
- The range query (start date inclusive, end exclusive) uses a long `WHERE` that compares year, month and day; the book calls it "somewhat verbose" [from source] (NEO4J p.91).
- The book's hierarchy: Year, Month, Day. An `Hora` (hour) level does **not** appear; it is [extrapolation].
- The labels and relationships in the example are `Timeline`, `YEAR`, `MONTH`, `DAY` and `BROADCAST_ON`; the v1 names `TEM_MES`, `OCORREU_EM` were invented.

## 3. Linked lists of events
- Many events have a temporal relationship with the previous and the next; `NEXT` and/or `PREVIOUS` create linked lists that allow very fast traversal of time-ordered events [from source] (NEO4J p.91-92).
- A doubly linked list is "a treat": in practice relationships are traversed in constant time in both directions [from source] (NEO4J p.92).
- Book examples: Ruth's message timeline with `CURRENT` and `PREVIOUS` (NEO4J p.21); order history with `MOST_RECENT` and `PREVIOUS`, which allows finding the most recent order and going back in time (NEO4J p.40); an author's publications, with `WROTE` and `PREV`, where reading the latest and inserting a new one are O(1) operations (NEO4J p.186).
- The relationship names `PROXIMO`, `PRIMEIRO_EVENTO`, `ULTIMO_EVENTO` (v1) are not from the book; use `NEXT`/`PREVIOUS` or the domain vocabulary.

## 4. Facts with start and end
- Timestamps on intermediate nodes ("facts") represent the start and end of a relationship in time, such as `start_date` on the employment `Job` node [from source] (NEO4J p.86-87).

## 5. Validity intervals on relationships (Global Post)
- Routes change throughout the year; the `CONNECTED_TO` and `DELIVERY_ROUTE` relationships have `start_date` and `end_date` properties, and the query only considers those that cover the requested period [from source] (NEO4J p.153-156).
- In Cypher: `all(r in relationships(upLeg) WHERE r.start_date <= {intervalStart} AND r.end_date >= {intervalEnd})` [from source] (NEO4J p.157).
- In the Traversal Framework version, a `PathExpander` returns only the relationships whose interval contains the period, with the interval passed as *branch state* [from source] (NEO4J p.160-161).
- For a given period, the lower part of the network is a simple tree (at most one route between base and area/segment), and the upper part is more interconnected [from source] (NEO4J p.151).

## 6. Versioning
Versioning the graph (recovering the state at a point in time) is not a first-class feature in most graph databases; it is possible within the model by timestamping and archiving nodes and relationships, but this scheme leaks into the queries [from source] (NEO4J p.92). Kernel transaction event handlers can mark logical deletion or archive "in time" [from source] (NEO4J p.177).

## 7. What the book does NOT say
- It does not recommend a time tree as a supernode mitigation (see `supernos-anti-padroes-e-mitigacoes.md`).
- It does not present the three-level `MERGE` as "idempotent" in a formal sense; it treats `MERGE` as a guarantee of the pattern's presence.
- It does not cover native temporal types or `datetime()` (current Neo4j): [extrapolation].
