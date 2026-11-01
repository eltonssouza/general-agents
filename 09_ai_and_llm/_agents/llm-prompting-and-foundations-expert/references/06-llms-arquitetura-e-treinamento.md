# LLMS p.21–30 — architecture, pre-training objectives, decoding and training

## 4.2.1 Architectures (LLMS p.22-23)
- Three types: **encoder-decoder** (T5, BART, Flan-T5), **causal decoder** (GPT series, OPT, BLOOM, Gopher; unidirectional attention) and **prefix decoder** (GLM-130B, U-PaLM; bidirectional on the prefix) (p.22). "Decoder-only" usually means causal decoder (p.22). Fig. 9 compares the attention patterns (p.23).
- **MoE**: activates a subset of weights per input (Switch Transformer, GLaM); scales parameters with nearly constant compute cost; training can be unstable due to "hard" routing; the assumption that GPT-4 is an MoE is speculation without official verification (p.22).
- **Emerging architectures** (SSM): Mamba, RWKV, RetNet, Hyena; the survey says SSMs still lag behind Transformers in performance (p.22-23). Tab. 6 (p.23): decoding/training complexity — Transformer O(H(T+H)) / O(TH(T+H)); RWKV and RetNet O(H²) / O(TH²); Hyena does not infer like an RNN (p.23).
- Tab. 5 (p.23): model cards (e.g., GPT-3 175B, 96 layers, 96 heads, d_model 12288, training context 2048; LLaMA 65B 80/64/8192; PaLM 540B 118/48/18432).

## 4.2.2 Detailed configuration (LLMS p.23-26)
- Tab. 7 (p.24): normalization (Post/Pre/Sandwich; LayerNorm, RMSNorm, DeepNorm), activations (ReLU, GeLU, Swish, SwiGLU, GeGLU), position (absolute, relative, RoPE, ALiBi).
- Pre-LN is more stable than post-LN but worse in performance; even so, most use pre-LN (p.24). GLU variants cost ~50% more parameters in the FFN (p.24).
- **RoPE** (p.25, Eq. 4-5, checked visually): rotation by t·θi; θi=b^(−2(i−1)/d), i=1..d/2, b=10000 by default; wavelength λi=2π·b^(2(i−1)/d)=2π/θi. ALiBi uses a predefined penalty (p.25).
- Attention: full, sparse (GPT-3), multi-query (PaLM, StarCoder), grouped-query (LLaMA 2), FlashAttention (IO-aware; FA-2 ≈2×), PagedAttention (KV cache) (p.25).
- Recommendation (p.26): pre RMSNorm, SwiGLU or GeGLU, RoPE or ALiBi; avoid LN right after the embedding.
- Script: `scripts/llm_calc.py rope`.

## 4.2.3 Pre-training tasks (LLMS p.26)
- **LM**: maximize Σ log P(x_i | x_<i) (Eq. 6). **Prefix LM**: slightly worse than LM with the same tokens. **DAE**: recover replaced spans, log P(x̃ | x\x̃) (Eq. 7); T5 and GLM-130B. **Mixture-of-Denoisers** (UL2): S-, R- and X-denoiser; used in PaLM 2 (p.26).

## 4.2.4 Decoding (LLMS p.26-27)
- Greedy: x_i = argmax P(x|x_<i) (Eq. 8); good when the output depends heavily on the input (translation/summarization), but produces repetition in open-ended tasks (p.26).
- Sampling: x_i ~ P(x|x_<i) (Eq. 9). **Temperature**: P(x_j|x_<i)=exp(l_j/t)/Σ exp(l_j'/t) (Eq. 10): t=1 standard sampling, t→0 equals greedy search, t→∞ becomes uniform sampling (p.27).
- **Top-k** truncates to the k most probable tokens; **top-p (nucleus)** uses the smallest set whose cumulative probability ≥ p (p.27). Beam search (size typically 3–6; larger beams can worsen results) and length penalty (p.27). Others: η-sampling, contrastive search, typical sampling, contrastive decoding, DoLa (p.27).
- Reported settings (p.27): T5 greedy (beam 4 and penalty 0.6 in translation/summarization); GPT-3 beam 4 and 0.6; Alpaca top-k 50, top-p 0.9, T 0.7; LLaMA T 0.1 (pass@1) and 0.8 (pass@100) for code; OpenAI API: temperature 0 ≈ greedy, top_p, best_of, presence/frequency penalty — even so "outputs may differ" **[DATED: 2023 API parameters]**.
- Fig. 10 (p.26): example "I am sleepy. I start a pot of" with a distribution over the vocabulary (coffee 0.661; water 0.119; tea 0.057; rice 0.017; chai 0.012...). Script: `llm_calc.py sampling`.

## 4.2.5 Why next-word prediction works (LLMS p.27-28)
There is no formal theoretical study of the advantage of decoder-only; the causal decoder had better zero-shot without multitask tuning [29]; studies of encoder-decoder at scale are lacking (p.28).

## 4.3 Training (LLMS p.28-30)
- Large batch (2,048 examples or 4M tokens); GPT-3 grows from 32K to 3.2M tokens (p.28). Learning rate: linear warm-up over 0.1–0.5% of the steps up to ~5×10⁻⁵–1×10⁻⁴ (GPT-3: 6×10⁻⁵), then cosine decay down to ~10% (p.28). AdamW/Adam with β1=0.9, β2=0.95, ε=10⁻⁸; Adafactor (PaLM, T5) (p.28). Clipping 1.0 and weight decay 0.1 (p.28). Tab. 8 (p.29): settings per model.
- Loss spikes: PaLM/OPT restart from an earlier checkpoint and skip data; GLM reduces embedding gradients (p.28-29).
- **3D parallelism**: data + pipeline (bubbles; GPipe, PipeDream) + tensor (Y=XA with A split by columns) (p.29). Mixed precision: FP16 vs **BF16** (more exponent bits; better for pre-training) (p.29-30). BLOOM: 8-way DP, 4-way TP, 12-way PP on 384 A100 (p.30). ZeRO, FSDP, activation recomputation (p.30).

## Rules
1. Choose a base architecture recipe: causal decoder + pre RMSNorm + SwiGLU + RoPE/ALiBi, according to the survey (p.22, 26) — `[inference]` that this is a "standard recipe" beyond what the text suggests.
2. Training instability: pre-LN normalization, clipping, restart/skip, BF16 (p.24, 28-30).
3. Output determinism: low temperature/greedy (p.27); the API may still vary (p.27).
