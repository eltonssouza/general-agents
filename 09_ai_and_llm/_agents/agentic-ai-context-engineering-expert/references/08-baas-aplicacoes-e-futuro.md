# BAAS chs. 10-11: multi-agent applications and perspectives

Source: BAAS (PDF p.246-272; printed = PDF − 25). Full reading. **Caution:** the examples of companies and products (Adobe Firefly, Universal Music, Salesforce Agentforce, GitHub Copilot Chat, Boston Dynamics, MIT RoboBrain, JPMorgan LOXM, Two Sigma Venn, HealthPal, DeepPill, Siemens MindSphere etc.) are **claims of the book, not verified** by this package, and `[DATED]` (2025). Do not use them as facts about real products.

## 1. Pattern of the four case studies
Each case in ch. 10 follows: problem statement, approach with several specialized agents, environment and external systems, "why it is better". They serve as **agent decomposition templates**, not as performance evidence (the book offers no measurements).

| Case | Agents | Environment/external systems | Page |
|---|---|---|---|
| Film previsualization | director, technical supervisor, visualization | asset database, production management, rendering API, version control, collaboration platform | p.248-250 |
| Enterprise knowledge management | query understanding, knowledge navigation (tracks provenance), answer synthesis | internal systems (documents, chat, projects, email, repositories, CRM), external APIs, **access control layer** (roles, classification, authentication, audit log) | p.251-252 |
| Manufacturing cell | planning and coordination, robot control, quality and optimization, exception handling | robots, vision, PLCs, MES/ERP/QMS, digital twin | p.254-256 |
| Supply chain | strategic planning, operational optimization, risk management, sustainability | ERP, TMS, WMS, external data, integration layer | p.258-260 |

- **[from source]** In the knowledge management case the book explicitly includes an access control layer with an audit log (p.252): it is the only application in ch. 10 in which permissions appear in the architecture.
- **[from source]** The agents collaborate through "shared context understanding", feedback loops and real-time adaptation (p.249, 252, 255, 259), without specifying the mechanism. For context-sharing mechanisms, see CE2 p.14-15.
- **[from source]** Capabilities of language agents: context retention, task execution, adaptive interaction, multimodal understanding (p.250-251).

## 2. Ch. 11: conclusion and future (p.264-272)
- **[from source]** Recap: reactivity, initiative and social ability; CWD as a practical structure (p.265).
- **[from source]** Trends: multimodality, language understanding, reinforcement learning (p.266-267). Models cited (GPT-4o, o1, RoboCat) are `[DATED]`.
- **[from source]** AGI: the book says AGI does not exist and that current systems are narrow AI (p.264, 268-269). Challenges: meta-learning (MAML), transfer learning, *few-shot*, explainability and reliability/safety "with safeguards and constant monitoring" (p.270).
- **[inference]** This chapter is forward-looking and high-level; do not use it for technical decisions.
