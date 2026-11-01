# 08. Economics: build cost and ROI (ch. 15-16, DPE p.78-90)

All the numbers below are from the book's **example** (a team of 200 engineers) and "reflect what the author typically sees"; the book itself says to use your own data (p.78-79). `[vendor claim]` the assumptions (20% failure, 80% waiting etc.) have no verifiable source.

## 8.1 Example parameters (p.78-79)
- `[from source]` CM = cost per engineering minute (US$ 1); DE = engineer working days per year (230); CE = DE × CM × 8 × 60 = cost per engineer-year (US$ 110,400); BL = 2000 local builds per day; BCI = 2000 CI builds per day; DW = 250 office days; BYL = BL × DW = 500,000; BYCI = BCI × DW = 500,000 (p.78). The book plans to migrate to a metric of builds per lines of code (p.79).
- `[from source]` Unproductive waiting fraction: WL = 80% of the local build; WCI = 20% of the CI build (p.79). The rationale for WL: below 10 minutes there is no significant context switching; it can even exceed 100% (p.79). For CI the book admits it has no good data (p.80).

## 8.2 Waiting (p.79-80)
- `[from source]` Annual cost of waiting per minute of local build: BYL × WL × CM = 500,000 × 0.8 × US$ 1 = US$ 400,000. Each second saved is worth ~US$ 6,667; 17 seconds equal one engineer; 5 minutes saved = US$ 2 million = 18 engineers or 9% of the team (p.79). If the local build grows 1 minute per year, the team would need 4.5 more engineers (p.79). Note: 4.5 only works out by adding the CI minute (US$ 100 thousand) to the local one (400 thousand); 1 local-only minute gives ~3.6 `[inference]`.
- `[from source]` CI: BYCI × WCI × CM = 500,000 × 0.2 × US$ 1 = US$ 100,000 per minute (p.80). Additional costs of slow CI (context switching, conflicts, more changes per build) are not quantified in the book's version (p.80).
- `[from source]` Antivirus anecdote: 1,300,128 local builds per year with 39 s extra each would be the cost of 8 engineer-years (p.80). Checked: 1,300,128 × 39 s ≈ 845 thousand min ≈ US$ 845 thousand ÷ 110,400 ≈ 7.7; the calculation ignores WL (uses the total wait).
- `[from source]` Suggested investments: incremental builds, build cache, metrics collection (p.80).

## 8.3 Debugging code failures (p.81-82)
- `[from source]` Example parameters: FL = 20% of local builds fail; FCI = 10% of CI builds; IL = 5% of failed local builds require investigation; ICI = 20% of CI; TL = 20 min; TCI = 60 min (p.81).
- `[from source]` Local cost: BYL × FL × IL × TL × CM = 500,000 × 0.2 × 0.05 × 20 × 1 = US$ 100,000; CI: 500,000 × 0.1 × 0.2 × 60 × 1 = US$ 600,000; total US$ 700,000 per year (p.81).
- `[from source]` Long builds do not "save": they accumulate changes, raise the failure rate and the investigation time (days in some cases); investigation grows exponentially with the time until the failure appears; without a pre-commit build the rate and time in CI go up; very poor test coverage lowers the rate but pushes problems to manual QA or production (p.82).

## 8.4 Faulty build logic (p.82-83)
- `[from source]` Parameters: FL = 0.2%, FCI = 0.1%, IL = ICI = 100%, TL = 240 min, TCI = 90 min in the table (p.82).
- `[from source]` Costs: local 500,000 × 0.002 × 1 × 240 × 1 = US$ 240,000; CI: the text computes 500,000 × 0.001 × 1 × **120** × 1 = US$ 60,000, and the total is US$ 300,000 (p.83).
- **Inconsistency in the book (checked on the rendered page):** the table on p.82 gives TCI = 90 minutes, but the calculation on p.83 uses 120; with 90 minutes the CI cost would be US$ 45,000 and the total US$ 285,000. `dpe_cost.py example` reproduces the book's calculation by default (120, total of US$ 3.2 million) and warns of the discrepancy; `--faulty-ci-min 90` shows the total with the table's value (US$ 3.185 million).
- `[from source]` Side effect: with faulty builds, developers stop using optimizations such as cache and incremental builds, increasing time (p.83). Investments: metrics, reproducible builds, disposable builds (p.83).

## 8.5 CI infrastructure and total (p.83-84)
- `[from source]` Typical CI hardware in the example: US$ 200 thousand per year; reduce via cache and metrics (p.83). Average times: AL = 3 min, ACI = 8 min (p.83).
- `[from source]` Total of the example (p.84): local waiting US$ 1.2 mi (3 × 400 thousand), CI waiting US$ 0.8 mi (8 × 100 thousand), debugging US$ 0.7 mi, build logic US$ 0.3 mi, CI hardware US$ 0.2 mi: **US$ 3.2 million per year**. Cutting it in half equals ~15 engineers (p.84). Unquantified costs: production failures and manual tests (p.84).
- `[inference]` The model is linear and deterministic, with no uncertainty, no cost of the solution and no correlation between parameters; the book does not compute payback or license cost.

## 8.6 Why opportunities stay hidden (p.84-85)
- `[from source]` (a) immediate needs come first and the absence of complaints becomes "no problem"; anecdotal feedback should not be the only criterion; (b) the benefit is underestimated by incremental steps; a model shows the value and the progress (p.84). Conclusion: the author says he has never seen a company where investing in more efficient builds did not give a significant return (p.84-85). `[vendor claim]`.

## 8.7 ROI calculator (ch. 16, p.86-90)
- `[from source]` Online tool from the vendor (URL in the book) that estimates R&D dollars recovered and hours saved per team and per developer; three blocks: speed up slow builds, avoid regressions over time, debug faster (p.86).
- `[from source]` Steps: (1) size the team and build (number of developers, total annual compensation including overhead, weekly local and CI builds) (p.87); (2) average local build time and the percentage of waiting reduced by the cache; for CI, the percentage of builds with a developer waiting ("typically at least 20%") (p.87-88); (3) maintain speed: "a corporate team can expect builds to be 15% or more slower per year" (p.88) `[vendor claim]`; (4) speed up debugging: states that Netflix internally estimated almost 25% of engineering time spent debugging builds (p.89) `[vendor claim]` no source; failure rate and investigation parameters (p.89).
- `[from source]` Recommends using real data, since most people underestimate the number of builds, and offers a product trial (p.90).
- `[inference]` The book does not provide the online calculator's formulas; `dpe_cost.py` reconstructs the ch. 15 model and labels as `[extrapolation]` any percentage-savings parameter chosen by the user (e.g. % of waiting reduced).

## 8.8 Use by the agent
`python -I scripts/dpe_cost.py example` reproduces the example (US$ 3.2 mi); `dpe_cost.py wait|debug|faulty|savings|total` accept your parameters. Always label: formula `[from source] (DPE p.N)`; user values as user data; reduction percentages as `[extrapolation]`.
