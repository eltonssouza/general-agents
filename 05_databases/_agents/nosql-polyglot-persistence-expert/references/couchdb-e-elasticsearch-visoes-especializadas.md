# CouchDB (COUCH, STRAUCH) and Elasticsearch (ELAST: landing page only)

Convention: `(SIGLA p.N)` = PDF page (see INDEX). COUCH is the technical text "1.1 Technical Overview" of the documentation ("stable" version, no number); ELAST is the Reference **landing page** (9.0+), with no technical content on inverted index, shards or NRT.

## 1. CouchDB
**Storage and API** `[from source]`
- A server hosts named databases that store documents; each document has a unique name; there is a **RESTful HTTP API** to read and update (COUCH p.1). Documents have fields (values of varied types, with no fixed limit on text size or elements), attachments and metadata maintained by the database (COUCH p.1). In STRAUCH: reading by GET, creating/updating by PUT, deleting by DELETE; the update requires the **revision number** that was read (STRAUCH p.77). The field name `_rev`, the HTTP 409 code and `/_replicate` **do not appear** in the sources (`[extrapolation]`).
- **Optimistic, lock-free** update: the client loads, changes and saves; if another client saved first, the save fails with an **edit conflict error**, and the client reopens the current version and reapplies (COUCH p.1). Updates to a document are all-or-nothing (p.1).
- **ACID per document**: file layout and commit protocol; never overwrites data already written ("crash-only": the server can simply be terminated); serialized updates; readers are not blocked; reads use **MVCC** with a consistent snapshot from the start to the end of the read (COUCH p.1). Documents are indexed in **B-trees** by DocID and by Sequence ID; updates always go to the end of the file (append-only) (COUCH p.2). Two-step commit (data and indexes with synchronous flush; header written in two identical blocks) (COUCH p.2). **Compaction** copies live data to a new file, with the database online (COUCH p.2).
- STRAUCH: documents are **not nestable** (note by Ippolito), 128-bit id, 32-bit revision by hash with no collision handling (p.74); Lotus Notes is the origin; Erlang (p.73); consistency "can be questioned" in a distributed scenario (p.78). `[DATED]`: check the current documentation for these details.

**Views (queries)** (COUCH p.2-4; STRAUCH p.75-76): views are JavaScript `map` (and `reduce`) functions defined in **design documents** (COUCH p.3-4; STRAUCH p.75), computed on demand and maintained incrementally by indexes, updated based on the Sequence ID; they do not alter the documents and replicate as normal documents (COUCH p.3). Documents with an open conflict are left out of the views (STRAUCH p.76; COUCH p.6, only the winner appears).

**Security and validation** (COUCH p.4-5): administrator accounts; JavaScript update-validation functions, for security and for data, also applied to replicated updates.

**Replication** (COUCH p.5-6; STRAUCH p.76-77)
- **Peer-based** distributed system: allows accessing and updating the same data while disconnected and **replicating bidirectionally later**; documents and designs replicate, taking entire applications to notebooks or remote offices (COUCH p.5).
- Replication is **incremental** (only documents changed since the last one); if it fails, it restarts from the last *checkpoint*; there are **partial** replicas by filter function (COUCH p.6). By default, without an extension, all data goes to all nodes; sharding only with filters or external frameworks (STRAUCH p.77).
- **Conflicts** are a common state, not an exception: any number of conflicting versions can coexist; each instance deterministically picks the same "winner"; the losers remain accessible until removed and replicate normally; resolution can be manual or automatic (COUCH p.6). `[inference]`: "multi-master" is the natural reading; the term is **not** used in COUCH (NEO4J-GDB p.217 uses "multimaster" for CouchDB).

**Implementation**: Erlang/OTP, lock-free concurrency, "shared nothing" clustering (COUCH p.7).

## 2. Elasticsearch (ELAST, p.1-3)
What the source says: "distributed search and analytics engine, scalable data store and vector database" built on **Apache Lucene**, optimized for speed and relevance, to search, index, store and analyze data "in near real time" (p.1). Lists topics: ingestion (Connectors, Web crawler, Data streams, Ingest pipelines), Mapping, data management (Downsampling, Snapshot and restore), query languages (**Query DSL**, **ES|QL**, **EQL**, SQL), aggregations, geospatial analysis, Machine Learning, Alerting, REST APIs, clients, Painless (p.1-3). It is the engine of the Elastic Stack (p.2).
**Not covered**: inverted index (term → documents), analyzers/tokenizers, primary shards and replicas, `translog`, 1 s `refresh`, TF-IDF/BM25, "milliseconds" (v1 cited ELAST p.1-4 for all of this). If the user needs the internal mechanism, answer as `[extrapolation]` and refer to the current official documentation.

## 3. Use
CouchDB: a good study of MVCC, append-only tree, incremental views and replication with conflicts as a normal state. Elasticsearch: treated here only as a search/analytics engine on Lucene; the role of "companion search database" for queries the primary store does not support appears as a pattern in STRAUCH p.51 ("companion" SQL or text database) `[from source]`, but without citing Elasticsearch.
