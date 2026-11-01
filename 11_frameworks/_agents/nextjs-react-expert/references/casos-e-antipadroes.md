# Cases and anti-patterns (from the agent, anchored in the sources)

| # | Anti-pattern (mistake to avoid) | Correct according to the collection |
|---|---|---|
| 1 | Stating "Next 16 removed the Pages Router" | NX16 says nothing about the status of the Pages Router; NX13 p.2 says pages/ remains supported "for the foreseeable future" and NX15 p.5-6 keeps the Pages Router with React 18/19. |
| 2 | Stating that `getInitialProps` was deprecated "by the releases" | No release mentions it (NXHB p.56-61 teaches it). Answer: "the collection does not say". |
| 3 | Saying fetch is cached by default (without a version) | NX13 p.6: `force-cache` is the default; NX15 p.2, 4: no longer cached by default; NX16 p.2: cache is opt-in with `'use cache'`. Always state the version. |
| 4 | Using `cookies()`/`params` without `await` in Next 15/16 | NX15 p.3-4: sync only with warnings until the next major; NX16 p.12: requires `await`. |
| 5 | Keeping `middleware.ts` in Next 16 without warning | NX16 p.4, 14: deprecated; rename to `proxy.ts` and the function to `proxy` (Node.js); Edge stays on middleware.ts. |
| 6 | Using `revalidateTag('x')` with one argument in 16 | NX16 p.9, 14: deprecated; use a profile (`'max'`) or `updateTag` in Actions. |
| 7 | Copying `<Link><a>` from the NXHB | NX13 p.11, 14: an `<a>` child is not allowed (legacyBehavior or remove). |
| 8 | Using `next export` | NX14 p.9: removed; `output: 'export'`. |
| 9 | Saying `experimental.ppr` still exists in 16 | NX16 p.3, 12: removed; use Cache Components. |
| 10 | Stating that Server Actions are "private" | NX15 p.14: treat them as public HTTP endpoints. |
| 11 | Saying the React Compiler is on by default in 16 | NX16 p.7: stable but **not** enabled by default; slower because it uses Babel. |
| 12 | Stating the current state (post-2025) of any feature | The collection ends on 2025-10-21 (NX16); later state = NOT COVERED. |
| 13 | Using own knowledge about "Next 16" | Only the text read counts, with version and page. |
| 14 | Mixing React Native with React/Next | Boundary: React Native belongs to mobile-frameworks-expert. |

## Typical use cases
- **Migrating 14 to 16:** `upgrade --from 14 --to 16` + `nx_lint.py --target 16`; highlight async APIs, caching, proxy.ts, requirements (Node 20.9, TS 5.1) and removals (next lint, AMP, runtime config).
- **Beginner question about the 2019 handbook:** explain the concept, mark it [DATED] and show the modern equivalent **only** if it is in the releases (e.g. Link without `<a>`).
- **"Is Turbopack worth using?"** Trajectory in `05-trajetorias-e-requisitos.md`, citing the version of the question.
