# 02 — CommonJS modules, npm, package.json, semver, lockfile, npx

Source: NODEHB (6/9/2018; npm 5.x; Node 10). **[DATED]**: npm commands, flags and behavior have changed since 2018; use the current documentation. Pages = PDF.

## module.exports and exports (NODEHB p.40-43)
- **[from source]** A Node file can import what others expose: `const library = require('./library')` (p.40). Everything that is not exported is private (p.41).
- **[from source]** Two ways: assign an object/function to `module.exports` (the file exports only that), or add properties to `exports` (`exports.car = ...`) to export several items (p.41-42).
- **[from source]** Difference: `module.exports` exposes the object it points to; `exports` exposes the **properties** of the object it points to (p.43).

## npm: basics (NODEHB p.43-46)
- **[from source]** npm = node package manager; "more than 350,000 packages in January 2017" (p.43); the registry had "almost 500,000" (p.3). **[DATED]**.
- **[from source]** `npm install` installs everything from `package.json` into `node_modules`; `npm install <package>` installs one; `--save` adds to `dependencies`, `--save-dev` to `devDependencies` (dev = tools such as test libraries; dependencies ship with the app in production) (p.43-44). Another point in the text: since npm 5 the default already writes to `dependencies` without `--save` (p.82).
- **[from source]** `npm update` and `npm update <package>` respect the version constraints (p.44-45).
- **[from source]** Tasks: `npm run <name>` with the `scripts` section of `package.json` (p.45-46). Note: the example on p.46 writes `$ npm watch` / `npm dev` / `npm prod` **without `run`** — an error in the text (see `casos-e-antipadroes.md`).
- **[from source]** Local vs global: a local install goes to the project's `node_modules` and adds to `dependencies`; global uses `-g`, and `npm root -g` shows the folder (p.46-48). With nvm the global path changes (p.48).
- **[from source]** In code, a local or global package is loaded with `require('name')` (p.48, p.80). Executables live in `node_modules/.bin/`; `npx` (npm >= 5.2) locates them (p.48-49).

## package.json (NODEHB p.49-63)
- **[from source]** It is the project manifest and a repository for tool configuration; for an application there are no required fields, it just needs to be valid JSON; for a package distributed on npm, a set of properties is required (p.50).
- **[from source]** Fields explained: `name` (fewer than 214 characters, no spaces, only lowercase letters, hyphens or underscores; becomes the URL on npm) (p.54); `author` and `contributors` (string or object) (p.54-55); `bugs`, `homepage` (p.56); `version` (semver x.y.z) (p.56-57); `license`, `keywords`, `description` (p.57-58); `repository` (shortcuts github:/gitlab:/bitbucket: or type/url object) (p.58-59); `main` (entry point) (p.59); `private: true` prevents accidental publishing (p.60); `scripts` (p.60-61); `dependencies`, `devDependencies` (p.61-62); `engines` (Node/npm/yarn versions) (p.62); `browserslist` (target browsers for Babel/Autoprefixer) (p.62-63); tool-specific fields (`eslintConfig`, `babel`) (p.63).

## Version ranges (NODEHB p.63-64, p.76-78)
- **[from source]** `^0.13.0` accepts patch and minor (0.13.1, 0.14.0); `~0.13.0` only patch (0.13.1 yes, 0.14.0 no); `*` accepts everything, including major; `>`, `>=`, `<`, `<=`; no symbol = exact version; `latest`; ranges (`2.1.0 - 2.6.2`) and unions (`||`) (p.63-64, p.77-78).
- **[from source]** Semver: major = incompatible change; minor = compatible functionality; patch = compatible fix (p.76).
- Note on the text: the list on p.77 repeats `<` where `>` should be (typographical error in the capture).

## package-lock.json (NODEHB p.64-69)
- **[from source]** Introduced in **npm 5**; records the exact version of each installed package so the product is **100% reproducible**, even if maintainers publish new versions (p.65). Solves the problem of `~`/`^` installing different versions on different machines (p.65-66).
- **[from source]** It must be **committed** to Git; `node_modules` is not committed (p.65-66). Updated by `npm update` (p.66). Each entry has `version`, `resolved` and `integrity` (p.66-69). The example shows `lockfileVersion: 1` **[DATED]**.

## Querying and choosing versions (NODEHB p.69-72)
`npm list` (tree), `npm list -g`, `npm list --depth=0`, `npm list <package>`; `npm view <package> version` and `npm view <package> versions`; installing a specific version: `npm install <package>@<version>` (also global).

## Updating (NODEHB p.72-75)
`npm outdated` lists what is new; `npm update` updates within the range and writes the lockfile, **without changing package.json**; **major is never updated** by `npm update`; for a major, the text uses `npm install -g npm-check-updates` and `ncu -u`, then `npm update` (or `npm install` if there is no `node_modules`).

## Uninstalling and global vs local (NODEHB p.78-82)
- **[from source]** `npm uninstall <package>` (`-D` if dev; `-g` if global) (p.78-79).
- **[from source]** The author's rule: install **locally** in general (each app with its own version); global only for packages that provide a **shell executable** reused across projects (p.80-81); examples cited: create-react-app, vue-cli, grunt-cli, mocha, react-native-cli, gatsby-cli, forever, nodemon (p.81).
- **[from source]** In production, `npm install` also installs the devDependencies (it assumes a development deploy); to avoid that, `--production` (p.82).

## npx (NODEHB p.82-85)
**[from source]** Available since npm 5.2 (Jul/2017): runs commands from the project's `node_modules` without a path; runs without installing (`npx cowsay "Hello"`, `npx create-react-app ...`), with `@version`; runs Node versions (`npx node@6 -v`) and **code from a URL** (gist), with the warning to be careful with code you do not control (p.85).

Related: `casos-e-antipadroes.md`, `datado.md`. Linter: NODE-PKG-* and NODE-GITIGNORE-* rules in `scripts/nbf_lint.py`.
