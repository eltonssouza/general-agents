# CE2 §6-9: use of context, emerging practices, applications, challenges

Source: CE2 (p.14-21; PDF page = printed). Full reading. `[DATED]` (Oct/2025). The numbers and practices come from **blogs and engineering reports cited by the paper** (Manus, Anthropic, Osmani, Dbreunig etc.), not from the paper's own experiments; treat them as dated, scoped heuristics, not laws.

## 1. Context sharing within a system (CE2 p.14-15)
- **[from source]** In multi-agent systems, a practical reason they work is that they allow consuming more tokens than a single agent could handle (p.14). Shared information must be precise, easy to interpret and directly usable in the next step (p.14).
- **[from source]** Three patterns (p.14-15): (a) **embed previous context in the prompt** of the next agent, often reformatted (AutoGPT, ChatDev); (b) **exchange structured messages** with a schema (task type, input data, results, reasoning steps) (Letta, MemOS); (c) **shared memory** for indirect communication, in blocks with metadata on who wrote, when and type, or organized as a *blackboard* by segments or as a **graph** (TME, G-Memory) (p.15).
- **[inference]** Compare with BAAS p.180-181: the book's message format (`message_type`, `sender`, `recipient`, `content`) corresponds to pattern (b).

## 2. Sharing across systems (p.15)
- **[from source]** At system boundaries the challenge is making context interpretable. Two approaches: **adapters** (one converter per connection; gives freedom, but one must be built per pair) and **shared representation**: a common data format or API (JSON), human-readable summaries in natural language, or semantic vectors. Trade-offs: schemas give precision but require strict coordination; natural language is flexible but hard to *parse* reliably; vectors are compact but poorly interpretable (p.15).
- **[from source]** The body text does **not** describe the *Model Context Protocol*; it appears only in the bibliographic notes (CE2 p.22, 25, 26). Do not attribute an MCP analysis to the paper.

## 3. Context selection for understanding (p.15-17)
- **[from source]** Even with long windows, LLMs are limited by the **quality** of the input tokens; irrelevant fragments distract reasoning and raise cost (p.16). Observation cited: the performance of coding agents tends to drop when the window exceeds about 50% occupancy (source: Osmani, 2025), suggesting that both excess and lack of context hurt `[DATED]` (p.16). Selection is described as "attention before attention" (p.16).
- **[from source]** Five selection factors (p.16): **semantic relevance** (vector search for near neighbors), **logical dependency** (dependency graph between steps, the MEM1 case), **recency and frequency**, **overlapping information** (discard or merge redundancies, actively) and **user preference and feedback**.
- **[from source]** Filtering strategies in RAG pipelines (p.16-17): segmentation (by fixed windows or by AST, respecting functions, classes and modules), semantic retrieval (embeddings), non-semantic (grep, by regex) and structured (knowledge and call graphs), and **reranking** (sometimes by LLM) with a trade-off between precision and efficiency.
- **[extrapolation]** The 50% threshold is specific to code agents in the cited source; do not generalize. The script `ctx_calc.py budget` uses it as a **configurable alert**, with the `[DATED]` label.

## 4. Proactive inference of needs (p.17)
- **[from source]** Today the use of context is mostly reactive; the paper proposes agents that infer latent needs: learn preferences (history, notes, indirect signals, direct questions), infer hidden goals from sequences of questions, and offer help when the user seems stuck (p.17). It is a research direction, without evaluation.

## 5. Lifelong context and four challenges (p.17-18)
- **[from source]** Four challenges (p.17-18): (I) **storage bottlenecks** (retaining as much as possible under resource constraints, with high compression, precise retrieval and low latency); (II) **processing degradation** (global attention O(n²) raises latency and memory; attention "gets thinner" and reasoning worsens; retrieval overloaded by similar and irrelevant items; conflicts between retrieved passages); (III) **system instability** (small errors propagate with accumulated memory); (IV) **evaluation difficulty** (benchmarks test only retrieval, not whether the information is still relevant, correct or useful; checking for contradictions, undoing wrong updates and tracing reasoning are lacking) (p.18).
- **[from source]** Vision: a "semantic operating system" for context, with active addition, modification and forgetting, new architectures and the ability to explain and correct reasoning steps (p.18). It is aspirational.

## 6. Emerging engineering practices (p.18-19, main source: Manus report, 2025)
- **[from source]** **KV cache** (p.18): storing attention keys and values of past tokens reduces recomputation; the hit rate affects latency and cost. Practices: keep a **stable prompt prefix** (variations such as a timestamp at the start invalidate the cache), **append-only and deterministic** updates, insert cache *checkpoints* manually when the server does not do incremental prefix caching, and use *warm-up* by predictive loading (p.18).
- **[from source]** **Tool design** (p.18-19): precise descriptions, without overlap; models can refine descriptions. Scale: large tool sets reduce reliability; loading tools dynamically breaks cache consistency. Report cited: for DeepSeek-v3 performance dropped above 30 tools and nearly always failed above 100 `[DATED]` (p.18). Alternative: stable tool list and constraint at the decoding level, masking logits (p.18-19).
- **[from source]** **Context content** (p.19): keeping errors visible lets the model learn; in agents, *few-shot* with very similar action-observation pairs makes the model repeat patterns, and Manus introduces small structured variations to break the repetition.
- **[from source]** **Multi-agent** (p.19, Claude's experience): the lead agent decomposes the query and assigns subtasks with **goal, output, tool guidance and limits**; vague instructions cause confusion; since agents misjudge workload, the prompt includes effort-scaling rules (simple query = 1 agent, hard = more); search from broad to focused; extended thinking mode improves accuracy.
- **[from source]** **Tricks** (p.19): keep a `todo.md` of subgoals and **recite** the goals in natural language when updating it, to keep them in recent context.

## 7. Applications (p.19-20)
- **[from source]** **CLI** (Gemini CLI): hierarchical `GEMINI.md` files (home, project root, subdirectories) for inheritance and isolation; static context loaded at startup and dynamic context accumulated; the file system plays the role of a lightweight database; compression replaces long histories with AI-generated summaries in a predefined format (overall goal, key knowledge, file system state, recent actions, current plan) (p.19). `[DATED]`.
- **[from source]** **Deep research** (Tongyi DeepResearch): cycle of searching, extracting, generating sub-questions and integrating evidence; a periodic summarization model compresses the history into "context snapshots", establishing a **context lifecycle**: collect, compress/abstract, reason and reuse over summaries (p.19) `[DATED]`.
- **[from source]** **Brain-computer interfaces** as context collection of internal states (attention, emotion, cognitive load), with noise and instability still significant (p.20). Speculative.

## 8. Challenges and directions (p.20-21)
Limited and inefficient collection (depends on explicit input), large-scale storage and management, models' limited understanding of context, long-context bottlenecks (quadratic complexity of the Transformer; alternatives such as Mamba, LongMamba and LOCOST still with weaknesses), still imprecise context selection and the idea of "digital presence" (p.20). Conclusion: a trajectory of lower human engagement in explicit context management (p.21).

## 9. Gaps of the paper (so the agent stays honest)
- **[from source]** The paper does not offer: token budget per component, cost formulas, experimental comparison of memory strategies, an evaluation protocol for context engineering, nor security (for example, injection via retrieved context). The only mention of security in the designs is secure storage (p.10) and minimum permissions per subagent (p.12).
