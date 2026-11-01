# [DATED] items and gaps

Rule: [DATED] is relative to the date of **each PDF**. Prior knowledge about versions does not count. The three captures were made on Aug 18, 2026 according to the PDF metadata (not printed on the pages).

## RN (React Native, docs 0.87)
- Version **0.87** (selector, RN p.1) and "Last updated on Aug 12, 2026" (RN p.4). Everything holds for that version/date; do not assert what existed/changed in others.
- The reference to "Native Components", to the Snack Player and to the organization of the docs describes the site in 2026.

## FLT (Flutter docs, landing page)
- **No version or date printed.** The card names (e.g., "Create with AI"), the Google I/O sessions and the "Full-stack developer guide" series are the state of the capture (FLT p.1-3). Do not infer a Flutter version number.

## SWT (A Swift Tour)
- **Swift version not stated**; footer "Copyright 2014-2026" (SWT p.19). Features shown (if/switch as an expression, `any`, actors, task groups) appear in the tour of the capture; **when they appeared** is NOT COVERED.
- Code in image and several boxes truncated (see INDEX §3).

## General gaps (NOT COVERED in the collection)
- **RN:** core components, JSX, hooks, state/props, styles, navigation, Metro/Hermes/new architecture, TypeScript, Expo beyond Snack, project creation, build/release, testing, performance.
- **FLT:** installation, the Dart language (only mentioned), widget list/usage, hot reload, state management, Material/Cupertino, navigation, testing, build/deploy, performance.
- **SWT:** SwiftUI, UIKit, Xcode, SwiftPM, `guard`, `inout`, ARC (`weak`/`unowned`), access control, property wrappers, macros, `Codable`, `Sendable`/`@MainActor`, forced unwrapping, opaque types, associatedtype, Swift version.
- **Comparisons:** performance, market, cost, ecosystem, choice recommendation.
- **Boundary:** React web/Next.js (agent `nextjs-react-expert`); Kotlin/native Android (not covered).

`python -I scripts/mob_lookup.py --gaps` lists the verifiable gaps.
