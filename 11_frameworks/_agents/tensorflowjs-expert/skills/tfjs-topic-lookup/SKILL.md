---
name: tfjs-topic-lookup
description: "Finds on which pages of the tensorflow.org/js captures (guide, landing, setup and getting started) a topic is covered and confirms what has NO coverage (API, backends, guide section contents). Use before citing a page about TensorFlow.js, tfjs-node, setup or the y = 2x - 1 tutorial, and when the user asks \"do the captures talk about WebGPU/transfer learning?\". Do not use to answer the question itself: use the result to cite."
---

# Topic lookup with pages

Sources (citation = code + PDF page of the capture): TFJG (Guide, 2 pages, 2022-01-24), TFJL (Landing, 9), TFJS (Setup, 7, 2023-11-15), TFJI (Getting started, 5, 2023-11-30). TFJB (Tutorial-Beginner) is a 404 page: not a source. No numbered TF.js version; everything is `[DATED]`. The index is `../../scripts/tfjs_index.json`.

## Procedure

1. Run the query (read-only, no network; terms may be Portuguese or English):
   ```bash
   python -I <PKG>/scripts/tfjs_lookup.py "tfjs-node" [--top 5] [--json]
   python -I <PKG>/scripts/tfjs_lookup.py --page TFJS 4
   python -I <PKG>/scripts/tfjs_lookup.py --sources
   python -I <PKG>/scripts/tfjs_lookup.py --gaps
   ```
   (`<PKG>` = package root; from this skill, `../../`.) Exit 0 = answer (including the NOT COVERED message for a term); 1 = invalid code or page, or a call without arguments (prints the help).
2. Interpret: each line carries the topic, citations `[CODE p.N]` and the file in `../../references/`; open the file (start with `INDEX.md`) before asserting details. **NOT COVERED**: API, backends (WebGL, WASM, WebGPU), versions, guide section contents, step-by-step conversion and transfer learning, bundlers, detailed CUDA. Answer only as `[extrapolation]` and if asked, without a page. General ML: refer to the agents in the 09_ai_and_llm folder.
3. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

## Response format

Topic — `[from source] (CODE p.N)` — reference file — what the captures do not say — labels.

## Limits

The index summarizes, it does not replace the text. Navigation pages, license and fragments have no indexed topic. It is an overview guide, not an API one.
