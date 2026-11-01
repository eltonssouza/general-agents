# Access control and identity (DZ Ch.5, PDF p.144-166; printed p.127-149)

DZ citations = PDF page (printed = PDF − 17). Paraphrase is mine.

## Problem (DZ p.144-145)
IAM deals with people and automated services that do CRUD in the environment; it balances too much access (breach) against too little (unproductivity). Topics: models, authentication and authorization for people, devices and services, IAM, and physical access.

## Models and concepts (DZ p.145-152)
- **[from source] (DZ p.145)** Definitions: *subject* (acts), *object* (passive), *clearance* (subject's level), *classification* (object's level).
- **[from source] (DZ p.146-147)** State machine model (regulated states and transitions) and information flow model (basis of Biba and Bell-LaPadula).
- **[from source] (DZ p.147)** **Bell-LaPadula** (confidentiality, MAC): *no read up* (simple property), *no write down* (star property) and the strong version (*strong star*: read/write only at the same level).
- **[from source] (DZ p.148)** **Take-Grant** (directed graph; take, grant, create, remove/revoke rights) to analyze the security of complex systems.
- **[from source] (DZ p.149)** **Brewer-Nash** (Chinese wall): avoids conflict of interest by segmenting access (e.g. a consultancy with several clients).
- **[from source] (DZ p.149)** **Biba** (integrity): *no read down*, *no write up*, invocation property. **[from source] (DZ p.150)** **Clark-Wilson** (integrity): separation of duties; constrained data only changes via an application with logging and auditing.
- **[from source] (DZ p.150)** Real-world models: **capability-based** vs **ACL-based**.
- **[from source] (DZ p.151-152)** Families: IBAC, LBAC (lattice; Bell-LaPadula in practice), **RBAC** (roles), RAC (rules, e.g. time of day), **MAC**, **DAC**, **ABAC** (policies over attributes), GBAC, HBAC and HPBAC.

## Authentication and authorization (DZ p.153-161)
- **[from source] (DZ p.153)** Authentication = confirming identity; authorization = what can be done afterwards. Authorization can be tied to classification labels.
- **[from source] (DZ p.154)** Factors: something you know, have, are; **MFA** combines distinct factors (password + "first dog's name" are two things you know, **not** MFA). Passwords: store as a salted hash; limit attempts (dictionary/brute force).
- **[from source] (DZ p.155)** Password complexity, password managers; **smart card** + PIN (weak PIN but with limited attempts); **biometrics** (no password to remember, but false positives/negatives, cannot be changed, cost).
- **[from source] (DZ p.156)** **SSO**: proves identity once; reduces password reuse and makes revocation easier.
- **[from source] (DZ p.156-158)** **NTLM**: obsolete but widespread protocol; flaws (relay, dictionary/GPU cracking, *pass-the-hash*, RCE in some scenarios); mitigations if it must be kept: SMB signing, block NTLMv1, LDAP/S signing and channel binding, EPA. **[DATED]** cracking speeds cited (GTX 1060).
- **[from source] (DZ p.158-160)** **Kerberos**: separate client, server and KDC; TGT, service tickets, SPN and *authenticator* with timestamp against replay.
- **[from source] (DZ p.160-161)** **PKI and X.509 certificates**: eliminates username/password, ideally with a second factor; an organizational CA distributes and revokes certificates at scale.
- **[from source] (DZ p.161-162)** Authorization: not every resource requires authentication; **least privilege** "is worth the work"; MAC, DAC, RBAC or ABAC (or combinations), e.g. ACL + RBAC.

## IAM (DZ p.162-164)
- **[from source] (DZ p.162)** IAM tools give a single identity across the user's lifetime (employees, customers, third parties), reflect role change and departure; they require a technical team and auditing; they help with HIPAA, SOX, GDPR. Directories (Active Directory) are different from IAM, but essential to it.
- **[from source] (DZ p.163)** Automation (HR creates the user in the directory and triggers actions), IDaaS. Policy questions: access model (RBAC? MAC?), provisioning of new users, who has which authorization, offboarding, **exceptions** (escalation, approval), **access review** (avoid accumulation at every role change), scope of automation (password reset, revocation on an HR signal), temporary third parties (federated identity?), SSO coverage (p.163-164), user onboarding (test the new hire's path).

## Physical access (DZ p.164-166)
- **[from source] (DZ p.164)** Human, mechanical, technological control (mantraps, turnstiles, biometrics, fobs, exit barriers) and perimeters; keys do not record entry, do not restrict hours nor prove identity, and are hard to revoke.
- **[from source] (DZ p.165)** **EAC**: time-of-day restriction, attempt logging, granular revocation, MFA (know/have/are; "where you are" only for digital access).
- **[from source] (DZ p.165-166)** Risks: tailgating (mantraps/turnstiles), destruction (bollards, detection), technological attacks (cloning cards, forcing PINs: MFA and rate limiting); add the physical access risks to the risk register.
