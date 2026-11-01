# Practical cases and antipatterns (only what the sources support)

> Each item separates what the sources say (`[from source]`) from what is deduction (`[inference]`) or outside knowledge (`[extrapolation]`). Pages = PDF. Items from v1 without backing were rewritten or downgraded.

## 1. Turning autovacuum off
- **Evidence**: the manual calls it "imprudent" to disable the daemon completely, except for an extremely predictable workload (PG16 p.789); fixed schedules can let the table bloat to the point of requiring VACUUM FULL (PG16 p.789); even with `autovacuum = off` the system starts vacuums to prevent wraparound (PG16 p.702, p.792); if that fails, there are warnings 40 million transactions from the limit and **refusal of new XIDs below 3 million** (PG16 p.794). The index-only scan depends on the visibility map maintained by vacuum (PG16 p.791, p.478).
- **Remediation [from source]**: keep autovacuum and tune thresholds **per table** with storage parameters (PG16 p.797); see the formula (PG16 p.796).
- **[extrapolation]**: values such as `scale_factor = 0.05` and `cost_limit = 2000` are common-practice starting points, not from the manual.
- **Corrected in v1**: it is not true that recovery requires single-user mode (PG16 p.795).

## 2. Indexes without a plan (and index of the wrong type)
- **Evidence**: every index has a maintenance cost and an index on a **column that is updated** prevents HOT (summarizing indexes, i.e. BRIN, do not prevent it: PG16 p.2576); remove the rarely used ones (PG16 p.468); evaluate with real data, ANALYZE and EXPLAIN (PG16 p.481-482); multicolumn "with moderation" and more than three columns rarely helps (PG16 p.471); many disjoint partial indexes do **not** replace partitioning (PG16 p.476-477); hash serves only equality and is neither unique nor multicolumn (PG16 p.469, p.2565).
- **BRIN on large correlated tables** [from source]: effective with physical correlation (PG16 p.2552); combining with partitioning is `[inference]` (PG16 p.132, p.2552).
- The book *SQL Antipatterns* has a chapter "Index Shotgun" (13, "Optimize Performance"; solution "MENTOR Your Indexes"), but the supplied excerpt only carries the **title** in the table of contents (ANTI-TOC p.7); there is no content to cite. The book also states that **performance, scalability and optimization are not the focus** (ANTI-INT p.9): for index decisions use PG16 and `index_advisor.py`.

## 3. SQL Injection through concatenation
- **Evidence**: see `prevencao-a-sql-injection-e-parametrizacao.md`. Summary [from source]: any part built by concatenation is potentially vulnerable (ANTI-INJ p.12); parameters are a very strong defense, not a universal one (ANTI-INJ p.9-11); stored procedures and frameworks do not immunize (ANTI-INJ p.11-12); injection can be indirect (ANTI-INJ p.14).
- **Remediation**: values through parameters; identifiers through DBMS/driver quoting (PG16 p.984-985, p.1364-1365); allow-list is `[extrapolation]`.

## 3b. Synchronous replication with a single standby (commits that never complete)
- **Evidence** [from source]: with `synchronous_standby_names` and `synchronous_commit` set to `on`, `remote_apply` or `remote_write`, commits "may never complete" if a synchronous standby goes down; the transaction's locks remain held during the wait (PG16 p.825-826).
- **Remediation [from source]**: name **several candidates** (`FIRST`/`ANY` with more names than the required number) or reduce/disable the number of synchronous standbys and reload the configuration; the standby only becomes synchronous in the streaming state (PG16 p.826). See `postgresql-16-replicacao-streaming-sincrona-hot-standby-e-failover.md`.
- **[extrapolation]**: no automatic failover tool (Patroni, repmgr) is from the manual (PG16 p.827).

## 3c. Forgotten prepared transactions and `idle in transaction`
- **Evidence** [from source]: a prepared transaction holds locks, prevents VACUUM from reclaiming space and can lead to a wraparound shutdown; without an external manager, leave `max_prepared_transactions = 0` (PG16 p.1990, p.654); an open, idle transaction also prevents vacuum from removing recently dead tuples (`idle_in_transaction_session_timeout`, PG16 p.708).
- **Remediation**: resolve the prepared ones (`COMMIT PREPARED`/`ROLLBACK PREPARED` outside a transaction block; `pg_prepared_xacts` lists them; PG16 p.1695, p.2008) and terminate the long sessions (PG16 p.794-795).

## 3d. `statement_timeout` or `lock_timeout` in `postgresql.conf`
- **Evidence** [from source]: the manual **does not recommend** setting them in `postgresql.conf`, because they affect all sessions (PG16 p.707-708); prefer per role, database or session. `idle_session_timeout` requires care with poolers (PG16 p.708).

## 3e. Extended statistics to "fix" joins
- **Evidence** [from source]: `CREATE STATISTICS` is not used by the planner for the selectivity of **joins between tables** (PG16 p.1808); it applies to columns of a single table. Columns with a badly wrong `n_distinct` can be fixed with `ALTER TABLE ... SET (n_distinct = ...)` (PG16 p.1644, p.1679).

## 4. Naive trees (`parent_id`)
- **Evidence [from source]**: Adjacency List cannot query all descendants without recursion; deletion is multi-step (ANTI-TREE p.7-9); but it can be "perfectly adequate" if there are only direct parents/children (ANTI-TREE p.10); standard recursive queries exist (ANTI-TREE p.11; PG16 p.174-175).
- **Remediation**: in PostgreSQL, `WITH RECURSIVE` (PG16 p.174-177); alternative models (materialized path, nested sets, closure table) are `[extrapolation]` because the excerpt does not carry them (see `modelagem-de-arvores-e-hierarquias-sql.md`).

## 5. Assuming serializability under Read Committed or Repeatable Read
- **Evidence**: the Red Book reports that many applications assume serializable isolation and that weak isolation is the default in most databases; examples: concurrent withdrawals and the Flexcoin incident (REDBK p.28-29). In PG16, Repeatable Read does not guarantee equivalence to a serial execution and "enforcing business rules at this level probably does not work without explicit locks" (PG16 p.528-529); Serializable detects and aborts (PG16 p.529-530).
- **Remediation [from source]**: use Serializable and handle `40001` by retrying the transaction, or use explicit locks (PG16 p.530-531).

## 6. Long transactions and "idle in transaction"
- **Evidence**: strict 2PL holds locks until the end (ARCH p.80-81); under Serializable, the manual advises short transactions and avoiding "idle in transaction" connections, with `idle_in_transaction_session_timeout` (PG16 p.531); in the wraparound scenario, the manual says to terminate long open transactions (PG16 p.794).
- **[inference]**: calling external services (HTTP, e-mail) inside an open transaction prolongs locks and delays VACUUM; the sources cite neither this example nor timings.

## 7. `fsync = off` and similar
- **Evidence [from source]**: turning off `fsync` disables the write synchronization logic and, after an OS crash, can cause "arbitrarily bad corruption"; **asynchronous commit** loses only the last transactions, without corruption, and gives "most of the gain" (PG16 p.900, p.899). Turning off `full_page_writes` is only safe with a file system that avoids partial page writes (PG16 p.897).
- **When it is acceptable**: the manual lists these options as "non-durable settings" for sites that **do not require the durability guarantee**, including UNLOGGED tables (not crash safe); even so, only an abrupt OS crash creates a risk of data loss or corruption (PG16 p.563). The manual does not use the term "disposable workload"; any reading along those lines is `[inference]`.
- **Corrected in v1**: the phrase "invalidates ARIES" does not exist in the manual; and `fsync = off` is not forbidden, only risky.

## 8. Routine VACUUM FULL
- **Evidence [from source]**: requires `ACCESS EXCLUSIVE`, rewrites the table and needs extra space; "avoid VACUUM FULL" and prefer frequent standard VACUUM (PG16 p.789-790).

## 9. Stale statistics
- **Evidence [from source]**: without statistics, the planner assumes default values that are "almost certainly inaccurate" (PG16 p.482); autovacuum runs ANALYZE by threshold, but not on partitioned or foreign tables (PG16 p.790-791, p.797). Estimation errors propagate multiplicatively through the plan (ARCH p.45).

## 10. Partial index and parameterized queries
- **Evidence [from source]**: predicate matching happens at planning time; "parameterized clauses do not work with a partial index" (PG16 p.475-476).

## 11. Expecting an index-only scan without a visibility map
- **Evidence [from source]**: the gain exists only if a large fraction of the pages are all-visible; if the row changed recently, the heap is visited (PG16 p.477-478); `INCLUDE` columns are of little value on tables that change a lot (PG16 p.478).

## 12. Mass DELETE on a large table
- **Evidence [from source]**: with partitioning, `DROP`/`DETACH PARTITION` is much faster than a mass DELETE and avoids the VACUUM cost (PG16 p.132).

## 13. SQL Antipatterns: what the excerpt is, the book's scope and the table of contents
**Scope [from source]** (ANTI-INT p.9, "What's Not in This Book"): the book does not teach SQL syntax; **performance, scalability and optimization are not the focus** (it points to other books for that); it describes vendor-independent SQL whenever possible; data access frameworks and ORMs are not the focus; the examples are in PHP; **database administration and operation** (server sizing, installation, configuration, monitoring, **backups**, log analysis and **security**) are not covered; and the book is about SQL and relational databases, not alternative technologies (key/value, column-oriented, document-oriented, etc.) (ANTI-INT p.9-10). Consequence: questions about query performance, backup or NoSQL are **not** answered by this book; use PG16 (optimization, backup and PITR) or say it is out of scope. Each antipattern chapter has the sections Objective, The Antipattern, How to Recognize the Antipattern, Legitimate Uses and Solution (ANTI-INT p.8-9).

**What the package has of the book** (see `INDEX.md` section 1): real content only for chapters 21 (injection, without the solution), 3 (trees, without section 3.5), 1 (introduction); for the rest there is only the **table of contents** (ANTI-TOC p.5-9), that is, titles. The titles per chapter, in four parts and an appendix (titles in English, as in the book):
- Part I, logical design (ANTI-TOC p.5-6): 2 Jaywalking (objective: store multivalued attributes; solution: Create an Intersection Table), 3 Naive Trees (Use Alternative Tree Models), 4 ID Required (Tailored to Fit), 5 Keyless Entry (Declare Constraints), 6 Entity-Attribute-Value (Model the Subtypes), 7 Polymorphic Associations (Simplify the Relationship), 8 Multicolumn Attributes (Create Dependent Table), 9 Metadata Tribbles (Partition and Normalize).
- Part II, physical design (ANTI-TOC p.6-7): 10 Rounding Errors (Use NUMERIC Data Type), 11 31 Flavors (Specify Values in Data), 12 Phantom Files (Use BLOB Data Types As Needed), 13 Index Shotgun (MENTOR Your Indexes).
- Part III, queries (ANTI-TOC p.7-8): 14 Fear of the Unknown (Use Null as a Unique Value), 15 Ambiguous Groups (Use Columns Unambiguously), 16 Random Selection (In No Particular Order...), 17 Poor Man's Search Engine (Use the Right Tool for the Job), 18 Spaghetti Query (Divide and Conquer), 19 Implicit Columns (Name Columns Explicitly).
- Part IV, application development (ANTI-TOC p.8-9): 20 Readable Passwords (Store a Salted Hash of the Password), 21 SQL Injection (Trust No One), 22 Pseudokey Neat-Freak (Get Over It), 23 See No Evil (Recover from Errors Gracefully), 24 Diplomatic Immunity (Establish a Big-Tent Culture of Quality), 25 Magic Beans (The Model Has an Active Record).
- Part V, appendices (ANTI-TOC p.9): A1 Rules of Normalization; A2 Bibliography.
**How to use [inference]**: given a book antipattern whose chapter is not in the excerpt, the package only knows the **chapter name and the solution title**; the explanation is `[extrapolation]`. Example: chapter 10 (Rounding Errors) has "Use NUMERIC Data Type" as its solution title (ANTI-TOC p.6-7); detailed reasoning about floating point and money would require the full chapter and would be `[extrapolation]`.

## 14. Partitioning, backup/PITR, JSON, RLS and triggers: where each thing went
- **Partitioning a log table**: `postgresql-16-particionamento.md` (primary key includes the partition key; `ATTACH` with `CHECK`; `DETACH CONCURRENTLY`; count of partitions touched and pruning; PG16 p.132-145).
- **Losing data between logical backups**: `postgresql-16-backup-pitr-e-replicacao-ha.md` (continuous archiving, `archive_timeout` and PITR; PG16 p.800-812).
- **JSON field**: `postgresql-16-json-jsonb-e-gin.md` (`jsonb` by default; GIN; row lock; PG16 p.219-225).
- **Trigger that "disappears" the INSERT**: `postgresql-16-triggers-e-row-level-security.md` (`RETURN NULL` in a row-level BEFORE skips the operation; PG16 p.1303).
- **User sees rows they should not / table owner is not filtered**: same file (RLS, `FORCE ROW LEVEL SECURITY`, permissive policies combined by OR; PG16 p.118).
