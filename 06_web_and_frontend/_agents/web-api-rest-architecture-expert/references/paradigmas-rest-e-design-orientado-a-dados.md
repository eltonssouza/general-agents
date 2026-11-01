# The REST paradigm and data-oriented design

## The book's thesis

Use HTTP directly, with the minimum of added concepts, and focus the design on the data (resources), letting HTTP provide the uniform API (APIGEE p.7, p.9, p.60).

## Why HTTP only

- SOAP/WSDL tried to bring CORBA/DCOM on top of HTTP and proved too complex and fragile; "RESTful" APIs became lighter, but still carry RPC ideas (APIGEE p.7).
- Put yourself in the user's place: they already know HTTP and other APIs; following standards is worth more than inventing. Examples given right in the introduction: a create POST returns `201` with `Location`; concurrency with `ETag` + `If-Match`; formats with `Accept` (APIGEE p.7).
- Custom mechanisms are allowed **in addition** to the standards, never instead of them (APIGEE p.7).
- The API's job is to make the application developer successful; they are the central link in the value chain (APIGEE p.8).

## REST, RESTful and "endpoint"

- **Web API**: the pattern of HTTP requests/responses of a site specialized for access by programs (APIGEE p.8).
- **REST**: the name of the architectural style of HTTP itself; HTTP is the reality, REST is the set of ideas that shaped it (APIGEE p.8).
- "Endpoint" and "parameter" come from RPC, not from HTTP/REST. **RESTful** denotes the mixed style, the most common, and has no precise definition; HTTP and REST do (the note says it is false to claim that REST is imprecise) (APIGEE p.8, p.9).
- The book uses "REST API" for APIs that use only concepts inherent to HTTP (APIGEE p.9).
- Stance: not purist; effectiveness matters, but, all else equal, fewer concepts beyond HTTP is better (Occam's razor, Saint-Exupéry quote) (APIGEE p.9).

## Coupling

- The coupling metric is how easy it is to change one side without breaking the other; HTTP has a rare track record of decoupling (20-year-old clients still work) (APIGEE p.9).
- Layers coming from RPC tend to undermine this low coupling: another reason to stay with HTTP (APIGEE p.9).

## Data-oriented vs function-oriented

- A REST API exposes domain entities (`/dogs` collection, each dog with its own URL), not functions (APIGEE p.10).
- With a resource's URL and HTTP you already know GET/DELETE/PATCH/PUT; with the collection URL, POST creates and GET searches, with filters in the query string (APIGEE p.10).
- The list `/getAllDogs`, `/getRedDogsWithoutSiblings`, `/newDogForOwner`… shows the cost of the function style: details without a pattern, knowledge that cannot be reused in another API (APIGEE p.11, p.12).
- Using HTTP natively "you do not need to invent an API": you define only the data. In REST this is the **uniform interface** constraint, which also makes universal browsers and search robots possible (APIGEE p.12).
- DBMS analogy: once you have learned the database API, only the schema changes; with HTTP, only the data model changes (APIGEE p.32, p.60).

## Elements that define the API

Representations (fields and links), standard HTTP headers (and sometimes custom ones), URLs and query URI templates, and behaviors required of clients (DNS caching, retries, tolerance of new fields) (APIGEE p.12).

## The book's conclusion

Designing an entity-oriented API is more like designing a database than a language API; it requires mapping in code, but yields simplicity, uniformity and low coupling (APIGEE p.60).
