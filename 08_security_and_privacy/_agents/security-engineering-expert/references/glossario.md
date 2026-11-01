# Glossary (terms from the book, with page)

Convention: "SE3 p.N" = PDF page (printed = PDF − chapter offset; see `INDEX.md`). Definitions in our own words, faithful to the book's usage `[from source]`; English terms kept as the author uses them. Where the definition goes beyond the page, it is marked `[inference]`.

## A-C
- **Abusability:** thinking about how the system can be abused by those who live with the victim (partner, family member), beyond usability (SE3 p.107).
- **ACL (access control list):** list of rights attached to the object; good when users manage their own security; hard to find "what this user has access to" (SE3 p.258).
- **ALE (annualized loss expectancy):** expected loss × expected number of incidents per year (SE3 p.1000).
- **Assurance:** estimate of how trustworthy a mechanism or the whole is; today it also depends on the vendor's future commitment (SE3 p.52-53, 1047-1048).
- **Attribution:** identifying the author of the attack; the book says that "it is hard" is often false (SE3 p.88).
- **Backup vs fallback:** backup restores the state; fallback is a less capable system used during the failure (SE3 p.300-301).
- **Bell-LaPadula (BLP):** MLS model: no read up (simple security) and no write down (\*-property) (SE3 p.364-365).
- **Biba:** integrity model, the dual of BLP (SE3 p.369-370).
- **Birthday theorem:** with N values, a collision after ~√N samples; 2^(n/2) for n bits (SE3 p.205).
- **Byzantine fault:** a component that gives a wrong answer instead of stopping; solution with n ≥ 3t+1 (SE3 p.297).
- **Capability:** delegable right that the bearer presents; efficient at runtime, hard to revoke and audit (SE3 p.260-261).
- **Chinese Wall:** Brewer-Nash conflict-of-interest policy: separation of duties + stateful MAC (SE3 p.412-415).
- **Clark-Wilson:** integrity model with CDI, UDI, TP, IVP and nine rules (SE3 p.451).
- **Common Criteria (CC):** evaluation regime by EAL, Protection Profile and Security Target (SE3 p.1057-1062).
- **Compliance budget:** limit on the compliance effort the user will accept; design so the data cannot be disclosed (SE3 p.136).
- **Confidentiality vs privacy vs secrecy:** secrecy is the effect of mechanisms; confidentiality is an obligation to protect others' secrets; privacy is the right/ability of the individual (SE3 p.62).
- **Covert channel vs side channel:** deliberate vs accidental leakage (SE3 p.675-676).
- **CPTED:** crime prevention through environmental design (SE3 p.515).
- **Credential stuffing:** reusing credentials leaked from other sites; largest volume of compromise attempts in 2019 `[DATED]` (SE3 p.90-95).

## D-H
- **DAC / MAC:** discretionary vs mandatory access control (SE3 p.261).
- **Dark patterns:** interfaces that induce the user against their own interest (SE3 p.131).
- **Differential privacy (DP):** privacy guarantee bounded by ε, with Laplace noise (SE3 p.434).
- **Dual control:** two people for a sensitive action; differs from functional separation (SE3 p.453-456).
- **EER (equal error rate):** the point at which FAR = FRR (SE3 p.611-612).
- **Environmental creep:** mechanisms designed for a smaller environment fail in the larger one (SE3 p.284-285).
- **FAR / FRR:** false acceptance / false rejection; trade-off described by the ROC (SE3 p.611-612).
- **Fault tree / FMEA:** top-down / bottom-up failure analysis (SE3 p.1003-1005).
- **Forward / backward secrecy:** future/past keys protected against current compromise (SE3 p.232, 705-708).
- **Gundecking:** inspectors who do not actually inspect (SE3 p.600).
- **Hack:** something the rules allow but the designers did not anticipate (SE3 p.63).
- **HMAC:** MAC built on a hash with constants 0x36 and 0x5C (SE3 p.230-231).
- **HSM:** hardware security module with a transaction API; API risks and featuritis (SE3 p.716-717).

## I-M
- **Identity:** correspondence between the names of two principals (SE3 p.61).
- **Inference control:** preventing inference of sensitive data from statistics (SE3 p.419-425).
- **k-anonymity:** operational definition; useless if the k share the sensitive attribute (SE3 p.422-423).
- **Kerckhoffs (modern):** public review is worth more than design secrecy (SE3 p.582-583, 910).
- **Kent's law:** the more items a credential lists, the shorter its lifetime (SE3 p.314).
- **Lemons (market for):** asymmetric information leads bad products to dominate (SE3 p.328-329).
- **Lock-in:** switching cost that traps customers (SE3 p.325-327).
- **Maximum Complacency:** certifiers competing for customers lower the rigor (SE3 p.1063-1065).
- **Middleperson:** intruder who mediates the communication between the parties (SE3 p.176-179).
- **MLS:** multilevel security with labels and upward flow (SE3 p.362-367).

## N-R
- **Nonce:** value used once to guarantee freshness (SE3 p.169).
- **Opsec:** operational security; rules only work with training, explanation and *social embedding* (SE3 p.135-136).
- **Pre-play attack:** attack on EMV that predicts the "unpredictable" number (SE3 p.493-494).
- **Principal:** entity that takes part in the system (person, role, equipment, channel, compound) (SE3 p.61).
- **Protection profile / security target / security policy:** implementation-independent target / detailed specification of the means / succinct statement of the strategy (SE3 p.63).
- **RBAC:** role-based control; lossy compression, but it works (SE3 p.368-369, 399).
- **Reference monitor / TCB:** mediator of all access / set of components whose failure can violate the policy (SE3 p.364).
- **Risk register:** list of risks with severity × probability, mitigation and owner (SE3 p.999).
- **ROC (receiver operating characteristic):** curve of the trade-off between errors (SE3 p.611-612).

## S-Z
- **Safety case:** structured argument that the system is safe (safety) (SE3 p.1002).
- **Security theatre:** visible controls that do not reduce risk (SE3 p.53).
- **Perfect secrecy:** one-time pad; all plaintexts equiprobable (SE3 p.195-196).
- **SIM swap:** fraudulent SIM replacement that breaks SMS 2FA (SE3 p.794-795).
- **Spear phishing:** targeted phishing; main vector against companies (SE3 p.752).
- **Tamper evidence / resistance:** detecting / resisting physical tampering (SE3 p.599, 636-638).
- **TOCTTOU:** time-of-check to time-of-use; race condition (SE3 p.280-281, 290).
- **TOFU:** trust on first use (SE3 p.184).
- **Trusted vs trustworthy:** what can break the policy vs what will not fail (SE3 p.61).
- **Fraud triangle:** motive, opportunity and rationalization (SE3 p.120-123).
- **Trusted path / trusted interface:** trustworthy channel between the user and what signs (SE3 p.154, 667-668).
- **Zooko's triangle:** names cannot be global, decentralized and human-readable at the same time (SE3 p.308).
