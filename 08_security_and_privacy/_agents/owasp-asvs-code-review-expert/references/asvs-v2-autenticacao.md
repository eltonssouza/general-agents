# ASVS V2 — Authentication (ASVS p.22-31)

Source: ASVS 4.0.3. Marks: `L1/L2/L3` = required at that level; `o` = recommended (only V2.8.7 at L2, ASVS p.29). V2.4 and V2.10 have no L1 **because they are not pentestable** (the book says to treat them as L1 in code review, ASVS p.26, 30).

## Chapter premises (ASVS p.22-23)
- [from source] Authentication = establishing that someone/something is authentic, with resistance to impersonation and no recovery/interception of passwords (ASVS p.22).
- [from source] The chapter adopts **NIST 800-63b**: usernames and KBA are public, SMS and e-mail are "restricted" authenticators and passwords are "pre-leaked"; this makes KBA, SMS/e-mail recovery, and password history/complexity/rotation useless (ASVS p.22). The ASVS uses "password" where NIST uses "memorized secret" (ASVS p.22).
- [from source] ASVS L1/L2/L3 map roughly to NIST AAL1/AAL2/AAL3, but the choice of AAL must follow NIST 800-63b §6.2; if the application is L3 or has an AAL3 regulatory requirement, choose L3 in V2 and V3 (ASVS p.22).
- [from source] Legend: empty mark = not required; `o` = recommended; checkmark = required (ASVS p.23).
- [from source] Applications should encourage MFA and allow reuse of tokens the user already has (FIDO/U2F) or integration with credential providers (CSP); trust in social identity depends on risk (government ≠ mobile game) (ASVS p.23).

## V2.1 Password security (ASVS p.23-24) — all L1/L2/L3
| ID | Requirement (paraphrase) | Page |
|---|---|---|
| V2.1.1 | user-set password with **at least 12 characters** (after collapsing multiple spaces) | ASVS p.23 |
| V2.1.2 | allow passwords of at least 64 characters; deny more than 128 | ASVS p.23 |
| V2.1.3 | no password truncation (consecutive spaces may be collapsed) | ASVS p.23 |
| V2.1.4 | accept any printable Unicode character, including spaces and emojis | ASVS p.23 |
| V2.1.5 / V2.1.6 | user can change the password; the change requires the current and the new password | ASVS p.23 |
| V2.1.7 | check passwords (sign-up, login, change) against a set of breached passwords (local or API without sending the password in clear); if breached, require a new one | ASVS p.24 |
| V2.1.8 | password strength meter | ASVS p.24 |
| V2.1.9 | **no composition rules** (no requirement for uppercase/number/special) | ASVS p.24 |
| V2.1.10 | **no periodic rotation or password history** | ASVS p.24 |
| V2.1.11 | allow paste, browser helpers and password managers | ASVS p.24 |
| V2.1.12 | allow temporarily viewing the masked password or the last character | ASVS p.24 |
- [from source] Note: passwords have no maximum lifetime or rotation; they must be checked against breaches, not changed regularly (ASVS p.26).
- **Tension with the OCRG (2017)**: the OCRG recommends complexity by character type and, for internal systems, periodic change with a history of 5 passwords (OCRG p.61) and its checklist asks about complexity/expiration (OCRG p.197-198). ASVS 4.0.3 says the opposite (V2.1.9, V2.1.10). Follow ASVS 4.0.3 and mark the OCRG as [DATED] here.

## V2.2 General authenticator security (ASVS p.25)
- [from source] "Authenticator agility": allow adding authenticators and retiring obsolete ones in order; plan a roadmap that does not depend on e-mail/SMS (ASVS p.25).
- L1/L2/L3: V2.2.1 effective anti-automation controls against credential stuffing, brute force and lockout (breached password lists, soft lockout, rate limit, CAPTCHA, increasing delays, IP/risk restrictions), **at most 100 failed attempts per hour per account**; V2.2.2 weak authenticators (SMS/e-mail) only as secondary verification/transaction approval, offering the strong ones first; V2.2.3 secure notifications after credential changes and logins from risky locations, without sensitive data (ASVS p.25).
- L3 only: V2.2.4 phishing resistance (MFA, cryptographic devices with intent, client certificates); V2.2.5 mutually authenticated TLS between a separate CSP and verifier; V2.2.6 replay resistance (OTP, cryptographic authenticators, lookup codes); V2.2.7 intent to authenticate (OTP or user action, e.g. a button on a FIDO key) (ASVS p.25).

## V2.3 Authenticator lifecycle (ASVS p.26)
- [from source] The authenticator lifecycle (passwords, tokens, biometrics) is critical: self-registration without evidence of identity suits a social network, not a bank (ASVS p.26).
- V2.3.1 (L1/L2/L3) system-generated initial passwords/activation codes: secure random, ≥ 6 characters, expire quickly, never become the long-term password; V2.3.2 (L2/L3) support user-provided authenticators (U2F/FIDO); V2.3.3 (L2/L3) warn in advance about renewing authenticators with an expiry (ASVS p.26).

## V2.4 Credential storage (ASVS p.26-27) — L2/L3 (not pentestable; code/tests only)
- [from source] Only verifiable by code review or tests; when using the ASVS as a review checklist, move these items back to L1 (ASVS p.26). Approved functions: NIST 800-63B §5.1.1.2 and BSI (2018), or more recent regional standards (ASVS p.26).
- V2.4.1 passwords salted and hashed with an approved derivation/hashing function (inputs: password, salt, cost); V2.4.2 salt ≥ 32 bits, unique per credential; V2.4.3 PBKDF2 with iterations as high as the server tolerates, typically ≥ 100,000; V2.4.4 bcrypt with factor ≥ 10; V2.4.5 additional iteration with a **secret salt** (pepper) stored separately (e.g. HSM) (ASVS p.26-27).
- The book **does not mention** scrypt or Argon2 (verified: terms absent from the text); cite as [extrapolation] if necessary.

## V2.5 Credential recovery (ASVS p.27)
- L1/L2/L3: V2.5.1 activation/recovery secret never in clear; V2.5.2 no password hints or KBA; V2.5.3 recovery does not reveal the current password; V2.5.4 no shared/default accounts (root, admin, sa); V2.5.5 notify the user when a factor is changed; V2.5.6 recovery through a secure mechanism (TOTP, push, offline). L2/L3: V2.5.7 loss of OTP/MFA requires proof of identity at the same level as registration (ASVS p.27).

## V2.6 to V2.9 Verifiers (ASVS p.27-29) — mostly L2/L3
- V2.6 (lookup code): used once; ≥ 112 bits of entropy (or with a unique 32-bit salt and hash); resistant to offline attack (ASVS p.27).
- V2.7 (out-of-band): L1: do not offer SMS/PSTN by default, offer push first (V2.7.1); expire codes in **10 minutes** (V2.7.2); single use and only for the original request (V2.7.3); independent secure channel (V2.7.4). L2/L3: only hash of the code (V2.7.5); code generated by a secure RNG with ≥ 20 bits (V2.7.6). E-mail and VOIP are **not** allowed as out-of-band (ASVS p.28).
- V2.8 (OTP): V2.8.1 TOTP with a defined lifetime (L1); L2/L3: protected symmetric keys (HSM/OS), approved algorithms, single use within the period, reuse of a logged-in MFA OTP rejected with notification, revocation of a stolen physical generator effective across sessions; V2.8.7 biometrics only as a secondary factor (L2 recommended `o`, L3 required) (ASVS p.29).
- V2.9 (cryptographic): keys in TPM/HSM/OS service; challenge nonce ≥ 64 bits and unique; approved algorithms (L2/L3) (ASVS p.29).

## V2.10 Service authentication (ASVS p.30) — no L1 (not pentestable)
- [from source] In review, assume a software key store as the L1 minimum; **a clear-text secret is never acceptable** (ASVS p.30).
- Level table with text: L2 = "OS assisted" (OS-assisted storage) and L3 = "HSM" for V2.10.1-V2.10.4 (ASVS p.30). V2.10.1 no immutable intra-service secrets (passwords, API keys, shared privileged accounts); V2.10.2 service account cannot be a default credential; V2.10.3 passwords stored against offline recovery; V2.10.4 secrets/integrations/seeds/API keys managed securely and **outside source code and repositories** (ASVS p.30).
- [from source] Section "Additional US Agency Requirements": the ASVS is a strict subset of NIST 800-63 (especially IAL1/2, AAL1/2) and is not sufficient for IAL3/AAL3; US agencies must implement the full NIST (ASVS p.30).

## Code review — where to look (`[inference]`)
- Login/reset/sign-up: V2.1.x, V2.2.1, V2.5.x. Storage: V2.4.x (by code reading only). Service-to-service integration: V2.10.x. Compare with the OCRG (A2, forgot password, CAPTCHA, OOB): `references/ocrg-a2-autenticacao-e-sessao.md`.
