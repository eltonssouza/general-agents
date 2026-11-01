# Relationships: links, query URLs and symmetry

## In the representation: links

- Conceptual relationships are represented in HTTP with links; replace/complement `ownerID` with `ownerLink`/`owner` and add `dogsLink` on the owner (APIGEE p.15, p.16, p.20). Details in [design-de-representacoes-json-e-metadados.md](design-de-representacoes-json-e-metadados.md).

## Links and URI templates coexist

- Links show where you can go from where you are (paved paths); URI templates are shortcuts "across the grass" when there is no link or the path is long (APIGEE p.17).
- Templates pay off more with readable values (a name instead of an obscure ID), for the same reason domain names exist (APIGEE p.18).
- Analogy with the web: search (Google) + navigation by links (Yahoo!'s root); an API's templates amount to a query language of its own, useful but something that must be learned for each API. The two mechanisms complement each other (APIGEE p.18, p.19).

## In query URLs

- Path style (`/persons/{personId}/dogs`) preferred over the parameter style (`/search?type=Dog&owner={personId}`): more readable, easier to implement, does not suggest support for every parameter combination and expresses graph traversal (`/dogs/123456/owner/spouse`) (APIGEE p.33).
- Meaning of `GET /persons/5678/dogs`: start from `/`, follow the `persons` relationship, select 5678, follow `dogs` (APIGEE p.34).
- General model: `/{relationship-name}[/{resource-id}]/…/{relationship-name}[/{resource-id}]`, with the ID only after a multivalued relationship; the first segment is a relationship of the root `/` (APIGEE p.34).
- POST to `/persons/5678/dogs` could create a dog for that person as a shortcut for POST to `/dogs`; the book leaves the decision to the reader (having two paths to the same thing) (APIGEE p.34, note 8).

## Symmetry

- If the query URL implies the relationship, include the corresponding link property (`dogs`) on every person; if the property exists, offer the query URL that traverses it without fetching the person (APIGEE p.35).
- The root `/` should expose `persons` and `dogs` (APIGEE p.35).
- Unification: query URLs let you traverse in one request sequences of relationships already defined in the data. The Rapier project tries to make it easier to specify APIs this way (APIGEE p.35).
- Nothing is sacred: use another pattern if you prefer, but a consistent pattern beats designing each URL in isolation (APIGEE p.35).
