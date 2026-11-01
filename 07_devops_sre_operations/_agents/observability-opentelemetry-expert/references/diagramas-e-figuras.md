# Diagrams and figures (pages rendered and described)

Method: the pages were rendered with PyMuPDF and inspected; the extracted text does not capture the figure labels. The descriptions below come from **visual reading** of the images (checkable by opening the PDF at the indicated page); the automatic verification only covers the text captions ("Figure N").

## DOW Figure 1, p.3: "Distributed system advantages at a business level"
[from source, figure] Top-to-bottom flowchart. Top: **Competitive Advantage**, which splits into **Availability** and **Scalability** (on the sides) and **Agility** (dark box in the center). From Agility come **Deployability**, **Testability** and **Maintainability**, which converge on **Velocity** and then on **Speed to Market**. Reading: the five characteristics from p.1 support competitive advantage and velocity. (DOW p.3)

## DOW Figure 2, p.5: "Detailed observability concept"
[from source, figure] An **Observability** diamond at the base connects, upward, to a **Profiling** box, which feeds three rounded boxes at the top: **Monitoring**, **Logging**, **Tracing**; from the diamond also come, downward, **Alerting** and **Graphing**. The text interprets: five pillars, three for collecting data about the application profile and two for interpretation (DOW p.5). Note: the text uses "metrics" where the figure uses "Monitoring" (tension in `observabilidade-conceitos-e-pilares.md`).

## DOW Figure 3, p.6: "Overview of an observability workflow"
[from source, figure] Dashed rectangle **Distributed Systems** with three boxes: **System Data**, **Application Data**, **Third Party**; "Collect" arrows lead to an **Agents** diamond; a "Send to remote storage" arrow leads to **Observability Platform** (funnel), which splits into four dark boxes: **Archive**, **Compression**, **Retention**, **Encryption**. Reading: agents collect three data origins and send them to a central platform, which handles archiving, compression, retention and encryption (DOW p.6). [inference] Retention and encryption appear only here and in the considerations table (DOW p.5).

## OTW, p.3 (figure without a numbered caption, before/after the Collector)
[from source, figure] Two halves connected by a downward arrow. **Before**: several "Application" instances with SDKs talking **directly** to different tools per signal, with no common standard: metrics path labeled "Prom. Expo" to **Telegraf** -> **Time Series DB** -> metrics visualization tool; logs labeled "Logfmt" to **Fluentd** -> **Document DB** -> logs visualization; traces labeled "Jaeger Thrift" to **Jaeger** -> **Trace storage** -> traces visualization. **After**: the applications with the **OTel SDK** send via **OTLP** to a single **OTel Collector**, which feeds the same three stores (Time Series DB, Document DB, Trace storage) and their visualization tools. Reading: the Collector replaces per-signal agents and protocols with a single point and a single protocol (OTW p.3). [inference] The arrow labels "Prom. Expo", "Logfmt", "Jaeger Thrift" indicate each tool's native formats; the page text does not explain them.

## Other pages
- DOW p.2 and OTW p.2: sponsor ads (LogicMonitor; InfluxDB), with no technical content. OTW p.1: ad banner (InfluxDB) + text. Remaining pages: text, table (DOW p.5) and code blocks (OTW p.3, 5, 6).
