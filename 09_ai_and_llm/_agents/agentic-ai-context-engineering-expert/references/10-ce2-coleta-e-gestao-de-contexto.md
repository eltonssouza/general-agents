# CE2 §4-5: context collection, storage, management, organization and abstraction

Source: CE2 (p.9-14; PDF page = printed). Full reading. `[DATED]` (Oct/2025): systems and products cited are examples from the paper, not recommendations. Memory formulas checked on p.12 by rendering. The paper presents **qualitative patterns and trade-offs**; it offers no measurements nor experimental comparison among them.

## 1. Collection and storage (CE2 p.9-10)
- **[from source]** Two design principles (p.9): **Minimal Sufficiency**, that is, collect and store only what the task needs, since the value of context lies in sufficiency, not volume; and **Semantic Continuity**, that is, the goal is to maintain continuity of **meaning**, not only of data.
- **[from source]** Era 1.0: collection on a single device with few sensors (GPS, clock, keyboard and mouse, application logs) and local storage, log files and caches discarded at shutdown (p.9-10).
- **[from source]** Era 2.0: distributed collection (phones, wearables, home sensors, cloud services, third-party APIs) and multimodal streams; **tiered** storage according to use (p.10): fast cache or edge nodes for ephemeral data; embedded databases (SQLite, LevelDB, RocksDB) for medium retention; secure OS storage or HSM when security is crucial; cloud for long persistence and cross-device synchronization.
- **[from source]** Coding agents with long, multi-session tasks cannot depend only on the context window; they write state and progress to long-term memory and restore it on resume (p.10). The paper cites structured notes from Claude Code written outside the window and retrieved when needed, and a Pokémon game example with thousands of steps resumed after resets `[DATED]` (p.10).
- **[from source]** Era 3.0 (speculative): storage as "cognitive infrastructure", with "forgetting" and "remembering" like humans and absolute user control over sensitive data (p.10).

## 2. Processing of textual context (p.10-11)
Four designs and their trade-offs, according to the paper:
| Design | How it works | Limitation noted | Page |
|---|---|---|---|
| Timestamp | each item gets a timestamp, preserving order | no semantic structure; the sequence grows linearly (storage and reasoning scale) | p.10 |
| Functional and semantic tags | tag by role (goal, decision, action), priority, origin | can be rigid and limit flexible reasoning | p.10-11 |
| Q&A pair compression | reformulates context as questions and answers | breaks the flow of ideas; poor for summarizing or reasoning about the whole | p.11 |
| Hierarchical notes | tree from broad to specific concepts | reflects grouping, not logical relations (cause and effect); does not capture the evolution of understanding | p.11 |

## 3. Multimodal context (p.11-12)
- **[from source]** The challenge is the heterogeneity of modalities. Three era 2.0 strategies: map inputs to a comparable vector space (one encoder per modality plus a projection layer), combine modalities in joint self-attention in the same Transformer, and use cross-attention so one modality queries another (p.11). Limit noted: traditional designs require specifying which modalities interact (p.11-12).
- **[inference]** This section describes model architecture, not the action of whoever assembles an agent's context; limited use for designing API-based agents.

## 4. Organization: layered memory architecture (p.12)
- **[from source]** OS analogy attributed to Karpathy: the model is the CPU and the context window is the RAM (fast and limited); context engineering decides what goes into the window (p.12). Example of a LeadResearcher that writes plans to persistent memory when context exceeds 200 thousand tokens (p.12) `[DATED]`.
- **[from source]** Two-layer model "for clarity", extensible to intermediate layers (working memory, episodic buffers, domain caches) (p.12). Formal definitions (checked on p.12):
  - **Short-term memory** `Ms = f_short({c ∈ C : w_temporal(c) > θs})`, that is, the subset of context with high temporal relevance, selected by a processing function that may involve human judgment, heuristics or system operations.
  - **Long-term memory** `Ml = f_long({c ∈ C : w_importance(c) > θl ∧ w_temporal(c) ≤ θs})`, the processed and abstracted subset with high importance (and already outside the high temporal relevance range).
  - **Transfer** `f_transfer: Ms → Ml`, the consolidation governed by repetition, emotional significance and relevance to existing knowledge.
- **[inference]** The weights `w_temporal`, `w_importance` and the thresholds `θs`, `θl` **have no values nor estimation method** in the paper; they are designer parameters. The script `ctx_calc.py memory-split` applies the two rules to weights **the user** supplies, and the tests verify only the definitional logic (no number from the paper).
- **[inference]** To compare with BAAS: short-term ≈ working memory (BAAS p.199) and long-term ≈ knowledge base (p.200-201); the paper has no named "episodic memory", but cites "episodic buffers" (p.12). See `12-cruzamento-baas-ce2.md`.

## 5. Context isolation (p.12-13)
- **[from source]** **Subagent**: isolates functional context and avoids "pollution" of the main context; in the Claude Code example, each subagent has an isolated window, its own system prompt and restricted tool permissions; the main system delegates when the task matches the specialty (p.12). The paper suggests separation by functional dimensions (analysis, execution, validation) or hierarchical layers (planning, implementation, review), each unit with the **minimum permissions** (p.12). Paper's observation: unlike static RAG, the LeadResearcher plans, can redo searches, adjust keywords and create subtasks, in parallel (p.12).
- **[from source]** **Lightweight references**: large outputs stay in external storage (for example, the *sandbox* of Hugging Face's CodeAgent) and only concise references enter the window; the same holds for state objects with a schema, where only selected fields are exposed (p.13). It reduces token overhead while keeping access to the full content.

## 6. Abstraction: "self-baking" (p.13-14)
- **[from source]** Raw context (turns, tool outputs, retrieved documents) grows fast; abstraction converts raw context into compact, structured representations. The paper calls the process *self-baking* (the agent "digests" its own context into persistent knowledge) and distinguishes it from mere memory: without it the agent only recalls; with it, it accumulates knowledge (p.13).
- **[from source]** Four designs developed in the text (p.13-14):
  1. **Hierarchical memory**: raw context at the base, progressively summarized into more abstract levels, with links back to the original; raw corresponds to short-term and abstract to long-term (p.13).
  2. **Natural-language summaries**: keeps the raw and generates periodic summaries (including multilevel); simple and flexible, but unstructured, which makes it hard to reason about connections between events (p.13).
  3. **Fact extraction with a fixed schema**: entity map, event records or task tree; more reasoning over facts, but layers can become inconsistent and good extractors are hard to build (p.13-14). The example is building a structured "dossier" before code review (CodeRabbit, `[DATED]`, p.14).
  4. **Progressive compression into vectors** (embeddings): compact and useful for semantic search, but not human-readable, which makes editing or inspecting hard (p.14).
- **[from source]** Fig. 4 (p.9, map of design considerations) also lists "store directly in structured format" as a form of *self-baking* (HMT example), which the text of §5.4 does not develop. Figures 4 and 6 were not visually inspected; what is above comes from the extracted text.

## 7. How to apply (label)
- **[inference]** To decide an agent's memory format, compare the "limitation noted" columns (p.11, 13-14) with the type of use: auditing and editing → schema or notes; retrieving by meaning → vectors; telling the story → summaries.
- **[extrapolation]** The choice of thresholds and the cost of summarization depend on the model and domain; the texts offer no numbers.
