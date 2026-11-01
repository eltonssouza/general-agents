# INDEX - TensorFlow.js (overview based on web page captures)

**Nature of the source:** 5 PDFs that are **captures of tensorflow.org/js pages (pt-br version, translated by Cloud Translation)**. Four have useful content; one is a 404 page. They are overview, setup and index pages; there is **no** text of the guide sections, the API or the cited tutorials (only their names and one-line descriptions). This agent is therefore a **doc-capture-based overview agent**: where the source does not cover, the answer is **NOT COVERED**.

## 1. Page convention
Citation = **code + PDF page** ("=== PAGE N ===" marker of the extracted text = page N of the capture PDF). There is no printed numbering. Example: `TFJS p.4`.

## 2. Source inventory
| Code | PDF | Pages | What it is | Useful? | Date on the page |
|---|---|---|---|---|---|
| TFJG | TensorFlowJS-Guide.pdf | 2 | "Guia TensorFlow.js" (TensorFlow.js Guide) page: list of 8 guide sections, each with a link and a one-sentence description | Yes (guide index, not the content) | Last updated **2022-01-24 UTC** (p.2) |
| TFJL | TensorFlowJS-Landing.pdf | 9 | Home page tensorflow.org/js: slogan, "How it works", 3 demos, blog news, community links | Partial (text heavily fragmented by the capture) | No "last updated"; blog posts from 2022-08-19 to **2023-03-30** (p.6) |
| TFJB | TensorFlowJS-Tutorial-Beginner.pdf | 2 | **404 page** ("Não foi possível encontrar essa página", This page could not be found), with the menu of the **TensorFlow Python** site (Installation, Quickstart, python/tf API reference). p.2 empty | **DO NOT use** | None |
| TFJS | TensorFlowJS-Tutorial-Setup.pdf | 7 | "Configurar um projeto TensorFlow.js" (Set up a TensorFlow.js project): browser (script tag, NPM) and Node.js (tfjs-node, tfjs-node-gpu, tfjs) with code snippets | Yes (the most substantive content) | Last updated **2023-11-15 UTC** (p.7) |
| TFJI | TensorFlowJS-Tutorials-Index.pdf | 5 | "Primeiros passos com o TensorFlow.js" (Getting started with TensorFlow.js) page: minimal tutorial (y = 2x - 1), plus "More ways to get started" (course, ml5.js, conversion, examples, tfjs-vis, data) | Yes | Last updated **2023-11-30 UTC** (p.5) |

Notes:
- **TFJB** (404): recorded and **discarded**; no agent claim comes from it. The file name suggests a "beginner tutorial", but the captured page is an error (the menu links are from the TensorFlow Python site, not TF.js).
- Dates differ across sources (2022-01, 2023-11); everything the agent says holds "as in the capture", [DATED] relative to those dates. The capture date itself **does not appear**.
- **TensorFlow.js version:** no numbered version appears; the examples use `@latest` (TFJS p.2, TFJI p.2). Claims about versions = NOT COVERED.

## 3. Reading coverage (honest)
- **Read in full:** the extracted text of the 5 sources (24 KB in total).
- **Checked visually (PyMuPDF render):** TFJS p.1-2 (the script tag line appears cut off in the capture), TFJI p.2-3 (the equation y = 2x - 1 and "2*20 - 1 = 39" were not in the extracted text; confirmed in the image), TFJL p.1.
- **Landing:** the extracted text is scrambled into narrow columns; only what is legible is stated (slogan, "How it works", 3 demos, posts, links).
- Images/illustrations (Landing hero) carry no textual information.

## 4. File map
| File | Content | Sources |
|---|---|---|
| 01-visao-geral.md | What TF.js is according to the Landing, "How it works", demos, community | TFJL |
| 02-guia-secoes.md | The 8 guide sections (name, link, description) | TFJG |
| 03-setup.md | Browser and Node.js: options, commands, snippets, notes | TFJS |
| 04-primeiros-passos.md | Minimal tutorial y = 2x - 1: prerequisites, commands, code, result | TFJI |
| 05-mapa-de-tutoriais.md | Topic -> resource named by the pages map (without their content) | TFJG, TFJL, TFJI |
| glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md | Cross-cutting | all |

## 5. Triggers -> file
| Question | Open |
|---|---|
| "what is TF.js? what can I do with it?" | 01 |
| "what does the guide cover? where do I learn tensors / saving a model?" | 02 (index only; the content is NOT COVERED) |
| "how do I install? script tag or npm? Node with GPU?" | 03 |
| "first example / hello world" | 04 |
| "which resource to convert a Keras model / visualize / data?" | 05 |
| any question on API, version, performance, WebGL/WASM/WebGPU, backends | NOT COVERED (see datado.md) |

## 6. Boundary
General machine learning (neural network concepts, optimizers, loss functions, deep learning, LLMs) belongs to the agents in `ROOT\09_ai_and_llm\_agents\` (for example, modern-deep-learning-expert, deep-learning-goodfellow-expert, llm-prompting-and-foundations-expert). This agent only reports what the TF.js pages say.
