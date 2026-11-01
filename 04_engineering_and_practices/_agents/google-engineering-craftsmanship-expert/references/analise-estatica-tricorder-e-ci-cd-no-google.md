# Static Analysis, Tricorder, Continuous Integration and Continuous Delivery (SWE-G Ch. 20, 23 and 24)

> Convention: pages = PDF (see `INDEX.md`). Source: `Software-Engineering-at-Google-completo.pdf`. Ch. 20 "Static Analysis" (PDF p.289-296, Caitlin Sadowski), Ch. 23 "Continuous Integration" (p.330-346, Rachel Tannenbaum), Ch. 24 "Continuous Delivery" (p.347-353, Radha Narayan, Bobbi Jones, Sheri Shipe and David Owens).

## 1. Static analysis (Ch. 20)
- [from source] (SWE-G p.289) Static analysis examines source code without executing it; at Google it serves to find bugs early, codify best practices, keep code up to date and prevent backsliding in migrations (link with deprecation).
- [from source] (SWE-G p.289-290) Scalability and usability: shardable and incremental tools; focus on new warnings (edited lines); "anything that can be fixed automatically should be fixed automatically" (p.290).
- [from source] (SWE-G p.290) Three lessons: focus on developer happiness, analysis is part of the core workflow, and make room for users to contribute (p.291). Only tools with a low false-positive rate are deployed; user trust is essential. "Effective false positive": an issue with no positive action by the developer after seeing it (p.290-291).
- [from source] (SWE-G p.291) Integration with code review is described as the "sweet spot". Tricorder shows warnings in Critique (gray boxes); it analyzes more than 50,000 changes per day.
- [from source] (SWE-G p.291-292) Four criteria for new Tricorder checks: understandable, actionable and easy to fix, with less than 10% effective false positives, and with the potential for a significant impact on code quality. The book says the overall effective false-positive rate is "just below 5%" (p.292) and that there are more than 100 analyzers in more than 30 languages.
- Critical fidelity note: the v1 package said that above 10% false positives "engineers turn the tool off" (p.290) and that a check is only authorized with false positives below 1%. The book does NOT say "1%". The 10% figure is a criterion for new Tricorder checks (p.292), with a real average below 5%. The v1 glossary repeated "below 1%" for Tricorder.
- [from source] (SWE-G p.292-293) Feedback channels ("Not useful", "Please fix"), suggested fixes (authors apply about 3,000 automatic fixes per day and there are about 250 "Not useful" clicks per day, p.293), customization per project and not per user (p.293-294).
- [from source] (SWE-G p.294) Presubmits block the commit (for example, a message with "DO NOT SUBMIT", tests alongside the code, formatting). Compiler integration: Error Prone checks with "ERROR" severity break the build; the policy of not emitting compiler warnings (p.294-295).
- [from source] (SWE-G p.295) It is also worth showing results in the IDE and when browsing code; TL;DR (p.295-296): focus on developer happiness, part of the core workflow, and users contribute.

## 2. Continuous integration (Ch. 23)
- [from source] (SWE-G p.330) Definition: CI is the practice of integrating frequently, with each integration verified by an automated build; the chapter's second definition is "the continuous assembly and testing of our entire complex and rapidly evolving ecosystem". CI guides which tests to run when and how to compose the SUT at each point.
- [from source] (SWE-G p.331) Fast feedback cycles: the cost of a bug grows almost exponentially the later it is found. List of feedback loops, from fastest to slowest. Canary and "version skew" (p.331-332); experiments and feature flags (p.332).
- [from source] (SWE-G p.332) Continuous Build (CB): integrates the head and runs build and tests; "true head" vs "green head".
- [from source] (SWE-G p.333) Release candidate (RC) assembled with code and configuration that passed the CB; configuration must be promoted together, because "a large part of production bugs come from silly configuration problems".
- [from source] (SWE-G p.334) Why presubmit is not enough: cost; "mid-air collision" (rare, but it happens almost every day at Google's scale); rule of thumb: only fast and reliable tests in presubmit; most teams run small tests in presubmit.
- [from source] (SWE-G p.335) RC tests (sanity, auditability, cherry-picks, emergency push) and in production (probers). Section "CI Is Alerting" (p.335-336).
- [from source] (SWE-G p.339) TAP is described as the "Test Automation Platform": the global CB of the entire repository; it handles more than 50,000 unique changes per day and runs more than four billion test cases per day.
- [from source] (SWE-G p.340) Google's strategy: a fast subset of tests runs in presubmit; empirically a change that passes presubmit has a very high probability (95% or more) of passing the rest; affected tests run asynchronously afterwards. Per-team "Build Cop" culture; the average wait time to submit a change is about 11 minutes. When TAP evaluates more than one change per second, it starts grouping changes ("batching") (p.340).
- [from source] (SWE-G p.341) Rollback as the fastest and safest way to fix the build; TAP already rolls back automatically when it has high confidence in the culprit. TAP uses the global dependency graph maintained by Forge and Blaze to decide which tests are affected; changes with fewer tests are executed first (p.341).
- Fidelity note: the v1 package said "hundreds of millions of tests", "running all tests for a 5-line change would be physically infeasible (p.332)" and "the vast majority runs in under 10 to 15 minutes". The book gives the numbers on p.339-341 above; the v1 package's sentence is not in it.

## 3. Continuous delivery (Ch. 24)
- [from source] (SWE-G p.347) The value of code is in the hands of users; Google pursues "launch and iterate".
- [from source] (SWE-G p.347-348) CD idioms at Google: agility (frequent, small releases), automation, isolation, reliability, data-driven decisions (A/B) and phased rollout.
- [from source] (SWE-G p.348) The book avoids claiming that CD is practical for all teams; it describes the culture change as an intermediate step. YouTube example: a manual regression cycle of 50 hours per release.
- [from source] (SWE-G p.349) "Flag guarding" of all changes; the flag can be changed independently of the binary through a dynamic configuration update; turning the flag on for 100% of users at once is not a good idea.
- [from source] (SWE-G p.349-350) Case of the Search binary (release train; from one release per week, rarely met, to one release every two days); "no binary is perfect" and "if you missed the train, it leaves without you".
- [from source] (SWE-G p.351-352) Staged rollouts to growing percentages of the user base; A/B tests of deploys; for apps with a small base, the recommended practice is "change-neutral releases" (all features behind flags).
- [from source] (SWE-G p.353) Conclusion and TL;DR: "faster is safer".
- Fidelity note: the v1 package claimed "1% of servers as canary, comparing 5xx error rate, p99 latency and CPU; automatic rollback in seconds (p.350-351)". Those metrics, the 1% figure and the rollback "in seconds" are NOT on those pages. [extrapolation] A canary with metric comparison against the stable version is common industry practice, but the numbers belong to the agent, not to the book.

## 4. Not audited
- The sections of the Google Takeout case study (p.341-345) and the conclusion of Ch. 23 (p.345-346) were read only in part (p.341-342).
