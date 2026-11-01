# Dimension Techniques: Keys, Denormalization and Hierarchies

> Convention: `(KIMBALL p.N)` = PDF page (printed = N − 3). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Dimension structure
[from source] Every dimension has a single primary key column, embedded as a foreign key in the fact tables where the row's context is exactly correct. Dimensions are usually wide, flat, denormalized, with many low-cardinality textual attributes; the most powerful attributes are verbose descriptions. They are the main target of query constraints and groupings, and the report labels come from their values (KIMBALL p.10).

## 2. Surrogate, natural and durable keys
- [from source] The dimension's primary key must **not** be the operational system's natural key, because there will be several rows per natural key when changes are tracked over time; moreover, natural keys may come from several source systems, incompatible or poorly administered. The DW/BI must take control of the keys: create anonymous integer primary keys for every dimension, assigned in sequence starting at 1 whenever a new key is needed (KIMBALL p.10).
- [from source] The date dimension is exempt from the surrogate rule; being very predictable and stable, it can use a more meaningful key, such as a YYYYMMDD integer, which helps partitioning; it still needs a special row for unknown/to-be-determined dates, and filters and groupings must use the dimension's attributes, not the "smart key" (KIMBALL p.11).
- [from source] Natural keys are subject to business rules outside the DW's control (e.g. an employee number that changes when the person is rehired). A **durable** (supernatural) key is then created, persistent, in a format independent of the business process, preferably a sequential integer starting at 1. Several surrogates can exist for the same employee over time; the durable key never changes (KIMBALL p.10).
- [inference] Advantages such as "faster joins" or "byte savings" of integers are general database knowledge, **not** stated in the document; treat as [extrapolation]. The use of negative values (-1, -2) for "unknown" is a market convention; the book only asks for a default row with a surrogate (KIMBALL p.7).

## 3. Drilling down
[from source] Drill down = adding a row header to an existing query (an attribute of any dimension attached to the fact, added to the GROUP BY). It does not require predefined hierarchies or drill paths (KIMBALL p.10).

## 4. Degenerate dimension
[from source] A dimension with no content beyond its key: with multi-line invoices, the fact rows inherit the invoice's descriptive keys and the invoice number remains a valid key at the line grain. It is placed in the fact with the explicit acknowledgment that there is no dimension table; it is most common in transactional facts and accumulating snapshots (KIMBALL p.10-11).

## 5. Denormalization, hierarchies, flags and nulls
- [from source] Designers should resist the normalization impulses coming from years of operational databases and denormalize fixed-depth many-to-one hierarchies into attributes of a flattened dimension row; this serves the "twin goals" of simplicity and speed (KIMBALL p.11).
- [from source] A dimension can have several natural hierarchies (e.g. date with day-week-fiscal period and day-month-year) coexisting in the same table (KIMBALL p.11).
- [from source] Cryptic abbreviations, true/false flags and operational indicators should be supplemented with full words; codes with embedded meaning should be broken into separate descriptive attributes (KIMBALL p.11).
- [from source] Null attributes in dimensions: replace with descriptive text such as "Unknown" or "Not Applicable", since databases handle nulls in grouping/filtering inconsistently (KIMBALL p.11).
- [from source] The calendar dimension is attached to virtually every fact; the book says Easter is looked up in the dimension, not computed in SQL; an additional date/time stamp goes in the fact as a standalone column; if users constrain by time of day, a time-of-day dimension is added (KIMBALL p.11).

## 6. Snowflake and outrigger
- [from source] Snowflaking = normalizing dimension hierarchies into secondary tables, forming a multilevel structure. The book says it should be **avoided**: it is hard for users to understand and navigate and can hurt performance; the flattened dimension contains exactly the same information (KIMBALL p.12).
- [from source] Outrigger = a dimension that references another (e.g. a bank account referencing the opening date); allowed, but sparingly; in most cases the correlation should be pushed down to the fact, with the two dimensions as separate keys (KIMBALL p.12). An outrigger with type 2 can cause explosive growth of the base dimension (KIMBALL p.21).
- [from source] The book does **not** classify the snowflake as obsolete/legacy nor quantify the space savings; use `[DATED]` only for what is technology of its time, not for this point.

## 7. Hierarchies (fixed depth, variable)
- [from source] Fixed depth: a series of many-to-one relationships with agreed-upon level names; the levels appear as separate positional attributes; it is the easiest to understand and gives predictable performance (KIMBALL p.17).
- [from source] Slightly ragged: a small variation in depth (e.g. geographic with 3 to 6 levels) can be fitted into a fixed positional design with columns for the maximum number of levels (KIMBALL p.17).
- [from source] Ragged of indeterminate depth: hard to model and query in SQL; solution: a **bridge** table with one row for each possible path, or alternatively a **pathstring** attribute, which does not allow quick substitution of alternate hierarchies nor shared ownership and may require relabeling if the structure changes (KIMBALL p.17).

## 8. Advanced dimension techniques (summary)
- [from source] Multivalued dimension: linked to the fact by a group key and a bridge table with one row per group item; if based on type 2, the bridge must have effective/expiration dates and the query must fix a point in time (KIMBALL p.21).
- [from source] Study groups (a table with only the durable keys of the result of complex analyses) (KIMBALL p.21-22); aggregated facts as dimension attributes, in bands (KIMBALL p.22); dynamic value banding (band dimension or CASE; the dimension tends to perform better) (KIMBALL p.22); comments in their own dimension; multiple time zones with two keys to role-playing date dimensions (KIMBALL p.22).
- [from source] Abstract/generic dimensions (e.g. a single "location" for store, warehouse and customer) should be **avoided**; hot swappable dimensions; audit dimension with ETL metadata and quality indicators; late arriving dimensions (placeholder rows updated by type 1; retroactive type 2 changes require a new row and re-presenting facts) (KIMBALL p.23).
- [from source] Real-time fact tables ("hot partition" in memory, without aggregations and indexes) and error event schemas (KIMBALL p.24).

## Terms from the original (checked by tests/audit_tokens.py)
- `surrogate`, `durable`, `supernatural`, `anonymous`, `drilling`, `degenerate` (KIMBALL p.10)
- `denormalized`, `hierarchies`, `YYYYMMDD`, `Unknown`, `flags` (KIMBALL p.11)
- `snowflakes`, `outrigger`, `sparingly` (KIMBALL p.12)
- `pathstring`, `ragged`, `bridge` (KIMBALL p.17)
