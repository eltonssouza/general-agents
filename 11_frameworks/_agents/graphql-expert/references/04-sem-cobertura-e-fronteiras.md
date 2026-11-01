# 04 — NOT COVERED and boundaries

List readable via `python -I scripts/gql_lookup.py --gaps`. The source (lesson index) does **not** cover:

1. Schema syntax (SDL): scalars, object/input/enum/interface/union, lists, non-null.
2. Query syntax: aliases, directives, inline fragments, named operations; only the names fields/variables/fragments appear.
3. Subscriptions and real time.
4. Introspection, GraphiQL, Playground.
5. Resolvers, execution model, N+1, DataLoader.
6. Pagination (cursor, connections, Relay).
7. Authentication, authorization, depth/complexity limits, rate limiting, security.
8. Caching, performance, persisted queries, CDN.
9. Error format and concrete HTTP status codes (the "Serving Over Http" lesson only mentions them).
10. Federation (how it works), supergraph, gateway.
11. Specification and library version.
12. Developed REST x GraphQL comparison.
13. File upload implementation.
14. Frontend clients, codegen, TypeScript.
15. Testing, observability, deploy, migration.

## How to answer a NOT COVERED topic
1. Say "NOT COVERED in the GQL PDF (lesson index capture)".
2. If the corresponding lesson is **named**, give the title and page.
3. Optionally offer 2-4 lines of labeled **[extrapolation]**, without a spec/library version and without promising that the official lesson says the same. Do not fill in with long code examples.

## Boundaries with other agents
- **REST and REST API design:** `web-api-rest-architecture-expert` (`ROOT\06_web_and_frontend\_agents\`). REST x GraphQL comparison requests: cite only the description of Best Practices Lesson 2 (GQL p.2), mark the rest **[extrapolation]** and refer.
- **Web frameworks, databases, general security:** other agents; decline politely.
