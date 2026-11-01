# HTTP 1.x: keep-alive, pipelining, multiple connections and the performance hacks

Convention: every cited page is the PDF page (`HPBN p.N`); the printed page is N − 18. Labels: `[from source]` = stated by the book (2013); `[inference]` = deduction from numbers in the book; `[DATED]` = treated as current in 2013 and superseded today; `[extrapolation]` = postdates the book (final section only).

When to open this file: decisions about connection reuse, per-host connection limits, sharding, bundling, sprites, inlining and header cost in HTTP/1.x. For multiplexing and HTTP/2, see `http2-binary-framing-multiplexing-e-streams.md`; for cache and hints, `otimizacoes-de-navegador-resource-hints-e-caching.md`.

---

## 1. How HTTP got to 1.1 (ch. 9)

- HTTP 0.9: a one-line ASCII request terminated by CRLF, a response as an ASCII stream of HTML, connection closed at the end of the document [from source] (HPBN p.173). No headers or metadata; the connection is closed after every request [from source] (HPBN p.174).
- HTTP 1.0: born from ad hoc experimentation between 1991 and 1995; RFC 1945 (May 1996) merely documents common usage and is informational only, not a standard [from source] (HPBN p.175). It adds a status line and headers on request and response, and the response stops being hypertext only; the connection is still closed after every request [from source] (HPBN p.176).
- Requiring a new TCP connection per request is a large performance penalty in 1.0 [from source] (HPBN p.177).
- HTTP 1.1: first official standard in RFC 2068 (January 1997), revised in RFC 2616 (June 1999). It brings keep-alive, chunked transfer, byte-range requests, more caching mechanisms, transfer encodings and pipelining [from source] (HPBN p.177).
- In 1.1 keep-alive is the default: without `Connection: close` the server must keep the connection open. The same feature was ported to 1.0 with `Connection: Keep-Alive` [from source] (HPBN p.179). Either side may close without warning, but ideally the intent is signaled to allow better reuse [from source] (HPBN p.179).
- Book example: an HTML file and a favicon on the same connection, the second request with `Connection: close`; the favicon comes with `Cache-Control: max-age=315360000` [from source] (HPBN p.178).
- HTTP 2.0 is announced in 2012 to improve transport performance without changing the semantics: headers, values and use cases remain [from source] (HPBN p.180). Even with the standard ready, 1.1 clients would have to be served for a decade or more [from source] (HPBN p.181).

## 2. General rules for HTTP 1.x (ch. 11, opening)

- On HTTP 1.0: every deployment should move up to 1.1 [from source] (HPBN p.205).
- 1.1 performance features: persistent connections, chunked, pipelining, byte serving and better-specified caching [from source] (HPBN p.205).
- Of Souders' 14 rules, half are about the network [from source] (HPBN p.205): reduce DNS lookups and HTTP requests (p.205), use a CDN, set Expires and ETags, apply Gzip and avoid redirects (p.206). Gzip typically reduces size by 60–80% [from source] (HPBN p.206).
- The rules above are "evergreen": eliminate unnecessary network latency and minimize bytes [from source] (HPBN p.206). Domain sharding, concatenation, spriting and inlining, on the other hand, are stopgaps for HTTP 1.1 limits; they should be unnecessary, but they must be used until the next revision of the protocol [from source] (HPBN p.206).
- Apple/iTunes case (WWDC 2012): 300% gain on slow networks by reusing TCP connections with keep-alive and pipelining [from source] (HPBN p.207).

## 3. Keep-alive: what is saved

Book scenario: two small resources (HTML with 40 ms and CSS with 20 ms of server time), RTT of 56 ms (28 ms each way, New York–London) [from source] (HPBN p.207).

- Each new connection costs one RTT of handshake plus, at minimum, one RTT of request/response; the minimum for a request on a new connection is therefore 2 RTTs [from source] (HPBN p.207, 208).
- Keep-alive eliminates the second handshake, another slow-start cycle and one RTT [from source] (HPBN p.209).
- For N requests on one connection: without keep-alive, 2 RTTs each; with keep-alive, 2 RTTs for the first and 1 RTT for the following ones. Total savings = (N − 1) × RTT [from source] (HPBN p.210). With an average of 90 resources per page, the savings reach seconds [from source] (HPBN p.210).
- The faster the server, the greater the relative weight of the fixed network cost per request [from source] (HPBN p.209).
- Totals in the example: 284 ms with separate connections; 228 ms with keep-alive; 172 ms with pipelining (a 40% reduction) [from source] (HPBN p.211). `[inference]` 284 − 56 = 228 and 228 − 56 = 172: each step eliminates exactly one RTT. The 40% figure is specific to that example and grows with latency and number of requests [from source] (HPBN p.211, 212).
- Practice: modern browsers use persistent connections on their own if the server cooperates. Check server and proxy configuration, prefer 1.1, and, if stuck with 1.0, use `Connection: Keep-Alive`. HTTP libraries and frameworks often default to no keep-alive; when using raw HTTP connections, reuse them [from source] (HPBN p.210).

## 4. Pipelining: what it promised and why it did not take off

- Keep-alive implies a strict FIFO queue on the client (send, wait for the full response, send the next). Pipelining moves the queue from the client to the server, which sits idle for one RTT in the scheme without pipelining [from source] (HPBN p.210).
- With pipelining, the whole queue costs two RTTs of network overhead [from source] (HPBN p.211).
- Central limitation: HTTP 1.x requires strict serialization of responses; data from several responses cannot be interleaved on the same connection [from source] (HPBN p.212). Even if the server processes in parallel, the ready response (CSS at 20 ms) stays in the buffer until the first (HTML at 40 ms) is sent: head-of-line blocking [from source] (HPBN p.212, 213).
- Practical implications cited [from source] (HPBN p.213): one slow response blocks all the following ones; the server must buffer parallel responses, which can exhaust resources (an attack vector); a failed response may terminate the connection and force the remaining ones to be requested again, with duplicate processing; detecting pipelining compatibility with intermediaries is difficult; some intermediaries abort the connection and others serialize everything.
- State in 2013: some browsers support pipelining as an advanced option, but most keep it turned off; it cannot be counted on for a site served to browsers [from source] (HPBN p.213).
- Where it still works: when you control both client and server (the iTunes case) [from source] (HPBN p.214). Checklist: client and server support pipelining; the application handles aborted connections and retries; handles idempotency of aborted requests; protects itself against faulty intermediaries. The most reliable way is an HTTPS tunnel between client and server [from source] (HPBN p.214).
- Priority order of use in HTTP 1.x: pipelining only when you control the endpoints [from source] (HPBN p.259).

## 5. Multiple TCP connections and the limit of six per host

- Without multiplexing, browsers open several TCP sessions in parallel: generally up to six connections per host, on desktop and mobile [from source] (HPBN p.214). The per-origin socket pool has a maximum size of six in the major browsers [from source] (HPBN p.273).
- With six connections: up to six parallel requests on the client and the server, and the cumulative initial cwnd is multiplied by six [from source] (HPBN p.214).
- Costs: extra sockets consume memory and CPU on client, server and intermediaries; bandwidth competition between streams; implementation complexity; parallelism still limited [from source] (HPBN p.215).
- The three legitimate reasons to use multiple connections: work around HTTP, work around the low initial cwnd and work around clients without window scaling. The last two are solved by updating the kernel; cwnd was raised to 10 packets [from source] (HPBN p.215). The number six is a compromise between overhead and parallelism [from source] (HPBN p.215).
- The limit protects against unintentional DoS, but creates the inverse problem: once the six connections are saturated, the seventh request stays pending until one finishes [from source] (HPBN p.215, 216). WebSocket, Server-Sent Events and hanging XHR occupy one connection each, even when idle, and can cause self-DoS [from source] (HPBN p.216).

## 6. Domain sharding

- Idea: spread resources across subdomains `{shard1, ..., shardn}.example.com`; since the limit is per host name, parallelism increases [from source] (HPBN p.216). `[inference]` With 4 shards the ceiling goes from 6 to 24 connections (4 × 6; HPBN p.214, 216).
- Average pages have 90+ resources, which causes queues with a single host [from source] (HPBN p.216). Shards are usually CNAMEs to the same server; the limit applies to the host name, not the IP; they can also point to a CDN [from source] (HPBN p.217).
- Costs: an extra DNS lookup per hostname, extra sockets on both sides and manual management of the split [from source] (HPBN p.217).
- There is no formula for the optimal number of shards; it depends on the number and size of resources and on the client's bandwidth and latency [from source] (HPBN p.217).
- Abuse produces dozens of underused streams, many never leaving slow-start, and can worsen the experience; with HTTPS the cost rises by the TLS RTTs [from source] (HPBN p.217).
- The book's procedure: exhaust TCP tuning first; remember that the browser already opens six connections; start with zero shards, increase gradually and measure in the application's metrics. Few sites gain from more than a dozen connections; at that level, reducing or consolidating resources yields more [from source] (HPBN p.217).
- High-latency clients, such as 3G and 4G, are the most harmed by excessive sharding [from source] (HPBN p.218).
- In HTTP/2 the meaning is reversed: multiple connections (sharding) is an antipattern, because it reduces the effectiveness of header compression and prioritization [from source] (HPBN p.260).

## 7. Protocol overhead (headers and cookies)

- Each browser request carries 500–800 extra bytes of HTTP metadata, not counting cookies, which are the biggest offender; together they can add up to several KB per request [from source] (HPBN p.218).
- RFC 2616 does not limit header size, but many servers and proxies impose 8 KB or 16 KB [from source] (HPBN p.218).
- HTTP/1.x headers go in plain text and uncompressed [from source] (HPBN p.218).
- Book example: a 15-byte JSON message, with 218 bytes of headers on the request and 134 on the response, results in 352 bytes of header, 96% overhead even without cookies [from source] (HPBN p.218, 219).
- Cookies: the standard does not limit the size, but browsers generally enforce 4 KB per cookie; several cookies per origin can add up to tens of KB, and large cookies can overflow the initial cwnd and cost RTTs [from source] (HPBN p.257). In HTTP/1.x use a dedicated "cookie-free" origin for static assets [from source] (HPBN p.257).

## 8. Concatenation and spriting

- "The fastest request is the one not made"; if it cannot be eliminated, in HTTP 1.x group them: concatenation joins JS/CSS; spriting joins images and the CSS positions each part [from source] (HPBN p.219). Concatenation is safe if the execution order is maintained [from source] (HPBN p.219).
- Gains: less protocol overhead and "pipelining at the application layer" [from source] (HPBN p.220).
- Costs [from source] (HPBN p.220): all resources of the same type end up under a single URL and cache key; the bundle may contain items unnecessary for the current page; any change invalidates and re-downloads the entire bundle; JS and CSS are only parsed and executed after the transfer ends. If there is a lot of change, separate the "stable core" (frameworks and libraries) into separate bundles [from source] (HPBN p.220).
- Memory: the browser decodes the entire sprite as an RGBA bitmap, 4 bytes per pixel; width × height × 4. Example: 800 × 600 × 4 = 1,920,000 bytes, about 1.83 MB [from source] (HPBN p.221).
- JS and CSS have no incremental execution, unlike HTML; large CSS delays the CSSOM and the first paint. The PageSpeed team's test suggests 30–50 KB compressed per JS bundle as a target range, varying by case [from source] (HPBN p.221).
- Decision questions [from source] (HPBN p.222): is the application stuck on many small downloads? Does combining some of the requests help? Does the loss of cache granularity hurt the user? Do combined sprites raise memory? Does time to first render suffer from the deferred execution?
- Gmail case: separates the CSS critical for first paint from the rest, delivers JS in smaller chunks for incremental execution, updates JS in the background (background preloading) to avoid self-inflicted DoS and injects critical CSS and JS into the HTML itself [from source] (HPBN p.222).

## 9. Resource inlining

- Reduces requests by embedding the resource: JS and CSS in `script`/`style` blocks; other types via `data:` URI [from source] (HPBN p.222). Example of a 1×1 GIF in base64 and a 32 KB limit for data URIs in IE8 [from source] (HPBN p.223).
- An inlined resource is not cacheable on its own (browser, CDN or proxy); if repeated across several pages, it is retransmitted on each one; if it changes, it invalidates all the pages that contain it [from source] (HPBN p.223).
- Non-text requires base64, which expands the bytes by 4/3, about 33% [from source] (HPBN p.223).
- Rule of thumb: consider inlining below 1–2 KB, where the HTTP cost exceeds that of the resource [from source] (HPBN p.223). Criteria: small and specific to one page, inline; small and reused across pages, bundle; small with a high update frequency, keep separate; reduce the size of cookies [from source] (HPBN p.223).

## 10. Optimization order in HTTP 1.x

1. Configure the server with the best TCP and TLS; then apply the evergreen and mobile practices; measure and iterate [from source] (HPBN p.259).
2. Only then evaluate the 1.x-specific optimizations: pipelining (if you control both ends), sharding (if the limit of six is the bottleneck), bundling and inlining of small resources; all can hurt if overdone, and "be wary of one-size-fits-all advice" [from source] (HPBN p.259).
3. Consider migrating to HTTP 2.0, which eliminates the need for most of these techniques [from source] (HPBN p.259). In HTTP/2: one connection per origin, remove unnecessary concatenation and spriting, and replace inlining with server push [from source] (HPBN p.260, 261).
4. Transition strategy (same code on 1.x and 2.0): first remove the sharding; then undo the bundles as users migrate [from source] (HPBN p.262).

## [DATED] summary

- Pipelining "generally turned off" and HTTP 2.0 as a draft in progress, with SPDY as the production version (HPBN p.213, 260).
- Sharding, sprites, concatenation and inlining as necessary practices (HPBN p.206, 259); with HTTP/2 they become antipatterns (HPBN p.260, 261).
- 32 KB data URI limit in IE8 (HPBN p.223).
- 2013 page averages (90 requests, 15 hosts, 1,311 KB; HPBN p.187).

## After the book [extrapolation]

- HTTP/2 was standardized (RFC 7540, then RFC 9113) and HTTP/3 runs over QUIC; the book's caveat about migration and dual-protocol applies as historical context.
- The six-connections-per-host limitation continues in HTTP/1.1; in HTTP/2 and HTTP/3 the recommendation is to consolidate origins and avoid sharding.
- Bundling remains useful in moderation: the number of modules and granular caching are still trade-offs, but a "single giant bundle" is no longer the rule.

## What the source does not cover

- Modern measurements of HTTP/2 or HTTP/3 adoption, or of pipelining in current proxies.
- Header compression in HTTP/1.x (it does not exist); HPACK is covered in the HTTP/2 chapters.
- Current per-browser connection limit values beyond the 2013 "six per host".
- Bundling strategy with ES modules, tree-shaking or code splitting.
- Optimal sprite size on high-density screens.
