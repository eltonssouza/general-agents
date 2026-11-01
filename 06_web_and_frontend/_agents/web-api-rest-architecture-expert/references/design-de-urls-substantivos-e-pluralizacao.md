# URL design: nouns, well-known URLs and permalinks

## Nouns are good; verbs are bad

- In the data-oriented model every URL identifies a thing; therefore well-known and query URLs, made for programmers to read and write, should be formed from nouns (APIGEE p.26).
- Even for calculations and conversions you can keep nouns: the URL identifies the response resource, not the algorithm (APIGEE p.37, p.39). See [modelagem-de-acoes-nao-crud.md](modelagem-de-acoes-nao-crud.md).

## Plural?

- [inference] The book uses plurals in collection examples (`/dogs`, `/persons`, `/owners`) (APIGEE p.10, p.26), but **does not state a pluralization rule** and also shows `/person/{name}` in the singular (APIGEE p.29, p.32). Do not attribute "always plural" to the book.

## Well-known URLs

- Every API must publish at least one well-known URL (e.g. `https://dogtracker.com/dogs`), otherwise the client cannot start (APIGEE p.26).
- Good practice: a root `https://dogtracker.com/` with the URLs of the other static entities, making the API discoverable and traversable; even so, the static URLs end up becoming well known (APIGEE p.26). The root can have `self`, `kind` and the `persons` and `dogs` relationships (APIGEE p.35).

## Entity URLs

- There is no need to define an entity URL format: the client should not build entity URLs from pieces — the book asks you to reread that sentence. The URL comes at creation or in searches (APIGEE p.26).
- An opaque URL (`https://dogtracker.com/ZG9n;a8098c1a`) would be enough for computers; for human convenience `https://dogtracker.com/dogs/a8098c1a` is common, and it can still be treated as opaque (APIGEE p.26, p.27).

## Permalinks

- Every link placed in a representation can be stored and reused: it must be stable. Tim Berners-Lee quote: putting mutable information in the name causes problems (APIGEE p.27).
- That is why link URLs tend to be unfriendly (random strings, as in Google Docs), but not every URL has to be like that: query URLs can be friendly (APIGEE p.27).
- Permalinks serve the server: it must route the GET to the right implementation unit, so besides identity the popular format includes the main type: `https://dogtracker.com/{type}/{uuid}`; the slash is a practical choice, not mandatory (APIGEE p.28).

## Type stability

- Putting the type in the permalink presupposes that it does not change; some types are less stable (hunter becomes prey, politician becomes lobbyist; a resource can have more than one type) (APIGEE p.32).
- Think of the current and future mapping between resources and handlers, not of the meaning to the client, for whom the link is opaque (APIGEE p.32).
