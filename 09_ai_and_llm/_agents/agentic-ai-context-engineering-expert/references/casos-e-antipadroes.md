# Cases and antipatterns

Each item says **what the texts support** and what is the package's inference. The "cases" below are examples from the texts themselves (travel agent and others), not real incidents.

## Architecture and tool antipatterns
| # | Antipattern | What the texts say | Origin |
|---|---|---|---|
| A1 | Agent that "plans" without tools and delivers a plan with invented data | The hierarchical example without tools produces a "completely fictitious" plan; integrating tools makes the plan factual (BAAS p.150-151) | from source |
| A2 | Assuming the LLM always knows when and how to use the tool | Smaller models err in knowing when to use it, assume wrong capabilities, choose the wrong sequence, ignore constraints; even capable ones have problems with long combinations and error recovery; test before deployment (BAAS p.152) | from source |
| A3 | Huge tool set with overlapping descriptions | Vague or overlapping descriptions cause failures; report of a performance drop above 30 tools and near-certain failure above 100 (DeepSeek-v3) `[DATED]` (CE2 p.18) | from source |
| A4 | Loading and unloading tools dynamically at each step | Breaks KV cache consistency and confuses references to earlier actions; alternative: stable list and logit mask (CE2 p.18-19) | from source |
| A5 | LLM manager for a complex flow | With an LLM manager the plan is arbitrary; it is "less flexible" and aimed at simple flows; with an agent manager the decomposition is controlled (BAAS p.148) | from source |
| A6 | Choosing a framework by the book's comparison | The comparison is based on the book's implementations and is `[DATED]` (BAAS p.159-160) | from source |
| A7 | Citing ch. 7 of BAAS as a source of guardrails | The preface says so (p.21, 214) but ch. 7 (p.186-211) has no section on it | from source (discrepancy) |

## Context and memory antipatterns
| # | Antipattern | What the texts say | Origin |
|---|---|---|---|
| B1 | Filling the context window | The performance of code agents tends to drop when the window exceeds about 50% occupancy (cited source), and irrelevant fragments distract and make inference more expensive `[DATED]` (CE2 p.16) | from source |
| B2 | Keeping only raw history with timestamps | There is no semantic structure and the sequence grows linearly (CE2 p.10) | from source |
| B3 | Free-text-only summaries when reasoning about relations is needed | Simple summaries lack structure, which makes linking events hard (CE2 p.13); fixed schemas help but can become inconsistent (CE2 p.14) | from source |
| B4 | Vector-only memory when auditing or editing is needed | Vectors are compact but not readable, which makes editing and inspecting hard (CE2 p.14) | from source |
| B5 | Timestamp or variation at the start of the system prompt | Invalidates the prefix cache; a stable prefix and append-only updates are recommended (CE2 p.18) | from source |
| B6 | Erasing errors from the agent's context | Keeping errors visible lets the model learn (CE2 p.19) `[DATED]` | from source |
| B7 | Few-shot action-observation examples all alike | The model tends to repeat patterns; small structured variations are suggested (CE2 p.19) | from source |
| B8 | Losing goals in long tasks | Keep a list of goals and recite it when updating to keep it in recent context (CE2 p.19) | from source |
| B9 | Lifelong memory without evaluation | There is no way to check contradictions, undo wrong updates and trace reasoning; errors propagate (CE2 p.18) | from source |
| B10 | Mixing context from several subtasks in the same window | Subagents with isolated windows reduce context "pollution" (CE2 p.12) | from source |
| B11 | Ignoring state transitions | Validate transitions, dependencies and rules before carrying out (BAAS p.197-198) | from source |

## Safety and trust antipatterns
| # | Antipattern | What the texts say | Origin |
|---|---|---|---|
| C1 | Letting the agent act on information it may have hallucinated | In agents, hallucination leads to actions; suggests real-time verification, action validation, confidence thresholds, multiple steps and human oversight (BAAS p.233-234) | from source |
| C2 | Full autonomy from the start | Progressive autonomy: start restricted and expand with demonstrated reliability (BAAS p.240) | from source |
| C3 | Evaluating the agent only by output quality | Agents require testing decision chains and action sequences (BAAS p.239); metrics of consistency, risk and adaptability (p.238) | from source |
| C4 | Actions without trail or reversal | Immutable action record, state versioning and checkpoints to revert; respect external policies (BAAS p.237-239) | from source |
| C5 | Privacy only at the data level | In agents, chains of decisions can reveal sensitive information even if each action seems compliant (BAAS p.235) | from source |
| C6 | Retrieved content treated as instruction | The texts do **not** discuss indirect prompt injection via retrieved context in detail. `[extrapolation]`: treat external data as data | package |

## Illustrative cases from the texts (to train reasoning)
- **Flight booking** (BAAS p.35-40): the agent asks for what is missing and calls the search and booking functions; parameter collection by LLM replaces string *parsing* (BAAS p.96).
- **Corporate trip with a US$ 2,000 limit** (BAAS p.202): illustrates task context and corporate policy in the decision.
- **Travel management system with safety layers** (BAAS p.238-239): financial limits, approval above a threshold, rollback with cancellation policy, monitoring.
- **Enterprise knowledge management** (BAAS p.251-252): three agents and an access control layer with auditing.
- **Deep research with context snapshots** (CE2 p.19): cycle of collection, compression, reasoning and reuse.
- **Gemini CLI with GEMINI.md** (CE2 p.19): hierarchical context by files and summary in a predefined format.
