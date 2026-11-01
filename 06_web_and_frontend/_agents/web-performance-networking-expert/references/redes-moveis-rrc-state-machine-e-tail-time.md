# Wireless networks, WiFi, mobile networks, RRC and energy tail

Single source: *High Performance Browser Networking* (HPBN), Ilya Grigorik, O'Reilly, 1st ed., 2013. All cited pages are **PDF pages** (printed = PDF − 18). Scope: ch. 5 (PDF p.97), ch. 6 WiFi (p.107), ch. 7 mobile networks (p.117–155) and ch. 8 optimizing for mobile networks (p.157–169). Everything the book presented as future or recent in 2013 is marked **[DATED]**. Content that postdates the book appears only in the last section, with no page.

---

## 1. Wireless fundamentals (ch. 5)

- There is no such thing as a "wired application": every app must do well on any network, and every optimization made for wireless networks also improves the other contexts (HPBN p.98).
- Classification by range: PAN (Bluetooth, ZigBee, NFC), LAN (802.11), MAN (WiMAX) and WAN (cellular: UMTS, LTE) (HPBN p.98). A single app can use several at the same time (NFC to pay, Bluetooth for P2P via WebRTC, WiFi for HD streaming); you do not bet on just one (HPBN p.99).
- Maximum capacity of a channel, by Shannon's formula: C = BW × log2(1 + S/N). Only two factors limit the rate: available bandwidth and signal-to-noise ratio (HPBN p.99).
- The medium is shared and the spectrum is allocated by governments (in the US, the FCC). The rate is proportional to the bandwidth: going from 20 to 40 MHz can double the rate, which is how 802.11n beats its predecessors (HPBN p.100).
- Low frequencies reach farther (macrocells), but require larger antennas and have more clients competing. High frequencies carry more data and cover less (microcells), requiring more infrastructure (HPBN p.100).
- ISM bands of 2.4–2.5 GHz (100 MHz) and 5.725–5.875 GHz (150 MHz) are "unlicensed" and underpin WiFi. The 2008 700 MHz auction in the US raised US$ 19.592 billion (HPBN p.102).
- To reach the desired rate in the presence of interference, you increase transmission power, decrease distance, or both (HPBN p.103).
- Near-far effect: a strong signal "drowns out" a weak one. Cell-breathing: the coverage area shrinks and expands according to accumulated noise and interference (HPBN p.104).
- Modulation: what matters is alphabet × symbol rate. Book example: 1,000 symbols/s with 2 bits per symbol gives 2,000 bit/s. Higher-order alphabets pay with lower noise robustness (HPBN p.104–105).
- Advertised rates hold for "ideal conditions" (maximum bandwidth, exclusive spectrum, no noise, best modulation, MIMO). The book cites 54 Mbit/s for 802.11g, 600 Mbit/s for 802.11n and over 100 Mbit/s advertised for LTE (HPBN p.105–106).
- Moving the receiver by a few centimeters can double the throughput, and moments later another client waking up can cut it in half; wireless performance is highly variable (HPBN p.106).
- Wireless latency depends on the specific technology, which is why the book treats it in the following chapters (HPBN p.106).

---

## 2. WiFi (ch. 6)

### 2.1 How WiFi accesses the medium
- 802.11 was born as an adaptation of Ethernet (802.3); the 1999 802.11b is what popularized it. WiFi operates in unlicensed ISM (HPBN p.107).
- Ethernet, ALOHAnet and WiFi treat the medium as a random-access channel: there is no central scheduler, each device decides on its own (HPBN p.108).
- Ethernet uses CSMA ("listen before talking"), with collision detection and exponential backoff. WiFi cannot detect a collision while transmitting (a radio limitation), so it uses CSMA/CA: it transmits only when the channel is idle, sends the whole frame and waits for an explicit acknowledgment (HPBN p.108).
- The probabilistic model works well with a lightly loaded network. For good channel utilization, the load must stay below 10%; above that, collisions rise quickly and performance becomes unstable (HPBN p.109).

### 2.2 Standards and numbers
- Table 6-1 of the book (HPBN p.109): 802.11b (1999, 2.4 GHz, 20 MHz, 1 to 11 Mbit/s per stream); g (2003, 2.4 GHz, 20 MHz, up to 54); n (2009, 2.4 GHz/20 MHz, up to 72.2; or 5 GHz/40 MHz, up to 150); ac (~2014, 5 GHz, 20 to 160 MHz, up to 866.7 per stream).
- b and g were the most widespread: 20 MHz, a single radio stream, typical power limited to 200 mW by regulation (HPBN p.109).
- n and ac double the bandwidth from 20 to 40 MHz, use higher-order modulation and multiple radios (MIMO) (HPBN p.109–110). **[DATED]** 802.11ac is described as "future", with the promise of more than 1 Gbit/s under ideal conditions (HPBN p.110).
- Before 802.11n, there was only one frame in flight at a time, with a link-layer ACK. 802.11n introduced frame aggregation (HPBN p.113).

### 2.3 Measuring and understanding performance
- There is no throughput or latency guarantee for any client. WMM (basic QoS extension) was poorly supported in routers and clients **[DATED]** (HPBN p.110).
- It is common to find dozens of overlapping WiFi networks in dense urban environments (HPBN p.110).
- The 2.4 GHz band has only three non-overlapping 20 MHz channels: 1, 6 and 11. With more than two or three neighboring networks, some necessarily compete for the same channel (HPBN p.111).
- If the neighbor on the same channel starts watching HD video, your bandwidth can drop by half or worse; the access point has no say in this contention (HPBN p.111).
- The 5 GHz band has much more spectrum and less interference, and a dual-band router serves old (2.4 GHz) and new (5 GHz) clients (HPBN p.111).
- The author's measurement, ping to the gateway with a dual-band 802.11n router less than 6 m away (Table 6-2, HPBN p.112):

| Band | Median | p95 | p99 |
|---|---|---|---|
| 2.4 GHz | 6.22 ms | 34.87 ms | 58.91 ms |
| 5 GHz | 0.90 ms | 1.58 ms | 7.89 ms |

- Summary from the book: no bandwidth/latency guarantee, bandwidth varies with SNR, power limited to 200 mW (or less), limited spectrum and access points overlap by design. There is no "typical performance" of WiFi (HPBN p.112).
- WiFi collisions rarely turn into visible TCP loss: retransmission and error correction stay in the link and physical layers. The effect shows up as greater variability in packet arrival times (HPBN p.112–113).

### 2.4 Optimizing for WiFi
- WiFi is generally an extension of a LAN connected to a WAN with no data cap. With averages of 8.6 Mbps at the edge and 3.1 Mbps globally (Table 1-2 of the book), the bottleneck is normally the WAN, not WiFi (HPBN p.113).
- Large downloads, updates and streaming should go over WiFi when possible; it is worth asking the user to switch networks. Carriers recommend "Wi-Fi offloading" for data-intensive apps (HPBN p.113–114). Exception: WiFi that is 3G/4G tethering is limited (HPBN p.113).
- Bandwidth can change from second to second through small changes in position and neighbor activity. The rate measured at the start of a video should not be extrapolated; you should adapt continuously (HPBN p.114).
- Reference H.264 video bitrates (Table 6-3, HPBN p.114): 360p 0.5 Mbit/s; 480p 1–1.5; 720p 2–2.9; 1080p 3–4.3.
- Adaptive streaming (ABR): the resource is encoded at several bitrates and segmented into chunks of 5 to 10 s (YouTube example); the client or server measures the rate of each segment and chooses the bitrate of the next. You start with a low bitrate to begin quickly. The book cites Netflix with more than 120 versions per stream (HPBN p.115).
- First-hop WiFi latency: under ideal conditions, below 1 ms. In dense environments, a median of 1–10 ms, occasionally 10–50 ms and, in the worst case, hundreds of ms. For latency-sensitive apps the book mentions WebRTC with unreliable UDP transport as an alternative (HPBN p.115).
- WiFi power saving: the access point emits DTIM in periodic beacons; the client sleeps between them. It reduces battery use and adds latency (HPBN p.132).

---

## 3. Cellular generations and standards (ch. 7, first half)

### 3.1 What to expect from each generation
- Peak (Table 7-1, HPBN p.118): 1G no data (analog); 2G in Kbit/s; 3G in Mbit/s; 4G in Gbit/s, packets only. "Peak" rates hold for ideal conditions; to calibrate expectations, assume the lower bound of throughput and the upper bound of latency (HPBN p.118).
- Table 7-2 (active connection, HPBN p.118), typical throughput and latency ranges by generation:
  - 2G: from 100 to 400 Kbit/s, with latency between 300 and 1000 ms.
  - 3G: from 0.5 to 5 Mbit/s, with latency between 100 and 500 ms.
  - 4G: from 1 to 50 Mbit/s, with latency below 100 ms.
- The 3G/4G classification is too coarse, and real performance varies by carrier, configuration, number of users in the cell, environment and device (HPBN p.118).

### 3.2 History that matters
- 1G in Japan in 1979. 2G (GSM) in Finland in 1991, with peak data of 9.6 Kbit/s (HPBN p.118). GPRS reached 172 Kbit/s with RTT in the hundreds of ms; EDGE (2.75G) reached 384 Kbit/s and debuted in the US in 2003 (HPBN p.119).
- Two non-interoperable families: 3GPP (GSM → UMTS → HSPA/HSPA+ → LTE; device with SIM) and 3GPP2 (IS-95 → CDMA2000 → EV-DO). GSM covered 80–85% of the market and IS-95 10–15% (HPBN p.119–121).
- 3GPP releases (Table 7-4, HPBN p.122): R99 (1999) UMTS; R4 (2001) all-IP core; R5 (2002) HSDPA; R6 (2004) HSUPA; R7 (2007) HSPA+; R8 (2008) LTE/SAE; R9 (2009); R10 (2010) LTE-Advanced.
- HSDPA + HSUPA = HSPA (3.5G), with a low single digit of Mbit/s in the real world. HSPA+ (3.75G) brought much lower latency, thanks to the simplified core architecture, and mid-to-high single-digit Mbit/s (HPBN p.122).
- EV-DO (Table 7-5, HPBN p.122): Rel. 0 (1999); Rev. A (2001) improves uplink, latency and QoS; Rev. B (2004) multicarrier; Rev. C/Advanced (2007). 3GPP2 has no competing official 4G standard, and CDMA carriers converged on LTE (HPBN p.123).
- "Broadband" is a relative term; for the book, 3G is what crosses the Mbit/s barrier (HPBN p.123).

### 3.3 4G, LTE and HSPA+
- 4G is a set of requirements (IMT-Advanced, ITU, 2008), not a technology: IP packet base, interoperable with 2G/3G, 100 Mbit/s on the move and Gbit/s+ stationary, control-plane latency < 100 ms and user-plane latency < 10 ms, variable bandwidth from 5 to 20 MHz (HPBN p.123–124).
- LTE (release 8) is technically a transitional 3.9G; LTE-Advanced (release 10) is the first 3GPP standard to meet IMT-Advanced. Carriers redefined the "4G" label and apply it to LTE and most of HSPA+; you have to read the fine print (HPBN p.124).
- LTE goals (HPBN p.124–125): all-IP core, simplified architecture, latency < 10 ms in the user plane and < 100 ms in the control plane, 100 Mbps, larger allocations with carrier aggregation, mandatory MIMO.
- LTE requires a parallel network and spectrum separate from 3G, but allows handoff to 3G and back. An LTE device has 3 to 4 radios (5–6 with 4x MIMO) (HPBN p.125).
- HSPA+ kept evolving (release 10 meets several IMT-Advanced criteria) because it is a cheap incremental migration, unlike LTE, which requires a new radio network. The book projected HSPA+ dominating the decade and took about a decade from specification to mass availability (HPBN p.125–127). **[DATED]** adoption forecasts through 2016 (HPBN p.126).
- Old networks will keep operating for at least another decade (relative to 2013); plan for multiple generations. **[DATED]** VoLTE still "in development": most 4G used circuit-switched for voice (HPBN p.127).
- The app must adapt to continuous changes in throughput, latency and even radio availability, because the user in transit alternates between LTE, HSPA+, HSPA, EV-DO and EDGE (HPBN p.128).
- Table 7-6 (HPBN p.128):

| | HSPA+ | LTE | LTE-Advanced |
|---|---|---|---|
| Peak downlink (Mbit/s) | 168 | 300 | 3,000 |
| Peak uplink (Mbit/s) | 22 | 75 | 1,500 |
| Max. MIMO streams | 2 | 4 | 8 |
| Idle → connected (ms) | < 100 | < 100 | < 50 |
| Dormant → active (ms) | < 50 | < 50 | < 10 |
| User-plane latency, one way (ms) | < 10 | < 5 | < 5 |

- HSPA+ and LTE are equivalent in practice: mid-to-high single-digit Mbps and under 100 ms, comparable to home WiFi, but you cannot treat them as an "always on" environment (HPBN p.128).

### 3.4 Device categories
- Throughput requires the device to match the network: the HSPA standard defines more than 36 UE categories; for 42.2 Mbps, category 20 (2x MIMO) or 24 (dual-cell) is required (HPBN p.129–130, Table 7-7). The Nexus 4 is category 24 (HPBN p.131).
- LTE (Table 7-8, HPBN p.130): category 1 = 10.3 Mbit/s downlink; 3 = 102; 4 = 150.8; 5 = 299.6 (4x MIMO); 8 = 2998.6. High-end smartphones sit in categories 3–5; initial deployments targeted categories 1–3 (HPBN p.130).

---

## 4. The RRC (Radio Resource Controller)

**Summary for "the first request after idle is slow"** (use all the items; details below):
- Who decides: the RRC controls who transmits, when, at what power and in what energy state (HPBN p.131, p.133). In LTE it sits at the tower (eNodeB); in 2G/3G it sat in the carrier's core (HPBN p.133, p.146).
- LTE states: Idle < 15 mW, no radio resources; Connected 1,000–3,500 mW (HPBN p.135).
- Transition targets: Idle→Connected < 100 ms (LTE-Advanced < 50 ms); from DRX to Connected < 50 ms (LTE-Advanced < 10 ms) (HPBN p.135, p.136, p.137).
- The return to lower-energy states is by network timers, because the RRC does not know when the transfer ended; the carrier tunes the parameters (HPBN p.134, p.135).
- HSPA/HSPA+: Idle→DCH up to 2 s; FACH→DCH up to 1.5 s (HPBN p.138).
- An idle radio does not drop TCP/UDP: connections stay at the carrier and the device is notified (paging) when data arrives (HPBN p.144, p.151). Carrier NAT: 5–30 min; a keepalive of ~5 min is enough (HPBN p.162).
- Rule of thumb for the control-plane cost: add ~100 ms (4G), 150–500 ms (3.5G+) or 500–2,500 ms (3G) (HPBN p.164).

### 4.1 Why it exists
- The RRC does all the connection management between the device and the base station and affects latency, throughput and battery (HPBN p.131). In 2G/3G it lived in the carrier's core; in 4G it was moved to the tower (eNodeB) to reduce coordination latency (HPBN p.133).
- It decides who talks when, allocated bandwidth, signal power and the energy state of each device. To transmit, the device must request resources from the RRC; for incoming data, the RRC tells it when to listen (HPBN p.133).
- There is no API to control the RRC; the app must know its constraints and work within them (HPBN p.133).

### 4.2 Energy: numbers from the book
- The radio is the second-largest consumer in the device, behind the active screen; keeping it always active would drain the battery in hours (HPBN p.133).
- WiFi: each device sets its power, typically 30–200 mW. 3G/4G radio: can sit at ~15 mW idle, but requires 1,000–3,500 mW when transmitting at high power (HPBN p.133).
- For large transfers with good signal WiFi tends to be much more efficient; for a mostly idle device, the cellular radio is better. There was no mechanism for dynamic switching between the two (HPBN p.134).
- Turning off the radio drops the radio context; resuming it requires exchanging control messages that add up to tens or hundreds of ms (HPBN p.134).

### 4.3 LTE state machine
- The machine is defined by 3GPP and is the same across LTE; the carrier only tunes the trigger parameters (HPBN p.134).
- **RRC Idle**: low power (< 15 mW), listens only to the control channel, no resources assigned. **RRC Connected**: high power (1,000–3,500 mW), with dedicated resources (HPBN p.135).
- In Idle the device neither sends nor receives data; it synchronizes, asks the RRC for promotion and the negotiation takes several round trips. The LTE target is ≤ 100 ms; in LTE-Advanced, 50 ms (HPBN p.135).
- The RRC does not know when the transfer ended (IP traffic is bursty, optimized TCP is long-lived and UDP has no end); so it depends on timers to step the state down (HPBN p.135).
- Substates of Connected (HPBN p.135–136): Continuous Reception (highest power, resources allocated), Short DRX and Long DRX (context kept, no resources allocated, the device wakes up to listen to periodic broadcasts). Long DRX only sleeps for longer periods than Short DRX. This resembles the DTIM of WiFi.
- Resuming from DRX ("dormant to connected") is < 50 ms in LTE and < 10 ms in LTE-Advanced. The book's conclusion: a negotiation of 10 to 100 ms may occur before any data (HPBN p.136).
- Table 7-9 (HPBN p.137): idle → connected < 100 ms (LTE) and < 50 ms (LTE-A); DRX → connected < 50 ms and < 10 ms; user plane one way < 5 ms in both.

### 4.4 HSPA / HSPA+ (UMTS)
- States (HPBN p.137–138): **Idle**; **Cell DCH** (high power, resources for up and down); **Cell FACH** (intermediate, low-speed shared channel, typically < 20 Kbps, consumes about half the power of DCH, intended for non-interactive traffic such as polling and status checks).
- DCH → FACH is by timer. In FACH, the device stays there as long as the send buffer does not exceed a threshold configured by the network, typically 100 to 1,000 bytes; if there is no data for a period, another timer takes it to Idle (HPBN p.138).
- Transition latencies: Idle → DCH can take up to 2 s and dozens of control messages; FACH → DCH up to 1.5 s. Recent HSPA+ networks improved and compete with LTE. The app should plan for delays of several seconds on old 3G (HPBN p.138).
- Despite finer control, LTE radios consume more energy than 3G ones; the LTE power profile is higher (HPBN p.138).

### 4.5 EV-DO (CDMA)
- Only two states, Idle and Connected, the simplest of the three. Every transfer requires promotion to Connected, with latency of hundreds to thousands of ms depending on the revision; return to Idle by carrier timeouts (HPBN p.139).

---

## 5. Energy tail and the cost of periodic transfers

- Every send, however small, promotes the radio to high power, and it only comes back when the inactivity timer expires; the size of the transfer does not change the timer, and there may be passage through intermediate states before Idle (HPBN p.140). The book calls this cost "energy tail" (HPBN p.140).
- Book example (HSPA+, DCH → FACH after 10 s of inactivity): an analytics beacon every 11 s leaves the device spending a few hundred ms on the transfer, then idle at high power, and the radio barely steps down before being woken again. It is the worst case for latency and battery (HPBN p.140).
- Each cycle pays: the latency cost of promotion, the transfer and the tail with the radio idle until the timers fire (HPBN p.140).
- **Pandora case (AT&T Labs, "Profiling Resource Usage for Mobile Applications")** (HPBN p.141): the music is downloaded all at once (correct), but audience-measurement pings every 60 s accounted for **0.2% of the bytes** and **46% of the app's energy consumption**. Grouping the data into fewer requests, or sending it with the radio already active, would nearly double energy efficiency.
- Application: a device idle for more than a few seconds should be treated as being in a low state; when you trigger a transfer, there will be a promotion cost (HPBN p.164).

---

## 6. End-to-end carrier architecture (LTE)

- Choice of LTE as the example: it is the most likely architecture in new deployments and the simplest (HPBN p.141).
- **RAN**: the eNodeB hosts the RRC, maintains the state machine and assigns resources to each user in the cell. Handoff between towers takes hundreds of ms in LTE (a light pause at the physical layer, transparent to the application) and can take several seconds in earlier generations (HPBN p.142).
- **Tracking area**: logical group of towers. The core normally knows only the area, not the tower. Movements within the same area, with the device in Idle, do not generate notifications, which saves energy (HPBN p.143).
- **Core (EPC)** (HPBN p.143–145): PGW (exit point to the Internet, allocates and maintains the device's IP, applies policies together with the PCRF), SGW (mobility anchor) and MME (user database: location, authentication, billing, services). Control uses SCTP; data uses GTP over UDP (HPBN p.143–144).
- The PGW can act as NAT, and dozens or hundreds of devices may share the same public IP; the same client may appear with different IPs. The book records low IPv6 adoption at the time **[DATED]** (HPBN p.144).
- **Radio state is not connection state**: dropping the radio context does not affect TCP/UDP sessions, maintained by the PGW. The device may have an idle radio and live connections; when data arrives, the radio is re-established and communication proceeds with the RRC as the only cost (HPBN p.144).
- In LTE the RRC is at the tower; previously it sat higher in the network, which imposed latency and a bottleneck on all control traffic (HPBN p.146).
- The backhaul can be the real bottleneck: a tower can serve up to three cells and hundreds of active users, and with 10+ Mbps per user it needs dedicated fiber. Connecting on 4G does not guarantee the radio's maximum throughput (HPBN p.146–147).

---

## 7. Packet flow and latency in a mobile network

### 7.1 Device-initiated request (HPBN p.147–149)
- With the radio in Idle, it is necessary to synchronize with the tower and request a new context: several round trips, up to 100 ms on 4G; in generations where the RRC sits at the gateway, up to several seconds (HPBN p.147).
- After that, each packet pays only user-plane latency (up to 5 ms on 4G) while the radio stays at high power (HPBN p.147).
- From the eNodeB to the Internet it passes through the SGW and PGW, with no latency guarantee. On deployed 4G, end-to-end latency with the device already connected tends to 30–100 ms; with ≤ 5 ms on the first hop, 25–95 ms of transit remain in the core (HPBN p.148).
- If the device went to DRX, the negotiation drops to up to 50 ms (HPBN p.149).
- Four latency components per new request (HPBN p.149): control plane (< 100 ms from Idle, < 50 ms from dormant), user plane (< 5 ms per packet), carrier core (in practice 30–100 ms) and Internet routing (variable). Only the last can be influenced by the developer, by bringing servers closer to the user.
- Jitter becomes more predictable when you consider the control cost of the first packet: up to 100 ms in LTE, 50 ms in LTE-Advanced, seconds in earlier generations (HPBN p.149).
- Core latency declared by AT&T (Table 7-10, HPBN p.150): LTE 40–50 ms; HSPA+ 100–200 ms; HSPA 150–400 ms; EDGE and GPRS 600–750 ms. The book's comparison: going around the Earth at the equator (24,901 miles) takes light 133.7 ms (HPBN p.150).

### 7.2 Incoming data with an idle device (HPBN p.150–151)
- The PGW still holds the connection. It routes the packet to the SGW, which queries the MME. If the device is in Idle, the MME sends **paging** to all the towers of the tracking area, which broadcast it; the device wakes up periodically to listen and, if it is on the list, starts the negotiation. The tower informs the MME, and the packet is delivered (steps 1–7 of Figure 7-13) (HPBN p.151).
- Once connected, there is a direct tower-SGW tunnel, and the following packets skip paging (HPBN p.151). Packets are held at the PGW, SGW and eNodeB until they can be delivered, and the observable effect is jitter, with the first packet worse (HPBN p.151).

### 7.3 HetNets and real measurements
- HetNets: layers of small cells over macrocells. A macrocell can cover tens of square miles in rural areas, but only 50 to 300 m in dense urban zones; micro, pico and femtocells cover a building, floors and an apartment. Consequence for the dev: expect more handoffs and greater variation in latency and throughput **[DATED]** (HPBN p.151–152).
- Study by Univ. of Michigan with AT&T Labs (46 Measurement Lab nodes, ~3,300 users, two months of 2011): early LTE showed good throughput and more stable RTT and jitter than other standards, comparable to or better than 802.11g WiFi. One test does not prove a general rule (HPBN p.153–155).

---

## 8. Optimizing for mobile networks (ch. 8)

### 8.1 Principles
- Battery, device form and radio are linked; the best practices for each often collide and it is up to the app to balance them. Protocol optimizations (keepalive, servers near the client, TLS) matter even more on mobile (HPBN p.157).
- The rules of ch. 8 hold for native apps and for browser apps (HPBN p.158).
- Guiding question: how does this affect battery life? A radio at maximum power drains the battery in hours, power grows with each generation, it is the second consumer after the screen and the energy profile is not linear with data. So, transfer as much as possible with the radio on and minimize the number of additional transfers (HPBN p.158).
- WiFi and cellular have different latency, throughput and energy profiles, so the app's behavior can and should be different on each (HPBN p.158).
- **AT&T ARO** (Application Resource Optimizer, free): collector (Android) and analyzer. It shows radio states, energy and traffic patterns, and recommends fixes (missing compression, redundant transfers). The numbers are estimates from a model, not measurements from the device; the analyzer accepts tcpdump pcap, and iOS uses that route (HPBN p.159–160). **[DATED]** the specific tool.

### 8.2 Eliminate periodic and inefficient transfers
- There is a fixed energy cost to rise to the high-power state, regardless of volume: for the battery there is no such thing as a "small request" (HPBN p.160).
- Book rules (HPBN p.160): polling is very expensive, minimize it; use push where possible; aggregate outgoing and incoming requests; defer non-critical requests until the radio is active.
- High-frequency push can cost as much as or more than polling. Questions to ask: what is the best interval and does it match the user's expectation? Can an adaptive interval be used? Can calls be aggregated? Can they be deferred? (HPBN p.160).
- Native apps use the platform's push services; web apps use Server-Sent Events and WebSocket, avoiding polling and expensive XHR techniques. Grouping several notifications into one push event, by adaptive interval, user preference or battery level, improves the energy profile (HPBN p.160).
- Server-side aggregation resembles Nagle's algorithm at the application layer: batch by time, count or size. The most efficient version is to push only when the client's radio is already active (for example, waiting for the client to initiate a request) (HPBN p.161).
- **[DATED]** The book mentions Google Cloud Messaging (GCM) for Android and Chrome as a service that aggregates messages and delivers them when the device is active, and states that there was no equivalent cross-browser API; the W3C Push API was supposed to supply this "in the future" (HPBN p.161).
- Intermittent audience and analytics beacons can cancel out everything else: log and defer until the radio is active, piggyback on existing traffic and watch the network pattern of third-party libraries (HPBN p.161).
- Incremental loading and progressive enhancement also generate intermittent accesses and the latency cost of each RRC transition (hundreds to thousands of ms), especially bad for interactive traffic (HPBN p.161).

### 8.3 Energy budget of background updates (HPBN p.162)
- Book assumptions: 5 Wh battery = 18,000 J; cycling the radio from idle to connected and back costs 10 J; polling every 1 minute consumes 60 × 10 J = **600 J per hour**, about **3%** of the battery per hour, for a single app. A few apps with non-overlapping intervals drain the battery before midday.
- Update frequency and battery life are opposed: evaluate bundling, adaptive intervals, pull versus push and measure with ARO or a similar tool (HPBN p.162).

### 8.4 Application keepalives
- The TCP/UDP lifecycle is independent of the radio state: the radio can be at low power while the carrier maintains the connections; when a packet arrives, the network notifies the device and promotes the radio. The app does not need to keep the radio active so the connection does not drop (HPBN p.162).
- Unnecessary keepalives usually come from a misunderstanding about the radio. Most carriers use a NAT timeout of **5–30 minutes**; a periodic keepalive of ~5 minutes is enough. If you need a shorter interval, first review your server, proxy and load balancer (HPBN p.162).

### 8.5 Latency of a simple HTTP request (HPBN p.163)
- A request can have from hundreds to thousands of ms of overhead on mobile: control plane, DNS, TCP, TLS and HTTP. Best case: radio already at high power, DNS resolved and connection reusable.
- Assumptions: RTT of 100 ms on 4G and 200 ms on 3.5G+. Table 8-1:

| Component | 3G | 4G |
|---|---|---|
| Control plane | 200–2,500 ms | 50–100 ms |
| DNS | 200 ms | 100 ms |
| TCP | 200 ms | 100 ms |
| TLS | 200–400 ms | 100–200 ms |
| HTTP | 200 ms | 100 ms |
| Total | 200–3,500 ms | 100–600 ms |

- The book's conclusion: up to half a dozen round trips before the response bytes; seconds on 3G and about half a second on 4G (HPBN p.163). See also [tls-handshakes-resumption-e-alpn.md](tls-handshakes-resumption-e-alpn.md) and [fundamentos-tcp-e-gargalos-de-transporte.md](fundamentos-tcp-e-gargalos-de-transporte.md).

### 8.6 Rule of thumb for RRC transitions (HPBN p.164)
- Device idle for more than a few seconds: the first packet pays a one-time additional control-plane cost. Add **100 ms on 4G, 150–500 ms on 3.5G+ and 500–2,500 ms on 3G**.
- The book's synthesis (HPBN p.164): state machines differ by standard; they are managed by the network; promotions occur when there is data; demotions occur by timeouts; LTE transitions take 10 to 100 ms; HSPA+ is competitive with LTE; HSPA and CDMA can take several seconds; every transfer, of any size, generates an energy tail.
- RRC latency is frequently noticeable by users when ignored (HPBN p.164).

### 8.7 UI, failures and estimates
- Decouple user interaction and network communication: acknowledge the input within a few hundred ms, fire the request in the background and give immediate feedback. Control-plane latency alone already blows the feedback budget; you cannot "fix" core and RRC latency (HPBN p.164–165).
- Design for variable interface availability: the user alternates between 4G, 3G and 2G; the app should subscribe to these transitions. The book mentions `navigator.onLine` for monitoring the connection (HPBN p.165).
- Bandwidth and latency estimates are stable only for tens to hundreds of ms, at most about one second; do not cache them for future decisions. Even on 4G, moving the device a few centimeters can go from hundreds of Kbit/s to Mbit/s+ (HPBN p.165–166). The book cites the iPhone 4 "antennagate" case as an example (HPBN p.166).
- ABR still applies to long streams (adapted in blocks of a few seconds), but without reusing old estimates. If possible, use coarse information about the network generation instead of estimating end to end, something the book says to avoid on mobile because the estimate comes out wrong (HPBN p.166).
- Large download with certainty of use: download the whole file at once and let the radio idle (as in Pandora). If you cannot, use ABR (high battery cost) or ask the user to use WiFi (HPBN p.166).
- Treat loss of connectivity as the rule, not the exception (HPBN p.166–167): do not cache or guess the network state; fire the request, listen for failures and diagnose; use retry with a backoff algorithm, no infinite loop; if offline, log and send later; use localStorage and AppCache for offline mode. **[DATED]** AppCache (HPBN p.167). Handoffs will grow with HetNets, which makes monitoring even more important (HPBN p.167).

### 8.8 "Burst Your Data and Return to Idle" (HPBN p.167)
- The mobile radio interface is optimized for bursts: group the requests, download as much as possible as fast as possible and let the radio return to Idle. This gives better throughput and longer battery life.
- LTE and HSPA+ networks allocate resources in 1 ms intervals and prioritize bursty flows. The only accurate way to measure network speed is to use it.
- Corollary: progressive loading in small chunks can do more harm than good (more variability and energy cost). Anticipate what the user will need, download it ahead and let the radio idle: whole large audio/video files, app content via prefetch with statistical models, pre-loaded third-party content (ads), and elimination of intermittent transfers.

### 8.9 Prefetch model (HPBN p.168)
- There is tension between downloading few bytes and reducing latency, variability and battery impact. There are at least three variables in balance: bytes transferred, battery impact and throughput/latency variability.
- Apps with a predictable usage pattern can prefetch aggressively without much byte overhead; poorly done prefetch downloads a lot of useless data. Define goals and usage patterns, implement, collect metrics and iterate.

### 8.10 Offload to WiFi and protocols (HPBN p.168–169)
- Cited estimate: close to 90% of the world's wireless traffic originates in indoor environments, often within WiFi range. Cellular generally has a data cap; WiFi uses less battery on large transfers and dispenses with the RRC. Use WiFi when available and, in data-intensive apps, ask the user to enable it (HPBN p.168).
- TCP, UDP and TLS optimizations, reuse of keepalive connections and servers close to the client are worth double on mobile networks (HPBN p.169).

---

## 9. Practical decisions (derived from the book)

| Situation | Decision supported by the book |
|---|---|
| Periodic telemetry/analytics | Queue and send along with traffic already in progress; avoid a beacon every few seconds (HPBN p.140, 141, 161) |
| Frequent background update | Compute the cost: 1 min = 600 J/h, ~3% of battery; use aggregation or an adaptive interval (HPBN p.162) |
| Notification to the client | Platform push or SSE/WebSocket instead of polling; aggregate on the server (HPBN p.160–161) |
| Keeping a connection open | No need to keep the radio active; a keepalive of ~5 min covers the 5–30 min NAT (HPBN p.162) |
| First request after idle | Add 100 ms (4G), 150–500 ms (3.5G+), 500–2,500 ms (3G) (HPBN p.164) |
| User action that depends on the network | Immediate UI feedback and background request (HPBN p.164–165) |
| Large media that will be used in full | Download everything at once; otherwise, ABR or invite the user to use WiFi (HPBN p.166) |
| Bandwidth estimate | Do not reuse; use only the network generation as a coarse hint (HPBN p.165–166) |
| Network failures | Retry with backoff, offline queue, never cache network state (HPBN p.166–167) |
| Bulky data | Prefer WiFi, warn the user (HPBN p.113–114, 168) |

---

## 10. After the book [extrapolation]

No book page; check a current source before using.

- 5G and LTE-Advanced Pro brought new states and energy-saving mechanisms in the RRC (for example, an intermediate inactive state); timer values and latencies differ from the 2013 numbers.
- In modern apps, background push usually goes through APNs (iOS) and FCM (Android), the successor to GCM, with scheduling and batching controlled by the operating system.
- Service Workers, Background Sync and the Push API implemented in current browsers replace the role of AppCache and cover the offline mode and the push that the book describes as future.
- WiFi 6/6E/7 changed the scheduling and efficiency picture of WiFi relative to the 802.11n/ac discussed in ch. 6.

---

## 11. What the source does not cover

- Duration of inactivity timers in real networks: the book only gives illustrative examples (10 s DCH → FACH, 11 s beacon, Pandora's 60 s ping) and says they are set by the carrier. It does not state a typical "tail time" of 10–20 s.
- Names of RRC signaling messages (random-access preambles etc.) and protocol details of promotion; the book only says there are several round trips.
- Power per state beyond the numbers cited (Idle < 15 mW, Connected 1,000–3,500 mW, WiFi 30–200 mW, FACH ≈ half of DCH); it does not give FACH/DRX powers in mW.
- 5G, FCM/APNs, Service Workers, Background Sync, Network Information API, WiFi 6 and later.
- Recommended frequency for batch sending (for example, "every X minutes"): the book says to aggregate and defer, without fixing an interval.
- Code or platform APIs to detect the radio state; it only mentions `navigator.onLine`, ARO and tcpdump.
