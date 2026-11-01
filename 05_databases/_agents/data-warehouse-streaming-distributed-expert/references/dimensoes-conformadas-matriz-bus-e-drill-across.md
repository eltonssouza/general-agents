# Conformed Dimensions, Bus Matrix and Drill-Across

> Convention: `(KIMBALL p.N)` = PDF page (printed = N − 3). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Conformed dimensions
- [from source] Dimensions **conform** when attributes of distinct tables have the same column names and domain contents. With a conformed attribute as the row header (grouping column), the results of distinct facts line up on the same rows of a drill-across report; this is the essence of integration in an enterprise DW/BI. They are defined once, in collaboration with data governance, and reused, bringing analytical consistency and lower development cost (KIMBALL p.13).
- [from source] **Shrunken rollup dimensions**: conformed dimensions that are a subset of rows and/or columns of a base dimension. They are needed for aggregate fact tables and for processes that capture data at a higher level (the book exemplifies forecast by month and brand, instead of date and product). It also occurs when two dimensions have the same level of detail and one is a subset of the rows (KIMBALL p.13).

## 2. Drilling across
[from source] It consists of running separate queries against two or more fact tables whose row headers are identical conformed attributes; the results are aligned by a **sort-merge** operation on the common header values. BI tools call the function "stitch" or "multipass query" (KIMBALL p.13). This is the alternative to a direct join between facts (see `regras-de-ouro-e-multipass-sql-kimball.md`, KIMBALL p.20).

[extrapolation] Implementing the final alignment with a `FULL OUTER JOIN` between two aggregated subqueries is a common form in SQL; the document speaks of sort-merge, not of an outer join.

## 3. Value chain and bus
- [from source] **Value chain** = the natural flow of the organization's main processes (e.g. retail: purchasing, warehousing, sales; general ledger: budget, commitments, payments). Each process, with its own metrics, intervals, granularity and dimensionality, generates at least one atomic fact (KIMBALL p.13).
- [from source] **Bus architecture**: an incremental approach to building the enterprise DW/BI; it breaks the planning into manageable pieces, focusing on business processes, and delivers integration through standardized, reused conformed dimensions. In implementation it corresponds to the rows of the bus matrix. It is independent of technology/platform: relational and OLAP structures can participate (KIMBALL p.13).

## 4. Bus matrix
- [from source] An essential tool for designing and communicating the bus architecture: **rows = business processes; columns = dimensions**; shaded cells indicate that the dimension is associated with the process. Reading each row tests whether the candidate dimension is well defined for the process; reading each column shows where the dimension must be conformed across processes. It also serves to prioritize projects with management: implement **one row of the matrix at a time** (KIMBALL p.14).
- [from source] The **detailed implementation** matrix expands each process into specific facts/cubes, where the grain and the list of facts are documented (KIMBALL p.14).
- [from source] **Opportunity/stakeholder matrix**: swaps the dimension columns for business functions (marketing, sales, finance); it helps define which groups to invite to the design sessions for each process (KIMBALL p.14).

## 5. Examples
[inference] Bus matrix tables with processes such as "Retail Sales", "Inventory" and "Billing" and dimensions "Date/Customer/Product" are the agent's didactic examples, not the document's. The book does not say that a monolithic 3NF model "does not achieve integration"; it says that integration comes from conformed dimensions.

## Terms from the original (checked by tests/audit_tokens.py)
- `conformed`, `shrunken`, `sort-merge`, `stitch`, `multipass`, `bus` (KIMBALL p.13)
- `matrix`, `opportunity`, `stakeholder` (KIMBALL p.14)
