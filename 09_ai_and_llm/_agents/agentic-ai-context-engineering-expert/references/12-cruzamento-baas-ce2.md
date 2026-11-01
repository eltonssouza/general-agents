# BAAS × CE2 cross-analysis (package synthesis)

**All the content of this file is `[inference]`** by the package: the two texts do not cite each other and use different vocabulary. Each line points to the page on each side so the reader can check.

About the sources: BAAS (Packt, Apr/2025) is a textbook on **agent architecture** with code examples and the recurring case of a travel agent; CE2 (arXiv, Oct/2025) is a conceptual paper on **context** (definition, eras, collection/management/use). Both are `[DATED]` regarding tools and products.

## 1. Concept map
| Topic | BAAS | CE2 | Observation |
|---|---|---|---|
| Short-term memory | working memory, erased at the end of the session (p.199) | `Ms`: context with high temporal relevance above a threshold (p.12) | BAAS gives a class example; CE2 gives a definition with a threshold, without values |
| Long-term memory | persistent knowledge base (p.200-201) | `Ml`: abstracted subset with high importance (p.12) | CE2 adds abstraction ("self-baking", p.13) |
| Episodic memory | interaction as episodes, with `retrieve_relevant_episodes` (p.201-202) | "episodic buffers" cited as a possible layer (p.12) | CE2 does not develop it |
| Context hierarchy | global / session / task (p.202-203) | layers by time and importance (p.12); isolation by subagent (p.12) | different axes: scope (BAAS) × time and function (CE2) |
| System prompt | persistent: role, limits, protocols, decision (p.179-180) | characterizing information of the application, e.g. system instructions (p.4-5) | BAAS is prescriptive; CE2 only includes it in the inventory |
| Tool description | description + required/optional parameters (p.135-137) | precise descriptions, without overlap; few items (p.18) | CE2 brings the empirical limit of 30/100 `[DATED]` |
| Messages between agents | format with type, sender, recipient, content (p.180-181) | structured messages or shared memory (p.14-15) | same pattern in two vocabularies |
| Delegation | coordinator → delegator → workers (p.164-168) | leader assigns with goal, output, tools and limits (p.19); isolated subagent (p.12) | CE2 details the content of the delegation |
| Task state | JSON object with dependencies (p.193) | state objects with schema and lightweight references (p.13) | CE2 ties this to token economy |
| Learning from experience | reflection, persisted feedback (p.113-114, 121-123) | abstraction/self-baking (p.13) | BAAS uses weights and feedback; CE2 uses context consolidation |
| Monitoring and evaluation | product metrics (p.115), decision metrics (p.238), action-chain tests (p.239) | difficulty evaluating memories (p.18) | neither offers a benchmark |
| Safety and limits | action limits, verification, rollback, HITL (p.237-240) | only minimum permissions per subagent and secure storage (p.10, 12) | safety is almost only in BAAS |
| Cost and latency | cost in prose, no numbers (p.116) | KV cache, window occupancy, tool set size (p.16, 18) | context and cost are almost only in CE2 |
| Definition of context | context management as hierarchy and switching (p.177-179) | formal definition of context and of context engineering (p.4-5) | BAAS does not use the term "context engineering" |

## 2. Divergences and silences
- **[inference]** BAAS treats memory as a functional component of the agent; CE2 treats it as a problem of **selection and compression under a window limit**. BAAS does not speak of token limits; CE2 does not speak of guardrails.
- **[inference]** Neither offers standardized metrics, benchmarks or comparative results of agent architectures or memory strategies; avoid claiming "the book shows that X is better than Y".
- **[inference]** BAAS describes ch. 7 as covering guardrails (p.21, 214), but the text of ch. 7 does not (see `06-baas-design-prompts-estado-memoria-e-workflows.md`); for action limits use ch. 9.

## 3. A design flow that uses both sources (package proposal)
1. Choose the architecture and the decomposition (BAAS p.65, 164-168).
2. List the agent's context by category (Char: user, application, environment, tools, memory, model; CE2 p.4-5) and decide what is persistent, session and task scoped (BAAS p.202-203).
3. Define small, well-described tools (BAAS p.135-139; CE2 p.18-19).
4. Plan the context budget and the selection and compression policy (CE2 p.12-16) with `ctx_calc.py budget`.
5. Define action limits, verification and rollback (BAAS p.237-240) and the action-chain test plan (BAAS p.239).
6. Define monitoring (BAAS p.198, 238) and acknowledge the evaluation gap (CE2 p.18).
`agent_spec.py` materializes this flow in a specification template.
