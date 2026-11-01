# Error handling

## Why it matters

- Developers think first of the happy path, but the quality of error handling is a critical part of the experience (APIGEE p.51).
- To the consumer, everything behind the interface is a black box: errors give context and visibility (APIGEE p.51).
- Two moments: learning to use the API (developers learn through errors, as in TDD/XP) and diagnosing problems after the app is in front of users (APIGEE p.51).

## Status and headers

- Use the standard HTTP statuses with their headers (201 + `Location`, 405 + `Allow`…). See [mapeamento-de-codigos-de-status-http.md](mapeamento-de-codigos-de-status-http.md) (APIGEE p.51, p.52).

## Message in the body

- Messages in the payload as verbose as possible (APIGEE p.52).
- The book's example of an error body "for people": `developerMessage` (verbose description, in plain language, with fix hints for the developer), `userMessage` (pass on to the app's user if needed), `errorCode` (numeric in the example: 12345) and a more-information URL. In the example this key is spelled `"more info"`, with a space (APIGEE p.53).
- Why JSON if it is for people: between the user and the message there is almost always a programmatic agent, which is the real audience (APIGEE p.53).
- Summary: verbose, plain language, as many hints as the team can imagine about the cause, and a link for more information (APIGEE p.53).

## Cautions when citing

- The four fields are an **example**, not a mandatory schema nor an "Apigee specification". [inference] The spelling `moreInfo` is a reasonable adaptation (the source advises against characters incompatible with identifiers, APIGEE p.47), but it is not the example's spelling.
- The source **does not mention** stack traces, validation `details`, `correlation_id`, RFC 7807/9457 (Problem Details) or "never return 200 with an error". If you use them, mark [extrapolation].
