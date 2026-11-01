# Developer experience, culture, leadership and transformation (DORA24 p.57-82)

Convention: `(DORA24 p.N)`. "Per +25%" leadership estimates: figure 18 (p.72). The authors' hypotheses are marked.

## 1. User focus (user-centricity) (p.58-62, 73)
- Survey questions: incorporating feedback to reprioritize; knowing what users want to accomplish; believing that focusing on the user is key to the business; believing that user experience is a business priority (DORA24 p.58). [from source]
- Finding: organizations that see user needs as a guide build better products; user focus increases productivity and satisfaction and reduces burnout risk (DORA24 p.59). [from source]
- **Highlighted finding (figure 15, p.60)**: when the organization knows user needs, delivery stability and throughput are **not** a requirement for product quality (it will be high if user experience comes first); without user focus, "doubling down" on fast and stable delivery is the only path to product quality (DORA24 p.59-60). [from source] Caution: this is a reading of the report's figure/text about predicted association; it is not a license to ignore delivery. [inference]
- Proposed mechanisms (hypotheses): sense of direction and purpose (p.61); more cross-functional collaboration, breaking down silos (p.62). External data cited on meaning at work: 93% consider it important; average willingness to give up 23% of future earnings (DORA24 p.61; external sources of the report). [from source: external citation]
- Recommendation: do not assume; observe users, ask and pivot; invest time and resources in getting to know users (DORA24 p.62). [from source]
- 2023: user-centered teams had 40% higher organizational performance than the others; in 2016 as well, better (DORA24 p.73, citing the 2023 report). Organizations can succeed without high speed/stability if user-focused (DORA24 p.73). [from source]
- Internal developers are also users; successful IDPs are developed as a product (DORA24 p.73). [from source]

## 2. Documentation (p.63-64)
- User focus + quality internal documentation amplify product performance (figure 16); without user signals, documentation does not significantly affect predicted product performance; with quality documentation, user signals weigh more (DORA24 p.63). [from source]
- Docs propagate user signals and feedback across the team and into the product (DORA24 p.63). The quality measure includes findability and reliability; the main audience is colleagues (or the "future you") (DORA24 p.64). [from source]
- The Agile Manifesto says "working software over comprehensive documentation"; the report still holds that quality documentation is part of working software; "comprehensive" may represent unhealthy practices (bureaucracy, distrust, writing without maintaining); excess can be as bad as lack (DORA24 p.64). [from source]
- Practices for a documentation culture (DORA24 p.64): document critical use cases; technical writing training; define an owner and an update process; distribute the work across the team; keep docs as part of the development cycle; delete obsolete/redundant docs; recognize the work in reviews and promotions. [from source]

## 3. Unstable priorities (p.65-68)
- Result: small but significant drops in productivity and **substantial** increases in burnout when priorities are unstable (DORA24 p.65). [from source]
- Not mitigated: strong leaders, good documentation and user focus do **not** offset the effect of unstable priorities on burnout (DORA24 p.65). [from source]
- Hypotheses (p.66): unclear expectations, less sense of control, more workload; the problem is the **frequency** of change, not the change itself (malleable priorities can be good); parallel with the chronic stress literature. [from source: hypothesis]
- Counterintuitive (p.66): when priorities stabilize, delivery performance drops (slower and less stable). Hypotheses: products in good shape change less; or shipping in larger batches. The authors call it an unexpected finding and ask the reader why. [from source: open hypothesis]
- Including AI experiences for users stabilizes priorities (clarity of direction), but comes with a ~10% drop in delivery stability (figure 17, p.67). [from source]
- Recommendation: stabilize priorities and protect people from the day-to-day affected by constant change; beyond that there is little to do against burnout in this case (DORA24 p.68). [from source]

## 4. Transformational leadership (p.70-73)
- Five dimensions (DORA24 p.70) [from source]: vision; supportive leadership; inspirational communication; intellectual stimulation; personal recognition.
- +25% transformational leadership (figure 18, p.72; all intervals far from zero in visual reading): satisfaction +9.1%; burnout -9.9%; productivity +8.7% (text p.71 says "9%"); team +8.7%; product +4.5%; organization +10.3% (DORA24 p.71-72). [from source]
- A 2017 study showed a statistically significant relationship between the dimensions and IT performance; strong correlation with eNPS (DORA24 p.71). [from source]
- Transformational leadership alone does not lead to high performance; it is an **enabler** of technical and product practices, via delegation of authority and autonomy, metrics and business intelligence to solve problems, and incentives based on delivering value rather than features (DORA24 p.71). Transformation requires allocated time and resources; engineers should not have to learn and automate in their spare time (DORA24 p.71). [from source]
- IT as an investment and not a cost; the ROI of DevOps whitepaper (2020) provides calculations (not reproduced in the report); dedicate specific capacity to improvement (DORA24 p.72). [from source]

## 5. Data orientation (p.74)
- More than 30 capabilities and processes identified (DORA24 p.74; list at dora.dev/capabilities, not in the report). [from source]
- Metrics as a requirement for excellence; deciding with data is usually preferable to opinion or intuition (DORA24 p.74). [from source] For the rules on using the four keys, see `metricas-de-entrega-e-niveis.md` section 4.

## 6. Cloud (p.6, 75)
- Flexible infrastructure = the five NIST characteristics (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) (DORA24 p.75). Successful teams use this flexibility more (DORA24 p.75). [from source]
- 2023 finding reiterated: using cloud without leveraging the five characteristics can be harmful and predicts a drop in organizational performance; it may be better to stay in the data center if there is no willingness to radically transform the application/service; iterative approach, starting with a few services (DORA24 p.75; p.6). [from source]

## 7. Transformation, J-curve and continuous improvement (p.69, 76, 81)
- Key to success: a continuous improvement mindset; high performance understands the variables holding the team back and improves methodically, using the DORA metrics as a baseline (DORA24 p.69). [from source]
- Transformation is a journey, not a destination; those who do not improve continuously "fall behind"; J-curve (initial dip and then large gains) with DevOps, SRE and, in 2024, platform engineering (DORA24 p.76). [from source]
- Do not get stuck planning the perfect transformation; "be a little better than yesterday"; "get better at getting better" (DORA24 p.76, p.81). [from source]
- Culture: one of the clearest predictors of performance; high-trust culture with a climate of learning and collaboration; it was the biggest predictor of security practices in application development in the 2022 research (DORA24 p.81). Well-being measures: burnout, productivity and satisfaction (DORA24 p.81). Westrum is cited as inspiration (DORA24 p.81). [from source]
- Software delivery + operational performance predict organizational performance and well-being (DORA24 p.80). [from source]

## 8. History and context (p.78-79, 82)
Timeline: 2009 Flickr (10 deploys per day) and first DevOpsDays in Ghent; 2011 survey; 2013 State of DevOps Report; 2014 Forsgren joins and links delivery performance to organizational performance (50% more market value growth over three years for public companies with high-performing IT); 2016 founding of DORA; 2017 the book *Accelerate*; 2018 independent DORA report and acquisition by Google Cloud at the end of the year; 2024 is the 10th report (there was none in 2020) (DORA24 p.78, 82). [from source]
Note: the report indicates that the term "DevOps" should leave the spotlight and that the research will remain platform-agnostic (DORA24 p.82). [from source]

## 9. Limits
Culture/leadership effects are survey associations; priority stability and user focus have no numeric effect estimate in the text (only direction and qualitative order of magnitude), except the ~10% drop in stability with AI in the product (p.67). NOT COVERED for other technical capabilities (CI/CD etc.).
