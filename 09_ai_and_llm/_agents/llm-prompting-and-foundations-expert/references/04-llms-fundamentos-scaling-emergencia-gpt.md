# LLMS p.1–11 — foundations, scaling laws, emergent abilities, GPT family

Convention: **PDF page = printed page** (arXiv, 1:1). Labels: `[from source]` (from the survey), `[inference]`, `[extrapolation]`, `[DATED]`.

## Source identification
- *A Survey of Large Language Models*, Wayne Xin Zhao, Kun Zhou, Junyi Li and others, Renmin University of China (LLMS p.1).
- Edition read: stamp **arXiv:2303.18223v19 [cs.CL], 18 Mar 2026**; p.1 also says "Version: v18 (major update on March 7, 2026)"; the log (p.98-99) runs up to 27 Feb 2026 (figure 3). First version: 31 Mar 2023 (LLMS p.98).
- **[DATED]** The text covers literature mainly up to 2025; the empirical experiments (Tab. 10, 16, 17, 21) use 2023 models (LLaMA/Vicuna/ChatGPT/Claude 2). The CODA (p.98) still says the "latest version" is from 23 Nov 2023 — old text not updated, while the log reaches 2026.
- Reading: p.1–99 read in full in extracted text (tables/figures as linearized text: Tab. 1 p.8, Fig. 3 p.9, Fig. 6 p.17, Tab. 16 p.67 checked only in text). Pages 100 to 144 are **bibliographic references, not used as content**.
- Section map: 1 Introduction p.1-4; 2 Overview p.4-11; 3 Resources p.11-16; 4 Pre-training p.16-30; 5 Post-training p.30-44; 6 Utilization p.44-55; 7 Capacity and evaluation p.55-70; 8 Applications p.70-78; 9 Advanced topics p.78-96; 10 Conclusion p.96-98. (P.4 describes Section 8 as a "practical guide to prompt design", but the prompt guide is in 6.1.1, p.44-47; Section 8 deals with applications.)

## Four generations of language models (LLMS p.1-3)
- SLM (1990s): n-gram/Markov, suffers from the curse of dimensionality, uses smoothing (back-off, Good–Turing) (LLMS p.1).
- NLM: neural networks, distributed representations, word2vec (LLMS p.1-2).
- PLM: ELMo, BERT, GPT-2; pre-train + fine-tune paradigm (LLMS p.2).
- LLM: scaling the model/data changes behavior and emergent abilities appear; GPT-3 (175B) does few-shot via ICL, GPT-2 does not (LLMS p.2-3). Fig. 2 (p.2): from a task-specific helper to a general solver.
- Three differences LLM vs PLM: emergent abilities; main access through prompting; end of the research/engineering separation (LLMS p.3). Note: an LLM is not necessarily more capable than a small PLM (LLMS p.3, note 1).
- Definition used: Transformers with hundreds of billions of parameters (LLMS p.4); no formal consensus; the survey focuses on models >10B (LLMS p.4, note 4).

## Scaling laws (LLMS p.4-5) — formulas checked visually on p.4
- **KM (Kaplan et al., 2020)**: L(N)=(Nc/N)^αN with αN≈0.076, Nc≈8.8×10¹³; L(D)=(Dc/D)^αD with αD≈0.095, Dc≈5.4×10¹³; L(C)=(Cc/C)^αC with αC≈0.050, Cc≈3.1×10⁸; L is the cross-entropy loss in nats; N and D in non-embedding parameters and tokens; C in FP-days (LLMS p.4, Eq. 1, note 6).
- **Chinchilla (Hoffmann et al.)**: L(N,D)=E + A/N^α + B/D^β with E=1.69, A=406.4, B=410.7, α=0.34, β=0.28 (Eq. 2); with C≈6ND: Nopt(C)=G·(C/6)^a and Dopt(C)=G⁻¹·(C/6)^b, a=α/(α+β), b=β/(α+β) (Eq. 3). G is "a scaling coefficient that can be computed from A, B, α, β"; the survey **does not give the formula for G** (LLMS p.4).
- KM favors allocating more of the extra budget to the model; Chinchilla proposes increasing model and data at equal scales (LLMS p.5).
- Discussion: predictable scaling (estimating large models from small ones; monitoring training); diminishing returns; public data may be "exhausted"; task-level predictability; **inverse scaling** (performance worsens with lower loss); ICL is not predictable by a scaling law (LLMS p.5).
- Script: `scripts/llm_calc.py scaling-kaplan|scaling-chinchilla|chinchilla-allocation`.

## Emergent abilities (LLMS p.5-6)
- Cited definition: abilities absent in small models that arise in large ones; performance rises far above random on reaching a certain scale (LLMS p.5).
- Three typical ones: **ICL** (GPT-3 175B; 3-digit arithmetic already appears in GPT-3 13B; 175B fails at Persian QA), **instruction following** (LaMDA-PT ≥68B; PaLM ≥62B), **step-by-step reasoning/CoT** (gain in PaLM/LaMDA >60B, more evident >100B; GSM8K > MAWPS > SVAMP for PaLM) (LLMS p.5-6).
- Relation to scaling laws: laws describe continuous/predictable improvement; emergence is an unpredictable jump; debate: part may come from discontinuous metrics; mention of grokking; child analogy without direct evidence (LLMS p.6, note 11).
- Key techniques: scaling, training (DeepSpeed, Megatron-LM; restart against loss spikes; mixed precision), eliciting abilities (CoT, instruction tuning), alignment (RLHF, helpful/honest/harmless criteria), tool use (calculator, search, plugins) (LLMS p.6-7).

## GPT evolution (LLMS p.7-11)
- GPT-1 (2018, decoder-only, generative pre-training); GPT-2 (1.5B, WebText; formulates p(output|input,task)); GPT-3 (2020, 175B, introduces ICL) (LLMS p.7-9).
- OpenAI improvements: training on code (Codex, Jul/2021; code-davinci-002 base of GPT-3.5; speculation about a link to CoT) and human alignment (preference RL 2017; PPO Jul/2017; InstructGPT Jan/2022 formalized 3-stage RLHF) (LLMS p.9-10).
- ChatGPT (Nov/2022, trained similarly to InstructGPT, with human conversations), GPT-4 (Mar/2023, multimodal; predictable scaling; red teaming), GPT-4V (Sep/2023), GPT-4 Turbo (Nov/2023; 128k tokens; knowledge up to Apr/2023; function calling; Assistants API) (LLMS p.10-11).
- **[DATED]** All of this history is that of the source's time; Fig. 3 (p.9) lists models up to 2026 only as a timeline.
- Persistent problems cited: hallucination and risky content (LLMS p.11).

## Open questions stated in the introduction (LLMS p.3)
Why emergence occurs; difficulty and cost of training LLMs (undisclosed details); difficulty of aligning to human values.
