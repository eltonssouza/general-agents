# NIST IR 8062: privacy engineering, security x privacy, privacy problems (chaps. 1-2 and appendices)

Source: NISTIR 8062, *An Introduction to Privacy Engineering and Risk Management in Federal Systems* (Jan/2017; 49 PDF pages). Pages = PDF; printed = PDF − 8 in the body (PDF 9 = printed 1). Labels: `[from source]` (on the cited PDF page), `[inference]`, `[extrapolation]`, `[DATED]`. Support material; not legal advice.

Context: it is an **introductory** report, for US federal agencies, that aligns privacy with systems engineering and the risk management of OMB A-130 (NIST8062 p.11). It is neither a law nor a complete method; see the limits at the end.

## Central idea
- `[from source]` "Privacy engineering" = a specialized discipline of systems engineering aimed at achieving the absence of conditions that could create problems for individuals, with unacceptable consequences, arising from the system when processing PII (NIST8062 p.6; repeated in NIST8062 p.18-19 and in the glossary, NIST8062 p.36).
- `[from source]` Three objectives (predictability, manageability, disassociability) and a risk model based on the problematic data action; it closes with a roadmap for future guidance (NIST8062 p.6). Details in `nist8062-objetivos-e-modelo-de-risco.md`.
- `[from source]` Building trustworthy systems requires translating high-level principles (FIPPs) into system requirements; NIST guidance had focused on confidentiality, integrity and availability (NIST8062 p.9).

## Security and privacy: relationship and difference
- `[from source]` Unauthorized access to PII is a subset of information security and a critical aspect of privacy, but there is a far less developed understanding of the privacy risks that go beyond it (NIST8062 p.9).
- `[from source]` Security and privacy are independent but related disciplines; a coordinated approach does not mean an identical approach (NIST8062 p.15). There are security issues unrelated to privacy (e.g., trade secrets) and privacy issues unrelated to security (NIST8062 p.15).
- `[from source]` Security tools, such as persistent activity monitoring, can create privacy concerns (NIST8062 p.16).
- `[from source]` In the security risk model, the concern is unauthorized activity that causes loss of confidentiality, integrity or availability; in the "byproduct" model, the processing of PII is planned and authorized, but generates implications for privacy (NIST8062 p.16; Figure 2, image, NIST8062 p.16).
- `[from source]` Security guides do not address the consequences of a poor consent mechanism, of purpose, of transparency or of changes in the use of PII when made by authorized personnel; hence privacy is not managed by security alone (NIST8062 p.16-17).
- `[inference]` Implication for the LGPD: complying with Art. 46 (security) does not exhaust the principles of purpose, necessity, transparency and suitability of Art. 6º (LGPD Art. 6º, I-III, p.3); the NIST list of problems shows why.

## Privacy problems
- `[from source]` "Privacy problem" = an adverse experience resulting from the processing of PII; the term was chosen to allow discussion without implying a legal conclusion (NIST8062 p.17).
- `[from source]` Examples: embarrassment or emotional distress from disclosure, economic loss from identity theft, stalking; from authorized processing: the discriminatory and stigmatizing effect of collection in public benefits, inaccurate data without correction (airline boarding), loss of trust that reduces adoption of beneficial services, impacts even on democratic institutions (NIST8062 p.17-18).
- `[from source]` Figure 3 (image, NIST8062 p.18), derived from Solove: **Loss of trust**; **Loss of self-determination** (loss of autonomy, of liberty, exclusion, physical harm); **Discrimination** (stigmatization, power imbalance); **Economic loss**. It is illustrative, not exhaustive (NIST8062 p.18).
- `[from source]` Appendix E gives examples beyond breach: cyber-physical systems (smart meters, smart cities, connected vehicles, body scanners, drones) (NIST8062 p.44-46); health (participant uncertainty about how much they consented; reidentification; 79% of respondents with concern) (NIST8062 p.46-47); big data and bias (ATS, ESTA, social media) (NIST8062 p.47-48).
- `[inference]` For use with the LGPD: the four categories of Figure 3 help describe the "harm" in a RIPD (LGPD Art. 5º, XVII, p.3) and think about the non-discrimination principle (LGPD Art. 6º, IX, p.4); the link is the agent's, not NIST's.

## Definition and systems engineering
- `[from source]` FIPPs are "value statements, not recipes" and, without an independent frame of reference, ad hoc application does not produce a repeatable and measurable process (NIST8062 p.19, third-party quotation). Being explicit about the desired outcome (systems that minimize problems from the processing of PII) gives a common purpose and allows requirements such as "limit the collection of a data set that could create problems without preventing the system's function" (NIST8062 p.19-20).
- `[from source]` The clause "unacceptable consequences" acknowledges risk acceptance: there is no system perfectly free of security risk, nor is it expected to eliminate all privacy risk (NIST8062 p.20).
- `[from source]` System boundary: privacy problems arise at any point in the handling of PII, from collection to disposal; the authorization boundary may exclude relevant stages; a programmatically expansive view may be needed (NIST8062 p.10; NIST8062 p.19).
- `[from source]` Systems engineering considers stakeholders throughout the life cycle; it can provide an evidence base to claim the desired level of trustworthiness and integrate other specialties (NIST8062 p.20-21).

## Risk management and compliance
- `[from source]` Risk management provides a common language and puts privacy risk on par with other risks (NIST8062 p.21). ISO and OASIS provide for privacy risk assessment, but do not teach how to conduct it (NIST8062 p.21-22). Assessments tend to check whether the notice exists, not whether people read it and benefit from it (NIST8062 p.22).
- `[from source]` OMB A-130 (2016) requires applying the RMF to privacy programs and emphasizes managing risk beyond compliance with laws (NIST8062 p.11).
- `[inference]` For the LGPD: Art. 6º, X (p.4) asks to demonstrate the *effectiveness* of the measures, which matches NIST's criticism of merely formal compliance; the reading is the agent's.

## Useful appendices
- Appendix A: the development process (2014 workshops, public comments); three key issues: communication gap between legal/policy, engineering and product management; lack of tools to measure effectiveness; risk as the driver (NIST8062 p.34).
- Appendix B: glossary (context, data actions, disassociability, manageability, PII, predictability, privacy control, privacy engineering, problematic data action, processing, risk, system privacy requirement, trustworthiness) (NIST8062 p.36-37).
- Appendix F: the nine FIPPs of A-130: Access and Amendment; Accountability; Authority; Minimization; Quality and Integrity; Individual Participation; Purpose Specification and Use Limitation; Security; Transparency (NIST8062 p.49).

## Limits of the NIST collection
- No PRAM, no NIST Privacy Framework, no control catalog, no risk matrix, no anonymization techniques (`python -I scripts/privacy_lookup.py --gaps --src NIST8062`). The report dates from 2017: everything later (NIST Privacy Framework 2020, SP 800-53 Rev. 5 with privacy controls) is `[extrapolation]` and `[DATED]`; see `extrapolacoes-e-datado.md`.
