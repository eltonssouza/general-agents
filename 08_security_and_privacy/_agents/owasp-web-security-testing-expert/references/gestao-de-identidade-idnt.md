# 4.3 Identity management (WSTG-IDNT-01 to IDNT-05)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased. In this category the "how to test" is mostly observational (questions, comparison of responses); avoid mass enumeration without express authorization and watch for account lockout (the guide warns on p.137; see also p.145 on lockout of the administrative account).

## WSTG-IDNT-01 Role definitions (p.128-129)
- **Objectives** [from source]: identify and document the roles; try to switch, change or access another role; review the granularity of the roles and the need for the permissions (p.128).
- Identification by documentation, guidance from developers/administrators, application comments, or "fuzzing" possible roles in a cookie variable, account variable, hidden directories and known users (p.128). The existence of roles is not a vulnerability in itself; roles can be protected by backend signing (p.128).
- Permission review: a support engineer must not perform administrative functions, manage backups or make transactions on behalf of the user; an administrator should not have total powers; sensitive functions can use the **maker-checker** principle or MFA (cites the 2020 Twitter incident) (p.128-129).
- Tools: Autorize extension (Burp) and Access Control Testing add-on (ZAP) (p.129).

## WSTG-IDNT-02 User registration process (p.130-131)
- **Objectives**: verify that the identity requirements of registration are aligned with business and security requirements; validate the registration process (p.130).
- Guiding questions: can anyone register? is there human vetting? can the same person register several times? can one register for different roles? what proof of identity is required? are the identities verified? can the identity information be forged or manipulated in the exchange? (p.130).
- **Remediation**: require identification and verification proportional to the security of the information the credential protects (p.131). Comparison in the guide: registration with e-mail only vs. registration with more data (p.130-131).

## WSTG-IDNT-03 Account provisioning (p.132-133)
- **Objective**: verify which accounts can provision others and of what type (p.132).
- Questions: which roles provision users and what types? is there verification, vetting and authorization of provisioning and **deprovisioning** requests? can an administrator create other administrators? can they create accounts with more privileges than their own? can anyone deprovision themselves? what happens to the files and resources of the removed user (deleted or transferred)? (p.132).
- Mainly a manual method; an HTTP proxy is useful (p.133).

## WSTG-IDNT-04 Account enumeration and guessable user accounts (p.134-137)
- **Objectives**: review the identification processes (registration, login) and enumerate users by analyzing responses (p.134).
- Compare the response to: valid credentials; valid user with wrong password; nonexistent user. The responses must be equal in message **and** in size; if they differ, look for the differentiating factor (p.134-135).
- Other avenues from the guide: login error code, **URLs and redirects** (error parameter), URI probing (403 vs 404 for user directories), page titles, **password recovery** messages, "friendly 404" (200 with an image) and **response time** (e.g., sending a recovery e-mail can add hundreds of milliseconds) (p.135-136).
- Guessing: sequential IDs, realm aliases, first-name and last-name patterns, LDAP or Google information (p.136-137).
- **Risks to the tester**: enumerating can **lock accounts** after attempts and lead to **IP banning** by WAF/IPS (p.137).
- Gray-box: verify that the response is the same for any authentication failure (p.137).
- **Remediation**: generic and consistent error messages; delete default and test accounts before production (p.137). Tools: ZAP, curl, Perl (p.137).

## WSTG-IDNT-05 Weak or unenforced username policy (p.138)
- **Objectives**: determine whether a consistent account-name structure (e.g., initial + surname) makes the application vulnerable to enumeration, and whether the error messages allow enumeration (p.138).
- Method: determine the structure, compare responses to valid and invalid names, enumerate with dictionaries (p.138). **Remediation**: generic and consistent messages (p.138).
