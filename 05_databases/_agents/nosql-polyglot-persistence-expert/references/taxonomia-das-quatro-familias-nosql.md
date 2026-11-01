# NoSQL database taxonomies: three classes in STRAUCH, four quadrants in NEO4J-GDB

Convention: `(SIGLA p.N)` = PDF page (see INDEX). v1 attributed to STRAUCH "four families" and graph chapters on pages 68 to 78: **wrong**. STRAUCH excludes graphs.

## 1. What STRAUCH classifies (2010-2011)
- The paper studies **key/value, document databases and column-oriented ones**; graph databases are left out, with resources in the appendix `[from source]` (STRAUCH p.5, 33).
- Taxonomies cited: Yen (key-value cache, key-value store, eventually consistent, ordered, "data-structures server" with Redis, tuple store, object, document, wide columnar) (p.27-28); North (p.28-29); Cattell (key-value, documents, *extensible record stores*) (p.29); Scofield/Popescu, table of performance/scale/flexibility/complexity/functionality per class (p.29-30); Ellis, who compares scalability, data model and API, and **persistence design** (Cassandra: Memtable/SSTable; CouchDB: append-only B-tree; MongoDB: B-tree; Redis: memory with background snapshots; Scalaris: memory only) (p.30-32); Hamilton: *features-first, scale-first, simple structure, purpose-optimized*, noting that the same database may appear in different classes (p.33).
- Ellis (cited): in-memory databases are very fast (Redis above 100,000 operations per second on one machine), but limited by RAM and with a risk of data loss between flushes (p.32).
- The paper's products are classified by data structure, following Yen, North and Cattell (p.33). The same text treats Cassandra as a key/value store influenced by Dynamo (p.19) and later among the column-oriented ones (p.108, 118).

## 2. Four quadrants in NEO4J-GDB (2015)
- Appendix A divides the NoSQL space into **four quadrants**: documents, key-value, column family and graphs (p.214); documents, key-value and columns are called **aggregate stores** because they persist self-contained records, in the DDD sense of *aggregate* (p.222-223). Aggregate stores do not handle highly connected data well (p.223).
- **Documents** (p.214-217): store and retrieve documents like an electronic filing cabinet; depend on indexes to access by attribute; most require planning the sharding; transactionality historically at the single-record level; without multi-key transactions, compensation is left to the application; some (CouchDB) bet on multi-master replication with optimistic control `[DATED in part]`.
- **Key-value** (p.217-219): the ancestor is Dynamo; they work as large distributed hashmaps with opaque values; replica formula **R = 2F + 1** to tolerate F failures (p.217); consistent hashing remaps only part of the keys (p.218); opacity forces reading the whole value to extract a sub-element, and richer queries usually use MapReduce (p.219).
- **Column family** (p.220-222): modeled on Bigtable, a sparse table with arbitrary columns; uses Cassandra terminology (column, super column, column family); they are aggregate stores without joins (p.222).
- **Graphs** (p.223-225): online database with CRUD that exposes a graph model; storage (native or not) and processing properties; **property graph**: nodes with properties and labels, named, directed relationships, always with a start and an end, also with properties (p.224); other models: hypergraphs and RDF triples (p.225).

## 3. Graphs: index-free adjacency
- *Index-free adjacency*: each node keeps direct references to its adjacent nodes; the "native" processing database uses this; the book's broad definition admits as a graph any database that exposes this model `[from source]` (NEO4J-GDB p.23, 167-168).
- Cost: with global indexes, a traversal costs ~O(log n) per hop; with index-free adjacency, traversing a relationship is O(1) (in Neo4j); query time depends on the portion of the graph traversed, not on its total size (p.168-169). The book also records the trade-off: it helps traversals, but queries without traversal can become hard or memory-expensive (p.24).
- Uses described: social, recommendations, geo, master data management, network and data center management, authorization and access control (p.124-129). Fraud detection appears only as an occasional example (NEO4J-GDB p.36, 42: atypical purchase patterns; p.206-207), **not** as one of the use cases listed in p.124-129; "knowledge graphs" and GBAC are not covered (`[extrapolation]`).

## 4. Key-value, documents and columns in STRAUCH, in brief
- Key-value: Dynamo (p.56-65), Voldemort (p.66-71), Tokyo Cabinet/Tyrant, **Redis** ("data-structures server", memory as the limit) and memcached/MemcacheDB, Scalaris (p.71-72). Dynamo offers only `get` and `put`; opaque key and value, key hashed by MD5 (p.58-59).
- Documents: CouchDB (p.73-80) and MongoDB (p.80-107).
- Columns: Bigtable, Hypertable, HBase and Cassandra (p.108-124).

## 5. What is not covered
That the key-value engine "never inspects" the value, except Redis, as a general rule (NEO4J-GDB p.219 says that in practice there is overlap, citing Riak); "Couchbase, Riak, Memcached, Neptune, Cloud Bigtable" as canonical examples of each family with a page; use cases and "microsecond" latencies for key-value.
