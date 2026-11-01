# Cases, anti-patterns and inconsistencies of the sources

Labels: `[from source]` (cited page), `[inference]`, `[extrapolation]`, `[DATED]`.

## A. Usage anti-patterns
1. **Comparing PES technique percentages as if they were a ranking**: each gain comes from a different model/dataset/metric (PES p.4-9; Table 1, p.10). E.g., ToT 74% vs 4% on Game of 24 (PES p.4) is not comparable with Self-Consistency +17.9% on GSM8K (PES p.2) `[inference]`.
2. **CoT as a silver bullet**: it only helps sufficiently large models and step-by-step reasoning tasks; it can worsen non-reasoning tasks (MNLI, SST-2, QQP) (LLMS p.53).
3. **Ignoring the order and choice of demonstrations**: ICL varies greatly with selection and order; there is recency bias (LLMS p.50).
4. **Assuming demonstrations always teach**: random labels in the demos do not always degrade performance, since the model may merely recognize the task (LLMS p.51); real learning only in large models (LLMS p.52).
5. **Increasing the number of instructions without quality control**: in the survey's experiment, 220K synthetic instructions made results worse (BBH 29.81→26.63) (LLMS p.35-36) `[DATED: LLaMA 7B 2023]`.
6. **Using SFT to "inject" missing knowledge**: SFT unlocks abilities but can induce hallucination when the demonstration exceeds the model's knowledge (LLMS p.42).
7. **High temperature for factual tasks**: increases the probability of irrelevant tokens and of hallucination (LLMS p.91).
8. **LLM as the sole judge**: position, verbosity and self-preference biases; weak on hard tasks (LLMS p.65-66, 77).
9. **Treating Tab. 16 as the current ranking**: 2023 models (LLMS p.66-70) `[DATED]`.
10. **Assuming RLHF = better than DPO (or the reverse)**: the survey lists advantages and limits of both and says RLHF is difficult and "little explored" in the public literature (LLMS p.41-43); no verdict.
11. **Copying decoding values as "optimal"**: they are settings of specific 2023 models (LLMS p.27).
12. **Expecting prompt security from the package**: prompt injection, jailbreak and guardrails are absent (NOT COVERED) (`llm_lookup.py --gaps`).

## B. Inconsistencies or fragile points in the sources themselves (flag them to the user)
1. **Chinchilla scaling law (LLMS p.4)**: the text defines a=α/(α+β) and b=β/(α+β) for Nopt and Dopt, but minimizing Eq. 2 under C≈6ND gives the exponent β/(α+β) for N `[inference: derivation; `llm_calc.py chinchilla-allocation` confirms numerically]`. The survey also does not give the formula for G.
2. **Tab. 18 (LLMS p.82)** prints "6TH" (without B) for Q,K,V; and the table sum gives ≈17.3 GiB for the example the text summarizes as "16GB" (LLMS p.81-82) `[inference]`.
3. **A100 Imax (LLMS p.83)**: 142.51 FLOP/byte is only reproduced by treating GB as 2³⁰ bytes (with 10⁹ it gives ≈153.0) `[inference]`.
4. **WikiFact (LLMS p.46)**: the same paragraph cites 29.25→31.21 and then "from 23.61 to 28.47"; Tab. 17 (p.68) gives 29.25 and 31.21.
5. **CODA (LLMS p.98)** says the most recent version is from 23 Nov 2023, but the log reaches 27 Feb 2026 (LLMS p.99).
6. **Section 8 (LLMS p.4)**: described as a "practical guide to prompt design", but the prompt design content is in 6.1.1 (p.44-47) and Section 8 is about applications (p.70).
7. **PES §2.4**: "User Interaction" in Fig. 2 (p.3) vs "User Interface" in the text (p.8); **EEDP**: authorship differs between Fig. 2 (p.3) and the text (p.5).
8. **PES: CoK** gives no numbers in the text (PES p.7-8).
9. **LLMS p.3, note 1**: an LLM is not necessarily more capable than a small PLM; emergence may not occur in some LLMs.
10. **Emergence**: the survey itself cites the debate that part of the "jump" may come from discontinuous metrics (LLMS p.6).

## C. Exemplary cases (how the agent should act)
- *"Which PES technique is best for math?"* → there is no "best"; list candidates (CoT, Self-Consistency, PoT, CoC, Step-Back...) with pages and the non-comparability warning; offer criteria (cost, external tool) (PES p.2-9).
- *"How many tokens should I use to train a 7B model?"* → the survey gives C≈6ND, Eq. 2 and the KM vs Chinchilla discussion (LLMS p.4-5); it gives no explicit "tokens per parameter"; compute with the script, show the alert about a/b and mark `[DATED]` and `[extrapolation]` for G.
- *"My RAG hallucinates, what should I do?"* → P4 and P10; no security recipe.
- *"How do I avoid prompt injection?"* → NOT COVERED; offer `[extrapolation]` only if asked.
- *"How much memory to train LLaMA-7B?"* → 16P ≈ 100GB of states (LLMS p.81) + activations (p.82); state the imprecision of the "16GB".
