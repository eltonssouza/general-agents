# HTTP 2.0 (2013 draft): header compression and server push

The file name was kept for compatibility, but the book **does not use the term HPACK**: it speaks of "header compression" done with "header tables" and differential encoding. This file covers header compression, server push, the push × inlining comparison and the server's role in prioritization. Cited pages are the **PDF** pages (printed = PDF − 18). Prioritization itself (31-bit priority, server strategy) is in the file `http2-binary-framing-multiplexing-e-streams.md`, section 6.

**[DATED]** Everything here describes the 2013 draft; the book warns that low-level details, field names and encoding may change (HPBN p.226, 229).

## 1. Header compression

### Motivation

- In HTTP 1.x the metadata always travels in plain text and adds up to 500 to 800 bytes per request, and kilobytes more when there are cookies (HPBN p.240). The same calculation appears in the HTTP 1.x chapter, which also says that cookies are the biggest offender and that the overhead can exceed the payload of a JSON API by an order of magnitude (HPBN p.218).
- Reducing this overhead is one of the three central goals of HTTP 2.0, along with multiplexing and prioritization/push (HPBN p.225).

### Draft mechanism: header tables (HPBN p.240-241)

- Instead of resending the same data on every request and response, client and server maintain "header tables" that store the key-value pairs already sent.
- The tables are valid for the entire connection and are updated incrementally by both sides.
- Each new pair is added to the table or replaces a previous value.
- Since both sides know what has already been sent, a new set of headers is encoded as a simple **difference** from the previous one (Figure 12-5).
- In the book's example, the second request only needs to communicate the path header that changed; everything else is inherited from the previous working set (HPBN p.241).
- Pairs that almost never change (user-agent, accept etc.) are transmitted only once. If nothing changes between two requests (for example, polling the same resource), the header cost is zero bytes (HPBN p.241).
- The book does not describe a predefined static table, numeric indexing, maximum table size or Huffman coding. For the full algorithm, it refers to `draft-ietf-httpbis-header-compression` (HPBN p.242).

### Header format changes (HPBN p.241)

- **[DATED]** The definitions of the request and response fields remain, with few exceptions: all keys become lowercase and the request line is split into the pairs `:method`, `:scheme`, `:host` and `:path`.
- The book does not list `:status` or `:authority` in this passage; `:host` is the draft's name.

### SPDY, CRIME and the change of algorithm (HPBN p.242)

- The first versions of SPDY compressed all headers with zlib and a custom dictionary, reducing header volume by 85% to 88%.
- The SPDY whitepaper cited by the book reports, on a 375 Kbps upload DSL link, gains of 45 to 1142 ms in load time from request header compression alone.
- In the summer of 2012 the "CRIME" attack against TLS and SPDY compression algorithms was published, capable of leading to session hijacking. zlib was disabled and ended up replaced by the index-table algorithm described above, which solves the security problem and, in practice, yields comparable performance.
- The book does not explain the CRIME mechanism; it only presents it as the reason for the change.

### Practical effects

- A single connection favors compression, because there is a single compression context (HPBN p.235).
- Using several connections (domain sharding) reduces the effectiveness of header compression and prioritization (HPBN p.260).
- With the per-request overhead reduced, the need for bundling largely disappears; even so it does not reach zero (HPBN p.261).
- Cookies: in 1.x they remain uncompressed; in 2.0 there is compression, but the potential overhead is still high, and large cookies can cost round trips by overflowing TCP's initial congestion window. The recommendation is to send the minimum (such as a session token), keep the rest on the server and avoid cookies on static resources (HPBN p.257).
- The general recommendation to reduce request bytes, such as cookies, holds in any protocol version (HPBN p.254).

## 2. Server push

### Concept and benefits

- It is the server's ability to send multiple responses to a single client request: besides the requested response, it pushes additional resources without the client asking for them (HPBN p.237).
- Motivation: a typical application has dozens of resources, discovered by the client when parsing the document. The server already knows which will be needed, so it can send them ahead of time and eliminate latency (HPBN p.238).
- The book recalls that anyone who has inlined CSS, JS or another resource via data URI has, in practice, done a manual push (HPBN p.238).
- With push in the protocol, the flow leaves the application and gains benefits (HPBN p.238):
  - the client can cache the pushed resource;
  - the client can decline it;
  - it can be reused across different pages;
  - the server can prioritize it.
- Pushed resources follow the same-origin policy: the server cannot push arbitrary third-party content, only content it is authoritative for (HPBN p.239).
- The SETTINGS exchanged at the opening can limit the maximum number of concurrent streams in both directions; **[DATED]** through this limit the client restricts pushed streams or disables push by setting the value to zero (HPBN p.238).

### `PUSH_PROMISE` (HPBN p.239, 247)

- Every push stream begins with a `PUSH_PROMISE` frame, which signals the server's intent to send the described resource, in addition to the response to the original request. The frame carries only the HTTP headers of the promised resource (HPBN p.239).
- At the frame level, `PUSH_PROMISE` is almost identical to a `HEADERS`, swapping the priority value for a "promised stream ID" (HPBN p.247).
- On receiving the `PUSH_PROMISE`, the client can decline the stream, for example if the resource is already in the cache. The book cites this as an important improvement over 1.x. The book does not specify the frame or error code used to decline; it only describes `RST_STREAM` as the signal for abnormal stream termination (HPBN p.239, 245). [inference] This is the path by which the refusal should be made.
- Restrictions (HPBN p.239):
  - the server respects the request-response cycle and only pushes in response to a request; it does not open push streams at will;
  - the `PUSH_PROMISE` frames must go out **before** the response, to avoid a race with the client (for example, the client requesting the same resource the server was about to push).
- Parity of the promised ID: on p.247 the server's IDs are odd, but this passage contradicts the analysis of Figure 12-9 (p.249), in which odd IDs belong to the client. Note the contradiction and do not state the parity as a fact of the book (see the other file, section 10).

### How the server decides what to push (HPBN p.239-240)

The standard defines no algorithm; the book lists three families of strategies, not a complete list:

1. The application initiates the push in its own code: full control, but tight coupling to the HTTP 2.0 server used.
2. The application tells the server, through an extra header, the associated resources: decouples from the server API. Book example: Apache's mod_spdy looks for the `X-Associated-Content` header.
3. The server learns on its own: it parses the document and infers the resources, or analyzes traffic (for example, collecting dependencies through the Referer header) and starts pushing the critical resources.

- A smarter strategy can infer what is in the cache through its own model, the client's cookie or another mechanism, instead of always pushing the same resources (HPBN p.240).
- Pushed resources go straight into the client's cache, as if it had requested them. There is no client API or JavaScript callback that notifies of a push arrival; the mechanism is transparent to applications in the browser (HPBN p.240).

### Push × inlining

- Inlining is a "forced push": the client can neither cancel it nor cache the inlined resource individually (HPBN p.239).
- Push makes most 1.x inlining uses obsolete. Inlining only continues to make sense if the resource is used on a single page and has no high encoding cost; in the other cases, the application should use server push (HPBN p.239).
- Chapter 13: most resources that were inlined in 1.x can and should go by push, so each is cached separately and reused across pages, instead of being embedded in each document (HPBN p.261). Push also improves caching at no extra network cost (HPBN p.261).
- The book says push can bring the greatest benefit to mobile clients, because of the high cost of round trips on 3G and 4G (HPBN p.261).
- In the two-phase migration, the book proposes: first eliminate sharding; then, as the 2.0 user base grows, undo bundling and use push where possible (HPBN p.262).

### Quality server (HPBN p.265)

- A 2.0 server must support push and ideally offer different implementations of push strategy; without that, the application loses the benefit.
- Servers vary in push mechanisms and strategies; application performance is tied to the quality of the chosen server.

## After the book [extrapolation]

Nothing below comes from HPBN or has a page.

- [extrapolation] The 2013 draft's header compression became, in the final version of HTTP/2, **HPACK** (RFC 7541, 2015), which uses a 61-entry static table, a per-connection dynamic table and Huffman coding; the name HPACK does not appear in the book.
- [extrapolation] RFC 7540 replaced `:host` with `:authority` and included `:status` among the response pseudo-headers.
- [extrapolation] Disabling push came to be done through the `SETTINGS_ENABLE_PUSH` parameter, and not through a zeroed concurrent-stream limit; the client declines a push with `RST_STREAM`.
- [extrapolation] In practice server push fell into disuse: it was little adopted and browsers such as Chrome removed it; alternatives such as `103 Early Hints` and `preload` took its place. This runs against the book's enthusiasm for push as a replacement for inlining.
- [extrapolation] The idea of "guessing the client's cache" (cookies, own model) cited on p.240 motivated cache digest proposals, which did not become stable practice.

## What the source does not cover

- Detailed compression algorithm: tables, indexes, maximum table size, integer and literal encoding (the book refers to the IETF draft, p.242).
- The technical mechanism of the CRIME attack.
- Static table, Huffman coding and the name HPACK.
- The exact frame or error code to decline a push; a flag to disable push in the style of the final specification.
- Push strategies in production beyond the three families described, and real measurements of push gain or bandwidth waste.
- Protection against "over-pushing" resources already in cache: the book only mentions the possibility of inferring the cache (p.240) and refusal by the client (p.239).
- Historical trail after 2013: RFC 7540/7541, HTTP/3 and the removal of push from browsers.
