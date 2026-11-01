# HTTP status: what the source shows and what it does not cover

## The book's rule

- Learn the standard HTTP statuses and use them correctly. Statuses do not live in isolation: they are part of complete messages (status + headers + body) with well-known patterns. Do not think of them as function return codes (APIGEE p.51).
- Learn the combinations of status and headers and the scenarios for each; repeating the pattern leverages what the user already knows about the web (APIGEE p.52).

## Combinations the source shows

| Status | Required/recommended pair | Page |
|---|---|---|
| `201 Created` | always with `Location` = URL of the new resource | APIGEE p.7, p.51 |
| `200 OK` (GET) | header bundle: `Content-Location`, `Content-Type`, `ETag`, `Content-Length`; the authors always include `Content-Location`, although it is optional | APIGEE p.52 |
| `405 Method Not Allowed` | necessarily with `Allow` listing the accepted methods | APIGEE p.52 |
| `303 See Other` | `Location` to the first page of a large collection | APIGEE p.43 |
| `401 Unauthorized` | appears only in a short list ("200 – OK", "401 – Unauthorized"), without discussion | APIGEE p.52 |

Other standard HTTP mechanisms cited: `ETag` + `If-Match` for concurrent updates, `Accept` for formats (APIGEE p.7, p.46).

## Outside the source

- **Not present** in the text: 202, 204, 400, 403, 404, 409, 422, 429 (`Retry-After`), 500 and the other 5xx. There is also no "never return an error with 200" rule: the source only says to use the standard statuses (APIGEE p.51).
- If the user asks about those codes, say that the source has no table, apply the general principle (APIGEE p.51, p.52) and answer the rest as [extrapolation] (RFC 9110 / general HTTP knowledge), with no page.
- The script `scripts/http_status_selector.py` separates what is [from source] from what is [extrapolation].
