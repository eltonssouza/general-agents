# [DATED] and limits of the collection

Dates of the sources: UDL — PDF dated 15 Feb 2024 (UDL p.1), text written through ~2023 (mentions ChatGPT, GPT-4, PaLM; UDL p.248, p.412, p.439). NNDL — text from 2015, footer "Last update: Thu Dec 26 2019" (NNDL p.2, p.57). Nothing in the collection is later than 2023-2024. **Never state the current state of the art.**

## 1. [DATED] items with pages
| Topic | What the book says | Source |
|---|---|---|
| Largest model | "~10^12 parameters" (largest models at the time) | UDL p.110 |
| Distributed training | 1 trillion parameters on 3,072 GPUs | UDL p.128 |
| ImageNet | best top-1 of 9.0% error (transformers) | UDL p.209 |
| Vision with transformers | ViT 11.45%; SWin 9.89%; DaViT 9.60% top-1 error | UDL p.243-246 |
| LLMs | GLaM, Gopher, Chinchilla, Megatron-Turing NLG, LaMDA, PaLM (540 bn; 780 bn tokens; 6,144 processors) | UDL p.248 |
| GPT-4 | "is not transparent" | UDL p.439 |
| Diffusion | DALL·E 2, Imagen, GLIDE, ControlNet, Stable Diffusion | UDL p.383-385 |
| RLHF | InstructGPT/ChatGPT (2022) | UDL p.412 |
| Ethics | McKinsey figures (2016-2030), CO₂ emissions from training | UDL p.443-444 |
| MNIST | 2013 record: 9,979/10,000 | NNDL p.52 |
| "Deep" networks | "5 to 10 hidden layers routine" | NNDL p.57 |
| ReLU | "widely used only for a few years" | NNDL p.259 |
| ImageNet | LRMD 2012; KSH 2012; GoogLeNet 2014; human 5.1% | NNDL p.282-287 |
| Tools | Theano 0.6/0.7, Caffe, Torch | NNDL p.253 |
| Future | the author's opinion on intent-based interfaces and AGI | NNDL p.296-303 |

## 2. Outside the collection (NOT COVERED) — verified by searching the extracted texts
Mixture-of-experts, FlashAttention, KV cache, RoPE (by name), ALiBi, RMSNorm, SwiGLU, Mamba/state-space models, scaling laws, chain-of-thought, instruction tuning (beyond what RLHF describes), LoRA, prompt engineering, hallucination, LLM agents, RAG, LLM weight quantization, mixed precision, TPU, Adafactor/Lion, neural tangent kernel, federated learning, jailbreak.
`python -I scripts/dl_lookup.py --gaps` lists the terms checked and the unread pages.

## 3. Limits of reading coverage
- UDL not read: p.197-199, 253, 278-281, 315-316, 413-414, appendix B (453-461), C.1-C.2 (462-469), bibliography and index (476-541); p.174 only partially.
- NNDL: code listings p.268-279 only in parts; the code was not executed (Python 2/Theano).
- Figures/plots in both PDFs were not interpreted beyond the captions and values cited in text; NNDL equations were read from textual context, except those checked by render (INDEX §1).
- Exercises/problems: read only when cited.

## 4. What the agent does with current questions
1. Answer what the book says, marking [DATED] with the source's date.
2. Say "the collection does not cover" for modern topics (model name, benchmark, recent parameter count).
3. If the user brings new data, agree and mark it [extrapolation] (not from a book) without correcting the book.
4. Do not invent benchmark or model numbers; only those on the pages read.
