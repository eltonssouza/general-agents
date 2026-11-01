# Test Data Management: requirements, synthetic data, masking, encryption and validation (TDM)

**Nature of the source.** TDM is a 9-page **DZone Refcard**, *Test Data Management: Patterns and Anti-Patterns for a Data Factory*, by Niall Crawford (Enov8), 2021 (TDM p.1, p.9). P.2 is a product advertisement (Enov8 DCS). Each method is presented with GOAL, PATTERN and ANTI-PATTERN. Convention: `(TDM p.N)` = PDF page (= printed). Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## 1. The problem and the "data factory"
- `[from source]` TDM is the discipline of building "data-ready" test environments throughout the development lifecycle (TDM p.1).
- `[from source]` The natural complexity of data makes TDM hard: heterogeneous architectures, several database vendors, different platforms (including legacy ones), database designs ranging from a few tables to thousands, and relationships managed outside the database (application or microservices) (TDM p.1).
- `[from source]` There is a wide choice of tools and different priorities between "delivery" (going fast) and "security" (being careful), which leads to "more than one mode of delivery", a "bimodal data" (TDM p.3).
- `[from source]` The **data factory** brings together methods: data requirements, profiling, synthetic data, sub-setting, virtualization, masking (or encryption), validation, orchestration, views and exemptions (TDM p.3); the table of contents also lists reporting (TDM p.1). The author warns that smaller teams may choose which methods to adopt (TDM p.3).

## 2. Data requirements
- `[from source]` Pattern: capture the data needs of each user story as tasks (the text's example: loan data with a female customer and created between 1 Jan 2021 and 31 Jul 2021) (TDM p.3).
- `[from source]` Anti-pattern: capturing requirements late; discovering them after provisioning the environments causes delays and blocks dev, test and QA work; benefits: avoids rework, environments ready on time, testability (TDM p.3-4).

## 3. Automated data profiling
- `[from source]` Pattern: profile automatically to discover schemas, tables, columns, relationships, constraints and PII risks (PII examples: full name, address, email, phone) (TDM p.4).
- `[from source]` Anti-pattern: profiling manually, because sources have thousands of columns and billions of data points and team workshops tend to fail (TDM p.4).

## 4. Synthetic data (fabricated, fake, dummy)
- `[from source]` Pattern: build synthetic test data for dev and test; two reasons: avoid sensitive production data and create data that does not exist yet (e.g. a new product) (TDM p.4).
- `[from source]` Useful in lower environments and early phases (unit and system); benefits: easy to share and reuse, fast provisioning, more security by avoiding production data in the early phases (TDM p.4-5).
- `[from source]` Anti-pattern: using fake data in higher environments (SIT, UAT, performance): complex data with relationships outside the database may not match the business rules; the value decreases as the lifecycle matures (TDM p.5).
- `[inference]` "Zero risk" of privacy violation and "100% risk reduction" (v1) is an exaggeration: the source says synthetic data **avoids** production data in the early phases; poorly generated synthetic data can still reproduce real patterns `[extrapolation]`.

## 5. Data masking
- `[from source]` Goal: obfuscate real sensitive data in a **non-reversible** way; the dataset is copied with PII/sensitive data obfuscated and must still look like production for the test (example: replacing the first name "Simon" with "John") (TDM p.6).
- `[from source]` Benefits: aligns with privacy regulations (the text cites GDPR, HIPAA, spelled "HIPPA", and PCI) and the data behaves like production (TDM p.6). **LGPD does not appear** in the source; treat as `[extrapolation]`.
- `[from source]` Anti-patterns: **over-protecting** (masking too much increases the risk of breakage and loss of integrity; keep the scope "tight", focused on primary PII) and **protecting inconsistently** (if Simon becomes John in one place, it must become John everywhere) (TDM p.6).
- `[from source]` The source has no distinction between static and dynamic masking (SDM/DDM), no preservation of CPF or card checksums, and no "absolute mathematical irreversibility"; those were v1 claims `[extrapolation]`.

## 6. Data encryption
- `[from source]` Unlike masking, encryption is **reversible** with a key; methods cited: DES, AES, RSA, plus weaker ciphers; example with AES128 turning "Smith" into ciphertext (TDM p.6).
- `[from source]` Anti-patterns: encrypting when it makes no sense (the data loses its "production-like" format) and breaking format rules (the application may break because of column constraints) (TDM p.6).

## 7. Data validation
- `[from source]` Pattern: have a screening process that confirms the sensitive data was remediated, because with thousands of columns the risk of forgetting PII is high (TDM p.6). Anti-pattern: manual inspection, unreliable with millions of changes; use automated methods that demonstrate the absence of production patterns (TDM p.7).

## 8. Views, orchestration, exemptions and reporting
- `[from source]` **Data views**: make it easy to find "fit for purpose" data and to **reserve** pools to avoid overwriting by others; anti-pattern: lists (spreadsheets) that age and attract everyone to the same data (TDM p.7).
- `[from source]` **Orchestration**: standardize and automate the key data operations (aligned with DevOps and CI/CD); anti-patterns: "the hero" and selective automation (TDM p.7).
- `[from source]` **Exemptions**: use production data only as a last resort (e.g. a serious incident) through a request process with documented risk, approval and a recorded window; anti-pattern: treating the exception as standard practice; "no one but the customer has the right to use the customer's information" (TDM p.8).
- `[from source]` **Reporting**: DataOps (tickets, lead time, execution time, frequency, success rate by type) and DataSec (coverage of profiled and protected platforms, exemption reports); anti-patterns: not reporting and reporting manually (TDM p.8).
- `[from source]` Conclusion: there is more to TDM than ETL; consider the methods as part of the data factory with DevSecOps practices (TDM p.8).

## 9. Unsupported in v1 (removed or downgraded)
Numbers such as "10 TB", "12 to 24 hours", "2% to 5% of the volume", "90% storage reduction", "million-dollar fines", "Static Masking (SDM)", "Dynamic Data Masking", "valid CPF with check digits" and "failure from collision in shared environments" (partly on p.7, "data views") are not in TDM. Use only as `[extrapolation]` and without a page.
