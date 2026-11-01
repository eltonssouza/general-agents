# Threat Modeling Manifesto (TMM): values, principles, patterns and anti-patterns

Source: **TMM** = *Threat Modeling Manifesto* (working group of 15 authors; 3-page PDF; CC BY 4.0 license). Convention: PDF page = document page (TMM p.1 to p.3). Everything below was read on the cited pages; paraphrase is mine.

## What it is and what it is for (TMM p.1)
- **[from source] (TMM p.1)** Threat modeling is analyzing *representations* of a system to highlight concerns about **security and privacy** characteristics.
- **[from source] (TMM p.1)** At a high level, **four questions** are always asked:
  1. *What are we working on?*
  2. *What can go wrong?*
  3. *What are we going to do about it?*
  4. *Did we do a good enough job?*
- **[from source] (TMM p.1)** Why: you come to recognize what can go wrong, locate design and implementation problems that require mitigation, early or throughout the system's life; the output (the *threats*) informs design, development, testing and post-deployment decisions.
- **[from source] (TMM p.1)** Who: "you, everyone", anyone concerned with the privacy, security and *safety* of their system.
- **[from source] (TMM p.1)** How to use the manifesto: as a guide to develop or refine your own methodology. It contains **ideas, it is not a how-to** and is **methodology-agnostic**. The format imitates the Agile Manifesto: *values* (something with relative merit; we value the item on the left more than the one on the right) and *principles* (fundamental truths; three types: general truths that make threat modeling viable, recommended patterns and anti-patterns to avoid).

## The five values (TMM p.1) (left > right)
1. A **culture of finding and fixing design issues** > "checkbox" compliance.
2. **People and collaboration** > processes, methodologies and tools.
3. A **journey of understanding** > a security or privacy snapshot.
4. **Doing** threat modeling > talking about it.
5. **Continuous refinement** > a single delivery.

## The four principles (TMM p.2)
1. The best use of threat modeling is to improve security and privacy through analysis **early and often**.
2. It must **align with the organization's development practices** and follow design changes in **iterations**, each scoped to **manageable portions** of the system.
3. Results are meaningful when they have **value for stakeholders**.
4. **Dialogue** is the key to the shared understandings that generate value; **documents** record those understandings and enable **measurement**.

## Patterns that help (TMM p.2)
| Pattern | Idea (paraphrase) |
|---|---|
| Systematic Approach | Rigor and repeatability when applying security and privacy knowledge in a structured way |
| Informed Creativity | Leave room for creativity: craft and science |
| Varied Viewpoints | Diverse team, with specialists and cross-functional collaboration |
| Useful Toolkit | Tools that increase productivity, improve workflows, provide repeatability and measurability |
| Theory into Practice | Field-tested techniques, aligned with local reality and informed by the latest thinking on their benefits **and limits** |

## Anti-patterns that get in the way (TMM p.2)
The text of each card describes the right stance against the anti-pattern.
| Anti-pattern | What the text says (paraphrase) |
|---|---|
| Hero Threat Modeler | Does not depend on innate skill or a single mindset; everyone can and should do it |
| Admiration for the Problem | Go beyond analyzing; seek practical and relevant solutions |
| Tendency to Overfocus | Do not lose the big picture (parts of the model are interdependent); avoid overemphasizing adversaries, assets or techniques |
| Perfect Representation | It is better to create **several** representations: there is no single ideal view and each new one can illuminate different problems |

## About the document (TMM p.3)
- **[from source] (TMM p.3)** Intent: share a distilled version of the collective knowledge to inform, educate and inspire the adoption of threat modeling and improve security and privacy during development. Current version at threatmodelingmanifesto.org [DATED: confirm on the website].
- **[from source] (TMM p.3)** Authors (working group): Zoe Braiterman, Adam Shostack, Jonathan Marcil, Stephen de Vries, Irene Michlin, Kim Wuyts, Robert Hurlbut, Brook S.E. Schoenfield, Fraser Scott, Matthew Coles, Chris Romeo, Alyssa Miller, Izar Tarandach, Avi Douglen, Marc French; thanks to Loren Kohnfelder and Sheila Kamath for the technical review.

## What the TMM does NOT provide
The manifesto does **not** describe STRIDE, DFD/data flow diagrams, attack trees, DREAD, PASTA, LINDDUN, trust boundaries, session steps, report format, nor numeric "good enough" criteria (verified in the text of the 3 pages). All of this, if used, is **[extrapolation]**. It also does not define "dialogue" or "stakeholder" beyond what is stated above.

## Operational use (inference)
- **[inference]** The four questions form a loop: the answer to the 4th feeds back into the 1st (value 5, continuous refinement; principle 2, iterations).
- **[inference]** "We already did threat modeling" as an isolated slide or document goes against values 3, 4 and 5 and principle 4.
