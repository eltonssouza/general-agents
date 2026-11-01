# Anti-patterns condemned by the source (with fixes)

| Anti-pattern | Why it is bad | The book's fix | Pages |
|---|---|---|---|
| List of functions (`/getAllDogs`, `/getRedDogsWithoutSiblings`, `/newDogForOwner`) | details without a pattern, learning is not reusable | `/dogs` collection + HTTP methods + filters in the query string | APIGEE p.10, p.11, p.12, p.36 |
| Verb in the URL | every URL identifies a thing | nouns; for calculations, a resource for the result | APIGEE p.26, p.37, p.39 |
| Home-grown mechanism instead of the HTTP standard | forces people to learn something invented | use the standard; extras only as additions | APIGEE p.7 |
| Create POST without `201` + `Location` | ignores the message standard | `201 Created` + `Location` | APIGEE p.7, p.51 |
| `405` without `Allow` | incomplete message | `Allow: GET, DELETE, PATCH` | APIGEE p.52 |
| JSON with IDs in the property-name position (Facebook Graph style) | hard to learn | names = properties; objects = entities | APIGEE p.14 |
| Only `ownerID` with no link | client hunts for the template and builds the URL | `ownerLink` / `owner` with a URL | APIGEE p.16, p.17, p.20 |
| Absolute URLs with the domain stored in the database | break when the domain/environment changes | strip scheme+authority when storing, or use relative URLs | APIGEE p.21 |
| Hierarchy in a link URL | hierarchies change and break links | flat permalink `/{type}/{uuid}`; hierarchy only in queries | APIGEE p.28 |
| Mutable name in the permalink | renaming breaks references | machine ID in the link, name in the query template, or aliases with redirect | APIGEE p.29, p.30, p.31 |
| Client building an entity URL piece by piece | couples the client to the format | the URL comes at creation/lookup; links | APIGEE p.26 |
| PUT with PATCH semantics | violates the semantics of PUT | PUT replaces everything; PATCH for partial updates | APIGEE p.56 |
| Updating only with PUT | client must preserve properties it does not know | support PATCH (Merge Patch / JSON Patch) | APIGEE p.46, p.56 |
| POST for a cacheable calculation | no HTTP caching, departs from the uniform interface | GET on a noun resource | APIGEE p.39 |
| Hyphen or reserved words in property names | breaks identifiers in JS etc. | camelCase, avoid `/\=:;,.?#<>@` | APIGEE p.47 |
| Only normalized resources → many GETs | "chatty API" | read-only denormalized resources; `fields` | APIGEE p.48, p.50 |
| Returning huge collections | bad for client and server | paginate (303 → Page with `next`/`previous`) | APIGEE p.43, p.44 |
| Version in the URL + links with no plan | server guesses the version of the linked resource | version header, 1+n URLs or relative URLs; or do not version | APIGEE p.57, p.58, p.59 |

Anti-patterns common in other guides but **not supported by this source** (mark [extrapolation] if used): error with 200, stack trace in the response, token in the query string, singular vs plural, nesting beyond N levels.
