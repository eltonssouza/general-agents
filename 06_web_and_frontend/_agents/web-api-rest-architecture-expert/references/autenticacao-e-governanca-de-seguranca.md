# Authentication and SDKs

## OAuth 2.0

- API guides used to discuss at length which authentication to use; today almost every major web API uses OAuth2 (PayPal, Twitter, Google, Facebook, GitHub): do the same (APIGEE p.55).
- Benefits cited: apps do not need to share passwords; the provider revokes tokens for one user or for a whole app without forcing a password change, which is critical if a device is compromised or a malicious app is discovered (APIGEE p.55).
- Result: better security and a better experience in web and mobile apps (APIGEE p.55).

## SDK as a complement

- A well-designed, consistent, standards-based, documented API may not need an SDK; documented code examples are critical (APIGEE p.55).
- Even so, most people prefer an SDK in their own language and come to see it as "the API"; the quality of the web API determines the cost, reliability and number of SDKs, and it shows up in debugging and performance tuning (DevTools) (APIGEE p.55).

## What the source does not cover

OAuth flows/grants (authorization code, PKCE, client credentials), Bearer tokens in the `Authorization` header, API keys, rate limiting, scopes, CORS, TLS, protection against stack-trace leakage. Answer as [extrapolation], with no page, or say that the source does not address it.
