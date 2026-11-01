# Pat Helland: entities, data on the inside/outside and life beyond distributed transactions

> **Source absent from the corpus.** The file `05_databases/Life-Beyond-Distributed-Transactions.pdf` (4 pages) **is not** Helland's paper: it is the astrophysics paper "HD 30963: A new HgMn star" (Monier, Gebran, Royer; arXiv:1609.03542v1, SF2A 2016), checked in this audit on PDF pages 1-4. Therefore there is **no citable page** and **nothing here is `[from source]`**. All the content below is the model's general knowledge about Helland's thesis (*Life Beyond Distributed Transactions: An Apostate's Opinion*, 2007), labeled `[extrapolation]`, and **has not been verified** against the original text. Tell the user so and suggest obtaining the correct PDF before citing Helland precisely.
>
> Labels: `[extrapolation]` = external knowledge not verifiable in the corpus; `[inference]` is reserved for deductions made from passages read in KIMBALL/STREAM.

## 1. Entity as the unit of consistency [extrapolation]
General idea attributed to the thesis: in very large systems, atomic transactions work within an "entity" (a set of data that resides on a single node/scale unit and is not split), and work between entities is done by messages, without a distributed transaction. The similarity to the DDD *aggregate* is the agent's analogy [extrapolation].

## 2. Data on the inside vs. data on the outside [extrapolation]
Distinction attributed to Helland's work (the name comes from an earlier article on "data on the outside"): data *inside* (a service's private mutable state) vs. data *outside* (shared messages/representations, immutable and versioned). Details (immutability, versioning, "almost ordered") require checking the original source; package v1 presented them as facts.

## 3. Two-phase commit and availability [extrapolation]
The phrase "two-phase commit is the anti-availability protocol" is usually attributed to Helland. General engineering reasoning: 2PC holds locks while the coordinator/participants do not respond, reducing availability under failures and partitions. The relation to the CAP theorem is a classic argument, not from the STREAM survey nor from KIMBALL. Evidence *inside the corpus* for contrast: the STREAM survey presents two-phase commit **per epoch** as a Spark/S-Store technique, and points out the drawback of low utilization due to synchronous execution (STREAM p.15).

## 4. Living without 2PC [extrapolation]
- Idempotent receivers: handle duplicate messages (a concept connected to what the survey says about idempotent outputs for sinks, `[from source]` STREAM p.20, but there the context is streaming, not microservices).
- Compensation/Saga: the Saga pattern (Garcia-Molina and Salem, 1987) and compensating transactions are modern extensions; Helland speaks of coordination by messages, "tentative operations" and cancellation/confirmation; **do not confuse** with the later formulation of Saga/Outbox.
- Eventual consistency: common practice; the degree of acceptance depends on the business.

## 5. How to use this file
1. If the user asks "what does the book say", answer that the collection's PDF is not the work and that the content is general knowledge labeled `[extrapolation]`.
2. For a bridge to what is actually in the corpus: output commit problem and idempotent sinks (STREAM p.18-20), per-epoch commit (STREAM p.15), snapshots (STREAM p.15-16), `drill-across` instead of a join between facts (KIMBALL p.20).
3. `entity_boundary_auditor.py` is an `[extrapolation]` checklist, not derived from a page.
