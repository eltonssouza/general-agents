# Load and performance testing with Apache JMeter (JMETER)

**Nature and version of the source.** JMETER is the Java Code Geeks *JMeter Tutorial* (2015), with examples in **JMeter 2.11** (Java 8u20, MySQL 5.6) (JMETER p.5-6). It is an introductory GUI tutorial; it does **not** contain "Little's Law", user-count calculation, percentiles or an HTML dashboard. Convention: `(JMETER p.N)` = **PDF** page; printed ("N / 46") = PDF − 7. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Types of test and what JMeter is
- `[from source]` JMeter configures and runs load, performance and stress tests with several protocols (databases, FTP, HTTP/HTTPS, other servers) (JMETER p.8).
- `[from source]` Tutorial definitions: **load** takes the system to what was designed and required, to measure behavior under extreme conditions; **performance** checks the response and stability for a specific load; **stress** tries to break the system with more resources beyond the design limits (JMETER p.8).
- `[from source]` It is a Java desktop application with a Swing interface, cross-platform; the framework allows concurrency with several threads and thread groups; it is extensible through plugins and is open source from Apache (JMETER p.9).
- `[from source]` Installation: JRE 1.6 or higher, the `JAVA_HOME` variable, download and extract JMeter and start `jmeter.bat` on Windows (JMETER p.11-12).
- `[from source]` Native protocols: web (HTTP/HTTPS), web services (SOAP/XML-RPC), JDBC, LDAP, JMS, email (POP3, IMAP, SMTP), FTP and functional tests with JUnit (JMETER p.14).

## 2. Anatomy of a Test Plan
- `[from source]` A Test Plan is a set of requests against servers configured by specific instructions, with parameters and success conditions (JMETER p.15).
- `[from source]` **Thread Group**: root of the plan; controls the core parameters: **number of threads**, **ramp-up period** (the time JMeter takes to start all the threads), **loop count** (number of iterations) and **error behavior** (stop the thread, stop the test, continue); there is also a "Scheduler" with start and end (JMETER p.15).
- `[from source]` **Samplers** send requests (HTTP, JDBC, JMS, FTP, SMTP, JUnit, TCP, LDAP, among others) (JMETER p.15-16).
- `[from source]` **Logic controllers** define the execution order of the samplers in the Thread Group (Simple, Loop, Once Only, Interleave, Random, If, While, ForEach, Transaction and others) (JMETER p.16-17).
- `[from source]` **Listeners** show the results (tables, trees, logs); they can sit anywhere in the plan, but only collect data from samplers at the same level or below (JMETER p.17).
- `[from source]` **Timers** define the interval between requests; without a timer JMeter runs the next request immediately after the previous one (JMETER p.18).
- `[from source]` **Config elements** create variables and values for the samplers and run at the start of the node they belong to (e.g. CSV Data Set Config, HTTP Request Defaults, HTTP Header Manager, JDBC Connection Configuration) (JMETER p.19).
- `[from source]` **Pre processors** run before the sampler; **post processors** run after and can extract values from the response (JMETER p.19-20).
- `[from source]` **Execution order**: config elements, pre processors, timers, sampler, post processors, assertions, listeners (the last three only if there are results) (JMETER p.21).
- `[from source]` A plan can contain other plans, a common practice for grouping tests by functional or technical logic (JMETER p.21).

```mermaid
flowchart LR
    TP[Test Plan] --> TG[Thread Group: threads, ramp-up, loops, error]
    TG --> CE[Config elements] --> PRE[Pre processors] --> TM[Timers] --> SM[Sampler] --> POST[Post processors] --> AS[Assertions] --> LS[Listeners]
```

`[from source]` The diagram above shows the **execution order** (p.21), not a hierarchical tree; v1 presented "Thread Group > Logic Controllers > Samplers > Timers > Pre/Post > Assertions > Listeners" as an architecture "JMETER p.8-18", which does not appear that way in the PDF.

## 3. Tutorial examples (real parameters)
- `[from source]` HTTP plan against the Wikipedia site: Thread Group with threads, ramp-up in seconds and iterations; HTTP Request with the server name without the protocol; View Results Tree (JMETER p.25-27).
- `[from source]` Constant timer of 500 ms: each request waits 500 ms after the previous one (JMETER p.29).
- `[from source]` Database plan: MySQL, driver in JMeter's `lib`, JDBC Connection Configuration (URL `jdbc:mysql://localhost:3306/jmeter`, driver class) and a JDBC Sampler with a `select`; the same sampler works to update data (JMETER p.32-35).
- `[from source]` Plan with JUnit: package the tests in a jar in `jmeter/lib/junit` and use the "JUnit Request" sampler; the example supports JUnit 4 methods and there is an option for JUnit 3 (JMETER p.37-38).
- `[from source]` Recording: Firefox uses JMeter's proxy at localhost:8080; Thread Group of **50 threads, 10 s ramp-up and 1 loop**; "Test Script Recorder" in the Workbench (which is not saved with the plan) (JMETER p.41-45).
- `[inference]` 50 threads in 10 s gives a start rate of 5 threads per second (simple arithmetic on p.42); the tutorial does not comment on that rate.
- `[from source]` Plugins: there are plugins for charts and for CI integration (the text cites the Jenkins Performance Plugin) (JMETER p.49).

## 4. Load sizing: what is NOT in the PDF (`[extrapolation]`)
The tutorial does not teach how to compute the load. The formulas below are general knowledge of queueing theory and performance, useful, but **without a page** in JMETER:
- **Little's Law**: N = X × R (users in the system = throughput × response time); with think time Z in a closed system, N = X × (R + Z), hence X = N / (R + Z).
- **Start rate** of the ramp-up: threads / ramp-up (arithmetic).
- **Percentiles** (p90, p95, p99) and JMeter's HTML dashboard (`-e -o`): a feature of versions later than 2.11 `[DATED]` relative to the PDF; check the current documentation.
`jmeter_calc.py` implements only these calculations and labels them.

## 5. v1 terms without backing in JMETER
"Industry standard", "heterogeneous load of 1,000 users", "Forever" as a loop (the PDF speaks of loop count, p.15), "Throughput in bytes/s", HTTP Header Manager with Content-Type (the text lists the element on p.19, but does not describe it), "Ramp-Up of 0 s takes down the firewall" (not present). Treat as `[extrapolation]`.
