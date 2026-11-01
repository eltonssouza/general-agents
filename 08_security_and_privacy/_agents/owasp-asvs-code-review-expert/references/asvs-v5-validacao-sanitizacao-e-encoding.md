# ASVS V5 — Validation, sanitization and encoding (ASVS p.38-41)

Source: ASVS 4.0.3. All V5.1, V5.2, V5.3 and V5.5 requirements are L1/L2/L3; V5.4 (memory) is L2/L3 and only applies to system languages/unmanaged code (ASVS p.40).

## Goal and premises (ASVS p.38)
- [from source] The most common flaw is not validating client/environment input before using it without output encoding; it leads to XSS, SQL injection, injection into interpreters, locale/Unicode attacks, file system attacks and buffer overflow (ASVS p.38).
- [from source] High-level requirements: an agreed validation/encoding pipeline against injection; strongly typed, validated data with range/length (or, at worst, sanitized); output encoded according to context, as close as possible to the interpreter (ASVS p.38).
- [from source] With modern architecture, **output encoding is more important than ever**: where robust validation is hard, use safer APIs (parameterized queries, auto-escaping templates, well-chosen encoding) (ASVS p.38).
- [from source] **Allow list** validation and strong typing can eliminate more than 90% of injection attacks; range/length reduce more. Developers and code reviewers should treat V5.1 as if all items were L1 (ASVS p.38).

## V5.1 Input validation (ASVS p.38)
- V5.1.1 defense against HTTP parameter pollution (if the framework does not distinguish GET/POST/cookie/header/environment); V5.1.2 frameworks protect against **mass parameter assignment** (or mark private fields); V5.1.3 all input (forms, REST, URL, headers, cookies, batch files, RSS...) validated by **allow list**; V5.1.4 strongly typed structured data validated against a schema (characters, length, pattern; consistency between related fields); V5.1.5 redirects/forwards only to allow-listed destinations, or a warning when redirecting to possibly untrusted content (ASVS p.38).

## V5.2 Sanitization and sandboxing (ASVS p.39)
- V5.2.1 untrusted HTML (WYSIWYG editors) sanitized with a sanitization library; V5.2.2 unstructured data sanitized (characters, length); V5.2.3 input sanitized before mail systems (SMTP/IMAP injection); V5.2.4 avoid `eval()` and dynamic code execution (if unavoidable, sanitize or sandbox the input); V5.2.5 template injection (input sanitized/sandboxed); V5.2.6 protection against **SSRF** (validate/sanitize data and metadata; allow list of protocols, domains, paths and ports); V5.2.7 SVG content with script (inline scripts, foreignObject) sanitized/disabled/sandboxed; V5.2.8 user template/expression languages (Markdown, CSS, XSL, BBCode) sanitized/disabled/sandboxed (ASVS p.39).

## V5.3 Output encoding and injection prevention (ASVS p.39-40)
- [from source] Encoding close or adjacent to the interpreter is critical; it is normally not persisted, and serves to make the output safe in the context of immediate use (ASVS p.39).
- V5.3.1 encoder specific to the interpreter/context (HTML, attribute, JavaScript, URL, header, SMTP) — including for names with Unicode/apostrophe; V5.3.2 preserve the user's character set/locale; V5.3.3 contextual escaping, preferably automatic, against reflected, stored and DOM XSS; **V5.3.4 database queries (SQL, HQL, ORM, NoSQL) parameterized, ORMs/entity frameworks or otherwise protected**; V5.3.5 without a parameterized mechanism, use context-specific escaping (e.g. SQL escaping); V5.3.6 JSON injection/eval/JavaScript expressions; V5.3.7 LDAP injection; V5.3.8 OS command injection (parameterized OS queries or contextual command-line encoding); V5.3.9 LFI/RFI; V5.3.10 XPath/XML injection (ASVS p.39-40).
- [from source] Note: parameterizing or escaping SQL is not always enough: **table/column names and ORDER BY cannot be escaped**; including escaped user data in those places breaks the query or allows injection (ASVS p.40).
- [from source] SVG note: the format allows ECMAScript in almost all contexts; if SVG upload is necessary, serve it as `text/plain` or from a domain separate from user content (ASVS p.40).

## V5.4 Memory, strings and unmanaged code (ASVS p.40) — L2/L3
- V5.4.1 safe strings, safe memory copy and pointer arithmetic to avoid stack/buffer/heap overflow; V5.4.2 constant format strings (no hostile input); V5.4.3 sign/range/input validation against integer overflow (ASVS p.40). Only applies to system languages/unmanaged code (ASVS p.40).

## V5.5 Deserialization prevention (ASVS p.41)
- V5.5.1 serialized objects with integrity checks or encrypted; V5.5.2 XML parsers in the most restrictive configuration, without external entity resolution (**XXE**); V5.5.3 avoid deserialization of untrusted data (or protect it) in own code and libraries (JSON, XML, YAML); V5.5.4 in browsers/JS backends, use `JSON.parse`, never `eval()` for JSON (ASVS p.41).
- Chapter references (ASVS p.41): validation, XSS, DOM XSS, mass assignment, XXE and deserialization cheat sheets; DOMPurify; Java Encoder; material on auto-escaping in Angular/React.

## Map to the OCRG (`[inference]`; see also `references/integracao-asvs-ocrg.md`)
| Topic | OCRG (PDF) | ASVS |
|---|---|---|
| SQLi, concatenation, parameterization, ORM | OCRG p.45-53 | V5.3.4, V5.3.5 |
| JSON/eval, XSS, context-based encoding | OCRG p.52, 72-77, 191 | V5.3.3, V5.3.6, V5.5.4, V5.2.4 |
| Validation (exact match, known good, canonicalization) | OCRG p.55-58 | V5.1.3, V5.1.4, V1.5.3 |
| Redirects and forwards | OCRG p.151-153 | V5.1.5 |
| Buffer overrun, format string, integer overflow | OCRG p.184-188 | V5.4.1-V5.4.3 |
| Mass assignment / binding | OCRG p.80-82, 137 | V5.1.2 |
- The OCRG does **not** cover SSRF, deserialization as an attack, XXE (only reference links on OCRG p.51), template injection or HTTP parameter pollution (terms verified absent; see `scripts/gaps.json`).
