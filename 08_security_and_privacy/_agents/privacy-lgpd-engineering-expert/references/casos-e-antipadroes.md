# Illustrative cases and anti-patterns

**Hypothetical** scenarios created by the agent to exercise the text; they are not real cases and come neither from NIST nor from the LGPD. Each case separates what the text says (`[from source]`, with Art./inciso (item) and PDF page) from the engineering reading (`[inference]`) and from the limits (`[extrapolation]`). **This is not legal advice**: take it to a lawyer/encarregado (DPO).

## Cases

### C1. "We collect CPF (Brazilian taxpayer ID) and location to improve the service"
- `[from source]` Purpose must be specific, explicit and informed (LGPD Art. 6º, I, p.3); collection limited to the minimum necessary (LGPD Art. 6º, III, p.3); consent requires determined purposes and generic authorizations are void (LGPD Art. 8º, §4º, p.5).
- `[inference]` "Improve the service" is a generic purpose. Separate purposes per data item (location for delivery; CPF for the invoice), choose the legal basis for each one and eliminate whatever has no purpose.
- NIST framing: minimization -> manageability/disassociability (NIST8062 p.26); NIST requirement example: limit collection that may cause problems without preventing the function (NIST8062 p.20).

### C2. Consent hidden in the terms of use
- `[from source]` If written, consent must appear in a highlighted clause (LGPD Art. 8º, §1º, p.5); it is void if the information is misleading/abusive or was not presented beforehand with transparency (LGPD Art. 9º, §1º, p.6); the burden of proof lies with the controller (LGPD Art. 8º, §2º, p.5).
- `[inference]` Keep evidence (text version, date, user action) and allow revocation as easily as giving consent (LGPD Art. 8º, §5º, p.5).
- NIST: assess whether people read and understood the notice, not only whether it exists (NIST8062 p.26).

### C3. Marketing with health data "by legitimate interest"
- `[from source]` Legitimate interest is in Art. 7º, IX (p.4); the list in Art. 11, II (p.6) for sensitive data is a different one; §4º of Art. 11 prohibits sharing health data for economic advantage, with exceptions (LGPD Art. 11, §4º, p.7).
- `[inference]` Literal reading: legitimate interest does not appear in Art. 11. Strong risk hypothesis; refer to a lawyer before proceeding. Do a RIPD (data protection impact report) (LGPD Art. 38, p.14).

### C4. Leak of a user table
- `[from source]` Notify the ANPD and the data subjects if there is relevant risk or harm, within a reasonable period as defined by the ANPD, with six minimum elements (LGPD Art. 48, caput and §1º, p.16); severity considers whether the data was unintelligible (LGPD Art. 48, §3º, p.16); liability for a security failure depends on the measures of Art. 46 (LGPD Art. 44, sole paragraph, p.15).
- `[inference]` Quick triage: which fields, how many data subjects, what was protected, who decides to notify. Use `scripts/ripd_templates.py incidente`.
- `[extrapolation]` The numeric deadline, the ANPD form and technical containment guidance are outside the sources.

### C5. Customer asks to delete everything
- `[from source]` The data subject has the right to deletion of data processed with consent, except in the cases of Art. 16 (LGPD Art. 18, VI, p.9); retention is authorized for legal or regulatory obligation, research, transfer to a third party and exclusive use by the controller in anonymized form (LGPD Art. 16, I-IV, p.8); inform partners with shared use (LGPD Art. 18, §6º, p.9).
- `[inference]` Separate what has another basis and must be kept (tax obligation), answer with the justification (LGPD Art. 18, §4º, II, p.9), delete the rest, including replicas and backups within the "technical limits" (LGPD Art. 16, caput, p.8).

### C6. Analytics SaaS hosted outside Brazil
- `[from source]` International transfer only in the cases of Art. 33 (LGPD Art. 33, I-IX, p.12-13), with proven safeguards (clauses, corporate rules, seals) or another case; changes to the safeguards are communicated to the ANPD (LGPD Art. 36, p.13).
- `[inference]` Include remote support and subprocessors in the flow map.
- `[extrapolation]` Standard clauses currently in force and the adequacy list (see `extrapolacoes-e-datado.md`).

### C7. App for children with ranking and ads
- `[from source]` Specific and highlighted consent from one of the parents (LGPD Art. 14, §1º, p.8); reasonable verification efforts (LGPD Art. 14, §5º, p.8); do not condition a game on data beyond what is necessary (LGPD Art. 14, §4º, p.8); public and accessible information (LGPD Art. 14, §§2º and 6º, p.8).
- `[extrapolation]` [DATED] Later legislation on the children's digital environment; confirm.

### C8. Score model decides credit limit
- `[from source]` Right to review of solely automated decisions, including credit decisions, and to information about the criteria (LGPD Art. 20, caput and §1º, p.10); the ANPD may audit discriminatory aspects (LGPD Art. 20, §2º, p.10); non-discrimination (LGPD Art. 6º, IX, p.4).
- `[inference]` Record the model version and variables per decision so the criteria can be explained. NIST: bias and discrimination in analytic systems as a privacy problem (NIST8062 p.47).

### C9. Sensor collects detailed consumption "with authorization"
- `[from source]` NIST: the problem can arise from authorized processing (by-product model) (NIST8062 p.16); smart meters reveal household behavior (NIST8062 p.10); context determines whether the action is problematic (NIST8062 p.31). LGPD: suitability to the context (LGPD Art. 6º, II, p.3) and legitimate expectations (LGPD Art. 10, II, p.6).
- `[inference]` Model the data action "high-resolution collection" and check the need for the granularity, disassociability (aggregation) and predictability (understandable notice).

### C10. "We anonymize by hashing the CPF"
- `[from source]` Anonymized data stops being personal data, unless reversible with the controller's own means or with reasonable efforts (cost, time, technology) (LGPD Art. 12, caput and §1º, p.7); a behavioral profile may be considered personal (LGPD Art. 12, §2º, p.7).
- `[inference]` If a small set of possible values allows the CPF to be reconstructed, reversal is feasible with reasonable means; treat it as pseudonymized, with the additional information kept separately and controlled (LGPD Art. 13, §4º, p.7). The text does not discuss hash functions (the term "hash" does not appear).

### C11. Processor hires another supplier without notice
- `[from source]` The processor processes according to the controller's instructions (LGPD Art. 39, p.14); it is jointly liable if it breaches the law or the lawful instructions (LGPD Art. 42, §1º, I, p.14).
- `[inference]` The text does not use "suboperador" (sub-processor; term absent); regulate it by contract and check the flow of instructions. ANPD guidance: `[extrapolation]`.

### C12. The ANPD requests the RIPD of an operation
- `[from source]` Minimum content: types of data, collection methodology and security assurance methodology, analysis of measures, safeguards and mitigation (LGPD Art. 38, sole paragraph, p.14); trade and industrial secrets observed (LGPD Art. 38, caput, p.14).
- `[inference]` Use the template `scripts/ripd_templates.py ripd`; add the NIST analysis of data actions and problems (NIST8062 p.29-31) as an internal method, labeled.

### C13. Persistent monitoring of employee activity (security)
- `[from source]` NIST: security tools such as persistent monitoring can create privacy concerns (NIST8062 p.16). LGPD: purpose, necessity, transparency (LGPD Art. 6º, I, III, VI, p.3-4).
- `[extrapolation]` Rules specific to labor relations are not in the compiled text (the term "trabalhador" (worker) does not appear).

## Anti-patterns (and fix)
| Anti-pattern | Why it fails (text) | Fix |
|---|---|---|
| "Privacy = security" | NIST shows risks of authorized processing outside the scope of security (NIST8062 p.16-17) | Treat purpose, necessity, transparency with their own requirements |
| Consent for everything | Each operation needs a suitable legal basis (LGPD Art. 7º, p.4); sensitive data has its own regime (LGPD Art. 11, p.6) | Map the basis per operation; consent only where it fits |
| Notice "exists" but nobody reads it | NIST values effectiveness (NIST8062 p.22; NIST8062 p.26) and the LGPD requires clear and prominent information (LGPD Art. 9º, p.5) | Test comprehension of the notice |
| RIPD copied and filed away | The law asks for the controller's analysis of safeguards and mitigation (LGPD Art. 38, p.único, p.14) | Process-specific analysis, reviewed |
| Anonymization by label | Reversal with reasonable efforts voids the anonymization (LGPD Art. 12, p.7) | Reversal test and controls on additional information |
| Governance program on paper only | The law asks to demonstrate effectiveness (LGPD Art. 50, §2º, II, p.17) and continuous updating (LGPD Art. 50, §2º, I, h, p.17) | Evidence, audit and periodic reviews |
| Formal compliance without measuring effect | NIST criticizes compliance-only assessments (NIST8062 p.22) | Measure effectiveness (notice reading, fulfillment of rights) |
| Treating the LGPD<->NIST mapping as law | No source links one to the other (see `mapeamento-lgpd-nist.md`) | Label as an agent comparison |
