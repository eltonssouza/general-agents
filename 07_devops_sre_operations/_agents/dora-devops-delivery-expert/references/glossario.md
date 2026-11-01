# Glossary (DORA24)

Terms from the report, with our own explanation. `(DORA24 p.N)` = PDF page.

| Term | Meaning (paraphrase) | Where |
|---|---|---|
| Four keys / quatro chaves | The four delivery metrics: change lead time, deployment frequency, change fail(ure) rate, failed deployment recovery time | p.9-10 |
| Change lead time | Time from commit/change to a successful deploy in production | p.10 |
| Deployment frequency | Frequency of deploys to production | p.10 |
| Change fail rate / change failure rate | % of deploys that cause a failure in production (hotfix/rollback); the report uses both spellings | p.10-11 |
| Failed deployment recovery time | Time to recover from a failed deploy (MTTR is not written in the report) | p.10 |
| Rework rate | Fifth metric (2024): unplanned deploys to fix a user-visible bug, question about the last 6 months | p.11 |
| Software delivery throughput | Factor: lead time + frequency + recovery | p.11-12 |
| Software delivery stability | Factor: failure rate + rework | p.11-12 |
| Software delivery performance | Umbrella concept for the five metrics | p.11-12 |
| Performance levels / clusters | Elite, High, Medium, Low; emerge from cluster analysis, they are not preset thresholds | p.13 |
| Cluster analysis | Statistical method that groups responses similar to each other and distinct from the rest | p.13 |
| Elite improvement | Idea that improving matters, not just reaching elite | p.14-15 |
| Value stream mapping | Exercise to find impediments to flow, recommended with the team | p.16 |
| DORA Quick Check | Online tool to drive a conversation and a baseline | p.16, p.79 |
| Reliance (in AI) | Dependence on/centrality of AI in tasks; preferred over frequency of use | p.30 |
| AI adoption (factor) | Factor derived from overall reliance and six tasks | p.30 |
| Toil / toilsome work | Repetitive, manual work with little long-term value | p.31 |
| Valuable work | Time spent on tasks the respondent considers valuable | p.31 |
| Flow | How much focus a person tends to achieve in development tasks | p.4, p.31 |
| Vacuum hypothesis | Hypothesis: AI speeds up valuable work and creates a "vacuum" of extra time | p.33 |
| Burnout | Emotional, physical and mental exhaustion from prolonged stress | p.4 |
| Organizational / team / product performance | Composite factors (definitions on p.4 and p.41) | p.4, p.41 |
| Small batch sizes | DORA principle of small batches; larger changes are slower and less stable | p.40 |
| Internal developer platform (IDP) | Internal platform with APIs, tools and services; broad definition in the survey | p.47, p.50 |
| Golden path | Automated self-service flow over delivery/operations resources | p.48 |
| Shifting down | Moving capability to a shared system (platform) | p.48 |
| Developer independence | A developer's ability to do lifecycle tasks without depending on an enabling team | p.51 |
| Enabling team | Enabling team the developer could depend on | p.51 |
| J-curve | Initial dip followed by gains in transformations (DevOps, SRE, platform) | p.52, p.76 |
| User-centricity | Focus on user needs and feedback in development | p.58-60 |
| Priority stability | Stability of organizational priorities | p.65-66 |
| Transformational leadership | Leadership model with five dimensions | p.70 |
| eNPS | Employee Net Promoter Score (propensity to recommend the company as an employer) | p.71 |
| Flexible infrastructure | The 5 NIST cloud characteristics | p.75 |
| Operational performance | Ability to make and keep promises about the product (studied since 2018) | p.80 |
| SLO / error budget | Service level objective / error budget, cited to calibrate appetite for instability | p.55, p.80 |
| Uncertainty interval (89%) | Interval shown in the figures; deliberate choice of 89% | p.108, p.112 |
| Bayesian statistics / posterior | Statistical approach used; posterior = distribution of plausible values | p.107-108 |
| DAG | Directed acyclic graph to decide what to adjust for in the causal estimate | p.105-106 |
| Confounder / confound | Variable that generates a spurious association (e.g., temperature) | p.105 |
| Micro->macro leap | Inferring team/organization effects from individual data | p.111 |
| LOOCV / WAIC | Leave-one-out cross-validation / Watanabe-Akaike criterion for comparing models | p.104 |
| CFA / lavaan | Confirmatory factor analysis / R package used | p.103 |
| Snowball sampling | Recruitment by chain referral (organic channel) | p.102 |
