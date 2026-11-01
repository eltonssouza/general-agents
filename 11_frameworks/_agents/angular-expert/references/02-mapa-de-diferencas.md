# 02 — Difference map between the NG18 to NG22 Overviews

**Golden rule:** what is compared is the **text of five captures**, not the framework. "Appears in A and not in B" = the text of B does not mention it; it does **not** mean removed, obsolete or incompatible. Comparator: `python -I scripts/ng_diff.py diff --from 18 --to 22` (also `--raw --src DIR`, `matrix`, `concept ID`, `meta`). Data: `scripts/ng_index.json` and `scripts/ng_changes.json`.

## Summary in one table (PDF pages)

| Item | NG18 | NG19 | NG20 | NG21 | NG22 |
|---|---|---|---|---|---|
| Pages / footer | 6 / 2010-2024 | 7 / 2010-2025 | 7 / 2010-2025 | 9 / 2010-2026 | 9 / 2010-2026 |
| "Built by Angular at ..." stamp | no | no | no | v21.2.20 (p.9) | v22.1.2 (p.9) |
| Useless pages | none | p.1 | p.7 | p.9 | p.9 |
| Opening "that users love"; "Angular.dev is the official home" | no | no | no | p.1 | p.1 |
| Headline "opinionated component model + flexible DI" | p.1 | p.2 | p.2 | no | no |
| DI described as modular/decoupled/testable | p.1 | p.3 | p.2 | no | no |
| DI as "sharing code between components" | no | no | no | p.3 | p.3 |
| Signals (fine-grained reactivity) | p.1-2 | p.2-3 | p.2 | p.2 | p.2 |
| SSR, SSG, hydration | p.2 | p.3 | p.2 | p.3 | p.3 |
| `@defer` / deferred loading / lazy templates | p.2 | p.3 | p.2 | no | no |
| Router + forms | p.2 | p.3 | p.2 | p.3 | p.3 |
| CLI, DevTools, `ng update`, language service | p.2-3 | p.3-4 | p.3 | p.3-4 | p.3-4 |
| Security, i18n, Vite/esbuild, monorepo, LTS | yes | yes | yes | yes | yes |
| Bluesky in the footer | no | p.7 | p.6 | p.8 | p.8 |
| Language footer | "Languages" (5: zh-CN, zh-TW, ja, ko, Greek) p.6 | "Languages" (5) p.7 | "Languages" (4, no Greek) p.6 | "Community translations" (8) p.8 | same p.8 |

## Step by step

### NG18 → NG19 (same content; different captures)
- Body text with the same concepts; changes only in the footer: copyright 2010-2024 → 2010-2025 (NG18 p.6; NG19 p.7) and **Bluesky** enters the list of networks (NG19 p.7).
- Capture artifact: NG19 p.1 is only cookies and navigation; the body starts on p.2; DevTools sentences are split between p.3 and p.4 (NG19 p.3-4).

### NG19 → NG20
- Same body. The language list goes from 5 to 4: Greek (Ελληνικά) is in NG19 p.7 and not in NG20 p.6. Same copyright (2010-2025).
- Artifact: the last page (p.7) is only copyright; the sentence about compatibility and migration tools is split between p.3 and p.4.

### NG20 → NG21 (the big change; it is one of **presentation and wording**)
- Opening: "...fast, reliable applications **that users love**" and "Angular.dev is the official home of the documentation" (NG21 p.1). The invitation to see code becomes two cards, Essentials and Tutorials.
- Features become **cards by title**: Components, Angular Signals, Server-side rendering, Dependency injection, Angular Routing, Forms in Angular (NG21 p.2-3) and, afterwards, CLI, DevTools, `ng update`, Language Service (NG21 p.3-4), with "Explore ..." links.
- **Do not appear in NG21** (but appeared in NG18-NG20): the headline about the opinionated component model and flexible DI; the "modular, decoupled, testable" DI description; the performance headline with deferred loading and the text about `@defer`; the headlines "make sure everything works together...", "never miss a version with ng update" and "productivity with IDE integration"; the expression "browser extension" in DevTools. The content on router, forms, `ng update`, DevTools and language service **remains** in the new cards.
- Footer: "Languages" → "Community translations" (8 languages, including Azərbaycanca, Español, Türkçe, Русский); copyright 2010-2026; stamp "Built by Angular at v21.2.20+sha-..." (NG21 p.8-9).
- Spelling: "ESBuild" (NG18-NG20) → "esbuild"; "Tensorflow" → "TensorFlow".

### NG21 → NG22
- Identical body (4-gram comparison found no difference). Only the version label (v22) and the stamp (v22.1.2+sha-...) change. Nothing can be concluded about framework changes between 21 and 22 from this collection.

## What CANNOT be claimed
- That `@defer`, modular DI, "browser extension" etc. were removed or stopped being valid in NG21/NG22.
- That NG22 brings nothing new: the Overview simply does not list it.
- Anything about advanced signals, standalone, zoneless, control flow, Signal Forms etc.: **NOT COVERED** (`03-sem-cobertura.md`).
- Release or end-of-support dates for any version.
