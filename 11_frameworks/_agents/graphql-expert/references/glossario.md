# Glossary (terms used by the GQL capture; no definitions beyond what it says)

| Term | What the source says (paraphrase) | Page |
|---|---|---|
| GraphQL API | object of the tutorial's "core concepts" | 1 |
| versionless | characteristic attributed to GraphQL in Lesson 1 (flexible, no versions); no explanation | 1 |
| strong type system | support for flexible APIs; no detail | 1-2 |
| schema language | language that defines the shape of the data with types | 1 |
| types | units with which the schema models data | 1 |
| query | request that selects exactly the data needed | 2 |
| field | part of the query; only the name appears | 2 |
| variable | query feature; name only | 2 |
| fragment | query feature; name only | 2 |
| mutation | data-modifying operation (update, delete) | 2 |
| Thinking In Graphs | shift from RESTful endpoints to graphs | 2 |
| Serving Over Http | GraphQL over HTTP: methods, headers, status, endpoint | 2 |
| File Uploads | uploads wrapped as mutations | 2-3 |
| schema governance | review + automated checks for a consistent, evolvable schema | 3 |
| centralized / federated / hybrid | schema ownership and governance models; names only | 3 |
| schema review | review and automated validation | 3 |
| schema change management | change management and versioning | 3 |
| GraphQL-JS / GraphQL.js | library used in a tutorial on schemas and queries | 4 |
| Apollo Odyssey | interactive courses with Apollo tools | 4 |
| Yoga | tutorial for GraphQL servers on Node, CF Workers, Deno | 4 |
| Hasura | fullstack tutorials | 4 |
| GraphQL Foundation | holder of the site's 2026 copyright | 6 |
| GraphQLConf 2026 | announced event, May 19-20, Fremont, California | 6 |

Terms such as resolver, subscription, introspection, directive, scalar: do **not** appear in the source (verified in `tests/verify_citations.py`, negative checks).
