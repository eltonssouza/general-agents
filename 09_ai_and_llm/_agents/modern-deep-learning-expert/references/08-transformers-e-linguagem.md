# 08 — Transformers: attention, layers, BERT, GPT-3, translation, long sequences and vision

Source: UDL ch.12 (PDF p.221-253; body and notes read through p.252; p.253 problems only, not read). NNDL does NOT cover transformers (the term does not appear; there is one mention of "attention" out of context, NNDL p.295). Everything is `[from source]` UDL unless marked.

## 1. UDL notation (important)
Tokens in the COLUMNS: `X ∈ R^{D×N}`; `Softmax[·]` acts per column; `Sa[X] = V · Softmax[KᵀQ]` (UDL p.226-227, eq. 12.7-12.8). In the most common convention (tokens in the rows) one writes `softmax(QKᵀ/√d)V`; that is `[extrapolation]` — the book does not use that notation. The dl_nets.py code uses lists of tokens (rows) but computes the same thing.

## 2. Motivation
Text has large inputs (example: 37 words × 1,024 = 37,888 inputs), variable length and ambiguity (the "it" that refers to the restaurant), so the network must share parameters across positions and have connections that depend on the data itself (UDL p.221-222).

## 3. Dot-product self-attention
- Values: `v_m = β_v + Ω_v x_m` (eq. 12.2); output n: `sa_n = Σ_m a[x_m, x_n] v_m` with non-negative weights summing to 1 — routing of the values (UDL p.222-223, eq. 12.3, fig. 12.1: weights 0.1; 0.3; 0.6).
- The number of attention weights grows with N² and is independent of D (UDL p.223). It is a "hypernetwork" (UDL p.223, p.249).
- Queries and keys: `q_n = β_q + Ω_q x_n`, `k_m = β_k + Ω_k x_m`; `a[x_m, x_n] = softmax_m(k_mᵀ q_n)` (UDL p.224, eq. 12.4-12.5). Queries and keys have the same dimension; values generally have that of the input (UDL p.224-225).
- Matrix form: `V = β_v 1ᵀ + Ω_v X` etc. (eq. 12.6) (UDL p.226).
- Self-attention is equivariant to permutations of the tokens, so it needs **positional encoding**: absolute (matrix Π added, fixed or learned) or relative (one parameter per offset) (UDL p.227-228). `[checked in dl_nets.py attention --perm-check]`.
- **Scaled attention**: divide by `√Dq` so the softmax does not saturate (eq. 12.9, UDL p.228). **Multi-head**: H heads with q/k/v of dimension D/H, concatenated and recombined by Ω_c (eq. 12.10-12.12, UDL p.228-229); "heads seem necessary; it is speculated that they make the model robust to bad initializations" (UDL p.229).

## 4. Layer and model
Transformer layer (UDL p.229-230, eq. 12.13): `X ← X + MhSa[X]`; `X ← LayerNorm[X]`; `x_n ← x_n + mlp[x_n]`; `X ← LayerNorm[X]` (LayerNorm AFTER each residual in the book). The note on p.251 explains that LayerNorm outside the residual block makes the gradients shrink and that training requires learning-rate warm-up and Adam (UDL p.251-252). `[extrapolation]` The book does not describe the variant with LayerNorm before the sublayers.

NLP pipeline: tokenizer (BPE: merge frequent pairs; fig. 12.8) → embeddings `X = Ω_e T` with T one-hot and `Ω_e ∈ R^{D×|V|}`, typical D 1,024 and |V| ~30,000 → K layers (UDL p.230-233).
Three types: encoder, decoder, encoder-decoder (UDL p.232-233).

## 5. BERT (encoder)
Vocabulary of 30,000, D=1,024, 24 layers, 16 heads, q/k/v of 64, MLP hidden size 4,096, **~340 million parameters** (UDL p.233). Self-supervised pre-training: mask words and predict them (batch 256, max length 512, 1 million steps ≈ 50 epochs of the 3.3-billion-word corpus) (UDL p.234); the auxiliary "next sentence" task helps little (note, UDL p.234). Fine-tuning: text classification with the `<cls>` token, per-word classification (NER), span prediction (SQuAD 1.1) (UDL p.235-236).
`[inference]` Our count (dl_calc.py xfmr-params --preset bert-large) gives ~333.5 million without LayerNorm (~333.6 with), close to "~340 million" but not equal; the book does not detail the calculation (positional embeddings, segment type, output head).

## 6. GPT-3 (decoder)
Autoregressive model: `Pr(t1…tN) = Pr(t1) Π Pr(tn | t1…t_{n−1})` (UDL p.236-237, eq. 12.14-12.15). Training with **masked attention**: dot products of future positions set to −∞ before the softmax (UDL p.237). Generation: argmax or sampling; reuses computation; beam search and top-K (UDL p.237-238). GPT-3: sequences of 2,048 tokens, batch of 3.2 million tokens, 96 layers, D=12,288, 96 heads, q/k/v dimension 128, 300 billion training tokens, **175 billion parameters** (UDL p.238). `[extrapolation]` With MLP 4D and vocabulary 50,257 dl_calc.py gives ~174.6 billion (neither the MLP nor the vocabulary is in the book).
Few-shot: examples in the context lead the model to complete the task, but "performance is erratic" and it is unclear whether it extrapolates or merely copies (UDL p.239).

## 7. Encoder-decoder, cross-attention, long sequences, vision
- Translation: the decoder uses masked attention and **cross-attention** (queries from the decoder, keys and values from the encoder) (UDL p.240-241, fig. 12.14).
- Quadratic cost in N; sparsify the interaction matrix (convolutional, dilated, global tokens, fig. 12.15) (UDL p.241-242). Notes: Linformer, BigBird, Performer, memory-compressed attention, kernelization (UDL p.250-251).
- Images: ImageGPT (decoder, 6.8 billion parameters, only 64×64 and 512 colors, 27.4% top-1 error on 48×48 ImageNet); ViT (16×16 patches, supervised pre-training on 303 million images and 18,000 classes, 11.45% top-1 error); SWin (9.89%) and DaViT (9.60%) (UDL p.242-246). `[DATED 2023]`.
- Training transformers is hard: it needs warm-up and Adam; factors interact (residuals, LayerNorm, q/k gradients smaller than v) (UDL p.251-252).

## 8. Relevant notes
RNN/LSTM/GRU, Bahdanau (2015) and Vaswani et al. (2017) (UDL p.247); LLMs listed (GLaM, Gopher, Chinchilla, Megatron-Turing NLG, LaMDA, PaLM with 540 billion parameters and 780 billion tokens) `[DATED 2022]` and the caveat that these models may memorize the training data and that claims of superhuman performance require caution (UDL p.248); tokenizers (WordPiece, BPE, unigram, SentencePiece) (UDL p.248); decoding: greedy, sampling, beam search, top-K (Fan 2018) and nucleus (Holtzman 2020) (UDL p.249); teacher forcing; types of attention (UDL p.249); positional: sinusoidal vs learned, relative, DeBERTa (UDL p.250). The book warns that many transformer improvements do not survive controlled tests (Narang 2021) (UDL p.247).

## 9. Outside the collection (declare NOT COVERED)
FlashAttention, KV cache, RoPE by name, ALiBi, mixture-of-experts, RMSNorm/SwiGLU, scaling laws, chain-of-thought, LoRA, instruction tuning (except as described under RLHF, UDL p.412), hallucination, evaluation of modern LLMs (`python -I scripts/dl_lookup.py --gaps`).

## 10. Scripts
`python -I scripts/dl_nets.py attention --tokens "1,0;0,1;1,1" --perm-check` · `... --mask` · `python -I scripts/dl_calc.py xfmr-params --preset bert-large --ln`.
