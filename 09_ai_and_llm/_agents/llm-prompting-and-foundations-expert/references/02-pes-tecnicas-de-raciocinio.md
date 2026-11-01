# PES §2.1–2.2 — prompting techniques without training, and reasoning techniques

All numbers below are **as reported by the survey** (PES, Mar/2025), each with the model/dataset of the original paper; they are not comparable with each other `[inference]`. General label: `[from source]`.

## 2.1 New tasks without extensive training (PES p.2)
- **Zero-shot**: the model receives only the task description, with no labeled examples; it uses pre-existing knowledge (PES p.2).
- **Few-shot**: a few input-output pairs in the prompt; improves complex tasks, but spends tokens, the choice/composition of examples influences behavior, and biases (e.g., favoring frequent words) persist (PES p.2).

## 2.2 Reasoning and logic (PES p.2-7)
| Technique | Idea (paraphrase) | Reported result | Cited limits | Page |
|---|---|---|---|---|
| CoT | examples that show the step-by-step reasoning before the answer | PaLM 540B: 90.2% accuracy on math/commonsense benchmarks | — | 2 |
| Auto-CoT | generates the chains automatically with "Let's think step by step" and samples diverse questions to limit errors | +1.33% (arithmetic) and +1.5% (symbolic) over CoT, with GPT-3 | individual chains may be wrong | 2 |
| Self-Consistency | samples several chains and picks the most consistent answer (marginalizes) instead of greedy decoding | +17.9% GSM8K, +11.0% SVAMP, +12.2% AQuA, +6.4% StrategyQA, +3.9% ARC-challenge vs base CoT | — | 2 |
| LogiCoT | think-verify-revise loop with reductio ad absurdum | Vicuna-33b/GPT-4: +0.16%/+1.42% GSM8K, +3.15%/+2.75% AQuA vs CoT | — | 2-4 |
| Chain-of-Symbol | condensed symbols in place of natural language (spatial tasks) | ChatGPT 31.8%→92.6% on Brick World; up to 65.8% fewer tokens | scalability, generalization, integration and interpretability | 4 |
| Tree-of-Thoughts | tree of "thoughts" with search (BFS/DFS), lookahead and backtracking | Game of 24: 74% vs 4% (CoT); word task: 60% vs 16% | — | 4 |
| Graph-of-Thoughts | thoughts as a directed graph, with aggregation and backtracking | T5-base +3.41% and T5-large +5.08% on GSM8K; ScienceQA +6.63%/+1.09% vs Multimodal-CoT | — | 4 |
| System 2 Attention | the LLM regenerates the context removing the irrelevant, then answers | factual QA 80.3%; long-form generation 3.82/5 on objectivity | — | 4 |
| Thread of Thought | analyzes chaotic contexts in segments, summarizing each; plug-and-play module | +47.20% (QA) and +17.8% (conversation) | — | 4 |
| Chain of Table | generates and executes SQL/DataFrame operations step by step over tables | +8.69% TabFact, +6.72% WikiTQ | — | 4 |
| Self-Refine | generate → self-critique → refine until a stopping criterion | GPT-4: +8.7 pts code optimization, +13.9 readability, +21.6 sentiment reversal | — | 4-5 |
| Code Prompting | reformulates a natural-language task as code (without executing) | GPT-3.5 +8.42 average F1; Mistral +4.22 | — | 5 |
| ECHO | clusters questions (Sentence-BERT + k-means), samples demos, unifies rationales | +2.8% over Auto-CoT on 10 benchmarks; with 50% fewer examples drops −0.8% (Few-Shot-CoT −1.3%) | behind GPT-3.5 on Mixtral due to rationale quality | 5 |
| Logic-of-Thought | extracts propositions, extends them with logical laws (Python module), translates back into the prompt | +4.35% (ReClor, CoT), +5% (LogiQA, CoT+SC), +8% (ProofWriter, ToT) | — | 5 |
| IAP | chooses the zero-shot prompt per instance using attention saliency (IAP-ss, IAP-mv) | IAP-mv: +1.82% LLaMA-3-8B and +3.31% Qwen-14B on math | — | 5 |
| EEDP | graph representation via paths between endpoints + adjacency lists | −55% tokens (molecular); EPCP +10.21%/+16.76%; EPDP +4.73%/+30.13% | — | 5-6 |
| Layer-of-Thoughts | filtering layers (keywords, semantics, confirmation) for legal retrieval | F2 0.835 (Japanese Civil Law) vs 0.807; recall 0.966 (German traffic) | — | 6 |
| Narrative-of-Thought | temporal narratives + Python class for temporal graphs | LLaMA3-8B F1 42.2 vs GPT-3.5 45.7 | models <10B stay ~50% behind GPT-3.5/4 without the technique | 6 |
| Buffer of Thoughts | meta-buffer of reusable "thought-templates" | +11% Game of 24, +20% Geometric Shapes, +51% Checkmate-in-One; 12% of the cost of multi-query methods; Llama3-8B+BoT outperforms Llama3-70B | — | 6 |
| CD-CoT | contrasts noisy rationales with clean ones, rewrites and votes | +17.8% on average | models copy flawed reasoning; self-correction without external feedback fails | 6 |
| R-CoT | generates reverse-chain geometric data (GeoChain + Reverse A&Q) for LMMs | 8B model outperforms GPT-4o by 12.5% (MathVista) and 14.5% (GeoQA) | — | 6-7 |
| Chain of Draft | short, dense steps instead of verbose CoT | matches/outperforms CoT; up to 80% fewer output tokens; latency −76.2% on average | — | 7 |

## How to use (rules)
1. No examples and no verification available: zero-shot or few-shot (PES p.2).
2. Multi-step reasoning: CoT; for robustness, Self-Consistency (PES p.2); if examples are lacking, Auto-CoT (PES p.2).
3. Exploration/backtracking: ToT or GoT (PES p.4); cost of multiple calls `[inference]` — compare with BoT (12% of the cost, PES p.6).
4. Logical verification: LogiCoT or Logic-of-Thought (PES p.4-5). Self-critique: Self-Refine (PES p.4-5).
5. Tables: Chain of Table (PES p.4). Graphs: EEDP (PES p.5-6). Spatial: CoS (PES p.4). Time: NoT (PES p.6).
6. Token/latency efficiency: CoD, CoS, EEDP, BoT (pages above). Large/noisy context: ThoT, S2A (PES p.4).
7. To choose by criterion, run `scripts/prompt_technique_selector.py`.
