# BAAS chs. 1-2: generative AI, agency, autonomy, architectures and multi-agent systems

Source: BAAS = *Building Agentic AI Systems* (Biswas and Talukdar, Packt, April/2025). Pages = **PDF page** (printed = PDF − 25). Reading: full text of pp.28-74. The figures were not inspected. Every model or tool name below is `[DATED]` (2025).

## 1. Ch. 1 (PDF p.28-50): generative AI as the foundation of agents

- **[from source]** Generative AI learns the distribution of the training data and samples from it; it differs from discriminative models, which separate classes (BAAS p.29).
- **[from source]** Types covered: VAEs (p.30), GANs (p.31), autoregressive models and the Transformer (p.32-33). LLM types cited: autoregressive, encoder-only, encoder-decoder, multimodal, instruction-tuned and domain-specific (p.34-35). Model names on those pages (GPT, BERT, T5, PaLM, BioBERT etc.) are `[DATED]`.
- **[from source]** "LLM agent" is not a model architecture type: it is an advanced application of LLMs, typically built on instruction-tuned LLMs plus extra components (BAAS p.35). It combines LLMs with techniques such as reinforcement learning, planning and tool use (p.41).
- **[from source]** Guiding example of the whole book: a flight-booking assistant. The information gathered in the conversation becomes parameters of backend APIs (the fictitious functions `flightLookup` and `bookFlight`, p.39); the model reasons step by step (the book calls it *chain of thought*) at the start of the conversation (p.40).
- **[from source]** Code generation: running LLM-generated code requires caution; the book mentions running in a *sandbox* and sanitizing before execution (p.42).
- **[from source]** Limitations: data bias (p.46), training data leakage (the book cites extraction with about US$ 200 in API calls, p.46-47), computational cost and SLMs as an alternative (p.47), deepfakes/IP/jobs and weak creative generalization (p.48).
- `[DATED]` Table 1.1 of commercial and open source tools (p.43-45) and training cost figures (p.47) are from 2025 or earlier.

## 2. Ch. 2 (PDF p.52-74): agency, autonomy and architectures

**Self-governance, agency and autonomy**
- **[from source]** Self-governance: the system decides, sets goals and regulates its own behavior; five aspects: self-organization, self-regulation, self-adaptation, self-optimization and self-determination (BAAS p.54).
- **[from source]** Agency has three elements: decision-making authority, intentionality and responsibility (p.54-55).
- **[from source]** Autonomy has three aspects: operational (executes without direct human intervention), functional (chooses actions to achieve goals, modulated by context) and hierarchical (how much decision-making power it receives within a larger structure) (p.55-56).
- **[from source]** Autonomy does **not** imply the absence of human oversight: systems operate within limits defined by designers or operators (p.56). The degree of hierarchical autonomy may depend on privacy preferences and on access to sensitive data and resources (p.56).
- **[from source]** Algorithm 1 (p.57-59) is a travel agent with goals, a knowledge base and a highest-score `MakeDecision`; the book itself says it has agency and autonomy, but is **not intelligent**: it needs airport codes and does not interpret free text (p.59-60).

**Intelligent agent**
- **[from source]** Definition: a self-governing entity that perceives the environment and acts to achieve goals. Key attributes: reactivity, proactiveness and social ability (p.60). Additional attributes: learning/adaptation, reasoning/planning, autonomy (p.60-61).

**Three architectures (BAAS p.61-65)**
| Architecture | Idea | Strengths | Limits | Page |
|---|---|---|---|---|
| Deliberative (symbolic) | cycle sensing → knowledge update → planning/reasoning → execution, over an explicit knowledge base | complex reasoning, planning, well-defined environments | computational cost, hard to formalize changing knowledge | p.61-62 |
| Reactive (stimulus-response) | maps perception directly to action | speed, robustness, parallelism, emergent behavior | no long-term planning, limited reasoning and learning | p.63-64 |
| Hybrid | reactive layer (fast responses) + deliberative layer (planning) | combines both | integration is still a research area | p.64-65 |

- **[from source]** Techniques cited for hybrid architectures: task decomposition, selection among multiple plans, planning with external modules, reflection and refinement, planning with memory (p.65).
- **[from source]** The choice of pattern depends on task complexity, environment uncertainty and the need for real-time response (p.65).
- **[inference]** Mapping to modern LLM agents: a "model → tool call → observation" loop with explicit planning behaves like a hybrid; the book does not make this mapping on those pages.

## 3. Multi-agent systems (MAS) in ch. 2

- **[from source]** MAS is a subfield of distributed AI: several agents interact, cooperate and coordinate for collective goals (p.65-66). Domains cited: supply chain, traffic, robotics/manufacturing, environmental monitoring, sensor networks, simulations (p.66).
- **[from source]** Seven characteristics: autonomy, interaction, adaptability, distributed control, scalability, heterogeneity and decentralized data/knowledge (p.67).
- **[from source]** Three interaction mechanisms: cooperation (p.68), coordination (p.69) and negotiation, with auctions, voting, bargaining or game theory (p.69-70).
- **[from source]** Algorithm 2 (p.71-72) models airlines, hotels and a travel agency as agents that cooperate and coordinate; the book warns that the MAS still needs discrete inputs and does not interpret natural-language messages (p.73).

Continuation: CWD orchestration in `05-baas-multiagente-cwd.md`.
