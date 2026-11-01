# INDEX — llm-prompting-and-foundations-expert

Closed collection of **two sources**. All pages cited in this package are **PDF pages = printed pages** (arXiv, 1:1 numbering; there is no offset). Automatic verification: `tests/verify_citations.py` (see `tests/relatorio-de-fidelidade.md`).

## 1. Sources
| Abbreviation | Work | Edition read (stamp) | Pages | Body read | Cite as |
|---|---|---|---|---|---|
| **LLMS** | *A Survey of Large Language Models* — Wayne Xin Zhao, Kun Zhou, Junyi Li and others (Renmin University of China) | arXiv:2303.18223v19 [cs.CL], 18 Mar 2026; "Version: v18 (major update on March 7, 2026)" (LLMS p.1) | 144 | p.1–99 in full (extracted text; tables/figures as text only); p.100–144 = bibliographic references, **not used as content** | `LLMS p.N` |
| **PES** | *A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications* — Pranab Sahoo, Ayush Kumar Singh, Sriparna Saha, Vinija Jain, Samrat Mondal, Aman Chadha | arXiv:2402.07927v2 [cs.AI], 16 Mar 2025 (PES p.1) | 12 | p.1–10 in full (Tab. 1, p.10, as linearized text); p.10–12 also contain references | `PES p.N` |

**[DATED]**: PES = Mar/2025; LLMS = v19 of Mar/2026, with content mostly up to 2025 and experiments from 2023. Nothing here describes the current state of the art. Formulas used in scripts (Eq. 1-3 p.4, Eq. 4-5 p.25, Eq. 10 p.27, Tab. 18-20 p.82-84, p.86) were **checked visually** on the rendered pages.

## 2. Section map
**LLMS**: 1 Introduction p.1-4 · 2 Overview p.4-11 · 3 Resources p.11-16 · 4 Pre-training p.16-30 · 5 Post-training p.30-44 · 6 Utilization p.44-55 · 7 Capacity and evaluation p.55-70 · 8 Applications p.70-78 · 9 Advanced topics p.78-96 · 10 Conclusion p.96-98 · CODA/log p.98-99. (P.4 calls Section 8 a "practical guide to prompt design", but the guide is in 6.1.1, p.44-47.)
**PES**: 1 Introduction p.1-2 · 2 Techniques by area (2.1-2.12) p.2-9 · Fig. 2 taxonomy p.3 · Table 1 p.10 · 3 Conclusion p.10.
Command: `python -I scripts/llm_lookup.py --sections` and `--page N --source LLMS|PES`.

## 3. Where each topic is
| Topic | File | Pages |
|---|---|---|
| Identification, taxonomy (12 areas, 41 techniques), PES Table 1 | `01-pes-visao-geral-e-taxonomia.md` | PES p.1-3, 10 |
| Reasoning techniques (zero/few-shot, CoT, Auto-CoT, SC, ToT, GoT, Self-Refine, CoD...) | `02-pes-tecnicas-de-raciocinio.md` | PES p.2-7 |
| Hallucination (RAG, ReAct, CoVe, CoN, CoK), Active-Prompt, APE, ART, CCoT, Emotion, code, OPRO, RaR, Step-Back | `03-pes-alucinacao-codigo-otimizacao-e-demais.md` | PES p.7-9 |
| Four generations, scaling laws (KM/Chinchilla), emergence, GPT | `04-llms-fundamentos-scaling-emergencia-gpt.md` | LLMS p.1-11 |
| Checkpoints, corpora, datasets, libraries, pre-training data, tokenization, curriculum | `05-llms-recursos-dados-pretreino.md` | LLMS p.11-21 |
| Architectures, RoPE, objectives, decoding, training optimization and parallelism | `06-llms-arquitetura-e-treinamento.md` | LLMS p.21-30 |
| Instruction tuning, RLHF, DPO, SFT vs RLHF, PEFT/LoRA | `07-llms-adaptacao-instrucao-alinhamento-peft.md` | LLMS p.30-44 |
| Prompting (principles, Tab. 12), ICL, CoT, planning | `08-llms-utilizacao-prompting-icl-cot-planejamento.md` | LLMS p.44-55 |
| Evaluation: abilities, benchmarks, approaches, 2023 empirical | `09-llms-avaliacao-e-capacidades.md` | LLMS p.55-70 |
| Applications (NLP, IR, RecSys, MLLM, KG, domains) | `10-llms-aplicacoes-e-pesquisa.md` | LLMS p.70-78 |
| Long context, agents, training memory, inference, compression | `11-llms-topicos-avancados-contexto-agentes-eficiencia.md` | LLMS p.78-88 |
| RAG, hallucination, long CoT/test-time scaling, conclusion, log | `12-llms-rag-alucinacao-raciocinio-longo-e-conclusao.md` | LLMS p.88-99 |
| Glossary | `glossario.md` | — |
| Procedures P1–P11 | `procedimentos.md` | — |
| Cases, anti-patterns and inconsistencies of the sources | `casos-e-antipadroes.md` | — |
| Items that age | `datado.md` | — |

## 4. Scripts (`scripts/`, Python 3 stdlib, no network, `python -I`)
- `llm_lookup.py` + `llm_index.json`: topic → pages search; `--page`, `--sections`, `--gaps` (NOT COVERED), `--datado`.
- `prompt_technique_selector.py` + `pes_techniques.json` (41 techniques, each with a page) + `llms_prompt_tips.json` (Tab. 12): selector by criteria, `--show`, `--compare`, `--tips`.
- `llm_calc.py`: scaling laws, Chinchilla allocation, RoPE, decoding, training memory (16P), activations (Tab. 18), arithmetic intensity (Tab. 19/20), LoRA, quantization, SmoothQuant, pass@k, majority vote, WordPiece.

## 5. Declared gaps (NOT COVERED)
Prompt injection, jailbreak, guardrails, MCP, prompt caching, system prompt, structured output/JSON mode, prompt chaining/DSPy, KTO, watermarking, prices, GDPR/LGPD, carbon footprint and all content after the sources: see `python -I scripts/llm_lookup.py --gaps`. LLMS pages 100 to 144 (references) were not used as content.

## 6. Label convention
`[from source]` = is on the cited page (here, "from the survey"); `[inference]` = direct deduction; `[extrapolation]` = knowledge outside the collection (no page); `[DATED]` = ages.
