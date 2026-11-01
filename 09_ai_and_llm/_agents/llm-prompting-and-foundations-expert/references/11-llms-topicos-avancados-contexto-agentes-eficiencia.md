# LLMS p.78–88 — advanced topics: long context, agents, training memory, inference, compression

**[DATED]** GPUs/libraries/techniques as per the source (2023–2025). Formulas checked visually: p.82 (Tab. 18), p.84 (Tab. 19/20), p.86 (quantization).

## 9.1 Long context (LLMS p.78-79)
- Position extension (p.78): direct fine-tuning at increasing lengths (2K→8K→32K), **position interpolation** (multiplies the indices by L/L′, L<L′), position truncation (ReRoPE), **base modification** (increasing the RoPE base vs decreasing it; decreasing extrapolates better, increasing is better within the training length), basis truncation (p.78-79).
- Adapting the window (p.79): parallel context window, Λ-shaped mask (StreamingLLM; "lost in the middle"), token selection (k-NN, blocks). Long data: a few billion tokens suffice; quality (coherent/cohesive vs chaotic) matters (p.79).

## 9.2 LLM-based agents (LLMS p.79-81)
- Components: **memory** (short-term = context window; long-term = external storage, e.g., vector store; profile), **planning** (text or code; propose candidates and choose; refine with feedback) and **execution** (LLM or tools) (p.80).
- Workflow (p.80): receive information → short memory → (retrieve from long memory) → plan → execute with tools → adjust via feedback.
- Applications: AutoGPT, GPT-Engineer, XAgent, WebGPT, ProgPrompt, Voyager; cooperative multi-agent (free dialogue, structured document, embeddings) or competitive (debate), LangChain, AgentVerse, AutoGen (p.80-81). Challenges: computational cost, alignment with sociability/role-play, tool extension and robustness/reliability (p.81).

## 9.3 Training memory and efficiency (LLMS p.81-83)
- **Model states** (p.81): for P parameters with mixed precision, parameters (2P) + gradients (2P) = 4P bytes; Adam/AdamW keeps in FP32 the parameter copy, the momentum and the variance (4P each = 12P); **total 16P bytes**; LLaMA-7B (P≈6.7×10⁹) ≈ 100GB for states alone.
- **Activations** (Tab. 18, p.82): listed per operation, in bytes, per layer (multiply by L): X: 2BTH; Q,K after RoPE: 4BTH; attention: Q,K,V 6BTH (the table prints "6TH") and softmax 2BT²N; output: 2BTH; Add&Norm: 2BTH; FFN inputs G,U: 2BTH and 4BTH′; D: 2BTH′; loss: 2BTH + softmax 4BTV. The text states ≈16GB per device for LLaMA-7B (V=32,000, L=32, H=4,096, H′=11,008, N=32) with B=1, T=2,048 (p.81-82). **When summing the table, the script's result (~17.3 GiB) does not exactly match the text's "16GB"**; treat the text's value as an approximation `[inference]` — see `llm_calc.py train-activations`.
- Other costs (p.82): PyTorch ~1GB, distributed frameworks 1–4GB, extra softmax 8BTV bytes, fragmentation 0.5–1GB.
- Optimizations (p.82-83): gradient checkpointing, **ZeRO-1/2/3** (optimizer states, gradients, parameters; ZeRO-3 +~50% communication), FSDP, offload (ZeRO-Offload/Infinity), FlashAttention (LLaMA-2 7B, seq. 2,048, batch 8: 1/10 of the time), sequence parallelism (DeepSpeed-Ulysses, Ring Attention).

## 9.4 Inference (LLMS p.83-85)
- Two stages: **prefill** (computes states and the KV cache of the input) and **decoding** (one token per step, updates the KV cache) (p.83).
- Metrics (p.83): compute capacity (FLOP/s), bandwidth (byte/s) and **maximum arithmetic intensity** Imax = compute/bandwidth; A100 half-precision example: 312 TFLOP/s and 2,039 GB/s → **Imax = 142.51 FLOP/byte** (the value is only reproduced by treating GB as 2³⁰ bytes `[inference]`). An operation is **memory-bound** if I<Imax; **compute-bound** if I>Imax.
- Tab. 19/20 (p.84): per operation, computation, transfer and intensity. For linear layers in prefill, I≈1/(1/H+1/(BT)); attention: (1+1/D)/(1/D+1/T); others ≈1. In decoding, linear layers I≈1/(1/H+1/B). With N=32, D=128, H=4096, B=8, T=1024 the text gives: linear ≈2730.67, attention ≈114.67, others ≈1 → prefill compute-bound; decoding with I<8 → memory-bound ("memory wall") (p.83). Script: `llm_calc.py arithmetic-intensity`.
- System optimization (p.84-85): FlashAttention/Flash-Decoding, PagedAttention, continuous batching (vLLM), Dynamic SplitFuse (DeepSpeed-MII). Algorithmic (p.85): speculative decoding (2×–3× without losing quality), cascade inference (FrugalGPT), non/semi-autoregressive decoding (Medusa), early exit and mixture-of-depths.

## 9.5 Compression (LLMS p.85-88)
- **Quantization**: QAT vs **PTQ** (PTQ preferred for LLMs); function x_q = R(x/S) − Z and dequantization x̃ = S·(x_q+Z) (p.86); activation outliers appear from ~6.7B; methods: mixed-precision decomposition (LLM.int8()), protecting salient weights, fine-grained quantization (group of 128), **SmoothQuant** (Y=(X diag(s)⁻¹)(diag(s)W), s_j = max(x_j)^α / max(w_j)^(1−α)), GPTQ/AWQ (p.86); QLoRA and QAT (p.87).
- Findings (p.87): INT8 weights are generally lossless; 4 bits depends on the method; with the same memory, 4-bit 60B > 8-bit 30B; activations are harder than weights; ICL, CoT and instruction following are little affected by 4-bit weights. Tab. 21 (p.88): LLaMA 7B 16-bit 12.58 GiB, 8-bit 6.65, 4-bit 3.94; 13B 24.40/12.53/7.34.
- Distillation (MINILLM), pruning (SparseGPT 60% unstructured; LLM-Pruner 20% with 93.6%; Sheared LLaMA 7B→2.7B with 87.8%) and libraries (bitsandbytes, GPTQ, AutoGPTQ, llama.cpp) (p.87-88).

## Rules
1. Estimate training memory as 16P bytes + activations, and add overheads (LLMS p.81-82).
2. In inference, identify whether the bottleneck is compute or memory via arithmetic intensity (LLMS p.83).
3. To reduce deployment memory, start by testing 4-bit weights (survey recommendation, p.87).
