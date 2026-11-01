# Graph modeling guidelines and patterns

Source: NEO4J chs. 3-4. Pages = **PDF** (printed = N − 18).

## 1. Starting point: questions and user stories
- Modeling is abstraction motivated by a need; there is no "natural" representation, only selections useful for a goal [from source] (NEO4J p.43).
- Describe the model in terms of the application's needs; a user story (`AS A`/`I WANT`/`SO THAT`) reveals entities and relationships and the question of the query [from source] (NEO4J p.84).
- "Design for queryability" in five steps: user goals, rewrite them as questions, identify entities and relationships, translate them into Cypher paths, express the questions as patterns [from source] (NEO4J p.81).
- Common nouns become labels; verbs with an object become relationship names; proper nouns become instances (nodes with properties) [from source] (NEO4J p.81).
- Informal test: read the graph as sentences starting from a node and check that it makes sense [from source] (NEO4J p.58).

## 2. Nodes for things, relationships for structure
Guidelines on p.85 [from source] (NEO4J p.85):
- nodes for entities; relationships for connections and semantic context; direction to clarify the semantics;
- node properties for attributes and metadata (timestamps, versions); relationship properties for strength, weight, quality and metadata;
- bidirectional: queries ignore the direction, instead of two relationships.
- If it is tempting to model an entity (e-mail, review) as a relationship, you must make sure it will never relate to more than two entities; if that changes, refactoring is a "breaking change" [from source] (NEO4J p.85).
- General antipattern: do not encode entities in relationships; "verbing" (turning a noun into a verb, "emailed") hides the entity [from source] (NEO4J p.81-82).

## 3. Fine-grained vs. generic relationships
- Contrast: `DELIVERY_ADDRESS`/`HOME_ADDRESS` versus `ADDRESS {type:'delivery'}`/`ADDRESS {type:'home'}` [from source] (NEO4J p.85).
- "Relationships are the real road into the graph": differentiating by name eliminates large portions of the graph in the traversal; deciding by property costs extra I/O on the first read, because properties live in another storage file (afterwards, they are cached) [from source] (NEO4J p.85).
- Use fine granularity when the set of names is closed; weights (for weighted shortest path) rarely form a closed set and go as a property [from source] (NEO4J p.86).
- For "all addresses", the book offers two options: list the types in the query (`HOME_ADDRESS|WORK_ADDRESS|DELIVERY_ADDRESS`) or create a generic `ADDRESS` in addition to the specific ones [from source] (NEO4J p.86).
- In TeleGraph, fine-grained relationships were almost twice as fast as a single type with properties [from source] (NEO4J p.143).

## 4. Facts as nodes
- When two or more entities interact over a period, a "fact" emerges, represented by an intermediate node with links to each entity; timestamps on that node mark start and end [from source] (NEO4J p.86).
- Book examples: employment (`Job` between `Person`, `Company` and `Role`), performance (`Performance`), sending an e-mail (`Email` with `TO` and `CC`) and review (`Review`) [from source] (NEO4J p.86-89).
- The e-mail case (the first iteration loses the e-mail; the second creates `Email` nodes with `SENT`, `TO`, `CC`, `BCC`) is detailed in `casos-e-antipadroes.md` [from source] (NEO4J p.70-76).

## 5. Complex value types as nodes
- Values without identity whose equivalence is by value only (money, address, SKU); those with multiple fields, such as an address, can become separate nodes [from source] (NEO4J p.89).
- Example: `MATCH (:Order {orderid:13567})-[:DELIVERY_ADDRESS]->(address:Address) RETURN address.first_line, address.zipcode` [from source] (NEO4J p.89).
- The book does **not** address shared city/neighborhood, nor does it say that a single string is an antipattern with regex search; that is [inference].

## 6. Iterative evolution
- Developing the model feature by feature and story by story identifies the relationships the application uses [from source] (NEO4J p.92).
- New facts and compositions become new nodes and relationships; optimizing for performance typically means adding a direct relationship between nodes previously linked by intermediaries, preserving the high-fidelity model [from source] (NEO4J p.92).
- Coexistence example: `DELIVERY_ADDRESS`, `BILLING_ADDRESS` and `ADDRESS` serving different needs [from source] (NEO4J p.93).
- Adding new relationship types does not affect existing queries; changing properties or using existing types requires running a representative set of queries [from source] (NEO4J p.76).
- It is bad practice to merge data elements at write time to gain read efficiency; by modeling according to the questions, a faithful model emerges and the database performs [from source] (NEO4J p.82).
- Versioning inside the graph is possible, but it "leaks" into all queries [from source] (NEO4J p.92).
