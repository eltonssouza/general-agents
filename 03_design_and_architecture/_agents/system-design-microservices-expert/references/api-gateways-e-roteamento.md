# API Gateways, BFF, and routing

Sources: MS-MIC, MS-CLD, JMG, SOA, SDH, and APIGW (which is Liam Crilly/F5's e-book, "Deploying NGINX as an API Gateway", 2021 — the previous package called it a "whitepaper"). Pages = PDF. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Why a gateway

- Direct client-to-microservice communication may serve small apps, but in large apps (dozens of services, mobile/SPA clients) it causes: client coupling to the internal decomposition, many round trips (latency), a larger attack surface, and cross-cutting concerns (authorization, SSL) repeated in every service. [from source] (MS-MIC p.55) (MS-MIC p.56) (MS-MIC p.57)
- MS-CLD lists the same problems: client subject to back-end refactorings, larger surface, duplicated concerns, and complex client code; it recommends an API Gateway between the front end and the services. [from source] (MS-CLD p.70) (MS-CLD p.71)
- JMG: the typical client would need to know dozens of endpoints; the service registry should not be public; the gateway reduces round-trips (costly on mobile networks and paid per call in the cloud). [from source] (JMG p.115)
- SOA describes an "API layer" (facade) in microservices that abstracts the location and granularity of services, with some intelligence/orchestration that can be refactored over time. [from source] (SOA p.40)

## 2. The API Gateway pattern

- MS-MIC definition: a service that offers a single entry point for groups of microservices, similar to the Facade; also called "backend for frontend" when designed for the needs of the client app; it acts as a reverse proxy and can offer authentication, SSL termination, and caching. [from source] (MS-MIC p.57)
- Core features (MS-MIC): reverse proxy/routing (layer 7, usually HTTP), request aggregation (reduces client-backend chatter; more useful for remote clients), and offloading of cross-cutting concerns (authentication/authorization, service discovery integration, cache, retry/circuit breaker/QoS, rate limiting/throttling, load balancing, logging/tracing/correlation, header/claims transformation, IP allowlisting). [from source] (MS-MIC p.59) (MS-MIC p.60)
- In MS-CLD the gateway acts as a reverse proxy, insulates the client from the internal partitioning, and is the first line of defense for identity, caching, resilience, metering, and throttling; it must be simple and fast, with no business logic, otherwise it becomes a bottleneck and a "monolith". [from source] (MS-CLD p.71)
- JMG definition: a server that acts as an API front end, applies throttling and security policies, routes and can transform/orchestrate requests, collect metrics, and cache. [from source] (JMG p.115)
- Modernization: the gateway between clients and a monolithic API allows new services to be added without clients noticing. [from source] (MS-MIC p.59)
- Example of path-based routing in NGINX (`/api/warehouse/inventory` and `/pricing` to distinct backends) and grouping of upstreams. [from source] (APIGW p.9) (APIGW p.12) (APIGW p.13)
- Aggregation ("fan-out") and "SSL termination at the gateway" are product features; TLS termination appears, for example, as a function of an ADC/Application Gateway that relieves the hosts' CPU. [from source] (MS-MIC p.55) (MS-CLD p.73)

## 3. Backend for Frontend (BFF)

- A single gateway serving several client types tends to bloat and become a monolith; MS-MIC recommends splitting into several smaller gateways, by client type (and, on a second axis, by business boundary), and not having a single gateway aggregating all microservices. [from source] (MS-MIC p.58) (MS-MIC p.59)
- Each gateway can offer a tailored API (e.g., mobile vs. web); MS-CLD justifies this by the differences in capability of each device. [from source] (MS-CLD p.71) (MS-CLD p.72)
- JMG: BFF optimizes for a specific platform, but "can drift into the danger zone"; GraphQL can serve as a BFF. [from source] (JMG p.119) (JMG p.120)
- Contractual quotas, public/partner API, and "standardized" OpenAPI as a third type of BFF (text from the previous package) are NOT in the sources. [extrapolation]

## 4. Risks and criticisms

- MS-MIC: gateway coupling with the internal services ("the new ESB", citing Clemens Vasters), single point of failure, additional latency (generally lower than that of a chatty client), bottleneck if it does not scale, development/maintenance cost if it has custom logic, team bottleneck if a single team maintains it. [from source] (MS-MIC p.62) (MS-MIC p.63)
- JMG ("On the Dark Side"): vendors add features and the gateway becomes middleware with business logic and orchestration, hard to test and with single points of control; it cites ThoughtWorks' Technology Radar. [from source] (JMG p.120)
- [inference] The three sources converge: keep the gateway thin, with no business rules, and split it by client/domain.

## 5. NGINX as a gateway (APIGW)

- Three ways of use: native NGINX functionality, extension with Lua (OpenResty), and stand-alone third-party gateways. Two recommendations: pay attention to performance/latency and a "converged approach" (web and API traffic on the same NGINX). [from source] (APIGW p.4)
- NUMBER FROM THE BOOK: "our own tests for simple Lua scripts show performance drops of 50% to 90%" — this is an F5/NGINX measurement for simple scripts, cited as a warning to validate peak performance, not a general law. [from source] (APIGW p.4)
- Use-case table: protocols (REST, gRPC, HTTP/2...), routing by host/URL/parameters, rewriting of legacy requests, rate limiting by multiple criteria, authentication (JWT, API keys, OpenID Connect), service discovery, and blue-green (NGINX Plus). [from source] (APIGW p.6)
- Rate limiting in NGINX: `limit_req_zone` defines zones (by IP and by API key) and `limit_req` applies them; by default the excess gets 503 and `limit_req_status` can switch it to 429. The text on p.22 speaks of 10 req/s per IP while the code shows `rate=1r/s` (the source is inconsistent; the zone name suggests 10). [from source] (APIGW p.22) (APIGW p.23)
- Request body limit: NGINX rejects bodies above 1 MB by default; the example uses `client_max_body_size 16k`. [from source] (APIGW p.29)
- API key authentication via `auth_request` and JWT (`auth_jwt`); JSON body validation via the NGINX JavaScript module. [from source] (APIGW p.18) (APIGW p.19) (APIGW p.28) (APIGW p.30)
- Rejecting invalid paths with 400 instead of 404 is optional and requires clients that follow the documentation. [from source] (APIGW p.17)
- gRPC: NGINX as a gRPC gateway (port 50051, gRPC metadata as HTTP/2 headers, active health checks on the upstreams). [from source] (APIGW p.34) (APIGW p.38) (APIGW p.42) (APIGW p.43)

## 6. Load balancing and discovery

- Algorithms listed in SDH: Round Robin, Weighted Round Robin, Least Connections, Least Response Time, IP Hash. [from source] (SDH p.10) "Consistent Hashing" is NOT listed as an LB algorithm in SDH; consistent hashing appears as a technique for data distribution in a cluster (SDH p.18).
- L4 vs. L7: the corpus only describes L7 — "routing based on the actual content of an HTTP message, not just low-level TCP packets" (MS-CLD) and "layer 7 routing, usually HTTP" (MS-MIC). [from source] (MS-CLD p.73) (MS-MIC p.59) The detail on L4 (IP/port, without inspecting content, less CPU) is general knowledge. [extrapolation]
- Forward vs. reverse proxy: short definitions. [from source] (SDH p.21)
- Service discovery: a mechanism for services to locate each other dynamically via a registry. [from source] (SDH p.24) JMG discusses options (Eureka, ZooKeeper, etcd, Consul). [from source] (JMG p.110) (JMG p.111) (JMG p.112) [DATED] The tools in that chapter (Netflix OSS: Eureka, Zuul 2; Spring Cloud) reflect the Java ecosystem around 2018-2019; check the current state of each one.
- Service mesh (sidecar) assumes service discovery, load balancing by observed latency, retry, and metrics, taking this out of the services' code. [from source] (MS-CLD p.95) (MS-CLD p.96) (MS-CLD p.134)
- Heartbeats to detect failures: [from source] (SDH p.22).

## 7. Out of scope

Detailed configuration of Kong/Envoy/Traefik, WAF, end-to-end OAuth2 (MS-MIC has a security chapter, outside the focus of this package), GraphQL Federation (only mentioned in MS-MIC p.47).
