# Fidelity report — graphql-expert

## Source
`14_frameworks\GraphQL-Learn-Official.pdf`: 6 pages, ~4 thousand characters, no images (checked with PyMuPDF), capture of graphql.org/learn from 18 Aug 2026 (metadata). Content = lesson index + landing page. Page convention: PDF page. No page is a 404 or empty; page 6 is navigation only.

## Citation verification
`python -I tests/verify_citations.py`: **37 positive checks** (key terms present on the cited pages) and **20 negative** (subscription, resolver, introspection, directive, DataLoader/N+1, pagination, over/under-fetching, scalars/enum/union, auth, caching, federation, deprecation, multipart, GraphiQL, concrete HTTP statuses, clients, spec version, GraphQL code, GraphQL history, TypeScript/codegen). Result: **0 failures**.
Note: the number of checks is proportional to a source of ~4 thousand characters, not to the 60 requested for large books.

## Script tests
`python -I tests/run_script_tests.py`: 19 tests (lookup with hit, gap, off-topic, JSON, invalid page; checklist with good notes, short notes, Portuguese notes, injection and nonexistent file; verify_citations). Result: **19 PASS, 0 FAIL** when the extracted source text is available (otherwise verify_citations is SKIPped). One defect found and fixed: the lookup warning said "the source names the lesson above" even with no entry shown; it now distinguishes the two cases. Another: cp1252 output on Windows broke accents in subprocess; the scripts now reconfigure stdout to UTF-8.

## Test cases
`tests/casos-de-teste.md`: 21 cases (6 conceptual, 4 practical, 5 edge, 4 out of scope, 2 injection). Those that depend on scripts were executed (lookup of "mutations", "fragments variables", "federated", "n+1 resolvers", "pagination", "spec version", "Apollo Hasura Yoga", "http methods status codes", "versioning"; checklist on the fixtures). The rest were checked manually against the prompt and the references. **It was not run blind by an independent model**; the evaluation of the agent's behavior is from its author.

## Limitations
- Shallow source by nature: the agent only enumerates what the index names; any real technical question falls into NOT COVERED.
- Descriptions cut on pages 1-2 and 2-3 and "Show more" buttons: the set of lessons is incomplete.
- The lookup is keyword-based (accents normalized); very free-form queries may not match and return NOT COVERED. Portuguese and English keywords are recognized.
- The checklist detects a mention by keyword, not correctness.

## Open items
None critical. If the user obtains captures of the full lessons, create a larger agent (graphql-lessons-expert) instead of inflating this one.
