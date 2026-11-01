# LLMS p.55–70 — capability and evaluation

**[DATED]** Empirical results (Tab. 16/17, p.66-70) use 2023 models (LLaMA/LLaMA 2 7B, Pythia, Falcon, Vicuna, Alpaca, ChatGLM, Davinci-002/003, ChatGPT, Claude, Claude 2). They are not a current ranking.

## 7.1 Basic abilities (LLMS p.55-61)
- **Language generation**: language modeling (Penn Treebank, WikiText-103, the Pile, LAMBADA; perplexity; follows the scaling law), conditional generation (translation, summarization, QA; BLEU/ROUGE; LLM as evaluator), code synthesis (pass@k = 1 if at least one of the k programs passes all tests (p.56 note 37); APPS, HumanEval, MBPP; top 28% on Codeforces for AlphaCode) (p.55-56).
- Problems (p.56-58): unreliable generation evaluation (inconsistency between reference metrics and humans; humans also disagree; LLMs as evaluators have order bias and a preference for LLM-written text) and insufficient specialized generation (catastrophic forgetting, "alignment tax", structured data).
- **Knowledge utilization** (p.58-60): closed-book QA (scales with size/data), open-book QA (retriever; evidence can make a smaller model outperform one 10× larger; recency), knowledge completion (WikiFact: good on frequent relations, poor on rare ones). **Hallucination**: intrinsic (conflicts with the source) and extrinsic (unverifiable) (Fig. 17, p.59); mitigation by alignment, tools, uncertainty estimation (SelfCheckGPT) (p.59). **Recency**: updating is expensive and causes forgetting; external retrieval is practical; parameter editing works poorly in LLMs (EasyEdit) (p.59-60).
- **Complex reasoning** (p.60-61): knowledge (CSQA, StrategyQA, ScienceQA), symbolic (last letter, coin flip, in-domain vs out-of-domain; scratchpad; code + interpreter), mathematical (SVAMP, GSM8k, MATH; continued pre-training on math; ATP with PISA/miniF2F and Lean/Isabelle/Metamath). Problems: **reasoning inconsistency** (right answer via an invalid path and vice versa; mitigate with tools, re-checking, Self-Refine, process supervision, code) and **numerical computation** (tokenizing digits individually helps; example 7481 → "7 481" and 74815 → "748 15") (p.61).

## 7.2 Advanced abilities (LLMS p.61-63)
Human alignment (TruthfulQA, HaluEval, HH-RLHF, CrowS-Pairs, WinoGender, RealToxicityPrompts; human and expert evaluation; quality pre-training data reduces effort) (p.62); interaction with the environment (VirtualHome, ALFRED, BEHAVIOR, ALFWorld, WebShop, Mind2Web, Voyager, GITM; emergent ability) (p.62); tool manipulation (plugins; in-context exemplars or tuning with simulated data; retrieval of tool usage when there are many APIs; LLMs can create tools) (p.62). Tab. 14 (p.57) lists datasets per ability.

## 7.3 Benchmarks and approaches (LLMS p.63-66)
- **Comprehensive benchmarks** (p.63): MMLU (GPT-4: 86.4% in 5-shot [DATED]); BIG-bench (204 tasks; BIG-bench-Lite with 24; BBH — with CoT it surpasses the human average); HELM (16 scenarios and 7 metric categories; IT helps; code pre-training helps reasoning); human-level tests (AGIEval, C-Eval etc.); frameworks LM Evaluation Harness, OpenAI Evals; Open LLM Leaderboard.
- **Approaches** (p.63-66, Tab. 15, p.64): **benchmark**-based (format the prompt, generate, parse by rules, compute the metric; few-shot suited to base models; CoT for reasoning), **human**-based (pairwise comparison or single score; Chatbot Arena) and **model**-based (AlpacaEval, MT-bench; position bias, verbosity and self-preference; does not serve hard tasks well).
- **Pros/cons** (p.65-66): benchmarks are automatic and cheap, but sensitive to the prompt, to zero/few-shot and to the parser, and suffer from **data contamination**; humans reflect real use, but have biases, cost and low reproducibility; models scale and explain, with the biases cited.

## 7.4 Empirical evaluation (LLMS p.66-70)
- Setup: general zero-shot; 3-shot on hard reasoning and tools; per-task metrics (LAMBADA accuracy, WMT'22 BLEU-4, XSum ROUGE-L, HumanEval pass@10...) (p.66).
- Findings (p.69-70): ChatGPT strong overall; strong models on environment/tools (plugins); all weak on MATH and HotpotQA; among open models, instruction-tuned > base (but Vicuna/Alpaca worsen on LAMBADA); small open models are weak on math, environment and tools; ranking varies across alignment tasks; LLaMA 2 7B stands out in reasoning (~2T tokens of data and cleaning); scaling helps more on complex tasks. The conclusions hold for the sizes tested (p.70).

## Rules
1. To compare models, state the setting (prompt, shot, parser) and check for contamination (LLMS p.65).
2. Do not use an LLM as the sole judge on hard tasks; mitigate order/verbosity biases (p.65-66, p.77).
3. Do not cite Tab. 16 numbers as the current state `[DATED]`.
