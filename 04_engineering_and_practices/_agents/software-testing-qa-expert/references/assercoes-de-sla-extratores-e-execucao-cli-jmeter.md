# Assertions, data extraction and non-GUI execution in JMeter (JMETER)

Source: *JMeter Tutorial* (Java Code Geeks, 2015; JMeter 2.11). Convention: `(JMETER p.N)` = **PDF** page (printed = N − 7). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Assertions
- `[from source]` Assertions confirm the validity of the plan by validating a sampler's response, much like unit test assertions; you choose which ones are active per plan (JMETER p.18).
- `[from source]` List of assertions available in 2.11: Response, Duration, Size, XML, XPath, HTML, XML Schema, MD5Hex, Compare, plus BeanShell, BSF and JSR223 (JMETER p.18).
- `[from source]` **Duration Assertion** in the example: configured to fail if the response takes longer than **100 ms**, only for the main sample; the test showed failures, and with **2000 ms** almost all requests passed (JMETER p.29-30). This demonstrates the mechanics; the tutorial does not define an SLA, p95 or target latency.
- `[from source]` **Size Assertion** in the example: requires a response larger than **5000 bytes**; an error response would probably be smaller and would fail (JMETER p.30-31).
- `[from source]` The tutorial lists the **Response Assertion** (p.18) but does not describe its configuration. v1 said it validates HTTP code 200/201 and a regex in the body "JMETER p.30"; that is `[extrapolation]` (general JMeter knowledge).
- `[inference]` For a "latency SLA" use the reasoning of the Duration Assertion example (limit in ms per sample), but the SLA value (e.g. 150 ms) comes from the user, not from the book.

## 2. Data extraction (pre and post processors)
- `[from source]` Post processors listed: Regular Expression Extractor, XPath Extractor, CSS/JQuery Extractor, Result Status Action Handler, Debug PostProcessor and the JSR223, JDBC, BSF and BeanShell variants; they run after the sampler and can extract values used later (JMETER p.20).
- `[from source]` Pre processors listed: HTML Link Parser, HTTP URL Re-writing Modifier, HTTP User Parameter Modifier, User Parameters, RegEx User Parameters, JDBC/JSR223/BeanShell/BSF PreProcessor (JMETER p.19).
- `[from source]` Config elements such as `CSV Data Set Config` and `User Defined Variables` create variables used by the samplers (JMETER p.19).
- `[extrapolation]` **JSON Path Extractor / JSON Extractor** is not in the JMeter 2.11 list in the PDF; later versions have native JSON support (check the current documentation). v1 cited a JSON extractor ("JMETER p.21") with `$.token`: unsupported.
- `[extrapolation]` Correlating a login token for subsequent requests (storing it in a variable and sending it in a header) is general practice; the PDF only says post processors extract values for later use (p.20).

## 3. Execution and best practices (p.50)
- `[from source]` Although the GUI is useful for creating plans, "experienced users" prefer **non-GUI mode** to run and store results: `jmeter -n -t test.jmx -l test.jtl` (give the full path of the plan) (JMETER p.50). This is a tutorial **preference/best practice**, not a "prohibition" nor a warning with CPU numbers.
- `[from source]` Listeners help with analysis but consume **a lot of resources and memory**; use as few as possible (JMETER p.50). The text says the `-l` flag makes them unnecessary when they are not needed.
- `[from source]` Check "View only errors" in the results tree; use variables and loops in a single sampler instead of several nearly identical samplers; in JUnit plans give meaningful error and assertion messages; **Stop** (Ctrl+.) immediately stops the threads and **Shutdown** (Ctrl+,) asks them to stop at the end of their current work (JMETER p.50).
- `[from source]` The PDF mentions the Jenkins Performance plugin for running plans from the CI tool (JMETER p.49).
- `[from source]` SWE-G on load tests: they require sending a large volume of traffic, are a "highly emergent" property of the system and must mimic production; when comparing versions, run both on the same machine or calibrate with several runs (SWE-G p.204, p.213).

### Command with HTML report (`[extrapolation]`, `[DATED]` relative to the PDF)
`jmeter -n -t plano.jmx -l resultado.jtl -e -o pasta_relatorio/` uses the `-e`/`-o` options to generate the HTML dashboard at the end of the run. These options are **not in the PDF** (JMeter 2.11) and appear in later versions; check the current documentation before using them. The dashboard's p90/p95/p99 percentiles are also not covered by the tutorial.

## 4. v1 claims removed
| v1 | Status |
|---|---|
| Strict "prohibition" of the GUI, "NEVER" run load through the GUI, "consumption close to 100% CPU" | Exaggeration: p.50 recommends non-GUI for experienced users and warns about the cost of listeners |
| `-e -o` and dashboard as "from source (JMETER p.50)" | `[extrapolation]` |
| JSON Path Extractor | `[extrapolation]` |
| Little's Law "JMETER p.9-10, p.14-16" | Not present (p.9-10 is Java/Swing and scope; p.14-16 is the list of protocols and samplers) |
| "Response Assertion validates status 200/201" | `[extrapolation]` |
