# Query URLs, filters and non-persistent responses

## Query URLs as a query language

- Query URLs are to HTTP what queries are to a DBMS; by defining URI templates the designer creates an API-specific query language, and every extra freedom is a learning burden for the client. Goal: URLs that are regular and predictable from the data model (APIGEE p.32).
- Preferred path style; general model by relationships; symmetry: see [relacionamentos-e-simetria-em-subrecursos.md](relacionamentos-e-simetria-em-subrecursos.md) (APIGEE p.33, p.34, p.35).
- `/search?type=Dog&ownerId={personId}` is **not** treated by the book as a "verb in the URL": it presents it as an equivalent form of the same query (APIGEE p.19, p.33) and prefers the path style only for the four reasons on p.33. Do not cite p.26 against `/search`.

## Path (matrix) parameters

- Alternative syntax: `/persons;5678/dogs`, `/persons;id=5678/dogs` (synonym), `/persons;name=JoeMCarraclough/dogs`; rule `/{relationship-name}[;{selector}]/…` (APIGEE p.36).
- Advantage: each segment is exactly one relationship traversal. Disadvantage: little familiarity; only Jax-RS has explicit support, although the authors implemented it in Express (APIGEE p.36).

## Filters

- More complex filter clauses traditionally go in the query string: `/dogs?color=red&state=running&location=park` (APIGEE p.36).
- Path and query string combine: `/persons/5678/dogs?color=red` (APIGEE p.37).
- **Sorting (`sort`) and full-text search (`q`) are not covered in the source.** The only `?q=` in the text is Google search used as an analogy (APIGEE p.19). If you suggest them, mark [extrapolation].

## Responses that are not persistent resources

- Common in finance, telecom and automotive; clues: calculate, translate, convert (APIGEE p.37).
- There is no need to abandon the noun model: the URL identifies the response resource, not the algorithm; to the client it makes no difference whether it was computed or read from the database (APIGEE p.37).
- Examples: `/monetary-amount?quantity=100&unit=EUR&in=CNY` or `/monetary-amount/100/EUR/CNY` (APIGEE p.37); content negotiation with `GET /monetary-amount/100/EUR` + `Accept-Currency: CNY` (a header from the example, not presented as a standard) (APIGEE p.38).
- POST to a noun URL (`/currency-converter`) is acceptable, with two costs: a response that HTTP cannot cache (the cache key you would invent is equivalent to the GET URL) and a departure from the uniform interface toward RPC, like stored procedures in a database (APIGEE p.38, p.39).
- Use GET when there is a direct path; URLs can always be nouns (APIGEE p.39).
