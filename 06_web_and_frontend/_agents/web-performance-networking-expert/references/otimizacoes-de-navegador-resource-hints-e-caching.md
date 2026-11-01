# Browser optimizations, resource hints and caching

Convention: every cited page is the PDF page (`HPBN p.N`); the printed one is N − 18. Labels: `[from source]`, `[inference]`, `[DATED]`, `[extrapolation]` (the latter only in the final section).

**Source limits.** The book covers caching in a few lines: `Cache-Control` with `max-age`, `Last-Modified` and `ETag`. It does not explain `no-store`, `private`/`public`, `immutable`, or the `If-None-Match`/304 flow (text search with no hits); `no-cache` only appears inside response examples. Those details are in "After the book". The book also has neither `preconnect` nor `preload` as a link `rel`; what it has is `dns-prefetch`, `subresource`, `prefetch` and `prerender`.

When to open: deciding what the browser does on its own, which hints to insert in the HTML, how to configure resource caching, and when browser optimizations help or hurt. For the render pipeline, see `critical-rendering-path-dom-cssom-e-layout.md`; for bundling and inlining, `http1x-keepalive-pipelining-e-sharding.md`.

---

## 1. What the browser already does for you

- A modern browser is more than a socket manager; performance is a competitive differentiator and it does DNS pre-resolution, pre-connection, prefetching and prioritization of critical resources [from source] (HPBN p.201).
- Two classes of optimization [from source] (HPBN p.201):
  - Document-aware: the network stack integrates with the document, CSS and JS parsers to identify and prioritize critical assets, dispatch them early and bring the page to an interactive state (resource priorities, look-ahead parsing).
  - Speculative: the browser learns navigation patterns and tries to predict actions (pre-resolving DNS, pre-connecting to likely hosts).
- Four common techniques [from source] (HPBN p.201, 202):
  1. Resource prefetching and prioritization: resources that block first render get high priority, and low-priority requests may be held in a queue.
  2. DNS pre-resolve: of likely hosts, triggered by learned history, by an action such as hovering over a link, or by other page signals.
  3. TCP pre-connect: after DNS, the browser can open TCP speculatively; if it guesses right, it eliminates a whole RTT (the handshake).
  4. Page pre-rendering: rendering the entire page in a hidden tab, to swap it in instantly when the user navigates.
- Typical result: hundreds of milliseconds of network latency saved, automatically [from source] (HPBN p.201). Understanding the mechanisms lets you help the browser [from source] (HPBN p.201).
- Chrome: learns the topology of visited sites and navigation patterns; a simple hover over a link can trigger the network stack's "predictor" [from source] (HPBN p.274).
- Socket pools: sockets are kept in pools grouped by origin; pending requests are queued, prioritized and bound to sockets of the pool; unless the server closes it, the same socket is reused [from source] (HPBN p.272). Origin = protocol + domain + port; all major browsers limit the pool to six sockets [from source] (HPBN p.273).
- Benefits of this architecture: serving the queue by priority, reusing sockets, opening sockets proactively, optimizing the closing of idle sockets and bandwidth allocation [from source] (HPBN p.273).
- The application only handles URL and data; the browser formats the request and manages the connection lifecycle (principle of least privilege) [from source] (HPBN p.275). Connection limits, formatting, TLS and same-origin are enforced by it [from source] (HPBN p.274).

## 2. Hints in the HTML (what the book documents)

Syntax and semantics (hosts and paths below are fictitious; the book uses four equivalent lines) [from source] (HPBN p.202):

```html
<link rel="dns-prefetch" href="//cdn.exemplo.com.br">
<link rel="subresource"  href="/js/app.js">
<link rel="prefetch"     href="/img/banner-grande.jpg">
<link rel="prerender"    href="//loja.exemplo.com.br/proxima.html">
```

- `dns-prefetch`: pre-resolves the hostname.
- `subresource`: prefetches a critical resource found later on this page.
- `prefetch`: prefetches a resource for this navigation or a future one.
- `prerender`: prerenders a page in anticipation of the user's next destination.
- They are speculative hints: the browser does not guarantee to act, but may use them. If it does not support them, they are treated as a harmless no-op; use them where possible [from source] (HPBN p.202).
- Each extra RTT of DNS, TCP or TLS costs tens to hundreds of ms; helping the browser anticipate them removes bottlenecks [from source] (HPBN p.203).

Support in 2013 (Table 10-2) [from source] (HPBN p.203):

| Browser | dns-prefetch | subresource | prefetch | prerender |
| :--- | :--- | :--- | :--- | :--- |
| Firefox | 3.5+ | n/a | 3.5+ | n/a |
| Chrome | 1.0+ | 1.0+ | 1.0+ | 13+ |
| Safari | 5.01+ | n/a | n/a | n/a |
| IE | 9+ (as `prefetch`) | n/a | 10+ | 11+ |

- `[DATED]` The whole table and the existence of `subresource` (HPBN p.203). In IE 9 DNS prefetch was called `prefetch`; from IE 10 on `dns-prefetch` and `prefetch` are equivalent to a DNS prefetch in both cases [from source] (HPBN p.203).

## 3. Resource scheduling: help and don't hinder

- The browser determines the loading order on its own; we can help with hints and hinder by hiding resources from it [from source] (HPBN p.258).
- Preload scanner: when the parser is blocked, it looks ahead and dispatches downloads early; it only works in that situation, yielded about 20% in Chrome tests, and does not see resources scheduled by JavaScript [from source] (HPBN p.258).
- Early HTML flush: the server should flush the available markup as fast as possible; Google Search sends the static header before parsing the query [from source] (HPBN p.203).
- Gmail preloads updated files in the background while the user works with the old version, repeating this one or more times a day [from source] (HPBN p.222).

## 4. Client-side caching: what the book prescribes

- "The fastest request is the one not made": keep a cache of data already downloaded [from source] (HPBN p.254).
- Headers [from source] (HPBN p.254): `Cache-Control` specifies the resource's lifetime (`max-age`); `Last-Modified` and `ETag` provide validation.
- Rule: always set an explicit lifetime and a validation mechanism. Providing only one of the two yields redundant transfers (without validation) or revalidation on every use (without lifetime) [from source] (HPBN p.254).
- Souders' rule: `Expires` defines the object's lifetime and eliminates the request; `ETag` and `Last-Modified` give efficient revalidation (fingerprint or date stamp) [from source] (HPBN p.206).
- The browser evaluates cache directives, revalidates expired resources when possible and manages size and eviction; the server's part is to return `Cache-Control`, `ETag` and `Last-Modified` on all resources [from source] (HPBN p.275).
- Before dispatching, the browser consults the cache, validates and returns the local copy; if there is none, it fetches from the network and stores the response, if allowed [from source] (HPBN p.275).
- Response examples in the book: `Cache-Control: max-age=0, no-cache` alongside `Expires` equal to the response date, on dynamic HTML; `Cache-Control: max-age=315360000` with `Expires` in 2037 and a weak `ETag` (`W/...`) on a favicon [from source] (HPBN p.177, 178).
- Caching on smartphones (AT&T Labs and Univ. of Michigan, MobiSys 2012): redundant transfers add up to 18% and 20% of HTTP traffic in the two datasets, and 17% of bytes, 7% of radio energy, 6% of signaling and 9% of radio resource utilization in the second dataset. The causes: cache implementations that do not follow the specification or developers who do not use the libraries' support [from source] (HPBN p.255). Review the application and add tests to catch regressions [from source] (HPBN p.255).
- Interaction with HTTP/1.x optimization: an inlined resource is not individually cacheable; a bundle is invalidated entirely on each change; splitting the "stable core" into a separate bundle improves caching [from source] (HPBN p.220, 223).
- Caching and application protocol choice: low-latency protocols such as SSE and WebSocket may fail the criterion of taking advantage of the browser cache [from source] (HPBN p.276).

## 5. Bytes and requests that never need to leave

Evergreen practices [from source] (HPBN p.253, 254):

- Reduce DNS lookups; reuse TCP connections (keep-alive); minimize redirects (the ideal number is zero); use a CDN; eliminate unnecessary resources.
- Cache on the client; compress in transfer; eliminate unnecessary request bytes; parallelize request and response processing; apply protocol-specific optimizations.
- Compression: Gzip reduces text assets by 60–80% on average; images are more than half the bytes of an average page; strip metadata, resize on the server, choose the right format and use lossy compression whenever possible [from source] (HPBN p.255). The wrong format (for example PNG for a photo) can cost hundreds or thousands of KB [from source] (HPBN p.255, 256).
- WebP (2013): lossless 26% smaller than PNG; lossy 25–34% smaller than JPEG; lossless transparency with 22% more bytes; decoding about 1.4× the CPU time of JPEG; supported in Chrome and Opera [from source] (HPBN p.256). `[DATED]` the limited support to Chrome and Opera (HPBN p.256).
- Resizing an image on the client penalizes CPU, GPU and memory [from source] (HPBN p.256).
- Cookies: monitor the size; send the minimum (a secure session token) and use a server-side session cache; avoid cookies on requests for static assets [from source] (HPBN p.257). In HTTP/1.x, use a dedicated cookie-free origin [from source] (HPBN p.257).

## 6. Decision: HTTP/1.x versus HTTP/2 for these optimizations

- In HTTP 1.x apply, in this order, pipelining (if you control the endpoints), sharding, bundling and small inlining, measuring the effect [from source] (HPBN p.259).
- In HTTP/2: one connection per origin; remove concatenation and spriting; swap inlining for server push so that each resource is cached individually and reused across pages [from source] (HPBN p.260, 261).
- Server minimum for HTTP 2.0: initial cwnd of 10 segments, TLS with ALPN (NPN for SPDY) and TLS session resumption [from source] (HPBN p.260). `[DATED]` NPN/SPDY as 2013 context (HPBN p.260).

## After the book [extrapolation]

- `preconnect`: opens DNS, TCP and TLS ahead of time, with `crossorigin` for fonts; `preload`: fetches a critical resource with high priority, with `as=`. `prefetch` is low priority today. `prerender` was replaced by Speculation Rules. `subresource` was removed.
- `Cache-Control` details (RFC 7234, later RFC 9111): `no-cache` requires revalidation before reuse, `no-store` forbids storing, `private` and `public` define whether shared caches may store it, `immutable` and `stale-while-revalidate` refine freshness. Conditional validation: `If-None-Match` with `ETag` returns `304 Not Modified`, with no body.
- For assets with a hash in the name, a one-year `max-age` with `immutable` is common practice.
- Service Workers, `Cache Storage`, `fetchpriority`, Early Hints (103) and HTTP/3 came later.
- Core Web Vitals (LCP, INP, CLS) are the current measurement vocabulary.

## What the source does not cover

- The `no-store`, `private`, `public`, `must-revalidate`, `immutable` directives and the detailed flow of conditional revalidation with 304.
- Freshness heuristics when there is no `max-age` or `Expires`.
- `rel=preconnect`, `rel=preload`, `fetchpriority` and fetch priorities by resource type.
- Offline application cache, Service Workers and `Cache Storage`.
- Site-partitioned cache keys and `Vary`.
