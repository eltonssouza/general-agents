# LLMS p.70–78 — applications in research and in domains

**[DATED]** State of the field in 2023–2025 according to the source; no product recommendation.

## 8.1 Research directions
- **Classic NLP** (LLMS p.70-71): on word/sentence tasks (similarity, sentiment), small models fine-tuned on full data usually outperform LLMs using ICL; on sequence tagging (NER, POS) ICL struggles with ambiguous classes ("MISC", "ORG"); on information extraction ICL falls below full-data fine-tuning, but LLM + small model collaboration helps; on generation (translation, summarization) LLMs are strong, yet weak in low-resource languages/domains (e.g., Marathi→English). Suggestion: choose an LLM or a small model based on flexibility, data, compute and efficiency (p.71).
- **Information retrieval** (LLMS p.71-72): retrieve-then-rerank pipeline; LLMs as **pointwise, pairwise or listwise** rerankers (sliding window, setwise); LLMs enhance IR by generating annotations, queries, query rewriting/expansion and document expansion; problems: inference cost, long texts and need for adaptation (p.72).
- **Recommender systems** (LLMS p.72-73): LLM as recommender (zero-shot, instruction tuning, InstructRec), LLM as enhancer (intent, feature encoder, distillation) and as simulator (RecAgent, AgentCF); in zero/few-shot they tend to fall below ID-based recommenders; latency is a constraint (p.73).
- **MLLMs** (LLMS p.73-75): image encoder + LLM + connection module; two-stage training (vision-language alignment and visual instruction tuning); with fewer than ~1M pairs only the connection is updated; with ~1B pairs the encoder can be tuned (p.73). Evaluation: perception vs cognition, object hallucination (POPE), VQA, closed/open paradigms (MMBench, CircularEval), benchmarks (LVLM-eHub, Reform-Eval, MME, SEED-Bench, MM-Vet) (p.74). Safety: hallucination and harmful content also occur (p.75).
- **KG-enhanced LLM** (LLMS p.75-76): ⟨head, relation, tail⟩ triples; retrieval-augmented (subgraph in the prompt; serializing loses structure) and synergy-augmented (multi-turn queries, StructGPT) (p.75-76).
- **LLM for evaluation** (LLMS p.76-77): evaluation by score (pairwise, with reference) or by language (critiques); methods with varied contexts, multi-agent and fine-tuned evaluators; meta-evaluation (MT-Bench: GPT-4 agrees with humans on no-tie comparisons of 80 multi-turn questions; LLMBar); problems: order bias, self-preference and length bias; LLMs do not identify their own errors well without external feedback (p.77).

## 8.2 Domains (LLMS p.77-78)
- **Healthcare**: varied tasks; Med-PaLM with expert-level performance on the USMLE; risks: medical misinformation and privacy when sending patient data (p.77).
- **Education**: student-level performance on exams; risks: plagiarism, bias, dependence and unequal access (p.77).
- **Law**: analysis, judgment prediction, drafting; GPT-4 in the top 10% on a simulated US bar exam [DATED]; risks: copyright, personal data leakage, bias (p.77).
- **Finance**: sentiment analysis, financial NER; BloombergGPT; general LLMs fall below domain PLMs on some tasks; risk of inaccurate content affecting markets (p.77).
- **Scientific research**: literature review, hypotheses, data analysis, writing and review; reliability is lacking and hallucination occurs (p.77-78).
- Others: psychology (ToM), software engineering (code suggestion, repair) (p.78). Cross-cutting considerations: accuracy, biases, privacy and data security (p.78).

## Rules
1. On classic tasks with plenty of labeled data, evaluate a fine-tuned small model before assuming an LLM is better (LLMS p.70-71).
2. In regulated domains (healthcare, law, finance) remember the risks of hallucination, privacy and bias (LLMS p.77); **does not replace professional advice** `[extrapolation]`.
