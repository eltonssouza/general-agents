# Step-by-step procedures (derived from the texts; steps organized by the agent)

Each procedure combines what the text requires (`[from source]`, with Art./inciso (item) and page) and the organization into steps (`[inference]`). Additions outside the two sources are `[extrapolation]`. Support material; **not legal advice**: validate with a lawyer/encarregado (DPO).

## P1. Determine whether the LGPD applies and to what
1. Check the alternative territorial criteria of Art. 3º (operation in Brazil; offer of goods/services or processing of individuals located in Brazil; data collected in Brazil) (LGPD Art. 3º, I-III, p.1).
2. Check the exceptions of Art. 4º (LGPD Art. 4º, I-IV, p.2). For academic purposes, arts. 7º and 11 still apply.
3. Result: scope per process. Output: `python -I scripts/compliance_checklist.py list --area escopo`.

## P2. Map processing operations and choose the legal basis
1. List operations (cycle: collection to deletion; Art. 5º X, p.3) and data (sensitive? children?).
2. For each operation, choose a basis from Art. 7º (or Art. 11 for sensitive data) and document it (LGPD Art. 7º, p.4; Art. 11, p.6).
3. If consent: highlighted clause, determined purpose, proof, easy revocation (LGPD Art. 8º, p.5). If legitimate interest: concrete situation, strictly necessary data, transparency (LGPD Art. 10, p.6).
4. Record the operations (LGPD Art. 37, p.14). Template: `python -I scripts/ripd_templates.py registro`.

## P3. Privacy by design (reading of Art. 46 §2º + NIST)
1. `[from source]` Security measures must be observed from design through execution (LGPD Art. 46, §2º, p.15).
2. Translate principles into verifiable system requirements (NIST8062 p.20; NIST8062 p.37): purpose per field, minimization, retention, fulfillment of rights.
3. Organize capabilities by predictability / manageability / disassociability (NIST8062 p.24-28) and keep evidence (NIST8062 p.25).
4. Delimit the system boundary with a broad view, from collection to disposal (NIST8062 p.10; NIST8062 p.19).
5. Output: `python -I scripts/compliance_checklist.py pbd`.

## P4. Risk assessment and RIPD
1. Describe the process and the data actions (NIST8062 p.31; minimum content of the RIPD: LGPD Art. 38, p.único, p.14).
2. For each action, identify potential problems (Figure 3, NIST8062 p.18) and the context (NIST8062 p.31).
3. Estimate likelihood and impact (NIST8062 p.30) and relate to the probability and severity required in governance (LGPD Art. 50, §1º, p.16). Scales are `[inference]`: NIST does not provide them.
4. Define measures, safeguards and mitigation mechanisms and the accepted residual risk (LGPD Art. 5º, XVII, p.3; NIST8062 p.30-31).
5. Generate the document: `python -I scripts/ripd_templates.py ripd --org "..." --processo "..."`. Who requests/orders it: the ANPD (LGPD Art. 38, p.14; Art. 10 §3º, p.6). Specific regulation: `[extrapolation]`.

## P5. Handle a data subject request
1. Receive the express request (LGPD Art. 18, §3º, p.9); at no cost (LGPD Art. 18, §5º, p.9).
2. Classify the right (Art. 18, I-IX) and locate data in all systems and processors.
3. Confirmation/access: simplified format immediately or a complete statement within 15 days (LGPD Art. 19, p.10).
4. If not possible, reply with the reasons or who the agent is (LGPD Art. 18, §4º, p.9).
5. Correction/deletion/anonymization/blocking: notify the agents with shared use (LGPD Art. 18, §6º, p.9).
6. Template: `python -I scripts/ripd_templates.py titular`.

## P6. Security incident and notification
1. Containment and technical investigation: outside the collection (`[extrapolation]`; use the security collection).
2. Assess whether there is relevant risk or harm (LGPD Art. 48, p.16) and consider whether the data was unintelligible (LGPD Art. 48, §3º, p.16).
3. If so: notify the ANPD and data subjects within a reasonable period as defined by the ANPD, with the six elements (LGPD Art. 48, §1º, I-VI, p.16). Numeric deadline: `[extrapolation]`/`[DATED]`.
4. Keep evidence of measures and cooperation (sanction criteria: LGPD Art. 52, §1º, p.18).
5. Template: `python -I scripts/ripd_templates.py incidente`.

## P7. International transfer
1. Map flows that cross borders (cloud, support, analytics).
2. For each flow, choose the Art. 33 case (LGPD Art. 33, I-IX, p.12-13) and keep the evidence; for consent, require prominence and prior information on the international nature (LGPD Art. 33, VIII, p.13).
3. Communicate changes to the safeguards to the ANPD (LGPD Art. 36, p.13). Standard clauses in force: `[extrapolation]`.

## P8. Governance program
1. Assemble the elements of Art. 50 §2º, I (a-h): commitment, scope, adaptation, systematic risk assessment, relationship of trust, oversight, incident response, continuous updating (LGPD Art. 50, §2º, I, p.16-17).
2. Be able to demonstrate effectiveness to the ANPD (LGPD Art. 50, §2º, II, p.17).
3. Appoint and publish the encarregado (LGPD Art. 41, p.14).
4. Periodic review; publish good practice rules if applicable (LGPD Art. 50, §3º, p.17).

## P9. Citing the law in a document
1. Cite Art., paragraph and inciso (item) and state that the text consulted is the compiled one from the PDF, with the date (see `lgpd-disposicoes-finais-vigencia-e-alteracoes.md`).
2. If the article was amended, mention the amending law (`python -I scripts/privacy_lookup.py --amendments --art N`).
3. Check the current wording at Planalto: `[DATED]`.
