# Modeling trees and hierarchies in SQL (Naive Trees)

> **Source coverage: the excerpt of the "Naive Trees" chapter (ANTI-TREE, an 11-page PDF) ends at section 3.4 ("Legitimate Uses of the Antipattern") and does NOT include section 3.5 "Solution: Use Alternative Tree Models".** Only the table of contents (ANTI-TOC p.5) shows that this section exists. Therefore Path Enumeration, Nested Sets and Closure Table **are not described in any source of this package**; what appears below about them is `[extrapolation]`, and v1 wrongly presented them as `[from source] (ANTI-TREE p.4-11)`.
> Pages = PDF; in ANTI-TREE the printed numbering coincides with the PDF's (page 6 shows "6"). The numbering of ANTI-TOC and ANTI-INT differs (see `INDEX.md`).

## 1. The problem and the antipattern [from source]
- **Scenario**: a news site with comments that reply to one another; the naive solution is for each comment to reference the comment it replies to. It is hard to retrieve a long chain of replies in a single query: you only get the immediate children or, with joins, up to a fixed depth; threads have unlimited depth; fetching all the comments to assemble the tree in application memory is impractical for millions of comments (ANTI-TREE p.5).
- **Objective** of the chapter: store and query hierarchies; terminology: node, child, parent, root, leaf, non-leaf nodes; examples: org chart and threaded discussion (ANTI-TREE p.5-6).
- **Antipattern "Always Depend on One's Parent"**: add a `parent_id` column that references another row of the same table, possibly with a *foreign key*; this design is called **Adjacency List** and is "probably the most common" (ANTI-TREE p.6).
- **Why it fails**: it cannot do the most common task on a tree, "query all descendants", without a recursive query; each level requires another JOIN and the number of JOINs in an SQL query is fixed; the four-level example does not reach beyond the fourth; aggregates such as `COUNT()` become hard; rebuilding the tree in the application copies a huge volume of data (ANTI-TREE p.7-8).
- **Maintenance**: inserting a leaf and moving a node/subtree (changing `parent_id`) is easy; **deleting** is more complex: to delete a subtree you must find the descendants and remove them bottom-up because of the *foreign key*; `ON DELETE CASCADE` automates this if you always want to delete descendants; to promote the children of a non-leaf node, first change the children's `parent_id` and then delete the node (ANTI-TREE p.9).
- **How to recognize it**: questions such as "how many levels do we need to support?", "I'm afraid to touch the code that manages the tree", "I need to run a periodic script to clean up orphan rows" (ANTI-TREE p.10).
- **Legitimate uses**: the Adjacency List's strength is getting a node's parent or direct children and inserting rows; if that is enough, it can do; "don't over-engineer" (the anecdote of the inventory that never needed deep trees) (ANTI-TREE p.10-11).
- **Recursive queries**: SQL-99 defines the recursive syntax with `WITH` and a common table expression; at the time of the book, SQL Server 2005, Oracle 11g, DB2 and PostgreSQL 8.4 supported it; MySQL, SQLite and Informix did not; Oracle has the proprietary syntax `START WITH ... CONNECT BY PRIOR`; the author expects the recursive syntax to become widespread and then "using Adjacency List will not be so limiting" (ANTI-TREE p.11). [DATED]: the product list is from 2010 (version P3.0 of 2012).
- Chapter anatomy: Objective, The Antipattern, How to Recognize It, Legitimate Uses and **Solution** (ANTI-INT p.8-9). The Solution of chapter 3 is called "Use Alternative Tree Models" (ANTI-TOC p.5).

## 2. PostgreSQL 16: recursive queries [from source]
PG16 supports `WITH RECURSIVE`: a non-recursive term, `UNION [ALL]` and a recursive term that refers to its own result; it is "typically used for hierarchical or tree-structured data"; **internally it is evaluated iteratively** with a working table (PG16 p.174-175). There is depth-first/breadth-first ordering by computed columns or by the `SEARCH DEPTH|BREADTH FIRST` syntax, and cycle detection by a path array or the `CYCLE` clause (PG16 p.175-178). The `ltree` type (additional module) represents label paths in a tree and offers search operators (PG16 p.2864).

## 3. [extrapolation] Alternatives to the Adjacency List (outside the excerpt)
General modeling knowledge; **verify in the full book before attributing to Karwin**:
- **Path Enumeration** (materialized path): each node stores the path of ancestors as text; subtree by path prefix; referential integrity is not enforced by the database and moving a subtree requires rewriting paths.
- **Nested Sets**: each node stores two numbers (left/right bounds); subtree by interval; inserting or moving requires renumbering many rows.
- **Closure Table**: an auxiliary table with (ancestor, descendant, depth) pairs; subtree queries without recursion and integrity through foreign keys; higher storage cost.
- In PostgreSQL, recursion (`WITH RECURSIVE`, PG16 p.174) and `ltree` (PG16 p.2864) are native alternatives to all of these.
The heuristic of the `tree_evaluator.py` script for recommending among these models is also `[extrapolation]` (declared in the script's output).

## 4. [inference]
Given that the book admits the Adjacency List "can work well" if only the parent/direct children are needed (p.10) and that standard recursive queries exist in several products (p.11), **and** that PG16 has `WITH RECURSIVE` (p.174), the assessment most faithful to the sources is: in PostgreSQL 16, Adjacency List + `WITH RECURSIVE` is a legitimate option to consider before more complex models. v1 said the opposite ("CTE generates expensive plans and high CPU consumption"), which the excerpt does **not** state.

## 5. What the sources do NOT say
- That "Codd's model has no operators for acyclic graphs" (v1, ANTI-TREE p.1-2) and that querying direct children is "O(1)": they are not in the excerpt.
- That Closure Table is "the solution recommended by Karwin", column names `nsleft/nsright`, tables `comentarios`/`arvore_caminhos`, cost $O(N\times D)$: none of this is in the available pages (the book's example uses the `Comments` table).
- Any quantitative performance comparison between the models.
