# PES — overview and taxonomy (12 pp.)

Page convention: **PDF page = printed page** (arXiv, 1:1 numbering). Labels: `[from source]` (here, "from the survey"), `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. Source identification
- Title: *A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications* (PES p.1).
- Authors: Pranab Sahoo, Ayush Kumar Singh, Sriparna Saha, Vinija Jain, Samrat Mondal, Aman Chadha; affiliations IIT Patna, Stanford and Amazon AI (PES p.1).
- Edition read: arXiv stamp arXiv:2402.07927v2 [cs.AI], 16 Mar 2025 (PES p.1). The identifier number suggests the first version was in Feb/2024 `[inference]`. The reference list (final pages of the PDF) includes works from 2025.
- **[DATED]** **Mar/2025** source. Models (GPT-3, PaLM, GPT-4, Llama 2/3 etc.), benchmark numbers and the list of techniques reflect the literature up to that date. The package does not claim the current state of the art.
- Reading: pages 1–10 read in full in the extracted text (Table 1, p.10, comes as linearized text); pages 10 to 12 also contain the references (used only for authors/title).

## 2. What the survey says about itself
- Prompt engineering = designing task-specific instructions ("prompts") to guide the model's output **without changing its parameters**; it applies to LLMs and vision-language models (PES p.1).
- Prompts can be natural-language instructions or learned vectors (PES p.1).
- Fig. 1 shows the components: instruction, context and user input feeding the LLM (PES p.1).
- Stated contribution: organize the techniques **by application area**, with methodology, applications, models used, datasets, strengths and limitations, plus a taxonomy diagram (Fig. 2, p.3) and a table (Tab. 1, p.10) (PES p.1-2).
- Numeric scope: "more than 41" techniques in the introduction (PES p.1) and "41" in the conclusion (PES p.10). Counting Fig. 2 gives 41 `[inference: count made on Fig. 2, p.3]`.
- Conclusion: persistent challenges (biases, factual inaccuracies, interpretability gaps), trends (meta-learning, hybrid prompting architectures) and an emphasis on responsible development (PES p.10).

## 3. Taxonomy (Fig. 2, p.3) — 12 areas, 41 techniques
| § | Application area | Techniques (PES p.3; description on p.) |
|---|---|---|
| 2.1 | New tasks without extensive training | Zero-shot (p.2), Few-shot (p.2) |
| 2.2 | Reasoning and logic | CoT (p.2), Auto-CoT (p.2), Self-Consistency (p.2), LogiCoT (p.2-4), Chain-of-Symbol (p.4), Tree-of-Thoughts (p.4), Graph-of-Thoughts (p.4), System 2 Attention (p.4), Thread of Thought (p.4), Chain of Table (p.4), Self-Refine (p.4-5), Code Prompting (p.5), ECHO (p.5), Logic-of-Thought (p.5), IAP (p.5), EEDP (p.5-6), Layer-of-Thoughts (p.6), Narrative-of-Thought (p.6), Buffer of Thoughts (p.6), CD-CoT (p.6), R-CoT (p.6-7), Chain of Draft (p.7) |
| 2.3 | Reducing hallucination | RAG, ReAct, CoVe, Chain-of-Note (p.7), Chain-of-Knowledge (p.7-8) |
| 2.4 | User interaction | Active-Prompt (p.8) |
| 2.5 | Fine-tuning and optimization | APE (p.8) |
| 2.6 | Knowledge-based reasoning and generation | ART (p.8) |
| 2.7 | Consistency and coherence | Contrastive CoT (p.8) |
| 2.8 | Emotions and tone | Emotion Prompting (p.8) |
| 2.9 | Code generation and execution | Scratchpad (p.8-9), Program of Thoughts (p.9), Structured CoT (p.9), Chain of Code (p.9) |
| 2.10 | Optimization and efficiency | OPRO (p.9) |
| 2.11 | Understanding user intent | Rephrase and Respond (p.9) |
| 2.12 | Metacognition and self-reflection | Step-Back (p.9) |

Fidelity notes:
- The label of §2.4 is "User Interaction" in Fig. 2 (p.3) and "User Interface" in the text heading (p.8) — an inconsistency in the survey itself.
- The authors attribute EEDP to "Yuan et al., 2024" in Fig. 2 (p.3) and to "Hong et al., 2024" in the text (p.5); the reference list (end of the PDF) cites Hong et al. Use "EEDP" without asserting authorship.
- The text (p.8) says APE "leverages reinforcement learning" to choose the optimal prompt; the original description of the method cannot be verified in this collection — report it only as the survey says.

## 4. Table 1 (p.10)
For each technique: application, **prompt origin** (Manual, LM Generated, Retrieval Based, Hybrid), **turns** (Single/Multi), language models, datasets and metrics (PES p.10). The per-technique attributes are in `scripts/pes_techniques.json` (fields `acquisition`, `turn`, `models`, `datasets`, `metrics`). The application labels inside Table 1 appear shifted in the text extraction; use **Fig. 2** as the official classification `[inference]`.

## 5. Limits of the survey (so the agent does not extrapolate)
- It provides no side-by-side comparison between techniques: each number comes from an original paper with a **different model, dataset and metric** (PES p.4-9, p.10). Comparing percentages across techniques is invalid `[inference]`.
- Percentages are reported "as reported"; the package did not verify them against the original papers `[inference]`.
- Costs/latency appear only for efficient techniques: CoS (up to 65.8% fewer prompt tokens, p.4), EEDP (55% fewer tokens on molecular graphs, p.6), BoT (12% of the cost of multi-query methods, p.6), CoD (up to 80% fewer output tokens, average latency −76.2%, p.7).
- No security section (prompt injection etc.): **NOT COVERED** in the PES.
