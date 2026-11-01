# 01 — Concepts by topic (with pages per version)

Format: concept — what the Overview says (paraphrase) — pages. "≈" indicates different wording between versions (see `02-mapa-de-diferencas.md`). Generated/checked with `python -I scripts/ng_diff.py matrix`.

## Features that drive development
- **Components** — split the code into well-encapsulated pieces. NG18 p.1; NG19 p.3; NG20 p.2; NG21 p.2; NG22 p.2. In NG18-NG20 the headline speaks of an "opinionated component model and flexible DI system" (NG18 p.1; NG19 p.2; NG20 p.2).
- **Dependency injection (DI)** — NG18-NG20: keeps code modular, decoupled and testable (NG18 p.1; NG19 p.3; NG20 p.2). NG21/NG22: "Dependency injection" card, sharing code between components across the whole application (NG21 p.3; NG22 p.3).
- **Signals / fine-grained reactivity** — a model with compile-time optimizations; it tracks where and how state is used, enabling fast updates with optimized instructions. NG18 p.1; NG19 p.2-3; NG20 p.2; NG21 p.2; NG22 p.2. (The detailed description of the tracking is in NG18 p.1, NG19 p.3, NG20 p.2; NG21/NG22 carry only the short description on the "Angular Signals" card.)
- **SSR, SSG and full DOM hydration** — NG18 p.2; NG19 p.3; NG20 p.2; NG21 p.3 ("Server-side rendering" card); NG22 p.3.
- **Deferred loading / `@defer` blocks** — "next-generation deferred loading"; blocks in templates declaratively split the template into pieces that load on demand. **Only NG18 p.2, NG19 p.3, NG20 p.2**; it does not appear in NG21 or NG22.
- **Router** — navigation kit with route guards, data resolution, lazy-loading. NG18 p.2; NG19 p.3; NG20 p.2; NG21 p.3 ("Angular Routing"); NG22 p.3.
- **Forms** — standardized system for form participation and validation. NG18 p.2; NG19 p.3; NG20 p.2; NG21 p.3 ("Forms in Angular"); NG22 p.3. In NG18-NG20 router and forms are presented together under "official modules for forms, routing and more".

## Develop faster
- **Angular CLI** — a project running in under a minute, with the commands to grow it to production. NG18 p.2; NG19 p.3; NG20 p.3; NG21 p.3-4; NG22 p.3-4. (No specific command is listed, except `ng update`.)
- **Angular DevTools** — extension alongside the browser tools: component tree inspector, DI tree view and performance flame chart. NG18 p.2; NG19 p.3-4; NG20 p.3; NG21 p.3-4; NG22 p.3-4. The expression "browser extension" appears only in NG18-NG20.
- **`ng update`** — runs automatic code transformations for routine breaking changes, simplifying major-version updates; staying up to date keeps the app fast and secure. NG18 p.2-3; NG19 p.4; NG20 p.3; NG21 p.4; NG22 p.4.
- **Language service (IDE)** — code completion, navigation, refactoring and real-time diagnostics. NG18 p.3; NG19 p.4; NG20 p.3; NG21 p.4; NG22 p.4.

## Ship with confidence
- **Commit-by-commit verification in Google's monorepo** — hundreds of thousands of internal tests. NG18 p.3; NG19 p.4; NG20 p.3; NG21 p.4-5; NG22 p.4-5.
- **Stability and compatibility** — commitment to large Google products (including Google Cloud); changes are tested and backward compatible, with migration tools where possible. NG18 p.3; NG19 p.4; NG20 p.3-4 (broken sentence); NG21 p.5; NG22 p.5.
- **Support policy and release schedule** — predictable time-based schedule; LTS windows for critical security fixes; official migration tools, guides and schematics. NG18 p.3; NG19 p.4; NG20 p.3; NG21 p.5; NG22 p.5. **No capture gives dates, LTS durations or release version numbers.**

## Works at any scale
- **Internationalization** — message translation and formatting, with ICU syntax (Unicode standard). NG18 p.4; NG19 p.5; NG20 p.4; NG21 p.5; NG22 p.5.
- **Security by default** — in collaboration with Google security engineers; HTML sanitization and trusted types support, against XSS and CSRF. NG18 p.4; NG19 p.5; NG20 p.4; NG21 p.5-6; NG22 p.5-6. The text does not describe security APIs.
- **Build with Vite and esbuild** — fast pipeline; reports of projects with hundreds of thousands of lines built in under a minute. NG18 p.4; NG19 p.5; NG20 p.4; NG21 p.6; NG22 p.6.
- **Proven in large Google apps** — Google Fonts and Google Cloud as examples. NG18 p.4; NG19 p.5; NG20 p.4; NG21 p.6; NG22 p.6.

## Open source and community
- **Open development on GitHub; public roadmap and RFCs** — NG18 p.4; NG19 p.5; NG20 p.5; NG21 p.6; NG22 p.6.
- **Community** — courses/blogs (Google for Developers library, DevLibrary), open source collaboration, GDEs and company partnerships. NG18 p.5-6; NG19 p.6-7; NG20 p.5-6; NG21 p.7-8; NG22 p.7-8.
- **Partnerships** — Chrome's Aurora: optimizations such as NgOptimizedImage and Core Web Vitals improvements; work with Firebase, TensorFlow, Flutter, Material Design and Google Cloud. NG18 p.5; NG19 p.6; NG20 p.5-6; NG21 p.7-8; NG22 p.7-8. NgOptimizedImage is only cited by name: **no explanation of use**.

## Footer and navigation (meta)
- Networks/links: Blog, X, YouTube, Discord, GitHub, Stack Overflow, Community, Contribute, Code of Conduct, Report Issues, DevLibrary, GDEs, Press Kit, Roadmap; **Bluesky** from NG19 p.7 (NG20 p.6; NG21 p.8; NG22 p.8). Languages: see `02-mapa-de-diferencas.md`.
