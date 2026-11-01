# Versioning

## The book's position

- A controversial topic, with contradictory guidance on the internet; the most practiced pattern is probably the version in a path segment. Two ideas from the book (APIGEE p.56):
  1. doing nothing to version is a smart approach, increasingly considered;
  2. links and a version in the URL combine poorly.

## Do nothing

- The authors used to start with `/v1` in the path "just in case" and never changed it (APIGEE p.56).
- Many changes are compatible; if it can be done without changing the version, do it (APIGEE p.56). Aids:
  - adding properties is safe if clients know in advance; to test this, put random properties on the server's resources (APIGEE p.56);
  - use PATCH instead of PUT: PUT requires resending everything, including properties the client did not even know about; PATCH changes only what is referenced and the server does the merge. Never implement PUT with PATCH semantics. SQL's `UPDATE` has PATCH semantics (note 9) (APIGEE p.56);
  - new resource types can usually be added without breaking anything, with care when references to them appear in old data (APIGEE p.56).
- Fundamental changes to the model require a new API and migration, with or without versioning (APIGEE p.57).
- Versioning presupposes an intermediate range of changes; many find that it does not exist in their API — it happened to the authors (APIGEE p.57).
- "You must version from the start because you cannot add it later" is not true in their experience: adding it later is easy, in a URL or header; requests without a version are V1. When in doubt, you can leave it out (APIGEE p.57).

## If you do version: URL vs header

- With links, a version in a header is the simplest option (APIGEE p.57).
- The problem with a version in the URL: when returning `owner: …/v2/persons/…` the server guesses the desired version of the linked resource (do persons have a V2?), and conceptually the dog does not belong to a version but to a person (APIGEE p.57, p.58).
- Way out 1: 1+n URLs (one for the entity, one per version); the link uses the entity URL and the client converts it according to external documentation — OpenStack does it this way (APIGEE p.58).
- Way out 2 (one database): return relative URLs (`/persons/98765432`) that the client prefixes with `/v1` or `/v2`; this is not standard URL resolution, it is string manipulation (APIGEE p.58, p.59).
- Conclusion: a version in the URL works with links but with more complexity than an `Accept-Version` header or similar; both require clients with documented knowledge; not versioning is simpler still (APIGEE p.59). The book's conclusion reinforces that "doing nothing" is defensible (APIGEE p.60).

## Common mistakes when citing

- "The book mandates `/v1` and never releasing without a version": false in this work (APIGEE p.57).
- "The book forbids a version in the URL": false, it says it works with more complexity (APIGEE p.59).
- Versioning only the major version, `v1.2` forbidden, an API subdomain: not in the source.
