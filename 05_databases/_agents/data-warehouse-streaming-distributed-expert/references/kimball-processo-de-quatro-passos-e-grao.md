# Kimball's Four-Step Process and Declaring the Grain

> Page convention: `(KIMBALL p.N)` = **PDF** page (cover = p.1, table of contents = p.2-3, text starts on p.4); printed page = N − 3. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. The document is a summary of the "official" Kimball Group techniques extracted from *The Data Warehouse Toolkit*, 3rd ed. (2013) (KIMBALL p.4), not the complete book.

## 1. Before modeling: requirements and data realities
- [from source] Before starting the dimensional effort, the team needs to understand the business needs (through sessions with representatives: key indicators, problems, decisions, analytical needs) and the realities of the source data (meetings with system experts and high-level profiling) (KIMBALL p.4).
- [from source] Models should be designed collaboratively, in interactive workshops with experts and data governance representatives; the modeler leads, but should not work isolated from those who understand the business (KIMBALL p.4).

## 2. The four decisions
[from source] The four key decisions of dimensional design, in this order: (1) choose the business process, (2) declare the grain, (3) identify the dimensions, (4) identify the facts. The answers come from combining business needs with the data realities in the collaborative sessions; after that the team defines table and column names, sample values and business rules, with governance present (KIMBALL p.4).

### Step 1: business process
- [from source] Business processes are the organization's operational activities (e.g. taking an order, processing a claim, enrolling students, taking a monthly account snapshot). Their events generate or capture metrics that become facts; most fact tables focus on the result of **one** process; choosing the process defines the target of the design and makes it possible to declare grain, dimensions and facts; each process corresponds to a row of the bus matrix (KIMBALL p.4).
- [inference] Since the book defines a process as an operational activity, modeling by process (and not by org chart) is the natural reading; the text does **not** contain a rule like "never model by department". Departments appear only in the opportunity/stakeholder matrix, which serves to decide whom to invite to the workshops (KIMBALL p.14).

### Step 2: grain
- [from source] Declaring the grain is the central step: it establishes exactly what one row of the fact table represents and becomes the design's "binding contract". It must be declared before choosing dimensions and facts, since every candidate must be consistent with it; this gives uniformity to the design (KIMBALL p.5).
- [from source] Atomic grain = the lowest level at which the process captures data. The Kimball Group "strongly encourages" starting with atomic-grained data because it withstands unpredictable queries; aggregated summaries matter for performance, but presuppose the business's common questions (KIMBALL p.5).
- [from source] Each proposed grain results in a separate physical table; different grains must not be mixed in the same fact table (KIMBALL p.5).

### Step 3: dimensions
- [from source] Dimensions provide the "who, what, where, when, why and how" context of the event; they contain the descriptive attributes used to filter and group facts. Whenever possible, a dimension should have a single value for each fact row. They are called the "soul" of the DW because they contain the entry points and labels of the analysis; they receive disproportionate governance effort because they drive the BI experience (KIMBALL p.5).

### Step 4: facts
- [from source] Facts are the measurements resulting from the business event, almost always numeric. A fact row has a one-to-one relationship with a measurement event of the grain; the table corresponds to an observable physical event, not to a report's demand. Only facts consistent with the grain are included (the book exemplifies: quantity and extended price yes; store manager's salary no) (KIMBALL p.5).

## 3. Star and OLAP cube
- [from source] A star schema is the dimensional structure in a relational DBMS: fact tables linked to dimensions by primary/foreign keys. An OLAP cube is the dimensional structure in a multidimensional database, equivalent to or derived from the star schema, accessed by languages more analytical than SQL (e.g. XMLA) (KIMBALL p.5).

## 4. Graceful extensions (resilience)
[from source] Dimensional models tolerate changes without altering existing BI queries/applications or their results. Four cases (KIMBALL p.6):
1. adding facts consistent with the grain (new columns);
2. adding dimensions to the fact (new foreign key columns), as long as they do not alter the grain;
3. adding attributes to dimensions (new columns);
4. making the grain more atomic by adding attributes to a dimension and re-presenting the fact at the smaller grain, preserving the existing column names.

## 5. Examples used in this package
[inference] When the package uses examples such as "order item" with date/customer/product dimensions and quantity/amount facts, they are the agent's illustrations, not content of the document (which cites order, claim, enrollment and retail in a general way).

## Terms from the original (checked by tests/audit_tokens.py)
- `profiling`, `workshops`, `grain`, `dimensions`, `facts`, `business` (KIMBALL p.4)
- `binding`, `contract`, `soul`, `uniformity`, `atomic-grained`, `XMLA` (KIMBALL p.5)
- `resilient`, `columns`, `grain` (KIMBALL p.6)
