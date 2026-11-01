# Synchronous communication: styles, REST, and gRPC

Sources: MS-MIC, MS-CLD, JMG, SDH, EDS, APIGW, and REST (Baeldung, *Build Your API with Spring*, which is a Spring implementation guide: it does NOT contain the Richardson Maturity Model, a table of safe/idempotent methods, or the justification of DTOs as a defense against mass assignment — the previous package attributed these to it). Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Communication types and styles

- Two axes: synchronous protocol (HTTP) vs. asynchronous (AMQP); and single receiver (e.g., Command) vs. multiple receivers (publish/subscribe, which must be asynchronous). [from source] (MS-MIC p.64)
- What matters is not the protocol but integrating microservices asynchronously while preserving independence; critical rule: communication between microservices must be asynchronous, without depending on other internal services in the response to the original request, not even for queries. [from source] (MS-MIC p.65)
- MS-CLD interactions: Query (needs a response), Command (asks for an action, response not mandatory), Event (publisher and subscribers do not know each other). [from source] (MS-CLD p.77) (MS-CLD p.78)
- EDS: commands ask for something and may have a response; events are a fact/notification, with no response; queries have no side effects; commands tend to stay inside the bounded context. [from source] (EDS p.45) (EDS p.46)
- SDH: REST (stateless, resource-based, HTTP methods, JSON/XML) vs. RPC (action-oriented, several protocols). [from source] (SDH p.35) (SDH p.36)

## 2. Chains of synchronous calls (anti-pattern)

- Chains of synchronous HTTP between microservices: blocking and poor performance, coupling, failure in any link brings the chain down; "you would have an HTTP-based monolith across processes". It recommends minimizing request/response chains. [from source] (MS-MIC p.50) (MS-MIC p.51)
- MS-CLD alternatives: Materialized View (denormalized local copy of others' data, updated via pub/sub), Service Aggregator (a microservice that centralizes the calls), and Request/Reply with queues and a correlation ID. [from source] (MS-CLD p.79) (MS-CLD p.80) (MS-CLD p.81)
- If the service needs data from another, replicate it (only the needed attributes) via events and eventual consistency instead of requesting it synchronously. [from source] (MS-MIC p.66)
- Direct HTTP calls should be minimized: they are always synchronous and couple the services; the latency of a chain is the sum of the steps. [from source] (MS-CLD p.78) (MS-CLD p.79)
- Usage rule: synchronous HTTP only from the client to the front end (gateway and first level of services); internally, asynchronous messaging. [from source] (MS-MIC p.70)

## 3. REST

- Definition and six constraints (uniform interface, separate client/server, stateless, cacheable, layered system, optional code on demand) and mapping of methods to collection and item URLs. [from source] (JMG p.21)
- Safety and idempotency: an idempotent operation produces the same effect if the same input is sent several times; a safe one does not modify the resource. JMG table: GET, OPTIONS, and HEAD are safe and idempotent; PUT and DELETE are idempotent and not safe; POST and PATCH are neither idempotent nor safe. [from source] (JMG p.21) (JMG p.22)
- JMG points out the cost of REST: lack of first-class support for discoverability and introspection; explicit contracts come with OpenAPI. [from source] (JMG p.22)
- Status codes matter and "can make or break the service"; in Spring, a request with no mapping gets 405 (with an `Allow` header), a mapped request gets 200 by default, and runtime exceptions mapped by `@ResponseStatus` produce 4xx. [from source] (REST p.27) (REST p.28)
- Content negotiation in Spring: the `Accept` header chooses the `HttpMessageConverter` for the response; `Content-Type` decides the converter for the received body; `@ResponseBody`/`@RequestBody` bind the body to the method. [from source] (REST p.35) (REST p.36)
- Spring supports REST through MVC with ModelAndView (old, verbose) and through message converters/annotations (lightweight). [from source] (REST p.20)
- DTO: the chapter covers conversion between internal entities and published DTOs, using ModelMapper. The security motivation (mass assignment) and the "mandatory separation" from the previous package are NOT in the book. [from source] (REST p.52) (REST p.53) [extrapolation] DTOs avoid exposing the entity and allow the internal model to evolve without breaking clients; mass assignment is a known risk in automatic binding.
- Error handling in Spring (from oldest to newest): `@ExceptionHandler` in the controller, `HandlerExceptionResolver`, `@ControllerAdvice` (global), and `ResponseStatusException` (Spring 5, good for prototypes). [from source] (REST p.61) (REST p.62) (REST p.67) (REST p.68)
- Discoverability and HATEOAS: the client should be able to discover actions from the response itself; in practice: `Allow` header on the 405 response, `Location` header when creating a resource, `Link` for pagination (next/prev/first/last). Spring HATEOAS provides `Link`/`ResourceSupport`/`ControllerLinkBuilder` and generates `_links`. [from source] (REST p.78) (REST p.79) (REST p.80) (REST p.86) (REST p.89) (REST p.90) (REST p.102)
- Pagination: the page is part of the representation (it is not a resource), with `page` and `size` parameters in the query string. [from source] (REST p.100) (REST p.101)
- Richardson Maturity Model (levels 0-3): MS-MIC cites it only as an additional reading link, without describing the levels. [from source] (MS-MIC p.68) The description of the four levels is general knowledge. [extrapolation]
- The "order CREATED/PAID with conditional links" example from the previous package is a pedagogical illustration with no backing in the sources. [extrapolation]
- For a POST that is safe against repetition, the sources show (a) events/commands with a unique identity for deduplication (MS-MIC: `IdentifiedCommand` with `RequestId`) and (b) the example of a duplicate payment due to retry (EDS). [from source] (MS-MIC p.165) (EDS p.127) "Idempotency-Key" as a header is industry practice. [extrapolation]
- In microservices, Swagger/OpenAPI generate client stubs. [from source] (MS-MIC p.68)

## 4. gRPC

- gRPC is a modern, high-performance RPC framework (originated at Google, a CNCF incubating project); it generates code for clients and servers from `.proto` contracts; it abstracts the plumbing across languages. [from source] (MS-CLD p.90) (MS-CLD p.91)
- Over HTTP/2: binary framing, multiplexing of parallel requests on the same connection (HTTP/1.1 processes one at a time), bidirectional full-duplex communication, native streaming, and header compression. [from source] (MS-CLD p.90)
- NUMBER FROM THE BOOK: gRPC "can be up to 8x faster than JSON serialization, with messages 60-80% smaller". The previous package said "7 to 10 times" and cited the wrong page. It is a technical-marketing claim from MS-CLD, with no methodology on the page. [from source] (MS-CLD p.91)
- Protocol Buffers: binary serialization, cross-platform IDL in `.proto` files, `protoc` compiler. [from source] (MS-CLD p.91) JMG: gRPC uses only HTTP/2 as transport; Protobuf is the IDL and format. [from source] (JMG p.24) (JMG p.25)
- When to favor gRPC: synchronous microservice-to-microservice with an immediate response, polyglot environments, low latency/high throughput, point-to-point real time with bidirectional streaming, constrained networks. [from source] (MS-CLD p.92) (MS-CLD p.93)
- Browsers do not control HTTP/2 sufficiently; gRPC-Web is used. [from source] (MS-CLD p.93) [DATED] JMG called gRPC-Web beta (JMG p.25); check the current state.
- In eShopOnContainers the aggregators talk gRPC with the backend services; "gRPC should be the first choice for direct synchronous communication between microservices", while REST remains strong for public APIs and compatibility. [from source] (MS-CLD p.93) (MS-CLD p.94) (MS-CLD p.95)
- The four modes (unary, server streaming, client streaming, bidirectional) and the name HPACK are not listed in the corpus; only "streaming" and "header compression". [extrapolation]
- NGINX gateway for gRPC: see `api-gateways-e-roteamento.md` (APIGW p.34-44).

## 5. When to use each (synthesis)

[inference] According to the sources: REST/JSON at the edge and for queries; gRPC for unavoidable internal synchronous calls; messaging/events to propagate changes between services; materialized views to eliminate synchronous queries.

## 6. Out of scope

GraphQL in depth (JMG p.23 describes principles), SOAP/WS-*, REST API versioning (the corpus only covers contract versioning in SOA p.13-15), HTTP/3.
