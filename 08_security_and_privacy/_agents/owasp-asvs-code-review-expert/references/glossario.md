# Glossary (terms from the sources, explained in our own words)

Sources: **ASVS** = *OWASP Application Security Verification Standard 4.0.3* (footer = PDF); **OCRG** = *OWASP Code Review Guide v2.0* (PDF; printed = N − 1). Terms in the original; explanation in English.

## Standard and levels (ASVS)
- **ASVS requirement / ID** — verifiable item, `<chapter>.<section>.<requirement>` (e.g. 1.11.3); preferred format `v4.0.3-1.11.3` (ASVS p.13; requirement 1.11.3 is on ASVS p.20).
- **L1 / L2 / L3** — verification levels: minimum and pentest-testable (L1); recommended for most (L2); critical/high assurance (L3) (ASVS p.11-12).
- **Marks R / o / empty** — required (checkmark), recommended ("o"), not required (ASVS p.23).
- **Trusted service layer** — any trusted enforcement point (microservice, serverless API, server, API on a client with secure boot, partner APIs) (ASVS p.19). **Untrusted client** — front end that renders the presentation (ASVS p.19).
- **Verifier** — person/team that reviews the application against the ASVS; also the NIST term for whoever verifies possession of authenticators (ASVS p.67, 30).
- **Hybrid review / hybrid pentest** — testing at L2/L3 with access to code, documentation and developers (ASVS p.15).
- **CWE** — community list of software weaknesses; ASVS 4.0 maps requirements to CWEs (ASVS p.9, 65).
- **NIST AAL/IAL** — NIST 800-63 authentication/identity assurance levels; the ASVS maps L1-L3 roughly to AAL1-AAL3 (ASVS p.22).
- **Memorized secret** — NIST term for "password" (ASVS p.22). **CSP** (here: Credential Service Provider, not Content Security Policy) — identity provider; **RP** (Relying Party) — application that trusts another's authentication (ASVS p.30, 66).
- **OOB (out-of-band)** — authenticator over a separate channel; SMS/PSTN are "restricted" and email/VOIP not allowed (ASVS p.28).
- **Half-open attack** — abuse of a session/profile object reused across unauthenticated, semi- and fully authenticated states (ASVS p.35).
- **Allow list** — list of permitted data or operations, used in validation (ASVS p.65).
- **SBOM** — maintained inventory of third-party libraries (V14.2.5, ASVS p.62).
- **SSRF** — attack that abuses server functionality to read/update internal resources through a supplied URL (ASVS p.66).
- **XXE** — XML external entity that accesses local/remote content (ASVS p.67).

## Code review (OCRG)
- **Secure code review** — auditing the code to verify that security and logic controls exist, work and are invoked in the right places (OCRG p.11).
- **S-SDLC** — secure software development lifecycle (OCRG p.7, 21).
- **Source-to-sink** — tracing inputs (sources) to dangerous points (sinks) to find flaws and root cause (OCRG p.18).
- **Sink** — insecure pattern such as dynamic SQL, log writer, response to the client, `innerHTML` (OCRG p.18, 190-191).
- **Code crawling** — sweeping the codebase for APIs/keywords that flag risk areas (OCRG p.43).
- **360 review** — using code review to plan the pentest and the pentest to direct a new review (OCRG p.15).
- **Satellites (BSIMM)** — developers with an interest in security who act as local specialists in the teams (OCRG p.13).
- **Pre-commit / post-commit** — reviewing before or after the code enters the repository (OCRG p.23).
- **Delphi** — risk technique with independent, anonymous consultations (OCRG p.25).
- **Reduce / Accept / Avoid** — responses to the risk found in review; transfer does not apply (OCRG p.26).
- **Risk density** — defects per LOC/function point classified by risk (OCRG p.40). **Defect density** — defects per LOC without weighting severity (OCRG p.40).
- **Cyclomatic complexity (CC)** — number of decisions + 1; ranges 0-10, 11-15, 16-20 (OCRG p.42). **Bad fix probability** — chance that a fix introduces an error, grows with CC (OCRG p.42).
- **Threat model** — set of documents: decomposition, ranked threats, countermeasures (OCRG p.39). **Entry point / asset / trust level / DFD** — input interface, attacker's target, rights granted to external entities, data flow diagram (OCRG p.32-35).
- **STRIDE / ASF / DREAD** — threat categorization from the attacker's view; from the defender's view (controls); ranking by Damage, Reproducibility, Exploitability, Affected users, Discoverability (OCRG p.36-38). **Risk = Probability x Impact** (conceptual) (OCRG p.39).
- **Exact match / known good / known bad / encode bad** — validation hierarchy from strongest to weakest (OCRG p.55).
- **Canonicalization** — reducing equivalent forms of a name to a canonical form before validating (OCRG p.55).
- **Parameterized query / prepared statement** — query whose structure does not depend on the input, with values bound through typed setters (OCRG p.46).
- **Mass assignment / over-posting / data binding** — automatic binding of parameters to object fields, including unexposed ones (OCRG p.80-82).
- **Complete mediation** — checking authorization at every step of a function (OCRG p.138). **Maker/checker** — dual approval for high-risk roles (OCRG p.138).
- **Synchronizer token / double submit cookie** — anti-CSRF defenses by token in the session or a value repeated in cookie and parameter (OCRG p.143-145).
- **Challenge-response** — strong defense against CSRF (CAPTCHA, reauthentication, one-time token) (OCRG p.146).
- **Active defense / AppSensor / CAPEC / honey account** — detection and response inside the application itself; design of detection points; classification of attack patterns; decoy account (OCRG p.178-180).
- **Failing securely** — an error does not leave the application in an insecure state (OCRG p.164).
- **RAII** — resource acquisition is initialization; automatic release at the end of scope (OCRG p.174).
- **FxCop** — .NET binary analyzer with configuration security rules (OCRG p.115-117).
- **Salt** — non-secret value, unique per record, added to the hash to make rainbow tables infeasible (OCRG p.120, 129).
- **FIPS 140-2** — US validation of cryptographic modules cited by the OCRG (OCRG p.121) `[DATED]`.
- **RSQ** — Relative Attack Surface Quotient, a measure of attack surface (OCRG p.132).
