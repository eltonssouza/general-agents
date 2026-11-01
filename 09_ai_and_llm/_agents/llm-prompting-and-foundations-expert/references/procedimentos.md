# Procedures (P1–P11)

Labels: `[from source]` = supported on the page; `[inference]` = step organized by the package. Run the scripts when indicated (`python -I scripts/...`).

## P1 — Choose a prompting technique from the PES taxonomy
1. Classify the problem into one of the 12 areas (PES p.3) or list criteria: `prompt_technique_selector.py --need math` (aliases in `--tags`).
2. Filter constraints: no external tool (`--no-external`), a single call (`--turn single`), prompt origin (`--acq Manual`). Per the survey, "Single/Multi" and the prompt origin come from Table 1 (PES p.10).
3. Read the card (`--show ID`): idea, reported result, limits and page.
4. Compare two candidates with `--compare A B`, but do **not** compare the percentages: models and datasets differ (PES p.4-9, p.10) `[inference]`.
5. Deliver: technique(s), why, risks, and what the PES does not say (monetary costs, security, ranking). Mark `[DATED]`: the PES is from Mar/2025.

## P2 — Design a prompt (LLMS guide, 2023)
1. Include the 4 ingredients: task description, input data, context and style (LLMS p.44-45).
2. Apply the 5 principles: clear goal, decomposition, demonstrations, friendly format, role (LLMS p.45-46).
3. Consult the T/I/C/D/O tips of Tab. 12: `prompt_technique_selector.py --tips [--principle N]` (LLMS p.47).
4. If there is a factual basis, retrieve documents and paste them into the prompt (tip I1, LLMS p.47); ask for the output to be checked (O1, LLMS p.47).
5. Test with and without the "detailed" prompt: in the survey, careful prompts helped more on complex tasks (LLMS p.46) `[DATED: ChatGPT 2023]`.

## P3 — Diagnose weak ICL
1. Demonstrations: relevance and information (selection by k-NN/diversity), format and **order** (recency bias) (LLMS p.50).
2. Does the task require new learning? Per the survey, *task learning* only emerges in large models (≥66B in the cited study), while *task recognition* arises in small ones (LLMS p.52).
3. Duplication in pre-training data worsens the ability to copy from context (LLMS p.20) `[from source]`.
4. Consider CoT only for step-by-step reasoning and models ≥10B (LLMS p.53).

## P4 — Reduce hallucination
1. Provide external context: RAG (PES p.7; LLMS p.88-90) with rerank/compression to avoid "lost in the middle" (LLMS p.89).
2. Verify: CoVe (PES p.7) or self-checking; for noisy documents, Chain-of-Note (PES p.7).
3. Decoding: high temperature increases the risk of irrelevant tokens (LLMS p.91) `[from source]`.
4. Alignment: RLHF helps, but can induce sycophancy (LLMS p.92).
5. Detection: consistency across samples (SelfCheckGPT), token probabilities, tools (LLMS p.91-92).

## P5 — Estimate training resources
1. FLOPs: C ≈ 6ND (LLMS p.4): `llm_calc.py compute --N ... --D ...`.
2. Estimated loss: `scaling-chinchilla` (Eq. 2). **[DATED]** 2022 coefficients; extrapolating is `[extrapolation]`.
3. Allocation: `chinchilla-allocation --C ...`. **Alert**: the survey prints a=α/(α+β), but minimizing Eq. 2 itself gives β/(α+β) for N; the script shows both and a numerical check (LLMS p.4) `[inference]`.
4. Memory: states 16P bytes (LLMS p.81) + activations (Tab. 18, p.82): `train-states`, `train-activations`; add overheads (LLMS p.82).

## P6 — Estimate inference bottleneck and memory
1. Weight memory: `weights-memory` `[inference]` and compare with Tab. 21 (LLMS p.88).
2. Bottleneck: `arithmetic-intensity --phase prefill|decode` with your B, T, H, FLOP/s and bandwidth (LLMS p.83-84). Per the survey, decoding tends to be memory-bound (p.83).
3. Reduce: weight quantization (start with 4-bit, LLMS p.87), continuous batching, speculative decoding (LLMS p.84-85).

## P7 — Choose an adaptation strategy
1. Goal "follow instructions/format": instruction tuning with diverse, high-quality data (LLMS p.31-33, 36).
2. Goal "preferences/safety": RLHF (LLMS p.38-40) or alternatives (DPO etc., p.40-41); remember the costs and instability (LLMS p.43).
3. Limited budget: LoRA/PEFT (LLMS p.43-44); with quantization, QLoRA (LLMS p.87).
4. New knowledge: SFT "unlocks" more than it injects (LLMS p.42); for current facts, RAG (LLMS p.59-60) `[from source]`.

## P8 — Evaluate an LLM
1. State the model type (base, fine-tuned, specialized) and the approach (benchmark, human, model-based) (LLMS p.63-66).
2. Fix prompt, shot and parser; check for contamination (LLMS p.65).
3. If using an LLM judge: mitigate order/verbosity/self-preference biases (LLMS p.65-66, 77).
4. Record the date and do not generalize 2023 numbers `[DATED]`.

## P9 — Configure decoding
Determinism: greedy or t→0 (LLMS p.27); diversity: temperature, top-k, top-p (LLMS p.27). Use `llm_calc.py sampling` to see the effect. Cited values from models (Alpaca, LLaMA) are 2023 examples (LLMS p.27).

## P10 — Plan a RAG pipeline
Retrieval (lexical vs dense), prompt construction (rerank/compression), generation with self-checking; improvements: retrieval unit, query rewriting/expansion, iteration and training with RAG (LLMS p.89-90). RAG cost/latency and security: NOT COVERED.

## P11 — Question outside the collection or post-source
Run `llm_lookup.py TERM`. If "NOT COVERED": say that the package does not cover it; offer `[extrapolation]` only if asked and without a page; recommend current sources.
