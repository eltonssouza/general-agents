# BAAS ch. 5: tool use, planning for LLM agents and frameworks

Source: BAAS (PDF p.132-161; printed = PDF − 25). Full reading. Versions, models and APIs cited are `[DATED]` (April/2025 or earlier): CrewAI, AutoGen, LangGraph/LangChain, GPT, Claude and Llama models.

## 1. Tool use
- **[from source]** Tool use extends the agent beyond its training knowledge. Without the tool, the model may invent an answer or admit it does not know (weather example, BAAS p.133).
- **[from source]** The book distinguishes *function calling* (structured calls to pre-defined functions in the same execution environment) from *tool calling* (interaction with external APIs and systems) and says the terms are used as synonyms (p.134). This distinction is the book's; do not treat it as an industry standard `[extrapolation]`.
- **[from source]** The LLM **does not execute** code: it generates a structured response saying which tool to use, which parameters and in what format; the **Agent Controller** (external environment) executes (p.134-135). This is the basis of any safety control over actions: whoever executes can validate (see `07-baas-confianca-seguranca-e-etica.md`).
- **[from source]** Minimum to define a tool: a description of what it does and of the expected inputs; required and optional parameters (p.135). Two forms: *docstring* in frameworks (p.136) and JSON schema when using the model API directly, with fields name, description and `input_schema` (p.137). The format depends on the model; that is why frameworks that abstract the definition are preferred (p.137).
- **[from source]** Not every LLM is good at *tool calling*; the book cites models trained for it `[DATED]` (p.136).

### Tool types (p.138)
APIs, database tools, utility functions, integration tools and hardware interfaces.

### Design considerations (p.139)
- **[from source]** Composition and chaining; tool selection (capability, reliability, performance, cost); error handling and *fallbacks*; tool state management; updating and versioning; security and access control (credentials, authorization, secure channels), respecting rate limits and quotas (p.139).
- **[from source]** The Rome example with CrewAI (p.139-141) is a simulation, not a real integration; the book itself warns about this (p.141).

### Reasoning about tools (p.151-153)
- **[from source]** The reasoning behind tool choice is largely done by the LLM itself, from the descriptions; therefore clear descriptions are the main point (p.151-152).
- **[from source]** Smaller models or models without tool-use training may: fail to notice when to use the tool, assume wrong capabilities, use the wrong sequence, miss opportunities to use it or ignore constraints. Even capable models struggle with multi-step combinations, selection inconsistency, tools with similar functionality and error recovery (p.152). The book recommends **testing tool-use patterns before deployment** (p.152).

## 2. Planning for LLM agents
- **[from source]** The book's classification by practicality for LLM agents (p.142): least practical = STRIPS, A*, GraphPlan and MCTS (p.142-143: binary logical states, costs hard to define in language, combinatorial explosion, and each MCTS simulation would require real LLM calls, which would be expensive); moderate = Fast Forward, with "relaxed" adaptation by LLM (p.143-144); most practical = **LLM-based planning** (p.145-147) and **HTN** (p.147-150).
- **[from source]** Cautions with LLM planning: optimistic or impractical plans if there are no constraints, and difficulty with hard numeric or temporal constraints if they are not handled explicitly (p.147).
- **[from source]** HTN in CrewAI: hierarchical process with a *manager* (agent or LLM); with an LLM manager the plan is arbitrary and less controllable, suitable for simple flows (p.148). Without access to tools the system produces a "completely fictitious" plan (p.150).
- **[from source]** Integration: the plan only becomes factual with tools (p.151). The planning flow for tool use: understand the goal, choose tools and their order, incorporate tools into the plan and adjust to new information (p.153-154).

## 3. Frameworks (p.154-159) `[DATED]`
| Aspect | LangGraph | CrewAI | AutoGen | Page |
|---|---|---|---|---|
| State | explicit state management, with *checkpointer* (`MemorySaver`) and `thread_id` | through agent instances and task context | group chat message history | p.158-159 |
| Tools | dedicated tool node | `@tool` decorator and direct association with the agent | associated directly with each agent | p.154-157, 159 |
| Flow | graph of nodes and conditional edges | hierarchical or sequential decomposition | turn-taking (*round robin*) with a text termination condition (`TERMINATE`) | p.155-159 |

- **[from source]** The book's selection criteria: workflow complexity, need for state management, multi-agent collaboration and development complexity; CrewAI is the most direct, AutoGen is strong in multi-agent interaction, LangGraph gives robust flow control with more configuration (p.160). This comparison is based on the book's implementations (p.159).
- `[DATED]` Do not use this section to choose a framework today: APIs and class names change. Check the current documentation.

## 4. What the chapter does not cover
- **[from source]** There is no section on standardized tool protocols, nor on limits to the number of tools, nor on injection via tool results. For limits on the size of the tool set and description design, see the CE2 paper in `11-ce2-uso-praticas-e-desafios.md` (p.18-19); this is a complement from **another source**, not from ch. 5.
