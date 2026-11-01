# Cases and anti-patterns of interpretation and application (DORA24)

The report has no named company cases with data; it has aggregated findings and quotes from anonymous interviewees (P1..P11). The "cases" below are usage scenarios for the findings, with the source of each claim; the scenario itself is [extrapolation] by the agent.

## Anti-patterns in using the metrics
| # | Anti-pattern | Why it is a problem | Source |
|---|---|---|---|
| A1 | Ranking teams or people by the four keys | The report asks to use them to visualize improvement, not to compare teams and certainly not individuals | DORA24 p.74 |
| A2 | Measuring at the organization/business-line level | The four keys should be applied per application/service | DORA24 p.74 |
| A3 | Treating Elite/High/Medium/Low as a maturity model or a goal | Labels have little value in the journey; improving matters more | DORA24 p.14-15, p.74 |
| A4 | Treating the 2024 cutoffs as official fixed thresholds | Clusters emerge from each year's data | DORA24 p.13 |
| A5 | Optimizing only speed or only stability | They tend to move together; but medium is more stable and slower than high; depends on users and goals | DORA24 p.10, p.14 |
| A6 | Counting as failures changes blocked before production | Note 1: a failure only counts if it affects production; blocking is a success of the process | DORA24 p.16 |
| A7 | Ignoring user feedback metrics | They are as important as the four keys | DORA24 p.74 |
| A8 | Expecting immediate results and quitting at the initial dip | J-curve; change does not happen overnight | DORA24 p.16, p.52, p.76 |

## Anti-patterns in statistical interpretation
| # | Anti-pattern | Correction | Source |
|---|---|---|---|
| S1 | "The report proves that X causes Y" | No longitudinal data or experiment; theoretical temporal precedence; theoretical DAG | DORA24 p.110 |
| S2 | "AI increases productivity by 2.1%" as a fixed number | It is per +25% adoption, an association estimate with an 89% interval | DORA24 p.32, p.108 |
| S3 | Extrapolating linearly (50% AI = -14.4% stability) | The report does not publish that curve; the extrapolation is the reader's | DORA24 p.40 (+25% only) |
| S4 | Treating the authors' hypothesis as a finding (e.g., larger batches explain the delivery drop with AI) | They are hypotheses, not measurements | DORA24 p.40 |
| S5 | Using figure 12 (learning curves) as data | It is an abstraction, not derived from real data | DORA24 p.44 |
| S6 | Generalizing a survey average to the specific team | Effects are averages; the report says to expect different results and to replicate | DORA24 p.7, p.83 |
| S7 | Reading product +0.2% with AI as a benefit | Interval crosses zero; text says no obvious association | DORA24 p.42-43 |
| S8 | Calling something "significant" without looking at the interval | Authors avoid significance; speak of direction and plausible magnitude | DORA24 p.107, p.114 |
| S9 | Forgetting the micro-macro leap | Effects at the organization level come from individual data under an assumption | DORA24 p.111 |
| S10 | Confusing product-team correlation (r=0.56) with an AI effect | It is a correlation between outcomes, reciprocal | DORA24 p.43 |

## Anti-patterns in AI adoption
| # | Anti-pattern | Evidence |
|---|---|---|
| I1 | Declaring success because adoption increased | The report recommends measuring downstream impacts, not only adoption (p.46) |
| I2 | Letting change size grow with code generation | Hypothesis of larger batches as the explanation for the delivery drop (p.40) |
| I3 | Trusting faster review as a sign of quality | Review speed is not rigor; risk of overconfidence (p.38) |
| I4 | Expecting AI to reduce toil/burnout | Toil and burnout remained practically unchanged (p.35) |
| I5 | Ignoring clear policies | Recommends a mission and policies (where to put code, tools) (p.45) |

## Platform anti-patterns
| # | Anti-pattern | Evidence |
|---|---|---|
| P1 | Platform without a product mindset/feedback | Without a user-centered approach, the platform gets in the way (p.49); not collecting feedback has a negative impact (p.51) |
| P2 | Requiring exclusive use of the platform across the whole lifecycle | Associated with -6% throughput (p.53) |
| P3 | Ignoring stability after introducing a platform | -14% stability and a link with burnout (p.54) |
| P4 | Platform only for developer experience | DBAs, security and operations are also part of delivery (p.55) |
| P5 | Measuring success only at the start | J-curve by age (p.50-52) |

## Culture/organization anti-patterns
| # | Anti-pattern | Evidence |
|---|---|---|
| C1 | Changing priorities frequently and expecting good leaders/docs to compensate | They do not offset burnout (p.65) |
| C2 | Documenting only out of bureaucracy or without maintaining | Low quality, wrong audience; excess is also bad (p.64) |
| C3 | Building features on assumptions about the user | Likelihood of "brilliant but little-used" features (p.60) |
| C4 | Moving to the cloud without using the cloud's flexibility | May predict a drop in organizational performance (p.75) |
| C5 | Expecting engineers to learn and automate in their spare time | It must be on the agenda; leaders must allocate time and budget (p.71) |
| C6 | Treating leadership as sufficient | It is enabling, not sufficient (p.71) |

## Application scenarios [extrapolation by the agent on report findings]
1. **Team with a 2-week lead time, weekly deploys, 10% failure rate**: profile close to Medium (p.13); instead of "moving up a level", agree with the team on which impediment (VSM, p.16) and what the user expects (p.14).
2. **Team that adopted a code assistant and saw failures increase**: consistent with the stability drop associated with AI (p.40); check batch size (hypothesis, p.40), tests (p.40, p.46) and review (p.38). Do not conclude a cause without a local experiment (p.83).
3. **New internal platform with a throughput drop**: expected as a possibility (p.53) and the J-curve (p.51-52); check handoffs, exclusive use, feedback (p.53, p.55).
4. **Executive asks for a "squad ranking"**: decline based on p.74; propose a per-service dashboard with technical and business metrics.
