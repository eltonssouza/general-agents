# Chatty APIs, pagination and partial responses

## "REST is chatty" is a myth

- A chatty API comes from poorly chosen resources, not from REST; the myth comes from thinking that a REST API must mirror a normalized relational schema (APIGEE p.48).
- Strategy: normalized read-write resources (simple updates) + as many **read-only denormalized** resources as are useful; they are legitimate REST resources, with their own URL and meaning, even if their state overlaps (APIGEE p.48).
- Other ways of denormalizing complicate updates, like "update through a view" in relational databases (APIGEE p.48).

## Pagination by links

- Large collections should be paginated (APIGEE p.43). One way the authors used: `GET /dogs` answers `303 See Other` with `Location: …/dogs?limit=25,offset=0`; the client follows it and receives `200` with `Content-Location` and an object `kind: "Page"`, `pageOf` (the collection), `next` and `contents`; `previous` appears when there is a previous page (APIGEE p.43, p.44). [inference] The example separates `limit` and `offset` with a comma, not `&`; treat it as a peculiarity of the example.
- Use relations registered with IANA (`next`, `previous`, `first`, `last`) when they fit; invent names only for domain relations; registering new relations is possible but hard. Ontologies with URLs for properties are a less practical alternative outside the semantic web (APIGEE p.45).
- The full content of the collection is the concatenation of the pages' `contents`; the authors did not create their own media type for this (APIGEE p.45). There is no standard for the representation of pages (APIGEE p.45).

## Pagination with explicit control

- Sometimes the client wants explicit control, beyond following `next`/`previous`/`first`/`last` (which are often enough, without complex templates) (APIGEE p.50). Here the client builds the URL with parameters; it is not link navigation. Period comparison: Facebook `offset`/`limit`, Twitter `page`/`rpp`, LinkedIn `start`/`count`. Records 50–75: offset 50/limit 25; page 3/rpp 25; start 50/count 25 (APIGEE p.50). [DATED: period APIs.]
- The book prefers `limit` and `offset`, admitting that the ordering of the data and the database may impose compromises (APIGEE p.50).
- The source defines neither a default nor a maximum page size, nor does it address cursor/keyset.

## Partial response

- Gives the developer only what is needed (a tweet carries much more than the app uses) (APIGEE p.48).
- Google pioneered it; Google and Facebook use the optional `fields` parameter; LinkedIn uses `:(id,first-name,…)`, elegant but less common (APIGEE p.49).
- Recommendation: a comma-separated list, `/dogs?fields=name,color,location` (APIGEE p.49).
- Advantages: simple to read, the app picks what it needs, less bandwidth (important for mobile); the syntax can also bring in associated resources and reduce requests (APIGEE p.50).
- The source mentions neither GraphQL nor `?embed=`.
