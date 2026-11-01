# Slowly Changing Dimensions (SCD types 0 to 7)

> Convention: `(KIMBALL p.N)` = PDF page (printed = N − 3). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Types 0 to 7 are on KIMBALL p.15-16. The business examples here are the agent's, unless indicated.

## Type 0: retain original
[from source] The attribute value never changes; facts always group by the original value. Appropriate for attributes labeled "original" (e.g. the customer's original credit score), durable identifiers and most attributes of a date dimension (KIMBALL p.15).

## Type 1: overwrite
[from source] The old value is overwritten; the attribute always reflects the most recent assignment and therefore **destroys history**. It is easy to implement and creates no rows, but the aggregate fact tables and OLAP cubes affected by the change must be **recalculated** (KIMBALL p.15).

## Type 2: new row
[from source] A new row is added to the dimension with the updated values. This requires generalizing the primary key beyond the natural/durable key, since there will be several rows per member. When the new row is created, a new surrogate is assigned, used as the foreign key in all facts from the moment of the change until the next change. The book recommends **at least three** additional columns: (1) row effective date/time, (2) expiration date/time, (3) current row indicator (KIMBALL p.15).
- [extrapolation] The value "9999-12-31" for an open expiration and the two-statement SQL flow (expire and insert) are common ETL conventions; they are **not** in the document. The same goes for calling type 2 the "queen technique".

## Type 3: new attribute
[from source] An attribute is added to preserve the old value; the new value overwrites the main attribute as in type 1. It is sometimes called "alternate reality": the user groups and filters by the current value or by the alternate reality. It is used **relatively little** (KIMBALL p.15).

## Type 4: mini-dimension
[from source] Used when a group of attributes of a dimension changes rapidly and is split off into a mini-dimension (a situation called a "rapidly changing monster dimension"). Heavily used attributes in dimensions with millions of rows are also candidates, even if they do not change frequently. The mini-dimension has its own key, and the keys of the base and of the mini are both in the fact (KIMBALL p.15).

## Type 5: mini-dimension + type 1 outrigger
[from source] Preserves historical values accurately and allows reporting historical facts by current values. It starts from type 4 and embeds in the base dimension a *current* type 1 reference to the mini-dimension, making it possible to access the current mini attributes without going through the fact. Logically the base and the mini-outrigger are presented as a single table; the ETL must overwrite the type 1 reference when the current assignment changes (KIMBALL p.15-16).

## Type 6: type 1 attributes in a type 2 dimension
[from source] Also delivers historical and current values. It starts from type 2 and embeds *current* (type 1) versions of the same attributes in the row, so that facts can be filtered or grouped by the type 2 value valid at the time of the measurement or by the current value. The type 1 attribute is systematically overwritten in **all** rows tied to the same durable key when updated (KIMBALL p.16).
- [extrapolation] The mnemonic "1+2+3=6" is community folklore; the document does **not** include it nor mention a type 3 component in type 6.

## Type 7: dual type 1 and type 2
[from source] The final hybrid for as-was and as-is reporting. The fact is accessed through a dimension modeled at the same time as type 1 (only the most recent values) and type 2 (correct historical profiles). Both the durable key and the surrogate go in the fact. Type 1 perspective: restrict on the current indicator and join by the durable key; type 2 perspective: do not restrict on the indicator and join by the surrogate. The two perspectives are deployed as separate views (KIMBALL p.16).

## Other changes related to SCD
- [from source] Late arriving dimensions: when the dimensional context arrives after the fact, special rows are created with natural keys not yet resolved, later updated by type 1; retroactive changes to type 2 attributes require inserting a new row and **re-presenting** the associated facts (KIMBALL p.23).
- [from source] In dimensions with a type 2 outrigger, a change in the outrigger forces type 2 processing on the base, with explosive growth; alternative: bring the outrigger key into the fact (KIMBALL p.21).
- [from source] Timespan tracking in facts (effective/expiration/current), as in type 2, for cases such as slowly changing inventory balances (KIMBALL p.20).

## Terms from the original (checked by tests/audit_tokens.py)
- `overwritten`, `destroys`, `effective`, `expiration`, `alternate`, `monster`, `mini-dimension` (KIMBALL p.15)
- `durable`, `as-was`, `as-is`, `views` (KIMBALL p.16)
