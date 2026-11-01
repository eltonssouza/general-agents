# Representation design: JSON, links and metadata

The book starts with the design of representations, not URLs, because it is a data-oriented model (APIGEE p.13).

## Representation and media types

- Representation: the data exchanged between client and server; the resource's state is not seen directly, only its representation; all media types of a resource should encode the same information (APIGEE p.13).

## Use JSON, and simple JSON

- JSON is the de facto standard and should be used; limitation: it has no type for dates or URLs, which become strings interpreted by context (APIGEE p.13).
- Names in JSON should always be property names, and objects should correspond to entities of the model. Counterexample: the Facebook Graph API JSON with user IDs in the name position and an artificial `data` key (APIGEE p.14).

## Links

- HATEOAS: the idea of generic clients guided only by the data, like browsers. Such clients are expensive, less satisfying and rarely built (exception: IoT, note 5); the book admits it does not find the description of HATEOAS in Fielding's thesis clear (note 4). The recent shift: links improve usability and learning for **every** API (APIGEE p.15).
- Step 1 (existing API): add `ownerLink` while keeping `ownerID`, and `dogsLink` on the owner (APIGEE p.16). Benefits: no hunting for a template in the documentation, no guessing which value fits which template, no writing a *template processor*; `dogsLink` reveals that the navigation exists (APIGEE p.17).
- Links can be read-only at first: `ownerID` is changed with PUT/PATCH and the server recomputes the link (APIGEE p.20).
- Step 2 (new API): `owner` with a URL value, read-write, eliminating `ownerID`; handles owners of different types (person or institution) without `ownerType`; the client reacts to what it finds, like a browser (APIGEE p.20, p.21).
- Server-side caution: do not store absolute URLs with the domain in the database; strip scheme and authority from own URLs before storing and put them back on read; external URLs stay absolute. Alternative: accept/produce "path-absolute" relative URLs (starting with `/`), pushing base resolution to the client (APIGEE p.21).
- Preferred format: a simple name/value pair, `"owner": "https://dogtracker.com/persons/98765432"`; drawback: a generic client has to guess which strings are URLs (APIGEE p.22). Appendix: `{"href": ...}` is the "next simplest" (it lets you find URLs without metadata; Terrifically Simple JSON project) and the `links` array with `rel` is from JSON hyper-schema, for which the book suggests a specialized media type (APIGEE p.62). The format the authors **used on a whole project and abandoned** was `{"dataType": "URI", "value": ...}`: they forgot to use it and it generated bugs, so they went back to plain strings (APIGEE p.63). Siren, HAL, JSON-LD, RDF/JSON, Collection+JSON and Hydra add concepts beyond links (APIGEE p.63).
- Who uses it: Google Drive API (`selfLink`, `parentLink`) and GitHub (`url`, `comments_url`, some values are URI templates) (APIGEE p.22, p.23, p.24, p.25). [DATED: period examples, Drive v2.]

## `self` and `kind`

- Include `kind` (sometimes `type` or `isA`) and `self` (on GitHub, `url`; the name `self` comes from ATOM and is registered with IANA) in **every** JSON object, including nested ones (APIGEE p.40).
- `self` removes the need to know which GET the object came from; `kind` lets the client recognize what it knows how to process and lets you add concepts without changing the version (APIGEE p.40).

## Collections

- Preferred: an object with `self`, `kind: "Collection"` and `contents` (array of objects, each with `self` and `kind`; an array of URLs also works) (APIGEE p.41).
- Against the bare array: the collection becomes a special case, stops being self-describing and loses a place for properties such as `creationDate` and `owner` (APIGEE p.42). There is no known standard for this (APIGEE p.42).
- A custom name (`"dogs": [...]`, `kind: "Dog-Collection"`) is descriptive but hinders a generic client; "any of them will do". Collection+JSON: too complex for the authors, with no objection in principle (APIGEE p.42, p.43).
- Resource types could be URLs (`https://apigee.com/collections#Collection`) instead of strings; this avoids conflicts but makes the JSON larger; there is no standard (APIGEE p.45, p.46).

## Formats and PATCH

- Several output formats: support the `Accept` header (APIGEE p.46).
- Support PATCH ("you should"): JSON Merge Patch (simple, does not cover everything) and JSON Patch (more complete and complex) formats; you can have both. PUT replaces the whole resource and makes evolution fragile (APIGEE p.46).
- HTML output helps SPAs get indexed by search engines; outside the scope of the book (APIGEE p.46).

## Property names

- snake_case vs camelCase: the science is inconclusive; pick what pleases clients; for most web APIs, camelCase, which the book recommends unless the audience is atypical (APIGEE p.47).
- Avoid the hyphen (subtraction in JS) and the characters `/\=:;,.?#<>@`; avoid reserved/global words — the list includes `self`, `type`, `this`, `window`, `class`… (APIGEE p.47).
- [inference] Internal tension: the book recommends the `self` property and accepts `type` as a spelling of `kind` (APIGEE p.40), but puts them on the list to avoid (APIGEE p.47). Flag the conflict to the user.

## Dates

- More than a dozen standards; the most common is the XML Schema one, a subset of ISO 8601 (Bing); the Twitter format follows none (APIGEE p.47, p.48).
- Unix time since 1970 (Foursquare): simple and differenceable, compromised by how leap seconds are implemented, but still worth considering (APIGEE p.48). [inference] The book speaks of milliseconds, but the Foursquare example (`1475795458`) is in seconds.
- The book does not tell you to use UTC nor does it forbid numeric timestamps.
