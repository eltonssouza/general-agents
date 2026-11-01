# BAAS ch. 3: knowledge representation, reasoning, learning, utility and planning (classical view)

Source: BAAS (PDF p.76-98; printed = PDF − 25). Full reading. Planning specific to LLM agents (STRIPS, HTN, LLM-based planning) is in ch. 5 and lives in `04-baas-ferramentas-planejamento-e-frameworks.md`.

## 1. Knowledge representation (BAAS p.77-81)
- **[from source]** Defined as the way of structuring data so the agent can make inferences, solve problems and decide (p.77).
- **[from source]** Semantic networks: nodes (concepts) linked by labeled edges; they allow property inheritance and inference by graph traversal (p.77-78).
- **[from source]** *Frames*: attribute-value pairs organized in a hierarchy, with inheritance; they may contain procedures, and the book compares them to object-oriented programming classes (p.79-80).
- **[from source]** Logical representations (propositional, first-order, modal/temporal): formally rigorous, with guarantees of correctness (*soundness*) and completeness, which makes them attractive in critical domains; they are less intuitive (p.80-81).

## 2. Reasoning (p.81-86)
- **[from source]** Reasoning in agents is rarely monolithic: it combines styles; the example is a question-answering system that uses semantic *parsing*, deduction over a logical base and a neural model to write the answer (p.82).
- **[from source]** Deductive (from general premises to specific conclusions, p.82-83), inductive (from observations to probable generalizations, p.83-84) and abductive (inference to the best explanation, p.84-85). Abduction generates hypotheses that deduction and induction do not generate alone, but does not guarantee the correct explanation; it is usually validated by deduction (p.85).
- **[from source]** Limitations of abduction in agents: computational cost of generating and evaluating hypotheses, uncertainty, difficulty maintaining the representation, and scale and explainability problems (p.86).

## 3. Learning (p.86-87)
- **[from source]** Four mechanisms cited: supervised, unsupervised, reinforcement and transfer learning, generally used in combination (p.86-87).

## 4. Utility function (p.88-90)
- **[from source]** A utility function maps outcomes to real values that reflect preference; the rational agent chooses the action of highest expected utility, that is, the sum of the utilities of the possible outcomes weighted by their probabilities (p.88-89). *Fidelity note:* the mathematical notation of the formula does not appear in the extracted text; I rendered p.88 and it carries only the prose definition, so this package does **not** reproduce a formal utility formula beyond the verbal description.
- **[from source]** Numeric example (p.88-89): price utility = (1000 − price) × 0.05; comfort = rating × 10; convenience = rating × 15. For "Budget Airline" (price 300, comfort 3, convenience 2) the utility is **95.00**; for "Road Trip" (150, 4, 3) it is **127.50** (p.89). The weights 0.05/10/15 are, in the book's words, arbitrary (p.88). The code on p.88 has a variable-name inconsistency (`conv_utility` × `convenience_utility`); the book's numeric result matches the correct calculation. The script `ctx_calc.py utility` reproduces both numbers.
- **[from source]** Forms of utility: weighted score, constraint satisfaction, economic and multiplicative utilities (p.89). Difficulties: complex, context-dependent preferences, risk attitude, dependencies between attributes and uncertainty; techniques cited: preference elicitation, inverse reinforcement learning and learning from human feedback (p.89-90).

## 5. Classical planning algorithms (overview, p.90-92)
| Family | Idea | Book's observation | Page |
|---|---|---|---|
| Graph-based | state space and edge costs; search (DFS, BFS, Dijkstra) and optimal path (Bellman-Ford, A*) | state fixed beforehand; exponential growth | p.90-91 |
| Heuristic search | heuristics guide the search | trades optimality for efficiency; the heuristic is the challenge | p.91 |
| Monte Carlo tree search | random simulations build an asymmetric tree | *anytime* behavior; depends on a good simulation model; hard to tune | p.91-92 |
| Hierarchical | decomposes into goals and subgoals | subplan reuse and scalability, not always optimal | p.92 |
| Constraint satisfaction | variables and constraints, propagation | separates representation from the solving method | p.92 |

## 6. Generative AI empowering agents (p.93-96)
- **[from source]** Four contributions: data augmentation, context understanding, NLP and creative problem solving (p.93); integrated cycle: learning, knowledge representation, decision processes, generative models and feedback loops (p.93-94).
- **[from source]** "Popular" frameworks at the time of writing: LangGraph (described as the most popular), AutoGen, CrewAI and MetaGPT `[DATED]` (p.94). The book uses Python, LangGraph and OpenAI GPT models as the default (p.94).
- **[from source]** First LLM-based agent: function calling in the OpenAI SDK with the model `gpt-4-turbo` `[DATED]` (p.95); the LLM knows when the `book_flight` tool can be called and asks for the missing parameters, instead of relying on heuristic string *parsing* (p.96). Tools = mechanism for the agent to interact with the outside world (p.96).
