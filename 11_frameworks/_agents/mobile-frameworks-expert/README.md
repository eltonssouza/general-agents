# mobile-frameworks-expert

An **overview agent based on documentation captures** about **React Native, Flutter and Swift**, built from three short sources (folder `14_frameworks`):

| Sigla | Source | Pages | Nature | Version/date (from the PDF itself) |
|---|---|---|---|---|
| **RN** | React-Native-Getting-Started | 4 (useful 1-3) | Introduction to the React Native documentation (audience, prerequisites, Snack Player, notes). **Minimal source** | docs **0.87**; "Last updated on Aug 12, 2026" [DATED] |
| **FLT** | Flutter-Docs | 4 (useful 1-3) | **Landing page**: cards, links, constraints sentence, videos. **Minimal source** | **no version or date**; capture of Aug 18, 2026 only in the metadata |
| **SWT** | Swift-A-Tour-of-Swift | 19 | *A Swift Tour* (language). **Main source**; code in **images**, several truncated boxes | **Swift version NOT stated**; copyright 2014-2026 [DATED] |

**Not a complete reference** for any of the three technologies. What the sources do not cover is **NOT COVERED** (installation, JSX/hooks/navigation in RN; Dart/widgets/hot reload in Flutter; SwiftUI/UIKit/Xcode/`guard`/ARC/version in Swift; network, testing, build, performance; **recommendation of which to choose**) (`python -I scripts/mob_lookup.py --gaps`). Prior knowledge about versions **does not count**: only the text that was read, with `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`. **Web** React/Next.js belongs to `nextjs-react-expert`; native Kotlin/Android is not covered.

## Page convention
PDF page (marker `=== PAGE N ===`); the sources have no printed numbering. Map and capture quality (code in images, truncated, blank Snack): `references/INDEX.md`.

## What was read
- **In full:** RN (4 pages), FLT (4), SWT (19), as text extracted with PyMuPDF; **all 19 SWT pages were rendered and viewed** (the code only exists as an image); FLT p.1-3 and RN p.2 rendered.
- **Not checked:** the content of the Snack Player (RN p.2, blank) and of the videos (FLT p.2-3, thumbnails only): it does not exist in the capture.
- Notes and images: `scratch/frameworks/mobile-frameworks-expert/notes/`.

## Structure
```
mobile-frameworks-expert/
├── .claude-plugin/plugin.json
├── agents/mobile-frameworks-expert.md            # canonical prompt + frontmatter
├── AGENTS.md                                     # Codex adapter
├── .github/agents/mobile-frameworks-expert.agent.md   # GitHub Copilot adapter
├── references/  INDEX.md, 01..10 (by real topic), glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md
├── skills/       4 skills (SKILL.md per folder): mobile-topic-lookup, mobile-compare, swift-static-lint, swift-tour-checklist
├── scripts/     mob_lookup.py + mob_index.json, mob_compare.py, swift_lint.py, swift_tour_checklist.py
└── tests/       casos-de-teste.md, relatorio-de-fidelidade.md, verify_citations.py, citation-checks.json,
                 run_script_tests.py, fixtures/
```
Copy of the tests: `14_frameworks/_agents_tests/mobile-frameworks-expert/`.

## Installation
**Important:** formats and fields change between versions. Check the current documentation of each platform (Claude Code, OpenAI Codex, GitHub Copilot) before installing.

### Claude Code
- Local plugin: `claude --plugin-dir <path>/mobile-frameworks-expert`; or copy `agents/mobile-frameworks-expert.md` to `~/.claude/agents/` (or `.claude/agents/`) and `references/` and `scripts/` to an accessible location, adjusting paths.
- Via the collection marketplace (`general-agents/.claude-plugin/marketplace.json`): `/plugin marketplace add /path/to/general-agents` and then `/plugin install mobile-frameworks-expert@general-agents`.
- Usage: `@mobile-frameworks-expert what does the tour say about optionals?`

### OpenAI Codex (and agents that read `AGENTS.md`)
- Copy `AGENTS.md`, `agents/`, `references/` and `scripts/` to the repository root.

### GitHub Copilot (custom agent)
- Copy `.github/agents/mobile-frameworks-expert.agent.md` to the target repository's `.github/agents/` and `references/` and `scripts/` to the root (or adjust `<PKG>` in the file).

## Using the scripts (from the package root; Python 3 stdlib, no network, they never run the analyzed code)
```bash
python -I scripts/mob_lookup.py optional
python -I scripts/mob_lookup.py swiftui                    # NOT COVERED (only mentioned as a link in FLT)
python -I scripts/mob_lookup.py --page SWT 14
python -I scripts/mob_compare.py table
python -I scripts/mob_compare.py show layout concorrencia
python -I scripts/mob_compare.py ask "which is better?"      # NOT COVERED
python -I scripts/swift_lint.py tests/fixtures/ruim.swift
python -I scripts/swift_lint.py MyCode.swift --json --no-info
python -I scripts/swift_tour_checklist.py scan tests/fixtures/tour-like.swift
python -I scripts/swift_tour_checklist.py next --done 1,2,3
python -I tests/run_script_tests.py --src <folder with the 3 extracted .txt files>
python -I tests/verify_citations.py --src <folder with the 3 extracted .txt files>
```
Files expected in `--src`: `React-Native-Getting-Started.txt`, `Flutter-Docs.txt`, `Swift-A-Tour-of-Swift.txt` (text per page with `=== PAGE N ===`).

The lookup and comparator criteria accept Portuguese and English keywords (e.g. `concorrencia`/`concurrency`, `desembrulhar`/`unwrap`).

## Limitations
- Short, dated sources; RN and Flutter are almost only navigation; the Swift Tour has code in images and truncated.
- Heuristic linter (regex and brace counting, not a Swift parser); rules backed by the tour, except SWF-X1..X3 and SWF-18 [extrapolation], SWF-04/19 [inference]. "No findings" does not prove it compiles.
- The automatic verifier only checks the **prose**; claims that come from the tour's code were checked visually (19 `render` items in `tests/citation-checks.json`).
- No map of changes per version (one version per source).
- **Independent testing:** the cases were run by the author; there was no blind run by an independent model (`tests/relatorio-de-fidelidade.md`).
