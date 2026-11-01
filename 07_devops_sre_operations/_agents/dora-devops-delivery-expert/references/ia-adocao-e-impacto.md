# AI: adoption, attitudes and downstream impact (DORA24 p.17-46)

Convention: `(DORA24 p.N)`. Effects in "% per +25% AI adoption" are association estimates (observational survey), with 89% uncertainty intervals (p.108); see `metodologia-e-limites-estatisticos.md`.

## 1. Adoption (p.17-21)
- 81% of respondents say the organization prioritized AI more in applications/services; 49.2% describe the increase as moderate or significant; 3% report a reduction (within the margin of error); 78% trust that the organization is transparent about AI use (DORA24 p.18). [from source]
- Reliance on AI is statistically equal across industries; larger organizations report less reliance than smaller ones (DORA24 p.19). [from source]
- 75.9% rely on AI, at least in part, in one or more daily responsibilities (DORA24 p.19). [from source]
- Tasks (figure 3, p.20), percentage of those who have the task and use AI at least in part: writing code 74.9%; summarizing information 71.2%; explaining code 62.2%; optimizing code 61.3%; documenting 60.8%; writing tests 59.6%; debugging 56.1%; data analysis 54.6%; code review 48.9%; security analysis 46.3%; language migration 45%; codebase modernization 44.7% (DORA24 p.20). [from source]
- Interfaces: chatbots 78.2%; external web interfaces 73.9%; IDE 72.9%; internal web interfaces 58.1%; automated CI/CD pipelines 50.2%. The report warns that the CI/CD and internal platform numbers may be artificially low due to lack of awareness (DORA24 p.20). [from source]
- Data scientists/ML engineers rely more; hardware engineers, less (DORA24 p.20). [from source]
- Drivers in the interviews: competitive pressure and the perception of AI proficiency as a new entry requirement (DORA24 p.21). [from source] (11 interviews, p.109: indicative, not representative. [inference])

## 2. Perceptions (p.22-26)
- 75% report a productivity gain from AI in the previous three months; more than a third describe the gain as moderate (25%) or extreme (10%); less than 10% report a negative impact, even slight (DORA24 p.22). [from source]
- Largest gains: security professionals, system administrators and full-stack devs; smallest (but positive): mobile, SRE, project managers (DORA24 p.23). [from source]
- 67% report some improvement in their ability to write code; only 5% report harm (DORA24 p.23). [from source]
- Trust in the quality of generated code: 87.9% some level of trust; 39.2% little (27.3%) or none (11.9%) (DORA24 p.23; p.6 repeats 39.2%). [from source]
- Authors' hypothesis: absolute trust is not required; "almost right" code that is adjusted with touch-ups is already useful and compatible with existing quality processes (DORA24 p.24). [from source: authors' hypothesis]
- Expectations: positive for product quality; negative for careers, environment and society, with the negative impact fully felt in ~5 years (DORA24 p.25, figure 6). [from source]

## 3. How AI was measured (p.30)
- They measured **reliance** and not just frequency, since a rare task can be central (DORA24 p.30). [from source]
- Factor analysis: the overall reliance item overlaps with six tasks (writing code, summarizing, explaining, optimizing, documenting, writing tests), forming the "AI adoption" factor (DORA24 p.30; the text speaks of seven items, counting the overall item). [from source] + [inference about the count]

## 4. Impact on the individual (p.31-35), +25% adoption (figure 7, p.32)
| Outcome | Estimate | 89% interval (visual reading of the figure) |
|---|---|---|
| Flow | +2.6% | does not cross zero |
| Job satisfaction | +2.2% | does not cross zero |
| Productivity | +2.1% | does not cross zero |
| Time in toilsome work | +0.4% | crosses zero |
| Burnout | -0.6% | crosses zero |
| Time in valuable work | -2.6% | does not cross zero |
(DORA24 p.32) [from source]. The authors say +2.1% productivity seems small, but it is at the individual level (DORA24 p.32).
- The "complicated" part: more AI associated with **less** time in valuable work, with toil unchanged (DORA24 p.33). [from source]
- **Vacuum hypothesis** (the authors' explanation, not a result): AI speeds up the work the person considers valuable, time is left over, and that time is not filled with more valuable work (DORA24 p.33). AI does not help with toil (meetings, bureaucracy) (DORA24 p.35). The meaning of work comes from the impact on others, not from the act of coding (DORA24 p.34). [from source: hypothesis]
- Toil and burnout remained "stubborn" in the face of AI: AI did not worsen them (DORA24 p.35). [from source]

## 5. Impact on the development flow (p.36-38), +25% (figure 9, p.37)
- Documentation +7.5%; code quality +3.4%; review speed +3.1%; approval speed +1.3%; code complexity -1.8% (text, DORA24 p.37). Technical debt -0.8% and cross-functional coordination +0.1% (figure, p.37), with intervals that cross zero (visual reading); approval has an interval touching zero (visual reading). [from source] + [visual inference]
- Authors' caveats: faster review/approval does not mean better review; there may be overconfidence in AI; it is unclear whether quality improved because AI generated it or because AI helps extract value from low-quality code/docs; both explanations can coexist (DORA24 p.38). [from source]

## 6. Impact on delivery (p.39-40), +25% (figure 10)
- Delivery throughput: -1.5% (small, probably negative); delivery stability: -7.2% (DORA24 p.40; figure p.39). Both intervals far from zero (visual reading). [from source]
- Surprise: improvements in documentation, code quality, review, approval and complexity normally lead to better delivery; not here (DORA24 p.40). [from source]
- Authors' hypothesis: the field may have forgotten **small batches**; with AI, changelists tend to grow, and DORA has already shown that larger changes are slower and less stable (DORA24 p.40). **It is a hypothesis, not a measurement**: the report did not measure batch size at this point. [from source: hypothesis] + [inference]
- Conclusion: improving the development process does not automatically improve delivery, without adherence to basics such as small batches and robust tests; AI is not a panacea (DORA24 p.40). [from source]
- External context cited: research suggests code churn may double compared with the pre-2021 baseline (DORA24 p.28, external source cited by the report). [from source: external citation]

## 7. Impact on team, organization and product (p.41-44), +25% (figure 11)
- Organization +2.3%; team +1.4% (DORA24 p.43); product +0.2%, no obvious association (interval crosses zero in the figure, p.42; text p.43). [from source]
- Pearson correlations: product-team r = 0.56 (95% CI 0.51-0.60); product-organization r = 0.47 (95% CI 0.41-0.53) (DORA24 p.43). [from source]
- Authors' hypotheses: team/organization factors (communication, knowledge, decision-making, culture) are eased by AI; product depends more on development and delivery flow, still stabilizing, and on creativity/empathy; adoption is at an early stage, benefits and harms may take time (DORA24 p.43). Figure 12 (learning curves) is an abstraction, **not derived from real data** (DORA24 p.44). [from source: hypothesis]
- Connecting individual adoption to organizational performance is "hard and noisy", lunch analogy (DORA24 p.42); micro-macro leap explained on p.111.

## 8. Report recommendations for AI strategy (p.45-46) [from source]
1. Define a clear AI mission and policies, with transparent information (including where code may be placed and which tools are available) (DORA24 p.45).
2. Culture of learning and experimentation: dedicated time, autonomy, sandbox/low risk; consider mitigating risks with robust test automation; measure AI by downstream impacts (how it helps employees, those who use the product, team potential) and not just by adoption (DORA24 p.46).
3. Acknowledge trade-offs: less time in valuable work, excess reliance, gains in one area creating problems in another, impact on stability/throughput (DORA24 p.46).

## 9. AI in the product (p.67)
Teams that began including AI experiences for end users had a ~10% drop in delivery stability compared with those that did not; and this move is associated with more stable priorities, which the authors attribute to clarity of direction, not to AI itself (DORA24 p.67). [from source]

## 10. Limits and [DATED]
- Survey from early 2024 (p.22) about the tools of that moment: all adoption/trust numbers are [DATED] for use after 2024.
- Associations, not proven causality (DORA24 p.110).
- There is no analysis by AI tool/product or by batch size: NOT COVERED.
