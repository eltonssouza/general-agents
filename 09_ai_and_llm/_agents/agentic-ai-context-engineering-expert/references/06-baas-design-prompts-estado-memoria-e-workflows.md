# BAAS ch. 7: focused prompts, state and environment, memory and context management, sequential and parallel workflows

Source: BAAS (PDF p.186-211; printed = PDF − 25). Full reading. This is the book's chapter closest to "context engineering", but the book **does not use that term** nor "context window"; it uses "context management" (p.177-179). The chapter's example code is illustrative, not a library.

**Note an internal discrepancy in the book:** the preface (p.21) and the opening of ch. 8 (p.214) say that ch. 7 deals with *guardrails*, constraints and the balance between autonomy and control. The actual text of ch. 7 (p.186-211) **has no dedicated section** on this: it covers prompts/instructions, state space and environment, memory and context, and workflows. The content on action limits is in ch. 9 (p.237-240). See `07-baas-confianca-seguranca-e-etica.md`.

## 1. Focused instructions and system prompts (BAAS p.187-192)
- **[from source]** A focused instruction defines objective, constraints and operational context; clarity and explicitness strongly influence performance (p.187).
- **[from source]** Clear objectives give an evaluation reference; in the example, metrics such as customer satisfaction, query resolution and plan quality (p.187). Example prompt with blocks *Objective*, *Core functions*, *Constraints* and *Behavior* (p.187-188).
- **[from source]** Task specification: steps, expected outputs and potential challenges (p.188-189), with a flight query example (p.190).
- **[from source]** Contextual awareness in global and local layers (international restrictions, weather, hotel policies) (p.190-191; figure 7.1 on p.191 was not inspected); examples: destination intelligence, dynamic adaptation, cultural competence (p.191).

## 2. State space (p.192-193)
- **[from source]** The state space defines how the agent maintains and updates its understanding of the situation, available actions and outcomes. Three groups in the example: customer profile state, travel context state and booking state (p.192-193). The state must capture static and dynamic elements while maintaining efficiency (p.193).
- **[from source]** Example state in JSON: `booking_id`, `status`, components (flights and hotels, each with status, cancellation deadline and dependencies) and customer preferences (p.193).

## 3. Environment modeling (p.194-195)
- **[from source]** Three questions: which systems and services does the agent interact with? which rules and constraints govern? which changing conditions to monitor? (p.194).
- **[from source]** **Static** elements: business rules (booking, payment, cancellation policies, SLAs, regulatory compliance) and interfaces (endpoints, database schemas, authentication, error handling, rate limits and quotas) (p.194-195). **Dynamic** elements: resource availability (inventory, prices, outages, weather) and system performance (latency, errors, resource usage, queues, health) (p.195).
- **[from source]** Many integration points make the system complex; the mitigation indicated is to use **several specific agents**, each good at one or two tasks, that coordinate with each other (p.195).

## 4. Integration and interaction patterns (p.196-198)
- **[from source]** **Event-driven updates** (instead of *polling*): events such as `FLIGHT_CHANGE` and `WEATHER_ALERT` trigger dependency checks, notification and reassessment (p.196).
- **[from source]** **State and consistency validation**: validate transitions (for example "pending" → "confirmed" requires payment received, seats available and valid price), dependencies (hotel after flight arrival) and business rules (passport, insurance, cancellation policy); if any validation fails, the state change is blocked with an error (p.197-198).
- **[from source]** Monitoring and adaptation (p.198): state update latency, decision accuracy, resource utilization, error rates and recovery time, and customer satisfaction; adapt allocation, rules and parameters (p.198).
- **[inference]** State transition validation is, in practice, an action control (a barrier before a side effect), even though the book presents it as booking integrity.

## 5. Memory architecture and context management (p.198-204)
**Three memory types (p.198-202)**
| Type | Role according to the book | Book's implementation example | Page |
|---|---|---|---|
| Short-term (working) | immediate workspace; conversation context; erased at the end of the session | class with `current_interaction`, `update_context`, `clear_session` | p.199 |
| Long-term (knowledge base) | persistent repository across sessions: profiles, history, knowledge of destinations and regulations | customer profile and travel knowledge classes | p.200-201 |
| Episodic (interaction history) | discrete episodes with temporal order and outcomes, to learn patterns | `record_interaction` with *timestamp* and `retrieve_relevant_episodes` | p.201-202 |

- **[from source]** The book states that episodic memory "emerged" especially for conversational interfaces (p.201).
- **[from source]** Context hierarchy: **global** (system settings and alerts), **session** (interaction state, active searches, temporary preferences) and **task** (booking details, current step, dependencies) (p.202-203). Book example: business trip with a corporate policy limiting flights to US$ 2,000 (p.202).
- **[from source]** Context switching: **preservation** (saving state and change history), **restoration** and **merging** (combining contexts and resolving conflicts) (p.203).
- **[from source]** Integration with decision-making: information retrieval (history, similar cases, matching with current context, filtering and prioritization), pattern recognition and decision optimization with weighted evaluation, constraints and risk mitigation (p.204).
- **[inference]** The book does **not** cover token limits, compression, summarization, similarity-based relevance, nor the cost of memory. Those topics are in the CE2 paper (`10-ce2-coleta-e-gestao-de-contexto.md`).

## 6. Sequential and parallel workflows (p.205-209)
- **[from source]** Sequential when there is dependency (flight before hotel; payment: verify funds, process, confirm, send documents) (p.205). Parallel for independent tasks (querying several airlines, weather, advisories) and background processing (updating profile, monitoring prices) (p.206).
- **[from source]** Workflow optimization (p.207-209): dependency analysis (critical path), priority (urgency, SLAs), resource management (CPU/memory, throttling, connections and caches; rate limits and quotas of external APIs, retry strategies), dynamic adjustment (load balancing, queues, *backpressure*) and monitoring (times, success, throughput, latency).
- **[from source]** Questions and answers (p.209-211): factors for choosing sequential × parallel: dependencies, resources, time constraints, system load and performance requirements (p.211).

## 7. Derived practical rules (label)
- **[inference]** In the system prompt, separate what is persistent (role, limits, protocols, p.179-180) from what is session and task scoped (p.202-203).
- **[inference]** Model task state explicitly (JSON as on p.193) and validate transitions before carrying out actions (p.197).
- **[extrapolation]** Long-term memory with personal data requires retention policies and access control; the book addresses privacy in ch. 9, not in memory.
