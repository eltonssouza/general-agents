# UDP, NAT and traversal (STUN, TURN, ICE)

Sole source: *High Performance Browser Networking* (Grigorik, 2013), chapter 3. Cited pages are the PDF pages (printed = PDF − 18). For the use of ICE inside WebRTC, see [webrtc-p2p-ice-stun-turn-e-datachannel.md](webrtc-p2p-ice-stun-turn-e-datachannel.md).

---

## 1. What UDP is (and what it is not)

- UDP entered the suite in August 1980 (Jon Postel), when TCP and IP were being separated into distinct RFCs. Its appeal lies in what it omits; it is called the "null protocol", and RFC 768 is short (HPBN p.53).
- Datagram: an independent unit with enough information to be routed without depending on earlier exchanges. The term is usually reserved for services with no delivery guarantee or failure notice (HPBN p.53).
- DNS is the best-known use of UDP, which every browser depends on; even so, UDP was never a first-class transport for pages until WebRTC, which exposes it with a client API (HPBN p.53, p.54).
- IP does not guarantee delivery or report failures; recovering is the job of a protocol above it, if desired (HPBN p.54).
- 8-byte UDP header: just source port, destination port, length and checksum. Source and checksum are optional; the application may omit the checksum, delegating error detection and correction to itself (HPBN p.54, p.55). At bottom UDP is just "application multiplexing" over IP (HPBN p.55).
- List of non-services (HPBN p.55): no delivery guarantee (no ACK, retransmission or timeout); no ordering guarantee (no sequence, no reordering, no head-of-line blocking); no connection state (no handshake or teardown); no congestion control; no feedback mechanisms from the client or the network.
- Difference from TCP: TCP is a byte stream with no message boundaries; UDP preserves boundaries: each datagram goes in one IP packet and each read returns the whole message; there is no fragmentation of the datagram at the UDP layer (HPBN p.55).
- The book's warning: designing your own protocol over UDP risks ending up as a poorly implemented TCP; TCP's algorithms have been refined for decades (HPBN p.55, p.56). Also consider the interaction with middleboxes, especially NAT.

### When UDP makes sense
- Applications that tolerate loss and disorder and are sensitive to latency/jitter: audio (a codec can insert a small glitch instead of waiting for the packet), game state (waiting for the packet from instant T−1 when you already have the one from T is useless) and, for that reason, WebRTC uses UDP as its base (HPBN p.49, p.50).
- Absence of head-of-line blocking: a lost datagram does not hold back the following ones (HPBN p.55). Comparison with TCP in [fundamentos-tcp-e-gargalos-de-transporte.md](fundamentos-tcp-e-gargalos-de-transporte.md).

### Cost of choosing UDP
- The application will probably have to reimplement a lot (retransmission, reordering, flow and congestion control), and each part must coexist well with other peers and protocols (HPBN p.62).
- Congestion-insensitive UDP can overload the network and, in severe cases, lead to congestion collapse (HPBN p.62).

---

## 2. UDP and NAT

### Why NAT exists
- IPv4 has 32 bits, or 4.29 billion addresses. NAT (RFC 1631, mid-1994) was created as a stopgap solution: a device at the edge keeps a table that maps local (IP, port) tuples to public tuples, allowing the local space to be reused behind the translator (HPBN p.56). It became a permanent part of the infrastructure (routers, firewalls, proxies) (HPBN p.56).
- IANA reserved three private ranges, which can never be assigned to public machines (HPBN p.57):

| Range | Size |
|---|---|
| 10.x.x.x (/8 block) | 16,777,216 addresses |
| 172.16.x.x to 172.31.x.x | 1,048,576 addresses |
| 192.168.x.x | 65,536 addresses |

### Connection state timeouts
- TCP has a state machine (handshake, data, teardown) that lets NAT create and remove entries. UDP does not, so the translator keeps state about a stateless flow, and must decide on its own when to discard it (HPBN p.57).
- Since there is no teardown sequence, UDP entries expire by timer. The book says there is no definitive answer: the period depends on vendor, model, version and configuration (HPBN p.57, p.58). **There is no fixed timeout number in the source.**
- Recommended practice for long UDP sessions: send bidirectional keepalives to renew the timers on all NATs along the path (HPBN p.58).
- In practice, many NATs apply similar timeout logic to TCP as well; if TCP connections drop for no reason, suspect the NAT timeout, and bidirectional keepalives may be needed (HPBN p.58).
- RFC 5405 allows keepalives when necessary, with a minimum interval of 15 seconds (HPBN p.63).

### NAT traversal: the problem
- The internal client does not know its public IP. If it advertises the private IP to an external peer, the connection fails; "transparent translation" ceases to hold and the application must discover its own public address (HPBN p.58).
- Even knowing the public IP, an incoming packet with no matching entry in the NAT table is simply dropped, unless the user configures port forwarding (HPBN p.58, p.59).
- This does not affect clients that initiate communication from inside. It affects P2P applications (VoIP, games, file sharing) that need to receive incoming connections (HPBN p.59). The solution: traversal techniques (TURN, STUN, ICE) (HPBN p.59).

### STUN (RFC 5389)
- Lets the application discover whether there is a NAT and, if so, obtain the public IP:port tuple allocated for the current connection; requires a public, well-known STUN server (HPBN p.59).
- Flow: the application sends a *binding request* to the STUN server (address obtained via DNS or configured manually); the response carries the client's IP and port as seen from outside (HPBN p.60).
- Benefits (HPBN p.60): the application can use the public address in data exchanged with peers; the outgoing request creates routing entries in the NAT, so incoming packets on that tuple find the way back; STUN defines keepalive to avoid expiry.
- Procedure between two peers: each makes its binding request; after a response on both sides, they use the public tuples to exchange data (HPBN p.60).
- Limit: STUN does not solve all NAT topologies, and UDP may be blocked by a firewall (common in corporate networks) (HPBN p.60).

### TURN (RFC 5766)
- Fallback when STUN fails; can run over UDP and switch to TCP if nothing else works (HPBN p.60).
- Mechanics: both clients send an *allocate request* to the same TURN server and negotiate permissions; then they send their data to the server, which relays it to the other peer (HPBN p.61).
- It is the most reliable way to connect any two peers, but it stops being P2P and has a high operating cost: the relay needs capacity for all flows. Use it as a last resort (HPBN p.61).

### Practical data: libjingle
- The libjingle library (C++, used in Google Talk) handles STUN, TURN and ICE; its documentation indicates 92% of connections direct (STUN) and 8% requiring a relay (TURN) (HPBN p.61) [DATED]. The book's conclusion: even with STUN, a relevant share of users cannot get a direct P2P tunnel; a reliable service needs TURN.

### ICE (RFC 5245)
- A protocol and set of methods that seek the most efficient tunnel: direct connection when possible, STUN negotiation when necessary and, finally, fallback to TURN (HPBN p.61, p.62).
- Recommendation: for P2P over UDP, use a platform API or library that implements ICE, STUN and TURN (HPBN p.62).

---

## 3. Guidelines for those who use UDP

From RFC 5405 (guidelines for unicast applications over UDP), the book's sample (HPBN p.62, p.63):
- tolerate a wide variety of path conditions;
- control the transmission rate;
- apply congestion control over all traffic;
- use bandwidth similar to TCP's;
- back off the retransmission counters after losses;
- do not send datagrams larger than the path MTU;
- handle loss, duplication and reordering of datagrams;
- be robust to delivery delays of up to 2 minutes;
- enable the UDP checksum on IPv4 and (mandatorily) on IPv6;
- keepalives may be used, with a minimum interval of 15 seconds.

The book's final advice: reuse a library or framework that already handles NAT traversal and fairness with other flows; WebRTC is one of those frameworks (HPBN p.63).

TLS's use of UDP: DTLS (RFC 6347) adapts TLS to keep the datagram model (HPBN p.66). Details in [tls-handshakes-resumption-e-alpn.md](tls-handshakes-resumption-e-alpn.md).

---

## After the book [extrapolation]
- In later literature, NATs are classified by mapping/filtering behavior (full cone, restricted, symmetric); symmetric NAT usually forces the use of a TURN relay. The book does not make this classification.
- ICE candidates (host, server-reflexive via STUN, relay via TURN) and connectivity checks appear in the ICE specification; the book only describes the order of preference direct, STUN, TURN. The current version is RFC 8445.
- QUIC (RFC 9000) is a new transport built over UDP; it puts into practice the idea of "UDP as a base for new protocols" mentioned in HPBN p.62, but is later than the book.

---

## What the source does not cover
- NAT types (full cone, restricted, symmetric), hole punching and the detail of ICE candidates: ch. 3 only gives the STUN/TURN/ICE overview.
- A numeric NAT timeout value for UDP: the book states that it varies by equipment.
- QUIC, HTTP/3, DTLS in detail and SRTP.
- WebRTC and its data channels (ch. 18) are in another file.
- IPv6 as an alternative to NAT: the book only mentions the scarcity of IPv4.
