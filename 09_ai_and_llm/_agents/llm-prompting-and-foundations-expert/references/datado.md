# [DATED] items — what ages in these sources

Dates: **PES = arXiv v2, 16 Mar 2025**; **LLMS = arXiv v19, 18 Mar 2026** (log up to 27 Feb 2026; the main text and the experiments are mostly from 2023-2025). This package does not claim the current state of the art.

| Item | Where | Note |
|---|---|---|
| List of 41 techniques and the benchmark numbers | PES p.2-9, p.10 | Reflect 2020-2025 papers; models of the time (GPT-3, PaLM, GPT-4, Llama 2/3) |
| OpenAI models, APIs and parameters (ada/babbage/curie/davinci, gpt-3.5-turbo, gpt-4-1106-preview; temperature, top_p, best_of, penalties) | LLMS p.12-13, 27 | 2023 names; the source itself says the names point to the latest version |
| Tab. 1 (LLMs >10B), Fig. 3 (timeline), LLaMA/Mistral/Gemma/Qwen/GLM/Baichuan series | LLMS p.8-9, 11-12 | Snapshots of models up to 2024/2026 |
| Empirical results (Tab. 10, 16, 17, 21) | LLMS p.35, 67-70, 88 | LLaMA 1/2 7B-13B, Vicuna, Alpaca, ChatGPT, Claude/Claude 2, Davinci |
| Context windows (128K GPT-4 Turbo, 200K Claude 2.1) | LLMS p.96 | 2023 values |
| MMLU 86.4% (GPT-4, 5-shot); GPT-4 in the top 10% of a simulated law exam | LLMS p.63, 77 | 2023 results |
| Scaling coefficients (KM 2020; Chinchilla E=1.69 A=406.4 B=410.7 α=0.34 β=0.28) | LLMS p.4 | Fitted over specific size ranges (p.4); extrapolating is `[extrapolation]` |
| Long CoT, reasoning models (DeepSeek-R1, "o" series, STILL-2, Kimi-K1.5) and RL with verifiable reward | LLMS p.92-96 | 2025 section |
| Prompt tips (Tab. 12) and principles | LLMS p.45-47 | Collected in 2023; e.g., "OpenAI models perform better in English" |
| Libraries/hardware (A100/H100, DeepSpeed, vLLM, bitsandbytes, llama.cpp) | LLMS p.16, 83-88 | 2023-2025 state |
| Hallucination, RAG and PEFT as the state of the field | LLMS p.43-44, 88-92 | Rapidly evolving techniques |

Rule: when citing any line above, append `[DATED]` and the source date; if the user brings a more recent fact that contradicts it, agree and mark `[DATED]`.
