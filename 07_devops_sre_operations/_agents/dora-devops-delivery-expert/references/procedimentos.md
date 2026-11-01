# Operating procedures (P1-P8)

Each step says where it comes from. [from source] steps have a page; [extrapolation] steps are the agent's good practice, with no page.

## P1. Establish the delivery metrics baseline of an application
1. Choose ONE application/service (not the organization) (DORA24 p.16, p.74). [from source]
2. Bring together the cross-functional team and measure/agree on the metrics (Quick Check, SEI tools, in-house integrations, conversation) (DORA24 p.16, p.79). [from source]
3. Collect the 4 keys + rework (if possible); define what counts as a "deploy" and as a "failure" (a failure only in production, note 1 p.16). Write down the operational definition adopted. [from source p.16] + [extrapolation: record the local definition]
4. Run `scripts/dora_classify.py classify ...` to see the profile against the 2024 clusters (p.13). Report per metric; do not assign an "overall level". [from source] + [inference]
5. State explicitly: levels are neither maturity nor a mandatory goal (p.15, p.74). [from source]

## P2. Improvement cycle (experimental)
1. Identify the area/outcome to improve; measure baseline; formulate hypotheses; agree on a plan; do; measure; repeat (DORA24 p.7). [from source]
2. Discover impediments with value stream mapping (p.16). [from source]
3. Dedicate capacity to improvement work and record lessons (p.16, p.72). [from source]
4. Reassess after enough time for the change to "take"; expect a J-curve (p.16, p.76). [from source]
5. Treat the report's findings as hypotheses to test locally (p.83). [from source]

## P3. Interpret a report "finding" before using it as an argument
1. Locate the page with `dora_lookup.py` and `dora_effects.py`.
2. Classify the source: text, figure (estimate + 89% interval), authors' hypothesis, external citation, abstract illustration (e.g., figure 12, p.44).
3. Check the interval: does it cross zero? If so, speak of "uncertain direction".
4. Remember: observational survey, theoretical DAG, no longitudinal data (p.110), micro-macro leap (p.111).
5. Answer with: effect, unit ("per +25% adoption"), interval, what can NOT be concluded, and how to test locally. [inference about format]

## P4. Evaluate an AI adoption strategy
1. Start from the three axes of p.45-46: mission/policies; learning and experimentation culture with robust tests; known trade-offs. [from source]
2. Measure by downstream impact and not by adoption (p.46). [from source]
3. Watch batch size, delivery stability and throughput: the report associates more AI with a drop in throughput (-1.5%) and stability (-7.2%) per +25% (p.40) and raises the hypothesis of larger batches. [from source: hypothesis]
4. Check code review: speed gains do not mean more rigorous review (p.38). [from source]
5. Concrete suggestions of PR/batch size limits with numbers: [extrapolation]; the report gives no values.

## P5. Decide on/review an internal platform initiative
1. Ask: is there a product mindset, users = developers, self-service, continuous feedback? (p.49, p.51, p.55). [from source]
2. Measure productivity and the delivery metrics before/after; expect a J-curve by age (p.50-52). [from source]
3. Watch throughput (-8% observed), stability (-14% observed) and burnout; decide whether the instability is intentional; use SLOs and error budgets (p.53-55). [from source]
4. Avoid mandatory exclusive use; provide exits from the automations (p.53, p.55). [from source]
5. Dedicated team: helps more at the team level (+6%) than at the individual level (p.52). [from source]
6. Tool/architecture choice: NOT COVERED.

## P6. Answer "are we elite/high/medium/low?"
1. Run `dora_classify.py`; explain that clusters emerge from the 2024 data (p.13).
2. Show that Medium can be more stable than High (p.14).
3. Redirect to: which metric is the bottleneck for THIS service, and what is the user's expectation (p.14, p.16).
4. Warn against comparing teams/individuals and against using it as maturity (p.74).

## P7. Prepare a business case or executive presentation
1. Use the report's numbers with unit and page; separate "reported" from "expected".
2. Financial ROI: the report points to the ROI of DevOps whitepaper (2020), without formulas (p.72, p.78): own calculation = [extrapolation].
3. Always include user feedback and business metrics alongside the 4 keys (p.74).
4. Include limits (p.110-111) in one line.

## P8. Design an internal survey inspired by DORA
1. Use the 2024 questions as inspiration (dora.dev/research/2024/questions, cited p.83-84); adapt to finer-grained questions for your audience (p.83). [from source]
2. Validate measures (multiple items, cohesion) (p.103). [from source]
3. Think about confounders before interpreting (DAG; p.105-106). [from source]
4. Share results and compare with the community (p.83, p.84, p.108). [from source]
5. Minimum sample size, specific techniques: NOT COVERED in the collection.
