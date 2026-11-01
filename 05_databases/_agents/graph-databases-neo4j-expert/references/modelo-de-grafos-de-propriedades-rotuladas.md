# Labeled property graph model (LPG)

Source: NEO4J (Robinson, Webber, Eifrem, 2nd ed., 2015). Pages = **PDF** (printed = N − 18). See `INDEX.md`.

## 1. Model definition
- A graph is, formally, a set of vertices and edges, that is, nodes and the relationships that connect them [from source] (NEO4J p.19).
- The *labeled property graph* has: nodes and relationships; properties (key-value pairs) on nodes; one or more labels per node; relationships that are named, directed and always have a start and end node; properties on relationships too [from source] (NEO4J p.22; recapped on p.44-45).
- Labels group nodes and indicate the role each node plays; a node can have several labels [from source] (NEO4J p.38, p.44).
- In Neo4j, property keys are strings and values are strings/Java primitives plus arrays of those types [from source] (NEO4J p.44).
- Properties on relationships serve for algorithm metadata, to give semantics (quality, weight) and to restrict queries at runtime [from source] (NEO4J p.45).
- The book adopts the property model because most graph databases use it; the other two dominant models are RDF triples and hypergraphs (see `nosql-apendice-e-modelos-de-grafo.md`) [from source] (NEO4J p.23).

## 2. Labels as first-class citizens
- Besides indicating roles, labels allow associating metadata with nodes: indexing all `User` nodes or requiring every `Customer` node to have a unique `email` [from source] (NEO4J p.62).
- The "Labels in the Graph" section uses labels to locate "all `User` nodes" and says a node can have more than one label [from source] (NEO4J p.38).
- In the data center example, most nodes have two labels: a specific one (`Database`, `App`, `Server`) and a general `Asset`, to query by type or by any asset [from source] (NEO4J p.57).

## 3. Relationships
- A relationship always has a direction, a single name and a start and end node; there are no "dangling" relationships [from source] (NEO4J p.44).
- Direction and name together give semantic clarity to the structure [from source] (NEO4J p.44).
- Relationships naturally form paths; querying (traversal) is following paths, which aligns the database operations with the data layout [from source] (NEO4J p.38).
- Bidirectional relationship: the book recommends that queries ignore the direction, instead of creating two relationships [from source] (NEO4J p.85).
- Relationships are "first-class citizens" in the model; in other DBMSs the connection is inferred by foreign keys or external processing [from source] (NEO4J p.24).

## 4. Absence of schema and additivity
- Graphs are "additive": new relationship types, nodes, labels and subgraphs enter without disturbing existing queries [from source] (NEO4J p.27).
- Because they have no schema, they lose the schema-oriented data governance mechanisms; the book proposes programmatic governance with tests [from source] (NEO4J p.27).
- Labels allow declarative indexes and constraints (see `cypher-fundamentos-e-padroes-de-consulta.md`) [from source] (NEO4J p.65).

## 5. What the book does NOT say
- The book does not limit the number of labels nor describe native temporal/spatial property types; current Neo4j data types (dates, points, lists) are [extrapolation] and should be checked in the current documentation.
- `NEO_START` (4 pages) **does not define** the LPG: the PDF is just an index page of the site with topic titles (NEO_START p.1-2). Any technical definition comes from NEO4J.
- The rule "relationship type always in uppercase" is a convention of the book's examples (`KNOWS`, `FRIEND`), not a rule of the model [inference].
