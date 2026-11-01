# Sub-setting, data virtualization and data in large tests (TDM p.5; SWE-G p.210-211)

Convention: `(TDM p.N)` and `(SWE-G p.N)` = PDF page. Labels: `[from source]`, `[inference]`, `[extrapolation]`.

## 1. Data sub-setting (TDM p.5)
- `[from source]` Sub-setting means reducing the data footprint by selecting data with a **repeatable** criterion; the text's example uses only customers whose name starts with C (TDM p.5).
- `[from source]` Small footprints make it easier to provision and share data and to use self-service methods such as containers or "sandpits"; benefits: lower storage cost and less batch processing time (TDM p.5).
- `[from source]` Anti-pattern: loose subset design; sub-setting must be **precise**, otherwise needed data goes missing and relationships are lost, which breaks the business logic and the platform stops working (TDM p.5).
- `[inference]` "Preserve referential integrity" (foreign keys) is the direct reading of the anti-pattern above; the source does not describe graph algorithms or sampling percentages.

## 2. Data virtualization (TDM p.5)
- `[from source]` A "modern and somewhat safer" alternative to sub-setting: identify **deltas** ("differencing") between the source of truth and the local copy; the virtual copy is a snapshot of the changes made by the team, and unchanged data stays in the source (TDM p.5).
- `[from source]` Benefits: quickly provision database copies for dev and test, with a small footprint (TDM p.5).
- `[from source]` Anti-patterns: **using non-desensitized data in the source** (the team still has indirect access to the original source; obfuscate the sensitive data in the source first) and **transforming the delta** (if you need to transform, transform the source; transforming the copies can make them "explode" in size) (TDM p.5).
- `[extrapolation]` v1 called this "Copy-on-Write" with a "90% storage reduction" and reset "in seconds"; those terms and numbers are not in the source.

## 3. Views and orchestration applied to test environments
- `[from source]` To avoid contention for data, create "data views" that locate and reserve fit-for-purpose data pools (example: `Data-Pool1` assigned to a team) (TDM p.7).
- `[from source]` Data operations are usually the slowest activities when preparing environments; identify the key operations, standardize them and automate them (TDM p.7). The text cites provision, subset, mask and age as examples of DataOps types (TDM p.8).

## 4. Test data in large tests (SWE-G ch. 14)
- `[from source]` A large test needs two kinds of data: **seeded data** (initial state of the SUT) and **test traffic** (data sent during the test) (SWE-G p.210).
- `[from source]` Seeding the SUT can be orders of magnitude more complex than a unit test's setup (domain data, a realistic baseline, seeding APIs that respect triggers and checks) (SWE-G p.210).
- `[from source]` Sources: hand-crafted data, copied data (typically from production) and **sampled** data; "smart sampling" copies the minimum needed for maximum coverage (SWE-G p.210-211).
- `[from source]` Hand-crafted unit data covers few cases and reflects the author's bias; data copied from production is more faithful, but it is hard to create realistic traffic before launch (SWE-G p.203).
- `[inference]` SWE-G does not address masking, LGPD/GDPR or PII when copying production; combine it with TDM p.6 (masking) and label the bridge as `[inference]`.

## 5. What the sources do not say
Graph-based subsetting algorithms, target sizes, restore time, specific tools (Delphix, Tonic, Docker snapshots), automatic scenario selection by statistics. Treat as `[extrapolation]`.
