# WebRTC: P2P, ICE/STUN/TURN, SDP, DTLS/SRTP/SCTP and DataChannel

Summary of chapter 18 of *High Performance Browser Networking* (Grigorik, 2013), PDF p.327–380. The pages are **PDF** pages (printed = PDF − 18). Labels: `[from source]`, `[inference]` (my deduction), `[DATED]` (2013 draft/state that has changed). NAT, STUN and TURN in UDP terms are in [`udp-e-protocolos-de-transporte-alternativos.md`](udp-e-protocolos-de-transporte-alternativos.md); WebSocket in [`websockets-full-duplex-e-enquadramento.md`](websockets-full-duplex-e-enquadramento.md).

---

## 1. Overview and state in 2013

- WebRTC is a set of standards, protocols and JavaScript APIs for peer-to-peer audio, video and data between browsers, without plug-ins. Three main APIs: `MediaStream` (audio and video capture), `RTCPeerConnection` (audio and video communication) and `RTCDataChannel` (arbitrary data) [from source] (HPBN p.327).
- Unlike all other browser communication, WebRTC carries its data over **UDP**; but UDP is only the starting point [from source] (HPBN p.327).
- [DATED] The book states WebRTC is enabled for more than 1 billion users (recent Chrome and Firefox) and "under construction": the chapter's APIs and protocols could change (HPBN p.328). The examples use unprefixed APIs, and the code may need adjusting to the browser (HPBN p.341).
- Bodies: the W3C WEBRTC group defines the APIs; the IETF RTCWEB group defines protocols, formats and security. WebRTC reuses concepts from VoIP, SIP clients and the telephone network (PSTN), without requiring interoperability (HPBN p.328).
- The book cites 4.7 trillion dollars as the size of the telecommunications industry in 2012 (HPBN p.328).

---

## 2. Audio and video engines and `getUserMedia`

- The browser ships audio and video engines that process the signal: noise reduction, echo cancellation, narrowband or wideband codecs and concealment of jitter and packet-loss errors; video is equivalent (HPBN p.329-330). The pipeline continuously adapts to network conditions (HPBN p.330).
- `MediaStream` contains one or more tracks (`MediaStreamTrack`) synchronized with each other; the source can be a microphone, webcam or local or remote file; the output can go to an audio or video element, JavaScript code or a remote peer [from source] (HPBN p.330-331).
- `getUserMedia()` takes mandatory and optional constraints (the example requires minimum width 320 and minimum height 180, and optionally asks for maximum width 1280, 30 frames per second and front camera) [DATED by the `mandatory`/`optional` syntax and callbacks] (HPBN p.331-332).
- The captured media can feed Web Audio, Canvas and CSS3/WebGL (HPBN p.332).

### Bit rates [from source] (HPBN p.332-333)
| Codec | Range |
| :--- | :--- |
| Opus (audio) | 6–510 Kbit/s, constant or variable rate, adapts without interruption |
| VP8 (video) | 100–2,000+ Kbit/s |
| VP8 720p at 30 FPS | 1.0–2.0 Mbps |
| VP8 360p at 30 FPS | 0.5–1.0 Mbps |
| VP8 180p at 30 FPS | 0.1–0.5 Mbps |

An HD call with a single interlocutor may need 2.5+ Mbps; with more peers, quality has to drop (HPBN p.333). [DATED] Opus and VP8 were the codecs of the implementations of the time (HPBN p.332).

---

## 3. Why UDP and what the stack is

- Real time prioritizes timeliness over reliability: codecs fill small gaps, and the brain is sensitive to variable latency but tolerates occasional losses [from source] (HPBN p.333).
- TCP buffers everything after a lost packet and waits for the retransmission. UDP offers "non-services": no delivery guarantee (no ACKs, retransmission or timeouts), no ordering guarantee (no sequence or HoL), no connection state and no congestion control [from source] (HPBN p.333). It is a thin layer over best-effort IP (HPBN p.334).
- But raw UDP does not solve NAT and firewall traversal, parameter negotiation, encryption, and congestion and flow control. Hence the stack (HPBN p.334-335):

| Protocol | RFC (per the book) | Role |
| :--- | :--- | :--- |
| ICE | 5245 | establish and maintain the peer-to-peer connection over UDP |
| STUN | 5389 | public address discovery (used by ICE) |
| TURN | 5766 | last-resort relay (used by ICE) |
| SDP | 4566 | session description format, exchanged out of band |
| DTLS | 6347 | encryption and key exchange; encryption is mandatory |
| SCTP | 4960 | application data transport (DataChannel) |
| SRTP | 3711 | audio and video transport |

- Note on an inconsistency in the book: the list on p.335 gives RFC 4566 for SDP, but the text on p.342 writes "RFC 4568". Prefer 4566 [inference].
- SDP does not appear in the diagram because offer and answer travel out of band (HPBN p.335).

---

## 4. `RTCPeerConnection`

Handles the lifecycle of each connection: runs the full ICE flow, sends automatic STUN keepalives, tracks local and remote streams, renegotiates streams automatically when needed, generates offers, accepts answers and lets you query the state [from source] (HPBN p.335-336). Once established, adding or removing streams triggers automatic SDP renegotiation (HPBN p.352).

---

## 5. Signaling

- Establishing a P2P connection requires much more than opening XHR, EventSource or WebSocket, which presuppose HTTP and a reachable server. Peers are often on private networks, behind NATs, with no direct reachability [from source] (HPBN p.337).
- Problems to solve: notify the other peer of the intent to connect; identify route paths on both sides and exchange that information; agree on stream parameters (protocols, encodings). ICE solves the routes and connectivity verification; **signaling and the initial negotiation are left to the application** [from source] (HPBN p.338).
- The standard neither recommends nor implements the signaling channel, to allow interoperating with SIP, Jingle (an XMPP extension) and ISUP (telephone network) [from source] (HPBN p.338-339). You can use gateways to those systems or your own service with your own protocol (HPBN p.339). Example of proprietary signaling: Skype (HPBN p.340).
- Choice: there is no single answer. There are gateways that interoperate (Asterisk, with a WebSocket module for SIP); if interoperation is not needed, a custom signaler is simple: the site already knows who is logged in and relays the messages. Before inventing one, evaluate commercial and open-source options, and consider the latency of the signaling transport [from source] (HPBN p.340).

---

## 6. SDP, JSEP and the offer/answer flow

- SDP describes the "session profile": media types (audio, video, data), network transports, codecs and settings, bandwidth and other metadata; it does not deliver media [from source] (HPBN p.341). The example shows lines `m=audio ... RTP/SAVPF`, `a=candidate ... typ host` and `a=rtpmap ... opus/48000/2` (HPBN p.341).
- The application rarely touches the SDP: JSEP (JavaScript Session Establishment Protocol) hides it behind `RTCPeerConnection` methods. The SDP can be sent as plain text or re-encoded, for example to XMPP via Jingle [from source] (HPBN p.342).

Symmetric flow, with peers Amy (initiator) and Bob [from source] (HPBN p.342):
1. Amy registers local streams, calls `createOffer()` and sets the offer as the local description.
2. Amy sends the offer to Bob over the signaling channel.
3. Bob sets the offer as the remote description, registers his streams, generates the answer (`createAnswer()`) and sets it as the local description.
4. Bob returns the answer.
5. Amy sets the answer as the remote description.

Answerer code: the bulk of the logic runs when the offer arrives (`setRemoteDescription`, media capture, `createAnswer`) (HPBN p.352-353). Fewer than a hundred lines of JavaScript give a P2P video conference; SimpleWebRTC wraps this (public STUN, `getUserMedia`, WebSocket for signaling; you only decide the room name) (HPBN p.354).

---

## 7. ICE, STUN and TURN

### The ICE agent
- Each `RTCPeerConnection` contains an ICE agent that gathers local candidates (IP, port), performs connectivity checks and sends keepalives [from source] (HPBN p.343).
- When a session description is set, the agent: (1) queries the operating system for local IPs; (2) if configured, queries a STUN server to obtain the public IP and port; (3) if configured, adds TURN as a last-resort candidate, which relays the data if P2P fails [from source] (HPBN p.343).
- In the example SDP, `typ host` (192.168.1.73) and `typ srflx` (50.76.44.100, public address returned by STUN) candidates appear (HPBN p.344-345).
- Each new candidate fires `onicecandidate`; so does the end of gathering (HPBN p.344). The servers go in the configuration, for example `iceServers` with a `stun:` and a `turn:` with credential [DATED by the `url` syntax] (HPBN p.344).
- "What is my public IP?" is a manual STUN; the protocol lets the browser know whether it is behind NAT and discover the public IP and port (HPBN p.344).

### Connectivity check
- With the remote description set and the other peer's candidates, the agent sends a *STUN binding request*; the peer must confirm with a successful STUN response. If all candidates fail, the connection is marked as failed or falls back to a TURN relay [from source] (HPBN p.345-346).
- The agent orders the candidates: local IPs first, then public ones, TURN last. Once the connection is established, it continues to send periodic STUN requests as keepalive [from source] (HPBN p.346).
- Even when connected, the agent may test other candidates to find a better route (HPBN p.349).
- For performance: the process may cost several round trips to the STUN servers and between peers before the first byte (HPBN p.346).

### Trickle ICE
- Gathering local IPs is fast; querying STUN requires an external round trip, followed by another round of checks between peers (HPBN p.346).
- Trickle ICE: both exchange SDP offers **without** candidates; candidates go over the signaling channel as soon as they are discovered; checks start as soon as each candidate arrives [from source] (HPBN p.346). It generates more signaling traffic, but greatly improves connection time, and is the recommended strategy: send the offer as soon as possible and "trickle" the candidates (HPBN p.347).
- In code: `onicecandidate` sends `evt.candidate` over signaling; on receipt, `addIceCandidate()` (HPBN p.347).
- Book remark: the `c=IN IP4 0.0.0.0` in the SDP indicates use of trickle ICE (HPBN p.369).

### States
`iceGatheringState` has three values: `new`, `gathering`, `complete` [from source] (HPBN p.348). `iceConnectionState` has seven (HPBN p.348-349):

| State | Meaning |
| :--- | :--- |
| `new` | gathering and/or waiting for remote candidates |
| `checking` | received remote candidates and is testing pairs, no connection yet |
| `connected` | found a usable connection for all components, but is still looking for a better one |
| `completed` | finished gathering and checks and found a connection for all |
| `failed` | tested all pairs and found no connection for at least one component |
| `disconnected` | liveness checks failed; more aggressive than `failed`, may resolve on its own on an unstable network |
| `closed` | the agent stopped and no longer responds to STUN |

A successful connection establishes connectivity for all requested streams; it can alternate between `connected` and `disconnected` while the agent looks for a path (HPBN p.349). Debugging tool: `chrome://webrtc-internals` shows connections, SDPs and statistics on bandwidth, latency and bitrate [from source] (HPBN p.350).

### STUN and TURN in practice [from source] (HPBN p.345, 378)
- Always provide a STUN server, unless use is restricted to the internal network; without it most connections fail. It only acts at establishment, but it must speak STUN and have provisioned capacity (HPBN p.378).
- Even with STUN, about **8%–10%** of P2P connections fail because of network policies (for example, blocked UDP); the text on p.345 says ~8%. TURN is needed for reliability (HPBN p.345, 378).
- TURN is a last resort: extra hop and 1+ Mbps streams saturate the service; it requires capacity planning (HPBN p.378).

---

## 8. Secure delivery: DTLS

- All WebRTC data (audio, video, application) must be encrypted in transit. TLS does not work over UDP because it depends on reliable, ordered delivery; DTLS is used, which is TLS with minimal changes for datagrams [from source] (HPBN p.355).
- Problems DTLS solves: the TLS handshake requires reliable, ordered delivery that accepts fragmentation; TLS integrity checks fail if records are fragmented or processed out of order (HPBN p.355).
- DTLS adds a "mini-TCP" just for the handshake: a sequence number and fragment offset in each handshake record and retransmission timers. Records follow the exact order of TLS (HPBN p.356).
- Both peers generate **self-signed** certificates; there is no chain of trust to verify. The DTLS handshake takes **two round trips** (extra latency at connection) [from source] (HPBN p.356-357).
- Additional rules: each DTLS record with data fits in a single UDP packet (TLS allows up to 16 KB, but UDP neither fragments nor reassembles); stream ciphers are forbidden, a block cipher is used (HPBN p.357).
- DTLS gives encryption and integrity, but leaves authentication to the application: prior login, or an *identity provider* declared in the SDP (a mechanism still under discussion at the W3C in 2013 [DATED]) (HPBN p.357-358).

---

## 9. Media: SRTP and SRTCP

- The application only defines the media constraints; the rest (encoding, loss, jitter, flow control) belongs to the browser. There is no direct control over optimization or delivery [from source] (HPBN p.358-359).
- The browser's flow and congestion control starts transmitting at a low rate (**< 500 Kbps**) and adapts quality throughout the connection; it is a variant of *adaptive streaming*. It may deliver lower quality than captured, but **never higher**; the 360p constraint works as a bandwidth ceiling [from source] (HPBN p.359).
- SRTP is the secure profile of RTP (RFC 3550 in the original; security in RFC 3711). It guarantees neither timeliness nor error recovery: it only wraps audio samples and video frames with metadata [from source] (HPBN p.359-360).
- **12-byte** SRTP header plus optional fields: increasing sequence number (detects out of order), timestamp of the first byte's sampling (synchronizes tracks, such as audio and video), stream **SSRC** identifier, optional metadata, encrypted payload and authentication tag (HPBN p.360).
- SRTCP is each stream's out-of-band feedback channel: it accounts for bytes and packets sent and lost, last sequence number and inter-arrival jitter; periodically the peers exchange this data to adjust rate and quality [from source] (HPBN p.360-361).
- Required adaptations: SRTP/SRTCP do not negotiate keys, so DTLS runs first and the shared secret becomes keying material; both ask for one port per stream, and WebRTC uses a multiplexing extension to deliver several streams and controls on the same destination port; the IETF was developing new congestion control algorithms based on SRTCP [from source] (HPBN p.361).

---

## 10. Data: SCTP over DTLS over UDP

DataChannel transport requirements: multiplex independent channels; each channel with ordered or unordered, reliable or unreliable delivery, and optional priority; message-oriented API (fragmentation and reassembly); flow and congestion control; confidentiality and integrity [from source] (HPBN p.362). DTLS already covers the last two; SRTP does not suit application data (HPBN p.362).

| | TCP | UDP | SCTP |
| :--- | :--- | :--- | :--- |
| Reliability | reliable | no | configurable |
| Delivery | ordered | unordered | configurable |
| Transmission | byte-oriented | message-oriented | message-oriented |
| Flow control | yes | no | yes |
| Congestion control | yes | no | yes |

[from source] (HPBN p.362)

SCTP terminology: *association* = connection; *stream* = unidirectional channel within which messages go out in sequence (unless the channel is unordered); *message* = application data; *chunk* = smallest unit within an SCTP packet. The book compares with HTTP/2's streams, messages and frames, but at a lower layer (HPBN p.363).

Packet and data chunk [from source] (HPBN p.363-364):
- **12-byte** common header: source and destination ports, random association verification tag and checksum.
- Data chunk: type 0x0; U bit (unordered); B and E bits (B=1,E=0 first fragment; B=0,E=0 middle; B=0,E=1 last; B=1,E=1 unfragmented message); length (includes the 16-byte header); 32-bit TSN (acknowledges receipt and detects duplicates); stream identifier; stream sequence number (fragments of the same message share it); PPID.
- DataChannel uses the PPID to mark the type: **0x51** for UTF-8 and **0x52** for binary.
- There are redundant fields (the ports, already present in UDP) (HPBN p.364). SCTP keeps the sequence number per message for ordered delivery; with the U bit, it still uses the sequence for fragmentation, but delivers out of order (HPBN p.365).
- **Total overhead: 28 bytes** per data chunk (12 of common header + 16 of chunk header) (HPBN p.365).

Performance remarks [from source] (HPBN p.365):
- SCTP also has its own handshake, similar to TCP's, and TCP-friendly flow and congestion control, with the same initial window and growth and reduction logic in the congestion avoidance phase. Costs and implications are similar to TCP's (see [`fundamentos-tcp-e-gargalos-de-transporte.md`](fundamentos-tcp-e-gargalos-de-transporte.md)).
- Base SCTP (RFC 4960) lacks two things: configuring reliability per message, solved by the partial reliability extension (RFC 3758), and stream prioritization, which has no field in the protocol and is left to higher layers.

"Raw SCTP" over IP: existing routers and NATs do not handle SCTP properly, so WebRTC tunnels it over UDP and DTLS, in user space. In controlled networks (such as the core of mobile operators) SCTP works well [from source] (HPBN p.366). Message orientation avoids the HoL of stream-oriented protocols such as TCP (HPBN p.366).

---

## 11. DataChannel

### API and comparison with WebSocket [from source] (HPBN p.366-368)
- Bidirectional exchange of text or binary between peers, with the same shape as the WebSocket API: callbacks `onerror`, `onclose`, `onopen`, `onmessage` and fields `binaryType`, `bufferedAmount` and `protocol`. The API is a superset of WebSocket's, so everything that holds for text/binary processing and subprotocols applies.
- Differences: it is created by a `RTCPeerConnection` method (`createDataChannel`), not by URL; either peer can open a channel and the other receives `onDataChannel` [DATED by the event name]; each channel has its own delivery and reliability semantics.

| | WebSocket | DataChannel |
| :--- | :--- | :--- |
| Encryption | configurable | always |
| Reliability | reliable | configurable |
| Delivery | ordered | configurable |
| Multiplexed | no (extension) | yes |
| Transmission | per message | per message |
| Binary / UTF-8 | yes / yes | yes / yes |
| Compression | no (extension) | no |

[from source] (HPBN p.368). WebSocket runs over TCP; DataChannel over UDP (P2P connectivity), DTLS (encryption) and SCTP (multiplexing, flow and congestion) (HPBN p.368).

### Setup and negotiation [from source] (HPBN p.368-371)
- Before any data, the entire offer/answer flow and connectivity checks apply (HPBN p.368). Media uses SRTP; data uses SCTP, announced in the SDP: `m=application 1 DTLS/SCTP 5000`, `a=fmtp:5000 protocol=webrtc-datachannel; streams=10` (up to 10 parallel streams) (HPBN p.369).
- It is enough for one of the peers to register the DataChannel before generating the SDP. For a data-only connection, `OfferToReceiveAudio` and `OfferToReceiveVideo` constraints set to false [DATED by the syntax] (HPBN p.369).
- The SDP does not describe each channel; therefore the initiator sends a **DATA_CHANNEL_OPEN** message with type, reliability and application protocol. It plays a role similar to HTTP/2's HEADERS: it opens the stream implicitly and data can follow right away (HPBN p.369-370).
- Each channel is an **independent SCTP stream**, multiplexed in the same association, which avoids HoL between channels (HPBN p.370).
- Out-of-band negotiation: `negotiated: true` suppresses DATA_CHANNEL_OPEN, and both peers pass the same integer `id`. No performance gain with few peers; useful when the signaling server distributes the same description to many participants (HPBN p.370-371).

### Order and reliability [from source] (HPBN p.371-373)
Two partial-reliability policies: **maximum retransmissions** (count) or **lifetime** (ms). They are mutually exclusive: specifying both raises an error. The WebRTC client itself applies them; the application does not manage counters or timers.

| Configuration | Ordered | Reliable | Parameter |
| :--- | :--- | :--- | :--- |
| Ordered + reliable | yes | yes | none (equivalent to TCP) |
| Unordered + reliable | no | yes | none (TCP without HoL) |
| Ordered + partial (count) | yes | partial | `maxRetransmits` |
| Unordered + partial (count) | no | partial | `maxRetransmits` |
| Ordered + partial (time) | yes | partial | `maxRetransmitTime` (ms) |
| Unordered + partial (time) | no | partial | `maxRetransmitTime` (ms) |

- Default configuration `{}`: ordered and reliable. `{ ordered: false, maxRetransmits: 0 }` = unordered and unreliable delivery, UDP semantics (HPBN p.372-373).
- [DATED] Names and options are those of 2013: `maxRetransmitTime` and the `reliable` attribute, which returns false if any partial policy is used; `maxRetransmits` and `maxRetransmitTime` are read-only after creation (HPBN p.372-373).
- Several channels, each with its own configuration, share the SCTP association; example: reliable, ordered chat and transient or low-priority updates unordered and partially reliable (HPBN p.373).

### Message size on a partially reliable channel [from source] (HPBN p.373-374)
Book scenario: unordered channel, `maxRetransmits: 0`, ~1% loss, 120 KB message.
- SCTP packet MTU: **1,280 bytes** (the recommended IPv6 minimum). Overhead: IP 20–40, UDP 8, DTLS 20–40, SCTP 28 bytes, rounded to ~130, leaving ~**1,150 bytes** of payload per packet and **107 packets** for the 120 KB.
- With 1% loss per packet, the chance of losing at least one of the 107 is high; one is enough to discard the whole message.
- Remedies (ideally both): use retransmission (count or time) and shrink the message. On an unreliable channel, each message should fit in **one packet (< 1,150 bytes)**; if it does not fit, use retransmission. There is no universally optimal count or timeout value, because loss and latency vary; the best result comes from small messages.

---

## 12. Performance and multiparty architectures

### Bandwidth and latency (HPBN p.374-375)
- Audio and video remain limited by latency and bandwidth: HD asks for 1–2 Mbps, the global average in Q1 2013 was 3.1 Mbps, and HD asks for at least a 3.5G+ connection [DATED as to the numbers] [from source].
- Asymmetric connections: a 10-to-1 ratio is common (for example, 10 Mbps down and 1 Mbps up). A mobile client may receive HD (1 Mbps+) but need to send less; each party can transmit at a different bitrate. Media competes for bandwidth with DataChannel and other traffic [from source] (HPBN p.375).
- The media engines probe bandwidth; on DataChannel, the application must monitor the buffer and adjust [from source] (HPBN p.375).

### Mesh and star (HPBN p.376-377)
- One to one is simple. In a call with N participants, each peer connected to all the others (mesh) requires N − 1 connections per peer and N × (N − 1) in total; with a low uplink, it saturates the link with few participants.
- **Star** alternative: peers connect to a *supernode* that distributes the streams, so that only it pays the cost of N − 1 streams. The supernode can be a peer (in the simple case, the initiator; better, the peer with the highest throughput, which requires election and signaling, left to the application) or a dedicated or third-party service.
- "P2P optimization as a service": services such as Google Hangouts use proxies that aggregate and compose streams and deliver just one to each client (each receives one stream instead of N − 1). In games, a server filters and distributes only the relevant updates [from source] (HPBN p.377).

### Infrastructure and capacity [from source] (HPBN p.377-379)
- Every WebRTC application needs central infrastructure for signaling, NAT/firewall traversal, identity verification and other services (HPBN p.377).
- **Signaling:** low-latency transport (WebSocket or SSE with XHR); size for the signaling rate; after connecting, signaling can be migrated to the DataChannel, relieving the server and reducing latency. Signaling latency weighs on call setup time, especially with trickle ICE (HPBN p.378).
- **STUN/TURN:** see section 7.
- **Multiparty gateways:** like TURN, but an "intelligent proxy" consumes far more CPU and GPU to process each stream (HPBN p.378-379).

### Data efficiency
The media engines adjust bitrate automatically. DataChannel applies no compression or processing: the application must optimize binary payloads and compress UTF-8, and take into account the extra overhead of UDP, DTLS and SCTP and the peculiarities of partially reliable delivery. The WebSocket compression extension has no equivalent in WebRTC [from source] (HPBN p.379).

### Performance checklist [from source] (HPBN p.379-380)
- **Signaling:** low-latency transport; sufficient capacity; consider signaling over the DataChannel after connecting.
- **NAT and firewall:** provide STUN when creating the `RTCPeerConnection`; use trickle ICE whenever possible (more signaling, faster connection); provide TURN for connections that fail; provision capacity for the relays.
- **Distribution:** consider a supernode or dedicated intermediary in large groups; consider optimizing the data at the intermediary before forwarding.
- **Efficiency:** appropriate media constraints; optimize binaries and compress UTF-8 on DataChannel; monitor the DataChannel buffer.
- **Delivery and reliability:** unordered delivery to avoid HoL; if ordered, small messages; messages < 1,150 bytes; set appropriate retransmissions or timeouts (they depend on size, data type and latency between peers).

---

## After the book [extrapolation]

- The 2013 APIs changed: `getUserMedia` became `navigator.mediaDevices.getUserMedia` with Promises; `addstream`/`onaddstream` were replaced by `addTrack`/`ontrack`; `iceServers` uses `urls`; the channel options became `maxPacketLifeTime` and `maxRetransmits`, and the event is `ondatachannel`.
- Trickle ICE was standardized (RFC 8838), and the DataChannel protocol and its establishment have their own RFCs (RFC 8831 and RFC 8832) in place of the cited draft.
- SDP came to be handled with "unified plan" semantics; the WebSocket per-message compression standard (RFC 7692) does not apply to DataChannel.
- Additional codecs (H.264, AV1) and WebTransport appear as alternatives; check caniuse for current support.

## What the source does not cover

- NAT types (cone, symmetric) and ICE's candidate pair priority logic: the book only orders local, public and TURN, and refers to chapter 3 for NAT.
- The name `relay` for the TURN candidate type: the book's example shows only `typ host` and `typ srflx`.
- ICE gathering times in seconds, H.264 and the Trickle ICE RFC numbering: not in the book.
- Detailed format of DATA_CHANNEL_OPEN, full SDP encoding, simulcast, SVC, SRTCP congestion control in detail.
- Any identity security beyond what the book calls "under discussion", and browser support after 2013.
