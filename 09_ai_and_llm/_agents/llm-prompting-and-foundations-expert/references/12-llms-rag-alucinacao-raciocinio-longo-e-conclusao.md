# LLMS p.88–99 — RAG, hallucination, long reasoning (long CoT), conclusion and log

## 9.6 RAG (LLMS p.88-90)
- RAG = a prompting strategy that integrates external information into the prompt (LLMS p.89). **Flow**: context retrieval (lexical/sparse with an inverted index, or semantic/dense with vectors and ANN), prompt construction (ask the model to use the documents; reranking and compression because long contexts suffer from "lost in the middle") and generation (self-checking, deciding whether to re-retrieve) (p.89).
- Improvements (p.89-90): retrieval granularity (propositions as the unit), query expansion/decomposition and **query rewriting** (including by LLM and distillation), result refinement (rerank, filter, extract/compress, token-level compression), **iterative and adaptive retrieval** (confidence-based stopping criterion; interleaved CoT), **training with RAG** (instructions with position bias and noise; reconstruction pre-training tasks) (p.90).

## 9.7 Hallucination (LLMS p.90-92)
- Definition (p.90): intrinsic/extrinsic in the old view; today the focus is open **factual hallucination**: entity error, relation error, incompleteness, outdatedness, exaggeration (overclaim) and unverifiability.
- Sources (p.90-91): data (quality/imitative falsehoods, bias, recency, domain, long tail); training (attention decays with length, **exposure bias** from teacher forcing; distillation with hallucinated synthetic data; RLHF can lead to sycophantic behavior); generation (poorly legible or abstract prompt; **high temperature** gives probability to irrelevant tokens) (p.91).
- Detection (p.91-92): model-based (HaluEval; CoT helps; extract claims and judge), uncertainty (token probability, consistency — SelfCheckGPT, question reconstruction) and tools (FActScore, FacTool, HaluAgent).
- Mitigation (p.92): alignment (HaluEval 2.0; beware of sycophancy), RAG (RARR, LLM-Augmenter, Verify-and-Edit, IRCoT) and decoding (DoLa, ITI, CAD, KCTS).

## 9.8 Complex reasoning — long CoT (LLMS p.92-96; added in the 11 Mar 2025 update, p.99)
- What it is: a long thinking process before the answer, "slow thinking", typical of reasoning models (note 55 explains the term; OpenAI's "o" series; examples with DeepSeek-R1 in Fig. 19) (p.92-93). Patterns: verification, reflection, backtracking, divide and conquer, self-refinement (p.93).
- Advantages vs standard CoT: allows revising and verifying within the answer and can emulate search (ToT/GoT) in text; this ability **emerges with training** (p.93).
- Long CoT data (p.93-94): distillation from open models (STILL-2 with DeepSeek-R1-Lite-Preview and QwQ-32B-preview; length reflects difficulty), synthesis by search (MCTS with per-step Q-values) and multi-agent collaboration.
- Training (p.94-95): **instruction tuning** with long CoT (STILL-2: Qwen2.5 32B with 3.9K distilled samples yielded performance comparable to o1-preview on math; generalizes across disciplines; tendency to use long CoT even on simple problems) and **RL scaling** (DeepSeek-R1, Kimi-K1.5): policy model (SFT warm-up; R1-Zero dispenses with SFT using a format reward), **verifiable reward** (1/0 for a correct answer or tests), GRPO/RLOO algorithms without a value model, monitoring the average response length (p.95).
- **Test-time scaling** (p.96): trading inference cost for performance; criteria: token efficiency and performance ceiling; RL tends to have higher efficiency and ceiling (R1-Zero keeps improving after >8,000 steps); Self-Consistency, planning and agents are also forms of test-time scaling.
- **[DATED]** 2025 section; model names and ranking are not the current state.

## 10 Conclusion and directions (LLMS p.96-98)
Basic principles (why next-token prediction generalizes; data contamination), architecture (GPT-4 Turbo's 128K and Claude 2.1's 200K context at the time [DATED]; models still do not use the whole context well), training (data-centric infrastructure, predictable scaling, proxy models), utilization (why prompts are good/bad is still an open question; RAG and long-context utilization), **safety and alignment** (hallucination, malicious use, cost of RLHF, red teaming, federated learning for privacy), ecosystem (Assistants API, GPT Store) and AGI with safety as a priority (p.96-98).

## CODA and log (LLMS p.98-99)
Chronology: first version 31 Mar 2023; major revisions on 29 Jun 2023, 10 Sep 2023, 23 Nov 2023, 25 Sep 2024, 11 Mar 2025 (long CoT) and 27 Feb 2026 (Fig. 3) (p.98-99). The experiments are partial due to compute limitations (p.99). **Inconsistency**: the CODA text (p.98) still cites 23 Nov 2023 as the most recent version.

## Rules
1. For factuality: RAG (reranking and compression), checking/verification and low temperature; consider sycophancy after RLHF (LLMS p.89-92).
2. For hard reasoning: long CoT/reasoning models cost more inference (test-time scaling) (LLMS p.96).
3. Do not assert the 2026 state of the art from this source `[DATED]`.
