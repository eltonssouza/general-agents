# CE2 §1-3: formal definition of context engineering, entropy and the four eras

Source: CE2 = *Context Engineering 2.0: The Context of Context Engineering* (Qishuo Hua et al., SII-GAIR, arXiv:2510.26493v1 [cs.AI], 30/10/2025; 28 pp.). **PDF page = printed page** (p.1 = cover/abstract). The body (p.1-21) was read in full; p.22-28 are references. Formulas checked by rendering p.5 and p.12. This is a **position/conceptual survey paper**, `[DATED]` (Oct/2025); it presents no experiments of its own nor benchmarks for context engineering. Names of systems and products cited (Claude Code, Gemini CLI, Manus, Letta, MemOS etc.) reflect the state of 2025.

## 1. The central thesis (CE2 p.1-4)
- **[from source]** Context engineering is not a recent invention of the agent era: the paper states that related practices have existed for more than 20 years, since the 1990s, going through phases tied to the level of machine intelligence (HCI → human-agent interaction → possibly human-level or superior intelligence) (p.1).
- **[from source]** Practice definition (introduction): designing, organizing and managing contextual information so that machines act in line with human intent; techniques cited as instances: prompt engineering, RAG, tool calling and long-term memory mechanisms (p.3).
- **[from source]** "Context" is usually defined narrowly (dialogue history, system prompts or input from the agent's environment); the paper argues for a broader definition (p.3). It also considers the current narrowing a step back relative to the era 1.0 theories (p.7).

## 2. Context engineering as entropy reduction (p.3-4)
- **[from source]** Humans "fill in gaps" in communication; machines, today, do not. That is why context needs to be pre-processed: the central effort is to transform high-entropy contexts and intents into low-entropy representations the machine understands (p.3).
- **[from source]** The more intelligent the machine, the more natural context engineering becomes and the lower the cost of human-machine interaction (p.4; Fig. 1 on p.1).
- **[inference]** "Entropy" is used as a metaphor, with no quantitative measure in the paper. There is no formula or metric for context entropy; the script `ctx_calc.py` does **not** compute this.

## 3. Formal definitions (p.4-5)
Checked visually on p.5.
1. **Entity and characterization:** let E be the space of entities (users, applications, objects, environments) and F the space of characterizing information; `Char: E → P(F)` returns the set of information that characterizes entity e (p.4).
2. **Interaction:** any observable engagement between user and application, explicit (clicks, commands) or implicit (attention, environment adjustments) (p.5).
3. **Context:** C is the union of Char(e) for the entities e in Erel, the subset of entities considered relevant to the interaction (p.5; Dey's (2001) definition is cited as the basis).
4. **Context engineering:** a systematic process of designing and optimizing the **collection, storage, management and use** of context to improve machine understanding and performance; `CE: (C, T) → f_context`, where T is the task or domain and `f_context(C) = F(φ1, …, φn)(C)` is a composition of operations (parallel, iterative, conditional) (p.5).
- **[from source]** The eight operations φ cited for era 2.0: collect, store and manage, represent in a consistent and interoperable format, handle multimodality, integrate and reuse past context ("self-baking"), select relevant elements, share across agents or systems and adapt dynamically from feedback (p.5).
- **[from source]** The paper's example for Erel: user, application (Gemini CLI), terminal environment, external tools, memory modules and model service; Char(e) includes the prompt, system instructions, working directory, available plugins, session history and model capabilities (p.4-5).
- **[inference]** Practical usefulness: the definition serves as an **inventory** of what goes into an agent's context. The script `agent_spec.py` uses these categories in the context fields; this is our application, not the paper's.

## 4. The four eras (p.6-8, Table 1)
| Era | Period in the paper | Intelligence | Characteristic | Page |
|---|---|---|---|---|
| 1.0 | 1990s-2020 | primitive computation | structured, predefined inputs; humans as "intent translators" | p.6-7 |
| 2.0 | 2020-present | agent-centered (GPT-3 marks the start) | natural language, ambiguity, reasoning over gaps | p.6, 8 |
| 3.0 | future | human-level | interpreting social and emotional cues; collaborative "peers" | p.6 |
| 4.0 | speculative | superhuman | the machine builds context for the human and reveals unexpressed needs ("God's-eye view") | p.6 |

- **[from source]** Fig. 1: "Context as translation / instruction / scenario / world" for 1.0-4.0; the paper declares it is in era 2.0 in transition to 3.0 (p.1).
- **[from source]** Table 1 (p.6): typical systems of 1.0 (Context Toolkit, Cooltown, ContextPhone) and of 2.0 (ChatGPT, LangChain, AutoGPT, Letta); core mechanisms: sensor fusion and rule-based triggers (1.0) × prompting, RAG, CoT and memory agents (2.0); tolerance of raw context and human-likeness: relatively low (1.0) × high (2.0).
- **[from source]** Era 1.0 (p.7): Weiser (1991) and ubiquitous computing; context-aware computing; Dey's (2001) definition of context; **Context Toolkit** with five abstractions: *Widgets* (encapsulate sensors), *Interpreters* (derive meaning), *Aggregators* (integrate sources), *Services* (application access) and *Discoverers* (component registration and discovery) (p.7).
- **[from source]** Era 2.0 (p.8): more diverse sensors (Table 2, p.8), tolerance of "human-native signals" (free text, image, video) and a shift from "context-aware" systems (rules such as "if at the office, mute the phone") to "context-cooperative" ones, which interpret what the user does and collaborate (p.8).
- **[inference]** Eras 3.0 and 4.0 are speculative (the paper labels them as such, p.6); do not use them as a technical forecast.

## 5. Recommended uses
- Explain to a team why "context" is more than chat history: see §3, p.5.
- Structure a review as **collection → management → use** (p.4): see `10-ce2-coleta-e-gestao-de-contexto.md` and `11-ce2-uso-praticas-e-desafios.md`.
- **[extrapolation]** "Context engineering" is today also used more narrowly (assembling the prompt at each agent step); the paper adopts a broader definition, which may diverge from other uses.
