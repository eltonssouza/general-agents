# Redis: persistence, replication, backup and scaling (REDIS ~2015) `[DATED]`

Convention: `(SIGLA p.N)` = PDF page (see INDEX). Seguin's book covers persistence in **a few paragraphs**; what v1 described (fork, copy-on-write, `appendfsync`, `BGREWRITEAOF`, hybrid strategy, `maxmemory`) **is not in the collection** and becomes `[extrapolation]` below. For any real configuration, use the current Redis documentation.

## 1. What the book says
- **Snapshot (default)**: Redis writes the database to disk according to the number of changed keys: "if X keys change, save every Y seconds"; by default, every 60 seconds if 1000 or more keys changed, up to 15 minutes if 9 or fewer changed `[from source]` `[DATED]` (REDIS p.9).
- **Append mode**: an alternative (or complement) to the snapshot; whenever a key changes, an *append-only file* (AOF) is updated on disk `[from source]` (REDIS p.9).
- The author notes that in some cases losing 60 s of data is acceptable in exchange for performance, and in others it is not; "Redis gives you the option" (p.9). A third option is to **delegate persistence to a slave** (p.9, 29).
- **Backup**: copy the snapshot (by default `dump.rdb`) to wherever you like (S3, FTP) at any time; it is not uncommon to disable snapshot and AOF on the master and let a slave do it, allowing more aggressive parameters without harming the master `[from source]` (REDIS p.29).
- **Replication**: writes on the master keep slaves up to date (`slaveof`); it protects data, and reads on the slaves may be slightly stale "but, for most apps, it is worth it" (p.29). `[DATED]`: the book states that there is **no automatic failover**; if the master dies, a slave must be promoted manually (p.29). "Master/slave" terminology is that of the time.
- **Scaling**: replication is the first tool; then, distributing keys among instances (some drivers offer consistent hashing); **Redis Cluster** was "under development" and would bring horizontal scaling, rebalancing and automatic failover `[from source]` `[DATED]` (REDIS p.29-30).
- Memory: Redis keeps everything in RAM; STRAUCH adds that the amount of data is limited by main memory and that, for this reason, it suits caching (p.71) and that it loses data if the server crashes without persistence (STRAUCH p.25, 32).

## 2. What is NOT in the sources (`[extrapolation]`)
- Snapshot mechanism via `fork()`/copy-on-write and the `BGSAVE` command.
- `appendfsync` policies (`always`, `everysec`, `no`) and the "maximum loss of 1 second".
- AOF rewrite (`BGREWRITEAOF`) and `auto-aof-rewrite-*`.
- "Recommended hybrid strategy" RDB + AOF.
- `maxmemory`, `maxmemory-policy`, `noeviction`, `allkeys-lru`, and the OOM error.
- Sentinel, replication with automatic failover, current Redis Cluster, modules, streams, RESP3, ACLs.
If the user asks about them, answer as labeled general knowledge `[extrapolation]` and refer to the current official documentation.

## 3. How to use
To decide durability: ask how much data may be lost and whether a source of truth exists in another database (the author says most teams use Redis to *supplement* a more general data solution, p.3) `[from source]`. For production operation: validate against the current documentation, since persistence, replication and cluster have changed a lot since 2015 `[DATED]`.
