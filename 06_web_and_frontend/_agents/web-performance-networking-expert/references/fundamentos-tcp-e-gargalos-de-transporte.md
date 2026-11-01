# Latency, bandwidth and TCP fundamentals: where network time really goes

Sole source of this file: *High Performance Browser Networking* (Grigorik, O'Reilly, 2013), chapters 1 and 2. Every cited page is the PDF page (printed = PDF − 18). The book is from 2013: what it treats as recent is marked [DATED].

---

## 1. Latency and bandwidth (ch. 1)

### Definitions and components of latency
- Latency is the time between the source emitting a packet and the destination receiving it. Bandwidth is the maximum throughput of a logical or physical path (HPBN p.21).
- End-to-end latency is the sum of four delays (HPBN p.23):
  - **propagation**: distance divided by signal speed;
  - **transmission**: time to put all the bits on the link, a function of packet size and link rate;
  - **processing**: reading the header, checking for bit errors, deciding the route;
  - **queuing**: waiting in the input buffer when packets arrive faster than the router can process them.
- Propagation is independent of bandwidth; transmission is independent of distance. Book example: 10 Mb on a 1 Mbps link takes 10 s to enter the wire; at 100 Mbps, 0.1 s (HPBN p.23).
- **Bufferbloat**: routers with huge input buffers, assuming that dropping a packet is always bad, break TCP congestion control and produce high, variable latency. The book cites the CoDel algorithm, then present in Linux 3.5+ kernels (HPBN p.24) [DATED].

### Physical limit
- Speed of light in a vacuum: 299,792,458 m/s. In fiber, the rule of thumb is about 200,000,000 m/s (refractive index ~1.5; fibers range from 1.4 to 1.6) (HPBN p.24).
- Book Table 1-1 (one-way in fiber / RTT in fiber): New York–San Francisco 4,148 km, 21 ms / 42 ms; New York–London 5,585 km, 28 ms / 56 ms; New York–Sydney 15,993 km, 80 ms / 160 ms (HPBN p.25).
- These values are optimistic (they assume the great-circle route). The real New York–Sydney RTT is between 200 and 300 ms (HPBN p.25).
- Improving materials and routers would yield at most about 30% more, because we are already at ~1.5 times the speed of light (HPBN p.30).
- Example of the cost of latency: the "Hibernia Express" transatlantic cable (early 2011) aimed to save 5 ms between London and New York, for more than US$ 400 million, or US$ 80 million per millisecond (HPBN p.22) [DATED].

### User perception (design rule)
- Above ~100–200 ms of delay the user already reports "lag"; above 300 ms the interaction feels slow; at 1,000 ms many have already switched mental context. The book's conclusion: the application must respond in hundreds of milliseconds, and network latency must be an explicit design criterion (HPBN p.25).

### Last mile and measurement
- The last mile is usually the expensive stretch. FCC measurement in February 2013, peak hour: fiber-to-the-home 18 ms, cable 26 ms, DSL 44 ms to the first ISP node (HPBN p.26) [DATED].
- `traceroute` (on Windows, `tracert`) sends packets with an increasing hop limit (1, 2, 3...); each intermediate node that exceeds the limit returns ICMP Time Exceeded, which allows measuring the delay hop by hop (HPBN p.27).

### Bandwidth in the core and at the edge
- Each fiber carries several wavelengths (WDM); capacity is rate per channel × number of channels. The book cites, in early 2010, more than 400 wavelengths at 171 Gbit/s each, above 70 Tbit/s per fiber (HPBN p.27) [DATED].
- At the edge capacity is much lower and variable; the bandwidth available to the user is that of the slowest link between client and server (HPBN p.28).
- Global average measured by Akamai in Q1 2013: 3.1 Mbps; South Korea 14.2 Mbps; United States 8.6 Mbps (HPBN p.28) [DATED].
- Increasing bandwidth is feasible (more fibers, more links, better WDM); reducing latency runs into physics. Hence the book's recipe is to reduce round trips, move data closer to the client, and hide latency with caching and prefetch (HPBN p.29, p.30).
- A CDN reduces propagation time by serving content from nearby; it does not make the packet travel faster, it shortens the distance (HPBN p.25).

### Latency, not bandwidth, is the web's bottleneck
- The book states that latency is the bottleneck for most sites and refers to "More Bandwidth Doesn't Matter (Much)" (HPBN p.27).
- Mike Belshe's study cited in ch. 10: going from 1 to 2 Mbps cuts load time almost in half, but above 5 Mbps the gains are single-digit percentages, and from 5 to 10 Mbps it is only ~5% (HPBN p.195).
- In the same study, every 20 ms less latency gives a linear gain in load time (HPBN p.196).
- Reason: HTTP flows are short and bursty, while TCP is optimized for long-lived connections and bulk transfer; RTT limits throughput in most cases (HPBN p.196).

---

## 2. TCP (ch. 2)

### What TCP delivers and what it costs
- IP does host-to-host addressing and routing; TCP creates the abstraction of a reliable network over an unreliable channel: retransmission, in-order delivery, congestion control, integrity (HPBN p.31). That is why it is optimized for correct delivery, not for fast delivery (HPBN p.31).
- HTTP does not require TCP, but in practice all HTTP traffic of the time runs over TCP (HPBN p.31, p.32). Understanding TCP is necessary because the application's decisions determine its performance (HPBN p.32).

### Three-way handshake (cost: 1 RTT)
- Steps: the client sends SYN with random sequence number x; the server replies SYN-ACK with x+1 and its own random y; the client sends ACK with x and y incremented (HPBN p.32).
- The client can send data right after the ACK; the server can only send data after receiving that ACK. So every new connection pays a full round trip before any application data (HPBN p.33).
- Book example: client in New York, server in London, fiber: a minimum of 56 ms for the handshake alone; bandwidth has no influence (HPBN p.33).
- Consequence: new connections are expensive and connection reuse is a critical optimization (HPBN p.33).

### TCP Fast Open (TFO) [DATED]
- Allows sending data already in the SYN. Google studies cited: 15% drop in HTTP transaction latency, more than 10% in page load time on average and up to 40% in high-latency scenarios (HPBN p.34).
- Client and server support in Linux 3.7+ kernels (HPBN p.34).
- Limits: there is a cap on the payload size inside the SYN; only certain types of HTTP request can be sent; it works only on repeat connections, because it requires a cryptographic cookie (HPBN p.34).
- The book treats it as a new optimization that requires support on both sides and asks you to evaluate whether the application can use it (HPBN p.51). Its reference is an IETF draft, not an RFC (HPBN p.34).

### Congestion collapse and the motivation for the controls
- In 1984 John Nagle described congestion collapse (RFC 896) (HPBN p.34, p.35); in 1986, with more than 5,000 nodes, real incidents cut capacity by up to a factor of 1,000 (HPBN p.35).
- Response: flow control, congestion control and congestion avoidance. In 1988 Van Jacobson and Karels documented slow-start, congestion avoidance, fast retransmit and fast recovery (HPBN p.37).

### Flow control and rwnd
- Each side advertises its receive window (rwnd) in every ACK; the initial size comes from the system default. Zero window means "stop sending until the application drains the buffer" (HPBN p.35).
- In a typical web page the main flow is server→client, so the client's window tends to be the limit; in uploads, the server's (HPBN p.35).
- **Window scaling (RFC 1323)**: the original 16-bit field limits rwnd to 65,535 bytes; the option, negotiated in the handshake, applies a bit shift and raises the ceiling to 1 GB (HPBN p.36).
- Intermediaries (routers, firewalls) can rewrite or strip this option; if the connection does not use the available bandwidth, the first place to look is the interaction between window sizes. Linux: `sysctl net.ipv4.tcp_window_scaling` (check) and `sysctl -w net.ipv4.tcp_window_scaling=1` (enable) (HPBN p.36, p.37).

### Slow-start and cwnd
- Flow control protects the receiver, but nothing protected the network; neither sender nor receiver knows the available bandwidth at the start, so it must be estimated by measuring (HPBN p.37).
- The server keeps, per connection, a private variable `cwnd` (neither advertised nor exchanged), initialized with a conservative value (`initcwnd` on Linux) (HPBN p.37).
- Central rule: the maximum amount of unacknowledged data in flight is the minimum of rwnd and cwnd (HPBN p.38).
- Initial cwnd value: 1 segment originally; RFC 2581 (April 1999) raised it to up to 4; RFC 6928 (April 2013) raised it to 10 (HPBN p.38) [DATED].
- Growth: for each ACK received, cwnd grows by 1 segment, which is equivalent to doubling per round trip (exponential growth) (HPBN p.38).
- Book Equation 2-1: time to reach a window of N segments = RTT × log2(N / initial cwnd) (HPBN p.39).
- Book's numeric example (rwnd 65,535 bytes, initial cwnd 4, RTT 56 ms): 65,535/1,460 ≈ 45 segments; 56 ms × log2(45/4) = 224 ms, four round trips just to reach 64 KB (HPBN p.39). The link's Mbps capacity does not change this.
- How to shorten it: reduce the RTT (closer server) or raise the initial cwnd to 10 (HPBN p.40).
- For long downloads, the cost of slow-start is diluted; for short, bursty HTTP transfers, the connection often ends before reaching the maximum window, and RTT becomes the performance limit (HPBN p.40).

### Slow-start restart (SSR)
- After an idle period TCP resets cwnd to a safe default. This hurts long-lived connections that sit idle between bursts, such as HTTP keepalive; the book recommends disabling it on the server (HPBN p.41).
- Linux: `sysctl net.ipv4.tcp_slow_start_after_idle` (check) and `sysctl -w net.ipv4.tcp_slow_start_after_idle=0` (disable) (HPBN p.41).

### Full example: 20 KB on a new vs. reused connection
Parameters (HPBN p.41): RTT 56 ms; bandwidth 5 Mbps on both sides; rwnd 65,535 bytes; initial cwnd 4 segments (4 × 1,460 ≈ 5.7 KB); 40 ms of server processing; no loss; the GET fits in one segment.

| Time | Event (HPBN p.42–43) |
|---|---|
| 0 ms | Client sends SYN |
| 28 ms | Server replies SYN-ACK |
| 56 ms | Client sends ACK and already sends the GET |
| 84 ms | Server receives the request |
| 124 ms | Response ready; sends 4 segments and stops |
| 152 ms | Client receives and acknowledges 4 |
| 180 ms | Server sends 8 |
| 208 ms | Client acknowledges 8 |
| 236 ms | Server sends the rest |
| 264 ms | Client receives everything: **264 ms total** |

- On the already-open connection, the same request takes 96 ms (request, 28 ms; response ready at 68 ms; all 15 segments at once; arrival at 96 ms), a 275% improvement (HPBN p.43, p.44).
- Redoing the calculation with initial cwnd 10, one whole round trip disappears, a 22% improvement (HPBN p.43).
- The difference between first and second request only grows with a larger RTT; the 5 Mbps bandwidth played no role (HPBN p.44). This is the justification for keepalive, pipelining and multiplexing.

### Increasing the initial cwnd to 10 (IW10) [DATED]
- One of the simplest ways to improve all applications over TCP. On Linux it is the default in all kernels **above** 2.6.39 (HPBN p.44); the book recommends upgrading to 3.2+ for other gains, among them PRR, which is the default congestion avoidance algorithm from 3.2 on (HPBN p.44, p.45).

### Congestion avoidance and PRR
- TCP uses packet loss as a feedback signal: it is not a question of whether there will be loss, but when. Slow-start doubles every RTT until it hits the flow window, the `ssthresh` threshold or a loss; then congestion avoidance takes over (HPBN p.44).
- Implicit assumption: loss indicates congestion. The sawtooth throughput graph is the window adjustment at each loss (HPBN p.45).
- Variants cited: Tahoe, Reno, Vegas, New Reno, BIC, CUBIC (default on Linux), Compound TCP (default on Windows); the core implications hold for all of them (HPBN p.45) [DATED].
- Original AIMD: on packet loss, halve the window and then grow by a fixed amount per RTT (HPBN p.45).
- PRR (Proportional Rate Reduction, RFC 6937): recovers faster from losses; Google measurements show a 3–10% reduction in average latency of connections with loss; default on Linux 3.2+ (HPBN p.45) [DATED].
- Packet loss is necessary to TCP: it is the feedback that adjusts the rate and avoids bufferbloat (HPBN p.49).

### Bandwidth-delay product (BDP)
- Definition: link capacity × end-to-end delay; it is the maximum amount of unacknowledged data that can be in flight (HPBN p.46). If rwnd/cwnd are smaller than this, gaps appear in the flow and throughput drops, regardless of the advertised bandwidth (HPBN p.46).
- Book example 1: a minimum window (cwnd, rwnd) of 16 KB and an RTT of 100 ms give 131,072 bits / 0.1 s = 1.31 Mbps ceiling (HPBN p.47).
- Example 2: to saturate 10 Mbps with an RTT of 100 ms, the window must be at least 122.1 KB, above the 64 KB of rwnd without window scaling (HPBN p.47).
- Causes of use below the available bandwidth: a saturated peer advertising a low rwnd, losses that reset cwnd, or explicit traffic shaping (HPBN p.47).
- BDP also matters on a LAN: 1 Gbit/s with an RTT of 1 ms requires a cwnd of at least 122 KB (HPBN p.48).

### Head-of-line blocking in TCP
- Each packet carries a sequence number and data is delivered in order. When a packet is lost, the following ones are held in the receiver's TCP buffer until the retransmission arrives; the application sees none of this and merely notices a delay in reading the socket (HPBN p.48).
- Advantage: the application does not deal with reordering and reassembly. Cost: unpredictable variation in arrival time (jitter) (HPBN p.48).
- Applications that tolerate loss or disorder and are sensitive to latency/jitter are better off with UDP: audio, video and game state (HPBN p.49, p.50). See [udp-e-protocolos-de-transporte-alternativos.md](udp-e-protocolos-de-transporte-alternativos.md).
- In HTTP/2, the loss of one TCP packet still blocks all streams of the single connection; the book acknowledges the limitation and nonetheless keeps one connection per origin as the best strategy (HPBN p.236). Details in [http2-binary-framing-multiplexing-e-streams.md](http2-binary-framing-multiplexing-e-streams.md).

---

## 3. TCP optimization recipe

Principles the book restates (HPBN p.50): the handshake costs a full round trip; slow-start applies to every new connection; flow and congestion control regulate all throughput; throughput depends on the current cwnd. Result: RTT often limits the rate, and latency, not bandwidth, is the bottleneck.

**Server configuration** (HPBN p.50, p.51):
1. Upgrade the kernel to the latest version (the best single bet; on Linux, 3.2+ in the checklist of HPBN p.52).
2. Initial cwnd at 10 segments.
3. Disable slow-start after idle.
4. Keep window scaling enabled.
5. Evaluate TFO, if both sides support it.
6. Tool: `ss --options --extended --memory --processes --info` shows statistics of open sockets on Linux (HPBN p.51).

**Application behavior** (HPBN p.52):
- No bit is faster than the one not sent: eliminate unnecessary resources and compress.
- Bring the bits closer to the client (CDN, geo-distribution).
- Reuse TCP connections to avoid the repeated cost of slow-start.

**Book checklist** (HPBN p.52): updated kernel; cwnd = 10; no slow-start after idle; window scaling enabled; eliminate redundant transfer; compress data; servers close to the user; reuse established connections.

---

## After the book [extrapolation]
- TFO was later standardized as RFC 7413; its real-world use remained limited by middleboxes.
- IW10 became common practice; CUBIC and, later, BBR (congestion control based on a bandwidth and RTT model, not on loss) changed the congestion landscape.
- The 16-bit receive window + scaling (RFC 1323) was revised in RFC 7323.
- TCP's HOL blocking motivated QUIC/HTTP/3, which multiplexes streams over UDP (details outside the book).

---

## What the source does not cover
- BBR, HTTP/3/QUIC, ECN and modern congestion control in detail; the book only names variants up to CUBIC/Compound.
- SACK, delayed ACKs and fast retransmit are only mentioned in passing (HPBN p.50), without mechanics.
- Final TFO (RFC 7413) and its adoption history.
- Post-2013 measurements of bandwidth, last-mile latency and IPv6 adoption.
- The argument "resources under ~14 KB fit in one RTT" is a derivation of 10 × 1,460 bytes; the book does not state it in terms of a web page. What it shows is the calculation with cwnd 4 and the saving of one round trip with cwnd 10 (HPBN p.43).
