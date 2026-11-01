# Origins, motivation and criticisms of the NoSQL movement

Convention: `(SIGLA p.N)` = PDF page (see INDEX). Main source: STRAUCH (~2010-2011 paper, **[DATED]** on products and versions). No sentence here is a copy; everything is synthesis.

## 1. The term and the context
- The term NoSQL was first used in 1998 for a relational database that dispensed with SQL; it was revived in 2009 at meetings of advocates of non-relational databases, and Eric Evans is cited as the one who popularized the term, with the idea of seeking alternatives when relational is a poor choice for the problem `[from source]` (STRAUCH p.6).
- The author defines the scope: the paper covers key/value, documents and columns; it **excludes** graph databases, pure XML, objects and special-purpose systems, and does **not** suggest individual products, since that would contradict the idea that there is no "one size fits all" solution `[from source]` (STRAUCH p.5).
- NoSQL as "Not Only SQL" (or "No to SQL") also appears in NEO4J-GDB, which defines the term by what the databases are *not* and highlights the dimensions volume, velocity and variety `[from source]` (NEO4J-GDB p.211-212).

## 2. Motivations cited (Computerworld, Shalom, Hoff, others)
All attributed to third parties within STRAUCH `[from source]`:
- Avoiding unnecessary complexity: not every application needs the ACID properties; example of session replicas kept only in memory (STRAUCH p.6).
- High throughput, horizontal scale and commodity hardware; schema rigidity; the cost of manual sharding in RDBMS (STRAUCH p.7-8).
- Avoiding the expensive object-relational mapping, when the structures are simple or close to those of the languages (STRAUCH p.7, 9).
- Trading reliability for performance in scenarios such as HTTP session data, and the argument that "one size fits all" is wrong (STRAUCH p.8).
- The myth of effortless distribution: the abstraction does not shield the application from network failures and latency; it is suggested to model for a partitioned environment from the start (STRAUCH p.9).
- Cloud: requirements of almost unlimited scalability and low administration (STRAUCH p.9-10); "MySQL + memcached" was the stopgap (STRAUCH p.10).
- Hardware that fails as the "normal mode of operation" and the **eight fallacies of distributed computing** (STRAUCH p.11-12).

## 3. Theoretical work: Stonebraker et al.
The paper "The End of an Architectural Era" argues that RDBMSs, as 25-year-old legacy code, are not optimal even in the OLTP market; the H-Store prototype, in-memory and single-threaded, ran TPC-C 82 times faster than a commercial DBMS (with the author's caveat that only part of the benchmark was implemented) `[from source]` (STRAUCH p.12-17). Conclusion of the cited paper: we are heading toward several specialized engines (STRAUCH p.18). Avoiding *two-phase commit* because of network round trips is one of the suggestions (STRAUCH p.15).

## 4. Criticisms
Business skepticism (open source with no "culprit"), hype, "nothing new", the "no to SQL" reading, Stonebraker's view, administrators' requirements, performance × scalability and "not every RDBMS is MySQL" `[from source]` (STRAUCH p.19-26). The final part of the critique lists choices by need (reporting and ACID: relational; cache: Tokyo Tyrant; counters: Redis; transactions: Postgres) `[from source]` (STRAUCH p.25-26).

## 5. Polyglot persistence
`[from source]` Scofield, noting the trend toward a pluralistic approach, says he suggested "polyglot persistence" "although he did not coin the term", and cites "LessSQL" by Ezra Zygmuntowicz (STRAUCH p.26). The source does **not** attribute the term to Martin Fowler (that is `[extrapolation]`, external knowledge). The passage in STRAUCH p.25-26 is the only basis for "use the right tool for the need".

Mapping of workloads to databases (financial ledger → relational; sessions and counters → Redis; catalogs → documents; telemetry → columns; recommendation → graphs): it is an `[inference]` supported by the uses the sources describe (REDIS p.7, 12, 20; MONGO-PAT p.89-97; STRAUCH p.118-119; NEO4J-GDB p.124-126), **not** a list from the book.

## 6. What the sources do not say
- A numbered "three determining factors", or "the limit of scale-up with exponential cost": the text lists several motivations, without this triad.
- That 2PC "locks all the cluster's transactions": STRAUCH says that protocols like 2PC/3PC are expensive and that round trips degrade performance (p.11, 15).
- Web 2.0 details on "petabytes of documents" etc.: not present.
