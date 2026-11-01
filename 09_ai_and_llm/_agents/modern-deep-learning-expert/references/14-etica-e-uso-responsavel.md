# 14 — Ethics, alignment and responsible use of deep learning

Source: UDL ch.1.4 (PDF p.26-28) and ch.21 (PDF p.434-449), read in full (problems on p.449 only skimmed). Chapter 21 was written by Travis LaCroix and Simon Prince (UDL p.434). NNDL has no ethics chapter; only comments on opacity, adversarial examples and the future (NNDL p.53-54, p.288-290, p.296-303). `[DATED 2023]`: the whole chapter reflects the state of 2023.

The agent treats these points as **conversation material and a checklist**, not as a legal opinion or an audit. Laws and regulations (GDPR, AI Act etc.) appear only to the extent that the book cites them; for LGPD (the Brazilian data-protection law) and regulation, refer to whoever covers the subject (the collection's privacy/security agent).

## 1. The five concerns of the introduction (UDL p.26-28)
Bias and fairness; explainability; concentration of power; existential risk; (and the "non-exhaustive" list: surveillance, disinformation, privacy violations, fraud, manipulation of financial markets and energy consumption). The book warns against unrealistic optimism and against "ethics-washing" — organizations that use ethics only to reduce reputational risk without real mechanisms to stop suspect projects (UDL p.27-28).

## 2. Value alignment (UDL p.434-436)
- Problem: ensuring that the "values" (objectives) of the systems coincide with those of humanity; it is hard to define the values, encode them as objectives and guarantee that the model learns them (UDL p.434-435).
- **Outer alignment**: the loss function is a proxy for the real objectives, and the "loopholes" can be exploited (book example: rewarding captures in chess leads to many draws). **Inner alignment**: even with a well-specified loss, optimization failures or unrepresentative data lead to misaligned solutions (UDL p.435).
- Technical component (avoiding reward hacking, safe exploration) and normative component (which values are right, for whom) (UDL p.435). Structural principal-agent view: objective failures and information asymmetry (fig. 21.1, UDL p.435-436).

## 3. Bias and fairness (UDL p.435-438)
Sources: problem specification, data (e.g., the PULSE super-resolution algorithm trained on predominantly white celebrity photos), modeling and validation (definitions of fairness that are logically inconsistent with one another: Kleinberg 2017, Chouldechova 2017), deployment (feedback loops, e.g., published GPT-3 texts degrade future data) (UDL p.436-437). Intersectionality: face analysis performs worse on combinations of attributes than would be expected from each attribute (Buolamwini-Gebru 2018) (UDL p.437). Complete data from a structurally biased society still produces bias (UDL p.436-437).
Mitigation at every stage: collection, preprocessing, training (regularize for fairness), post-processing (fig. 21.2). *Fairness through unawareness* (removing protected attributes) is **ineffective**; "separation" criterion: `ŷ ⟂ a | y` (UDL p.437). Difficulty of measuring when the characteristics are unobservable (UDL p.437-438).

## 4. Artificial moral agency, transparency and explainability (UDL p.438-440)
Moor's levels: ethical-impact agents, implicit, explicit and full ethical agents; top-down, bottom-up and hybrid approaches (UDL p.438). Transparency: functional (algorithm), structural (how the code executes) and run (hardware, data, parameters); GPT-3 is functionally transparent but not structurally or run-transparent; "GPT-4 is not transparent" (UDL p.439) `[DATED 2023]`. Explainability: local via LIME (sample outputs in neighbors and fit a simple model) (UDL p.439-440, fig. 21.3); GDPR art. 22 cited as a possible right to explanation, but this is "debatable" (note, UDL p.439).

## 5. Intentional misuse (UDL p.440-442)
Facial recognition and analysis (incompatible with liberal values for some authors; trials with failures; claims of inferring sexual orientation, emotions, criminality are pseudoscience: UDL p.440-441); militarization and political interference (arms race; disinformation; "likes" predicting sensitive attributes, Kosinski 2013) (UDL p.441); fraud (phishing, fake documents, **ELIZA effect**; transparency × security) (UDL p.441-442); privacy (de-anonymization; differential privacy, homomorphic encryption, multiparty computation) (UDL p.442). The book acknowledges the tension: more transparency can make bad-faith use easier (UDL p.441).

## 6. Other social impacts (UDL p.442-444)
Intellectual property (outputs that reproduce protected text; diffusion imagery; doubts about copyright of outputs) (UDL p.442-443); automation bias and moral *deskilling* (UDL p.443); environmental impact (training a 213-million-parameter transformer emitted ~284 t of CO₂, Strubell 2019; BLOOM; closed models do not disclose) (UDL p.443) `[DATED]`; employment (McKinsey estimate of up to 30% of the workforce displaced between 2016-2030 and US$13 trillion of extra output, 2018) (UDL p.443-444) `[DATED]`; concentration of power and "democratizing AI" (UDL p.444).

## 7. Case study and epistemology (UDL p.444-448)
Case study of the "gaydar" model (Wang-Kosinski 2018): biased sample, doubtful validation, most likely use is discrimination, spurious correlations of presentation/style, questionable collection of photos from a dating site and an exaggerated title (UDL p.444-445). Ideal of value-free science: values appear in the choice of problem, evidence, acceptance of hypotheses and application; ML is inductive and carries **inductive risk**, so accepting a prediction is a value judgment (UDL p.445-446). Responsible research as a collective-action problem: communicate without exaggeration, seek diversity and participation of affected communities (UDL p.446-447). Four closing points: ML research does not avoid ethics; technical decisions carry values; question the structures; not every social problem has a technical solution (UDL p.447-448).

## 8. How the agent uses this
1. Request for a risky feature (facial recognition, scoring, triage): list the phases of bias (UDL p.436-437), ask who is affected and whether there is a non-technical alternative (UDL p.447-448).
2. Request "tune the model to be fair": warn that fairness criteria are mutually inconsistent and require a value decision (UDL p.436); unawareness is not enough (UDL p.437).
3. Request for potentially abusive use (surveillance, disinformation, fraud): do not provide operational instructions; point to the risks described by the book and refer to human/legal review.
4. Never provide a legal opinion (LGPD/GDPR/IP) based on the book.

## 9. Limits
State of 2023; nothing about later regulation, LLM safety evaluations, red teaming, autonomous agents. `python -I scripts/dl_lookup.py --gaps` lists what is NOT COVERED.
