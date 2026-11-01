# Extrapolations and [DATED] items: what is OUTSIDE the collection (compiled LGPD + NIST IR 8062)

Rule: everything in this file is `[extrapolation]` (knowledge outside the two sources) or `[DATED]` (the text predates later changes). The agent uses this information only with the label, **without a page**, and recommends checking the current official source and consulting a lawyer/encarregado (DPO). Nothing here is legal advice. The norm numbers below come from the model's memory and **were not verified against an official source in this session**: confirm all of them before citing.

## 1. ANPD regulation (the law refers to regulation at several points)
The compiled LGPD text refers to ANPD regulation for: deadlines for fulfilling rights (LGPD Art. 18, §5º, p.9), portability (LGPD Art. 18, V, p.9), incident notification deadline (LGPD Art. 48, §1º, p.16), minimum security standards (LGPD Art. 46, §1º, p.15), duties and exemption of the encarregado (LGPD Art. 41, §3º, p.14), RIPD (LGPD Art. 38, p.14), standard clauses and international transfer (LGPD Art. 35, p.13) and fine methodology (LGPD Art. 53, p.18-19).
- `[extrapolation]` [DATED] The ANPD has issued resolutions on several of these points (the model's memory points to, among others: enforcement, small-scale agents, sanction calculation (dosimetria), security incident notification, encarregado, international transfer and standard clauses). **Numbers, deadlines and content must be confirmed on the official ANPD website before use.** In particular, the numeric deadline for incident notification is not in the text of the law (the expression "72 horas" (72 hours) does not appear) and must be sought in the resolution in force.
- `[extrapolation]` ANPD guidance documents (legal bases, processing agents and encarregado, information security) exist but are not part of the collection.

## 2. Amendments to the law itself
- `[from source]` The PDF records amendments from Laws 13.853/2019, 14.010/2020, 14.460/2022 and 15.352/2026 (`python -I scripts/privacy_lookup.py --amendments`; summary in `lgpd-disposicoes-finais-vigencia-e-alteracoes.md`).
- `[DATED]` The collection is the file provided, with no comparison against the official website; amendments after the PDF was drafted are not known. The institutional context of the ANPD (transformation into a special agency/autarchy) is `[extrapolation]`: the PDF only shows the 2026 wording (LGPD Art. 55-A, p.19).

## 3. Children and the digital environment
- `[extrapolation]` [DATED] There is later legislation specific to the protection of children and adolescents in digital environments (Estatuto Digital da Criança e do Adolescente, "Digital Statute of Children and Adolescents", a 2025 law according to the model's memory; number and effective date to be confirmed). Also, the age definition of child and adolescent comes from the ECA (Statute of the Child and Adolescent), not from the LGPD. The compiled LGPD only has Art. 14 (LGPD Art. 14, p.8).

## 4. International comparisons
- `[from source]` NIST IR 8062 merely cites the GDPR (EU Regulation 2016/679) as an example of emphasis on risk management, without explaining it (NIST8062 p.22), and cites ISO/IEC 29100 for the definition of "processing" (NIST8062 p.16).
- `[extrapolation]` Comparisons with the GDPR (for example, DPIA, 72-hour notification, data protection by design) belong to another source. Differences and similarities with the LGPD are a legal matter; do not assert them without a source.
- `[extrapolation]` ISO/IEC 27701 and other privacy management standards are not in the collection.

## 5. NIST after 2017
- `[extrapolation]` [DATED] After this report, NIST published a Privacy Framework (2020) and privacy risk assessment guidance (the model's memory cites PRAM), plus revision 5 of SP 800-53 with integrated privacy controls. None of these is in NIST IR 8062 (the terms PRAM, "Identify-P" and "Revision 5" are verified as absent: `python -I scripts/privacy_lookup.py --gaps --src NIST8062`). The only "Privacy Framework" in the text is the ISO one (NIST8062 p.21).
- `[DATED]` NIST IR 8062 foresees future guidance (NIST8062 p.32-33). Treat it as a 2017 conceptual introduction, not as the current state of NIST practice.

## 6. Technical controls and incident response
- `[extrapolation]` The LGPD asks for "apt" (aptas) measures (LGPD Art. 46, p.15) but does not list controls; NIST IR 8062 contains neither controls nor encryption (term "encryption" absent). Controls (encryption, MFA, access management, logs) and incident response processes must come from other sources (for example, the project's security collections). Label `[extrapolation]` and do not attribute to the LGPD or NIST.
- `[extrapolation]` Anonymization techniques (k-anonymity, differential privacy), tokenization, pseudonymization with keys: outside the collection.

## 7. Topics without coverage (see `--gaps`)
Artificial intelligence, cookies/tracking, marketing, worker data, facial recognition, right to be forgotten, joint control and sub-processors, data inventory/mapping: the compiled LGPD does not use these terms. Any answer about them is `[extrapolation]`, with a recommendation to consult ANPD regulation, case law and a lawyer.

## 8. Agent stance
- Answer first with what the text says (with Art./inciso and page), then mark the extrapolation in a separate block.
- Never invent a resolution number, deadline or amount; if you cannot verify, say "not verified in this session".
- When the user cites a recent norm or fact, accept the possibility, mark `[DATED]` and ask for the source.
