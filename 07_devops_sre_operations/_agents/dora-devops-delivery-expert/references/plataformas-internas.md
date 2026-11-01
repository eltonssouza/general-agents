# Platform engineering and internal developer platforms (DORA24 p.47-56)

Convention: `(DORA24 p.N)`. The platform numbers come from the text (no intervals published in the text); the definition of internal platform was deliberately left broad in the survey (p.50).

## 1. Concept (p.47-48) [from source]
- Platform engineering: a sociotechnical discipline; engineers at the intersection of social interactions between teams and technical aspects of automation, self-service and repeatability (DORA24 p.47).
- DORA research usually focuses on how software is delivered to external users; the output of platform teams is inward-facing: APIs, tools and services supporting the development and operations lifecycle (DORA24 p.47).
- **Golden paths**: highly automated, self-service flows for interacting with the resources needed to deliver and operate applications; they abstract complexity so the dev worries only about the code. Examples: provisioning a new application, database, schema management, test execution, build/deploy infrastructure, DNS (DORA24 p.48).
- "Shifting down" (moving capability to a shared system) may seem the opposite of "you build it, you run it", but the report sees the platform as a way to scale those practices: what goes into the platform teams get "for free" (DORA24 p.48). Example of CI as a platform resource (DORA24 p.48).
- Success factor: a user-centered approach (users = developers), developer independence and a product mindset; without that, the platform gets in the way more than it helps (DORA24 p.49).

## 2. Positive results (p.49-52) [from source]
- 89% of respondents use some internal platform (broad definition; very diverse interaction models) (DORA24 p.50).
- IDP users: individual productivity +8%; team performance +10%; organization delivery and operations performance +6% (DORA24 p.49; p.50 repeats 8%, 10%, 6% for productivity, team and organization). The text does not define the unit of this percentage change beyond "more"/"higher": treat it as a relative difference in the score. [from source] + [inference]
- **Platform age** (figure 14, p.50): organizational performance in the visual reading rises from the "< 1 year" group to "1-2 years", drops at "2-5 years" and recovers at "> 5 years" (J-curve). The text on p.51 describes the pattern as "productivity" (initial gain, drop and recovery) while the figure axis is organizational performance: a small inconsistency in the report. Productivity gains hold in the long term (DORA24 p.50-51). [from source] + [visual inference]
- **Developer independence** (performing application lifecycle tasks without depending on an enabling team): +5% productivity at the individual and team level (DORA24 p.51). Collecting feedback from platform users is important; common methods: informal conversations and issue trackers, then co-development, surveys, telemetry, interviews; **not** collecting feedback has a negative impact; the survey did not indicate which form is most effective (DORA24 p.51). [from source]
- **Dedicated platform team**: negligible impact on individual productivity; +6% at the team level. Hypothesis: teams have more diverse tasks (DORA24 p.52). [from source: hypothesis]
- Key factors (DORA24 p.52): a user-centered approach that enables independence via self-service; and the J-curve also applies to platforms, with gains stabilizing through continuous improvement.

## 3. The unexpected downside (p.53-54) [from source]
- **Throughput**: a drop of ~8% compared with those who do not use a platform. Hypotheses: more "handoffs" between systems/teams (automated testing, security, deploy, monitoring), each adding time, but with a net gain in capacity to do work (DORA24 p.53). For those **required to use** the platform exclusively across the whole lifecycle, -6% throughput (not a definitive connection; it may be the same cause) (DORA24 p.53).
- **Change stability**: a 14% drop, i.e., significantly higher failure rate and rework with a platform (DORA24 p.54).
- **Burnout**: instability combined with a platform is linked to more burnout; "not to say that platforms lead to burnout" (DORA24 p.54).
- Three hypotheses from the authors for instability/burnout (DORA24 p.54): (1) the platform gives confidence to publish because remediation is fast, so instability may be acceptable and even desired (experimentation); (2) the platform does not guarantee the quality of changes, or teams do not improve their tests because they prioritize throughput; (3) reverse causality: teams with instability and burnout create platforms to solve it, i.e., the platform as a symptom. None was tested to distinguish them. [from source: hypotheses]

## 4. Balancing the trade-offs (p.55-56) [from source]
1. Collaboration and feedback improve user orientation: use more than one collection method (DORA24 p.55).
2. Monitor change instability and understand whether it is intentional; use SRE SLOs and error budgets to calibrate risk appetite and the platform's effectiveness in enabling safe experimentation (DORA24 p.55).
3. Prioritize functionality that gives independence and self-service; mind the balance with the requirement of exclusive use; provide ways to opt out of the platform's automations (independence), at the cost of complexity, mitigable with a dedicated team that collaborates and gathers feedback (DORA24 p.55).
4. Platforms emphasize developer experience, but DBAs, security and operations are also needed (DORA24 p.55).
5. A culture of user centrality and continuous improvement aligned with the organization's goals (DORA24 p.56).

## 5. Relevant methodology
Platform was one of the three random tracks of the survey (AI, work environment, platform), so only part of the sample answered this block (DORA24 p.102). [from source] Total sample of ~3,000 (p.91): smaller subsamples = greater uncertainty. [inference]

## 6. Outside the collection
Platform architecture, tools (Backstage etc.), team organization (only reading *Team Topologies* is recommended, p.117), internal platform metrics: NOT COVERED; any advice is [extrapolation].
