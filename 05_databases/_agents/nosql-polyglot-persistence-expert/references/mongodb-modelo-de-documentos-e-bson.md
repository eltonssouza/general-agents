# MongoDB: document model, BSON, polymorphic schemas and GridFS

Convention: `(SIGLA p.N)` = PDF page (see INDEX). MONGO-PAT: printed = PDF − 14. Different eras: MONGO-PAT (2013, MongoDB 2.x), STRAUCH (2010, MongoDB 1.6/1.7) and MONGO-MAN-H (docs 8.3, 2026). **MONGO-MAN-I is the same page as MONGO-MAN-H in pt-BR**, without the BSON/ObjectId "Introduction" that v1 attributed to it.

## 1. Document, collection and flexibility
- In MongoDB, a record is a document (field-value pairs) similar to JSON objects; values can be other documents, arrays and arrays of documents; documents live in **collections**, which impose no rigid schema; embedded documents and arrays reduce the need for joins; dynamic schemas support polymorphism `[from source]` (MONGO-MAN-H p.2-3; in Portuguese: MONGO-MAN-I p.9-15). In version 8.3, the page's example uses `ObjectId("...")` as `_id` (MONGO-MAN-H p.2).
- MONGO-PAT (2013): documents are modeled in JSON format but stored as **BSON**; a document is a dictionary of key-value pairs whose values can be primitive JSON types, BSON types (datetime, ObjectId, UUID, regex), arrays, objects or null `[from source]` (MONGO-PAT p.22). MongoDB allows storing an array where 1NF would require one value per cell, obtaining denormalization benefits without the redundancy; hence schema design "depends" (p.22).
- Documents are stored **contiguously** on disk, which is why embedding gives locality (MONGO-PAT p.23).
- Appropriate types save space and allow range queries: the 28-byte log date text fits in 8 bytes in the UTC timestamp type; numbers as strings cost more and query worse (MONGO-PAT p.52). The `ObjectId` **embeds the creation time** (MONGO-PAT p.53). The internal 12-byte structure (4+5+3) is **not** described in the sources `[extrapolation]`.

## 2. Polymorphic schemas (MONGO-PAT ch. 2, p.31-37)
- "Schemaless" means no structure is imposed; in a well-designed application, the collection usually contains documents of the same or similar structure: a **polymorphic schema** (p.31).
- Cases: mirroring OO inheritance (CMS with wiki pages and photos in one `nodes` collection, simple URL query; in relational, a single table wastes space, a table per concrete class requires several queries, and polymorphic inheritance requires joins) (p.32-34); **schema evolution** without blocking `ALTER TABLE`, with gradual background migration (p.34-35); semi-structured data, with a `properties` subdocument or an indexable array of property-value pairs (p.36-37).
- Drawback: without a schema at the collection level, field names and types are stored in each document; long names with small values increase storage; mitigation: short names (harder to inspect) or an ODM (MongoEngine, MongoKit, Ming) (p.35-36).

## 3. Size limit
- Documents have a hard limit of **16 MB** (at the time of the book: "currently"), and the text warns that memory and document-copying problems are likely before the limit is reached (MONGO-PAT p.26-27, 117).
- `[DATED]`: STRAUCH (MongoDB 1.6) says BSON objects are limited to **4 MB** (STRAUCH p.106). Neither MONGO-MAN-H nor MONGO-MAN-I cites a limit.

## 4. GridFS
- Convention implemented in the client for blobs larger than 16 MB: each blob is a metadata document (name, md5, MIME) plus documents with the content in **256 kB** *chunks*; two collections, one for metadata and one for *chunks* (`cms.assets.files` and `cms.assets.chunks` in the example) (MONGO-PAT p.117). v1 said 255 KB and cited MONGO_MAN_I, which is incorrect.
- STRAUCH describes GridFS (4 MB BSON limit in 1.6) and when to consider it (many files that change; not for many small, static files) (STRAUCH p.106).
- On shards: a note in MONGO-PAT that sharding by `_id` keeps queries routable (p.125).

## 5. Transactions: contrast of eras `[DATED]`
- MONGO-PAT (2013): MongoDB was designed **without multi-document transactions**; updates to a single document are atomic and isolated; this motivated the chapter "Mimicking Transactional Behavior" (p.24, 39-47). STRAUCH (2010): atomicity exists only for update/delete with `$atomic` and modifier operations (p.89-91).
- MONGO-MAN-H (8.3): supports **ACID multi-document transactions**, including distributed across sharded clusters (p.3). Hence "absence of multi-document transactions" is `[DATED]`, but MONGO-PAT's modeling patterns remain useful as cost/benefit reasoning `[inference]`.

## 6. What the sources do not say
Decimal128, Binary for UUID, length prefixes that "speed up scanning", the byte structure of ObjectId, random initial counter, `getTimestamp()`, `_id` generation "by the driver" as a distributed advantage, `WiredTiger`/buffer pool (v1 attributed this to MONGO_PAT p.15-18; the book talks about RAM and page faults of the MongoDB of the time, p.26).
