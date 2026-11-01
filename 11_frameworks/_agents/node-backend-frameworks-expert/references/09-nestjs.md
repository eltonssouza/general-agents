# 09 — NestJS (NEST)

Source: **NEST** — "First steps" page of the NestJS documentation (web capture, 10 pages). Branding: requires **Node.js >= 20** (p.2); footer "Copyright © 2017-2026" (p.7); Nest version **not declared**. **Minimal coverage**: only p.2-6 have content; p.1 (icons), p.7 (sponsors/newsletter) and p.8-10 (empty) do not. Pages = PDF. This agent does **not** cover Nest modules/providers/decorators beyond what is below (NOT COVERED).

## Language and prerequisites (NEST p.2)
- **[from source]** Nest is compatible with **TypeScript** and **plain JavaScript**; for plain JS a **Babel** compiler is required; the examples are mostly in TypeScript, with a button to switch to JS (p.2).
- **[from source]** Prerequisite: **Node.js version >= 20** (p.2). **[DATED]** relative to the capture (2026); check the current docs.

## Creating the project (NEST p.2)
**[from source]** With the Nest CLI: `npm i -g @nestjs/cli` and `nest new project-name`; the CLI creates the folder, installs dependencies and populates `src/` with core files. The `--strict` flag of `nest new` enables TypeScript's strictest set (HINT on p.2).

## Initial files (NEST p.3-4)
- **[from source]** `app.controller.ts` (basic controller with one route), `app.controller.spec.ts` (controller unit tests), `app.module.ts` (**root module**), `app.service.ts` (basic service with one method), `main.ts` (entry file that uses `NestFactory` to create the application instance) (p.3).
- **[from source]** `main.ts`: an `async function bootstrap()` function that does `const app = await NestFactory.create(AppModule)` and `await app.listen(process.env.PORT ?? 3000)`, then calls `bootstrap()` (p.3; code checked visually on the rendered page, because text extraction scrambles the braces).
- **[from source]** `NestFactory` exposes static methods to create the application; `create()` returns an object that fulfills the `INestApplication` interface, whose methods appear in later chapters (p.4). The generated project encourages **keeping each module in its own directory** (p.4). By default, if there is an error creating the application, it exits with code 1; to throw an exception instead: `NestFactory.create(AppModule, { abortOnError: false })` (p.4).

## Platform: Express or Fastify (NEST p.4-5)
- **[from source]** Nest aims to be **platform-agnostic**; technically it works with any Node HTTP framework as long as an adapter exists; two platforms are supported out of the box: **express** and **fastify** (p.4).
- **[from source]** `@nestjs/platform-express` is the **default** package (Express described as minimalist, battle-tested and production-ready) (p.4). Fastify is described as high-performance and low-overhead, focused on efficiency and speed (p.5).
- **[from source]** Each platform exposes its interface: `NestExpressApplication` and `NestFastifyApplication`; when you pass the type to `NestFactory.create<NestExpressApplication>(AppModule)`, the `app` object gains the platform's methods; you only need to provide the type if you want to access the underlying platform API (p.5).

## Running, SWC, lint and formatting (NEST p.5-6)
- **[from source]** `npm run start` starts the app on the port defined in `src/main.ts`; open `http://localhost:3000/` to see "Hello World!" (p.5). `npm run start:dev` watches for changes, recompiles and reloads (p.5-6).
- **[from source]** **SWC** builder: `npm run start -- -b swc` — the text claims builds "20 times faster" (HINT, p.5); a claim of the docs, without a benchmark.
- **[from source]** The project already ships with **eslint** and **prettier** (base packages); scripts `npm run lint` (with autofix) and `npm run format`, designed for CI and git hooks (p.6).

## What is NOT in this PDF (NOT COVERED)
Decorators (`@Module`, `@Controller`, `@Injectable`, `@Get`...), dependency injection, providers, middleware, pipes, guards, interceptors, DTOs/validation, configuration, testing beyond the `.spec` file, microservices, GraphQL, databases. The page mentions "80+ chapters" of official courses (p.4) — advertising, no technical content.

Related: `08-fastify.md`, `07-express.md`, `10-comparativo-express-fastify-nest.md`. Linter: NEST-NODE-VERSION.
