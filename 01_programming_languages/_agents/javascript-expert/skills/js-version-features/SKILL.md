---
name: js-version-features
description: Answers "in which JavaScript/ECMAScript version did X enter?", "is this legacy (Annex B)?", "is this the language or the [HOST] environment?" and compares Eloquent JS 1st edition [DATED] with the modern one (EJpt / Spec ES2026), stating "version not stated in the sources" whenever the Spec and the books do not give the entry edition. Use when the user asks the version of a JS feature, differences between ES5/ES2015/ES2026, incompatibilities in Annexes E and F, whether a feature belongs to Annex B or to the host, or how to modernize EJ1-era code. Do not use to locate the detailed algorithm in the Spec (use js-spec-lookup) nor for general code review (use js-code-review).
---

# Versions, epoch, Annex B and the `[HOST]` boundary in JavaScript

Full table in `../../references/versoes-e-datado.md`.
**Fundamental rule:** the ECMA-262 Spec (17th edition, ES2026) describes the current state of the language and **almost never states in which edition each feature appeared** (apart from occasional notes and Annexes E and F, Spec p.865–869). EJpt declares it uses "the 2024 version of JavaScript" (EJpt p.9) and dates only `class`, `Symbol`, arrow functions and ES modules to 2015 (and `var`/CommonJS as pre-2015). **Being in the 2026 Spec only proves that the feature exists in ES2026 (Spec p.25).**

## Procedure

1. **Query the version script** (read-only, no network):
   ```bash
   python -I scripts/js_version_lookup.py groupBy
   python -I scripts/js_version_lookup.py class
   python -I scripts/js_version_lookup.py substr
   python -I scripts/js_version_lookup.py --category dated
   python -I scripts/js_version_lookup.py --category annex-b
   python -I scripts/js_version_lookup.py --category host
   python -I scripts/js_version_lookup.py --summary
   ```
2. **If the feature is in the `dated` category (dated by the sources):** give the exact edition/year and cite the source and page (`Spec p.N`, `EJpt p.N`, `EJ1 p.N`), marking it **[VERSION-DEPENDENT]**.
3. **If the feature is in the `unversioned` category (present in the 2026 Spec / EJpt without a date):** you must answer **"version not stated in the sources"** and give the page where the 2026 Spec or EJpt defines it. **Never** fill it in with "entered in ES2020/ES2022/ES2024" as if it came from the sources; if you add the edition from your external knowledge, explicitly label it **[extrapolation]** and keep it separate from what the sources say.
4. **If the feature is in the `annex-b` category (legacy):** state that it belongs to Annex B (or is marked `Legacy` / `Normative Optional` in the Spec), mandatory only in browsers, discouraged in new code and often disabled in strict mode or `Module` (Spec p.446, p.843–859) — mark it **[DATED] [HOST]** and indicate the modern alternative from the sources.
5. **If the feature is in the `host` category:** clarify that it is **not part of the ECMAScript language** (Spec p.26–28, Annex D p.863–864), but of the host environment (browser or Node.js) — mark it **[HOST]**.
6. **If the feature appears in none of the sources** (e.g. `Temporal`, `structuredClone`, `queueMicrotask`, `AbortController`, TypeScript): state that it does not appear in the three sources and label any external explanation **[extrapolation]**.

## Summary of what the sources actually date

- **Historical overview (EJpt p.9; EJ1 p.6):** ES3 supported from ~2000 to 2010; version 4 abandoned in 2008; version 5 came out in 2009 (EJ1 p.6 confirms that ES5 was already out when the 1st ed. was revised); version 6 came out in 2015 and, since then, there have been small yearly updates; EJpt uses the 2024 version; the Spec is the 17th edition, ES2026 (Spec p.25).
- **Dated to 2015 / ES2015:** `class` (Spec p.29; EJpt p.132), `Symbol` (EJpt p.141), arrow functions `=>` (EJpt p.56), ES modules `import`/`export` (EJpt p.221), `let`/`const` and the ASI change with `let` (Spec p.867; EJpt p.31–32, p.52–53), `var` and CommonJS/IIFE as pre-2015 **[DATED]** (EJpt p.31–32, p.225–226), Annex E corrections (Spec p.865) and Annex F incompatibilities marked ES2015 (Spec p.867–869, including `Object.freeze`/`keys`/`isFrozen` accepting primitives, `Number("0b...")`/`Number("0o...")` and `RegExp` flags on the prototype).
- **Dated to ES2016 / ES2017 / ES2018 / ES2019 (Spec p.222, p.867–869):** Unicode 8.0.0 and `U+180E` ceasing to be whitespace in `trim` (ES2016, Spec p.867); requirement of the latest Unicode version, removal of `arguments.caller` and permission of an initializer in `for (var x = ... in ...)` in non-strict mode (ES2017, Spec p.222, p.867–868); canonicalization of template objects by Parse Node (ES2018, Spec p.867); renaming of `Atomics.wake` to `Atomics.notify` and reduction of the number of Jobs enqueued by `await` (ES2019, Spec p.869).
- **Old editions in the Spec:** double `valueOf` in `ArraySetLength` since the 2nd edition (Spec p.219); passing `thisArg` without coercion in `apply`/`call` relative to Edition 3 (Spec p.473).

## Response format

1. **Direct classification:** edition stated by the source (**[VERSION-DEPENDENT]**), **"version not stated in the sources"** (with the page where the feature is defined in the 2026 Spec/EJpt), legacy (**[DATED]**) or environment (**[HOST]**).
2. **What each source says** (`Spec p.N`, `EJpt p.N`, `EJ1 p.N`).
3. **Practical implication** for the user's code (e.g. difference in strict mode/`Module`, modern alternative).
