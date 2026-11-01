# 09. Vendor bias, promotional claims and [DATED] items

## 9.1 Nature of the source
`[from source]` The book is published and written by Gradle Inc.: authors include the CEO, the VP of Marketing and product team leads (p.9-10); the "About Gradle" section describes Gradle Enterprise as "the leading enabling technology" of DPE (p.10); there are appeals for a trial and commercial contact (p.90-91). It is neither an independent review nor a peer-reviewed empirical study. `[inference]`

## 9.2 Promotional claims or claims without a verifiable source (flag to the user)
| Claim | Where | Note |
|---|---|---|
| DPE delivers "hard ROI" with little resistance; "business case is a no-brainer" | p.14, p.20 | rhetoric; ROI depends on the user's assumptions |
| DPE is "the most important movement since Agile, lean and DevOps" | p.19 | opinion of the chapter's author |
| DPE metrics "cannot be gamed nor are they arbitrary" | p.24 | too strong; see 01 §1.5 |
| "Proven in over a hundred" brands | p.18 | no list or data |
| Average savings of 90% and minimum of 50% with cache | p.42 | no methodology |
| Test execution = 60-90% of build time | p.43 | customer reports, no sample |
| Cache and distribution raise the MABP "by an order of magnitude" | p.51 | no data |
| Company builds "slow down 15% or more per year" | p.88 | no source |
| Netflix: ~25% of engineering time debugging builds | p.89 | internal study cited without reference |
| IDC: 65% of GDP "digitalized" in 2022 | p.17 | citation of a 2020 report, tangential |
| TechValidate study: over 90% see waiting as a challenge | p.16 | sponsored survey source, not detailed |
| Build Scan "de facto standard" | p.64 | self-description |
| Google 1.5%/16% flaky tests; Facebook "all flaky" | p.73 | cited without reference in the book |
| Calculation of productivity lost because "nobody complains" (30% more code, 10% faster = millions) | p.56 | illustration without derivation |

Mitigating factor `[inference]`: the book acknowledges limits (JVM/Android-only support, p.25; "not fire and forget", p.58; parameters must be the users', p.78-79), and the cost formulas are simple and auditable.

## 9.3 What is a general concept vs what is product
- General `[from source]`: fast feedback, toolchain instrumentation, reproducibility, flaky quarantine, fix-it days, data-driven prioritization, cost = builds × time × cost/minute.
- Vendor-specific `[from source]`: Gradle Enterprise, Build Scan, Test Distribution, Failure Analytics, ROI calculator. Equivalent concepts may exist in other tools, but the book does not describe them `[extrapolation]`.

## 9.4 [DATED] items (book from March 2022)
- `[DATED]` Product name and packaging (the book says "Gradle Enterprise"); check the vendor's current documentation.
- `[DATED]` Ecosystem support (book: JVM and Android, p.25), Maven/Gradle versions, existence of cache in other tools.
- `[DATED]` External reports and numbers (TechValidate, IDC 2020, Google/Facebook, Netflix) and the example's US$ 1/min, US$ 110,400/year.
- `[DATED]` News and practices after 2022 (e.g. DORA/SPACE metrics, internal developer platforms, AI code assistants) do **not** appear in the book: `NOT COVERED`; only `[extrapolation]` if the user asks.

## 9.5 Discrepancies and internal inconsistencies found
1. **File name vs content:** "Data-Platform-Engineering" vs a Developer Productivity Engineering book (INDEX §1).
2. **TCI = 90 vs 120 minutes** in 15.7 (p.82 vs p.83).
3. **180 builds per developer** for Team 2 does not check out (1010 ÷ 6 ≈ 168) (p.28).
4. **"Scales exponentially"** (p.29) with a linear table.
5. **Context-switch formula:** factor `2` on p.30 and "number of switches" on p.67.
6. **Text about the "flaky failure probability"** (p.74): states a product of tests × rate × builds, but the formula given is Π(1−P); they are equivalent only for small rates `[inference]`.
7. **Broken cross-references** in the extracted text ("[sec-fragility]", p.44-45).
