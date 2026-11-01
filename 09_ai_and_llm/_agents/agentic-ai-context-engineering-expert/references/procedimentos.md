# Procedures (P1-P10): how the agent reasons and what each step supports

Each step carries its origin: `[from source]` (BAAS), `[from source]` (CE2), `[inference]` (package organization) or `[extrapolation]`. Pages = PDF. The procedures are **the package's**; the individual ideas come from the texts on the cited pages.

## P1. Choose an agent's architecture
1. Classify the task by complexity, environment uncertainty and need for real-time response `[from source]` (BAAS p.65).
2. Task with reasoning and planning in a well-defined environment → deliberative; fast reaction under uncertainty → reactive; both → hybrid with layers `[from source]` (BAAS p.61-65).
3. If the task calls for several competencies or many integrations, split into specific agents that coordinate `[from source]` (BAAS p.195).
4. For LLM agents, map the deliberative loop to "plan → call tool → observe" `[inference]`.

## P2. Specify an agent (use `agent_spec.py`)
1. Role, goal and (if using a CrewAI-type framework) *backstory* `[from source]` (BAAS p.168-169).
2. System prompt with role and scope, constraints, communication protocols and decision framework `[from source]` (BAAS p.179-180). Objective, functions, constraints and behavior in the format of the example `[from source]` (BAAS p.187-188).
3. Tasks: steps, expected outputs and potential challenges `[from source]` (BAAS p.188-190).
4. Task state and environment: accessible systems, rules and changing conditions `[from source]` (BAAS p.192-195).
5. Tools (P3), memory and context (P4), action limits (P7), evaluation (P8).
6. Context inventory by category (user, application, environment, tools, memory, model service) `[from source]` (CE2 p.4-5).

## P3. Define tools
1. Clear description of what it does, required and optional parameters, expected return `[from source]` (BAAS p.135-136).
2. In direct API use, JSON schema with name, description and `input_schema`; format depends on the model `[from source]` (BAAS p.137).
3. Precise, non-overlapping descriptions; avoid large sets (report: drop above 30 and near-certain failure above 100 for DeepSeek-v3 `[DATED]`, `[from source]`, CE2 p.18).
4. Plan for error, *fallback*, tool state, version, credentials, rate limits `[from source]` (BAAS p.139).
5. The LLM only emits the call; the executor validates and executes `[from source]` (BAAS p.134-135), the natural point to check parameters and permissions `[inference]`.
6. Test tool use before deployment, especially on smaller models `[from source]` (BAAS p.152).

## P4. Design memory and context
1. Separate what is persistent (system prompt), session and task scoped `[from source]` (BAAS p.202-203) and what is long-term, short-term and episodic `[from source]` (BAAS p.199-202).
2. Apply Minimal Sufficiency and Semantic Continuity to what you collect and store `[from source]` (CE2 p.9).
3. Tiered storage by use (cache, embedded database, secure, cloud) `[from source]` (CE2 p.10).
4. Choose the form of abstraction: summaries, schema, vectors or hierarchy, weighing the limitation of each `[from source]` (CE2 p.13-14).
5. Define selection (semantic relevance, logical dependency, recency/frequency, overlap, preference) `[from source]` (CE2 p.16) and when to transfer short → long-term (`ctx_calc.py memory-split`, rule from CE2 p.12).
6. Large outputs outside the window with lightweight references `[from source]` (CE2 p.13).
7. Context switching: preserve, restore, merge `[from source]` (BAAS p.203).

## P5. Budget the context (use `ctx_calc.py budget`)
1. List the components: system prompt, tool definitions, retrieved memory, history, retrieved documents, draft/plan, reserved output. The four context sources cited by the paper: *scratchpad*, memory, tool definitions and RAG `[from source]` (CE2 p.16); the rest of the list is `[inference]`.
2. Provide tokens per component (measured by you; the script does not tokenize).
3. Compare occupancy with a **user threshold**. The 50% threshold comes from an observation about code agents cited by the paper `[DATED]` (CE2 p.16); use it as an alert, not as a rule.
4. Count tools and compare with 30 and 100 (CE2 p.18 report, `[DATED]`, specific to DeepSeek-v3).
5. Check prefix stability and cache (practices from CE2 p.18); costs only with prices that **you** provide `[extrapolation]`.

## P6. Decompose a multi-agent system
1. Define coordinator, delegator and workers and the information flow in both directions `[from source]` (BAAS p.164-165).
2. Each subtask with goal, expected output, tool guidance and limits `[from source]` (CE2 p.19).
3. Consistent message protocol and output format `[from source]` (BAAS p.180-181); context sharing mechanism `[from source]` (CE2 p.14-15).
4. Conflict rule: mediation by the delegator, final decision by the coordinator by predefined criteria `[from source]` (BAAS p.177-178).
5. Isolate context and permissions per subagent `[from source]` (CE2 p.12).

## P7. Define action limits and oversight
1. Action limits by risk: finances, destinations, when changes can be autonomous `[from source]` (BAAS p.237, 238-239).
2. Verification before effect (multi-step, constraints) and human approval above thresholds `[from source]` (BAAS p.237-239).
3. Action logging and reversal capability, respecting real-world constraints (cancellation policies) `[from source]` (BAAS p.237-239).
4. Progressive autonomy and emergency protocols `[from source]` (BAAS p.240).
5. State transition validation before carrying out `[from source]` (BAAS p.197-198).

## P8. Test and monitor
1. Test decision chains and action sequences in simulated scenarios, not only the output `[from source]` (BAAS p.239).
2. Product metrics (acceptance, complaints, engagement) and decision metrics (consistency, risk) `[from source]` (BAAS p.115, 238).
3. Monitor state latency, errors and recovery, utilization and satisfaction `[from source]` (BAAS p.198).
4. Acknowledge that memory benchmarks test only retrieval and that contradiction checks and tracing are lacking `[from source]` (CE2 p.18).

## P9. Review an existing agent (use `agent_checklist.py`)
1. Answer the items by area. 2. An item answered "no" or "don't know" becomes a finding with the page that supports it. 3. Separate findings by origin (book, paper, inference). 4. Say what the collection does not cover (detailed operational security, quantitative evaluation, tool protocols).

## P10. Share context between agents or systems
1. Within the system: embedded prompt, structured messages or shared memory (blackboard, graph) `[from source]` (CE2 p.14-15).
2. Across systems: adapters, or shared representation (JSON/API, natural-language summary, vectors), weighing precision, flexibility and interpretability `[from source]` (CE2 p.15).
