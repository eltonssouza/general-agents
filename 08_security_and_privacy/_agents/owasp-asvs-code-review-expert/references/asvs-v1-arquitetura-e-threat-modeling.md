# ASVS V1 — Architecture, design and threat modeling (ASVS p.17-21)

Source: ASVS 4.0.3. **No** V1 requirement is L1: all are L2/L3, except V1.11.3 which is L3 only (verified in the data; ASVS p.17-21). Marks below: `L2/L3` = required in L2 and L3.

## Chapter goal (ASVS p.17)
- [from source] Security architecture became a "lost art"; it is a way of thinking about a problem with several possible answers, not a single implementation (ASVS p.17).
- [from source] Implementation always changes while architecture evolves slowly; sound decisions today allow reuse of "architecturally compatible" solutions. Book example: a single federated identity provider (SAML) can be upgraded to new requirements (NIST 800-63) without changing the applications' interfaces (ASVS p.17).
- [from source] It covers availability, confidentiality, processing integrity, non-repudiation and privacy; "shift left" (from developer enablement to final independent testing) is critical because developers ship code tens/hundreds of times a day (ASVS p.17).

## V1.1 Secure software development lifecycle (ASVS p.17-18) — all L2/L3
| ID | Idea (paraphrase) | Page |
|---|---|---|
| V1.1.1 | use a secure SDLC that addresses security in all phases (C1) | ASVS p.17 |
| V1.1.2 | threat modeling for every design change or sprint planning (identify threats, countermeasures, risk responses, guide tests) | ASVS p.17 |
| V1.1.3 | every user story/feature has functional security constraints (e.g. "I must not see/edit another user's profile") | ASVS p.17 |
| V1.1.4 | document and justify trust boundaries, components and relevant data flows | ASVS p.17 |
| V1.1.5 | define and analyze the high-level architecture and all connected remote services | ASVS p.17 |
| V1.1.6 | centralized, simple ("economy of design"), vetted and reusable security controls to avoid duplicated/missing/ineffective ones (C10) | ASVS p.18 |
| V1.1.7 | secure coding checklist/policy/guide available to developers and testers | ASVS p.18 |

## V1.2 Authentication architecture (ASVS p.18) — L2/L3
- [from source] Strong hardware MFA is useless if an attacker resets the account by calling a call center and answering well-known questions: **all authentication paths must have the same strength** (ASVS p.18).
- V1.2.1 unique or special low-privilege OS accounts for every component/service/server; V1.2.2 communication between components (APIs, middleware, data layer) authenticated, with least privilege; V1.2.3 **a single** vetted authentication mechanism, extensible to strong authentication and with logging/monitoring; V1.2.4 consistent strength across all identity management paths and APIs, with no weaker alternatives (ASVS p.18).
- V1.3 (session) is only a placeholder for future requirements (ASVS p.18).

## V1.4 Access control (ASVS p.18) — L2/L3
- V1.4.1 enforce access control at **trusted enforcement points** (gateways, servers, serverless functions); never on the client; V1.4.4 a single vetted mechanism for all access to protected data (no copy-and-paste paths); V1.4.5 **attribute/feature**-based control (checks authorization for the function/data, not just the role; permissions still assigned through roles) (ASVS p.18). V1.4.2 and V1.4.3 were removed (ASVS p.18).

## V1.5 Input and output (ASVS p.19) — L2/L3
- [from source] The book replaces "server-side" with **"trusted service layer"**: any trusted enforcement point (microservice, serverless API, server, trusted API on a client with secure boot, partner APIs). "Untrusted client" = technologies that render the presentation (front end). "Serialization" includes complex objects with logic (ASVS p.19).
- V1.5.1 input/output requirements define handling by type, content and laws/policies; V1.5.2 **do not use serialization** with untrusted clients (or enforce integrity and, if sensitive, encryption, against object injection); V1.5.3 input validation in a trusted service layer; V1.5.4 **output encoding close to the target interpreter** (ASVS p.19).

## V1.6 Cryptographic architecture (ASVS p.19) — L2/L3
- [from source] "Encrypting everything is wasteful; encrypting nothing is legal negligence": balance this in the design; retrofitting costs more; architectural requirements are hard to test by unit/integration and must be reviewed in architecture, code review or retrospectives (ASVS p.19).
- V1.6.1 explicit key policy and lifecycle according to a standard (e.g. NIST SP 800-57); V1.6.2 consumers protect keys and secrets with vaults or API-based alternatives; V1.6.3 all keys/passwords replaceable, with a defined re-encryption process; V1.6.4 client-side secrets (symmetric keys, passwords, API tokens) treated as insecure, never used to protect/access sensitive data (ASVS p.19).

## V1.7 to V1.10 (ASVS p.20) — L2/L3
- V1.7.1 common log format and approach across the system; V1.7.2 logs securely transmitted to a preferably remote system (analysis, alerting, escalation).
- V1.8.1 all sensitive data identified and classified into protection levels; V1.8.2 each level with requirements (encryption, integrity, retention, privacy) enforced in the architecture.
- V1.9.1 communication between components encrypted, especially between containers/systems/sites/clouds; V1.9.2 each side verifies the other's authenticity (e.g. validate TLS certificates and chains).
- V1.10.1 version control with tickets/change and controlled access with identifiable users (traceability) — the section is named "Malicious Software Architecture".

## V1.11 Business logic (ASVS p.20)
- V1.11.1 components defined/documented by business or security function (L2/L3); V1.11.2 high-value flows (authentication, session, access control) **without unsynchronized shared state** (L2/L3); V1.11.3 these flows **thread-safe and resistant to TOCTOU** (L3 only).

## V1.12 to V1.14 (ASVS p.21) — L2/L3
- V1.12.2 user-uploaded files, if displayed/downloaded, must be served as octet-stream or from an unrelated domain (e.g. a bucket), with an appropriate CSP (V1.12.1 removed).
- V1.14.1 segregate components of different trust (firewalls, API gateways, reverse proxies, security groups); V1.14.2 binary signatures, trusted connections and verified endpoints when deploying binaries to remote devices; V1.14.3 build pipeline warns about and acts on outdated/insecure components; V1.14.4 build step that builds and verifies the secure deployment (infrastructure defined as software); V1.14.5 deployments with sandbox/container/network isolation (especially for dangerous actions such as deserialization); V1.14.6 no obsolete client technologies (NSAPI, Flash, Shockwave, ActiveX, Silverlight, NACL, Java applets).

## How to use it in code review (summary)
- `[inference]` V1 is not "testable" by pentest; in review it becomes design questions: where is the trust boundary, who enforces authorization, is there a single mechanism, where are the keys, how is data classified. The OCRG has the operational version: design questions (Table 4, OCRG p.29-30) and threat modeling (OCRG p.32-39). See `references/ocrg-threat-modeling-aplicado.md` and `references/integracao-asvs-ocrg.md`.
- Chapter references (ASVS p.21): Threat Modeling Cheat Sheet, Attack Surface Analysis Cheat Sheet, SAMM, Microsoft SDL, NIST SP 800-57.
