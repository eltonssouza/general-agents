# Special Dimensions: Role-Playing, Junk and Degenerate

> Convention: `(KIMBALL p.N)` = PDF page (printed = N − 3). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Role-playing
[from source] A single physical dimension can be referenced several times in the same fact, each reference tied to a logically distinct **role** (e.g. several date fields pointing to the date dimension). It is essential that each foreign key point to a separate *view* of the dimension (with unique column names), so that the references are independent; these views are the roles (KIMBALL p.12).
- [inference] Agent's example: order, payment, shipping and delivery dates pointing to the same date dimension, via views; the document only speaks of "several dates" (KIMBALL p.12).
- [from source] The same mechanism appears for time zones: two keys to role-playing date (and time-of-day) dimensions, one in universal time and the other local (KIMBALL p.22).

## 2. Junk dimension
[from source] Transactional processes generate assorted low-cardinality flags and indicators. Instead of one dimension per flag, **one** junk dimension is created (often called a *transaction profile dimension*). It does not need to be the Cartesian product of all possible values; it contains only the combinations that **actually occur** in the source data (KIMBALL p.12).
- [from source] Embedding many foreign keys to low-cardinality dimensions in the fact, instead of a junk dimension, is one of the causes of a **centipede fact table** (KIMBALL p.18).
- [inference] Examples of flags (payment method, gift wrapping) are the agent's illustrations.

## 3. Degenerate dimension
[from source] A dimension that has only the key: e.g. an invoice number with several lines; it remains as a key at the line level, placed in the fact with no associated dimension table. Most common in transactional facts and accumulating snapshots (KIMBALL p.10-11).
- [inference] Order numbers, tax invoices and support tickets are examples of the same pattern (the book cites the invoice).

## 4. Other dimensions cited in the document (for completeness)
- [from source] Step dimension: indicates which step of a session (e.g. web page events) the row is at and how many steps remain (KIMBALL p.22-23).
- [from source] Audit dimension: ETL metadata (code version, timestamps, quality indicators) useful for compliance (KIMBALL p.23).
- [from source] Hot swappable: the same fact paired alternately with different copies of the same dimension (e.g. stock quotes with proprietary attributes per investor) (KIMBALL p.23).

## Terms from the original (checked by tests/audit_tokens.py)
- `role-playing`, `roles`, `junk`, `Cartesian`, `profile` (KIMBALL p.12)
