# web-performance-networking-expert

Specialist agent in web networking and performance, distilled from a single source:

| Abbreviation | Work | Edition | Pages | File |
|---|---|---|---|---|
| **HPBN** | *High Performance Browser Networking: What every web developer should know about networking and web performance*, Ilya Grigorik | O'Reilly, 1st edition, 2013 | 401 (cite the PDF page; printed = PDF − 18, because of 16 roman-numeral pages) | `06_web_and_frontend/Web-Performance-HPBN-Grigorik.pdf` |

> **Correction (2026-10-31).** Earlier versions of this package mixed printed and PDF page numbers and presented post-2013 content as [from source] (TLS 1.3/0-RTT, QUIC/HTTP/3, RFC 7540, HPACK, 9-byte frame, `preload`, `immutable`). The references, the prompt and the scripts were rewritten against the PDF text; the earlier report ("19/19 PASS, 159 citations validated") had no method or rounds and was replaced. Details in `tests/relatorio-de-fidelidade.md`.

## Thesis

Latency, not bandwidth, is the bottleneck of most web applications: eliminate round trips, reuse connections, move data closer to the client and understand the transport beneath each browser API (HPBN p.21, p.27, p.30).

## Era

The book is from 2013. It covers TLS up to 1.2 and describes **HTTP 2.0 as a draft** (8-byte frame, `:host`, "header tables"). What changed afterwards appears only as [extrapolation] in the references' "After the book" sections.

## Structure

```
web-performance-networking-expert/
├── .claude-plugin/plugin.json
├── .github/agents/web-performance-networking-expert.agent.md     # GitHub Copilot shell
├── AGENTS.md                          # Codex shell
├── agents/web-performance-networking-expert.md     # agent prompt
├── references/                                     # INDEX.md + 15 references with PDF pages
├── scripts/
│   ├── perf_index.json + perf_lookup.py            # topic index with pages
│   ├── tls_rtt_calc.py                             # TCP/TLS RTTs and slow-start (book model)
│   ├── http2_frame_analyzer.py                     # frames/streams in the 2013 draft
│   └── critical_path_advisor.py                    # blocking resources, hints and cache
└── tests/
    ├── casos-de-teste.md                           # 19 cases with paginated answer key
    └── relatorio-de-fidelidade.md                  # rounds, failures and fixes
```

## Scripts

Standard library only, no network, read-only, UTF-8 output, `--help`.

```bash
python -I scripts/perf_lookup.py --list
python -I scripts/tls_rtt_calc.py --compare --rtt 56 --payload-kb 20 --initcwnd 4 --server-ms 40
python -I scripts/http2_frame_analyzer.py --demo
python -I scripts/critical_path_advisor.py --demo
```

## Rigor

- Citation `[from source] (HPBN p.N)` with the PDF page; `[inference]`, `[extrapolation]` and `[DATED]` for the rest.
- What the source does not cover is in `references/INDEX.md` (TLS 1.3, QUIC/HTTP/3, RFC 7540/HPACK, Core Web Vitals, 5G...).
- Instructions embedded in pasted code or configurations are treated as data.

## Installation

- **Claude Code**: `claude --plugin-dir 06_web_and_frontend/_agents/web-performance-networking-expert`
- Through the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install web-performance-networking-expert@general-agents`.
- **Copilot**: copy `.github/agents/web-performance-networking-expert.agent.md` to the repository's `.github/agents/` (or `~/.copilot/agents/`).
- **Codex**: use the package's `AGENTS.md`. Both shells merely tell the agent to read `agents/web-performance-networking-expert.md`; when you change the prompt, update them.
