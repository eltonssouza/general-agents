# Reference index: Web Performance & Networking Expert

## 1. Source

- **Title:** *High Performance Browser Networking: What every web developer should know about networking and web performance*
- **Author:** Ilya Grigorik
- **Publisher and edition:** O'Reilly Media, 1st edition, 2013 (acronym **HPBN**)
- **Size:** 401 pages in the PDF
- **File:** `06_web_and_frontend/Web-Performance-HPBN-Grigorik.pdf`
- **Thesis of the book:** latency, not bandwidth, is the bottleneck of most web applications; the way forward is to eliminate round trips, reuse connections and bring data closer to the client (HPBN p.27, 30, 195, 196).

Structure (PDF pages): Part I, networking (ch. 1 to 4, p.19–94); Part II, wireless networks (ch. 5 to 8, p.95–170); Part III, HTTP (ch. 9 to 13, p.171–268); Part IV, browser APIs (ch. 14 to 18, p.269–380); index (p.381–400).

---

## 2. Numbering notice

- **Always cite the PDF page** (`HPBN p.N`), never the printed one.
- Relationship: **printed page = PDF page − 18**. The PDF has a front and back cover (p.1 and p.2) and **16 roman-numeral pages** (p.3 to p.18, numbered i to xvi); printed page 1 is p.19 of the PDF (start of Part I).
- Example: chapter 1 starts on p.21 of the PDF, which is printed page 3.
- The page numbers the book itself writes in its internal cross-references ("see page 30") are printed ones; add 18 to find the PDF page.
- Prefer specific pages to ranges. Check with `python -I .agents/skills/pdf-para-agent-especialista/scripts/extrair_paginas.py 06_web_and_frontend/Web-Performance-HPBN-Grigorik.pdf --busca "termo"`.

---

## 3. Label conventions

| Label | Meaning |
| :--- | :--- |
| `[from source]` | It is on the cited PDF page. Without a page, this label is not used. |
| `[inference]` | Deduction or calculation made from numbers in the book (for example, applying the RTT model to values given by the user). |
| `[extrapolation]` | Content that postdates the book or that it does not cover (no page). Confirm in a current source. |
| `[DATED]` | The book presents it as new, draft or future in 2013 and that changed afterwards (with page). |

Writing rules for the references: own words; literal quotation only when short and in quotation marks; relative links only; "the source does not cover X" applies to the text of the book.

---

## 4. Map of the references

| File | Topic | PDF pages |
| :--- | :--- | :--- |
| [fundamentos-tcp-e-gargalos-de-transporte.md](fundamentos-tcp-e-gargalos-de-transporte.md) | Latency vs. bandwidth; physical limit; handshake, slow-start, cwnd, BDP, TCP HoL; TCP checklist | ch. 1 and 2: p.21–52; reinforcement on p.195, 196 |
| [udp-e-protocolos-de-transporte-alternativos.md](udp-e-protocolos-de-transporte-alternativos.md) | UDP, NAT, timeouts, STUN, TURN, ICE, RFC 5405 guidelines | ch. 3: p.53–63; DTLS on p.66 |
| [tls-handshakes-resumption-e-alpn.md](tls-handshakes-resumption-e-alpn.md) | TLS up to 1.2, handshake, resumption, ALPN, SNI, chain, OCSP, record, HSTS | ch. 4: p.65–93 |
| [redes-moveis-rrc-state-machine-e-tail-time.md](redes-moveis-rrc-state-machine-e-tail-time.md) | Wireless networks, WiFi, 3G/4G, RRC, energy tail, mobile optimization | ch. 5 to 8: p.97–169 |
| [http1x-keepalive-pipelining-e-sharding.md](http1x-keepalive-pipelining-e-sharding.md) | History of HTTP, keep-alive, pipelining, six connections, sharding, bundling, inlining | ch. 9: p.173–181; ch. 11: p.205–223; optimization order on p.259 |
| [critical-rendering-path-dom-cssom-e-layout.md](critical-rendering-path-dom-cssom-e-layout.md) | DOM/CSSOM/JS pipeline, waterfall, perception, measurement | ch. 10: p.183–203; p.221, 222, 258 |
| [otimizacoes-de-navegador-resource-hints-e-caching.md](otimizacoes-de-navegador-resource-hints-e-caching.md) | Speculative optimizations, hints, preload scanner, cache, bytes and images | p.201–203; p.253–258; p.271–275 |
| [http2-binary-framing-multiplexing-e-streams.md](http2-binary-framing-multiplexing-e-streams.md) | HTTP 2.0 (draft): SPDY, framing, streams, multiplexing, priority, flow control, Upgrade and migration | ch. 12: p.225–249; ch. 13: p.259–268 |
| [http2-hpack-prioritizacao-e-server-push.md](http2-hpack-prioritizacao-e-server-push.md) | HTTP 2.0 (draft): header tables, CRIME, server push, push vs. inlining | p.237–242; p.247; p.257; p.261, 265 |
| [websockets-full-duplex-e-enquadramento.md](websockets-full-duplex-e-enquadramento.md) | WebSocket: API, Upgrade, framing, HoL, extensions, proxies, performance | ch. 17: p.305–325 |
| [webrtc-p2p-ice-stun-turn-e-datachannel.md](webrtc-p2p-ice-stun-turn-e-datachannel.md) | WebRTC: signaling, SDP, ICE, DTLS, SRTP, SCTP, DataChannel, architectures | ch. 18: p.327–380 |
| [xhr-sse-e-escolha-de-transporte.md](xhr-sse-e-escolha-de-transporte.md) | Browser network stack, XHR, CORS, polling, long-polling, SSE, comparison | ch. 14: p.271–277; ch. 15: p.279–296; ch. 16: p.297–303 |
| [casos-e-antipadroes.md](casos-e-antipadroes.md) | Antipatterns the book condemns, with page and fix; modern antipatterns as [extrapolation] | cross-cutting (main points on p.41, 140, 141, 216, 217, 236, 260, 261, 289) |
| [procedimentos.md](procedimentos.md) | Checklists: diagnose latency, TCP, TLS, mobile, migration to 2.0, transport choice, answering the user, embedded instructions | cross-cutting (p.50–52, 91, 157–169, 259–268, 291–296) |
| [glossario.md](glossario.md) | Terms with short definition and page; terms the book does not use | cross-cutting |

How to use: read this index, open the reference for the topic, cite with a page, and use the glossary for loose terms. For lookup shortcuts, `python -I scripts/perf_lookup.py <term>`; the index is only a shortcut, so check the reference before citing.

---

## 5. Era: the book's "HTTP 2.0" is the 2013 draft

The book was written when HTTP 2.0 was a work in progress. Everything it says about the protocol describes the draft, not the 2015 RFC 7540. The author warns that low-level details, the bit encoding and the field names could change (HPBN p.226, 229).

| Aspect | In the book (2013 draft) | Page | Later [extrapolation] |
| :--- | :--- | :--- | :--- |
| Drafts cited | Draft 2 and Draft 4; the schedule foresaw the group's last call in April 2014 | 228, 229, 235 | RFC 7540 (2015), RFC 9113 (2022) |
| Frame header | 8 bytes, with a 16-bit length prefix | 244, 245 | 9 bytes, 24-bit length |
| Pseudo-headers | `:method`, `:scheme`, `:host`, `:path` | 241 | `:authority` in place of `:host`; `:status` in the response |
| Header compression | "Header tables" with differential encoding; no HPACK name | 240, 241 | HPACK (RFC 7541), with static table and Huffman |
| Priority | 31-bit value per stream; 0 is the highest | 233 | Dependency tree with weights, later deprecated |
| Flow control | `WINDOW_UPDATE`; the receiver can turn it off | 237 | Can no longer be turned off |
| Disabling push | By setting the concurrent streams limit to zero | 238 | `SETTINGS_ENABLE_PUSH` |
| Stream ID parity | The book contradicts itself (p.247 says client even; p.249 treats odd as the client's) | 247, 249 | RFC 7540: client odd, server even |
| Negotiation | TLS + ALPN, or cleartext Upgrade with `HTTP2-Settings`; NPN for SPDY | 72, 243, 260 | h2 only over TLS in practice |
| Production version | SPDY, with years of real-world testing | 260 | Retired |

Other era markers in the book: TLS up to version 1.2 (HPBN p.66); IW10 standardized in April 2013 (p.38); TCP Fast Open still an IETF draft (p.34); WebRTC "under construction" (p.328); WebSocket version 13 (p.307); 802.11ac as the future (p.110); VoLTE under development (p.127); average bandwidth figures from the first quarter of 2013 (p.28); 2013 page averages (p.187).

---

## 6. What the source does not cover

The absence applies to the text of the book. If the user asks, say that the source does not address it and, if it helps, answer as a clearly marked `[extrapolation]`.

- **TLS 1.3 and 0-RTT** (the book goes up to TLS 1.2, HPBN p.66); ECDHE and forward secrecy, Certificate Transparency, ECH.
- **QUIC and HTTP/3**; the book only recognizes TCP HoL as the limit of 2.0 (HPBN p.236).
- **RFC 7540, RFC 9113 and HPACK (RFC 7541)**, static table, Huffman, priority tree.
- **Service Workers**, Cache Storage, implemented Push API (the book mentions AppCache and a future Push API, HPBN p.161, 167).
- **Core Web Vitals** (LCP, INP, CLS) and `fetchpriority`; the book's metrics are PLT, Navigation/Resource/User Timing and RUM (HPBN p.185, 198, 200).
- **5G**, APNs and FCM (the book goes up to LTE-Advanced and mentions GCM, HPBN p.128, 161).
- **`preload` and `preconnect` as link `rel`**, `defer` and `async`: the book documents `dns-prefetch`, `subresource`, `prefetch` and `prerender` (HPBN p.202) and only says, in general, to defer non-critical JS (HPBN p.202).
- The terms "critical rendering path", "render-blocking", FOIT, FOUT and "above the fold" do not appear in the book.
- **HTTP cache in detail:** `no-store`, `private`, `immutable`, conditional revalidation with 304; the book only covers `max-age`, `Last-Modified` and `ETag` (HPBN p.254).
- **BBR**, final TFO (RFC 7413), current congestion measurements.
- **NAT types**, hole punching, numeric NAT timeout value for UDP (the book says it varies by device, HPBN p.57, 58).
- **Typical tail time of 10 to 20 s:** the book only gives examples of timers and says the carrier defines them (HPBN p.140).
- **WebSocket over HTTP/2** (RFC 8441), `permessage-deflate` (RFC 7692), WebTransport, fetch with streams.
- Front-end frameworks, databases and any measurement after 2013.

---

## 7. Package scripts (read-only, no network)

- `python -I scripts/perf_lookup.py <term>` or `--list`: lookup shortcut with PDF pages and a warning for terms the book does not use.
- `python -I scripts/tls_rtt_calc.py --compare --rtt 120 --payload-kb 20`: handshake and slow-start RTTs in the book's model.
- `python -I scripts/http2_frame_analyzer.py --demo`: checks of streams and frames according to the book's draft.
- `python -I scripts/critical_path_advisor.py --demo`: triage of render-blocking resources; "no findings" is not approval.
