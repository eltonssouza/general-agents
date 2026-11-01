# PES §2.3–2.12 — hallucination, interaction, optimization, code and other areas

Numbers "as reported" (PES, Mar/2025); not comparable across techniques `[inference]`.

## 2.3 Reducing hallucination (PES p.7-8)
- **RAG**: analyzes the input, builds a query, searches a pre-built knowledge base and incorporates the passages into the prompt; outperforms seq2seq and task-specific architectures on ODQA, with EM up to 56.8% (TriviaQA) and 44.5% (Natural Questions) (PES p.7).
- **ReAct**: generates reasoning traces and actions in an interleaved fashion; uses a simple Wikipedia API on HotpotQA and Fever to reduce hallucination and error propagation; on ALFWorld and WebShop it reports success of 34% and 10% with few examples (PES p.7).
- **CoVe (Chain-of-Verification)**: four steps — baseline answer, plan verification questions, answer them independently, produce a revised answer (PES p.7). Reduces hallucination in lists, QA and long-form generation (PES p.7).
- **Chain-of-Note**: assesses the relevance of the retrieved documents and filters out the irrelevant, including answering "unknown" when information is missing; +7.9 average EM with noisy documents and +10.5 in rejection rate for out-of-knowledge questions (PES p.7).
- **Chain-of-Knowledge**: reasoning preparation and dynamic knowledge adaptation from internal sources, external bases and the prompt itself (PES p.7-8). The survey gives no numbers for CoK `[from source]`.

## 2.4 User interaction (PES p.8)
- **Active-Prompt**: chooses, by uncertainty (inspired by active learning), the most useful questions for annotating CoT examples; outperforms Self-Consistency by 7.0% on average (text-davinci-002) and 1.8% (code-davinci-002) across eight tasks (PES p.8). Table 1 lists the uncertainty metrics: disagreement, entropy, variance and self-confidence (PES p.10).

## 2.5 Fine-tuning and optimization (PES p.8)
- **APE**: generates and selects instructions automatically; outperformed human prompts on 19 of 24 BIG-Bench tasks (PES p.8).

## 2.6 Knowledge and tools (PES p.8)
- **ART**: multi-step reasoning through structured programs, pausing for external tool outputs; outperforms traditional prompting on BigBench and MMLU and, in some cases, matches hand-written demonstrations (PES p.8).

## 2.7 Consistency (PES p.8)
- **Contrastive CoT**: shows valid **and** invalid demonstrations; 4–16% gain on strategic/mathematical reasoning vs CoT, ~+5% with Self-Consistency; open question: generating contrasts automatically and applying them beyond reasoning (PES p.8).

## 2.8 Emotions and tone (PES p.8)
- **EmotionPrompt**: appends 11 emotional-stimulus phrases; +8.00% relative on instruction induction, +115% on BIG-Bench tasks; study with 106 participants: +10.9% in performance, truthfulness and responsibility (PES p.8).

## 2.9 Code and execution (PES p.8-9)
- **Scratchpad**: the model generates intermediate tokens before the answer; 46.8% on MBPP-aug; limits: fixed 512-token window and dependence on supervised learning (PES p.9).
- **Program of Thoughts**: reasoning as Python programs executed by an interpreter; ~12% average gain over CoT on math and financial problems (PES p.9).
- **Structured CoT**: program structures (sequence, branch, loop) in the steps; up to +13.79% over CoT on HumanEval/MBPP/MBCPP (PES p.9).
- **Chain of Code**: flexible pseudocode; an interpreter captures undefined behavior and an "LMulator" simulates it; 84% on BIG-Bench Hard (+12%) (PES p.9).

## 2.10 Optimization (PES p.9)
- **OPRO**: uses the LLM as an optimizer via prompts; optimized prompts outperform human ones by up to 8% (GSM8K) and up to 50% (Big-Bench) (PES p.9).

## 2.11 User intent (PES p.9)
- **RaR**: the LLM rephrases and expands the question; a two-step variant uses one LLM to rephrase and another to answer (PES p.9).

## 2.12 Metacognition (PES p.9)
- **Step-Back**: an abstraction step (general principles) and then reasoning; PaLM-2L: +7% MMLU Physics and Chemistry, +27% TimeQA, +7% MuSiQue (PES p.9).

## Decision rules
1. External/up-to-date knowledge: RAG (PES p.7); with reasoning and an API: ReAct (PES p.7); unreliable documents: Chain-of-Note (PES p.7).
2. Fact self-checking: CoVe (PES p.7).
3. Math/finance with exact computation: PoT or CoC (PES p.9); per the survey, the interpreter does the computation (PES p.9).
4. Optimize prompts automatically: APE or OPRO (PES p.8, p.9). In Table 1 both are `Single` turn; APE has a "LM Generated" prompt and OPRO "Manual" (PES p.10).
5. Choose examples to annotate: Active-Prompt (PES p.8).
6. The survey does **not** cover prompt security, monetary costs or a selection guide `[inference]`.
