# Appendix A of the book: NoSQL overview and graph models

Source: NEO4J Appendix A (printed 193-210; PDF 211-228). Pages = **PDF** (printed = N − 18).

## 1. Why NoSQL
Volume, velocity of change and structural variety motivated NoSQL; the "join pain" stems from the data model, which builds the set of all answers before filtering [from source] (NEO4J p.211).

## 2. ACID vs BASE
- ACID: atomic, consistent, isolated, durable; it requires sophisticated locking, which can cause logical unavailability and is considered heavyweight for many cases [from source] (NEO4J p.213).
- BASE: basic availability, soft-state, eventual consistency; more optimistic, values availability [from source] (NEO4J p.213-214).
- Exception cited: RavenDB (.NET) supports ACID across aggregate stores; many graph databases keep ACID [from source] (NEO4J p.213).

## 3. NoSQL quadrants
- **Document**: hierarchical documents (JSON/XML), attribute indexes, transactionality traditionally per document, sharding generally planned by the user [from source] (NEO4J p.214-217).
- **Key-value**: descended from Amazon's Dynamo; distributed hashmaps; R = 2F + 1 replicas to tolerate F failures; consistent hashing; opaque values [from source] (NEO4J p.217-219).
- **Column families**: modeled on BigTable; Cassandra terminology (column, super column, column family); "maps of maps"; still aggregate stores and without joins [from source] (NEO4J p.220-222).
- The three are called *aggregate stores*; for complex queries, data is usually extracted to external infrastructure (MapReduce/Hadoop), which is very high-latency [from source] (NEO4J p.222-223).
- **Graphs**: definition of a graph database and the two properties (storage and engine); they traverse "millions of nodes per second" versus joining through a global index, "many orders of magnitude" slower [from source] (NEO4J p.223-224).

## 4. Graph models
- **Property graph** (nodes and relationships with properties, labels) [from source] (NEO4J p.224).
- **Hypergraph**: a hyperedge connects any number of nodes; Alice and Bob owning three vehicles would require six relationships in the property graph; the two models are isomorphic; hypergraphs need fewer primitives to qualify one relationship with another ("meta-intent") [from source] (NEO4J p.225-226).
- **Triples (RDF)**: subject-predicate-object; Semantic Web; SPARQL; they are not native (no IFA); the sweet spot is analytics, not OLTP [from source] (NEO4J p.226-228).
- Graph databases can serve as the backend of an RDF/SPARQL endpoint (Blueprints SAIL) [from source] (NEO4J p.228).

## 5. What the book does NOT say
- It does not cover current multi-model or vector databases, nor the evolution of the ecosystem after 2015 [extrapolation]. `NEO_START` merely names "Embedding & Vector Indexes" and composite databases as topics (NEO4J does not address them; NEO_START p.2).
