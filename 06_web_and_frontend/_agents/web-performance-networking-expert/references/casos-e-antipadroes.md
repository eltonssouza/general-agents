# Cases and antipatterns that the book condemns or analyzes

Source: *High Performance Browser Networking* (Grigorik, O'Reilly, 2013). Every page is the PDF page (printed = PDF − 18). Each entry gives: what you see, why the book condemns it (with page) and the fix it gives (with page). Labels: `[from source]` = it is on the cited page; `[inference]` = deduction from numbers in the book; `[DATED]` = 2013 state of affairs that has since changed; `[extrapolation]` = later than the book, only in section 9, no page.

For the reasoning behind each point, open the topical reference named in each section. General map in [INDEX.md](INDEX.md); execution steps in [procedimentos.md](procedimentos.md).

---

## 1. Network and transport (TCP, UDP)

Base: [fundamentos-tcp-e-gargalos-de-transporte.md](fundamentos-tcp-e-gargalos-de-transporte.md) and [udp-e-protocolos-de-transporte-alternativos.md](udp-e-protocolos-de-transporte-alternativos.md).

**AP-01. Buying bandwidth to fix page slowness.** [from source]
- Why it is wrong: above ~5 Mbps the gain in load time is a single-digit percentage, and going from 5 to 10 Mbps yields about 5% (HPBN p.195); each 20 ms less RTT yields a linear gain (HPBN p.196). The HTTP flow is short and bursty, and RTT dominates (HPBN p.196).
- The book's fix: reduce round trips, move data closer to the client, hide latency with cache and prefetch (HPBN p.30).

**AP-02. Opening a new connection per request.** [from source]
- Why it is wrong: every new TCP connection pays a full round trip before the first byte (HPBN p.33); in HTTP 1.0 this was a large penalty (HPBN p.177). With N requests the loss is (N − 1) × RTT (HPBN p.210).
- Fix: persistent connections (keep-alive) and, when possible, reuse the ones already open (HPBN p.210, 52).

**AP-03. Leaving slow-start restart on in a server with persistent connections.** [from source]
- Why it is wrong: after idleness TCP resets the cwnd, which hurts precisely the long-lived connections that alternate bursts and silence (HPBN p.41).
- Fix: turn it off on the server (`sysctl -w net.ipv4.tcp_slow_start_after_idle=0`) (HPBN p.41, 51).

**AP-04. Server with an old kernel and a low initial cwnd.** [from source]
- Why it is wrong: an initial cwnd of 4 segments needs four round trips to reach 64 KB in the 56 ms example (HPBN p.39). Raising it to 10 eliminates a whole round trip in the 20 KB example (HPBN p.43).
- Fix: update the kernel and use an initial cwnd of 10 (HPBN p.44, 50, 51, 52). [DATED] the book cites Linux 2.6.39 and recommends 3.2+ (HPBN p.44).

**AP-05. Receive window stuck at 64 KB.** [from source]
- Why it is wrong: without window scaling the rwnd does not exceed 65,535 bytes; to fill 10 Mbps with a 100 ms RTT at least 122.1 KB would be needed (HPBN p.36, 47). Intermediaries can rewrite or remove the option (HPBN p.36).
- Fix: check and enable `net.ipv4.tcp_window_scaling` (HPBN p.36, 37).

**AP-06. Custom protocol over UDP with no congestion control, no keepalive and no relay.** [from source]
- Why it is wrong: UDP provides no ordering, retransmission or congestion control, and the result tends to be a poorly made TCP (HPBN p.55, 56). Congestion-insensitive UDP can lead to collapse (HPBN p.62). NAT entries for UDP expire on a timer (HPBN p.57, 58).
- Fix: follow the RFC 5405 guidelines cited by the book, send bidirectional keepalives, reuse a library that already does ICE/STUN/TURN (HPBN p.58, 62, 63).

**AP-07. Relying on STUN alone for P2P.** [from source]
- Why it is wrong: libjingle records 92% direct connections and 8% that require a relay (HPBN p.61) [DATED]; the WebRTC chapter repeats the order of 8% (HPBN p.345).
- Fix: provide TURN and provision capacity for it; use STUN for establishment (HPBN p.61, 378).

**AP-08. Assuming that HTTP 2.0 with a single connection solves blocking at the transport layer.** [from source]
- Why it is wrong: HTTP's HoL goes away, but TCP's remains, and packet loss shrinks the window of the entire connection (HPBN p.236).
- The book's fix: keep one connection per origin (measurements of the time favor it) and invest in a well-tuned TCP on the server (HPBN p.236, 260).

---

## 2. TLS

Base: [tls-handshakes-resumption-e-alpn.md](tls-handshakes-resumption-e-alpn.md).

**AP-09. Full TLS handshake on every connection.** [from source]
- Why it is wrong: the full handshake costs two round trips and the abbreviated one costs one (HPBN p.70); the browser opens several connections to the same host, so resumption is indispensable (HPBN p.74).
- Fix: enable session IDs and tickets together, with a cache shared across workers and monitoring of the hit rate (HPBN p.73, 75, 85).

**AP-10. TLS compression turned on.** [from source]
- Why it is wrong: the CRIME attack (2012) uses TLS compression to extract authentication cookies, and transport-level compression recompresses data that is already compressed (HPBN p.87).
- Fix: turn it off on the server and compress text assets with Gzip (HPBN p.87, 88).

**AP-11. Bloated or incomplete certificate chain.** [from source]
- Why it is wrong: a missing intermediate forces the browser to fetch it (DNS, TCP and HTTP GET) (HPBN p.88); a superfluous certificate, including the root, overflows the initial cwnd and costs a round trip (HPBN p.88, 89).
- Fix: a chain with the site plus intermediate, few intermediate CAs, root left out of the chain (HPBN p.89).

**AP-12. TLS record misaligned with the TCP segment.** [from source]
- Why it is wrong: a small record pays more overhead (from ~6% on a 1,500 MTU); a large record spreads over several packets and waits for reassembly (HPBN p.86).
- Fix: one record per segment, around 1,400 bytes (HPBN p.86, 87).

**AP-13. Checking revocation online on every connection.** [from source]
- Why it is wrong: OCSP blocks navigation and tells the CA which sites the client visits (HPBN p.80).
- Fix: OCSP stapling, noting that the 400 to 4,000 byte response can overflow the cwnd and that only one response can be attached (HPBN p.89, 90).

**AP-14. Terminating TLS only at the distant origin.** [from source]
- Why it is wrong: each handshake round trip pays the full RTT to the origin (HPBN p.83).
- Fix: terminate TCP and TLS on a server close to the user, with a pool of secure connections to the origin (HPBN p.83, 84, 85).

**AP-15. Mixing HTTP and HTTPS content on the page.** [from source]
- Cited as a developer mistake in the TLS checklist (HPBN p.91). Fix: serve everything over HTTPS and send the HSTS header, which also avoids HTTP→HTTPS redirects (HPBN p.90, 91).

**AP-16. Depending on NPN.** [from source] [DATED]
- NPN, born from SPDY, is obsolete; ALPN inverts the order (client lists, server chooses) and is the IETF-approved version (HPBN p.72). Fix: migrate clients and servers to ALPN (HPBN p.72).

---

## 3. Mobile networks

Base: [redes-moveis-rrc-state-machine-e-tail-time.md](redes-moveis-rrc-state-machine-e-tail-time.md).

**AP-17. Periodic beacon, ping or polling.** [from source]
- Pandora case: audience pings every 60 s were 0.2% of the bytes and 46% of the app's energy (HPBN p.141). Every send promotes the radio and leaves an "energy tail" (HPBN p.140, 164).
- Fix: treat polling as very expensive, prefer push, aggregate requests and defer the non-critical ones until the radio is active (HPBN p.160, 161). Aggregating on the server is reminiscent of Nagle's algorithm at the application layer (HPBN p.161).

**AP-18. Application keepalive to "keep the radio" or the connection alive.** [from source]
- Why it is wrong: the life of the TCP/UDP connection is independent of the radio state; the PGW keeps the sessions (HPBN p.144, 162).
- Fix: most carriers have a NAT timeout of 5 to 30 minutes, so a keepalive of about 5 minutes is enough; if you need less, review server, proxy and load balancer first (HPBN p.162).

**AP-19. Caching bandwidth and latency estimates.** [from source]
- Why it is wrong: they are valid for tens to hundreds of milliseconds, at most about one second (HPBN p.165, 166).
- Fix: do not store them, use at most the network generation as a rough hint and adapt continuously (HPBN p.166).

**AP-20. Loading in small, frequent slices.** [from source]
- Why it is wrong: the radio is optimized for bursts; incremental loading multiplies RRC transitions (HPBN p.161, 167).
- Fix: "burst your data and return to idle": download as much as possible at once, anticipate what the user will need (HPBN p.167, 168).

**AP-21. Assuming the network is available and retrying in an infinite loop.** [from source]
- Fix: do not guess the network state, fire and handle failures, retry with backoff, offline queue (HPBN p.166, 167). `navigator.onLine` appears as a way to monitor (HPBN p.165). [DATED] AppCache as offline mode (HPBN p.167).

**AP-22. Background update with no energy accounting.** [from source]
- With the book's numbers (5 Wh = 18,000 J; 10 J per radio cycle), 1-minute polling costs 600 J per hour, about 3% of the battery per hour, for a single app (HPBN p.162).
- Fix: batch, adaptive interval, push instead of pull, measure (HPBN p.162).

**AP-23. User action that waits for the network before reacting.** [from source]
- The control plane alone already blows the feedback budget (HPBN p.164, 165). Fix: acknowledge the input within a few hundred ms, send in the background, give immediate feedback (HPBN p.164, 165).

**AP-24. Redundant transfer due to poorly used cache.** [from source]
- On smartphones, 18% and 20% of HTTP traffic in two datasets was redundant (HPBN p.255). Fix: review the application and add tests (HPBN p.255).

---

## 4. HTTP 1.x

Base: [http1x-keepalive-pipelining-e-sharding.md](http1x-keepalive-pipelining-e-sharding.md).

**AP-25. Pipelining on without controlling both ends.** [from source]
- Why it is wrong: responses must go out in order, a slow one blocks the following ones, intermediaries abort or serialize, and most browsers keep it off (HPBN p.212, 213).
- Fix: use only when you control both client and server (iTunes case), handling aborts, idempotency and intermediaries; the most reliable way is an HTTPS tunnel (HPBN p.214).

**AP-26. Excessive domain sharding.** [from source]
- Why it is wrong: each hostname costs DNS and sockets, many streams end up underutilized and in slow-start, and high-latency clients (3G, 4G) suffer more (HPBN p.217, 218).
- Fix: exhaust TCP tuning first, start with zero shards, increase gradually and measure; few sites gain from more than a dozen connections (HPBN p.217). [inference] 4 shards raise the ceiling from 6 to 24 connections (HPBN p.214, 216).

**AP-27. Heavy cookies and headers on every request.** [from source]
- The metadata adds up to 500 to 800 bytes per request, not counting cookies, which are the biggest offender (HPBN p.218). The book's example: 15 bytes of JSON with 352 bytes of header, 96% overhead (HPBN p.218, 219).
- Fix: send the minimum (a session token), keep the rest on the server, and serve static assets from a cookieless origin under HTTP 1.x (HPBN p.257).

**AP-28. Huge bundles, CSS or sprites.** [from source]
- Why it is wrong: any change invalidates the whole bundle, JS and CSS do not execute incrementally, a sprite becomes an RGBA bitmap at 4 bytes per pixel (800 × 600 results in 1.83 MB) (HPBN p.220, 221).
- Fix: separate the "stable core"; aim for 30 to 50 KB compressed per JS bundle as an order of magnitude (HPBN p.220, 221); answer the decision questions on p.222.

**AP-29. Inlining a large or reused resource.** [from source]
- An inlined resource is not cacheable on its own, repeats on every page and, if it is not text, grows about 33% because of base64 (HPBN p.223). Rule of thumb: consider inlining below 1 to 2 KB and for page-specific resources (HPBN p.223).

**AP-30. Long-lived connections (SSE, WebSocket, hanging XHR) consuming the pool of six.** [from source]
- Each one occupies a connection even when idle and can cause the self-DoS that leaves the seventh request pending (HPBN p.215, 216). Each WebSocket takes its own TCP connection (HPBN p.314).

---

## 5. Rendering, cache and bytes

Base: [critical-rendering-path-dom-cssom-e-layout.md](critical-rendering-path-dom-cssom-e-layout.md) and [otimizacoes-de-navegador-resource-hints-e-caching.md](otimizacoes-de-navegador-resource-hints-e-caching.md).

**AP-31. Late CSS and scripts blocking the DOM.** [from source]
- The DOM does not advance until the JS executes, and the JS does not execute until the CSSOM is ready; hence styles at the top and scripts at the bottom (HPBN p.186).
- Fix: critical resources discoverable early, CSS delivered early, non-critical JS deferred (HPBN p.202). The book does not mention `defer`/`async`.

**AP-32. Hiding resources from the preload scanner.** [from source]
- Resources scheduled by JavaScript are not seen by the scanner, which yielded a gain of about 20% in Chrome tests (HPBN p.258). Fix: weigh fine-grained control against the lost visibility (HPBN p.258).

**AP-33. Waiting for the whole document on the server before sending.** [from source]
- HTML is parsed incrementally; sending early what already exists (Google Search case) gives the browser time to discover resources (HPBN p.202, 203).

**AP-34. Cache without validation or without a lifetime.** [from source]
- A lifetime alone yields redundant transfer; validation alone yields revalidation on every use (HPBN p.254). Fix: always set `Cache-Control` and `ETag`/`Last-Modified` (HPBN p.254, 275).

**AP-35. Wrong image format and text without Gzip.** [from source]
- Images account for more than half of the bytes of an average page; PNG for a photo can cost hundreds or thousands of KB; Gzip reduces text by 60 to 80% (HPBN p.255, 256, 206).

**AP-36. Measuring only `onload` or only averages.** [from source]
- PLT is insufficient for applications (HPBN p.185); use histograms, medians and quantiles (HPBN p.199); combine synthetic tests with RUM (HPBN p.197).

**AP-37. Optimizing only the "front-end".** [from source]
- The name is misleading: server time and network latency are equally critical, and bandwidth is underused while waiting on RTT (HPBN p.192, 193, 194).

---

## 6. HTTP 2.0 (2013 draft)

Base: [http2-binary-framing-multiplexing-e-streams.md](http2-binary-framing-multiplexing-e-streams.md) and [http2-hpack-prioritizacao-e-server-push.md](http2-hpack-prioritizacao-e-server-push.md).

**AP-38. Keeping sharding under HTTP 2.0.** [from source]
- Multiple connections reduce the effectiveness of header compression and prioritization (HPBN p.260). Fix: consolidate origins; it is the first critical step of the migration (HPBN p.261).

**AP-39. Keeping concatenation and sprites under HTTP 2.0.** [from source]
- The costs of invalidation, memory and deferred execution almost always outweigh the benefits with many small multiplexed resources; there is a measured exception for resources always used together and rarely changed (HPBN p.261).

**AP-40. Inlining where push would fit.** [from source]
- Inlining is a forced push: the client cannot decline it or cache it (HPBN p.239). Fix: push so that each resource is cached and reused across pages (HPBN p.261).

**AP-41. Pushing without considering the client cache.** [inference]
- The book says the client can decline a push that is already cached (HPBN p.239) and that the server can infer what is cached by a model or cookie (HPBN p.240). The book does not discuss "over-pushing" as such; the antipattern is a deduction from those two pages.

**AP-42. Downgrading 2.0 to 1.x in the internal infrastructure.** [from source]
- It is the "reverse" path: it de-optimizes an optimized session (HPBN p.264). Fix: convert 1.x requests into 2.0 streams and standardize the interior on 2.0 (HPBN p.264, 265).

**AP-43. Naive server with poor prioritization.** [from source]
- Ignoring priorities saturates bandwidth with images while the client waits for CSS/JS; strict ordering reintroduces HoL (HPBN p.234, 235, 265). Fix: choose the server carefully, since the standard does not define the algorithm (HPBN p.234, 265).

**AP-44. Cleartext HTTP 2.0 relying on intermediaries.** [from source]
- Incompatible intermediaries require an encrypted channel in the first deployments (HPBN p.244, 265). Fix: TLS with ALPN and, only if necessary, Upgrade (HPBN p.243, 244).

**AP-45. Load balancer that terminates TLS without ALPN.** [from source]
- Many cloud load balancers terminate TLS but do not negotiate ALPN (HPBN p.267). Fix: terminate TLS where ALPN exists, use TCP proxy mode, and only as a last resort the unencrypted Upgrade flow (HPBN p.267, 268).

**AP-46. Treating SPDY or the draft as the final specification.** [from source]
- The author himself warns that bit encoding and field names may change (HPBN p.226, 229) and that "SPDY is not HTTP 2.0" (HPBN p.227). That is why the package labels these details as [DATED].

---

## 7. Real time: XHR, SSE, WebSocket

Base: [xhr-sse-e-escolha-de-transporte.md](xhr-sse-e-escolha-de-transporte.md) and [websockets-full-duplex-e-enquadramento.md](websockets-full-duplex-e-enquadramento.md).

**AP-47. Using XHR for streaming.** [from source]
- `responseText` accumulates the entire response, there is only text and browsers diverge (HPBN p.289, 290). The book concludes that XHR is not good for streaming (HPBN p.290, 296). Fix: SSE (server to client, text) or WebSocket (bidirectional) (HPBN p.291).

**AP-48. Periodic polling with no accounting.** [from source]
- Each empty poll costs about 850 bytes; 10,000 clients every 60 s give ~1.13 Mbps of ingress while delivering nothing, and at 1 s it exceeds 60 Mbps (HPBN p.293). There is no optimal interval (HPBN p.292).
- Fix: only with long intervals, predictable events and large payloads (HPBN p.292).

**AP-49. Long-polling with frequent messages.** [from source]
- HTTP overhead remains per message and can open more requests than periodic polling (HPBN p.295). Fix: aggregate what is low priority and deliver high priority immediately (HPBN p.295).

**AP-50. XHR without a timeout and a large upload in a single `send`.** [from source]
- XHR has no timeout by default (HPBN p.289) and does not stream the request (HPBN p.286). Fix: set a timeout; slice the `Blob` into chunks (1 MB example with `Content-Range`) to resume only what failed (HPBN p.286, 287).

**AP-51. WebSocket without WSS and without a fallback plan.** [from source]
- Intermediaries can buffer, alter or drop the traffic, and some networks block WebSocket (HPBN p.319, 323). Fix: use WSS and have a fallback strategy (HPBN p.319, 323, 325).

**AP-52. Ignoring the WebSocket send queue.** [from source]
- `send()` is asynchronous and messages go out in queue order, so one large message delays the others (HPBN p.310, 314). Fix: split messages, watch `bufferedAmount`, keep your own priority queue (HPBN p.310, 325).

**AP-53. Using WebSocket or SSE for cacheable content or large binary.** [from source]
- Binary over WebSocket does not enter the browser or CDN cache (HPBN p.323); SSE was designed for UTF-8 and base64 costs 33% (HPBN p.301, 303). Fix: notification channel over SSE/WebSocket and download the asset via XHR (HPBN p.303, 323).

**AP-54. Default proxy and load balancer timeouts.** [from source]
- The example's Nginx uses 60 s by default; HAProxy handles the tunnel through `timeout tunnel` (HPBN p.324). Fix: check the infrastructure before writing keepalive in the application (HPBN p.324).

**AP-55. Trusting a polyfill without inspecting the transport.** [from source]
- The fallback may be XHR polling, with delay and overhead (HPBN p.299, 307). Fix: use the native interface when it exists and measure the fallback (HPBN p.307).

---

## 8. WebRTC

Base: [webrtc-p2p-ice-stun-turn-e-datachannel.md](webrtc-p2p-ice-stun-turn-e-datachannel.md).

**AP-56. Large message on a partially reliable channel.** [from source]
- 120 KB example with 1% loss: ~107 packets, and losing one discards the message (HPBN p.373, 374). Fix: retransmission by count or time and messages below ~1,150 bytes (HPBN p.374, 380).

**AP-57. Full mesh in a call with many participants.** [from source]
- N × (N − 1) connections saturates the uplink (HPBN p.376). Fix: supernode or intermediary service (HPBN p.376, 377, 380).

**AP-58. Not using trickle ICE.** [from source]
- Waiting for all candidates delays the connection (HPBN p.346). Fix: send the offer right away and "trickle" the candidates (HPBN p.346, 347, 379).

**AP-59. Assuming DTLS authenticates the peer.** [from source]
- The certificates are self-signed; authentication is left to the application (HPBN p.357, 358).

---

## 9. Modern antipatterns with no support in the book [extrapolation]

None of these has an HPBN page. Confirm in a current source before recommending.

- **Server push as the default in final HTTP/2.** In practice it was little used and removed from browsers; alternatives such as `103 Early Hints` and `preload` replaced it.
- **Treating HTTP/3 as "faster HTTP/2" without measuring.** The book only anticipates the HoL problem in TCP (HPBN p.236); QUIC and HTTP/3 are outside it.
- **Keeping TLS 1.0/1.1 and weak ciphers.** The book's example uses TLSv1 and RC4-SHA (HPBN p.92); today that is a discouraged practice.
- **Enabling 0-RTT without thinking about replay.** TLS 1.3 does not exist in the book.
- **Giant bundles versus excessive module granularity.** The book condemns the monolithic bundle under HTTP 2.0 (HPBN p.261), but does not cover code splitting, ES modules or tree shaking.
- **Measuring only by Core Web Vitals.** They postdate the book; the book's measurement base is PLT, Navigation/Resource/User Timing and RUM (HPBN p.185, 198, 200).
- **Web fonts without hints.** `preload` and `preconnect` are not in the book (what it has is `dns-prefetch`, `prefetch`, `subresource` and `prerender`, HPBN p.202).
- **Mobile push over a persistent WebSocket without evaluating APNs/FCM.** The book cites GCM and a future W3C Push API (HPBN p.161) [DATED].
- **Immutable cache without modern directives.** `immutable`, `stale-while-revalidate`, `no-store` and the `If-None-Match`/304 flow are not explained in the book.
