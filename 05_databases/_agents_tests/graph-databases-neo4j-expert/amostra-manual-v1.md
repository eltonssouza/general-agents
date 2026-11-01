# Manual sample from the v1 audit (reading the PDF pages)

Each row is a claim of the ORIGINAL package (v1), with the citation as it was (**printed** numbering; PDF = printed + 18) and the PDF page where the text was read. Verdicts: **OK** (supported), **PAG** (supported, but on another page), **NS** (not supported), **EX** (exaggeration or embellishment over what the book says).

Total: 91 claims. OK: 22; wrong page: 1; not supported: 40; exaggeration: 28.

Sample coverage: 14 of the 15 reference files (the glossary repeats the rest), the agent prompt and the script rules; all chapters 1-7 of the book (Appendix A and the index were never cited by v1).

| # | Area | Claim (v1) | v1 citation | Verdict | Evidence (PDF) |
|---|---|---|---|---|---|
| 1 | IFA | the cost of following a relationship is O(1) | print. 8, 149-151 | OK | PDF 168-170 (O(1) vs O(log n)) |
| 2 | IFA | traversal O(k^d), independent of N | print. 8-9, 18-21 | NS | PDF 26, 168: 'proportional to the part traversed'; k^d notation absent |
| 3 | IFA | relational joins cost O(k^d . log N) via B+ tree | print. 8-9, 11-14 | NS | PDF 29-32, 168: only O(log n)/O(m log n); no B+ |
| 4 | IFA | from 100,000 to 100,000,000 rows the time degrades continuously | print. 8, 14 | NS | PDF 38-39: the book gives Table 2-1 (1,000,000 people) |
| 5 | IFA | beyond 3-4 hops the relational query hangs or runs out of memory (join explosion) | (no page) | EX | PDF 39: depth 4 = 1543 s; depth 5 'unfinished'; memory not cited |
| 6 | IFA | the index only locates the starting node | print. 28, 150 | PAG | PDF 185-186 (print. 167-168); print. 28/150 do not say this |
| 7 | IFA | node indexes are B-Trees or Lucene | print. 28, 150 | NS | search: 'Lucene' and 'B-tree' absent from the book |
| 8 | Relational | an FK is just a column; the database does not know about the relation until the JOIN | print. 11-13 | OK | PDF 29-30 |
| 9 | Relational | N:M join tables degrade reads | print. 12-14 | OK | PDF 30 |
| 10 | Relational | recursive WITH RECURSIVE queries are slow; ANTI-TREE p.2-6 | print. 14-15 | EX | PDF 32: 'recursive joins' and CONNECT BY; CTE absent; ANTI-TREE out of scope |
| 11 | Relational | aggregates: reference to STRAUCH p.50-70 | print. 15-18 | NS | source outside the declared scope; not verifiable in this agent |
| 12 | Relational | there is no native link between documents on different servers | print. 15-18 | EX | PDF 33-34: embedded ids, no first-class relationships |
| 13 | Relational | joins in the application remove the transactional guarantee | print. 16-18 | EX | PDF 33-36: 'prohibitively expensive'; transaction not cited |
| 14 | Relational | comparison table (full ACID; BASE; ERP strength) | print. 18-24 | NS | PDF 37-42; ACID/BASE only in App. A (PDF 213-214) |
| 15 | Cypher | ASCII-art syntax for nodes and relationships | print. 28-30 | OK | PDF 46-48 |
| 16 | Cypher | MATCH, WHERE, RETURN | print. 30-31 | OK | PDF 47-49 |
| 17 | Cypher | RETURN can use avg() and JSON | print. 30-31, 50 | EX | PDF 68-69: count, collect; avg and JSON absent |
| 18 | Cypher | CREATE creates; MERGE avoids duplication | print. 31-32, 45-48 | OK | PDF 64 |
| 19 | Cypher | MERGE with ON CREATE SET and ON MATCH SET | print. 31-32, 47-48 | NS | search: ON CREATE/ON MATCH absent |
| 20 | Cypher | WITH chains queries | print. 51-52 | OK | PDF 69-70 |
| 21 | Cypher | never interpolate literals; plan cache | print. 46-47 | NS | PDF 64-66: indexes; plan/cache absent |
| 22 | Cypher | interpolation exposes Cypher injection | print. 46-47 | NS | injection absent from the book |
| 23 | LPG | four primitives: nodes, labels, relationships, properties | print. 26-28 | OK | PDF 22, 44 |
| 24 | LPG | zero, one or several labels per node | print. 26-28 | EX | PDF 22: 'one or more' |
| 25 | LPG | a label anchors an index and CONSTRAINT ASSERT IS UNIQUE | print. 28, 46-48 | OK | PDF 62, 65 |
| 26 | LPG | a unique type in uppercase and no orphan relationships ('inviolable rules') | print. 26-27 | EX | PDF 44: unique name and start/end nodes; uppercase = convention of the examples |
| 27 | LPG | properties: homogeneous arrays | print. 27-28 | EX | PDF 44: 'arrays of these types'; 'homogeneous' absent |
| 28 | LPG | properties on relationships eliminate association tables | print. 27-29 | EX | PDF 45: metadata, weight, semantics |
| 29 | LPG | NEO_START p.1-2 defines the LPG | NEO_START 1-2 | NS | NEO_START is a website index page (topic titles) |
| 30 | Modeling | nodes for things, relationships for structure | print. 66-67 | OK | PDF 85 |
| 31 | Modeling | 'always' use fine-grained relationship types | print. 67-68 | EX | PDF 85-86: trade-off; weights in properties |
| 32 | Modeling | the engine groups relationships by type on disk/cache; hops go through the type's list | print. 67-68, 154 | NS | PDF 173: one list per node/side; it iterates until it finds a candidate |
| 33 | Modeling | reify: EmploymentContract links Person, Company, Role, Department | print. 68-71 | EX | PDF 86-87: Job between Person, Company and Role |
| 34 | Modeling | address in shared Neighborhood/City | print. 71-72 | EX | PDF 89: only the Address node |
| 35 | Modeling | evolution with zero downtime | print. 74-76 | EX | PDF 27, 76, 92: additive, fewer migrations |
| 36 | Temporal | time tree Year-Month-Day-Hour | print. 72-74 | EX | PDF 90-91: Year, Month, Day; hour absent |
| 37 | Temporal | query without scanning or date conversion | print. 73-74 | EX | PDF 91: long, verbose WHERE |
| 38 | Temporal | a :NEXT chain finds the successor in O(1) | print. 73-74 | OK | PDF 91-92 (names: NEXT/PREVIOUS) |
| 39 | Temporal | validity intervals: two strategies (plan subscription) | print. 74, 124-128 | NS | PDF 153-157 (Global Post); print. 124-128 = access control |
| 40 | Supernodes | supernodes: tens of thousands to millions of edges | print. 52-54, 150 | NS | search: 'supernode'/'dense node' absent; PDF 70-72 is the email case |
| 41 | Supernodes | supernodes cause write-lock contention | print. 150, 162 | NS | PDF 168, 180-181: no link to supernodes |
| 42 | Supernodes | supernode traversal becomes a linear O(k) scan | print. 150-152 | NS | PDF 173 only describes the linked list |
| 43 | Supernodes | the email case evolves supernodes | print. 52-64 | NS | PDF 70-82: lossy relationship -> Email node |
| 44 | Supernodes | a time tree distributes the email fan-out | print. 58-64, 72-74 | NS | PDF 76-82 do not use a time tree |
| 45 | Supernodes | four mitigation strategies | print. 60-64, 150-152 | NS | absent from the book |
| 46 | Supernodes | low cardinality (gender) as a property | print. 66-68 | NS | only an inference from PDF 85 |
| 47 | Storage | 15-byte node: 1+4+4+5+1 | print. 152-153 | OK | PDF 171 (figure), 172 |
| 48 | Storage | 34-byte relationship; last byte = direction/properties flag | print. 153-155 | EX | PDF 171: the last byte is firstInChainMarker |
| 49 | Storage | 'circular' doubly linked list | print. 153-155 | EX | PDF 173: 'doubly linked'; 'circular' absent |
| 50 | Storage | offset = ID x record size | print. 152 | OK | PDF 172, 174 |
| 51 | Storage | strings/arrays go to dynamic stores | print. 156-157 | OK | PDF 174-175 |
| 52 | Storage | off-heap page cache | print. 157-158 | OK | PDF 175-176 (since Neo4j 2.2; LRU-K) |
| 53 | Storage | off-heap cache eliminates GC stop-the-world pauses | print. 157 | NS | search: 'stop-the-world' absent |
| 54 | Storage | in-memory traversal with sub-microsecond latency | print. 158 | NS | no latency numbers in the book |
| 55 | Storage | heap 8-16 GB; OS 2-4 GB; page cache 44 GB; dbms.memory.* | print. 95-98, 157 | NS | PDF 115: 4-8 GB heap; no dbms.memory |
| 56 | Transactions | atomicity with full rollback | print. 162 | OK | PDF 180-181 |
| 57 | Transactions | existence constraints checked before commit | print. 162-163 | NS | absent |
| 58 | Transactions | default isolation Read Committed | print. 163 | NS | search: 'read committed' absent |
| 59 | Transactions | reads without locks | print. 162 | NS | PDF 180-181: only write locks |
| 60 | Transactions | lock on both nodes when creating/deleting a relationship | print. 150, 162-163 | EX | PDF 180-181: write locks 'on the nodes and relationships involved' |
| 61 | Transactions | deadlock via Wait-For Graph; aborts one transaction | print. 163 | NS | PDF 181: detects and serializes |
| 62 | Transactions | WAL: flush the log before applying and replying | print. 163-164 | OK | PDF 181 |
| 63 | Cluster | Causal Cluster: Core + Read Replicas with Raft/Paxos | print. 81-84, 164-168 | NS | search: Raft/Paxos/Causal absent; book = master-slave HA (PDF 99-102, 182-183) |
| 64 | Cluster | 3 or 5 core servers, majority N/2+1 | print. 81-83 | EX | PDF 116: redundancy 1 with 3 or 4; 2 with 5 |
| 65 | Cluster | asynchronous read replicas | print. 82-84, 166-168 | NS | PDF 182-183: slaves; frequent master writes |
| 66 | Cases | Talent.net: WORKED_IN query; <10 ms; nightly MapReduce | print. 111-123 | NS | PDF 129-140: WORKS_FOR/INTERESTED_IN/WORKED_ON; no such numbers |
| 67 | Cases | RBAC: recursive joins with UNION ALL take seconds | print. 123-125 | EX | PDF 141: 'many minutes'; UNION ALL absent from the problem |
| 68 | Cases | GBAC with MEMBER_OF*0.. sub-millisecond | print. 125-132 | NS | PDF 142-149: ALLOWED_INHERIT/DENIED; 'milliseconds' |
| 69 | Cases | Campinas->Recife logistics with shortestPath | print. 132-147 | NS | PDF 150-165: Global Post; invented example |
| 70 | Cases | native weighted Dijkstra in Cypher | print. 138-144 | NS | PDF 157-159, 164: Cypher uses reduce; Dijkstra via Java |
| 71 | Advanced Cypher | *1..3 and *2 as variable-length rules | print. 48-49 | EX | PDF 58, 66, 78: examples *1..5, *1..2, *1..4 |
| 72 | Advanced Cypher | '-[*]->' causes OutOfMemoryError; always bound it | print. 49, 115, 116 | NS | PDF 80 uses FORWARD_OF* without a bound; PDF 136 only warns of inefficiency |
| 73 | Advanced Cypher | shortestPath/allShortestPaths based on BFS | print. 50-51, 116-118 | NS | allShortestPaths absent; PDF 97, 106 only shortestPath |
| 74 | Advanced Cypher | FOAF query with count(friend) | print. 111-118 | NS | the query is not in the book |
| 75 | Theory | DFS and BFS | print. 171-173 | OK | PDF 189-191 |
| 76 | Theory | greedy Dijkstra with a priority queue | print. 173-176 | EX | PDF 191: 5 steps; priority queue absent |
| 77 | Theory | A*: f(n) = g(n) + h(n) | print. 181-182 | OK | PDF 199 |
| 78 | Theory | Euclidean/geodesic heuristic | print. 181-182 | EX | absent; the book only mentions 'heuristic' |
| 79 | Theory | triadic closure: 'extremely high' probability | print. 182-184 | EX | PDF 200: 'higher probability' |
| 80 | Theory | structural balance: balanced triangles | print. 184-188 | OK | PDF 205 |
| 81 | Theory | local bridge: removal pushes the distance beyond 2 hops | print. 188-190 | NS | PDF 207: informal definition (the only channel between groups) |
| 82 | Theory | weak ties spread innovations (Granovetter) | print. 189-190 | EX | PDF 208: example is job hunting |
| 83 | Procedures | time tree with cascading MERGE | print. 72-74 | OK | PDF 91 |
| 84 | Procedures | CREATE INDEX ON :Label(prop) | print. 46-47 | OK | PDF 65 |
| 85 | Procedures | EXPLAIN/PROFILE with NodeUniqueIndexSeek | print. 46-47 | NS | search: absent |
| 86 | Procedures | supernode diagnosis with size((n)<--()) > 50000 | print. 52-64, 150 | NS | absent; invented threshold |
| 87 | Anti-patterns | Kitchen Sink Relationship: the engine reads all relationships and compares the property string | print. 67-68, 154 | EX | PDF 85: properties live in another file (extra I/O on first read); the name 'Kitchen Sink' is v1's |
| 88 | Anti-patterns | client-side traversal: a loop of queries to the database | print. 16-18, 100 | EX | PDF 34-36 talk about joins in the application in aggregate stores; PDF 118 is CSV import |
| 89 | Anti-patterns | a composite value in a single string forces regex search | print. 71-72 | EX | PDF 89 only recommends a node for a complex value type; regex is an invented consequence |
| 90 | Agent | warn about interpolation; mandatory parameters | print. 46-47 | NS | see Cypher |
| 91 | Agent | FOAF recommendation engine | print. 111-118 | NS | see Advanced Cypher |
