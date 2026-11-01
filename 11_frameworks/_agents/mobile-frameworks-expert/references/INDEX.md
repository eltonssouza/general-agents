# INDEX - mobile-frameworks-expert

**Overview agent based on documentation captures** of three short sources from the mobile universe: the **React Native** introduction, the home page of the **Flutter** documentation and **"A Swift Tour"** (the Swift language). It is not a complete reference for any of the three. What the sources do not say is **NOT COVERED** or, if the user asks, a labeled `[extrapolation]`.

## 1. Sources, versions and dates (recorded from the PDFs themselves)

| Code | PDF file | Pages | What it really is | Version / date that appears |
|---|---|---|---|---|
| **RN** | React-Native-Getting-Started.pdf | 4 (useful 1-3; p.4 is footer) | "Introduction" page of the React Native documentation (reactnative.dev): audience, prerequisites, Snack Player, "Developer Notes", formatting. It does **not** contain getting-started (p.1 says it "moved to their own section") | Version selector **0.87** (p.1); "Last updated on Aug 12, 2026" (p.4). [DATED] to Aug 12, 2026 |
| **FLT** | Flutter-Docs.pdf | 4 (useful 1-3; p.4 is footer/license) | "Flutter documentation" **landing page**: navigation cards (Install, Widget catalog, API docs, Learning resources, Videos, Create with AI), "New to Flutter?" blocks, Building layouts, Understanding constraints, interactivity, FAQ, videos. Almost only links; no tutorial | **No version or date** in the text. The PDF metadata indicates capture on Aug 18, 2026 (not printed on the page) |
| **SWT** | Swift-A-Tour-of-Swift.pdf | 19 (~19 thousand characters of prose; **code in image**) | "A Swift Tour" from *The Swift Programming Language* (swift.org): values, control flow, functions/closures, classes, enums/structs, concurrency, protocols, errors, generics | **Swift version does NOT appear** in the text or in the images. Footer: "Copyright 2014-2026"; PDF metadata: capture on Aug 18, 2026. [DATED] to 2026 |

"Current" state of any version: **the model's prior knowledge does not count**; only the text above. The Swift version **was not identified**: do not say "Swift 5" or "Swift 6" as if it were in the source (nor in which version `any`, `if` as an expression or actors existed: the text does not say).

## 2. Page convention
PDF page (marker `=== PAGE N ===`). The three sources **have no printed numbering**; PDF = the only numbering, no offset. Always cite with the code: `RN p.N`, `FLT p.N`, `SWT p.N`.

## 3. Capture quality (for those who cite)
- **SWT: the code is in an IMAGE** (raster), not extractable text. The `.txt` only has the prose and the "Experiment" boxes. The code snippets were read by **rendering all 19 pages** (PyMuPDF, 70 dpi) and checked by eye. Therefore the automatic citation verifier only checks the prose; claims that come from code are in the "visual check" list of the fidelity report. Such citations appear as `(SWT p.N, código)`.
- **SWT: scrollable code boxes truncated.** Several boxes were captured cut off (start/end of blocks on p.2-3, 5, 6-7, 9-10, 12-13, 14, 15-16, 17-18, 19; e.g. `calculateStatistics` p.6-7, `Square` p.9-10, `Rank`/`Suit` p.11-13, `anyCommonElements` p.19). The agent only asserts what is legible; it does not complete the rest from memory as if it were from the tour. Output lines ("// Prints ...") also appear cut off in some blocks.
- **SWT p.19:** site footer (copyright, CC BY 4.0, Light/Dark/Auto theme) overlaid on the final "Experiment".
- **RN p.2:** the **Snack Player** space (interactive example) came out blank: there is no example code. P.4 is footer only ("Is this page useful?", edit page, date).
- **FLT:** p.1-3 are links/cards; p.1 has the text "everything is a widget" with the word "widget" broken onto another line (rendered and checked). Embedded videos (p.2-3) came out as YouTube thumbnails (rendered: titles "What's new in Flutter", "Develop with Google Antigravity and Flutter", "Write great Flutter code" and "A Full-Stack Developer Guide" only appear in the image; the video itself is not in the capture). P.4 = license and footer links.
- **No page is a 404** or "Page not found". All three sources have some useful content; **RN and FLT are minimal sources**, SWT is the main source.

## 4. Map topic -> pages -> file

| Topic | Source and pages | File |
|---|---|---|
| React Native introduction: audience, prerequisites, Snack, notes, formatting, version 0.87 | RN p.1-4 | 01-react-native-introducao.md |
| Flutter landing: cards, "New to Flutter?", layouts, constraints, interactivity, videos, license | FLT p.1-4 | 02-flutter-landing.md |
| Swift: Hello world, let/var, types, strings, arrays/dictionaries, control flow, ranges, optionals, switch | SWT p.1-6 | 03-swift-valores-e-controle-de-fluxo.md |
| Swift: functions, argument labels, tuples, nested functions, functions as values, closures | SWT p.6-8 | 04-swift-funcoes-e-closures.md |
| Swift: classes, init/deinit, inheritance, override, computed properties, willSet/didSet, `?.` | SWT p.8-11 | 05-swift-classes-e-objetos.md |
| Swift: enums (raw values, associated values) and structs (copy vs. reference) | SWT p.11-14 | 06-swift-enums-e-structs.md |
| Swift: async/await, async let, Task, task groups, actors | SWT p.14-15 | 07-swift-concorrencia.md |
| Swift: protocols, mutating, extensions, protocol as a type (`any`) | SWT p.15-17 | 08-swift-protocolos-e-extensoes.md |
| Swift: errors (throw/throws/do-catch/try?/defer) and generics (`where`) | SWT p.17-19 | 09-swift-erros-e-genericos.md |
| Comparison RN x Flutter x Swift **by source criteria** | RN, FLT, SWT | 10-comparacao-rn-flutter-swift.md |
| Terms, procedures, cases, dated items | all | glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md |

## 5. Triggers -> file
| Question | Open |
|---|---|
| "what is React Native / prerequisites / Snack?" | 01 |
| "what does the Flutter doc say? layouts? constraints?" | 02 |
| "`let` or `var`? inference? interpolation? empty array?" | 03 |
| "argument labels, tuple, closure, `$0`?" | 04 |
| "class, init, override, getter/setter, willSet?" | 05 |
| "enum with associated values? struct vs. class?" | 06 |
| "async/await, Task, actor?" | 07 |
| "protocol, extension, mutating, `any`?" | 08 |
| "throws/try/catch/defer, generics/where?" | 09 |
| "which to choose: RN, Flutter or Swift?" | 10 (the sources do **not** recommend; NOT COVERED) |
| "SwiftUI, UIKit, Xcode, Dart, hot reload, navigation, state in RN, build/release..." | **NOT COVERED** (see `datado.md`) |

## 6. Reading coverage (honest)
- **Read in full:** RN (4 pages), FLT (4 pages), SWT (19 pages) as text; **all 19 SWT pages rendered and viewed** (code included); FLT p.1 and RN p.2 rendered.
- Extracted texts already existed in `scratch/frameworks/`; supporting images in `scratch/frameworks/mobile-frameworks-expert/notes/`.
- **Not checked:** the content of the Snack Player (RN p.2, blank) and of the videos (FLT p.2-3, thumbnails only): their content does not exist in the capture.
