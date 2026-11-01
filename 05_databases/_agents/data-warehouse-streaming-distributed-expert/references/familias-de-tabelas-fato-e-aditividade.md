# Fact Table Families and Additivity

> Convention: `(KIMBALL p.N)` = PDF page (printed = N − 3). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Fact table structure
[from source] A fact table contains the numeric measures produced by a real-world measurement event; at the lowest grain, one row corresponds to one event and vice versa. The design is based on the physical activity, not on future reports. There are always foreign keys to each associated dimension, plus (optional) degenerate dimension keys and date/time stamps. Fact tables are the main target of the dynamic computations and aggregations of queries (KIMBALL p.7).

## 2. Additivity
[from source] Numeric measures fall into three categories (KIMBALL p.7):
- **Fully additive**: summable across any dimension; the most flexible and useful.
- **Semi-additive**: summable across some dimensions, not all; balances are the common example, additive across all dimensions except time.
- **Non-additive**: for example ratios. A good approach, when possible: store the fully additive components and sum them before computing the final non-additive measure, a calculation normally done in the BI layer or the OLAP cube.

[inference] Percentage margin = sum of profit / sum of revenue is an example consistent with this rule; the book only cites "ratios". The book does **not** say how to aggregate semi-additive measures over time (average, last balance, etc.); that is general practice [extrapolation].

## 3. Nulls and fact conformance
- [from source] Nulls in *measures* are handled "gracefully" by SUM, COUNT, MIN, MAX and AVG. Foreign keys of the fact, however, cannot be null (they would violate referential integrity): the dimension must have a default row (with a surrogate key) for "unknown/not applicable" (KIMBALL p.7).
- [from source] Conformed facts: if the same measure appears in different fact tables, the technical definitions must be identical so they can be compared; if consistent, the same name; if incompatible, different names to warn users and applications (KIMBALL p.7).

## 4. The three basic grains and the other techniques
[from source] The document states that there are **three basic grains** of fact table: transactional, periodic snapshot and accumulating snapshot (KIMBALL p.20). Factless, aggregate and consolidated are additional techniques (KIMBALL p.8-9).

### Transactional
[from source] A row corresponds to a measurement event at a point in space and time. The atomic transactional grain is the most dimensional and expressive (it allows the maximum slicing and dicing). It can be dense or sparse, since rows exist only if a measurement occurred. It always has a foreign key to each dimension and, optionally, precise time stamps and degenerate keys; the facts must be consistent with the transactional grain (KIMBALL p.7).

### Periodic snapshot
[from source] A row summarizes many events that occurred in a standard period (day, week, month); the grain is the period, not the transaction. It usually has many facts. It is uniformly dense in its keys: even with no activity, a row with zero or null is generally inserted for each fact (KIMBALL p.8).

### Accumulating snapshot
[from source] A row summarizes the events at predictable steps between the beginning and the end of a process (a pipeline/workflow such as order fulfillment or claims processing). It has a date key for each critical milestone; the row (e.g. an order line) is inserted when the item is created and **revisited and updated** as the process advances, which is unique among the three types. It contains keys of other dimensions, optionally degenerate ones, and often lag measures and milestone completion counters (KIMBALL p.8).
- [from source] Lag/duration: instead of computing each interval from the dates, one lag per step measured from the start of the process is stored; any lag between two steps becomes a simple subtraction (KIMBALL p.18).

### Factless
[from source] Events without a numeric measure (e.g. a student attending a class) generate a fact row with only keys. They also allow analyzing what did **not** happen: the coverage table (all possibilities) minus the activity table (what occurred) (KIMBALL p.8).

### Aggregate / cube
[from source] Numeric rollups of the atomic data built only to speed up queries; they must be available to the BI layer at the same time as the atomic ones (open "aggregate navigation"); they must behave like indexes; they contain keys of "shrunken" conformed dimensions (KIMBALL p.8). Aggregate OLAP cubes are usually accessed directly by users (KIMBALL p.8).

### Consolidated
[from source] Combines facts from multiple processes in a single table when they can be expressed at the same grain (e.g. actual sales with forecasts), making actual vs. forecast analysis easier than building a drill-across application. It adds load to the ETL but relieves the BI; indicated for cross-process metrics that are frequently analyzed together (KIMBALL p.9).

## 5. Other fact techniques (summary)
- [from source] Fact surrogate key: optional; serves as a single-column PK, an immediate row identifier for ETL, lets an interrupted load be undone/resumed and lets updates be decomposed into inserts plus deletes (KIMBALL p.18).
- [from source] Header/line: bring all the header's keys and degenerate dimensions into the line fact; facts of a different grain (e.g. header freight) must be **allocated** to the lines by business rules (KIMBALL p.18-19).
- [from source] Multiple currencies: a pair of columns per fact (true currency and standard currency) plus a currency dimension; multiple units: store in the standard unit and conversion factors in the row itself (KIMBALL p.19). YTD: compute in the BI/cube layer, do not store (KIMBALL p.19).
- [from source] Timespan tracking: in isolated cases add effective date/expiration/current indicator to the fact (KIMBALL p.20). Late arriving facts: look up in the dimensions the keys valid on the event date (KIMBALL p.20).
- [from source] Measure type dimension (collapse into a generic fact) is generally **not** recommended, acceptable when there are hundreds of potential facts and few applicable per row (KIMBALL p.22). Facts as supertype/subtype ("core and custom") for heterogeneous products (KIMBALL p.24).

## Terms from the original (checked by tests/audit_tokens.py)
- `additive`, `semi-additive`, `non-additive`, `ratios`, `balance`, `conformed`, `surrogate` (KIMBALL p.7)
- `periodic`, `accumulating`, `factless`, `aggregate`, `navigation`, `coverage` (KIMBALL p.8)
- `consolidated`, `forecasts` (KIMBALL p.9)
