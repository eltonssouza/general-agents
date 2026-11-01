# INDEX: collection of the agentic-ai-context-engineering-expert agent

This agent uses **two sources** (closed collection). Both are `[DATED]` (2025); nothing here describes the current state of the art.

| Acronym | Source | Details |
|---|---|---|
| **BAAS** | *Building Agentic AI Systems: Create intelligent, autonomous AI agents that can reason, plan, and adapt* | Anjanava Biswas and Wrick Talukdar; Packt Publishing (Birmingham, UK); first published **April 2025**; ISBN 978-1-80323-875-3; forewords by Matthew R. Scott and Alex Acero; 289 PDF pages, native text (BAAS p.1-3). Pages 24 and 287 call the book *Building Agentic Systems with Generative AI* (variation within the PDF itself). Full code is in the book's GitHub notebooks, **not** in the PDF |
| **CE2** | *Context Engineering 2.0: The Context of Context Engineering* | Qishuo Hua, Lyumanshan Ye, Dayuan Fu, Yang Xiao, Xiaojie Cai, Yunze Wu, Jifan Lin, Junfei Wang and Pengfei Liu (SII-GAIR; SJTU, SII, GAIR); arXiv:2510.26493v1 [cs.AI], **30 October 2025**; 28 pages (body p.1-21; references p.21-28). Conceptual position paper, with no experiments of its own |

## 1. Page convention (always use this)
- **"BAAS p.N" = PDF page** (marker `=== PAGE N ===` of the extracted text). **Printed page = PDF − 25** in the body (ch. 1 starts on printed 3 = PDF 28). Preface in Roman numerals (xix = PDF 20); back-of-book index on printed 249-257 = PDF 274-282. The offset was checked against the book's index (for example "abductive reasoning 59-61" = PDF 84-86).
- **"CE2 p.N" = PDF page = printed page** (no difference).
- Blank pages of BAAS (dividers): 13, 27, 51, 75, 99, 101, 131, 185, 213, 273, 283, 289.
- `python -I scripts/ctx_lookup.py --printed N` converts printed to PDF (BAAS); `--page N --fonte BAAS|CE2` shows chapter and topics.

## 2. Reading coverage (precise statement)
- **BAAS:** the extracted text of all **289 pages** was read sequentially, in blocks, with per-block notes saved to disk (outside the package). This includes preface, table of contents, the 11 chapters, the back-of-book index (used to check the offset) and the final pages. **Figures and diagrams were not visually inspected** (only the extracted text); p.88 was rendered to check that the formal utility formula is not in the text. The code of the GitHub notebooks is not part of the PDF.
- **CE2:** the body (**p.1-21**) was read in full; the **formulas on p.5 and p.12 were checked by rendering**. The references (p.22-28) were only sampled and are not used as a source of claims (MCP, for example, appears only there). Figures 1-7 were not visually inspected.
- **No** blind reading by an independent model was done (see `tests/relatorio-de-fidelidade.md`).

## 3. Chapter map
| Source | Ch. | Title | PDF | Printed start | Reference |
|---|---|---|---|---|---|
| BAAS | 1 | Fundamentals of Generative AI | 28-50 | 3 | `01-baas-fundamentos-e-arquiteturas.md` |
| BAAS | 2 | Principles of Agentic Systems | 52-74 | 27 | `01-baas-fundamentos-e-arquiteturas.md`, `05-baas-multiagente-cwd.md` |
| BAAS | 3 | Essential Components of Intelligent Agents | 76-98 | 51 | `02-baas-componentes-raciocinio-e-planejamento.md` |
| BAAS | 4 | Reflection and Introspection in Agents | 102-130 | 77 | `03-baas-reflexao-e-introspeccao.md` |
| BAAS | 5 | Enabling Tool Use and Planning in Agents | 132-161 | 107 | `04-baas-ferramentas-planejamento-e-frameworks.md` |
| BAAS | 6 | Exploring the Coordinator, Worker, and Delegator Approach | 162-184 | 137 | `05-baas-multiagente-cwd.md` |
| BAAS | 7 | Effective Agentic System Design Techniques | 186-211 | 161 | `06-baas-design-prompts-estado-memoria-e-workflows.md` |
| BAAS | 8 | Building Trust in Generative AI Systems | 214-229 | 189 | `07-baas-confianca-seguranca-e-etica.md` |
| BAAS | 9 | Managing Safety and Ethical Considerations | 230-245 | 205 | `07-baas-confianca-seguranca-e-etica.md` |
| BAAS | 10 | Common Use Cases and Applications | 246-263 | 221 | `08-baas-aplicacoes-e-futuro.md` |
| BAAS | 11 | Conclusion and Future Outlook | 264-272 | 239 | `08-baas-aplicacoes-e-futuro.md` |
| CE2 | 1-2 | Introduction; Theoretical Framework | 3-6 | n/a | `09-ce2-definicao-e-eras.md` |
| CE2 | 3 | Historical Evolution (Era 1.0 and 2.0) | 6-8 | n/a | `09-ce2-definicao-e-eras.md` |
| CE2 | 4-5 | Context Collection and Storage; Context Management | 9-14 | n/a | `10-ce2-coleta-e-gestao-de-contexto.md` |
| CE2 | 6 | Context Usage | 14-19 | n/a | `11-ce2-uso-praticas-e-desafios.md` |
| CE2 | 7-9 | Applications; Challenges and Future Directions; Conclusion | 19-21 | n/a | `11-ce2-uso-praticas-e-desafios.md` |

## 4. When to open each file
| Question / trigger | Open |
|---|---|
| What an agent is, agency, autonomy, deliberative/reactive/hybrid architectures, MAS | `01-baas-fundamentos-e-arquiteturas.md` |
| Knowledge representation, reasoning, utility, classical planning | `02-baas-componentes-raciocinio-e-planejamento.md` |
| Reflection, meta-reasoning, self-explanation, self-modeling | `03-baas-reflexao-e-introspeccao.md` |
| Tools, tool calling, LLM planning/HTN, CrewAI/AutoGen/LangGraph | `04-baas-ferramentas-planejamento-e-frameworks.md` |
| Coordinator/worker/delegator, roles, communication between agents | `05-baas-multiagente-cwd.md` |
| Prompts, state, environment, memory, context (the book's view), workflows | `06-baas-design-prompts-estado-memoria-e-workflows.md` |
| Trust, XAI, agent risks, action limits, rollback, HITL, testing | `07-baas-confianca-seguranca-e-etica.md` |
| Case studies and perspectives | `08-baas-aplicacoes-e-futuro.md` |
| Formal definition of context engineering, entropy, eras | `09-ce2-definicao-e-eras.md` |
| Collection, storage, layered memory, isolation, self-baking | `10-ce2-coleta-e-gestao-de-contexto.md` |
| Sharing, selection, KV cache, tools, applications, challenges | `11-ce2-uso-praticas-e-desafios.md` |
| Relating the two texts | `12-cruzamento-baas-ce2.md` |
| Terms, design steps, cases and antipatterns, dated items | `glossario.md`, `procedimentos.md`, `casos-e-antipadroes.md`, `datado.md` |

## 5. What the collection does NOT cover (answer "NOT COVERED")
Verifiable list: `python -I scripts/ctx_lookup.py --gaps`. Main ones: MCP and A2A as protocols (MCP only in CE2 references); RAG in BAAS (in CE2 only as a retrieval technique, p.3, 12, 16-17); prompt injection and agent threat models (BAAS cites "prompt injection" once, p.46); agent benchmarks and quantitative evaluation; named observability; ReAct/Reflexion techniques; token budgeting, pricing and *prompt caching* as a method (CE2 treats KV cache only qualitatively, p.18); vendor SDKs; AGENTS.md/CLAUDE.md-type files (only GEMINI.md, CE2 p.19). BAAS **does not use** the terms "context window" nor "context engineering".

## 6. Recorded internal discrepancies
1. **BAAS title:** cover/copyright say *Building Agentic AI Systems*; p.24 and p.287 say *Building Agentic Systems with Generative AI* (BAAS p.1, 3, 24, 287).
2. **BAAS ch. 7 and guardrails:** the preface (p.21) and the opening of ch. 8 (p.214) say that ch. 7 covers guardrails, constraints and autonomy × control, but the text of ch. 7 (p.186-211) has no such section; the equivalent content is in ch. 9 (p.237-240). Verified by negative check.
3. **BAAS p.88 code:** the utility function uses `conv_utility` and then `convenience_utility` (variable name inconsistency); the printed numbers (95.00 and 127.50) match the correct calculation.
