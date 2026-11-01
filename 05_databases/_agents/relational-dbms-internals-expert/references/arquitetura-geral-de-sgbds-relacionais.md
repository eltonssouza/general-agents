# General architecture of a relational DBMS

> Page convention: `(SIGLA p.N)` = **PDF** page (map in `INDEX.md`). ARCH: printed = N + 140. PG16: printed = N − 38.

## 1. The five components and the "life of a query" [from source]
- The article takes the **relational** DBMS as its focus and says a typical RDBMS has **five main components**, shown in Figure 1.1 (ARCH p.4). It presents them by following a simple query (the airport gate agent who asks for the passenger list of a flight) (ARCH p.4-7).
- Step 1, **Client Communications Manager**: establishes and remembers the connection state, responds to SQL commands and returns data and control messages; the client can talk directly to the server (two tiers), through an intermediate server (three) or with an additional application tier (four) (ARCH p.4-5).
- Step 2, **Process Manager**: assigns a "computation thread" to the command and connects its outputs to the client; the most important decision at this point is **admission control** (run now or defer until resources are available) (ARCH p.5).
- Step 3, **Relational Query Processor**: checks authorization, compiles the SQL into an internal plan and hands it to the *plan executor*, a collection of operators (joins, selection, projection, aggregation, sorting) (ARCH p.6).
- Step 4, **Transactional Storage Manager**: manages all data access; it includes *access methods* (tables and indexes), *buffer management*, the lock manager (invoked before accessing data) and the log manager (durability and undo) (ARCH p.6).
- Step 5: the stack "unwinds": the access methods return control to the operators, the results go to a buffer of the Client Communications Manager and, at the end, each module cleans up its state (ARCH p.7).
- On the right of Figure 1.1 are the **shared components and utilities** (catalog, memory manager and utilities that run independently of any query) (ARCH p.7); the detail is in Section 7 (ARCH p.100-110).

> Naming note: the article says *Relational Query Processor* and *Transactional Storage Manager*, not "Relational Engine" and "Storage Engine". Use the book's names when citing.

## 2. Where each topic is in ARCH (navigation map) [from source]
| Topic | PDF |
|---|---|
| Process models (process/thread/pool) | p.9-24 (see `modelos-de-processos-e-concorrencia-sgbd.md`) |
| Parallel architectures (shared-memory, shared-nothing, shared-disk, NUMA; partial failure and chained declustering p.29) | p.25-35 (see `modelos-de-processos-e-concorrencia-sgbd.md` section 5) |
| Query processor: parsing, rewrite, optimizer, executor (iterator, Halloween p.52-53) | p.36-55 (see `otimizacao-de-consultas-e-planos-de-execucao.md`) |
| Access methods, data warehouses (bitmap p.57-58, columnar p.62), extensibility | p.53-69 (see `data-warehouse-colunar-bitmap-e-extensibilidade.md`) |
| Storage and buffer pool | p.70-77 (see `buffer-pool-storage-engine-e-acesso-a-disco.md`) |
| Transactions: ACID, 2PL/MVCC/OCC, locks and latches, log/WAL, indexes | p.78-99 |
| Shared components: catalog, memory allocator, disks and RAID, replication (p.106-108), utilities | p.100-110 (see `componentes-compartilhados-catalogo-memoria-replicacao.md`) |

## 3. Points the book states that are often wrong when recalled from memory
- **Parallel execution of a query**: the iterator model does not change; parallelism is encapsulated in "exchange iterators" (ARCH p.50).
- **DDL** (CREATE TABLE, CREATE INDEX) normally does **not** go through the optimizer; it is implemented procedurally, calling the storage engine and the catalog manager (ARCH p.37).
- **Catalog**: it is stored as tables of the database itself, in the same format as the data; hot parts are materialized in memory in a "denormalized" form (ARCH p.100-101). A cited ERP had more than 60,000 tables (ARCH p.101).
- The truly **monolithic** part of the DBMS is the transactional storage manager (lock manager, log manager, buffer pool, access methods); the interface between the query processor and the transactional storage is well defined (ARCH p.78).
- **Architecture changed after the article**: Stonebraker, in the Red Book, says the details of the architecture article changed considerably within a few years, but the general parser/optimizer/executor structure remains valid; he states that column stores replaced row stores in data warehouses and that OLTP is moving toward main memory (REDBK p.2, p.21-22). [DATED] (2015 opinion).

## 4. PostgreSQL: path of a query [from source]
PG16 describes five stages: connection, parser, rewrite system, planner/optimizer, executor (PG16 p.2291). Details: "process per user" model with a supervisor (`postmaster`) that creates one backend per connection (PG16 p.2291-2292); the parser does not consult catalogs, the transformation phase does (PG16 p.2292-2293); the rewriter implements views by rewriting the tree (PG16 p.2293); the planner generates scan and join paths and chooses the cheapest (PG16 p.2293-2294).

## 5. [inference]
The component diagram is usually drawn as a cascade; the book says, on the contrary, that the components of the transactional storage are "deeply entwined" (ARCH p.78, p.95-97). When explaining, avoid suggesting that the lock manager, log and buffer pool are interchangeable modules.

## 6. What the sources do NOT say
- That the storage engine "typically uses 8 KB pages": that is from PG16 (PG16 p.2573); ARCH speaks only of the "size of a disk block" (ARCH p.74).
- The v1 mermaid flowcharts (Parser -> Catalog -> Optimizer etc.) were the package's own drawing, not a figure from the book; they were removed.
