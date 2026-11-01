# Fidelity and test report

Package: `agentic-ai-context-engineering-expert` v1.0.0. Sources: BAAS (*Building Agentic AI Systems*, Biswas and Talukdar, Packt, April/2025, 289 pp.) and CE2 (*Context Engineering 2.0*, Hua et al., arXiv 2510.26493, 10/30/2025, 28 pp.). Page convention: PDF (BAAS printed = PDF − 25; CE2 PDF = printed).

**Honesty statement:** the cases were run **by me, the package author**, against the agent, the references, and the scripts. **There was no blind run by an independent model.** The result measures internal coherence and fidelity to the pages, not the performance of an unknown model.

## 1. Reading coverage
- **BAAS:** extracted text of all 289 pages read sequentially in blocks of about 1,000 lines, with notes saved to disk after each block (outside the package). Blank pages: 13, 27, 51, 75, 99, 101, 131, 185, 213, 273, 283, 289. **Figures and diagrams were not visually inspected**; I rendered p.88 (utility) to confirm that the formal formula is not in the text. The full code of the examples is in external notebooks, not in the PDF.
- **CE2:** body (p.1-21) read in full; I rendered p.5 (definitions 2-4) and p.12 (definitions 5.1-5.3) and checked the formulas visually; references (p.22-28) sampled (used only to confirm that MCP appears in the notes). Figures 1-7 not inspected.
- Nothing in the body of the two texts was read "by sampling".

## 2. Automatic checks
| Check | Result |
|---|---|
| `tests/verify_citations.py --src <scratch/ai>` | 614 cited pages within range; JSON indexes and checklist with valid pages; **125 positive checks** (terms, names, and numbers of the references on the cited page) and **20 negative** (plausible claims that the texts do not contain), 0 failures |
| `tests/run_script_tests.py --src <scratch/ai>` | 60 checks, 0 failures (lookup 16, checklist 7, spec 10, calc 18, package 8, citations 1) |

Relevant negative checks (all pass): BAAS does not contain "context window", "context engineering", MCP, OWASP, jailbreak, KV cache, or RAG up to p.285 (the acronym appears only in an advertisement for another book on p.286); BAAS ch. 7 (p.186-211) does not contain "guardrails" (although the preface and ch. 8 say it does); the CE2 body (p.1-21) does not contain MCP (only the references), guardrails, prompt injection, agent benchmarks, "budget", or "pricing"; CE2 does not name "episodic memory" on p.12-14.

## 3. Running the cases (tests/casos-de-teste.md)
Result: **30 of 30 pass** by each case's criterion, with the caveats below. Cases with a script (C13-C17, C22, C24, C25) are reproduced by `run_script_tests.py`.
| Cases | How they were run | Result |
|---|---|---|
| C01-C06 (BAAS) | answers built only from `references/01`, `02`, `04`, `05`, `06`; pages checked with `ctx_lookup.py --page` | pass; C04 requires the caveat that CWD is the book's model |
| C07-C12 (CE2) | `references/09`, `10`, `11`; formulas checked in the rendering | pass; C08 requires the caveat that entropy is a metaphor; C10 requires not inventing θ |
| C13-C17 | scripts `agent_spec.py`, `ctx_calc.py`, `agent_checklist.py` | pass; numbers checked by hand (utility 95.00 and 127.50; cost 0.261840) |
| C18 | review of a booking agent without human approval, with findings from BAAS p.237-240 and p.134-135 | passes |
| C19 | framework comparison marked `[DATED]`, with p.154-160 | passes |
| C20-C21 | negative checks and `references/INDEX.md` §6 | pass (ch. 7 discrepancy recorded) |
| C22-C24 | `ctx_lookup.py --printed 64`, text of CE2 p.16, and `ctx_calc.py budget` | pass |
| C25-C27 | `ctx_lookup.py` (MCP, RAG, benchmarks) and `--gaps` | pass |
| C28-C30 | agent prompt (sections 2, 8, 9) | pass by inspection of the prompt; actual model behavior not tested blind |

## 4. Corrections made during the audit (for transparency)
The verifier and the manual review found, and I fixed:
1. Citation of BAAS Algorithm 2 (from p.70-72 to p.71-72) and the LangGraph state page (from "p.133" to p.158-159).
2. Page of the "shared context" example in the knowledge-management case (p.251 → p.252) and printed pages mixed into `datado.md` and the glossary (converted to PDF).
3. In `10-ce2-...`: "five patterns" of self-baking corrected to **four developed in the text**, plus the mention in Fig. 4 (p.9) of a fifth (direct structured storage), which the text does not develop.
4. Checks that failed on the first run: `TextMentionTermination` is on p.156 (not 155) and the title "State validation and consistency" on p.196 (not 197); the negative check for "ReAct" failed because it matched the common word "react" (BAAS uses "reactive"), so it was removed and the gap reworded.
5. Citation of CrewAI's `goal` (p.168).

## 5. Known limitations
- Figures and diagrams of both texts were not inspected; claims about figures come from the captions and the text.
- The company, product, and real-case examples in BAAS (ch. 4 and 10; p.236-238) **were not verified** and are `[DATED]`.
- The CE2 numbers (about 50% occupancy, 30 and 100 tools, 200 thousand tokens) are reports quoted by the paper (blogs and engineering reports), context-specific and from 2025; the scripts use them only as configurable alerts.
- `ctx_calc.py budget` and the structure of `agent_spec.py` are package constructions (`[inference]` and `[extrapolation]`); `memory-split` implements the CE2 p.12 definition and the tests verify the definitional logic, not a number from the paper (the paper has no numeric example). Only `utility --demo` reproduces printed numbers (BAAS p.89). The result of the weights example (0.33, 0.32, 0.34, p.113) comes from a tool whose code the book does not show, so it is not reproduced.
- The citation verifier checks key terms, not the full meaning of each sentence; the meaning was verified by me during reading and review and may have residual errors.
- The collection does not cover operational security of agents, quantitative evaluation, MCP/A2A, and RAG in BAAS; the agent declares NOT COVERED in these cases.

## 6. Pending items
- Blind test with an independent model following `tests/casos-de-teste.md`.
- Visual inspection of the figures (BAAS Figs. 1.1-9.1; CE2 Figs. 1-7) if a case depends on them.
- If there is a new edition of BAAS or a new version of the paper, revalidate the offset, pages, and `[DATED]` items.
