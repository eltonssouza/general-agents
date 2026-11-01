# 02 — Best Practices and Schema Governance (only what the descriptions say)

Source: GQL p.2-3.

## Best Practices (p.2)
- [from source] (GQL p.2) Section described as practical guidelines and real-world strategies to **design and operate** GraphQL APIs, "for scale and security". The list is truncated by "Show more": only 4 lessons are visible; the others were NOT captured (NOT COVERED as to how many and which exist).
- **Lesson 1 Introduction:** context behind the Best Practices lessons (p.2).
- **Lesson 2 Thinking In Graphs:** shifting the mindset from **RESTful endpoints** to graph thinking, aligning the schema with **business logic** and **legacy systems** (p.2).
- **Lesson 3 Serving Over Http:** how GraphQL operates over HTTP, including **methods, headers, status codes and endpoint design** (p.2). NOT COVERED: which method, which headers/statuses, URL convention.
- **Lesson 4 File Uploads:** handling uploads by **wrapping them as mutations**; the lesson presents the "recommended approach" for integration (p.2-3). NOT COVERED: what that approach is (multipart, pre-signed URL etc.).

## Schema Governance (p.3)
- [from source] (GQL p.3) Central claim: a healthy API starts with a well-governed schema, with **review processes and automated checks** to keep it consistent, secure and easy to evolve as the team grows.
- **Lesson 1 Schema Ownership and Governance Models:** cites three models, **centralized, federated and hybrid** (p.3). Names only: NOT COVERED as to differences, pros and cons, and Federation as a technology.
- **Lesson 2 Governance Tooling:** schema governance and management best practices (p.3). No tool is named.
- **Lesson 3 Schema Review:** review processes and automated validation (p.3).
- **Lesson 4 Schema Change Management:** managing schema changes and **versioning** for smooth evolution (p.3). NOT COVERED: strategy (deprecation, breaking changes, etc.).
- There are "Show more" and "Explore schema governance" buttons: the section has more lessons beyond the 4.

## Note on "versionless"
Page 1 says GraphQL enables *versionless* APIs, and page 3 has a lesson on "versioning in GraphQL". The PDF does **not reconcile** the two; do not invent the reconciliation. [extrapolation] only if labeled.

## REST boundary
The only bridge to REST is the description of Lesson 2 (p.2). Any REST x GraphQL comparison (verbs, HTTP caching, over/under-fetching, HATEOAS) is **[extrapolation]** and must be referred to `web-api-rest-architecture-expert` (`06_web_and_frontend\_agents\`), which has the source-backed REST content.
