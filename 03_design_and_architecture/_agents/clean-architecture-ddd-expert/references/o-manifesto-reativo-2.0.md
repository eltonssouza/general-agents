# The Reactive Manifesto 2.0

Source: *The Reactive Manifesto*, version 2.0, published on September 16, 2014 (acronym `REACT`; **2 PDF pages**). **Convention**: `(REACT p.N)` = PDF page. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

> **Authorship.** The PDF **does not list the authors** (there are no personal names in the text). Attribution to Jonas Bonér, Dave Farley, Roland Kuhn and Martin Thompson is external knowledge `[extrapolation]`.
> The manifesto is a **short position text**; it has no code, concrete examples, tool names, nor the term "supervisor", "actor model", "Akka", "Reactive Streams" or SLA numbers.

---

## 1. Motivation

- Organizations in different domains independently discover similar patterns for building software; these systems are more robust, resilient, flexible and better positioned for modern demands `[from source] (REACT p.1)`.
- The requirements have changed: a few years earlier, a large application had dozens of servers, seconds of response time, hours of offline maintenance and gigabytes of data; today it runs from mobile devices to cloud clusters with thousands of multicore processors, with users expecting responses in milliseconds, 100% availability and data measured in petabytes `[from source] (REACT p.1)`.
- Thesis: a coherent approach to systems architecture is needed; the necessary aspects are already individually recognized; systems that are Responsive, Resilient, Elastic and Message Driven are called **Reactive Systems** `[from source] (REACT p.1)`.
- Claimed benefits: systems that are more flexible, loosely coupled and scalable, easier to develop and change, more tolerant of failure, which respond to it "gracefully rather than disastrously" `[from source] (REACT p.1)`.

## 2. The four attributes

1. **Responsive** `[from source] (REACT p.1)`: the system responds in a timely manner if at all possible. It is the cornerstone of usability and utility, and allows problems to be detected and handled quickly; it focuses on fast and **consistent** response times, with reliable upper bounds, which simplifies error handling, builds trust and encourages interaction.
2. **Resilient** `[from source] (REACT p.1)`: the system stays responsive in the face of failure, and this applies to any system (a non-resilient system will become unresponsive after a failure). Resilience comes from **replication, containment, isolation and delegation**: failures are contained within each component, isolating them from one another; recovery of each component is **delegated to another (external) component** and high availability is ensured by replication where necessary; the component's client is not burdened with handling its failures.
3. **Elastic** `[from source] (REACT p.2)`: stays responsive under varying load; reacts to changes in the input rate by increasing or decreasing resources; this implies designs **with no contention points or central bottlenecks**, with the ability to *shard* or replicate components and distribute inputs; supports predictive and reactive scaling algorithms by providing real-time performance measures; achieves elasticity cost-effectively on commodity hardware and software.
4. **Message Driven** `[from source] (REACT p.2)`: relies on **asynchronous message passing** to establish a boundary between components that ensures loose coupling, isolation, location transparency and a means of delegating errors as messages. Explicit messages enable load management, elasticity and flow control by **shaping and monitoring the queues** and applying *back-pressure* when necessary. Messaging with location transparency allows failures to be handled with the same constructs and semantics in a cluster or on a single host; non-blocking communication allows recipients to consume resources only while active, reducing overhead.

The diagram on p.2 (Responsive at the top, Resilient and Elastic at the sides, Message Driven at the base) is a figure and is not legible as text in the PDF; only the labels appear. The reading "Message Driven is the foundation that enables the others" is an `[inference]` from the arrangement and the text (messaging is described as a means for isolation, error delegation, elasticity and flow control, p.2). The text does not use the words "foundation" or "enabling".

## 3. Composition

- Large systems are composed of smaller ones and depend on the reactive properties of their constituents; therefore the principles apply **at all scale levels**, making them **composable** `[from source] (REACT p.2)`.
- The world's largest systems rely on architectures with these properties and serve billions of people daily; it is time to apply these principles consciously from the start, instead of rediscovering them `[from source] (REACT p.2)`.

## 4. Useful distinctions (labeled)

- "Reactive Systems" (manifesto) is **not** the same as reactive programming (RxJS, Reactor etc.) `[extrapolation]`: the PDF does not make this distinction.
- *Back-pressure* is cited as a flow control mechanism (p.2); the definition "consumer signals the pace to the producer" is a reading `[inference]`; the expression "Reactive Streams" and specific protocols are `[extrapolation]`.
- "Supervisor" (actor model), "circuit breaker", "bulkhead", "Kubernetes HPA" are **not in the PDF** `[extrapolation]`. The text says only that recovery is delegated to another component (p.1).
- "Without human intervention" in scaling is **not** in the text; what is there is "react to changes in the input rate" (p.2).
- `[DATED]` Comparison numbers (dozens of servers, gigabytes) reflect the 2014 description (p.1).

## 5. Relationship with the other texts in the corpus

- The emphasis on isolation and error delegation recalls the protection of internal policies against external details in `CA12`, but the manifesto is **not** about source code or compile-time dependency: it deals with properties of running systems `[inference]`.
- The link with *Out of the Tar Pit* is indirect: the paper cites the actor/message model only in passing as a concurrency variation (`TARPIT p.14`) `[inference]`.
