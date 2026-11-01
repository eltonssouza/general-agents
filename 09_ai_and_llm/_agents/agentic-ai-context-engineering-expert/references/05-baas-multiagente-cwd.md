# BAAS ch. 6 (and MAS from ch. 2): multi-agent orchestration, CWD model, roles and communication

Source: BAAS (PDF p.162-184; basic MAS on p.65-73; printed = PDF − 25). Full reading. "CWD" (coordinator-worker-delegator) is a model **proposed by the book**; do not treat it as an industry standard `[extrapolation]`. Frameworks and examples are `[DATED]`.

## 1. The CWD model (BAAS p.163-165)
- **[from source]** Three roles: **coordinator** manages tasks, resources and overall flow (prioritizes by urgency, availability and dependencies, monitors, readjusts); **worker** executes specialized tasks; **delegator** bridges coordinator and workers, assigns load according to availability and balances throughput, latency and resource utilization (p.164).
- **[from source]** Four principles (p.165): separation of responsibilities (strategic planning, resource management, execution); hierarchical organization (top, middle, bottom); bidirectional information flow (downward: assignments, priorities, constraints; upward: progress, results, resource usage); adaptability and resilience (dynamic resource allocation, fault tolerance through redundancy, load balancing, role reassignment at runtime).
- **[from source]** Travel agent example (p.166-168): the coordinator decomposes the request; the delegator evaluates workers, assigns and monitors; the flight, hotel, activities and transport workers deliver to the delegator, which consolidates; the coordinator reviews and presents (nine steps, p.167-168).

## 2. Roles and agent definition (p.168-176)
- **[from source]** In CrewAI, an agent is defined by `role`, `goal` and `backstory`. The book states that the `backstory` is **merged into the system prompt** of the LLM together with the `role`, and that it is specific to CrewAI (p.169); the definition by `role`, `goal` and `backstory` is presented on p.168.
- **[from source]** Typical roles: Manager (synonym of coordinator), Analyst, Reflector, Searcher (all workers), Task Interpreter (synonym of delegator) (p.169-170). The book cites Kazík (2010) on roles in MAS (p.170) and the principles of role-based modeling: separating interaction logic from internal logic, dynamic role assignment and modular organization (p.171).
- **[from source]** Flow with parallelism (p.175-176): the coordinator makes the strategic plan; the delegator splits work between "core" workers (flight, hotel, activities, transport) and analysis workers (data analyst, reflector, searcher) in parallel; the outputs return to the delegator and the coordinator.
- **[inference]** Backstories with years of experience and numbers (p.171-174) are a *prompting* device of the example; the book does not show that these "credentials" improve decisions. Do not cite them as evidence.

## 3. Communication, coordination, negotiation and knowledge (p.176-178)
- **[from source]** Well-defined protocols, with message format and interaction patterns; the book cites FIPA ACL as an example of a protocol (p.177).
- **[from source]** Coordination through task prioritization, resource allocation and progress monitoring (p.177).
- **[from source]** Conflicts: the delegator can mediate and propose alternatives; if there is no agreement, the coordinator decides by predefined criteria (p.177-178).
- **[from source]** Knowledge sharing among agents (for example, insights from the analyst to the others) (p.178).

## 4. Implementation in generative systems (p.179-182)
- **[from source]** In traditional MAS, behaviors are programmed; in LLM-based systems they are controlled mainly by **prompts and interaction patterns** (p.179).
- **[from source]** The system prompt is the persistent configuration layer and should contain: role and scope definition, constraints and operational limits, communication protocols and the role's decision framework (p.179-180).
- **[from source]** Instruction formatting (p.180-181): structured input (for example `task_type` and `parameters`), output templates (for example `status` and `result` with `options`, `recommendations` and `constraints`) and messages with `message_type`, `sender`, `recipient` and `content`.
- **[from source]** Interaction patterns: message passing (with *handoff* and error recovery), state management (tracking progress and coordinating parallelism) and feedback loops (p.181-182).

## 5. MAS in ch. 2 (cross summary)
Characteristics and interaction mechanisms (cooperation, coordination, negotiation) are in `01-baas-fundamentos-e-arquiteturas.md` §3 (p.67-70).

## 6. Complement from another source: context in multi-agent systems
The CE2 paper covers how each agent **shares context** (prompt, structured messages, shared memory, *blackboard*, graph), the use of subagents with an isolated window and the delegation rule with goal, output, tools and limits (CE2 p.12, 14-15, 19). See `10-ce2-coleta-e-gestao-de-contexto.md` and `11-ce2-uso-praticas-e-desafios.md`. The cross-analysis is in `12-cruzamento-baas-ce2.md` and is `[inference]`.

## 7. Gaps
- **[from source]** Ch. 6 offers no experimental evaluation, nor token cost or latency of the exchanges between agents, nor failure modes of the coordinator. `[extrapolation]` More agents increase calls and error surface; the book does not quantify it.
