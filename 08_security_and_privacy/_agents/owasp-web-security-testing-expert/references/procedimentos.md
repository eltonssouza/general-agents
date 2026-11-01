# Procedures: test plan, scope and authorization, execution and reporting

Pages = PDF (WSTG p.N; printed = N − 2). Labels: [from source] = read on the cited page; [inference] = direct deduction; [extrapolation] = knowledge outside the guide (no page).

## 0. Scope and authorization: what the guide says and does not say
- [from source] The guide **has no chapter on legal authorization**. The points that exist: (a) "rules of engagement" may restrict the scope; without restriction, the ideal is to identify all applications accessible from the target (WSTG p.62); (b) PTES lists "pre-engagement" as the first phase of a pentest methodology (p.43); (c) the report must record the scope and limitations agreed with the organization (p.440); (d) on specific topics the guide asks for caution: account lockout (p.137, 145, 148), log-filling testing in production (p.96), an uploaded web shell must be removed or communicated to the target's team (p.112, 376), decompression bomb only with written approval (p.377), DoS tests not always feasible (p.91), authorization for alternative channels (p.167: "if testing is permitted and authorized").
- [extrapolation] Before any active test, the agent must ask for/remind of: written authorization from whoever has authority over the target, window, list of hosts/applications in and out of scope, test accounts, limits on destructive actions, DoS and social engineering, emergency contact and the rule for handling data found. The guide provides no template; use the client's/legal's. The agent does **not** guide testing against a target without authorization.
- [inference] Content discovered outside the agreed scope (e.g., new applications in INFO-04, p.62) must be confirmed with the client before testing.

## 1. Build the test plan
1. Define objective and approach: the chapter 4 method starts from black box (p.47); gray-box and white-box are cited per test (e.g., p.74, 106, 147, 173) and the guide encourages questioning the assumption that there is no source code (p.22).
2. Gather security requirements: positive (what the control must do) and negative/risk-driven (what must not happen), with use and abuse cases (WSTG p.26-30). [from source]
3. Choose the chapter 4 categories relevant to the application and map functionalities to IDs (script `scripts/test_plan_generator.py`; the functionality→test mapping is [inference]).
4. Reprioritize by business risk: the guide says time is limited and that the guide is not a checklist (p.8). [from source]
5. Plan recording: spreadsheet of entry points and requests (p.72), cookie × function spreadsheet (p.187), channel grid (p.167), process diagram for timing (p.366). [from source]
6. Combine with other techniques (code review, threat modeling); the guide calls isolated pentest "too late" (p.22). [from source]

## 2. Execution flow (ch. 4)
1. **Passive**: explore as a user with an HTTP proxy, map access points (headers, parameters, cookies, APIs) (p.48). Then the information gathering tests (`coleta-de-informacao-info.md`).
2. **Active** in the 12 categories (p.48); order suggested by the guide's index: INFO, CONF, IDNT, ATHN, ATHZ, SESS, INPV, ERRH, CRYP, BUSL, CLNT, APIT (p.3-6). [from source: order of the index; the execution order is the tester's choice]
3. For each test: read Summary, Objectives, How to Test, Remediation (standardized structure, p.10); record evidence with sensitive data masked (p.442).
4. Tests with two accounts (ATHZ-02, ATHZ-04, SESS-03, SESS-09): use test accounts provided (p.175, 183, 197, 215); preferably distinct machines or browsers to reduce false positives (p.198, 216).
5. Eliminate false positives before reporting: an incorrect finding hurts the credibility of the report (p.18). [from source]
6. The misuse test (BUSL-07) is concluded with the observations of all the other tests (p.371). [from source]

## 3. Reporting
- Use the structure of chapter 5 (`relatorio-e-apendices.md`): introduction (version, team, scope, limitations, schedule, disclaimer), executive summary, findings (summary + details), appendices (p.440-442).
- Each finding: ID, title, likelihood/exploitability, impact, risk, description with masked data, remediation, references (p.441-442). Suggested scale: Informational, Low, Medium, High, Critical, with the scale explained in an appendix; CVSS if required (p.441-442). [from source]
- Also recommended by the guide in the metrics part: vulnerability category, threat, root cause, testing technique, remediation and severity (p.35-36). [from source]
- Template and validation: `scripts/finding_template.py`.

## 4. Retest and metrics
- Guide the developer to reproduce and reverify (p.36); in a retest, summarize previous findings and status (p.441). [from source]
- Metrics: compare with a baseline, containment per phase, goals with deadlines (p.34-35). [from source]

## 5. When to forward
- Verification requirements (levels, ASVS) and secure code review: `owasp-asvs-code-review-expert`.
- Threat modeling and security strategy: `infosec-strategy-threat-modeling-expert`.
- Compliance (LGPD etc.): outside WSTG; the guide only cites regulations as examples (p.18, 26).
