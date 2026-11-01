# Reference index — web-api-rest-architecture-expert

## Single source

- **[APIGEE]** *Web API Design: The Missing Link — Best Practices for Crafting Interfaces that Developers Love*. Apigee / Google LLC, © 2018 (APIGEE p.1, p.65). 65-page e-book, no named author. File: `06_web_and_frontend/Web-API-Design-Apigee.pdf`.

**Note on the identity of the work.** This is not the earlier Apigee e-book (*Web API Design: Crafting Interfaces that Developers Love*, Brian Mulloy, 2012). The 2018 text presents itself as an evolution of "our previous book" (APIGEE p.5) and cites Mulloy only as the author of a 2011 webinar in the resources list (APIGEE p.61). Well-known recommendations from the 2012 book (mandatory `/v1` version, `?q=` for search, verbs for calculations, the 400/404/500 status table, `suppress_response_codes`, the `api.` subdomain) **are not in this source** and cannot be cited as [from source].

## Conventions

- **Page = PDF marker** (`[PDF p.N]` of the extracted text). In this PDF the printed table of contents matches the marker (e.g. "Designing URLs … 26" is on PDF p.26).
- Labels: **[from source]** with page; **[inference]** for a deduction from the text; **[extrapolation]** for general knowledge of HTTP/RFCs that the source does not provide; **[DATED]** for period examples (Twitter, LinkedIn, Google Drive v2 APIs from ~2015–2018).
- The book's JSON examples use the fictional domain `dogtracker.com` (dogs and owners).

## Map

| File | Topic | Pages |
|---|---|---|
| [paradigmas-rest-e-design-orientado-a-dados.md](paradigmas-rest-e-design-orientado-a-dados.md) | REST vs RESTful, HTTP only, coupling, data-oriented model vs functions, uniform interface | p.5–12, p.60 |
| [design-de-representacoes-json-e-metadados.md](design-de-representacoes-json-e-metadados.md) | simple JSON, links, `self`/`kind`, collections, formats, PATCH, property names, dates | p.13–25, p.40–48 |
| [design-de-urls-substantivos-e-pluralizacao.md](design-de-urls-substantivos-e-pluralizacao.md) | nouns vs verbs, well-known URLs, entity URLs, permalinks, type stability | p.26–28, p.32 |
| [a-web-e-plana-e-limites-de-aninhamento.md](a-web-e-plana-e-limites-de-aninhamento.md) | "the web is flat", the renaming dilemma, aliases and redirects | p.28–31 |
| [relacionamentos-e-simetria-em-subrecursos.md](relacionamentos-e-simetria-em-subrecursos.md) | links vs URI templates, query URLs by relationship, symmetry, general model | p.15–21, p.33–35 |
| [filtragem-ordenacao-e-busca-em-colecoes.md](filtragem-ordenacao-e-busca-em-colecoes.md) | query URLs, matrix parameters, filters, non-persistent responses | p.18–19, p.32–39 |
| [paginacao-e-respostas-parciais-contra-chatty-apis.md](paginacao-e-respostas-parciais-contra-chatty-apis.md) | the chatty-API myth, pagination, `fields` | p.43–45, p.48–50 |
| [mapeamento-de-codigos-de-status-http.md](mapeamento-de-codigos-de-status-http.md) | status + headers the source shows (200, 201, 303, 401, 405) and what it does not cover | p.7, p.43, p.51–52 |
| [tratamento-de-erros-e-padronizacao-de-payloads.md](tratamento-de-erros-e-padronizacao-de-payloads.md) | why errors matter, messages for people | p.51–53 |
| [modelagem-de-acoes-nao-crud.md](modelagem-de-acoes-nao-crud.md) | actions (start/stop/pause), calculations without a verb | p.37–39, p.53–54 |
| [autenticacao-e-governanca-de-seguranca.md](autenticacao-e-governanca-de-seguranca.md) | OAuth 2.0, SDK; security gaps | p.55 |
| [estrategias-de-versionamento-de-apis.md](estrategias-de-versionamento-de-apis.md) | not versioning, version in URL vs header, links | p.46, p.56–59 |
| [casos-e-antipadroes.md](casos-e-antipadroes.md) | anti-patterns the source condemns, with fixes | various |
| [procedimentos.md](procedimentos.md) | design and review checklists | various |
| [glossario.md](glossario.md) | terms | various |

## What the source does not cover

Status 204, 400, 403, 404, 409, 422, 429, 5xx; rate limiting; API keys; CORS; OpenAPI/Swagger; idempotency; cursor pagination; sorting (`sort`); full-text search; GraphQL; gRPC; webhooks; OAuth flows (PKCE, client credentials). Answer with [extrapolation] and no page, or say that the source does not address it.
