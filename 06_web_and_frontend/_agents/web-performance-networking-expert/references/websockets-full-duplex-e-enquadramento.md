# WebSocket: API, handshake, binary framing and operation

Summary of chapter 17 of *High Performance Browser Networking* (Grigorik, 2013), PDF p.305–326. All pages below are **PDF** pages (printed = PDF − 18). Convention: `[from source]` = stated on the cited page; `[inference]` = my deduction from what the book says; `[DATED]` = 2013 state of affairs that changed later.

Overview: WebSocket is the bidirectional, message-oriented channel for text and binary, and the closest thing to a raw socket in the browser; the browser still handles connection negotiation, same-origin, interoperability with the HTTP infrastructure, framing and subprotocol negotiation [from source] (HPBN p.305). But the book warns that it does not replace HTTP, XHR or SSE; the best performance comes from using each transport for what it does well [from source] (HPBN p.305, 319). The comparison among the four transports is in [`xhr-sse-e-escolha-de-transporte.md`](xhr-sse-e-escolha-de-transporte.md).

Two bodies define the set: the API is from the W3C; the protocol (RFC 6455) and the extensions are from the IETF HyBi group [from source] (HPBN p.305).

---

## 1. Browser API

- The constructor takes the resource URL and, optionally, an array of subprotocols; callbacks: `onopen`, `onmessage`, `onerror`, `onclose` [from source] (HPBN p.306, 311).
- Own schemes: `ws` (cleartext) and `wss` (TCP + TLS). The scheme is not `http` because the wire protocol can be used outside the browser and negotiated by a non-HTTP exchange; in practice, there is no alternative handshake standard [from source] (HPBN p.307-308).
- The API is similar to `EventSource` on purpose, but offers extended functions [from source] (HPBN p.306).
- The application does not need to buffer or reassemble data: `onmessage` only fires when the whole message (for example, 1 MB) has arrived [from source] (HPBN p.308).

### Received data types
- The protocol records only two pieces of metadata per message: length (variable field) and type (UTF-8 or binary) [from source] (HPBN p.308).
- Text arrives as a `DOMString`; binary arrives as a `Blob` by default. Setting `binaryType = "arraybuffer"` is a performance hint to the browser [from source] (HPBN p.308).
- Selection rule: `Blob` when the data is immutable and will not be sliced or processed (e.g., handing it to an image tag); `ArrayBuffer` when there will be further processing [from source] (HPBN p.308). The W3C specification justifies this: with `blob` the browser can offload to disk; with `arraybuffer` it is likely to keep it in memory [from source] (HPBN p.308).
- An `ArrayBuffer` can be read through several *views* (`Uint8Array`, `Uint16Array`, `Float32Array`) with offset and count; the book shows mapping a C struct (16-byte user, 2-byte id, 32 floats) at offsets 0, 16 and 18 [from source] (HPBN p.309).

### Sending and `bufferedAmount`
- `send()` accepts `DOMString` (becomes UTF-8 on the wire), `ArrayBuffer`, `ArrayBufferView` or `Blob` [from source] (HPBN p.309-310).
- On the wire, the frame is marked only as text or binary by one bit; any other content-type information needs a mechanism of its own [from source] (HPBN p.310).
- `send()` is asynchronous: the data goes into a client queue and the function returns immediately. A quick return does not prove it was sent [from source] (HPBN p.310).
- `bufferedAmount` reports how much is in the queue. The book shows sending the next update only if it is zero [from source] (HPBN p.310).
- Reason: messages go out in the exact order of queuing, so a large queue, or a single large message, delays everything behind it (*head-of-line blocking*). Mitigations: split large messages, watch `bufferedAmount` and keep your own priority queue [from source] (HPBN p.310).
- Applications with several message classes (high-priority control, low-priority background transfer) must decide carefully when each enters the socket [from source] (HPBN p.311).

### Emulation (polyfill)
- Version 13 (RFC 6455) was supported by all modern browsers except the Android browser [DATED] (HPBN p.307).
- Emulating the API is easy; the hard part is the transport. SockJS exposes a WebSocket-like object and ships its own server with alternative transports; Socket.IO adds heartbeat, timeout and automatic reconnection [from source] (HPBN p.307).
- Rule: always use the native interface when it exists and verify that the fallback transport (XHR polling, EventSource, iframe polling) meets the performance goal [from source] (HPBN p.307).

---

## 2. Subprotocols

- The protocol treats the content as opaque and there is no equivalent of per-message HTTP headers; metadata requires agreement between the parties [from source] (HPBN p.311).
- Strategies cited: an agreed fixed format (all JSON, or a custom binary); a consistent message header that instructs how to decode the rest; a mix of a text message (as "headers") followed by a binary message (payload) [from source] (HPBN p.311).
- Negotiation: the client passes the list (in the example, `appProtocol` and `appProtocol-v2`); the server picks one; in `onopen` one reads `ws.protocol`. If the server accepts none, the handshake does not complete: `onerror` fires and the connection ends [from source] (HPBN p.311-312).
- The names are defined by the application and travel in the HTTP handshake with no effect on the rest of the API [from source] (HPBN p.312).

---

## 3. HTTP Upgrade handshake

Why HTTP: compatibility with the infrastructure (WebSocket servers on 80 and 443, often the only open ports) and reuse of the Upgrade flow with its own headers [from source] (HPBN p.312, 316).

| Header | Sent by | Function |
| :--- | :--- | :--- |
| `Sec-WebSocket-Version` | client | protocol version (`13` = RFC 6455); if the server does not support it, it replies with the list of versions it supports [from source] (HPBN p.316) |
| `Sec-WebSocket-Key` | client | automatically generated key; it is the "challenge" that proves server support [from source] (HPBN p.317) |
| `Sec-WebSocket-Accept` | server | signed value derived from the key [from source] (HPBN p.317) |
| `Sec-WebSocket-Protocol` | both | client advertises a list; server replies with a single name [from source] (HPBN p.317) |
| `Sec-WebSocket-Extensions` | both | client advertises extensions; server confirms one or more by returning the header [from source] (HPBN p.317) |

Full flow [from source] (HPBN p.317-318):
1. `GET` request with `Connection: Upgrade`, `Upgrade: websocket`, version 13, key, and optionally subprotocols and extensions; the browser adds `Origin`.
2. `101 Switching Protocols` response with `Upgrade`, `Connection`, `Sec-WebSocket-Accept` and the server's choices. The book's example includes `Access-Control-Allow-Origin` to authorize cross-origin.
3. `Accept` algorithm: concatenate the key with a fixed GUID from the specification, compute SHA-1 and encode in base64 (HPBN p.318).
4. Once the handshake is complete, the connection becomes a two-way channel and there is no more explicit HTTP exchange; the WebSocket protocol takes over (HPBN p.318).

Mandatory minimum and decision rules [from source] (HPBN p.318):
- The client **must** send `Sec-WebSocket-Version` and `Sec-WebSocket-Key`; the server **must** confirm with `Sec-WebSocket-Accept`.
- Subprotocols are optional for the client; if the client lists them and the server supports none, the connection is aborted.
- Extensions are optional; without server confirmation, the connection proceeds without them.

Security in the handshake: the request is subject to the same-origin policy; the server decides whether to accept or deny cross-origin with CORS (HPBN p.317). The server can use the HTTP cookie from the upgrade to validate the user and refuse the connection [from source] (HPBN p.322).

---

## 4. Binary framing

Each application message becomes one or more **frames**; the receiver is only notified once the complete message has been reassembled. Terms: *frame* = smallest unit (variable header + payload); *message* = sequence of frames that forms a logical message. Whoever fragments is the client/server implementation, not the application [from source] (HPBN p.313).

Header fields [from source] (HPBN p.313-314):

| Field | Size | Meaning |
| :--- | :--- | :--- |
| FIN | 1 bit | indicates whether it is the last fragment of the message; a message can have a single frame |
| Opcode | 4 bits | 1 = text, 2 = binary (data); 8 = close connection, 9 = ping, 10 = pong (liveness control) |
| Mask | 1 bit | indicates whether the payload is masked (client to server only) |
| Payload length | variable | 0–125: is the size itself; 126: the next 2 bytes carry a 16-bit unsigned integer; 127: the next 8 bytes carry a 64-bit unsigned integer |
| Masking key | 32 bits | value used for masking |
| Payload | variable | application data plus extension data, if negotiated |

### Per-frame overhead
- Frame sent by the server: **2–10 bytes** of framing. Client: adds 4 bytes of key, resulting in **6–14 bytes** [from source] (HPBN p.314). Figure 17-1 summarizes it as "2–14 bytes + payload" (HPBN p.313).
- By payload range [inference from the length field]: server 2 bytes (≤125), 4 bytes (126, 16 bits) and 10 bytes (127, 64 bits); the client adds 4 in each case.
- No other metadata exists: the payload is an opaque block [from source] (HPBN p.314).
- Per-message comparison: SSE from 5 bytes; HTTP/1.x (XHR or other) 500–800 bytes of metadata plus cookies; HTTP/2 compresses headers and gets down to 8 bytes if they do not change. These numbers exclude IP, TCP and TLS, which add 60–100 bytes per message [from source] (HPBN p.321).

### Client masking
- Every client-initiated payload is masked with the value in the header. Purpose: to prevent malicious script on the client from carrying out a cache-poisoning attack against intermediaries that do not understand WebSocket. The book refers to the paper "Talking to Yourself for Fun and Profit" (W2SP 2011) for the attack [from source] (HPBN p.314).
- The book does not describe the mask algorithm, nor the obligation for the server to close the connection if it receives an unmasked frame [outside the book; see "What the source does not cover"].

---

## 5. Multiplexing and head-of-line blocking

- WebSocket suffers from HoL: frames of different messages cannot be interleaved, because there is no stream identifier like HTTP/2's. A large message, even fragmented, delays the others; for latency-sensitive data, limit the size of each message and split the large ones [from source] (HPBN p.314).
- Without multiplexing in the core of the specification, **each WebSocket connection takes its own TCP connection**, which weighs on HTTP/1.x because of the per-origin connection limit [from source] (HPBN p.314).
- The multiplexing extension (HyBi) puts a *channel ID* in the frames and maintains logical channels, each with its own handshake, over a single TCP. Each channel remains subject to HoL; possible workaround: distinct channels or dedicated TCPs to parallelize messages [from source] (HPBN p.314-315).
- The extension is only necessary on HTTP/1.x; for HTTP/2 there was no official specification, but it would be simpler to encapsulate WebSocket frames in HTTP/2 framing [DATED] (HPBN p.315).

---

## 6. Extensions and compression

- The specification allows extending the wire format with new opcodes and fields, with no intervention from application code. The client advertises the extensions in the Upgrade and the server selects and confirms the ones that apply for the entire connection [from source] (HPBN p.315-316).
- Two official extensions under development in 2013: multiplexing and compression [from source] (HPBN p.315).
- The base protocol does not compress: each frame carries the payload as the application delivered it. The compression extension is equivalent to HTTP's *transfer-encoding* negotiation [from source] (HPBN p.315-316).
- [DATED] State in mid-2013: no popular browser supported multiplexing; compression was limited, with recent Chrome and WebKit advertising `x-webkit-deflate-frame`, based on an old revision and doomed to be abandoned; per-frame compression is suboptimal for large messages split across several frames, and the per-message version was experimental and still unavailable (HPBN p.316).
- Practical consequence at the time: apply your own compression according to content type, especially on mobile, where each byte costs the user [from source] (HPBN p.316, 322).
- Compressing the entire stream makes no sense because binaries may already be compressed; hence compression needs to be selective per message (HPBN p.322).

---

## 7. Proxies, intermediaries and WSS

- Users usually have only ports 80 and 443 open; that is why negotiation uses HTTP Upgrade [from source] (HPBN p.319).
- HTTP intermediaries that do not understand WebSocket may: blindly promote the connection, buffer frames, alter content, treat the traffic as compromised HTTP [from source] (HPBN p.319).
- The Key/Accept exchange protects against servers and intermediaries that would accept the upgrade without understanding the protocol, but is not enough against transparent proxies, which can inspect and modify the stream without notice [from source] (HPBN p.319).
- Fix: **use WSS**. Negotiating TLS before the Upgrade creates an encrypted tunnel and solves these problems, mainly for mobile clients, whose traffic goes through varied proxies [from source] (HPBN p.319). On external networks, the TLS tunnel lets you traverse intermediary proxies; it does not prevent one from dropping idle TCP, but in practice it raises the success rate and often extends the timeouts [from source] (HPBN p.323).
- Some networks block WebSocket entirely: you need a fallback strategy [from source] (HPBN p.323).

### Own infrastructure
HTTP is optimized for short transfers, so servers, proxies and load balancers aggressively drop idle connections. Three layers to consider: own infrastructure (routers, load balancers, proxies), external proxies (ISP, carrier) and the client's network [from source] (HPBN p.323).
- Nginx 1.3.13+ proxies WebSocket but, by default, uses a 60 s timeout. The book's example uses `proxy_http_version 1.1`, passes along `Upgrade` and `Connection "upgrade"` and raises `proxy_read_timeout` and `proxy_send_timeout` to 3600 [DATED as to version] (HPBN p.324).
- HAProxy: the `connect`, `client` and `server` timeouts (30 s in the example) apply only to the HTTP Upgrade handshake; after the upgrade, what governs is `timeout tunnel` (1 h in the example) [from source] (HPBN p.324).
- Rule: check the infrastructure **before** implementing keepalive in the application [from source] (HPBN p.324). Long, idle sessions take up memory and sockets in all intermediaries, so short timeouts have a security and operational justification [from source] (HPBN p.324).

---

## 8. When to use and performance

### Data flow
Only WebSocket allows bidirectional communication over the same TCP connection, with low-latency delivery in both directions. XHR serves transactional request and response exchanges, with no request streaming; SSE does efficient server-to-client streaming and the client sends nothing after the initial handshake [from source] (HPBN p.320).

### Latency
Replacing XHR with SSE or WebSocket **does not reduce propagation latency** (RTT). What disappears is queuing latency: the message waiting for the next poll. "Low latency" here means eliminating that wait [from source] (HPBN p.321).

### Custom protocols and cache
- By using a custom protocol, the application gives up browser services (authentication, cache, compression) and may have to reimplement cache, state management and message metadata [from source] (HPBN p.322).
- Binary over WebSocket does not enter the cache of the browser or of intermediaries such as a CDN, which causes unnecessary transfers and more traffic at the origin. Suggested strategy: use the session for non-cacheable data (real-time updates, control messages) and fire XHR to download assets [from source] (HPBN p.323).

### Performance checklist [from source] (HPBN p.325)
1. Use WSS (TLS) for reliable deployments.
2. Mind polyfill performance, if any.
3. Use subprotocol negotiation to define the application protocol.
4. Optimize binary payloads.
5. Consider compressing UTF-8 content.
6. Set the correct `binaryType`.
7. Monitor `bufferedAmount`.
8. Split large messages to avoid HoL.
9. Use other transports where it makes sense.

Mobile: real-time push can be a battery antipattern. The book points to the topics of preserving battery, eliminating periodic transfers, Nagle with efficient push and eliminating unnecessary application keepalives [from source] (HPBN p.325). See [`redes-moveis-rrc-state-machine-e-tail-time.md`](redes-moveis-rrc-state-machine-e-tail-time.md).

---

## After the book [extrapolation]

- Per-message compression was standardized as the `permessage-deflate` extension (RFC 7692), replacing `x-webkit-deflate-frame`.
- RFC 8441 defines WebSocket over HTTP/2 (stream connection with extended CONNECT); per-channel multiplexing became unnecessary in that scenario.
- Fetch streaming APIs and WebTransport (over HTTP/3) attack, in another way, the HoL between messages that the book describes.
- The close codes and the mask/server rules come from the full RFC 6455.

## What the source does not cover

- The literal value of the `Sec-WebSocket-Accept` GUID, the size (16 bytes) of the key and the mask algorithm (XOR with the 4-byte key): the book only describes their existence and purpose.
- RSV1–RSV3 bits, the continuation opcode (0), close codes and detailed ping/pong semantics: the book lists only opcodes 1, 2, 8, 9 and 10.
- The rule that the server closes the connection on receiving an unmasked frame (and the client on receiving a masked one).
- Maximum message size, server backpressure policies, horizontal scaling and session authentication beyond the cookie on the upgrade.
- Any browser support later than mid-2013.
