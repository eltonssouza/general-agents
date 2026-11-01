# Glossary

Terms from *High Performance Browser Networking* (Grigorik, O'Reilly, 2013), in alphabetical order, with a short definition in the package's own words and the PDF page (printed = PDF − 18). The page given is where the book covers the term; for detail, open the topical reference. Terms the book does not use are under "Terms the book does not use", at the end. Labels: `[DATED]` = 2013 state that has since changed; `[extrapolation]` = postdates the book.

General map in [INDEX.md](INDEX.md).

---

- **ABR (adaptive bitrate streaming).** The resource is encoded at several bitrates and cut into chunks of a few seconds; the client picks the next one, second by second, according to the measured throughput. (HPBN p.115, 166)
- **ALPN (Application-Layer Protocol Negotiation).** TLS extension in which the client lists the application protocols and the server picks one, with no extra round trip. Replaces NPN. (HPBN p.72)
- **AppCache.** Offline-mode mechanism mentioned by the book [DATED]. (HPBN p.167)
- **Bandwidth.** Maximum throughput of a logical or physical path. (HPBN p.21)
- **BDP (bandwidth-delay product).** Link capacity times end-to-end delay; it is the maximum amount of unacknowledged data in flight. (HPBN p.46)
- **Bufferbloat.** High, variable latency caused by router buffers that are too large, which interfere with TCP congestion control. (HPBN p.24)
- **Cell DCH / Cell FACH.** HSPA radio states: DCH is high power with dedicated resources; FACH is intermediate, a slow shared channel. (HPBN p.137, 138)
- **CORS.** Server opt-in mechanism that allows cross-origin requests, using `Origin` and `Access-Control-Allow-Origin`. (HPBN p.282, 283)
- **CRL.** List published by the CA of revoked certificates; it only grows and can go stale in cache. (HPBN p.79, 80)
- **CSSOM.** Tree of style rules built from the CSS; combined with the DOM it forms the render tree. JS waits for it. (HPBN p.186)
- **cwnd (congestion window).** Sender-side limit on data in flight, private, initialized conservatively and growing during slow-start. The maximum in flight is the lesser of rwnd and cwnd. (HPBN p.37, 38)
- **Datagram.** Independent unit that is routable without prior exchanges; in UDP, it preserves message boundaries. (HPBN p.53, 55)
- **DNS pre-resolve / `dns-prefetch`.** Early resolution of host names, done by the browser or requested through a hint. (HPBN p.201, 202)
- **Domain sharding.** Spreading resources across subdomains to raise the number of parallel connections; becomes an antipattern in HTTP 2.0. (HPBN p.216, 260)
- **DRX (discontinuous reception).** Substates of connected LTE in which the device keeps its context and wakes up periodically to listen (Short DRX and Long DRX). (HPBN p.135, 136)
- **DTLS.** TLS adapted to datagrams (RFC 6347), with a "mini-TCP" for the handshake only. (HPBN p.66, 355, 356)
- **Early termination.** Terminating TCP and TLS on a server close to the user, which keeps long-lived secure connections to the origin. (HPBN p.83, 84)
- **Energy tail.** Energy spent with the radio at high power after a transfer, until the timers step it down; it occurs regardless of the size of the send. (HPBN p.140, 164)
- **ETag.** Resource version identifier, used as a validator. The book only mentions it as a validation mechanism alongside `Last-Modified`. (HPBN p.254)
- **EventSource.** Browser API for SSE; it reconnects on its own and delivers DOM events. (HPBN p.297, 298)
- **Event stream.** UTF-8 text format of SSE with the fields `data`, `event`, `id` and `retry`. (HPBN p.300, 301)
- **Frame (HTTP 2.0).** Smallest unit of communication; every frame has a header that identifies the stream. In the book's draft, the header is 8 bytes. (HPBN p.231, 244, 245) [DATED]
- **Frame (WebSocket).** Smallest unit of the protocol, with 2 to 10 bytes of header coming from the server and 6 to 14 coming from the client. (HPBN p.313, 314)
- **GOAWAY.** Draft frame that asks the peer to stop creating streams, reporting the last ID processed. (HPBN p.246) [DATED]
- **Head-of-line (HoL) blocking.** A delayed or lost item holds back the ones that follow. It shows up in HTTP 1.x (responses in order), in TCP (a loss holds back the buffer) and in WebSocket (messages are not interleaved). (HPBN p.48, 213, 236, 314)
- **Header tables.** Tables of key-value pairs kept per connection on both sides in the HTTP 2.0 draft; the new set is sent as a difference. The book does not use the name HPACK. (HPBN p.240, 241) [DATED]
- **HSTS.** Header-based policy (`Strict-Transport-Security`) by which the browser only speaks HTTPS to the origin. (HPBN p.90)
- **HSPA / HSPA+.** 3GPP evolution of UMTS; HSPA+ brought much lower latency. (HPBN p.122)
- **HTTP 2.0 (draft).** Version under construction in 2013, with a binary framing layer; the book warns that low-level details may change. (HPBN p.225, 226, 229) [DATED]
- **ICE.** Set of methods that seeks the most efficient path between two peers: direct, via STUN and, last, via TURN. (HPBN p.61, 62, 343)
- **Idle / Connected (RRC).** LTE states: Idle is low power (< 15 mW) with no resources; Connected is high (1,000 to 3,500 mW) with dedicated resources. (HPBN p.133, 135)
- **Initial cwnd (IW10).** Initial value of cwnd; 1, then 4 (RFC 2581), then 10 (RFC 6928). (HPBN p.38) [DATED]
- **Jitter.** Variation in arrival time; in TCP it comes from waiting for retransmission. (HPBN p.48, 149)
- **Keep-alive (HTTP).** Reuse of the TCP connection for several requests; it is the default in HTTP 1.1. (HPBN p.179, 209)
- **Last-Event-ID.** Header sent on SSE reconnection with the last ID received, so the server can resume. (HPBN p.301, 302)
- **Latency.** Time between the source emitting a packet and the destination receiving it; the sum of propagation, transmission, processing and queuing. (HPBN p.21, 23)
- **Long-polling.** The server holds the request until there is data and the client reopens it right after; also called Comet. (HPBN p.294)
- **Masking (WebSocket).** Every client payload is masked with a 32-bit key, to protect intermediaries that do not understand WebSocket. (HPBN p.314)
- **MSS.** Largest TCP payload per segment; the book uses it when saying a TLS record should fill the entire MSS. (HPBN p.86)
- **NAT.** Address translation at the edge, which maps local tuples to public ones; UDP entries expire on a timer. (HPBN p.56, 57, 58)
- **NPN.** Next-protocol negotiation born out of SPDY, in which the server advertises and the client chooses; obsolete in favor of ALPN. (HPBN p.72) [DATED]
- **OCSP / OCSP stapling.** Real-time query of a certificate's status; with stapling, the server attaches the signed response to the handshake. (HPBN p.80, 89, 90)
- **Origin.** Triple of protocol, domain and port; the browser's socket pool is per origin, with up to six. (HPBN p.273)
- **Paging.** Message sent to all the towers of a tracking area to locate a device in Idle. (HPBN p.151)
- **Pipelining (HTTP 1.1).** Sending several requests without waiting for the response; fails in practice because it requires responses in order and because of intermediaries. (HPBN p.210, 212, 213)
- **PLT (page load time).** Time until the `onload` event. (HPBN p.185)
- **Preflight.** `OPTIONS` sent before non-simple CORS requests; costs at least one round trip. (HPBN p.284)
- **Preload scanner.** Looking ahead in the document source, when the parser is blocked, to dispatch downloads. It does not see what JS schedules. (HPBN p.258)
- **PRR (proportional rate reduction).** Loss recovery algorithm; default in Linux 3.2+. (HPBN p.45) [DATED]
- **PUSH_PROMISE.** Draft frame with which the server announces a resource it is going to push; it must go out before the response. (HPBN p.239, 247) [DATED]
- **RRC (Radio Resource Controller).** Manages the device's connection to the base station and decides who talks, when and at what power; in LTE it sits at the tower. (HPBN p.131, 133, 146)
- **RTT (round-trip time).** A packet's round trip; Table 1-1 of the book gives the values over fiber. (HPBN p.25)
- **rwnd (receive window).** Receive window advertised in each ACK; without window scaling, limited to 65,535 bytes. (HPBN p.35, 36)
- **SCTP.** Message-oriented protocol with configurable reliability and ordering, tunneled over DTLS and UDP in the DataChannel. (HPBN p.362, 363, 366)
- **SDP.** Text format that describes the session (media, codecs, candidates); JSEP hides it behind `RTCPeerConnection` methods. (HPBN p.341, 342)
- **Session ID / Session ticket.** Two forms of TLS resumption: server-side cache (ID) or an encrypted ticket kept by the client (stateless). (HPBN p.73, 75)
- **SNI.** Extension in which the client states the hostname in the handshake so the server can choose the certificate. (HPBN p.72, 73)
- **SPDY.** Google's experimental protocol (2009) that served as the starting point for HTTP 2.0, but "is not HTTP 2.0". (HPBN p.226, 227) [DATED]
- **SRTP / SRTCP.** Secure profile of RTP for media and its feedback channel; 12-byte SRTP header. (HPBN p.359, 360, 361)
- **SSR (slow-start restart).** Reset of cwnd after idleness; recommended to turn off on servers with persistent connections. (HPBN p.41)
- **Slow-start.** Initial TCP phase in which cwnd grows with each ACK, doubling per RTT. (HPBN p.37, 38)
- **STUN.** Protocol in which the application discovers its public address and port behind the NAT. (HPBN p.59, 60)
- **Stream (HTTP 2.0).** Bidirectional flow of bytes within a connection, with an integer ID; messages are sequences of frames. (HPBN p.230, 231)
- **Supernode.** Peer or service that receives the streams of a group and redistributes them, instead of a full mesh. (HPBN p.376, 377)
- **Tail time.** The book does not use this name; it calls it energy tail. See "Energy tail".
- **TCP Fast Open (TFO).** Allows sending data already in the SYN, on repeat connections, with a cryptographic cookie; Linux 3.7+. (HPBN p.34) [DATED]
- **Three-way handshake.** SYN, SYN-ACK, ACK; costs one round trip before any data. (HPBN p.32, 33)
- **Tracking area.** Logical group of towers known to the carrier's core network. (HPBN p.143)
- **Trickle ICE.** Exchanging the SDP offer without candidates and sending them over signaling as they appear. (HPBN p.346, 347)
- **TURN.** Relay of last resort when the direct connection fails; it stops being P2P and is expensive to operate. (HPBN p.60, 61)
- **Window scaling.** TCP option (RFC 1323) that raises the rwnd ceiling to 1 GB. (HPBN p.36)
- **WSS.** WebSocket over TLS; `wss` scheme. (HPBN p.307, 319)
- **XHR.** API for controlling transfers; "XML" in the name is a leftover; XHR2 was merged in 2011. (HPBN p.279, 280, 281)

---

## Terms the book does not use

These terms appear in user questions, but a search of the book's text does not find them. Do not cite them as `[from source]`.

- **HPACK, RFC 7540, RFC 7541.** The book speaks of "header tables" and of a draft (HPBN p.240, 241). [extrapolation] The final version used HPACK.
- **Critical Rendering Path, render-blocking, above the fold, FOIT, FOUT.** The concepts appear under other names (processing pipeline, render tree, "first-paint critical CSS") (HPBN p.186, 222).
- **`defer`, `async`, `preload`, `preconnect`.** They do not exist in the book. What it has is `dns-prefetch`, `subresource`, `prefetch` and `prerender` (HPBN p.202).
- **Typical tail time of 10 to 20 s.** The book only gives illustrative examples of timers (10 s in the HSPA+ example) and states that they are set by the carrier (HPBN p.140).
- **TLS 1.3, 0-RTT, QUIC, HTTP/3, Service Workers, Core Web Vitals, 5G.** Postdate the book. [extrapolation]
