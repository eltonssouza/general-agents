# XHR, SSE and choosing a real-time transport

Summary of chapters 14 (browser networking primer, PDF p.271–277), 15 (XMLHttpRequest, p.279–296) and 16 (Server-Sent Events, p.297–303) of *High Performance Browser Networking* (Grigorik, 2013). Pages are **PDF** pages (printed = PDF − 18). Labels: `[from source]`, `[inference]` (my deduction), `[DATED]` (2013 state that has changed). WebSocket is in [`websockets-full-duplex-e-enquadramento.md`](websockets-full-duplex-e-enquadramento.md) and WebRTC in [`webrtc-p2p-ice-stun-turn-e-datachannel.md`](webrtc-p2p-ice-stun-turn-e-datachannel.md).

---

## 1. What the browser does for you (ch. 14)

- Under the appearance of a simple resource fetcher, the browser's network stack is a platform of its own, with optimization criteria, APIs and services [from source] (HPBN p.271). If the browser waits on the network, all the other stages are blocked (HPBN p.271).
- The application does not manage TCP/UDP sockets. The browser deliberately separates the **request** lifecycle from the **socket** lifecycle: pending requests go into a queue, are prioritized and only then bound to a socket from the pool. Unless the server closes it, the same socket is reused [from source] (HPBN p.272).
- Origin = triple (protocol, domain, port); `http://www.example.com:80` and `https://www.example.com:443` are different origins. Socket pool = sockets of the same origin; the major browsers limit the pool to **six sockets** [from source] (HPBN p.273).
- The automatic pool makes it possible to serve the queue by priority, reuse sockets, open sockets proactively, decide when to close idle ones and distribute bandwidth [from source] (HPBN p.273).
- Security and *sandbox*: no access to raw sockets (prevents port scanning or using the browser against mail servers), with connection limits, request formatting, TLS and same-origin enforced by the browser [from source] (HPBN p.274). There is no single same-origin policy, but a set of related mechanisms (HPBN p.275).
- Cache and cookies: before sending, the browser consults the cache and validates; the server should provide `Cache-Control`, `ETag` and `Last-Modified`. There is a per-origin "cookie jar" and a session shared across tabs [from source] (HPBN p.275-276).
- Chrome performs speculative optimizations (DNS pre-resolution, TCP pre-connection, pre-rendering) by learning the topology of the sites visited [from source] (HPBN p.274). See [`otimizacoes-de-navegador-resource-hints-e-caching.md`](otimizacoes-de-navegador-resource-hints-e-caching.md).

### Comparison table XHR, SSE and WebSocket [from source] (HPBN p.276)

| Feature | XHR | SSE | WebSocket |
| :--- | :--- | :--- | :--- |
| Request streaming | no | no | yes |
| Response streaming | limited | yes | yes |
| Framing mechanism | HTTP | event stream | binary framing |
| Binary data | yes | no (base64) | yes |
| Compression | yes | yes | limited |
| Application protocol | HTTP | HTTP | WebSocket |
| Network transport | TCP | TCP | TCP |

The book leaves WebRTC out of the table because it is peer to peer. There is no absolutely best protocol: every non-trivial application mixes transports according to cache, overhead, latency, reliability and data type (HPBN p.276-277).

---

## 2. XMLHttpRequest (ch. 15)

### Role and history
- XHR is the browser API that lets a script control data transfers; the browser takes care of connection, pool, HTTP choice, cache, redirects, content negotiation, security and authentication [from source] (HPBN p.279). Called the browser's "Swiss Army knife"; widely used as a fallback transport for old clients [from source] (HPBN p.280).
- The "XML" in the name is a leftover: the first version shipped inside Internet Explorer 5's MSXML library; the W3C specification only came out in 2006 [from source] (HPBN p.280).
- XHR2 (2008 draft) added timeouts, text and binary, media type override, progress events, efficient upload and secure cross-origin requests; in 2011 it was merged into the original specification, so "XHR" already means XHR2 [from source] (HPBN p.280-281).

### CORS
- The browser forbids the application from changing protected headers: `Accept-Charset`, `Accept-Encoding`, `Access-Control-*`, `Host`, `Upgrade`, `Connection`, `Referer`, `Origin`, `Cookie`, `Sec-*`, `Proxy-*` and others. This ensures the application does not forge agent, user or origin [from source] (HPBN p.281-282).
- Reason for the same-origin policy: the browser holds tokens and cookies that must not leak between applications [from source] (HPBN p.282). CORS is the voluntary opt-in mechanism for exceptions: the request code is the same, only the URL from another origin changes [from source] (HPBN p.282).
- Simple flow: the browser adds `Origin`; the server decides and responds with `Access-Control-Allow-Origin` carrying the allowed origin. Without the header, the browser fails the request. The wildcard `*` allows any origin, "think twice" [from source] (HPBN p.283).
- Safeguards: CORS omits credentials (cookies, HTTP authentication); the client is restricted to "simple" requests (GET, POST, HEAD methods and limited headers). For credentials, the client sets `withCredentials` and the server responds with `Access-Control-Allow-Credentials` [from source] (HPBN p.283).
- **Preflight**: for custom headers or "non-simple" methods, the browser first sends an `OPTIONS` with `Access-Control-Request-Method` and `Access-Control-Request-Headers`; the server responds with `Access-Control-Allow-Methods` and `Access-Control-Allow-Headers`. It costs at least one additional **round trip**, but the response can be cached by the client [from source] (HPBN p.284).
- [inference] Whoever controls both the server API and the client can avoid the preflight by keeping requests simple.

### Download
- Native types to encode and decode: `ArrayBuffer`, `Blob`, `Document`, `JSON`, `Text`; the type comes from content negotiation or from the explicit `responseType` [from source] (HPBN p.284-285).
- With `responseType = 'blob'` an image can be displayed in native format via an object URL, with no base64 or data URI, and no extra network or encoding cost (HPBN p.285). Release the object URL after loading (HPBN p.285). `Blob` serves as an opaque reference and as an exchange format between JavaScript APIs (HPBN p.286).

### Upload
- `send()` accepts `DOMString`, `Document`, `FormData`, `Blob`, `File` or `ArrayBuffer`, encodes it and sets the `Content-Type` [from source] (HPBN p.286).
- **No request streaming**: the complete payload is supplied to `send()`. Workaround: slice the `Blob` and send several XHRs, for example in 1 MB blocks with `Content-Range` (start-end/total). It does not replace real streaming, but it is viable and adds robustness on unstable connections: only the block that failed is redone or resumed [from source] (HPBN p.286-287).

### Progress and timeout
- Events: `loadstart` (once), `progress` (zero or more), `error`, `abort`, `load` (zero or one of each) and `loadend` (once) [from source] (HPBN p.288). For upload, the listeners go on `xhr.upload` (HPBN p.288).
- A percentage requires the response to have a known size (`lengthComputable`); in a chunked transfer the total is unknown [from source] (HPBN p.288-289).
- **XHR has no timeout by default**. Good practice: set a useful timeout and handle the error [from source] (HPBN p.289).

### Download streaming with XHR
- There is no simple, efficient, cross-browser API; `send` expects the whole payload and `responseText` was not made for streaming. Streaming was never an official use case [from source] (HPBN p.289).
- The possible technique (read `responseText` at `readyState > 2` and slice by offset) has problems: `responseText` accumulates the whole response (it is only released by finishing the request); text only; the application defines the message boundaries; browsers differ in buffering and in the content types accepted [from source] (HPBN p.289-290).
- The book's conclusion: XHR is not good for streaming [from source] (HPBN p.290, 296). Alternatives: SSE (server-to-client text) and WebSocket (bidirectional, binary and text) (HPBN p.291).
- [DATED] The Streams API was under discussion and unavailable in any browser; Firefox offered `moz-chunked-text` and `moz-chunked-arraybuffer`, and Internet Explorer `ms-stream`, with no equivalent in Chrome or Opera (HPBN p.289, 291).

---

## 3. Real-time notifications: polling and long-polling

Starting point: HTTP does not let the server initiate a connection to the client. To receive updates the client must poll or use a streaming transport [from source] (HPBN p.291). "Real time" has different meanings (from sub-milliseconds to minutes): **define latency and overhead goals before choosing** [from source] (HPBN p.291).

### Periodic polling [from source] (HPBN p.292)
- The client fires an XHR at a fixed interval; with nothing new, the response is empty.
- Each XHR is an independent HTTP request, with about **800 bytes** of header overhead (without cookies).
- A long interval delays delivery; a short one generates useless traffic and cost on the client and the server. There is no optimal interval.
- Works well with long intervals, events at a predictable pace and large payloads. On wireless networks it becomes a cost antipattern, because waking the radio drains the battery.

### Numeric model: e-mail with 60 s polling [from source] (HPBN p.293)
- Average delivery latency: the message waits on average **30 s** (half the interval, if arrivals are random).
- Overhead: 800 bytes of HTTP plus about 50 bytes of authentication cookie and last-message ID = **850 bytes** per empty query.
- 10,000 clients × 850 bytes × 8 bits / 60 s ≈ **1.13 Mbps** (167 requests/s) of constant ingress, delivering nothing.
- With a 1 s interval, the same clients would generate more than **60 Mbps**.

### Long-polling [from source] (HPBN p.294-295)
- Instead of responding empty, the server holds the request until there is data; on delivery, the client opens another immediately. Also known as Comet, "reverse AJAX", "AJAX push" or "HTTP push" (*hanging GET*) (HPBN p.294).
- Best possible latency and it eliminates empty queries. The HTTP overhead per message remains; with frequent arrivals, long-polling can open **more** requests than periodic polling (HPBN p.295).
- Tradeoff: long-polling always minimizes latency; if the application tolerates delay, polling aggregates messages and can save requests and battery (HPBN p.295).
- Recommended combination: aggregate low-priority updates on the server and deliver high-priority ones immediately (HPBN p.295).
- Historical example: Facebook chat was deployed in 2008 using long-polling via XHR over a persistent connection, in an iframe. Simple and supported by any browser with XHR, but less efficient (HPBN p.295-296).

### Verdict on XHR (HPBN p.296)
- Great for request-response cycle transfers, with authentication, compression and cache provided by the browser.
- Polling has high overhead and delay; long-polling has low latency, but per-message overhead; low latency with low overhead would require streaming, which XHR does not deliver well.
- With no specific reason for XHR polling, prefer SSE or WebSocket. XHR remains a common fallback strategy in real-time frameworks.

---

## 4. Server-Sent Events (ch. 16)

### What it is
SSE provides efficient server-to-client streaming of text event data. It has two components: the `EventSource` interface in the browser, which delivers notifications as DOM events, and the *event stream* data format [from source] (HPBN p.297). Advantages: low latency over a single long connection; efficient parsing without unbounded buffers; automatic tracking of the last message and reconnection; notifications as DOM events (HPBN p.297). Underneath, it is a cross-browser, economical implementation of XHR streaming over a long HTTP connection [from source] (HPBN p.297).

### `EventSource` API [from source] (HPBN p.297-299)
- `new EventSource(url)`; `onopen`, `onerror`, `onmessage` (events without an explicit type) and `addEventListener("foo", ...)` for typed events; `close()` ends it.
- It can be consumed from another origin with the same CORS flow as XHR.
- Unlike raw XHR, which keeps the whole response until the connection drops, SSE discards processed messages and does not accumulate everything in memory (HPBN p.298).
- If the connection drops, `EventSource` reconnects and can report the ID of the last message for resumption and retransmission (HPBN p.298-299).

### Event stream protocol [from source] (HPBN p.300-301)
- Ordinary `GET` request with `Accept: text/event-stream`; `200` response with `Content-Type: text/event-stream`, generally `Connection: keep-alive` and `Transfer-Encoding: chunked`; the body is UTF-8.
- Fields: `data:` (the payload is the value of one or more adjacent `data` fields; several lines become one message), `event:` (optional type), `id:` (optional ID) and `retry:` (reconnection interval in ms; the example uses 15000). Line breaks mark event boundaries.
- With a type, it fires a custom DOM event; without one, it calls `onmessage`.

### UTF-8, binary and compression [from source] (HPBN p.301)
- `EventSource` delivers the concatenated payload without processing it; JSON, for example, the application decodes.
- Everything is UTF-8. Binary via base64 costs **33%** extra bytes. SSE was not made for binary; for that the book points to WebSocket.
- Since it is a streaming HTTP response, it can and should be compressed with gzip.

### Reconnection and recovery [from source] (HPBN p.301-302)
- Automatic reconnection; the specification suggests a delay of **2 to 3 seconds**, a common default, which the server can change at any time with `retry`.
- The browser stores the last `id` and sends it in the `Last-Event-ID` header on reconnection (the example: `retry: 4500`, `id: 43`, then `Last-Event-ID: 43` and a response with `id: 44`).
- Recovery is the server's job. If losing messages is acceptable, no IDs are needed. If recovery is required, the server assigns IDs and keeps some local cache to retransmit what was missed; it can also write markers (checkpoints) into the stream. How far back to keep depends on the application (HPBN p.302).

### Limitations and uses [from source] (HPBN p.303)
1. Server to client only; it does not serve request streaming (for example, a large upload).
2. Designed for UTF-8; binary streaming is possible, but inefficient.
- UTF-8 workaround: SSE announces that a new asset exists and the application downloads it via XHR, at the cost of one extra round trip, but with the cache, compression and other services of XHR; a streamed asset is not cached by the browser.
- Battery: batch messages so as not to wake the radio and eliminate unnecessary keepalives; an SSE connection is not "dropped" just because the radio went idle.
- Intermediaries that do not know SSE (proxies, firewalls) may buffer the stream, causing latency or breaking the connection. If that happens, deliver the event stream over **TLS**.

### Emulation and support [from source, DATED part]
- [DATED] In early 2013, native support was missing in Internet Explorer and in the default Android browser (HPBN p.299).
- The interface is simple enough for a polyfill. But the transport underneath is XHR: polling brings delay and overhead, long-polling has low latency with high overhead, XHR streaming is limited and accumulates data in memory. The book mentions `jQuery.EventSource` as an example that uses XHR polling. Inspect the polyfill's implementation (HPBN p.299).

---

## 5. Decision: polling, long-polling, SSE or WebSocket

Procedure (combining the cited pages):

1. **Define a latency and overhead goal.** Without it, "real time" decides nothing (HPBN p.291).
2. **Ask about direction and data type.**
   - Server to client, text, notifications: **SSE** (HPBN p.297, 303).
   - Bidirectional, frequent messages, or efficient binary: **WebSocket** (HPBN p.276, 320).
   - Transaction with cache, authentication and compression: **XHR** (HPBN p.296).
3. **Cacheable data or a large binary with notification events:** use SSE or WebSocket as the control channel and download the asset via XHR (HPBN p.303, 323).
4. **Periodic polling** only if the intervals are long, the arrivals predictable and the payloads large (HPBN p.292). Compute the cost with the e-mail model: bytes × 8 × clients ÷ interval (HPBN p.293).
5. **Long-polling** when you want the best latency without WebSocket/SSE, accepting HTTP overhead per message; it is also the universal fallback (HPBN p.295-296).
6. **Problematic intermediaries:** TLS for SSE (HPBN p.303) and WSS for WebSocket (HPBN p.319).
7. **Mobile:** aggregate low-priority messages; avoid frequent polling and keepalives; real-time push has a battery cost (HPBN p.292, 295, 303, 325).

### Overhead and latency comparison (HPBN p.321)
- Propagation latency is the same across the four; queuing latency changes (polling waits for the next cycle; SSE and WebSocket send as soon as available).
- Per message: SSE ≥ 5 bytes; WebSocket 2–14 bytes of frame; HTTP/1.x XHR 500–800 bytes plus cookies; HTTP/2 up to 8 bytes when the headers do not change; IP, TCP and TLS add another 60–100 bytes.
- Compression: XHR negotiates per request; SSE compresses the entire session with gzip; WebSocket requires selective per-message compression, without stable native support in 2013 (HPBN p.322).

---

## After the book [extrapolation]

- The `fetch` API with `ReadableStream` offers response streaming where XHR did not; request streaming is still limited.
- `EventSource` gained support in the browsers that lacked it; with HTTP/2, the limit of six connections per origin no longer weighs on multiple SSE connections.
- Current real-time standards include WebTransport; RFC 8441 brings WebSocket to HTTP/2.

## What the source does not cover

- Additional CORS headers (for example, preflight cache time), `fetch`, `AbortController` and fetch's `credentials`.
- Server details for SSE: load balancing, heartbeat with comments, per-server connection limit.
- Real measurements of long-polling and SSE latency; the book's numbers are models.
- Current browser support for any feature mentioned.
