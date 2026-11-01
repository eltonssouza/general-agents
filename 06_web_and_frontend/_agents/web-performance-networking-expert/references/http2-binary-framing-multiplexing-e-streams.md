# HTTP 2.0 (2013 draft): binary framing, streams, multiplexing, priority and flow control

This file summarizes chapter 12 of *High Performance Browser Networking* (HPBN) and the HTTP 2.0 parts of chapter 13. The cited pages are the **PDF** pages (printed = PDF − 18). Chapter 12 occupies PDF pages 225–250; the HTTP 2.0 section of chapter 13 runs from pages 259 to 268.

## 0. Dating notice: the book describes a draft

- **[DATED]** The author himself warns that the standard is under construction: architecture and principles are defined, but low-level details may change, which is why the chapter only glances at the wire format (HPBN p.226).
- **[DATED]** The text cites the "Draft 4" of HTTP/2.0 and says that the bit encoding of each frame and the field names may change (HPBN p.229). Elsewhere the book also cites "Draft 2" (HPBN p.235, 236).
- **[DATED]** Schedule expected at the time: first implementation draft in July 2013, working group last call in April 2014 and submission to the IESG in November 2014 (HPBN p.228).
- Therefore the frame names, the header size and the fields below follow the book's draft, not the final specification. See the section "After the book".

## 1. SPDY and the road to HTTP 2.0

- SPDY is an experimental Google protocol, announced in mid-2009, to reduce page load time by attacking known limitations of HTTP 1.1 (HPBN p.226).
- SPDY goals: reduce load time (PLT) by 50%, require no change to site authors' content, keep deployment complexity low, develop with the open source community and collect real data to validate the experiment (HPBN p.226).
- To do so, SPDY introduced a binary framing layer to multiplex, prioritize and cut unnecessary latency (HPBN p.226).
- Lab result published by Google engineers: when downloading the 25 most popular sites over simulated home networks, pages loaded up to 55% faster (HPBN p.226).
- By 2012 SPDY already ran in Chrome, Firefox and Opera and was offered by major sites; the HTTP-WG opened the HTTP 2.0 effort in early 2012 (HPBN p.226-227).
- SPDY was adopted as a starting point, but "SPDY is not HTTP 2.0": the official standard had received and would continue to receive changes (HPBN p.227).
- SPDY version 2 was the base adopted in the summer of 2012. SPDY kept evolving in parallel as a test bed: v3 (2012) brought a new framing format and the first version of flow control; v4 was expected for 2013–2014 with framing revised once more, better priority, flow control and push (HPBN p.228-229).
- When HTTP 2.0 was ready, SPDY would be retired (HPBN p.229).
- The jump to "2.0" is due to the new binary framing layer, incompatible with 1.x clients and servers (HPBN p.228).

## 2. Goals and what does not change

- Main goals: less latency with full request and response multiplexing, less overhead with efficient compression of header fields, and support for prioritization and server push (HPBN p.225).
- The working group's charter asks for a measurable improvement in perceived latency, a fix for HTTP's head-of-line (HoL) blocking, parallelism without multiple connections (better use of TCP and congestion control), preservation of HTTP 1.1 semantics and a clear definition of coexistence with 1.x, especially in intermediaries (HPBN p.227).
- Application semantics do not change: methods, status codes, URIs and header fields remain; only how the data is formatted and transported changes. That is why existing applications work without modification (HPBN p.225).
- HTTP 1.x was designed to be simple to implement, at the cost of performance; 2.0 fills that gap (HPBN p.229).
- For those who do not write a server or client over raw TCP sockets, the framing is invisible; the noticeable difference tends to be only new, optional APIs, such as server push (HPBN p.228).

## 3. Binary framing layer

- It is the basis of all the gains: it defines how HTTP messages are encapsulated and transferred between client and server (HPBN p.229).
- It sits between the sockets interface and the HTTP API seen by the application: verbs, methods and headers stay the same, only the encoding in transit changes (HPBN p.230).
- Unlike HTTP 1.x in newline-delimited text, all communication is divided into messages and frames encoded in binary (HPBN p.230).
- Both sides must use this encoding: a 1.x client does not understand a 2.0-only server, and vice versa (HPBN p.230).
- The book compares it with HTTPS: encryption and decryption happen transparently, without changing the application (HPBN p.230).
- Advantage of length-prefixed binary: a more compact representation and easier, more efficient processing; the parser jumps straight to the next frame, a large gain over 1.x (HPBN p.244-245).

## 4. Streams, messages and frames

Chapter terminology (HPBN p.230-231):

- **Stream**: bidirectional flow of bytes within an established connection.
- **Message**: complete sequence of frames that corresponds to a logical message.
- **Frame**: smallest unit of communication; every frame has a header that identifies at least the stream it belongs to.

Consequences (HPBN p.231-232):

- A connection carries any number of bidirectional streams; each stream exchanges messages made of one or more frames, which can be interleaved and reassembled by the stream identifier present in each frame (HPBN p.231).
- All communication uses a single TCP connection; each stream has a unique integer identifier (1, 2, …, N); a message is a logical request or response; a frame carries a specific type of data (HTTP headers, payload etc.) (HPBN p.232).
- Figure 12-2 shows the relationship between stream, message and frame, not the actual encoding on the wire (HPBN p.231).

## 5. Request and response multiplexing

- In HTTP 1.x, parallelism requires several TCP connections because only one response at a time goes out on each connection (response queue); this causes HoL blocking and inefficient use of TCP (HPBN p.232).
- In 2.0, client and server break the message into independent frames, interleave them and reassemble them on the other side (HPBN p.232).
- In Figure 12-3, the client sends a DATA frame of stream 5 while the server interleaves frames of streams 1 and 3; there are three exchanges in flight at the same time (HPBN p.232-233).
- The book calls this the most important improvement of HTTP 2.0. Effects: interleave several requests and several responses without mutual blocking, use a single connection, reduce load time and do away with 1.x workarounds (HPBN p.233).
- With multiplexing, the reasons for file concatenation, sprites and domain sharding fall away; fewer TCP connections also reduce CPU and memory on client and server (HPBN p.233).

## 6. Request prioritization

- With the message split into frames, the delivery order can be optimized. In the draft, each stream receives a **31-bit** priority value: 0 is the highest priority and 2^31 − 1 the lowest (HPBN p.233).
- With this the server controls allocation of CPU, memory and bandwidth and gives precedence to higher-priority frames (HPBN p.233-234).
- Not every resource is worth the same: HTML builds the DOM, CSS builds the CSSOM, JavaScript can block both, and images tend to have lower priority. Browsers already prioritize by type, position on the page and even the history of previous visits (HPBN p.234).
- In HTTP 1.x the browser cannot tell the server the priority; it only has the up to six parallel connections per origin, and requests wait in a queue on the client. Pipelining tried to help, but did not catch on (HPBN p.234).
- In 2.0 the browser dispatches each request as soon as it discovers it, indicates the priority and lets the server decide the delivery, with no queue on the client (HPBN p.234).
- The standard does not define a prioritization algorithm: only the exchange mechanism. Priorities are hints, and quality varies by implementation. Since the developer rarely controls the client but does control the server, the book advises choosing the server carefully (HPBN p.234).
- Two bad extremes: ignoring priorities can block rendering by sending images while the browser waits for CSS and JS; strict ordering can reintroduce HoL (one slow request stalling the rest). The server should interleave frames of different levels, giving precedence to the higher ones but mixing levels to make use of the connection (HPBN p.234-235).
- The `PRIORITY` frame is used to assign or reassign the priority of a referenced resource (HPBN p.245).

## 7. One connection per origin; packet loss and HoL in TCP

- With no need for multiple connections, all 2.0 connections are persistent and a single one should be used between client and server (HPBN p.235).
- Lab data cited from Draft 2: fewer connections bring a consistent latency benefit and the total number of packets can drop by up to 40% relative to HTTP; many simultaneous connections are also a scaling problem on the server (HPBN p.235).
- Benefits listed: consistent prioritization across all streams, better compression by using a single context, less impact on the network from fewer TCP connections, and less time in slow-start with faster recovery from losses (HPBN p.235).
- HTTP is made of short, bursty transfers, and TCP is optimized for long, bulky transfers; reusing the connection brings the two closer (HPBN p.235).
- **Drawbacks**: HTTP's HoL is gone, but HoL at the TCP level remains (mechanism on HPBN p.48: in-order delivery; a lost packet holds the following ones in the receive buffer until retransmission; p.236 refers back to that section); the bandwidth-delay product limits throughput if window scaling is off; and packet loss reduces the congestion window, dragging down the maximum throughput of the entire connection (HPBN p.236).
- Even so, measurements up to then indicated that a single connection is the best strategy, since the negative effects of HoL (even with losses) are outweighed by the gains of compression and prioritization (HPBN p.236).
- Removing one bottleneck reveals the next; in 2.0 the next may be TCP, and that is why a well-tuned TCP stack on the server is critical. Research cited: TCP Fast Open, Proportional Rate Reduction and a larger initial window. 2.0, like its predecessors, does not mandate TCP; UDP is not out of the question (HPBN p.236).
- [inference] This links this file to the TCP fundamentals one: the 2.0 gain depends on the initial cwnd and on loss handling on the server.

## 8. Flow control

- Multiplexing streams on the same connection creates contention for bandwidth; priorities define relative order, but are not enough to control resource allocation among streams (HPBN p.236).
- Draft rules (HPBN p.237):
  - control is hop-by-hop, not end to end;
  - it is based on window update frames: the receiver advertises how many bytes it accepts per stream and for the whole connection;
  - the `WINDOW_UPDATE` frame carries the stream ID and the window increment;
  - it is directional: the receiver chooses whatever window it wants for each stream and for the connection;
  - **[DATED]** the receiver can turn off flow control, per stream or for the entire connection.
- When the connection opens, the two ends exchange `SETTINGS` frames that define the window sizes in both directions (HPBN p.237).
- The mechanism is practically the same as TCP's flow control, but TCP does not distinguish the streams of a 2.0 connection, so it alone is not enough (HPBN p.237).
- The standard does not define the algorithm, values or when to send `WINDOW_UPDATE`; that is left to the implementer. Advertising a smaller window on a stream limits its delivery rate (HPBN p.237).
- Flow control applies only to `DATA` frames; the stream metadata travels separately and may have a different priority (HPBN p.248).

## 9. The draft's frame header: 8 bytes

- **[DATED]** All frames share a common **8-byte** header with length, type, flags field and a 31-bit stream identifier (HPBN p.244-245).
- Fields (Figure 12-6, HPBN p.245):
  - **16-bit** length prefix: a frame carries up to 2^16 − 1 bytes (about 64 KB), not counting the 8-byte header;
  - 8-bit type field, which defines how the rest is read;
  - 8-bit flags field, whose meanings are specific to each frame type;
  - 1-bit reserved field, always 0;
  - 31-bit stream identifier.
- Types defined in the draft, with the book's names (HPBN p.245-246):
  - `DATA`: body of HTTP messages;
  - `HEADERS`: additional header fields of a stream;
  - `PRIORITY`: assign or reassign priority;
  - `RST_STREAM`: signal abnormal termination of a stream;
  - `SETTINGS`: configuration of how the two sides can communicate;
  - `PUSH_PROMISE`: promise to create a stream and serve the referenced resource;
  - `PING`: measure the round-trip time and check that the peer is alive;
  - `GOAWAY`: ask the peer to stop creating streams on that connection;
  - `WINDOW_UPDATE`: flow control per stream or per connection;
  - `CONTINUATION`: continue a sequence of header block fragments.
- `GOAWAY` reports the last processed stream ID, which eliminates races and lets the browser retry or cancel in-flight requests; it is necessary to multiplex safely (HPBN p.246).
- The book uses only fixed-size fields. Even halving the overhead with variable size, the gain in a 1,400-byte packet at 1 Mbps would be 4 bytes (0.3%) and less than 100 ns, not worth the parser complexity (HPBN p.247).
- The numeric values of the types, the flag values and other draft details do not appear in the book; only the `END_STREAM` flag is cited (HPBN p.248).

## 10. Starting streams, sending data and analyzing the flow

- Before any data, the stream must be created and metadata sent (priority and HTTP headers). Client and server can both start streams (HPBN p.247).
- The client opens a request with `HEADERS`, which carries the common header with the new stream ID, an optional 31-bit priority and the HTTP key-value pairs in the payload (HPBN p.247).
- The server starts a push stream with `PUSH_PROMISE`, almost identical to `HEADERS`, but with a "promised stream ID" in place of the priority (HPBN p.247).
- Both only communicate the metadata; the payload goes in `DATA` frames. When there is a payload, it can be split across several `DATA` frames, and the last one sets the `END_STREAM` flag (HPBN p.247-248).
- `DATA` applies no encoding or compression to the payload: gzip, image format etc. are up to the application or server. The frame is the 8-byte header plus the payload (HPBN p.248).
- The length field would allow 2^16 − 1 bytes, but the draft requires `DATA` not to exceed 2^14 − 1 (16383) bytes, to reduce HoL; larger messages are fragmented (HPBN p.248).

### Stream ID parity: internal contradiction in the book

- On p.247 the text says that client-initiated streams have **even** IDs and server ones have **odd** IDs, and that the offset avoids collisions (HPBN p.247).
- In the analysis of Figure 12-9 (p.249), the book states that streams 1, 3 and 5 are all odd and, therefore, **client-initiated**; there are no server streams (HPBN p.249). Figure 12-3 and the text of p.232 also treat 1 and 3 as client request streams (HPBN p.232).
- Conclusion: the two passages are incompatible. It cannot be resolved with the book alone; the agent must record the inconsistency and not assert the parity as a fact "from the book". [extrapolation] RFC 7540 fixed client = odd and server = even, which agrees with p.249 and disagrees with p.247.

### Reading Figure 12-9 (HPBN p.249)

- Three active streams (1, 3, 5); the server sends several `DATA` frames of stream 1 (the response, which indicates the response `HEADERS` came earlier), interleaves `HEADERS` and `DATA` of stream 3 and the client sends `DATA` on stream 5.
- The book's conclusion: the connection multiplexes three streams in parallel, in different phases; the server decides the frame order and a large stream (video) does not block the others (HPBN p.249).
- PDF page 250 has no extracted text (apparently only a figure or a blank page).

## 11. Upgrade, discovery and ALPN

- The migration will not be instantaneous: servers and intermediaries need to be updated and 1.x would persist for at least a decade, so the client must discover whether the server and intermediaries speak 2.0 (HPBN p.242).
- Three cases: a new HTTPS connection with TLS and ALPN, a new HTTP connection with prior knowledge and a new HTTP connection without prior knowledge (HPBN p.242).
- **TLS + ALPN**: support is negotiated during the normal HTTPS handshake and, since cutting latency is a central criterion, ALPN is always used in HTTPS (HPBN p.243).
- **Cleartext HTTP (port 80)**: without other information, the client uses the HTTP Upgrade mechanism. The 1.1 request carries `Connection: Upgrade, HTTP2-Settings`, `Upgrade: HTTP/2.0` and `HTTP2-Settings` with the SETTINGS payload in Base64 URL. The server either responds in 1.1 (declines) or returns `101 Switching Protocols` and moves to the new framing, with no extra round trip (HPBN p.243).
- Both also send a "connection header" (a byte sequence defined in the standard), which works as a quick check against intermediaries that accept the upgrade without understanding the protocol; cost of only a few bytes (HPBN p.244).
- The client may already know of the support by other means (DNS record, manual configuration) and send 2.0 frames directly over an unencrypted channel; in the worst case it falls back to Upgrade or to a TLS tunnel with ALPN (HPBN p.244).
- Prior knowledge does not guarantee a reliable connection, because in cleartext the support must exist end to end. 2.0 does not require TLS, but in practice TLS is the most reliable way to deploy; the ideal is to start with TLS + ALPN and also offer Upgrade (HPBN p.244).
- In chapter 13: the first HTTP 2.0 deployments will need an encrypted channel because of incompatible intermediaries (HPBN p.265). If there is no ALPN at the TLS termination point, the book suggests a load balancer in TCP proxy mode and, as a last resort, the unencrypted Upgrade flow (HPBN p.267-268). Load balancer details in section 12.

## 12. Chapter 13: what the book says to do with HTTP 2.0

### Minimum requirements and removal of 1.x optimizations (HPBN p.259-261)

- The focus of 2.0 is transport; so a well-tuned TCP and TLS have never been more important: server with an initial cwnd of 10 segments, TLS with ALPN (NPN for SPDY) and TLS session resumption (HPBN p.259-260).
- The general practices still hold: send fewer bytes, eliminate requests and adapt resource scheduling to wireless networks (HPBN p.260).
- **Undo** domain sharding, concatenation and image spriting: they are no longer needed and become harmful (HPBN p.260).
- **One connection per origin**: multiple connections (as in sharding) are an antipattern, since they reduce the effectiveness of header compression and prioritization (HPBN p.260).
- **Concatenation and sprites**: costs of cache invalidation, more memory, deferred execution and more complexity; with many small multiplexed resources, the costs of bundling almost always outweigh the benefits (HPBN p.261).
- Consolidate as many resources as possible on the same origin; eliminating sharding is the critical first step, and the rest can migrate gradually. Bundles do not affect the protocol itself, but weigh on cache and execution (HPBN p.261).
- Exception: the per-request overhead dropped, but is not zero; resources always used together and rarely updated may still gain from bundling. It is an exception, and must be measured (HPBN p.261).
- On push and inlining: see the other file in this series (`http2-hpack-prioritizacao-e-server-push.md`).

### Dual-protocol deployment strategies (HPBN p.262-263)

- If the application controls both client and server, it dictates the protocol and should use 2.0 exclusively (HPBN p.262).
- Same code for 1.x and 2.0: perhaps not optimal in either, but pragmatic. First step: eliminate sharding; then, as the 2.0 base grows, undo bundling and use push (HPBN p.262).
- Separate code per protocol: for example, an edge server that forwards according to the negotiated protocol; more operational complexity (HPBN p.262).
- Dynamic optimization: tools that rewrite the application at delivery and take the negotiated protocol into account. The book cites PageSpeed (mod_pagespeed and ngx_pagespeed, PSOL library), with the example of turning off combine_css and combine_javascript for SPDY/2.0 clients and keeping sharding only for 1.x clients (HPBN p.262-263).
- Irony pointed out: those who invested the most in optimization for 1.x will find it harder to migrate (HPBN p.262).

### 2.0 to 1.x translation and internal infrastructure (HPBN p.263-265)

- An intermediary server can accept a 2.0 session and dispatch 1.x requests to the existing infrastructure, the simplest path to start. Many web servers do this by default when acting as a reverse proxy (HPBN p.263-264).
- The book warns that this should not be a long-term strategy: it is the "reverse" path, since it de-optimizes an optimized session internally. The right approach is to convert incoming 1.x requests into 2.0 streams and standardize the infrastructure on 2.0 (HPBN p.264).
- Criteria for the internal infrastructure: persistent connections between load balancers/proxies and application servers, streaming and multiplexing by default, message-oriented and bidirectional communication. An end-to-end 2.0 session meets these, and removes the need for custom RPC layers between internal services (HPBN p.264-265).
- The book's summary: do not downgrade 2.0 to 1.x; upgrade 1.x to 2.0 (HPBN p.265).

### Server quality (HPBN p.265)

- Prioritization, push and multiplexing depend on the server's logic: it should understand priorities, prioritize processing and delivery, support push and ideally offer different push strategies.
- A naive server "speaks" the protocol but delivers poorly (for example, it saturates bandwidth with large images while the client waits for CSS/JS).
- The 2.0 client should be "optimistic": it sends everything as soon as possible and trusts the server; hence it depends even more on it. Each server (Apache, Nginx, Jetty etc.) was at a different implementation stage.

### TLS, ALPN and load balancers (HPBN p.265-268)

- Terminate TLS on the 2.0 server itself (simple) or upstream (load balancer); in that case the proxy completes TLS+ALPN and may open another encrypted tunnel or send unencrypted 2.0 frames to the server, a decision for the application as long as the internal network is controlled. Servers should be able to speak 2.0 unencrypted (HPBN p.265-266).
- A load balancer can use the protocol negotiated via ALPN to route clients to different servers; HAProxy supported NPN and routing by protocol (HPBN p.266).
- Many cloud load balancers terminate TLS but do not do ALPN, a requirement of 2.0 over TLS; in that case configure them as a TCP proxy (HPBN p.267).
- Practical rules: the TLS termination point must support ALPN; terminate TLS as close to the user as possible; without ALPN, use TCP balancing mode; without ALPN and without TCP mode, fall back to the Upgrade flow over an unencrypted channel (HPBN p.267-268).
- Early adopter's guide: SPDY was the "production" version, with years of real testing and growing support; the two were not in sync, but they share the same core features, and the discussion applies to both (HPBN p.260).

## After the book [extrapolation]

Nothing below comes from HPBN or has a page; it serves only to contrast the 2013 draft with the final standard.

- [extrapolation] RFC 7540 (2015) fixed the frame header at **9 bytes** (24-bit length, type, flags, reserved bit and 31-bit ID), with a default frame size of 16,384 bytes adjustable via SETTINGS.
- [extrapolation] RFC 7540 defined that client-initiated stream IDs are odd and server ones are even, resolving the book's inconsistency in favor of p.249.
- [extrapolation] The draft's `:host` pseudo-header became `:authority`.
- [extrapolation] The 31-bit priority was replaced in RFC 7540 by a dependency tree with weights; flow control could no longer be turned off. RFC 9113 (2022) made that tree obsolete.
- [extrapolation] The frame type numbers, the flags and the error codes were fixed in the RFCs. Cleartext upgrade (h2c) is hardly used in practice, and browsers only speak HTTP/2 over TLS with ALPN.
- [extrapolation] HTTP/3 (QUIC, over UDP) attacks the transport-level HoL that the book lists as a limitation on p.236.

## What the source does not cover

- Exact format and numeric values of the draft's frame types and flags, error codes and the SETTINGS parameter table (the book refers to the IETF draft).
- Stream states (idle, open, half-closed, closed) and error rules.
- Prioritization algorithm or `WINDOW_UPDATE` algorithm: the book says the standard leaves this to the implementer (HPBN p.234, 237).
- Weights and dependency tree, HPACK, RFC 7540/7541 and frames after Draft 4.
- HTTP/3, QUIC and the behavior of browsers after 2013.
- Concrete Nginx, Apache or HAProxy configuration for HTTP 2.0 (only the mod_pagespeed example on p.263 and the HAProxy mention on p.266).
- Measurements of real 2.0 gains beyond the SPDY lab numbers (p.226, 235).
