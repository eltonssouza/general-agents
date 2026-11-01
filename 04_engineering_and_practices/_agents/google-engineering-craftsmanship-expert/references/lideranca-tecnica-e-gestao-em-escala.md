# Technical Leadership, Leading at Scale and Productivity Metrics (SWE-G Ch. 5, 6 and 7)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`. Ch. 5 "How to Lead a Team" (p.65-82, Brian Fitzpatrick), Ch. 6 "Leading at Scale" (p.83-93, Ben Collins-Sussman), Ch. 7 "Measuring Engineering Productivity" (p.94-104, Ciera Jaspan).

## 1. Ch. 5: manager, tech lead and servant leadership
- [from source] (SWE-G p.65) Google recognizes two roles: the Manager leads people; the Tech Lead leads the technology efforts. In new teams the two can be the same person (Tech Lead Manager, TLM).
- [from source] (SWE-G p.66) The TL is responsible for technical decisions, architecture, priorities, velocity and project management; the book says that, when the TL can choose between doing something quickly alone or delegating, delegating is usually the right decision as the team grows. In larger, established teams it is customary to have a TL + manager pair.
- [from source] (SWE-G p.67-68) "Servant leadership": the most important thing a leader does is serve the team (remove bureaucratic obstacles, help build consensus); the advice "resist the urge to manage" is cited. The leader manages the team's technical and social health.
- [from source] (SWE-G p.69) Summary idea: traditional managers care about how things are done; great managers care about what things are done and trust the team for the how. "It's OK to fail" as long as the same mistake is not repeated; individual failures are criticized in private (p.69).
- [from source] (SWE-G p.70-72) Manager anti-patterns listed in the book: hiring "pushovers"; ignoring low performers; ignoring human issues; being friends with everyone; compromising the hiring bar; treating the team like children (permanent micromanagement indicates a hiring failure, p.72).
- [from source] (SWE-G p.73-78) Positive patterns (section titles): lose the ego (p.73), Zen Master and Catalyst (p.74), remove roadblocks and be a teacher and mentor (p.75), be honest (p.76), track the team's happiness (p.77), delegate without ceasing to get your hands dirty (p.78).
- [from source] (SWE-G p.81) TL;DR: do not "manage" in the traditional sense; focus on leadership, influence and serving the team; delegate; watch focus, direction and velocity.

## 2. Ch. 6: the "three Always"
- [from source] (SWE-G p.83) The chapter organizes leading at scale into Always Be Deciding, Always Be Leaving and Always Be Scaling.
- [from source] (SWE-G p.84-85) Always Be Deciding: identify the "blinders", identify the trade-offs and decide and iterate (avoid "analysis paralysis"). Web Search latency case study with the quality-latency-capacity triangle (p.85-86).
- [from source] (SWE-G p.86-88) Always Be Leaving: the leader must build an organization that solves the problem without them, so as not to be a single point of failure (SPOF); delegating is the main mechanism for forming leaders; a team's identity must lie in the problem it solves and not in a specific solution (p.88-89).
- [from source] (SWE-G p.89-92) Always Be Scaling: success cycle (analysis, struggle, traction, reward), important versus urgent (p.90), learning to "drop balls" deliberately (p.91).
- [from source] (SWE-G p.93) TL;DR of the three "Always": decide trade-offs and iterate; build an organization that solves the class of problem without you; protect your time, attention and energy.
- Fidelity note: the v1 package said "Always Be Leaving" would be the "take a month's vacation" test; the pages read talk about being a SPOF and the organization's self-sufficiency (p.86-88). Only what is on those pages was kept.

## 3. Ch. 7: measuring productivity with GSM and QUANTS
- [from source] (SWE-G p.94) Motivation: as the organization grows linearly, the cost of communication grows quadratically; hence there is a team of engineering productivity specialists. The improvement cannot cost more than it yields.
- [from source] (SWE-G p.95-97) Triage: before measuring, ask what is expected, what action will be taken if the result confirms it and if it is negative, who decides and when. The book says that, if no decision will change, it is not worth measuring; it also advises against measuring when the available metrics are imprecise (for example lines of code, p.97).
- [from source] (SWE-G p.97) GSM: Goal is the desired outcome, with no reference to how to measure; Signal is how we will know it was achieved; Metric is the proxy that can be measured. GSM avoids the "streetlight effect" and the bias of choosing metrics after the fact (p.97-98). Traceability metric -> signal -> goal (p.98).
- [from source] (SWE-G p.98-99) QUANTS: Quality of the code, Attention from engineers, Intellectual complexity, Tempo and velocity, Satisfaction. The book says they are components in trade-off with each other. Readability example (p.99-103). The v1 package cited p.95; the list is on p.98-99.
- [from source] (SWE-G p.100) Quantitative metrics give scale; qualitative ones give context. Example of the median build latency metric adjusted after an experience sampling study.
- [from source] (SWE-G p.103) TL;DR: before measuring, ask whether the result is actionable; use GSM; a good metric is a reasonable proxy of the signal and traceable to the goals.

## 4. What is NOT in these chapters
- "Goodhart's Law" does not appear in the book (full-text search with no results). [extrapolation] It is a well-known principle (a measure that becomes a target stops being a good measure), useful to warn about lines-of-code metrics, but it is not a statement of the book.
- Examples from the v1 package such as "median time to first comment on CLs under 200 lines" are not in the book. [inference] It would be a valid goal/signal/metric example in the GSM style, if labeled as the agent's example.
- "Three golden commandments" and the "decide/get out of the way/scale" rules with a commandment character are formulations of the package; the book uses "the three Always of leadership".
