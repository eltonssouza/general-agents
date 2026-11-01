# MongoDB: embedding × referencing, simulated transactions and comments in "buckets"

Convention: `(MONGO-PAT p.N)` = PDF page (printed = PDF − 14). Source: Copeland (2013), MongoDB 2.x, `[DATED]` as to features (no multi-document transactions, no `$lookup`, the old pymongo `insert/update` API). v1 cited "p.10-60" and attributed to Copeland "Subset Pattern", "Extended Reference Pattern" and "< 100 / > 100" limits: **none of this is in the book**.

## 1. Embed or reference (ch. 1, p.17-29)
Context: in relational, normalization avoids redundancy, but reading requires a JOIN, which costs **random seeks** on rotating disk (the seek dominates >99% of the time to read a row) and, with several machines, becomes a distributed join, "complex and generally slow" (p.20-21). Denormalizing reintroduces redundancy and complexity (p.21-22). In MongoDB there is no normalized "garden path"; the answer is "it depends" (p.22).

**In favor of embedding**
- **Locality**: documents are contiguous on disk; at most one seek brings everything. With no JOIN in MongoDB, referencing costs two trips to the database (p.23). If the app reads the contact with all its phone numbers, "almost certainly" embed (p.23).
- **Atomicity and isolation**: there are no multi-document transactions; deleting with two `remove` calls may leave orphaned numbers or readers seeing an incomplete state; with the embedded schema, one operation does it. MongoDB "skipped" joins and distributed transactions in order to do automatic sharding with better scaling. Single-document updates give the effect of the most conservative isolation level, without the cost (p.23-24).

**In favor of referencing**
- **Query flexibility**: if the access pattern is known and unique, embedding works; if the data is queried in various ways (e.g. "all comments by author X", ordering, `limit`/`skip`), a normalized collection is better (p.25-26).
- **High or unpredictable arity** (hundreds or thousands of comments): a larger document uses more RAM and makes fewer documents fit in cache (more page faults and random I/O); growing documents must be copied to larger spaces, which slows updates; and there is the 16 MB limit. The text says that memory and copying problems are generally reached **before** the limit (p.26-27).
- **Many-to-many**: a join table imitates the relational model and generates "joins" in the application; embedding everything mutually forces updates in all places; the middle ground is usually best: **embed a list of `_id`s** (p.27-28).
- Chapter conclusion: the two biggest benefits of embedding are locality and per-document atomicity; costs are loss of flexibility ("pre-join") and problems with high arity; the decision depends on access patterns, with fewer fixed rules than in relational (p.28-29).

## 2. Mimicking transactions (ch. 3, p.39-47)
- For 2PC, the text explains prepare/apply and the cost of holding locks until everyone finishes; MongoDB "gave up" on multi-document transactions (p.39-40).
- **Composite documents**: embed items in the order to delete/update with a single operation (p.40-42).
- **Complex updates**: `$inc`, `$push` and filters in `update` avoid the client-side read-modify-write race; check `updatedExisting` (p.42-43).
- **Optimistic update with compensation**: a "transactions" collection with states (`new`, `commit`, `rollback`), a list of pending transactions on each account, a time window, periodic cleanup and **idempotent operations** (`retire_transaction`, rollback) (p.43-47). The author warns: take extreme care when designing a 2PC in the application; the rule of thumb is to keep atomic updates within the boundary of a single document whenever possible (p.44).
- `[DATED]`: with multi-document transactions available in current versions (MONGO-MAN-H p.3), these patterns are for when one does not want to or cannot use them `[inference]`.

## 3. Comments in MONGO-PAT: three designs (ch. 6)
The book compares (p.125): **one document per comment** (maximum flexibility, no artificial limit on quantity; displays chronologically or as a tree; p.125-128), **all embedded in the parent** (best display performance, limited by document size; p.128-131) and **hybrid** (p.131-133).
- The **hybrid** stores comments in "buckets" of about 100 per document (`page`, `count`, `comments` array), with `$push` on the last page and `$inc` of `count`, creation of a new page when full, and a compound index on `node_id` and `page` (p.131-132). Pagination walks the pages subtracting `count` (p.132-133).
- Sharding (p.133-134): `node_id` must be part of the key; for one comment per document, `node_id` + `slug` (or `full_slug`); in the hybrid, `node_id` + `page`, to prevent a discussion from becoming a giant, indivisible *chunk*.
- "Bucket pattern" and "Subset pattern" as **pattern names** are later terminology (`[extrapolation]`); the book uses the word "buckets" only for the hybrid design (p.131); "subset" appears only in another context (subset of shards, p.62). Keeping only the 5 most recent items in the parent is a reasonable technique `[extrapolation]`, but it is not "from the book".

## 4. Summary heuristics `[inference]`
Embed when: 1:1 or 1:few relationship of bounded arity, read together, and updates that need to be atomic. Reference when: high/unbounded arity, queries by child, many-to-many, independent updates. Hybrid (buckets/pages) when the quantity is large but access is paginated. Numeric thresholds (e.g. 100 items) do **not** come from the book, except "about 100" per *bucket* in the comments example (p.131).
