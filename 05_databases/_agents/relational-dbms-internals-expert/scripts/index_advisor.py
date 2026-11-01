# -*- coding: utf-8 -*-
"""
index_advisor.py - heuristic for choosing an index type in PostgreSQL 16.

RULE ORIGINS (pages = PDF of the PG16 16.15 manual; printed = PDF - 38):
  R0  B-tree is the CREATE INDEX default and handles < <= = >= >, BETWEEN, IN, IS NULL         [from source] PG16 p.468
  R1  Only B-tree returns sorted data (ORDER BY without a sort) and only B-tree can be UNIQUE [from source] PG16 p.469, p.471, p.473
  R2  GIN: multi-component values (arrays, JSONB, tsvector)                                   [from source] PG16 p.470, p.223-225, p.484-485
  R3  GiST: geometries, ranges, nearest neighbor (<->)                                        [from source] PG16 p.469, p.2515-2517
  R4  BRIN: very large tables strongly correlated with physical order; per-range summaries    [from source] PG16 p.470, p.2552
  R5  Hash: '=' only, one column, no uniqueness; smaller than B-tree for long keys            [from source] PG16 p.469, p.2565
  R6  INCLUDE/index-only scan: B-tree, GiST and SP-GiST; depends on the visibility map        [from source] PG16 p.477-478
  X1  "Very large table" threshold for BRIN (default 10 GB, adjustable via --brin-min-gb)     [extrapolation] (the manual gives no number)
  X2  Priority order among the rules when more than one applies                               [inference]
Nothing here proves the index is the best one: confirm with EXPLAIN ANALYZE and real data (PG16 p.481-482).
No network; read-only.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

CMP_OPS = {"<", ">", "<=", ">=", "=", "between"}
GIN_OPS = {"@>", "<@", "@@", "?", "?|", "?&", "@?"}
GIST_OPS = {"&&", "&<", "&>", "<<", ">>", "<->", "-|-"}


def advise_index(data_type, operators, physical_correlation, table_size_gb,
                 brin_min_gb=10.0, equality_only=False, unique=False, need_order=False):
    ops = [o.strip().lower() for o in operators.split(",") if o.strip()]
    notes = []
    # R1: uniqueness or ordering forces B-tree
    if unique or need_order:
        why = "UNIQUE" if unique else "ORDER BY without a sort"
        return {
            "index_type": "B-tree",
            "origin": "[from source] PG16 p.469, p.471, p.473 (rule R1)",
            "pages": "PG16 p.468-469, p.471, p.473",
            "justification": "%s: only B-tree offers this among the built-in types." % why,
            "ddl_example": "CREATE %sINDEX idx_t_c ON tbl (col);" % ("UNIQUE " if unique else ""),
            "notes": notes,
        }
    # R2/R3 by data type
    if data_type in ("jsonb", "array", "fulltext"):
        notes.append("JSONB: jsonb_path_ops is usually smaller and more specific, but it only supports @>, @? and @@ and does not find isolated keys (PG16 p.223-225).")
        notes.append("GIN does not support index-only scan (PG16 p.477); fast update accumulates insertions in a pending list (PG16 p.2549).")
        notes.append("For full-text search, GiST (tsvector_ops) also exists (PG16 p.2517).")
        return {
            "index_type": "GIN",
            "origin": "[from source] PG16 p.470 (rule R2)",
            "pages": "PG16 p.470, p.223-225, p.484-485, p.2545",
            "justification": "Multi-component value (%s): GIN stores one entry per component." % data_type,
            "ddl_example": "CREATE INDEX idx_t_doc ON tbl USING gin (doc jsonb_path_ops);" if data_type == "jsonb"
            else "CREATE INDEX idx_t_c ON tbl USING gin (col);",
            "notes": notes,
        }
    if data_type in ("spatial", "range"):
        notes.append("GiST orders by distance only in operator classes that declare an ordering operator (PG16 p.469).")
        notes.append("Multicolumn GiST loses effectiveness if the first column has few distinct values (PG16 p.471).")
        return {
            "index_type": "GiST",
            "origin": "[from source] PG16 p.469 (rule R3)",
            "pages": "PG16 p.469, p.2515-2517",
            "justification": "Geometric data or ranges: GiST has operator classes for them (box_ops, circle_ops, range_ops...).",
            "ddl_example": "CREATE INDEX idx_t_geo ON tbl USING gist (col);",
            "notes": notes,
        }
    # operators as a hint (type 'scalar' or 'temporal_log')
    if set(ops) & GIST_OPS and not (set(ops) & CMP_OPS):
        return {
            "index_type": "GiST (candidate)",
            "origin": "[inference] from the given operators (rule R3)",
            "pages": "PG16 p.469, p.2515-2517",
            "justification": "Operators %s appear in the GiST classes; confirm the data type (geometry/range)." % sorted(set(ops) & GIST_OPS),
            "ddl_example": "CREATE INDEX idx_t_c ON tbl USING gist (col);",
            "notes": ["For arrays, '&&' is a GIN operator (PG16 p.470): pass --data-type array if that applies."],
        }
    if set(ops) & GIN_OPS:
        return {
            "index_type": "GIN (candidate)",
            "origin": "[inference] from the given operators (rule R2)",
            "pages": "PG16 p.470, p.223-225, p.2545",
            "justification": "Operators %s are indexable by GIN; '@>' also exists in GiST (ranges): confirm the data type." % sorted(set(ops) & GIN_OPS),
            "ddl_example": "CREATE INDEX idx_t_c ON tbl USING gin (col);",
            "notes": [],
        }
    # R4 BRIN
    if physical_correlation and table_size_gb >= brin_min_gb and (set(ops) & CMP_OPS):
        notes.append("The %.1f GB threshold is [extrapolation] (X1); the manual only says 'very large tables' with physical correlation (PG16 p.2552)." % brin_min_gb)
        notes.append("BRIN is 'lossy': it returns all tuples of the matching ranges and the executor rechecks them (PG16 p.2552).")
        notes.append("pages_per_range default 128; new ranges only get a summary after VACUUM or summarize (PG16 p.1758, p.2552).")
        return {
            "index_type": "BRIN",
            "origin": "[from source] PG16 p.470, p.2552 (rule R4) + [extrapolation] threshold (X1)",
            "pages": "PG16 p.470, p.2552-2553, p.1758",
            "justification": "%.1f GB table with values correlated with physical order (e.g., insertion date)." % table_size_gb,
            "ddl_example": "CREATE INDEX idx_t_data_brin ON tbl USING brin (event_date);",
            "notes": notes,
        }
    if physical_correlation and not (table_size_gb >= brin_min_gb):
        notes.append("There is physical correlation, but the table (%.1f GB) is below the BRIN threshold (%.1f GB, [extrapolation]); B-tree is the safe choice." % (table_size_gb, brin_min_gb))
    # R5 hash
    if equality_only:
        notes.append("Hash: '=' only, one column, does not check uniqueness, lossy scans; does not shrink without REINDEX (PG16 p.2565).")
        notes.append("When in doubt, B-tree also serves equality (PG16 p.468).")
        return {
            "index_type": "Hash (candidate)",
            "origin": "[from source] PG16 p.469, p.2565 (rule R5)",
            "pages": "PG16 p.469, p.2565-2566",
            "justification": "Equality-only queries; hash stores only 4 bytes per tuple and can be smaller than B-tree for UUIDs and URLs.",
            "ddl_example": "CREATE INDEX idx_t_c_hash ON tbl USING hash (col);",
            "notes": notes,
        }
    notes.append("Multicolumn: efficient with restrictions on the leading columns; avoid going beyond three columns (PG16 p.471).")
    notes.append("For index-only scan, consider INCLUDE (B-tree/GiST/SP-GiST) and keep the visibility map up to date (PG16 p.477-478).")
    return {
        "index_type": "B-tree",
        "origin": "[from source] PG16 p.468 (rule R0)",
        "pages": "PG16 p.468-469",
        "justification": "CREATE INDEX default; serves equality, range, BETWEEN, IN and IS NULL on sortable data, and anchored LIKE (with a suitable operator class outside the C locale, PG16 p.468, p.480).",
        "ddl_example": "CREATE INDEX idx_t_c ON tbl (col);",
        "notes": notes,
    }


def main():
    ap = argparse.ArgumentParser(description="Heuristic for choosing an index in PostgreSQL 16 (see the rule origins in the script header)")
    ap.add_argument("--data-type", default="scalar", choices=["scalar", "jsonb", "array", "fulltext", "spatial", "range", "temporal_log"])
    ap.add_argument("--operators", default="=,<,>,between", help="most-used operators, comma-separated (e.g., '=,between', '@>', '<->')")
    ap.add_argument("--physical-correlation", action="store_true", help="values correlated with physical order (append-only)")
    ap.add_argument("--table-size-gb", type=float, default=1.0)
    ap.add_argument("--brin-min-gb", type=float, default=10.0, help="size threshold [extrapolation] for suggesting BRIN")
    ap.add_argument("--equality-only", action="store_true", help="queries only use '=' (enables the Hash candidate)")
    ap.add_argument("--unique", action="store_true", help="needs a UNIQUE index")
    ap.add_argument("--need-order", action="store_true", help="needs ORDER BY without a sort")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = advise_index(a.data_type, a.operators, a.physical_correlation, a.table_size_gb,
                     a.brin_min_gb, a.equality_only, a.unique, a.need_order)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    print("=" * 68)
    print("INDEX RECOMMENDATION (PostgreSQL 16.15; pages = PDF; printed = PDF-38)")
    print("=" * 68)
    print("Recommended type : %s" % r["index_type"])
    print("Rule origin      : %s" % r["origin"])
    print("Pages            : %s" % r["pages"])
    print("Justification    : %s" % r["justification"])
    print("DDL example      : %s" % r["ddl_example"])
    for n in r["notes"]:
        print("Note             : %s" % n)
    print("Warning          : heuristic; confirm with EXPLAIN ANALYZE and real data (PG16 p.481-482).")
    print("Warning [from source]: EXPLAIN ANALYZE runs the command; for UPDATE/DELETE use BEGIN; ...; ROLLBACK; (PG16 p.550-551).")
    print("Warning [from source]: poor estimates with correlated columns: see CREATE STATISTICS + ANALYZE (PG16 p.555-557).")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
