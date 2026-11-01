# Browser rendering pipeline: DOM, CSSOM, JavaScript and the resource waterfall

Convention: every cited page is the PDF page (`HPBN p.N`); the printed one is N − 18. Labels: `[from source]`, `[inference]`, `[DATED]`, `[extrapolation]` (the latter only in the final section).

**Terminology note.** The book does not use the term "critical rendering path" nor "above the fold", "FOUC", "render-blocking" or the `defer`/`async` attributes (text search finds no occurrences). The concepts appear under other names: "browser processing pipeline" (HPBN p.186), "DOM, CSSOM, and JavaScript" (p.186), "render tree", "time to render" (p.186), "Start Render" and "Document Complete" in the waterfall (p.190), "preload scanner" (p.258), "first-paint critical CSS" (p.222) and "noncritical JavaScript should be deferred" (p.202, in a generic sense, without the HTML attribute). The items below respect these limits.

When to open: decisions about CSS/JS order in the document, time to render, reading a waterfall and metrics. For hints and cache, see `otimizacoes-de-navegador-resource-hints-e-caching.md`.

---

## 1. Pipeline: HTML, CSS and JS (ch. 10)

- Parsing the HTML builds the DOM. In parallel, the CSSOM is built from the style rules and resources. The two are combined in the render tree, at which point the browser has the information to do layout and draw (paint) [from source] (HPBN p.186).
- JavaScript complicates the picture: a synchronous `document.write` blocks parsing and DOM construction, and scripts can query computed style, so JS may wait for CSS [from source] (HPBN p.186).
- Consequence: DOM and CSSOM construction are interleaved; the DOM does not advance until the JS executes, and the JS does not execute until the CSSOM is available [from source] (HPBN p.186).
- Hence the maxim "styles at the top, scripts at the bottom": rendering and script execution are blocked by stylesheets, so deliver the CSS as early as possible [from source] (HPBN p.186).
- First-load performance and "time to render" depend on how this dependency graph between markup, styles and script is resolved [from source] (HPBN p.186).
- Rendering and script follow a single-threaded, interleaved model; there is no concurrent DOM modification [from source] (HPBN p.194). Optimizing JS and rendering is also useless if the browser is blocked waiting on the network [from source] (HPBN p.194).
- The network is part of the pipeline: when the browser waits for resources, all the other stages (parsing, layout, style, JS, rendering) wait along with it [from source] (HPBN p.271).

## 2. HTML is incremental; CSS and JS are not

- HTML is parsed incrementally; that is why the browser discovers resources early and dispatches requests in parallel. The moment each resource is fetched is determined largely by the structure of the markup, which creates the waterfall effect [from source] (HPBN p.190).
- Unlike HTML, parsing and execution of JS and CSS only begin after the entire file has been downloaded; neither model allows incremental execution [from source] (HPBN p.221).
- Effect: large CSS takes a long time to build the CSSOM and can delay the first paint; large JS delays execution, while smaller files allow "incremental" execution [from source] (HPBN p.221). Target suggested by PageSpeed: 30–50 KB compressed per JS bundle [from source] (HPBN p.221).

## 3. Page structure rules (what the book says to do)

Recommendations to help the browser [from source] (HPBN p.202):

1. Critical resources (CSS and JS) should be discoverable as early as possible in the document.
2. CSS should be delivered early, to unblock rendering and JS execution.
3. Non-critical JS should be deferred so it does not block DOM and CSSOM construction (the book gives the rule, not the `defer`/`async` mechanism; see "After the book").
4. HTML is parsed incrementally, so the document should be flushed periodically.

- Google Search case: the server immediately sends the static page header, even before parsing the query; while the client parses this beginning, the query goes to the index and the rest of the document arrives later. Dynamic parts of the header (such as the logged-in user's name) are filled in by JS [from source] (HPBN p.203).
- Gmail case: separates and delivers first the critical CSS for the first paint, delivers JS in smaller chunks for incremental execution and inlines critical CSS and JS in the HTML [from source] (HPBN p.222).
- Preload scanner: while the parser is blocked waiting for a script or other blocking resource, the browser looks ahead in the source and dispatches downloads early. It is a speculative optimization, used only when the parser is blocked, and yielded about a 20% improvement in load and render in Chrome data [from source] (HPBN p.258).
- Scanner limit: it does not execute scripts. Resources scheduled by JS are hidden from it; moving scheduling into scripts gives fine-grained control, but costs this visibility [from source] (HPBN p.258).
- Common bottlenecks in 1.x that delay page construction: blocking resources on the client, undersized servers and load balancers [from source] (HPBN p.258).

## 4. Timing goals and perception

Perception table [from source] (HPBN p.188): 0–100 ms feels instantaneous; 100–300 ms small, perceptible delay; 300–1000 ms "the machine is working"; above 1,000 ms likely mental context switch; above 10,000 ms the task is abandoned.

- Community rule of thumb: render, or at least give visual feedback, in under 250 ms [from source] (HPBN p.188).
- DNS, the TCP handshake and a few RTTs of a typical request can consume much or all of the 100–1,000 ms budget on the network alone [from source] (HPBN p.188).
- Revenue cost: a 2,000 ms delay in Bing searches reduced revenue per user by 4.3%; in the Aberdeen study of more than 160 organizations, one extra second implied 7% fewer conversions, 11% fewer page views and 16% less satisfaction [from source] (HPBN p.189). The book advises measuring the impact on your own site [from source] (HPBN p.189).

## 5. Reading the waterfall

- Each HTTP request has stages: DNS resolution, TCP handshake, TLS negotiation (if any), sending the request and downloading the content [from source] (HPBN p.190).
- Yahoo! example (March 2013): main document in 683 ms, with more than 200 ms (30%) waiting on the network; 52 resources from 30 hosts, 486 KB [from source] (HPBN p.190).
- Observations: new requests go out while the document is still arriving (incremental parsing); "Start Render" and "Document Complete" occur well before all resources finish; the rest (ads, widgets) completes later [from source] (HPBN p.190).
- Which metric to track (first render, document complete or last resource) depends on the application [from source] (HPBN p.192). Different browsers dispatch in different orders; WebPageTest lets you choose location, browser and version [from source] (HPBN p.192).
- "Front-end performance" is a misleading name: server response time and network latency are equally critical; a resource blocked on the network cannot be parsed or executed [from source] (HPBN p.192).
- Per-connection view: the download is only a small fraction of each connection's life; at Yahoo! there are 15 DNS lookups, 30 TCP handshakes and a lot of waiting for the first byte [from source] (HPBN p.192). Bandwidth utilization is low; the bottleneck is round-trip latency [from source] (HPBN p.193).

## 6. Latency, not bandwidth

- For ordinary browsing (hundreds of small resources, dozens of hosts), RTT latency is the limiting factor; HD video streaming is what depends on bandwidth (3+ Mbps for 1080p) [from source] (HPBN p.194).
- Belshe study: going from 1 to 2 Mbps load time almost halves; above 5 Mbps the gains are single-digit percentages; from 5 to 10 Mbps, only 5% [from source] (HPBN p.195). For each 20 ms less latency, the gain in load time is linear [from source] (HPBN p.196).
- Causes: TCP handshakes, flow and congestion control and HoL due to loss; HTTP uses small, bursty transfers, while TCP is optimized for long-lived connections [from source] (HPBN p.196). On wireless networks the effect is larger [from source] (HPBN p.196).
- 2013 averages (HTTP Archive): 90 requests from 15 hosts and 1,311 KB (HTML 10/52 KB, images 55/812 KB, JS 15/216 KB, CSS 5/36 KB, other 5/195 KB) [from source] (HPBN p.187). `[DATED]` The 2013 numbers are only good as an order of magnitude (HPBN p.187).

## 7. Measurement

- PLT (page load time): the `onload` event, when the document and its dependencies have finished [from source] (HPBN p.185). In applications, PLT is insufficient; define your own milestones (first interaction, engagement, conversion) [from source] (HPBN p.185).
- Synthetic tests give a controlled environment and a baseline; set a budget per metric and raise an alarm when it is exceeded [from source] (HPBN p.197). They do not capture the diversity of caches, intermediaries, hardware, browsers and connectivity, so complement with RUM [from source] (HPBN p.197).
- Navigation Timing (`performance.timing`) exposes DNS, TCP connection etc.; support in 2013: IE9+, Chrome 6+, Firefox 7+ [from source] (HPBN p.198). Resource Timing gives the same per resource; User Timing marks/measures application metrics with `performance.mark` [from source] (HPBN p.200).
- Analyze distributions (histograms, medians, quantiles), not averages [from source] (HPBN p.199).

## After the book [extrapolation]

- "Critical rendering path" is a term that postdates the book. It generally designates DOM, CSSOM, render tree, layout and paint, with CSS and synchronous JS treated as "render-blocking".
- `defer` and `async` attributes on `<script>`, `<link rel="preload">` and `fetchpriority` are later ways for the author to control scheduling; the book only describes the general rule of deferring non-critical JS, without citing these attributes.
- Core Web Vitals (LCP, INP, CLS) and the inline "critical CSS" technique are evolutions of metrics and practices that the book only anticipates in the Gmail case and in the first-render goals.
- `performance.mark` and Navigation Timing were refined into Performance Timeline and PerformanceObserver.

## What the source does not cover

- Detailed stages of HTML tokenization, the CSS cascade, specificity, the layer tree and GPU compositing.
- The difference between `visibility: hidden` and `display: none` in the render tree, FOUC/FOIT and web font behavior.
- Semantics of `defer`, `async`, ES modules, `preload`, `fetchpriority`.
- Modern metrics (First Contentful Paint, LCP, INP, CLS) and their thresholds.
- Reflow versus repaint and the cost of layout thrashing.
