# BAAS chs. 8-9: trust, safety, action guardrails, ethics, privacy and agent testing

Source: BAAS (PDF p.214-245; printed = PDF − 25). Full reading. **Warning:** the book treats agent safety at a conceptual level and with product lists (`[DATED]`, 2025). It does **not** offer a formal threat model, nor a prompt injection taxonomy, nor concrete security tests. This package does not replace a security review, authorized penetration testing or legal opinion; for systems security in general use the agent `security-engineering-expert` (collection 09).

## 1. Ch. 8: trust (p.214-229)
- **[from source]** Trust is multivariate: reliability, transparency and alignment with expectations and values; lack of trust leads to skepticism, misuse and less feedback and data (p.215-216).
- **[from source]** Transparency at two levels: **algorithmic** (architecture, training data, biases, for developers and regulators) and **presentation**/explainability (how the AI communicates its reasoning to the user) (p.216). XAI techniques cited: attention visualization, saliency maps and natural-language explanations (p.216-220; the book's notebook uses a BERT model for attention and saliency, p.217-219). The book says saliency serves computer vision more and natural-language explanations serve text generation more (p.221).
- **[from source]** Uncertainty and bias (p.221-222, 226-227): communicate uncertainty (for example, several options with confidence scores), probabilistic modeling, Bayesian inference and uncertainty quantification; bias via representative data, monitoring, debiasing algorithms, adversarial training and human oversight.
- **[from source]** Output communication (p.222-223): label content as AI-generated, give context and sources, guide users to verify facts. User control and consent (p.223-224). Ethics: fairness, privacy (differential privacy, secure multi-party computation, encryption) and intellectual property (p.224-225).
- **[inference]** For an agent that acts, the explainability of ch. 8 is complementary to the decision logging of ch. 9: the book links the two when speaking of "decision auditing" (p.232-233).

## 2. Ch. 9: agent-specific risks (p.231-237)
The book insists that the risks of generative AI **become more serious** when the system acts autonomously (p.231).
| Risk | Book's idea | Mitigations cited | Page |
|---|---|---|---|
| Adversarial attacks | manipulated inputs corrupt decisions and leak data; in agents they can cause harmful actions | adversarial training, input sanitization, anomaly detection; for agents: action verification, decision auditing, multi-step authentication | p.231-232 |
| Bias and discrimination | agents apply bias in decisions and actions, at scale | decision auditing, accountability structures, real-time bias detection, diverse stakeholders | p.232-233 |
| Hallucination | the agent may act on invented information | real-time verification, action validation, *fallback* procedures, uncertainty-sensitive decisions, multi-step verification, confidence thresholds, human oversight | p.233-234 |
| Privacy violation | agents access and decide on personal data; chains of decisions may reveal what should remain hidden | real-time privacy monitoring, privacy-aware decision protocols, adapted differential privacy | p.234-235 |
| Intellectual property | agents apply learned material at machine scale and speed | provenance monitoring, IP impact assessment before acting, automatic license verification | p.235-237 |

- `[DATED]` The book cites tools (Copyleaks, SynthID, Truepic, WIPO PROOF "discontinued" etc.) and cases (lawsuit against Stability AI, 2022) on p.236; do not treat them as the current state.

## 3. Safety and accountability in agents (p.237-240)
Central considerations (p.237-238): **action limits**, **decision verification**, **rollback capability**, **real-time monitoring**, **human-in-the-loop feedback** and **performance metrics**.
- **[from source]** *Action limits*: governance policies, RBAC and context-sensitive permissions to prevent unauthorized actions, especially in finance and healthcare (p.237). The book cites product features such as OpenAI Function Calling and Amazon Bedrock Guardrails `[DATED]` (p.237).
- **[from source]** *Decision verification*: multi-step validation, neuro-symbolic reasoning, constraint satisfaction and logical verification before executing (p.237).
- **[from source]** *Rollback*: immutable record of actions (event sourcing), versioning of the decision state and *checkpoints* to revert (p.237); product examples `[DATED]`.
- **[from source]** *Monitoring*: anomaly and *drift* detection, alerts or corrective actions, XAI to explain decisions (p.238).
- **[from source]** *HITL*: RLHF and hybrid human-AI flows that escalate decisions that require human judgment (p.238).
- **[from source]** *Metrics*: beyond output quality, measure decision consistency, ethical alignment, risk assessment and adaptability, supported by auditing and causal inference; tools cited `[DATED]` (p.238).
- **[from source]** Example of safety layers for a corporate travel system (p.238-239): financial limits for changes, restriction to risky destinations, multi-step checks and human approval above thresholds, *rollback* that respects cancellation policies, monitoring of atypical patterns and decision quality metrics. Figure 9.1 (p.239) was not inspected.
- **[from source]** **Agent testing** should evaluate *decision chains and action sequences*, in simulated scenarios with interlinked decisions and unexpected situations, and not only output quality (p.239). Human oversight starts monitoring decision patterns (p.239).
- **[from source]** Safe learning (p.240): *sandbox*, **progressive autonomy**, safety limits by action risk, continuous validation and emergency protocols. Explicit ethical constraints (constraint programming, ethical rule engines, RL with ethical reward), HITL, periodic ethical audits and *red teaming* for edge cases (p.240).

## 4. Ethics, privacy and deployment security (p.241-243)
- **[from source]** Human-centered design, accountability (multidisciplinary boards), privacy by design (minimization, k-anonymity, pseudonymization, federated learning, homomorphic encryption, SMPC; mentions GDPR, CCPA, HIPAA), diverse stakeholders (p.241-242).
- **[from source]** Data governance, role-based access control, PCI DSS, regular security risk assessments, secure coding standards, testing and audits (including penetration testing), user education, incident response plan (containment, investigation, notification), adversarial training and anomaly detection (p.242-243).

## 5. What to do with this (package rules)
- **[from source]** Autonomy should be calibrated: start restricted and expand with demonstrated reliability (p.240); require a human in high-risk decisions (p.238, 244).
- **[inference]** Agent review checklist: action limits, verification before effect, audit trail and reversal, monitoring, human oversight, action-chain tests. The script `agent_checklist.py` organizes these items with pages.
- **[extrapolation]** Current agent security patterns (indirect prompt injection via tools, per-tool credential isolation, allowlists) are **not** in these texts as a detailed technique. BAAS cites prompt injection once, in the context of training data extraction (p.46), and CE2 suggests least-privilege permissions per subagent (p.12). Use current security sources.
