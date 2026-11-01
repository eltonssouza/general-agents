# Redis: data structures, transactions, expiration and Lua (REDIS, Redis ~2.6-3.0)

Convention: `(REDIS p.N)` = PDF page (printed = PDF − 1). Seguin's book is short and from ~2015 (it cites Redis 3.0.3 as the most recent version, p.4): everything here is `[DATED]` as to versions. The commands are those of the book; current names and semantics may differ, consult the current documentation.

## 1. Philosophy
- Redis is often called a "persistent in-memory key-value store", but the author says this is not accurate: it exposes **five data structures**, only one of which is the typical key-value pair `[from source]` (REDIS p.7). Using specific structures for specific problems gives simplicity and speed (p.7); checking whether a value exists is O(1) (p.7).
- Databases are identified by number (default 0; `select`) (p.8). Keys identify data; the `:` separator is only a convention; values are treated as bytes (p.8).
- **Querying**: "keys are everything, values are nothing": the content of a value is not queried, so you cannot find "users from planet dune" from a JSON in a string (p.9). Some things "do not belong" in Redis because of this limitation (p.9).
- Speed: it is not only being in memory; the specialized structures are the reason; performance of "tens or hundreds of thousands of operations per second", depending on commands and data (p.10). Simplicity is compensated for with **more trips to the server** (p.10).
- Memory: Redis keeps all data in RAM; the cost is RAM; virtual memory was considered a failure and **deprecated** (p.9). Persistence: see `redis-persistencia-rdb-e-aof.md`.

## 2. The five structures (REDIS p.11-14)
| Structure | What the book says | Commands the book shows |
|---|---|---|
| Strings | the most basic structure; "scalars"; value can be anything; serialized objects, counters, cache | `set`, `get`, `strlen`, `getrange`, `append`, `incr`, `incrby`, `decr`, `decrby`, `setbit`/`getbit` (bitmaps; example of 128 million users in <50 ms and 16 MB) (p.11-12) |
| Hashes | like strings, with an extra level: the field; allows reading/updating/deleting parts without fetching the whole value | `hset`, `hget`, `hmset`, `hmget`, `hgetall`, `hkeys`, `hdel` (p.12); `hincrby` (p.18) |
| Lists | arrays ordered by key, index-based operations; logs, user trail, action queue | `lpush`, `ltrim` (O(N) in removed items; with one insert at a time it is O(1)), `lrange` (p.13); `rpush` (p.22) |
| Sets | unique values, unordered, set operations; friends, tags | `sadd`, `sismember` (O(1)), `sinter`, `sinterstore` (p.13-14) |
| Sorted sets | like sets, but with a **score** to order and rank; leaderboard is the most obvious case | `zadd`, `zcount`, `zrevrank` (p.14); `zremrangebyscore` (p.15); `zrangebyscore`/`zrangebyrank` cited (p.24) |

## 3. Complexity (REDIS p.15)
`sismember` O(1); `zadd` O(log N); `ltrim` O(N) where N is the number of removed elements; `zremrangebyscore` O(log N + M); `sort` O(N + M log M) (one of the most complex); no command is O(N²) or O(C^N). Big O deals with the worst case.

## 4. Modeling patterns (REDIS p.16-19)
- Lookup by two keys ("pseudo multi-key"): do not duplicate the object; use a **hash as a secondary index** (p.16).
- References and indexes are managed by hand; "there is no magic solution" (p.16-17).
- *Round trips* and **pipelining**: send several requests without waiting for the replies; Redis uses memory to queue them, so batching is advisable (p.17).
- **Transactions**: each command is atomic and Redis is **single-threaded**, which guarantees atomicity; `multi`/`exec`/`discard` execute commands in order, as an atomic operation, **all or nothing**; `watch` applies the transaction conditionally if the watched keys have not changed; the retry loop is done by the client (p.18-19). `incr` is a get followed by a set; `getset`, `setnx` (p.18).
- **`keys` anti-pattern**: does a linear scan over all keys; "never in production code" (the book's words); alternative: organize data into hashes (p.19). `scan` (Redis 2.8) is safe, with a cursor, a count that is only a hint, possible repeated results and a guarantee only for keys present throughout the whole iteration (p.23-24).

## 5. Beyond the structures (REDIS p.20-27)
- **Expiration**: `expire`, `expireat`, `ttl`, `persist`; `setex` sets a string and TTL in one atomic command (p.20).
- **Pub/sub** (`subscribe`, `publish`, `psubscribe`); `blpop`/`brpop` block until there is an element and can feed a simple queue (p.20-21).
- `monitor` (debugging only, be careful in production) and `slowlog` (last 1024 by default, in memory) (p.21).
- `sort` (by value, by pattern referenced `by`, `get`, `store`, `limit`, `alpha`, `desc`) (p.21-23); on large sets it can be slow (p.23).
- **Lua** (Redis 2.6): `eval`, `evalsha`, `script load`; each script runs without interruption, forming atomic commands; keys must be declared for future distributions (Cluster); default `lua-time-limit` of 5 s (p.25-27). Risks: hard-to-test code, business logic coupled to the data (p.25).

## 6. Basic administration (REDIS p.28)
`redis.conf` and `config set`/`config get`; `requirepass` + `auth` (once authenticated, the client can do anything, including `flushall`); `rename-command` for "security through obscurity" or disabling; practical limits per instance "in the hundreds of millions" of keys, fields or elements.

## 7. What the book does NOT contain (v1 attributed it to the book)
Event model with epoll/kqueue and "immunity to deadlocks" (the book only says it is single-threaded and atomic, p.18); SkipList + hash table in sorted sets; 512 MB limit per string; `ZREVRANGE`/`ZRANGE` as taught commands (there is only a mention of `zrangebyscore`/`zrangebyrank`, p.24); `SUNION`/`SDIFF` by name; queue with `LPUSH`+`BRPOP` as a recipe; "sliding-window rate limiter" with sorted sets; sub-millisecond latency; `maxmemory` and eviction policies. All of this is `[extrapolation]` (external knowledge, to be checked in the current documentation).
