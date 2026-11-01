# Glossary (terms with the page where the source defines them)

> Pages = PDF. Terms marked `[extrapolation]` are **not** defined in the package sources.

### A
- **ANY num_sync (...)**: **quorum**-based synchronous replication method: the commit waits for the WAL on at least `num_sync` standbys from the list (PG16 p.825, p.675).
- **Access method**: routine that manages access to the disk structures (heaps and indexes); all commercial systems implement heaps and B+-trees (ARCH p.53).
- **Adjacency List**: design in which each row has a `parent_id` referencing another row of the same table (ANTI-TREE p.6).
- **Admission control**: policy that does not accept new work without enough resources; acts in the dispatcher (connection limit) and in the query processor (estimated memory, CPU, I/O) (ARCH p.22-24).
- **ARIES**: "No Force, Steal" recovery algorithm with analysis, redo and undo and "repeating history" (REDBK p.18; ARCH p.90).
- **Autovacuum**: launcher + workers that run VACUUM and ANALYZE based on thresholds (PG16 p.796).

### B
- **BRIN**: index of summaries per range of adjacent blocks (PG16 p.2552); default `pages_per_range` is 128 (PG16 p.1758).
- **B-tree**: balanced multilevel tree, the only one that delivers ordered data and can be `UNIQUE` (PG16 p.468-469, p.473, p.2512).
- **Buffer pool**: array of frames the size of the disk block, with a hash table and metadata (dirty bit, pin count) (ARCH p.74-75).

### C
- **Crabbing (latch coupling)**: B+-tree descent in which the child is latched before the parent is released; only valid for B+-trees (ARCH p.92-93).
- **COMMIT PREPARED**: commits a prepared transaction (two-phase commit); outside a transaction block, same user or superuser (PG16 p.1695).
- **Checkpoint**: point at which dirty pages are flushed and a special record goes to the WAL (PG16 p.900); in ARIES the checkpoint is "fuzzy" (ARCH p.91).
- **Closure Table** `[extrapolation]`: auxiliary table of ancestor-descendant pairs (not described in the book excerpt).
- **Cost-based optimizer**: optimizer that estimates costs in I/O and CPU and looks for the cheapest plan (REDBK p.16; ARCH p.42-45).
- **Covering index**: index with extra `INCLUDE` columns to allow index-only scans (PG16 p.477-478).

### D
- **Dirty bit**: frame metadata that indicates a change since it was read from disk (ARCH p.75).
- **Deadlock**: wait cycle between transactions, detected periodically by the lock manager (ARCH p.83).

### F
- **FIRST num_sync (...)**: **priority-based** synchronous replication method; a synchronous standby that goes down is replaced by the next one in the list (PG16 p.825, p.675).
- **Failover**: promotion of the standby when the primary fails; PostgreSQL does not provide the failure detector (PG16 p.827).
- **Free Space Map (FSM)**: one byte per page indicating free space, organized as a tree; it does not exist for hash (PG16 p.2572).
- **Fuzzy checkpoint**: see Checkpoint (ARCH p.91).

### G
- **GID (global transaction identifier)**: name (under 200 bytes) of a prepared transaction, mapped to the xid in `pg_prepared_xacts` (PG16 p.1989, p.2577).
- **GIN**: inverted index (key, posting list) (PG16 p.2545).
- **GiST**: extensible balanced-tree infrastructure; supports nearest neighbor (PG16 p.469, p.2515).
- **Group commit**: deferring the log flush to group commit records into a single I/O (ARCH p.18).

### H
- **Hash index**: stores a 32-bit hash; only `=` (PG16 p.469, p.2565).
- **Hash join**: loads one relation into a hash table and probes it with the other (PG16 p.2294, p.546-547).
- **Heap**: unordered file of rows (ARCH p.53); in PostgreSQL, the main area of the table (PG16 p.477).
- **HOT (heap-only tuple)**: UPDATE optimization possible when the update does not modify columns referenced by the table's indexes, **not counting summarizing indexes (the only one in core is BRIN)**, and there is room in the page of the old row; it avoids new index entries (summarizing indexes may still need updating) and allows removing old versions in normal operation, even in SELECT; monitor in `pg_stat_all_tables` (PG16 p.2576).

### I
- **INCLUDE**: "payload" columns in a B-tree/GiST/SP-GiST index (PG16 p.478).
- **Index-only scan**: answer from the index alone, consulting the visibility map (PG16 p.477-478).
- **Iterator**: operator with `init()`, `get_next()`, `close()` (ARCH p.48-49).

### L
- **Latch**: lightweight mutual exclusion for internal structures; a latch deadlock is a bug (ARCH p.83-84).
- **Lock**: name registered in the lock table with modes and a wait queue (ARCH p.82-83).
- **LSN (Log Sequence Number)**: in PostgreSQL, the 8-byte `pd_lsn` indicates the last WAL record of the page (PG16 p.2574). "Recovery LSN" in ARIES: starting point of recovery (ARCH p.90).

### M
- **Merge join**: sorts both relations by the keys and scans them in parallel (PG16 p.2294, p.547).
- **MVCC**: each command/transaction sees a snapshot; reads do not block writes (PG16 p.525; ARCH p.81).

### N
- **n_distinct**: per-column option (`ALTER TABLE ... SET (n_distinct = ...)`) that overrides ANALYZE's estimate of distinct values; positive = exact, between −1 and 0 = fraction of the rows (PG16 p.1644).
- **Nested loop join**: the right relation is scanned once for each row of the left (PG16 p.2294, p.545-546).
- **Nested Sets** `[extrapolation]`: hierarchy model based on intervals (outside the excerpt).

### O
- **OCC (optimistic concurrency control)**: transactions without blocking, with validation before commit (ARCH p.81-82).
- **Operator class**: defines the operators an index uses for a column (PG16 p.479-480).

### P
- **pg_rewind**: resynchronizes a former primary by copying only the changed blocks; requires `wal_log_hints` or checksums and `full_page_writes` (PG16 p.2256).
- **Parallel Aggregate (Partial/Finalize)**: two-stage aggregation; not used with DISTINCT/ORDER BY, ordered-set, GROUPING SETS (PG16 p.567).
- **Partial index**: index with a WHERE predicate (PG16 p.474-476).
- **Pin count**: counter that keeps the page out of replacement (ARCH p.75).
- **Predicate lock (SIReadLock)**: non-blocking lock used by SSI (PG16 p.530).
- **Prepared statement**: query parsed and optimized once and executed with values later (ARCH p.47; ANTI-INJ p.12).
- **Process per worker**: one OS process per client; PostgreSQL uses only this model (ARCH p.13-14, p.20; PG16 p.2291).

### Q
- **Query parameter**: value supplied separately from the query text, interpreted as a single literal (ANTI-INJ p.9-10).

### S
- **STONITH**: mechanism to ensure that the former primary does not consider itself primary again after failover (PG16 p.827).
- **Replication slot**: makes the primary retain WAL not yet received by the standbys; can fill `pg_wal` (PG16 p.822).
- **SARG**: search argument "column operator constant" passed to the access method (ARCH p.54).
- **Selinger (System R optimizer)**: System R optimizer with dynamic programming and left-deep trees (REDBK p.16; ARCH p.42-44).
- **Serializable Snapshot Isolation (SSI)**: PG's Serializable level, built on Snapshot Isolation, with predicate locks (PG16 p.529-531).
- **Snapshot Isolation**: operates on the version as of the start of the transaction; first committer wins (ARCH p.87); it is PG's Repeatable Read (PG16 p.529).
- **Strict 2PL**: all locks are held until the end of the transaction (ARCH p.80-81).

### T
- **Thread pool**: workers multiplexed over a pool of threads; SQL Server's default (ARCH p.22).
- **TOAST**: out-of-line storage/compression of large values; threshold ~2 kB; four strategies (PG16 p.2569-2571).
- **Transaction ID wraparound**: the 32-bit XID wraps around; requires vacuuming each table every 2 billion transactions (PG16 p.791-792).

### V
- **VACUUM**: reclaims space, updates statistics and the visibility map, freezes XIDs (PG16 p.788).
- **Visibility map**: 2 bits per heap page: all-visible and all-frozen (PG16 p.2572).

### W
- **wal_log_hints**: writes the whole page to the WAL on the first modification after the checkpoint, even for hint bits; default off (PG16 p.665).
- **WAL**: changes to data are only written after the log records have been flushed (PG16 p.898; ARCH p.88-89).
- **Write skew** `[extrapolation]`: term from the isolation literature; it does not appear in ARCH, REDBK or PG16 (PG16 shows the concrete example, p.529-530).

### X
- **xmin / xmax (`t_xmin`, `t_xmax`)**: XID stamps of insertion and deletion in the tuple header (4 bytes each) (PG16 p.2575). `xmin`/`xmax` are also components of the snapshot, with a different meaning (PG16 p.429).

### Added terms (round 2 correction, alphabetical order)
- **ATTACH PARTITION / DETACH PARTITION**: attach an existing table as a partition or remove a partition, keeping it as a table; `DETACH ... CONCURRENTLY` requires only `SHARE UPDATE EXCLUSIVE` on the parent (PG16 p.135-136).
- **archive_timeout**: forces the WAL segment switch at most at this interval, to limit archiving lag; values of about one minute are reasonable, and very short ones bloat the archive (PG16 p.807).
- **Bitmap index**: one bit per record and value, good for few values and conjunctive filters (intersection), expensive to update; the paper's example uses 1 bit versus ~40 bits for a B+-tree (ARCH p.57-58).
- **Chained declustering**: fine-grained redundancy in shared-nothing in which copies of the tuples are kept on several nodes; on failure, the n-1 survivors each do n/(n-1) of the work (ARCH p.29, p.106).
- **Data Skip**: approach (Informix) in which queries run on the active nodes skipping the data of the failed node; *best effort* results (ARCH p.29).
- **Halloween problem**: update plan that rereads tuples it modified itself; solved by avoiding indexes on the updated column or by materializing RIDs before updating; nothing to do with ghosts (ARCH p.52-53).
- **jsonb**: JSON in decomposed binary format, indexable, faster to process and slightly slower to insert; `json` stores the exact text (PG16 p.219).
- **Log-based replication**: replication by sniffing/shipping the log; the paper's preferred solution for edge environments (ARCH p.107-108).
- **Memory context**: region-based allocator that frees everything at once at the end of the phase (parser, optimizer, executor) (ARCH p.101-103).
- **Partition pruning**: the planner (or the executor) proves that a partition contains no rows matching the `WHERE` and excludes it; driven by the partition bounds, not by indexes (PG16 p.142-144).
- **PITR (Point-in-Time Recovery)**: restore a base backup and replay archived WAL up to a target later than the end of the backup (PG16 p.805, p.811-812).
- **RAID 5 / RAID 1**: the paper criticizes RAID 5 for its poor write performance and prefers mirroring (level 1) for databases (ARCH p.106).
- **Right-link**: link from each B+-tree node to its right neighbor; readers "move right" after a split; basis of PostgreSQL's GiST (ARCH p.93).
- **RLS (Row-Level Security)**: per-table policies that filter rows by role; the owner is normally not filtered, unless `FORCE` is used (PG16 p.118).
- **RID**: physical row identifier used by indexes; moving the row forces secondary indexes to be updated (ARCH p.55).
- **Shared-disk / shared-nothing / shared-memory**: see `modelos-de-processos-e-concorrencia-sgbd.md` section 5 (ARCH p.25-35).
- **Timeline**: branch of the WAL history created at the end of each archive recovery (PG16 p.812).
- **BEFORE ROW trigger with RETURN NULL**: skips the operation on the row; AFTER ignores the return value (PG16 p.1303-1304).

### PT/EN equivalences (English terms the sources use; added in the round 4 correction)
- **Equivalences validated against the pages in round 6** (also in the `aliases` field of `relational_index.json`): *standard practice* = prática padrão (ARCH p.67-69); *full-text search* = busca textual (PG16 p.519-520) and busca de texto (ARCH p.65-66); *recovery conflict* = conflito de recuperação / conflitos de consulta (PG16 p.829-831, p.868). Standard practice (*prática padrão*) appears as an ARCH section title on p.20-21, p.33, p.67 and p.97.
- **Logical replication** (*replicação lógica*): publication/subscription per table, based on the replica identity, instead of physical blocks (PG16 p.905-927).
- **Row filter** (*filtro de linha*): WHERE clause of the publication that limits the replicated rows (PG16 p.912-920).
- **Column list** (*lista de colunas*): subset of a table's columns that the publication replicates (PG16 p.920-923).
- **Initial synchronization** (*initial table synchronization*, *initial data synchronization*, *initial synchronization*; Portuguese "sincronização inicial"): copy of the tables' snapshot before applying real-time changes (PG16 p.925).
- **Parallel query** (*parallel query*; Portuguese "consulta paralela"): plan in which workers run parts of the query and a node gathers the results (PG16 p.564-568).
- **Prepared transaction** (*prepared transaction*; Portuguese "transação preparada"): transaction left ready by PREPARE TRANSACTION, completed later by COMMIT PREPARED or ROLLBACK PREPARED (PG16 p.1989-1990).
- **Weak isolation** (*weak isolation*; Portuguese "isolamento fraco"): isolation levels below serializable, common in practice and with possible anomalies (REDBK p.28-29).
- **Table-level lock** (*table-level lock*; Portuguese "lock de tabela"): table-level lock, with several modes and a conflict matrix (PG16 p.531-534).
- **Row-level lock** (*row-level lock*; Portuguese "lock de linha"): row-level lock (FOR UPDATE, FOR SHARE etc.) (PG16 p.531-534).
- **CHECK constraint** (*check constraint*; Portuguese "restrição CHECK"): constraint requiring a boolean expression to be true in every row (PG16 p.99-104).
- **UNIQUE constraint** (*unique constraint*; Portuguese "restrição UNIQUE"): constraint that prevents repeated values in the column or group of columns (PG16 p.99-110).
- **Generated column** (*generated column*; Portuguese "coluna gerada"): column computed from other columns of the same row (PG16 p.99-110).
- **Trigger function** (*trigger function*; Portuguese "função de trigger"): function the trigger runs; in PostgreSQL it returns type trigger (PG16 p.1302-1304).
- **Row-level / statement-level trigger** (*row-level trigger*, *statement-level trigger*; Portuguese "trigger por linha / por comando"): fires once per affected row or once per command (PG16 p.1302-1304).
- **Partitioned table** (*partitioned table*; Portuguese "tabela particionada"): logical table divided into physical partitions by range, list or hash (PG16 p.132-145).
- **Range, list and hash partitioning** (*range partitioning*, *list partitioning*, *hash partitioning*; Portuguese "particionamento por faixa, lista e hash"): the three strategies of declarative partitioning (PG16 p.132-145).
- **Default partition** (*default partition*; Portuguese "partição default"): partition that receives the rows no other partition accepts (PG16 p.132-145).
- **Partition key** (*partition key*; Portuguese "chave de partição"): column or expression that decides which partition the row falls into (PG16 p.132-145).
- **Dead tuple** (*dead row versions*; Portuguese "tupla morta"): deleted or obsolete row version that stays physically in the table until VACUUM (PG16 p.788-791).
- **Page layout** (*page layout*; Portuguese "layout de página"): internal organization of a table or index page (header, item identifiers, free space, items) (PG16 p.2567-2576).
- **High availability** (*high availability*; Portuguese "alta disponibilidade"): continuous operation with a standby server, compared with other replication solutions (PG16 p.815-818).
- **Load balancing** (*load balancing*; Portuguese "balanceamento de carga"): distribution of queries among servers, compared with the other solutions (PG16 p.815-818).
- **Synchronous replication** (*synchronous replication*; Portuguese "replicação síncrona"): the commit only finishes after the standby confirms the WAL (PG16 p.824-827).
- **Quorum commit** (*quorum*; Portuguese "commit por quórum"): ANY method of synchronous replication: it is enough for the WAL to reach a minimum number of standbys (PG16 p.824-827).
- **Cumulative statistics** (*cumulative statistics*; Portuguese "estatísticas cumulativas"): system of accumulated activity counters, read by the pg_stat_* views (PG16 p.837-838).
- **Continuous WAL archiving** (*continuous archiving*, *wal archiving*; Portuguese "arquivamento contínuo de WAL"): copying of WAL segments to an external archive, the basis of PITR (PG16 p.804-807).
- **Cascading replication** (*cascading replication*; Portuguese "replicação em cascata"): a standby that passes the WAL on to other standbys (PG16 p.823).
- **Standby query conflict** (*query conflict*; Portuguese "conflito de consulta no standby"): query on the hot standby that interferes with WAL replay (or is canceled by it) (PG16 p.828-835).
- **Extended statistics** (*extended statistics*; Portuguese "estatísticas estendidas"): multi-column or expression statistics created by CREATE STATISTICS (PG16 p.555-557).
- **Statistics target** (*statistics target*; Portuguese "meta de estatísticas"): how much detail ANALYZE collects per column (PG16 p.1644).
- **Asynchronous commit** (*asynchronous commit*; Portuguese "commit assíncrono"): the commit returns before the WAL is written to disk, with the risk of losing the last transactions (PG16 p.899-900).
- **Page replacement** (*page replacement*; Portuguese "substituição de páginas"): buffer pool policy that chooses the page to evict (ARCH p.74-76).
- **Thread per worker** (*thread per dbms worker*; Portuguese "thread por worker"): process model in which each DBMS worker is a thread (ARCH p.12-16).
- **Process pool** (*process pool*; Portuguese "pool de processos"): model in which a set of processes serves the requests (ARCH p.12-16).
- **Star schema** (*star schema*; Portuguese "esquema estrela"): data warehouse design with a central fact table and dimension tables (ARCH p.56-62).
- **Column store** (*column store*; Portuguese "armazenamento colunar"): stores each column separately, favoring analytical queries (ARCH p.62).
- **System catalog** (*catalog*; Portuguese "catálogo do sistema"): tables that describe the tables, indexes, types and other objects of the database itself (ARCH p.100-101).
- **Memory allocator** (*memory allocator*; Portuguese "alocador de memória"): the DBMS's memory allocation service, with contexts that free everything at once (ARCH p.101-104).
- **Physical replication** (*physical replication*; Portuguese "replicação física"): replication by blocks or WAL, as opposed to logical (PG16 p.905).
- **Expression index** (*expression index*; Portuguese "índice de expressão"): index on the result of an expression, not only on columns (PG16 p.470-479).
- **Dynamic SQL** (*dynamic sql*; Portuguese "SQL dinâmico"): SQL assembled as a string with application variables (ANTI-INJ p.5).
- **Deterministic concurrency control** (*deterministic concurrency control*; Portuguese "controle de concorrência determinístico"): alternative to 2PL cited by the Red Book for in-memory OLTP (REDBK p.22).
- **Atomic commitment (AC)** (*atomic commitment*; Portuguese "commit atômico"): guarantees that the transaction commits or aborts on all servers involved; often called atomic commit; the classic is 2PC (REDBK p.18-19).
- **Consensus** (*consensus*; Portuguese "consenso"): protocol in which processes agree on a proposal; basis of replication (Paxos, Raft) (REDBK p.19).
- **Parallel vacuum** (*parallel vacuum*; Portuguese "vacuum paralelo"): use of several workers in the index phase of VACUUM (PARALLEL option) (PG16 p.2063-2065).
- **Eventual consistency** (*eventual consistency*; Portuguese "consistência eventual"): eventual consistency of the NoSQL databases that relax isolation (REDBK p.30).
- **Raw device** (Portuguese "dispositivo bruto"; *raw disk*, *raw-mode access*): the DBMS writes directly to the disk device and avoids the file system; the paper discusses the drawbacks (OS-specific interfaces) and the alternative of using a very large file as the disk space (ARCH p.70-74).
- **50-100x** (column vs. row in the Red Book): the range the Red Book cites for the gain of column storage is a 2015 opinion, with no benchmark on the page (REDBK p.21).
- **Active-active** (and *active-passive*): in active-active each replica executes the transactions; the Red Book (REDBK p.22) says that log-based active-passive replication proved in [6] to be a factor of 3 worse, and that MVCC does not guarantee the same order on the replicas, which motivated deterministic concurrency control [DATED].
