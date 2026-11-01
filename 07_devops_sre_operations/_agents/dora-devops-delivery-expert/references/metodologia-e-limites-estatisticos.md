# Methodology, sample and statistical limits (DORA24 p.3, 91-116)

Convention: `(DORA24 p.N)`. This file is the basis of the agent's "statistical honesty": use it whenever someone is about to cite a number from the report as law or guarantee.

## 1. Who responded (p.91-98) [from source]
- About 3,000 professionals responded in 2024; the decade adds up to ~39,000 (DORA24 p.91; p.3 says "more than 39,000"). 104 countries (p.97). 
- Demographic questions inspired by the Stack Overflow Developer Survey 2023 (90,000+ respondents), used as a population reference; "no major discrepancies" between the samples, and the authors see reason to consider the sample a reflection of the population (DORA24 p.91). [from source: authors' assessment] Caveat: Stack Overflow itself is a voluntary-participation survey; the report calls it "almost a census". [inference: comparing with another non-probability sample does not eliminate selection bias]
- Industry: technology 35.69%, financial services 15.66%, retail/e-commerce 9.49% (p.92). Size: 10,000+ employees 24.1%; 100-499 18.5% (p.92). Men 83%, women 12% (p.93). Median of 16 years of experience, 5 in the role, 3 on the team (p.94). Roles: devs 29%, managers 23%, senior executives 9% (+33% vs 2023), analytical ~5% (p.95). 90% full-time employees (p.96).
- Implication: the sample is dominated by technology/finance and by men; treat generalization to other contexts as [inference].

## 2. Collection (p.99-102, 109) [from source]
- Questions chosen for: connection with prior work, outcomes desired by the industry, capabilities under consideration, representativeness, blocking of bias paths, feasibility of answering (DORA24 p.100). Usability tests and cognitive interviews (p.100).
- Survey localized in English, Spanish, French, Portuguese, Japanese, Simplified Chinese (DORA24 p.101).
- Recruitment: **organic** channel (blogs, email, social networks, community, snowball sampling) + **panel** to fill in under-represented groups and industries/organization types (DORA24 p.102). In 2024 there were enough organic responses; the panel filled in the rest (p.102). Snowball and organic = no random sampling. [inference]
- Three randomly assigned streams: AI, work environment (Workplace), platform engineering (DORA24 p.102). [inference: each topic was answered by a fraction of the sample]
- Interviews: 11 participants, ~75 minutes planned (57 to 85 min actual, 14h15 in total), remote, automatic transcription and manual coding with the survey topics as a priori codes (DORA24 p.109). Qualitative, to triangulate and contextualize, not to generalize. [inference]
- All delivery metric measures are **self-reported** by people about their main application (DORA24 p.13). [from source] + [inference about self-report and perception bias]

## 3. Measure validation (p.103-104) [from source]
- Internal validity: multiple items per construct; confirmatory factor analysis with the lavaan package (R); if the items do not "stick together", the construct is revised or discarded (DORA24 p.103).
- External validity: the construct should relate as expected to others (e.g., happiness and sadness, negative correlation); too high a correlation between distinct constructs suggests they measure the same thing (DORA24 p.103-104).
- Model evaluation by parsimony (start simple and add complexity until it is no longer justified), with leave-one-out cross-validation (LOOCV) and the Watanabe-Akaike information criterion (DORA24 p.104).

## 4. Causal inference: what is claimed and what is not (p.105-106, 110) [from source]
- The authors want to "think causally" because the reader's question is causal and because the result depends on causal assumptions (DORA24 p.105).
- They use DAGs (directed acyclic graphs) to decide what to adjust for (confounding), trying to mimic an experiment; example of ice cream and shark attacks with temperature as a confounder (DORA24 p.105-106). **The DAGs are theoretical**: they adjust only for confounders that the authors imagined and measured.
- Mill's three conditions: correlation, temporal precedence, controlled bias paths. Correlation: ok. **Temporal precedence: "theoretical, not part of the data"** because the survey is a snapshot. Bias paths: handled by a theoretical exercise (DORA24 p.110).
- Explicit admission: they **did not run longitudinal studies or an experiment proper** (DORA24 p.110). "Correlation does not imply causation, but it does imply how you think about causation" (same page, paraphrase).
- Practical consequence (for the agent): describe results as "associated with"/"estimated" and not as "causes" or "guarantees"; any decision should become a local experiment (DORA24 p.7, p.83). [inference] + [from source]

## 5. From individual to organization: the micro-macro leap (p.111-112) [from source]
- Many effects link capabilities at the individual level (e.g., AI adoption) to team/organization outcomes. The authors admit it is not very intuitive and that it is easier to tell the story of the macro affecting the micro (DORA24 p.111).
- Justification: they assume p(individual does X | organization does X) > p(individual does X | organization does not do X), so that individuals "represent" their organizations; they illustrate with a simulation of heights in two countries (97.2% of 1,000 simulations in the correct direction), admitting that non-random samples, smaller differences and small samples can mislead (DORA24 p.111-112). [from source]
- Caveat from the report itself: the noise is high (DORA24 p.111); the heuristic says the organization influences the individual more than the reverse (DORA24 p.111). [from source]
- Implication: "organization +2.3% with +25% AI" (p.43) is a result under that assumption; the unit of analysis is the person, not the organization. [inference]

## 6. Bayesian statistics and intervals (p.107-108, 112) [from source]
- Bayesian analysis: probability of the hypothesis given the data; priors (weak/skeptical, p.112 note 7), exploration of the posterior distribution for magnitude and uncertainty (DORA24 p.107).
- "Simulation" = draws from the posterior (more than 1,000; in the text, 4,000 "little AIs") to explore plausible values; it is not made-up data (DORA24 p.108).
- Intervals shown: **89%** (explicit choice, no special reason, to avoid the habit of testing hypotheses at 95%) (DORA24 p.108, p.112 note 10); plots with many lines show what is most plausible and the uncertainty (DORA24 p.108). The report's Pearson correlations use a 95% CI (p.43).
- They move away from "significant/not significant" (DORA24 p.107). Therefore, avoid saying "statistically significant" when summarizing: say "the 89% interval excludes/includes zero" (visual reading of the figures) or "uncertain direction". [inference]

## 7. Models (p.113-116) [from source]
- Since 2023: many small models instead of one giant one, because it makes poor fit easier to find, avoids the "gravity" of many variables and avoids conditioning on something that creates spurious relationships (collider) (DORA24 p.113).
- Standard question: "if we do X, what happens to Y?"; they report certainty in direction and magnitude (DORA24 p.114).
- In 2024 the focus was estimating the effect of each capability on each outcome, with a repeated schematic model (the AI one as an example; simplified for reading); effects differ: AI hurts delivery, documentation and user-centricity help (DORA24 p.115).
- 2024 capabilities: AI adoption, platform use and age, transformational leadership, priority stability, user centrality (DORA24 p.114).

## 8. Declared or deducible limits (critical reading checklist)
Declared in the report: no longitudinal/experiment (p.110); micro-macro leap (p.111); "complexity that we are simplifying" (p.109); results "complex and sometimes unclear or contradictory" and an invitation to replicate (p.83); recommends treating findings as hypotheses (p.83, p.7); "expect your results to differ" (p.7); AI-in-CI/CD usage numbers may be underestimated (p.20); figure 12 is an abstraction (p.44).
Deducible [inference]: self-report; convenience sample (organic + panel); no weighting described; subsamples by stream; effects are population averages, not guarantees for a team; effects in "%" are relative to score scales and not physical units; small magnitude (e.g., +2.1% productivity) may be smaller than local measurement noise.

## 9. License
The report indicates a CC BY-NC-SA 4.0 license (DORA24 p.118). Even so, this package paraphrases and quotes the minimum.
