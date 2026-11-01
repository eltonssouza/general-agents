# Fact-to-Fact Join, Multipass SQL and Centipede

> Convention: `(KIMBALL p.N)` = PDF page (printed = N − 3). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. "Golden rule" is a package label, not a term of the document.

## 1. Multipass SQL and the prohibition of joins between facts
[from source] A BI application should **never** issue SQL that joins two fact tables on their foreign keys: it is impossible to control the cardinality of the answer set of such a join in a relational database, and incorrect results will be returned to the BI tool. The book's example: facts of shipments and returns by customer and product must not be joined directly; instead, the **drilling across** technique is used: each answer is produced separately and the results are merged by sort-merge on the common value of the row headers (KIMBALL p.20).

- [inference] When the package shows that "3 purchases x 2 returns = 6 rows", it is an arithmetic illustration by the agent; the book only says that the cardinality is uncontrollable.
- [extrapolation] The SQL pattern of two subqueries aggregated by a conformed attribute with a `FULL OUTER JOIN` (or CTEs) to do the merge is a common implementation; the book names the technique "multipass"/"stitch" and speaks of sort-merge (KIMBALL p.13, p.20).

```sql
-- [extrapolation] illustrative example (fictitious schema)
SELECT COALESCE(v.categoria, d.categoria) AS categoria,
       COALESCE(v.receita, 0) AS receita,
       COALESCE(d.devolvido, 0) AS devolvido
FROM (SELECT p.categoria, SUM(f.valor) AS receita
      FROM fato_vendas f JOIN dim_produto p ON p.produto_key = f.produto_key
      GROUP BY p.categoria) v
FULL OUTER JOIN
     (SELECT p.categoria, SUM(f.valor) AS devolvido
      FROM fato_devolucoes f JOIN dim_produto p ON p.produto_key = f.produto_key
      GROUP BY p.categoria) d
  ON v.categoria = d.categoria;
```

## 2. Centipede fact table
[from source] It results from normalizing each level of a many-to-one hierarchy into separate dimensions (e.g. day, month, quarter and year dimensions) and putting all the keys in the fact, producing dozens of hierarchically related dimensions. It **must be avoided**: collapse the fixed-depth hierarchical dimensions back to the lowest grain (in the example, the date). Centipedes also appear when several keys to low-cardinality dimensions are embedded instead of creating a junk dimension (KIMBALL p.18).

## 3. Other usage rules in the document
- [from source] Generic abstract dimensions should be avoided (KIMBALL p.23); snowflakes should be avoided (KIMBALL p.12); YTD measures should be computed in the BI layer (KIMBALL p.19); facts of a different grain should be allocated to the lines, and the profit and loss table is usually deferred from the initial phases because it requires cost allocation (KIMBALL p.19).
- [from source] "Never"/"must": the text uses categorical language only in the prohibition of the join between facts (KIMBALL p.20) and in "different grains must not be mixed" (KIMBALL p.5); the other guidance is "should"/"avoid"/"recommend".

## Terms from the original (checked by tests/audit_tokens.py)
- `drilling`, `sort-merged`, `cardinality` (KIMBALL p.20)
- `centipede`, `junk` (KIMBALL p.18)
