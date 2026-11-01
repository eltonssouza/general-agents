# Operating procedures (how the agent works)

Each step cites the source. Labels: `[from source]` = it is on the cited page; `[inference]` = composition of the steps by the package; `[extrapolation]` = outside the collection. Pages: ASVS = footer = PDF; OCRG = PDF (printed = N − 1). **Safety**: the agent reviews and verifies; it does not provide operational payloads/exploits beyond what the sources document for authorized testing, and it reminds about scope and authorization (ASVS p.14; penetration tests belong to `owasp-web-security-testing-expert`).

## P1 — Plan a risk-based secure code review
1. Classify the module/change by **ease of exposure**, **loss value** and **regulatory controls** (OCRG p.26); use an agreed risk technique (quantitative, qualitative or Delphi; OCRG p.25). [from source]
2. Define intensity: e.g. high-risk module → 3 reviewers including a security architect + extra criteria (test coverage/SAST); low risk → one peer's review (OCRG p.26). [from source]
3. Choose the **moment**: pre-commit, post-commit or audit (OCRG p.23-24) and the format (walkthrough, formal inspection, tool-assisted; OCRG p.21). [from source]
4. Estimate effort with LOC/complexity and inspection rate (e.g. 250 LOC/h as a baseline, for duration only) (OCRG p.40, 42-43). [from source]
5. Record the risk decision: reduce, accept (documenting) or avoid (OCRG p.26). [from source]

## P2 — Prepare the context before looking at the code
1. Collect business rules, sensitive data, roles/rights, app type, language, design (MVC/framework) and company standards (OCRG p.27-28); talk to devs/architect and see the application running (OCRG p.28-29). [from source]
2. For high risk, produce/read the **threat model** (decompose, rank, countermeasures; OCRG p.32-39) and cross entry points x assets x trust levels. [from source]
3. Go through the **design questions** (Table 4, OCRG p.29): existing controls, architecture, configuration/data stores, authentication/access control, data flow. [from source]

## P3 — Choose the ASVS level and generate the checklist
1. Choose the level by risk and data (L1 minimum; L2 most/sensitive data; L3 critical) (ASVS p.11-13); if there is a NIST AAL3 requirement, use L3 in V2/V3 (ASVS p.22). [from source]
2. `python -I scripts/asvs_checklist.py generate --level L2 [--chapters 2,3,4,5] --format md` — the script prints the **count validation**; refuse the checklist if the validation fails. [inference]
3. For code review, treat as L1 the sections the book says to treat that way: V2.4, V2.10 (ASVS p.26, 30), V5.1 (p.38), V6.2/V6.4 (p.42-43), V7.1-V7.3 (p.44-45). [from source]
4. Checklist forks are allowed as long as ID traceability is preserved (ASVS p.15). [from source]

## P4 — Review a feature by source-to-sink
1. List **sources**: browser input, cookies, properties files, external processes, feeds, service responses, flat files, command line, environment variables (OCRG p.33); include headers and hidden fields. [from source]
2. Follow each parameter through the code to the **sinks** (dynamic SQL, log writer, response to the client; OCRG p.18) and check validation/encoding **along the path** (OCRG p.18, 31). [from source]
3. For each flaw found, **enumerate all instances** of the same pattern in the codebase (OCRG p.18) and go back to review areas where the same class may exist (OCRG p.16). [from source]
4. Run the linter for an initial sweep: `python -I scripts/ocrg_lint.py SRC --format md` (and `--include-info` for crawling pointers). Triage each finding manually (OCRG p.11, 31). [inference]

## P5 — Review by vulnerability class (what to open for what)
| Class | Open | Key questions from the book |
|---|---|---|
| Injection/validation | `ocrg-a1-injecao-e-validacao-de-entrada.md`, ASVS V5 | SQL built by concatenation? parameterized/safe ORM? exact match/allow list? server-side validation? |
| Authentication/session | `ocrg-a2-...`, ASVS V2/V3 | TLS on login? do messages leak? lockout? new session ID on login, HttpOnly, timeout, logout, fixation? |
| XSS/DOM | `ocrg-a3-...`, ASVS V5.3 | context-based encoding? textContent? eval/innerHTML/setInterval with a string? |
| IDOR/authorization/CSRF/redirect | `ocrg-a4-a7-a8-a10-...`, ASVS V4 | object owner checked? authorization on every function? anti-CSRF token? redirect destination on an allow list? |
| Config/components | `ocrg-a5-...`, ASVS V14 | descriptors/web.config correct? debug/trace/errors? library allowed and tracked? |
| Crypto/data | `ocrg-a6-...`, ASVS V6/V8/V9 | safe algorithm and mode? key protected? unique salt? MD5/SHA-1? TLS/HSTS? |
| Logs/errors | `ocrg-logging-...`, ASVS V7 | password/session ID in the log? log injection? generic message? specific catch? resources released? |
| Concurrency/memory | `ocrg-concorrencia-e-memoria.md`, ASVS V1.11/V5.4 | shared static state? C functions without bounds? format string? integer overflow? |

## P6 — Triage a linter finding (`ocrg_lint.py`)
1. Read the **class** (`red_flag`, `verify`, `info`) and the **origin** (`[from source]`, `[inference]`, `[extrapolation]`) and the OCRG page (OCRG p.N). [inference]
2. Confirm context: does the value come from user input? is there validation/encoding before? is the constant internal? (the book: tools do not understand context; OCRG p.11). [from source]
3. If confirmed, map to the ASVS requirement (field `asvs_inference`) and record as `fail` in the checklist with the evidence. [inference]
4. If a false positive, record why; **absence of findings does not prove security**. [inference]

## P7 — Threat-guided review (STRIDE/DREAD)
1. Rank threats (prefer qualitative; OCRG p.38-39) and turn each into a review target: spoofing → authentication/session; tampering → validation/CSRF; repudiation → logging; information disclosure → errors/cryptography; DoS → expensive resources, uploads, logs; elevation → authorization (OCRG p.36-37). [from source/mapping inference]
2. For each threat without a countermeasure, open a non-conformity; decide reduce/accept/avoid (OCRG p.26, 39). [from source]

## P8 — Review report (merging the two formats)
- OCRG fields: date, application and modules, devs and reviewer, task/feature, classification and priority of vulnerabilities and actions, links (requirements, design, tests, threat model), checklist used, dev tests, tools used (OCRG p.22-23). [from source]
- ASVS fields: **scope** (including what was left out), summary of findings with **passes and fails** and how to fix, test method, evidence; N/A with justification (ASVS p.14). State that there is no OWASP certification (ASVS p.14). [from source]
- `[inference]` The ASVS does not define severity; prioritize by context risk (OCRG p.25-26) and use the linter's "class" field only as a hint.

## P9 — ASVS in the agile backlog and in procurement
- Backlog: start at L1, verify the application, open **tickets** for missing controls, prioritizing and making security visible as debt (ASVS p.15). [from source]
- Procurement: require "ASVS level X" and that the vendor prove it (with the OWASP Secure Software Contract Annex) (ASVS p.16). [from source]
- Tests: turn testable requirements (including business logic and access control) into unit/integration tests (ASVS p.11, 15). [from source]

## P10 — Evaluate user answers
1. Receive `ANSWERS.json` (ID → pass/fail/na with `reason`/unknown); run `asvs_checklist.py evaluate ... --level L2 --strict`. [inference]
2. Report coverage per chapter, failures with page, pending items and the **conditional verdict** (level achieved only if everything is `pass`/justified `na`). [inference]
