# BASE × ACID, eventual consistency and versioning

Convention: `(SIGLA p.N)` = PDF page (see INDEX). Sources: STRAUCH (~2010-2011) and NEO4J-GDB (2015).

## 1. ACID × BASE
- BASE, according to Brewer, gives up the consistency and isolation of ACID in favor of "availability, graceful degradation and performance". The letters: *basically available*, *soft-state*, *eventual consistency* `[from source]` (STRAUCH p.35).
- Summary by Ippolito: the application works practically all the time (BA), does not need to be consistent all the time (soft-state) and will be in some known state eventually (EC) `[from source]` (STRAUCH p.35).
- Brewer treats ACID and BASE as a **spectrum**, not as mutually exclusive alternatives `[from source]` (STRAUCH p.35). The comparison table (ACID: strong consistency, isolation, commit focus, conservative/pessimistic, hard evolution; BASE: weak consistency, "stale data OK", availability first, optimistic, simpler and faster) is in STRAUCH p.36.
- NEO4J-GDB, Appendix A: defines the ACID properties (atomic, consistent, isolated, durable), notes that ACID requires locks and may cause logical unavailability, and describes BASE (basic availability, soft-state, eventual consistency) as an optimistic strategy; stresses that the developer needs to know the BASE behavior of their database `[from source]` (NEO4J-GDB p.213-214). It also records that there are document databases with ACID (e.g. RavenDB) and graph databases with ACID (p.213, note 8).
- The attribution to "Dan Pritchett" appears only in the list of suggested readings ("BASE: An Acid Alternative", STRAUCH p.127); the text attributes BASE to Brewer.

## 2. Strict × eventual consistency
Lipcon (cited): consistency is "a continuum with trade-offs" that determines visibility rules and the apparent order of updates `[from source]` (STRAUCH p.36).
- **Strict**: every read returns the data of the last completed write, on any replica; requires reads and writes to occur on the same node or a distributed transaction protocol (2PC, Paxos); according to CAP, it cannot be obtained together with availability and partition tolerance (STRAUCH p.36).
- **Eventual**: readers will see the writes over time; "in steady state" the system returns the last written value; clients may see inconsistent state during updates in progress (STRAUCH p.36).
- Additional guarantees cited (STRAUCH p.36): *Read Your Own Writes* (the client sees its own updates even when reading from another server; others' updates are not instantaneous), *Session Consistency* (RYOW limited to a session, normally on one server), *Casual* (spelling as in the text; if the client reads version x and writes y, whoever reads y also sees x) and *Monotonic Read* (the client only sees newer versions on future reads).
- Ho: eventual is useful when concurrent updates to the same partition are unlikely and when clients do not depend on immediately reading their own updates (STRAUCH p.37).
- **Not covered**: *Monotonic Write Consistency*. The "time travel on F5" and "UPDATE before INSERT" examples from v1 are `[extrapolation]`.

## 3. Versioning in distributed scenarios (STRAUCH p.37-41)
When data is read and changed on several nodes without a distributed transaction, the book compares:
- **Timestamps**: depend on synchronized clocks and do not capture causality (p.37).
- **Optimistic locking** with a per-item counter: the Voldemort team observes that it works poorly in dynamic scenarios and requires total order (p.37).
- **Vector clocks**: a tuple of clocks, one per node; update rules (local increment, send, merge by maximum) and (partial) comparison; if neither dominates the other, there is a conflict of concurrent updates, to be resolved, for example, in the application (p.37-38). Advantages: they do not depend on synchronized clocks or total order, and do not require storing several revisions on all nodes (p.39).
- **Multiversion storage**: a timestamp per cell; allows reading "the most recent version before T" and snapshots (p.37).
- Propagation by **gossip** in a **state transfer** or **operation transfer** model (p.39-41): in gossip with n nodes, state takes O(log n) rounds to spread, so there is only eventual consistency (p.39).
- In Dynamo: the system is "always writable"; conflicting versions are reconciled on read by the application (semantic reconciliation) or by simple policies such as *last write wins* (p.58, 60).

## 4. What the sources do not say
That BASE "was formulated by Pritchett" in the body of the text; that "soft state" follows specifically from "gossip or anti-entropy" (STRAUCH's text links gossip to vector clocks and membership, p.39, 62); finite convergence windows with a time guarantee.
