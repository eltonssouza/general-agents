# 03 — NOT COVERED (topics that no Overview mentions)

Verified by text search over the 38 pages (`python -I scripts/ng_lookup.py --gaps`; the list is checked in `tests/citation-checks.json` through negative checks). For these topics the agent answers **NOT COVERED**; it gives an `[extrapolation]` only if asked, without attributing it to the captures and without asserting anything about versions 21 and 22 (unknown to the model).

- **Standalone** components / NgModule.
- **Zoneless**, zone.js, change detection.
- **Control flow** in templates (`@if`, `@for`, `@switch`) and the old structural directives.
- `computed`, `effect`, `linkedSignal`, `resource`/`httpResource`, **Signal Forms**.
- Incremental hydration, event replay.
- Angular Material/CDK as a library (the Overview only cites "Material Design" among partnerships).
- Animations, testing (Jasmine, Karma, Jest, Vitest), TypeScript, RxJS, `inject()`.
- CLI commands other than `ng update` (`ng new`, `ng serve`, `ng build`, `ng generate`), `ng update` arguments.
- AI/MCP, webpack, PWA/service workers, Angular Elements, AOT/Ivy.
- Release dates and numbers, exact LTS policy, compatibility matrix.
- Any API, signature, code example or configuration (`angular.json`, `tsconfig`).

Outside the boundary (other agents): React, Vue, Svelte and other frameworks; backends.

How to answer: "NOT COVERED in the NG18-NG22 Overviews (overview based on a documentation capture). [extrapolation] optional: ..." and recommend checking the official documentation for the user's version.
