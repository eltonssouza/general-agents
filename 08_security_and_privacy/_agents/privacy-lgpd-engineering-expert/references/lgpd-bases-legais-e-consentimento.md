# LGPD: legal bases for processing, consent, information to the data subject and legitimate interest (Art. 7 to 10)

Pages = PDF (4-6). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Not legal advice; refer to a lawyer/encarregado (DPO).

## The list in Art. 7 (ordinary personal data)
`[from source]` Processing "may only" occur in the cases below (LGPD Art. 7º, caput, p.4):

| Inciso (item) | Legal basis | Cite |
|---|---|---|
| I | consent by the data subject | (LGPD Art. 7º, I, p.4) |
| II | compliance with a legal or regulatory obligation by the controller | (LGPD Art. 7º, II, p.4) |
| III | public administration: public policies provided for in laws, regulations, contracts, agreements (subject to Chap. IV) | (LGPD Art. 7º, III, p.4) |
| IV | studies by a research body, with anonymization whenever possible | (LGPD Art. 7º, IV, p.4) |
| V | performance of a contract or preliminary procedures, at the request of the data subject | (LGPD Art. 7º, V, p.4) |
| VI | regular exercise of rights in judicial, administrative or arbitration proceedings | (LGPD Art. 7º, VI, p.4) |
| VII | protection of the life or physical safety of the data subject or a third party | (LGPD Art. 7º, VII, p.4) |
| VIII | health protection, exclusively by health professionals, health services or the health authority (wording of Law 13.853/2019) | (LGPD Art. 7º, VIII, p.4) |
| IX | legitimate interests of the controller or a third party, except where the data subject's fundamental rights and freedoms prevail | (LGPD Art. 7º, IX, p.4) |
| X | credit protection | (LGPD Art. 7º, X, p.4) |

- `[from source]` §§1º and 2º appear as revoked in the compiled text (LGPD Art. 7º, §§1º-2º, p.4).
- `[from source]` Publicly accessible data: consider the purpose, good faith and public interest that justified making it available (LGPD Art. 7º, §3º, p.5). Data manifestly made public by the data subject does not require consent, safeguarding rights and principles (LGPD Art. 7º, §4º, p.5).
- `[from source]` Communicating or sharing data with other controllers, when the basis was consent, requires specific consent for that purpose, except for legal exemptions (LGPD Art. 7º, §5º, p.5).
- `[from source]` Exemption from consent does not release the agents from the other obligations, especially the principles and the data subject's rights (LGPD Art. 7º, §6º, p.5). Further processing of data from §§3º and 4º may have new purposes, with legitimate and specific purposes and preservation of rights (LGPD Art. 7º, §7º, p.5; added by Law 13.853/2019).
- `[inference]` The text does not rank the bases: each operation needs at least one basis; record which one (see Art. 37, p.14). It is not correct to treat "consent" as the default basis.

## Consent (Art. 8 and 9)
- `[from source]` In writing or by another means that shows the data subject's will; if written, in a highlighted clause (LGPD Art. 8º, caput and §1º, p.5). The burden of proof lies with the controller (LGPD Art. 8º, §2º, p.5). Processing with defective consent is prohibited (LGPD Art. 8º, §3º, p.5).
- `[from source]` It must refer to determined purposes; generic authorizations are void (LGPD Art. 8º, §4º, p.5).
- `[from source]` It may be revoked at any time, by express statement, through a free and facilitated procedure; prior processing is ratified as long as there is no deletion request (LGPD Art. 8º, §5º, p.5).
- `[from source]` If the information in items I, II, III or V of Art. 9º changes, the controller informs with prominence and the data subject may revoke if they disagree (LGPD Art. 8º, §6º, p.5).
- `[from source]` The data subject has the right to easy access to clear, adequate and prominent information about: specific purpose; form and duration; identification and contact of the controller; shared use and its purpose; responsibilities of the agents; data subject rights with explicit mention of Art. 18 (LGPD Art. 9º, I-VII, p.5).
- `[from source]` Consent is void if the information has misleading or abusive content or was not presented beforehand with transparency, clearly and unambiguously (LGPD Art. 9º, §1º, p.6). A change of purpose that is incompatible requires prior information and makes revocation possible (LGPD Art. 9º, §2º, p.6). If processing is a condition for supplying a product/service or exercising a right, inform with prominence and explain how to exercise the rights (LGPD Art. 9º, §3º, p.6).

## Legitimate interest (Art. 10)
- `[from source]` It only supports processing for legitimate purposes, based on concrete situations, which include (without being limited to): support and promotion of the controller's activities; protection of the data subject's regular exercise of rights or provision of services that benefit them, respecting legitimate expectations and fundamental rights and freedoms (LGPD Art. 10, I-II, p.6).
- `[from source]` Only strictly necessary data (LGPD Art. 10, §1º, p.6); transparency measures (LGPD Art. 10, §2º, p.6); the ANPD may request a RIPD (LGPD Art. 10, §3º, p.6).
- `[inference]` In engineering: document the concrete situation, the need for each data item, the data subject's expectation and what the data subject could contest; keep the Art. 37 record (p.14), which the law especially asks for under this basis.
- `[inference]` The text does not describe a named "balancing test" or its steps (the expression "teste de proporcionalidade" (proportionality test) does not appear; see `scripts/privacy_lookup.py --gaps`); ANPD guidance on the subject is `[extrapolation]`.

## Pitfalls `[inference]`
- Treating a pre-ticked box, global acceptance of the terms of use or "bundled" consent as valid: the text requires a highlighted clause and determined purposes, and voids generic authorizations (Art. 8º §1º and §4º, p.5).
- Forgetting to propagate revocation to processors and partners (Art. 18 §6º, p.9, covers correction, deletion, anonymization and blocking).
- Using legitimate interest without a record and without transparency.
- Reusing publicly accessible data for any purpose: Art. 7º §3º (p.5) requires considering the purpose that justified the publicity.

## Links
- Sensitive data and children: `lgpd-dados-sensiveis-anonimizacao-criancas.md`. Rights: `lgpd-direitos-do-titular.md`. Checklist: `python -I scripts/compliance_checklist.py list --area bases`.
