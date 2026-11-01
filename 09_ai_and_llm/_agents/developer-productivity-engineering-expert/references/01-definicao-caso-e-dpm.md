# 01. DPE: definition, case, dedicated team and DPE vs DPM (DPE p.8-26)

Pages = PDF (printed = N − 5). Labels: `[from source]`, `[vendor claim]`, `[inference]`.

## 1.1 Scope and audience (p.8-12)
- `[from source]` The book presents itself as a "living document" and the second major update of a 2019 edition (p.8). It is divided into four parts: definitions and drivers; feedback cycles and acceleration; failures and reliability; economics (p.8-9).
- `[from source]` Declared audience: senior developers, build engineers, DPE managers/champions, engineering management, team members who want to build a business case, and CI teams (p.11). The chapters are independent (p.9).
- `[from source]` The author states that the lessons apply to any stack, language or build system (p.11), but chapter 4 admits that the vendor's solutions focus on JVM and Android (p.25). A tension to flag to the user.

## 1.2 Definition (p.14)
- `[from source]` DPE is a software development practice used to maximize developer productivity and happiness; it takes an engineering approach based on automation, actionable data and acceleration technologies, with measurable outcomes such as shorter feedback cycles and lower MTTR for failures (p.14).
- `[from source]` It contrasts with DPM (*Developer Productivity Management*), which sees productivity as a people challenge, addressed with management practices and activity-based metrics (p.14).
- `[from source]` Business goals cited: reduce time to market, increase quality, reduce operating cost, recruit and retain talent (p.14). Analogy with industrial/chemical engineering (p.14).
- `[from source]` DPE is not a new SDLC phase; it supports several phases, with the current focus on Build, Test and CI (Fig. 1, p.18).

## 1.3 The intuitive case (p.15-18)
- `[from source]` Thesis: software productivity depends on the effectiveness of the toolchain, which is defined by its ability to facilitate creative flow, collaboration and team productivity; without DPE, productivity suffers (p.15-16).
- `[from source]` Scientist metaphor: the developer forms hypotheses and dialogues with the compiler and tests; the quality of the flow depends on the timeliness and quality of the response (p.15).
- `[from source]` A TechValidate study is cited: more than 90% of respondents considered the wait time for build and test feedback an important challenge (p.16). `[vendor claim]` the study's source is not detailed in the book.
- `[from source]` Successful projects suffer more: an unmanaged, unaccelerated toolchain collapses as the stack, lines of code, developers, locations, dependencies and repositories grow (p.17).
- `[from source]` CI/CD teams often do not answer for productivity and optimize other metrics (auditability, vulnerability scanning) without considering the effect on developers (p.17). A DPE team's priorities come from fully instrumented toolchain data and require a culture of continuous improvement (p.17).
- `[from source]` The book states that DPE is not about treating developers as factory workers, but as creative craftspeople (p.18).

## 1.4 Forming a DPE team (p.19-20)
- `[from source]` Three reasons to launch now: (1) DPE requires dedicated focus and resources (signals priority, own goals and metrics, autonomy to develop talent), (2) ROI, (3) competitive advantage in recruiting and retention (p.19-20).
- `[from source]` Annual savings formula: engineering cost per minute × average build time reduction (min) × average number of builds per year (p.19). A dedicated team ensures that build, test and restore times do not regress (p.19-20).
- `[from source]` Claims savings "of double-digit engineer-years or millions of dollars" for moderately sized teams (p.20, p.24). `[vendor claim]` no source data.
- `[from source]` Conclusion of chapter 3: systemic gains require organizational focus; DPE should not be an informal, reactive task done in spare time (p.20). `[vendor claim]` expressions such as "business case is a no-brainer" are rhetoric.

## 1.5 DPE vs DPM (p.21-25)
- `[from source]` DPM focuses on people and answers "how to get more out of individuals and teams with the right metrics"; DPE focuses on process and technology and asks how to accelerate feedback and facilitate troubleshooting with analytics (p.21). Analogy: pilots (devs) and cars (toolchain); recommends DPE first (p.21).
- `[from source]` Advantages attributed to DPM: cohort analysis (location, domain, seniority, geography, size), support for building teams and managing time, and for evaluating individual performance and detecting a stuck developer (p.21-22).
- `[from source]` Limitations of DPM: flawed human metrics (citing Gergely Orosz and a 2018 article by the Nortal Cloud Team) because they can be gamed or lack context; many violate "do no harm" (e.g. commits per day); intuition still dominates; developer resistance ("big brother") when metrics become comparative evaluation; collision with existing tools (p.22-23).
- `[from source]` Advantages attributed to DPE: measures outcomes (build/test times, failure rates, build comparison) instead of activity (p.23-24); measurable ROI with a formula (p.24); senior developers are drivers and power users (p.24); more robust success stories (p.24).
- `[vendor claim]` "DPE metrics cannot be gamed nor are they arbitrary" (p.24) is a strong statement with no argument in the book; build time metrics can be distorted (e.g. splitting builds, skipping tests) `[inference]`.
- `[from source]` Limitations of DPE: a new and poorly understood discipline (e.g. confusion between build cache and dependency repository); solutions such as Gradle Enterprise focus on JVM and Android (p.25).
- `[from source]` Comparison table (p.25): DPM measures people and activity, phase "all", "soft" ROI; DPE measures process/technology and outcomes, focus Build+Test+CI, "hard" ROI. Conclusion: complementary, not competing; in a JVM ecosystem, start with DPE (p.25).

## 1.6 Solutions overview (p.26)
- `[from source]` Fig. 2 aligns pains, benefits and technologies; the text refers to Part 2 (p.26). The figure cannot be extracted; the package does not describe its content.

## 1.7 Next steps (p.91)
- `[from source]` Points to a "Learning Center" and to commercial contact with the vendor (p.91). Treat as marketing material.
