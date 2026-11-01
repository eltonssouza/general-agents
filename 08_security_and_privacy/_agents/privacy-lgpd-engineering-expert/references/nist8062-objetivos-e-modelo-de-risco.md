# NIST IR 8062: privacy engineering objectives and risk model (chap. 3, chap. 4 and figures)

Pages = PDF (printed = PDF − 8). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. Figures 4, 6, 7, 8 and 9 are images: they were read visually (page rendering), not through text. Support material; not legal advice.

## Components of privacy engineering (Figure 4)
- `[from source]` The PIA is a formal analysis and document on how PII is handled, the risks and how to mitigate them (NIST8062 p.23). Figure 4 (image, NIST8062 p.23) shows: laws, regulations and FIPPs generate privacy requirements; risk models generate risk assessment; privacy and security engineering objectives map system capabilities and provide assurance; the RMF selects controls; the PIA documents identified risks, implemented controls and how the system meets the requirements.

## Privacy engineering objectives
- `[from source]` By analogy with the CIA triad of security, the objectives organize privacy capabilities and controls and reduce the communication gap between legal/policy and engineering (NIST8062 p.24). They are not new policy statements; a system must exhibit each objective to some degree (NIST8062 p.24).
- `[from source]` Figure 6 (image, NIST8062 p.25), definitions:
  - **Predictability**: enabling reliable assumptions by individuals, owners and operators about PII and its processing by the system;
  - **Manageability**: providing the capability for granular administration of PII, including alteration, deletion and selective disclosure;
  - **Disassociability**: enabling the processing of PII or events without association to individuals or devices beyond the operational requirements of the system.
  The same definitions are in the glossary (NIST8062 p.36).
- `[from source]` Figure 7 (image, NIST8062 p.25) gives an example for identity brokers: the predictability capability can serve as evidence that the policy "the broker does not access user attributes" is true (NIST8062 p.25).
- `[from source]` The objectives supplement, not replace, the FIPPs (NIST8062 p.25).

### Figure 8: alignment of FIPPs x objectives (image, NIST8062 p.26)
| FIPP (A-130) | predictability | manageability | disassociability |
|---|---|---|---|
| Access and Amendment | | yes | |
| Accountability | yes | yes | yes |
| Authority | yes | | |
| Minimization | | yes | yes |
| Quality and Integrity | | yes | |
| Individual Participation | | yes | |
| Purpose Specification and Use Limitation | yes | | |
| Transparency | yes | | |
| Security | (aligned with confidentiality, integrity, availability) | | |

### Predictability (NIST8062 p.26-27)
- `[from source]` Supports transparency and accountability; assessing whether users read and understood the notice is worth more than checking that it was given (NIST8062 p.26). It does not require everyone to know the technical details: it means not surprising the parties with the processing of PII (NIST8062 p.26).
- `[from source]` May include technical measures such as de-identification to show that actual disclosures align with individuals' assumptions; supports purpose specification and use limitation without stalling innovation, by encouraging assessment of the impact of changes in processing (NIST8062 p.27).

### Manageability (NIST8062 p.27-28)
- `[from source]` Enables access and amendment, accountability, minimization, quality and integrity and individual participation: without granularity, inaccuracies cannot be identified and corrected, obsolete data discarded, collection limited or preferences implemented (NIST8062 p.27). It is not a policy statement about a right of control by the individual; in systems such as fraud detection or proof of eligibility, the individual may not edit, but a privileged actor administers the changes (NIST8062 p.27). It can support data tagging and attribute transmission standards (NIST8062 p.27-28).

### Disassociability (NIST8062 p.28)
- `[from source]` The system protects ("blinds") the identity or associated activities of the individual; unlike confidentiality, it recognizes exposure risks even within the authorized perimeter and is more closely tied to minimization (NIST8062 p.28). Associating information with individuals should be an operational requirement (e.g., proof of identity, direct health care), not mere difficulty in dissociating; the risk may be consciously accepted (NIST8062 p.28).
- `[from source]` Cryptographic techniques (example in the note: zero-knowledge proof) may map to this objective; a taxonomy of identity classifications is suggested (anonymity, de-identification, unlinkability, unobservability, pseudonymity) (NIST8062 p.28).

## Privacy risk model
- `[from source]` Risk = a measure of the extent to which an entity is threatened by a circumstance or event, typically a function of adverse impact and likelihood; the assessment requires a model that defines factors and relationships (NIST8062 p.29). In security, the factors are threat and vulnerability; these terms do not capture many privacy problems, because the smart meter collects in an authorized way (NIST8062 p.29).
- `[from source]` Proposed factor: **problematic data action** = a data action that causes an adverse effect or problem for individuals (NIST8062 p.29). It plays a functional role analogous to that of the threat in the security model (NIST8062 p.29).
- `[from source]` **Likelihood** = the chance that a data action becomes problematic for a representative individual; perceptions and context are central; demographics, similar scenarios, focus groups and surveys may be used (NIST8062 p.30).
- `[from source]` **Impact** = magnitude of cost or harm; only individuals directly experience the problem, which makes assessment difficult; proxies: costs of compliance, of mission failure (reluctance to use), of reputation and of internal culture; economic, national security and social repercussions may also be considered (NIST8062 p.30).
- `[from source]` Assessing risks prioritizes responses; risk can be managed, not eliminated; the aim is acceptable residual risk, balancing mission benefits, performance, security, reliability and resources (NIST8062 p.30-31).
- `[from source]` Characteristics: **data actions** (collection, retention, logging, analysis, generation, transformation or merging, disclosure, transfer, disposal) as the unit of analysis; **PII** (information that distinguishes or traces identity, alone or combined with other linkable information); **context** (circumstances of the processing): the same email may be harmless in a directory and problematic if linked to a health condition and disclosed outside that context (NIST8062 p.31).
- `[inference]` Minimum procedure derived from the text: (1) delimit the system with an expansive view (NIST8062 p.19); (2) list data actions (NIST8062 p.31); (3) for each, ask whether it can be problematic, in which context and for which problem category (Figure 3, NIST8062 p.18); (4) estimate likelihood and impact (NIST8062 p.30); (5) choose responses and state the accepted residual risk (NIST8062 p.30-31); (6) link the capabilities to the P/M/D objectives as evidence (NIST8062 p.24-28). **NIST IR 8062 does not provide scales, formulas or a matrix**; any scale is `[inference]`/`[extrapolation]`. Roadmap for use in a RIPD: `python -I scripts/ripd_templates.py ripd`.

## Roadmap (chap. 4)
- `[from source]` NIST intends to expand guidance to apply the risk model and the objectives to engineering and risk management practices; existing security guidance serves risks from unauthorized access, less so authorized processing (NIST8062 p.32). Figure 9 (image, NIST8062 p.33) lists security publications (SP 800-18, -30, -37, -39, -53, -53A, -60, -122, -160) with planned complementary guidance; the goal is parity for privacy in enterprise risk management (NIST8062 p.33).
- `[DATED]` The roadmap is from 2017. What came afterwards (for example the NIST Privacy Framework and the PRAM risk assessment; SP 800-53 Rev. 5) is not in the collection: all `[extrapolation]`. See `extrapolacoes-e-datado.md`.

## Link with the LGPD
See `mapeamento-lgpd-nist.md` (each row with level TEXTUAL, INFERENCE or NO_SUPPORT) and `python -I scripts/map_lgpd_nist.py by-objective`.
