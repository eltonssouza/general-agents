---
name: graph-model-advisor
description: Advises whether a concept should become a node, a relationship or a property in a graph model, following the guidelines of the book Graph Databases (p.85–92) and its treatment of time. Use when the user asks "is this a node or a property?", "model emails as a graph", "how do I model history/time?" or "should this relationship be a node?". Degree thresholds are the user's, not the book's.
---

# Node, relationship or property

Sources: NEO4J p.85–89 (guidelines) and p.90–92 (time), PDF pages (printed = N − 18). Context in `../../references/` (start with `INDEX.md`).

## Procedure

1. Start from the questions the data must answer (design for queryability, p.81, p.84).
2. Run the advisor (read-only, no network):
   ```bash
   python -I <PKG>/scripts/graph_advisor.py --name Email --kind action --links 3
   python -I <PKG>/scripts/graph_advisor.py --name Endereco --kind value --multi-field
   python -I <PKG>/scripts/graph_advisor.py --name Peso --kind attribute --weight
   python -I <PKG>/scripts/graph_advisor.py --name Pedido --kind entity --temporal order
   python -I <PKG>/scripts/graph_advisor.py --name Categoria --kind entity --fanout 200000 --threshold 50000
   ```
   (`<PKG>` = package root; from this skill, `../../`.)
3. Look for the hidden entity: a relationship that looks like a verb ("emailed") may be a noun (p.70–73, p.81–82).
4. Label: book guidelines `[from source]`; direct deduction `[inference]`; degree thresholds and current practices `[extrapolation]`. Trade-offs, not dogmas (fine-grained type against property, p.85–86).

## Response format

Concept — recommendation (node, relationship, property) — rule and origin — alternative and trade-off — pages.

## Limits

Supernodes/dense nodes are not covered in the book (`[extrapolation]`).
