# 11. Distributed systems, RPC, NFS and AFS (ch. 47-51)

PDF: ch.47 (dialogue) = p.760-761; ch.48 = p.764-780; ch.49 (NFS) = p.794-811; ch.50 (AFS) = p.816-829; ch.51 (dialogue) = p.833-834.

## 1. Communication (ch.48)

- **[from source]** Failure is the central challenge: machines, disks, networks and software fail; communication is **inherently unreliable** (flipped bits, faulty links/routers and, above all, lack of buffering) (OSTEP p.764-766). **UDP** is the unreliable layer (datagrams; sockets; includes a checksum but does not report loss) (OSTEP p.766-768).
- **[from source]** Reliable layer: **ack**, **timeout/retry** (keep a copy); a lost ack causes a duplicate; goal **exactly-once** via **sequence counter** (unique IDs would require unbounded memory); TIP on the value of the timeout and **exponential back-off** (OSTEP p.768-771). TCP is the most widely used reliable layer (p.771).
- **[from source]** Abstractions: **DSM** (distributed shared memory) via network page faults was abandoned (failures and unpredictable performance); **RPC** [BN84] with **stub generator** (marshaling/unmarshaling), server thread pool, run-time (names via host+port; transport: TCP generates two "extra" messages, so many RPCs use UDP with timeout/retry and **at-most-once**; long calls; fragmentation; **byte ordering** with XDR; asynchronous RPC) (OSTEP p.771-777). Aside: **end-to-end argument** (OSTEP p.776). Modern examples cited: gRPC and Thrift (p.777) **[DATED]**.

## 2. NFS (ch.49)

- **[from source]** Client: client-side file system + file server; NFSv2 goal: **simple and fast server crash recovery** (OSTEP p.795-796). Solution: **stateless protocol** (the server does not keep track of which files are open, offsets or caches); each request carries everything; shared state ("distributed state") complicates crash recovery (OSTEP p.797-798).
- **[from source]** **File handle** = volume ID + inode number + **generation number**; messages: GETATTR, SETATTR, LOOKUP, READ, WRITE, CREATE, REMOVE, MKDIR, RMDIR, READDIR; the client keeps fd → file handle and offset; one LOOKUP per path component; `close` does not talk to the server (OSTEP p.798-801).
- **[from source]** **Idempotency**: retry covers a lost request, a crashed server and a lost reply; MKDIR is an exception (TIP Voltaire's Law) (OSTEP p.802-804).
- **[from source]** Client caching and **cache consistency**: **update visibility** and **stale cache**; NFSv2 solutions: **flush-on-close (close-to-open)** and checking with **GETATTR**; **attribute cache** (~3 s) reduces GETATTR but makes it hard to know which version is being read (OSTEP p.804-806). The server **cannot** reply success to a WRITE before writing to stable storage (a/b/c example) (OSTEP p.806-808). **VFS/vnode** (Sun) allows several FSes in the same OS (OSTEP p.808). Initial security was weak; Kerberos came later (OSTEP p.809).

## 3. AFS (ch.50)

- **[from source]** Goal: **scale**; **whole-file caching** on local disk; Venus (client) and Vice (server); Fetch/Store/TestAuth; v1 problems: path traversal cost on the server and too many TestAuth calls; ~20 clients per server (OSTEP p.816-819). Lesson: Patterson's Law "measure then build" (p.818).
- **[from source]** **AFSv2**: **callbacks** (server promise to notify; cf. polling × interrupts) and **FID** (volume + file ID + uniquifier); the client walks the path and caches; ~50 clients per server (OSTEP p.819-821, p.824).
- **[from source]** Consistency: update visibility and invalidation happen together at **close()**; among processes on the same machine, writes appear immediately; with two clients writing, the last one to close wins and the file is entirely from one client (in NFS blocks could be mixed); **crash recovery** is more complex (suspect cache; in-memory callbacks; heartbeat) (OSTEP p.821-823).
- **[from source]** AFS × NFS comparison (Fig.50.4): re-reading a large file favors AFS (factor L_net/L_disk); overwriting and accessing a small part of a large file favor NFS (AFS fetches and returns the whole file) (OSTEP p.824-826). Other AFS features: global namespace, authentication, ACLs (OSTEP p.826-827). NFSv4 introduced server-side state (p.827).

## 4. What the book does NOT cover (mark [extrapolation])

Consensus (Paxos/Raft), CAP, logical clocks, replication, distributed transactions, HDFS/GFS/Ceph, QUIC/HTTP, TLS outside ch.57 (the text has "paxos" and "CAP theorem" absent; "raft" only as part of another word).
