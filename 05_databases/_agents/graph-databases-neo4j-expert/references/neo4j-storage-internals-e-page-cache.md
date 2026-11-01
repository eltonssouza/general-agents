# Neo4j native storage internals and page cache

Source: NEO4J ch. 6. Pages = **PDF** (printed = N − 18). **Version**: the book itself warns that the record layout is from Neo4j 2.2 and that other versions may have different sizes [from source] (NEO4J p.171). Everything here is [DATED] relative to current Neo4j.

## 1. Storage files
- The graph data lives in several storage files (nodes, relationships, labels, properties); separating the graph structure from property data makes traversals easier, even though the user's view and the on-disk records are structurally different [from source] (NEO4J p.171).
- Nodes live in `neostore.nodestore.db`; relationships in `neostore.relationshipstore.db` [from source] (NEO4J p.172).
- Both are *fixed-size record stores*, which makes it possible to compute a record's position from its ID (ID × record size), at O(1) cost instead of an O(log n) lookup [from source] (NEO4J p.172, p.174).

## 2. Sizes: the book's own inconsistency
- Figure 6-4 shows the node with **15 bytes** (fields inUse 1, nextRelId 4, nextPropId 4, labels 5, extra 1 byte) and the relationship with **34 bytes** (fields inUse, firstNode, secondNode, relationshipType, firstPrevRelId, firstNextRelId, secondPrevRelId, secondNextRelId, nextPropId, firstInChainMarker) [from source] (NEO4J p.171; the field names are in the figure image and were read from the rendered page, not from the extracted text).
- The text of the next page says each node record is **nine bytes** and gives the example of node 100 starting at byte 900 [from source] (NEO4J p.172). This contradicts the figure (15 bytes); the text's breakdown (1 + 4 + 4 + 5 + 1) adds up to 15. When answering, cite the discrepancy and prefer 15/34 (figure, breakdown and the 2.2 documentation) with the version caveat [inference].
- The book attributes Neo4j's historical choice of a "sweet spot" of capacity (graphs up to the 95th percentile of use cases) to the extensive use of fixed-size records and pointers [from source] (NEO4J p.185).

## 3. Node and relationship
- Node record: in-use flag (`in-use`), ID of the first relationship, ID of the first property, five bytes of labels (may be inline when few) and an `extra` byte for flags (one marks dense nodes) [from source] (NEO4J p.172).
- The node is "lightweight": only pointers to lists of relationships, labels and properties [from source] (NEO4J p.172).
- Relationship record: IDs of the start and end nodes, pointer to the type, pointers to the previous and next relationship of each of the two nodes, and a first-in-chain marker [from source] (NEO4J p.172).
- Each relationship "belongs" to two nodes and takes part in **two doubly linked lists** (the start node's and the end node's); the double linking allows iterating in both directions and inserting/removing efficiently [from source] (NEO4J p.173). The book does **not** say the list is "circular".
- Node and relationship properties form a **singly** linked list [from source] (NEO4J p.172-174).

## 4. How a traversal uses this
1. From the node record, the offset of the first relationship is computed (ID × size).
2. In the relationship record, the ID of the second node is read and multiplied by the node record size.
- Restricting by type adds a lookup in the relationship type file; restricting by label queries the label file [from source] (NEO4J p.174).
- Traversals are "pointer chasing" and can be done at high speed [from source] (NEO4J p.174).

## 5. Properties
- File `neostore.propertystore.db`; each record has four property blocks and the ID of the next property; each property takes from one to four blocks, so a record holds at most four properties [from source] (NEO4J p.174).
- The property name lives in the index file (`neostore.propertystore.db.index`); large values go to dynamic stores: strings in `neostore.propertystore.db.strings` and arrays in `neostore.propertystore.db.arrays` [from source] (NEO4J p.174-175).
- *Inlining*: data that fits in the blocks (phone number, postal code) stays in the properties file, reducing I/O [from source] (NEO4J p.175).
- The property index allows sharing the name record among properties with the same name [from source] (NEO4J p.175).
- That is why reading relationship properties costs extra I/O the first time (separate file) [from source] (NEO4J p.85).

## 6. Cache
- From Neo4j 2.2 an **off-heap** cache is used; Neo4j uses an "LRU-K" *page cache* tuned to pages: it divides each file into regions, keeps a fixed number of regions per file and evicts with an LFU policy adjusted by page popularity [from source] (NEO4J p.175-176).
- Spinning disks have millisecond seeks; SSDs are much better, but still higher-latency than memory [from source] (NEO4J p.175).
- The ideal sizing path: map the entire files in the page cache, with a modest heap (see `arquitetura-testes-capacity-e-importacao.md`) [from source] (NEO4J p.115).
- The book does **not** claim that the off-heap cache "eliminates GC pauses" nor does it mention *stop-the-world*; what it says about GC is in the embedded and server mode sections (see `arquitetura-testes-capacity-e-importacao.md`). Deduction: an off-heap cache avoids pressuring the collector [inference].

## 7. What the book does NOT say
- It gives no byte formula for "Offset on disk", only ID × size.
- It does not cite `dbms.memory.*`; the current configuration names are [extrapolation] and change per version.
