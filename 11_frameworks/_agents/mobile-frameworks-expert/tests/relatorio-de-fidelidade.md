# Fidelity report - mobile-frameworks-expert

## Sources and reading
- **RN** (React-Native-Getting-Started.pdf, 4 pages): read in full; docs introduction, **0.87**, updated Aug 12, 2026; the Snack Player page came out blank; p.4 is footer only.
- **FLT** (Flutter-Docs.pdf, 4 pages): read in full; **landing page** (links/cards, videos as thumbnails), no version/date; p.4 license/footer.
- **SWT** (Swift-A-Tour-of-Swift.pdf, 19 pages, ~19 thousand characters of prose): read in full as text; **all 19 pages were rendered (70 dpi) and viewed** because the code is in images (no OCR in the environment). Swift version **not stated**; copyright 2014-2026.
- Extracted texts already existed in `scratch/frameworks/`; supporting images in `scratch/frameworks/mobile-frameworks-expert/notes/`.
- PDF metadata: captures on Aug 18, 2026 (not printed on the pages).

## Page convention
PDF page (the only numbering; the sources have no printed number). Sigla in the citation: `RN p.N`, `FLT p.N`, `SWT p.N`.

## Automatic citation verification (`tests/verify_citations.py`)
Run with `--src scratch/frameworks`:
- Range: all pages cited with a sigla and the bare `p.N` in the references are within the limits (RN 4, FLT 4, SWT 19).
- **95 positive checks** (key terms present on the cited pages, across the three sources) and **25 negative** (plausible claims that the sources do NOT bring: TypeScript/Hermes/Metro/hooks/navigation/commands in RN; hot reload/pubspec/Material/Cupertino/Impeller/Dart as a language in Flutter; SwiftUI/UIKit/Xcode/Swift version/guard/ARC/Sendable/platforms/`!`/associatedtype in SWT). **Failures: 0.**
- **19 "render" items** (one per SWT page 1-19): claims coming from the **code in images**, checked visually; the verifier only counts them and cannot check them automatically.
- Proof that the verifier fails when it should: with a fake checks file ("guard" in SWT p.3; absence of "javascript" in RN p.1) it reports 2 failures (exit 1).
- **Limit:** the checks confirm that key terms appear (or not) on the page, not that each paraphrased sentence is correct; sentence-by-sentence fidelity depends on the full reading and rendering done by the author.

## Script tests (`tests/run_script_tests.py`)
41 tests (lookup, comparator, linter with 4 fixtures + `--json`/`--no-info`/stdin/`--rules`, checklist, citation verification): **41 passed, 0 failed**. The scripts do not run analyzed code or access the network.
- Fixtures: `ruim.swift` (one violation per rule, 22 rules), `bom.swift` and `tour-like.swift` (no findings; `tour-like` reproduces the structure of the tour examples with changed names, to check for false positives), `injecao.swift` (instructions in comments/strings treated as data).
- During development the following were fixed: a false positive of `switch` over a fully covered enum (SWF-04), enum payloads (`case result(String, String)`) counted as cases, and the count of tour exercises (20, not 19).

## Conceptual cases
`tests/casos-de-teste.md` (32 cases: conceptual, practical, edge/NOT COVERED, out of scope, injection). Run by the author against agent + references + scripts. **There was no blind run by an independent model.**

## Known limitations
1. RN and FLT are minimal sources (introduction and landing page): almost everything is NOT COVERED; the agent is an overview based on doc-capture.
2. **SWT code in images and truncated** (scrolling boxes cut off on several pages): claims coming from the code depend on my visual reading at 70 dpi; cut-off snippets were not completed.
3. **Swift version not identified**: no claim about "when it appeared" or "in which version".
4. Heuristic linter (regex and brace counting), not a Swift parser: it may have false positives/negatives (e.g. same method names in different types, variable shadowing). Rules: SWF-01..03, 05..10, 12..17 [from source]; SWF-04, 11, 14, 19 [from source]+[inference]; SWF-18 and SWF-X1..X3 [extrapolation].
5. There is no change map per version: each source brings a single version.
6. The verifier does not reach the content of images (code, video thumbnails, blank Snack).
