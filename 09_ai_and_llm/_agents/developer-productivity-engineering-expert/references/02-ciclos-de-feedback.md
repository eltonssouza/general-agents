# 02. Feedback cycles (ch. 6, DPE p.28-33)

## 2.1 Central thesis
- `[from source]` Central principle of DPE: minimize feedback cycles throughout the development and delivery cycle; the practice is not "bought" without understanding its role (p.28).

## 2.2 Creative flow and build frequency (p.28-29)
- `[from source]` Comparison of two customer teams: Team 1 with 11 developers, a 4-minute build with tests, 850 local builds (77 per developer); Team 2 with 6 developers, 1 minute, 1010 local builds (180 per developer) (p.28). The book concludes that Team 2 asks for feedback more than twice as often (p.29). The table does not state the period of the 850/1010 builds. **Arithmetic inconsistency in the book:** 1010 ÷ 6 ≈ 168, not 180 (850 ÷ 11 ≈ 77 checks out); the conclusion "more than twice" survives (168/77 ≈ 2.2).
- `[from source]` States that the number of builds is inversely proportional to duration, even when the build is not perceived as slow (p.29). `[vendor claim]` based on internal customer data, with no sample.
- `[inference]` Correlation between team size, duration and frequency is not proof of causation; the book presents the cause as "most likely" (p.29).

## 2.3 Wait time (p.29)
- `[from source]` For builds under ~10 minutes, context switching rarely pays off, so much of the time is pure waiting (p.29).
- `[from source]` Example: Team 2 (6 devs, 1010 builds, 1 min → 36 s with DPE) saves 44 days per year; Team 3 (100 devs, 12,000 builds per week, 9 → 5 min) saves 5200 days, ~25% of engineering time with 220 working days per year (p.29). Checked: 12,000 × 52 × 4 min = 5200 days of 8 h.
- `[from source]` The text says the gain "scales exponentially"; the example's numbers scale linearly with builds and minutes saved `[inference]`; use "proportional".

## 2.4 Context switching and failures (p.29-30)
- `[from source]` When the build fails or is intermediate, the developer pays the context-switch cost twice (going and coming back); typical cost of 10-20 minutes per switch; that is why most people prefer to wait for builds under 10 minutes (p.29-30).
- `[from source]` On average, 20% of build and test runs fail, a number considered healthy (p.30).
- `[from source]` Formulas (p.30, checked on the rendered page): average time of a successful build = average build time + (failure frequency × average build time) + average debugging time; context-switch frequency = failure frequency × number of builds × 2. In ch. 12 the final factor is "number of context switches" instead of 2 (p.67). The book's formula is an approximation: it does not model multiple failures per build `[inference]`.

## 2.5 Larger changesets and debugging (p.30-31)
- `[from source]` Long builds discourage frequent builds, which increases changesets; the build cost is a "fixed tax" per run, but debugging grows non-linearly with the number of changes (p.30). Extreme case cited: repositories that take a day to compile, with hundreds of suspect commits (p.30).
- `[from source]` With build cache and modularization, small changes become faster, encouraging frequent pushes of small changes (p.30).
- `[from source]` Fix time grows exponentially with time to detection (Fig. 4, p.31). In multi-repository setups, the consumer detects the contract break; the more dependencies change, the harder it is to identify responsibility (p.31). `[vendor claim]` "exponential" is a qualitative statement; the book provides no measurement.

## 2.6 Merge conflicts, project size and "shift right" (p.31-33)
- `[from source]` Larger changesets and more PRs per integration build raise the chance of conflict, in a vicious circle (p.31).
- `[from source]` Small projects also benefit (less waiting, better flow); large teams split the code into many repositories, which creates the producer-consumer problem (p.32).
- `[from source]` Many companies "shift feedback to the right": fewer local tests, and the PR build becomes the first to run unit tests; the book considers this the opposite of a healthy pipeline and states that the only solution is to accelerate the build (p.32-33).
- `[from source]` The problem grows with success: more teams, code and repositories; good developers look for other opportunities if nothing improves (p.33). The "dog eat dog" anecdote about a bank and a software company (p.33) is a field story without data.
- `[from source]` Conclusion: fast feedback reinforces good habits; the "soft" benefit that is perhaps the most important is developer happiness (p.33).

## 2.6 Use by the agent
To quantify: `python -I scripts/dpe_cost.py feedback --build-min 4 --fail-rate 0.2 --debug-min 20` (formulas p.30). Label the result `[from source]` only for the formula; the parameters are the user's.
