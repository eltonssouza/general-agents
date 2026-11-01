# LGPD: data subject rights (Art. 17 to 22; links to Art. 6 IV, 8 §5º, 9)

Pages = PDF (9-11). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Not legal advice; refer to a lawyer/encarregado (DPO).

## Ownership and list of rights
- `[from source]` Every natural person is assured ownership of their data and the fundamental rights of freedom, intimacy and privacy (LGPD Art. 17, p.9).
- `[from source]` The data subject may obtain from the controller, at any time and upon request (LGPD Art. 18, caput, p.9):
  - I confirmation of the existence of processing; II access to the data (LGPD Art. 18, I-II, p.9);
  - III correction of incomplete, inaccurate or outdated data (LGPD Art. 18, III, p.9);
  - IV anonymization, blocking or deletion of unnecessary, excessive or non-compliant data (LGPD Art. 18, IV, p.9);
  - V portability to another provider, upon express request, under ANPD regulation and observing trade and industrial secrets (wording of Law 13.853/2019) (LGPD Art. 18, V, p.9); portability does not include data already anonymized by the controller (LGPD Art. 18, §7º, p.9);
  - VI deletion of data processed with consent, except in the cases of Art. 16 (LGPD Art. 18, VI, p.9);
  - VII information on the public and private entities with which shared use took place; VIII information on the possibility of not giving consent and its consequences; IX revocation of consent (LGPD Art. 18, VII-IX, p.9).

## How the right is exercised (Art. 18 §§)
- `[from source]` Right to petition the ANPD against the controller (LGPD Art. 18, §1º, p.9) and also before consumer protection bodies (LGPD Art. 18, §8º, p.9).
- `[from source]` The data subject may object to processing exempt from consent in case of breach of the law (LGPD Art. 18, §2º, p.9).
- `[from source]` Exercise by express request of the data subject or a legally constituted representative to a processing agent (LGPD Art. 18, §3º, p.9); fulfilled at no cost, within the deadlines and terms of the regulation (LGPD Art. 18, §5º, p.9).
- `[from source]` If the measure cannot be adopted immediately, the controller replies: (I) that it is not a processing agent of the data and, if possible, indicates who is; or (II) states the factual or legal reasons that prevent it (LGPD Art. 18, §4º, p.9).
- `[from source]` Whoever corrects, deletes, anonymizes or blocks data immediately informs the agents with which shared use took place, so that they repeat the procedure, except in case of proven impossibility or disproportionate effort (LGPD Art. 18, §6º, p.9; wording of Law 13.853/2019).

## Access and portability in format (Art. 19)
- `[from source]` Confirmation or access: (I) in simplified format, immediately; or (II) by a clear and complete statement with the origin of the data, absence of record, criteria used and purpose, within 15 days of the request, observing trade and industrial secrets (LGPD Art. 19, I-II, p.10).
- `[from source]` Data stored in a format that favors the exercise of the right of access (LGPD Art. 19, §1º, p.10). Delivery by secure and suitable electronic means or printed, at the data subject's choice (LGPD Art. 19, §2º, p.10). If the origin is consent or contract, the data subject may request a full electronic copy in a format allowing subsequent use, under ANPD regulation (LGPD Art. 19, §3º, p.10). The ANPD may rule differently on the deadlines by sector (LGPD Art. 19, §4º, p.10).
- `[inference]` Engineering requirement: §1º implies designing storage to be queryable by data subject (search key per data subject, structured export). See M04 in `mapeamento-lgpd-nist.md` (manageability).

## Automated decisions (Art. 20)
- `[from source]` The data subject may request review of decisions made solely on the basis of automated processing that affect their interests, including decisions to define a personal, professional, consumer and credit profile or aspects of personality (LGPD Art. 20, caput, p.10; wording of Law 13.853/2019).
- `[from source]` The controller provides, when requested, clear and adequate information on the criteria and procedures of the decision, observing trade and industrial secrets (LGPD Art. 20, §1º, p.10). If it refuses on grounds of secrecy, the ANPD may audit discriminatory aspects (LGPD Art. 20, §2º, p.10). §3º appears as vetoed (LGPD Art. 20, §3º, p.10).
- `[inference]` The compiled text does not say that the review must be done by a natural person. In design, provide a decision trail (variables, model version) to be able to explain criteria. NIST IR 8062 treats biases in analytic systems as a privacy problem, without proposing a right of review (NIST8062 p.47).

## Others
- `[from source]` Data on the data subject's regular exercise of rights may not be used to their detriment (LGPD Art. 21, p.10). The defense of rights may be exercised in court, individually or collectively (LGPD Art. 22, p.10).
- `[from source]` Free access principle: facilitated and free consultation on form, duration and completeness (LGPD Art. 6º, IV, p.3). The information in Art. 9 (p.5) feeds the notices.
- `[inference]` Handling flow (rights desk): receive, authenticate the requester, classify the right, locate data in all systems (including processors), answer within the deadline, propagate the change, record evidence. Generate a template with `python -I scripts/ripd_templates.py titular`.
- `[extrapolation]` Deadlines for the other items beyond Art. 19, ANPD regulations on data subject rights and on portability: check the regulation in force (the text refers to regulation). The encarregado receives the complaints (LGPD Art. 41, §2º, I, p.14).
