# LGPD: foundations, scope, definitions and principles (Art. 1 to 6)

Source: Lei 13.709/2018, compiled text from the PDF (LGPD). Pages = PDF (1-4). Labels: `[from source]` checked against the cited page; `[inference]`; `[extrapolation]`; `[DATED]`. **Not legal advice**: refer to a lawyer/encarregado (DPO).

## Subject matter and foundations
- `[from source]` The law governs the processing of personal data, including in digital media, by a natural person or a legal entity under public or private law, to protect freedom, privacy and the free development of personality (LGPD Art. 1º, p.1). The general rules are of national interest and bind the Union, States, the Federal District and Municipalities (LGPD Art. 1º, sole paragraph, p.1; paragraph added by Law 13.853/2019).
- `[from source]` Seven foundations: privacy; informational self-determination; freedom of expression, information, communication and opinion; intimacy, honor and image; economic and technological development and innovation; free enterprise, free competition and consumer protection; human rights, dignity and citizenship (LGPD Art. 2º, I-VII, p.1).

## Territorial application (Art. 3)
- `[from source]` Applies to any processing operation, regardless of the medium, the country of the headquarters or where the data is located, if: (I) the operation takes place in national territory; (II) the activity aims to offer goods or services or to process data of individuals located in national territory; or (III) the data was collected in national territory (LGPD Art. 3º, I-III, p.1). Data is considered collected in Brazil when its data subject is in Brazil at the time of collection (LGPD Art. 3º, §1º, p.1).
- `[from source]` §2º removes item I for the processing in Art. 4º, IV (LGPD Art. 3º, §2º, p.1).
- `[inference]` The items are alternatives ("or"): one is enough for the law to apply; therefore a foreign company offering a service to people in Brazil is within scope. Confirm case by case with a lawyer.

## Exceptions (Art. 4)
- `[from source]` Does not apply to: exclusively private and non-economic purposes; exclusively journalistic and artistic purposes, or academic ones (for academic purposes arts. 7º and 11 apply); public security, national defense, state security, criminal investigation and prosecution; data coming from abroad without communication, shared use with Brazilian agents or transfer to a third country, provided the country of origin has adequate protection (LGPD Art. 4º, I-IV, p.2).
- `[from source]` For item III, specific legislation with proportional and strictly necessary measures is required (§1º); processing by a private-law person is prohibited, except under the guardianship of a public-law person (§2º); the ANPD issues opinions and requests impact reports (§3º); the entire database may never be processed by a private party, except a company with fully public capital (§4º, wording of Law 13.853/2019) (LGPD Art. 4º, §§1º-4º, p.2).

## Definitions in Art. 5 (those that weigh most in engineering)
- `[from source]` Personal data = information related to an identified or identifiable natural person (LGPD Art. 5º, I, p.2). Sensitive = racial/ethnic origin, religious belief, political opinion, membership of a union or religious/philosophical/political organization, health, sex life, genetic or biometric data, when linked to a natural person (LGPD Art. 5º, II, p.2).
- `[from source]` Anonymized = data of a data subject who cannot be identified, using reasonable technical means available at the time (LGPD Art. 5º, III, p.2). Anonymization = use of those means by which the data loses the possibility of direct or indirect association with an individual (LGPD Art. 5º, XI, p.3).
- `[from source]` Controller decides on the processing; processor processes on behalf of the controller; processing agents = both (LGPD Art. 5º, VI, VII and IX, p.2-3). Processing = any operation with personal data: collection, production, reception, classification, use, access, reproduction, transmission, distribution, processing, archiving, storage, deletion, evaluation or control, modification, communication, transfer, dissemination or extraction (LGPD Art. 5º, X, p.3).
- `[from source]` Encarregado = person appointed by the controller and processor as a communication channel between controller, data subjects and the ANPD (LGPD Art. 5º, VIII, p.3; wording given by Law 15.352/2026 according to the compiled text). National authority = public administration body responsible for overseeing, implementing and enforcing the law (LGPD Art. 5º, XIX, p.3; wording given by Law 15.352/2026).
- `[from source]` Consent = free, informed and unambiguous statement for a determined purpose (LGPD Art. 5º, XII, p.3). Blocking = temporary suspension of any operation, with retention of the data; deletion = removal of data or a stored set (LGPD Art. 5º, XIII-XIV, p.3).
- `[from source]` RIPD = controller documentation describing the processes that may generate risks to civil liberties and fundamental rights and the measures, safeguards and mitigation mechanisms (LGPD Art. 5º, XVII, p.3).
- `[from source]` International transfer = to a foreign country or an international body of which the country is a member (LGPD Art. 5º, XV, p.3). Shared use has its own definition (LGPD Art. 5º, XVI, p.3).

## Principles (Art. 6): good faith and ten principles
| Principle | Content in the text | Cite |
|---|---|---|
| Purpose (Finalidade) | legitimate, specific, explicit and informed purposes; no further incompatible processing | (LGPD Art. 6º, I, p.3) |
| Suitability (Adequação) | compatibility with the informed purposes, according to the context | (LGPD Art. 6º, II, p.3) |
| Necessity (Necessidade) | minimum necessary; relevant, proportional, non-excessive data | (LGPD Art. 6º, III, p.3) |
| Free access (Livre acesso) | facilitated and free consultation on form, duration and completeness | (LGPD Art. 6º, IV, p.3) |
| Data quality (Qualidade dos dados) | accuracy, clarity, relevance, updating | (LGPD Art. 6º, V, p.4) |
| Transparency (Transparência) | clear, precise and easily accessible information, with trade and industrial secrets preserved | (LGPD Art. 6º, VI, p.4) |
| Security (Segurança) | technical and administrative measures against unauthorized access and accidental or unlawful destruction, loss, alteration, communication or dissemination | (LGPD Art. 6º, VII, p.4) |
| Prevention (Prevenção) | measures to prevent damage | (LGPD Art. 6º, VIII, p.4) |
| Non-discrimination (Não discriminação) | processing for unlawful or abusive discriminatory purposes is prohibited | (LGPD Art. 6º, IX, p.4) |
| Accountability (Responsabilização e prestação de contas) | demonstrate effective measures and their effectiveness | (LGPD Art. 6º, X, p.4) |

## How to use (engineering) `[inference]`
- Each principle becomes a verifiable requirement: purpose -> purpose field per data item and a check on changes; necessity -> schema and log review; quality -> correction routines; transparency -> tested notices; accountability -> evidence (decision logs, records). Use `scripts/compliance_checklist.py list --area principios`.
- Mapping to NIST objectives (predictability, manageability, disassociability): see `mapeamento-lgpd-nist.md` (each row with a level of support).

## What the text does NOT say
- It does not define "pseudonymized data" in Art. 5 (pseudonymization appears in Art. 13 §4º, p.7), does not mention "privacy by design" by name (the basis is Art. 46 §2º, p.15) and has no list of security techniques. ANPD details and regulations: `extrapolacoes-e-datado.md`.
