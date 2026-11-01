# Software Engineering Over Time (SWE-G Ch. 1)

> Convention: pages = PDF page (see `INDEX.md`). Labels: [from source], [inference], [extrapolation], [DATED]. Source: `Software-Engineering-at-Google-completo.pdf`, Ch. 1 "What Is Software Engineering?" (PDF p.13-27, author Titus Winters).

## 1. Programming vs engineering: time, scale and trade-offs
- [from source] (SWE-G p.13) The chapter points to three differences between programming and doing software engineering: time, scale and the trade-offs involved. The phrase "software engineering is programming integrated over time" is presented as an internal Google saying ("within Google, we sometimes say").
- [from source] (SWE-G p.13) The expected lifespan of code varies by a factor of about 100,000 (from minutes to decades); short-lived code is "just" a programming problem.
- [from source] (SWE-G p.13) Sustainability: the project is sustainable if, over its expected lifespan, the team is capable of reacting to any valuable change (technical or business). The book emphasizes capability: one may choose not to do an upgrade.
- [from source] (SWE-G p.13) Scale: engineering is a team effort; the definition "multiperson development of multiversion programs" is cited.
- [from source] (SWE-G p.14) The work of those doing engineering is to pursue sustainability and control the costs of scale, weighing trade-offs; sometimes maintenance is deferred, but the choice must be explicit about the deferred costs.
- [from source] (SWE-G p.25) Programming and software engineering are different domains, with no value judgment that one is superior; certain tools (integration tests, CD, SemVer) may not be worth it in projects of a few days.
- [from source] (SWE-G p.25) Closing of the chapter: programming is the immediate act of producing code; software engineering is the set of policies, practices and tools needed to make the code useful for as long as necessary and to enable collaboration.

## 2. Time and change
- [from source] (SWE-G p.15) At some point between a throwaway program and a decades-long project the project must react to external changes. If there was no planning, the first update is painful for three compounding reasons: unprecedented task, inexperienced engineers and larger size (years of upgrades at once).
- [from source] (SWE-G p.15) Distinction "happens to work" versus "is maintainable".
- [from source] (SWE-G p.26) Footnote: most projects seem willing to update within five years; between 5 and 10 years is a conservative estimate for this transition (an observation of the book, not a rule).
- [from source] (SWE-G p.17) "Why not aim for nothing changing?": a project in pure C with no external dependencies may avoid refactorings, but most projects have exposure to technologies that change (vulnerabilities such as Heartbleed, Meltdown/Spectre, hardware efficiency). Change is not good in itself, but you must be able to change.

## 3. Hyrum's Law
- [from source] (SWE-G p.15) Statement: with a sufficient number of users of an API, it does not matter what you promise in the contract; all observable behaviors of the system will be depended on by somebody. Note (p.26): Hyrum tried to call it the "Law of Implicit Dependencies".
- [from source] (SWE-G p.15-16) It is compared to entropy: it does not remove the need for efficiency, it just has to be taken into account; it can be mitigated, never eradicated. Being clear about the interface's promises gives flexibility, but how hard a change is depends on how useful the observable behavior is to users.
- [from source] (SWE-G p.16) Example of hash table iteration order: experts say you cannot assume order; the nuanced answer is that, in short-lived code with no runtime change, it is fine, but without knowing the code's lifespan the assumption is incorrect. Reasons to change the order: hash flooding attacks and efficiency gains. Even if your implementation does not depend on the order, the caller of an RPC may come to depend on it.
- [from source] (SWE-G p.17) Some languages randomize hash order across versions or runs to avoid dependencies, but there are still surprises (code that uses the order as an inefficient random generator). In Ch. 1 this is described as what "some languages" do, not as Google policy.
- [from source] (SWE-G p.17) Sentence about "clever": it is programming if "clever" is a compliment; it is software engineering if "clever" is an accusation.

## 4. Scale and efficiency
- [from source] (SWE-G p.18) Everything the organization does repeatedly must scale well in human effort; test the policy by imagining 10x or 100x more engineers or code. Beware the "boiling frog" effect.
- [from source] (SWE-G p.18-19) Example of a policy that does not scale: deprecation where the team announces a removal date and pushes the migration onto clients. Alternative: the infrastructure team does the migration or updates in a compatible way (the "Churn Rule", from 2012).
- [from source] (SWE-G p.19) Long-lived development branches as a policy with a scale problem (the cost of resynchronizing and testing grows with the number of branches).
- [from source] (SWE-G p.19) Beyoncé Rule: if a problem caused by an infrastructure change was not detected by tests in the CI system, it is not the change's fault ("if you liked it, you should have put a CI test on it"). Implication: ad hoc tests outside the common CI do not count.
- [from source] (SWE-G p.20) The 2006 compiler upgrade (several thousand engineers, about five years without changing compilers): it was painful; the book concludes that the first update is much more expensive than the following ones and lists flexibility factors (expertise, stability, conformity, familiarity, policy).
- [from source] (SWE-G p.21) "Shift left": finding problems earlier in the workflow (design, implementation, review, tests, commit, canary, production) tends to cost less; defense in depth.

## 5. Trade-offs and costs
- [from source] (SWE-G p.21) Decisions must have an explicit reason ("because I said so" is cited as the place where bad decisions live); the goal is consensus, not unanimity, and there must be a decider.
- [from source] (SWE-G p.21-22) "Cost" includes financial, resource, personnel, transaction, opportunity and societal. The book states that, in software engineering, personnel cost is usually the limiting one (p.22).
- [from source] (SWE-G p.23) Two situations: measurable/estimable quantities (CPU/RAM/network conversion table) and subtle quantities, where experience, leadership and precedent are used.
- [from source] (SWE-G p.24) Example of distributed builds and the Jevons Paradox (consumption grows when efficiency increases); example of dependency versus fork (avoid forks of interfaces that cross projects and time, such as serialization formats and protocols).
- [from source] (SWE-G p.24-25) Data-based decisions need to be revisited when the data changes; leaders who admit mistakes are more respected.

## 6. What is NOT in Ch. 1
- The chapter does not name "three pillars"; [inference] the time-scale-trade-offs triad is the thematic axis (SWE-G p.13).
- It does not state that "Google randomizes the hash seed in tests". [extrapolation] Randomizing order in tests is a known practice and may be useful, but it is not a policy attributed to Google here.
- It does not state that "no change is 100% safe" nor give latency/optimization "10x" numbers; that was v1 package text with no backing on the page.
