# INDEX - rails-getting-started-expert

Agent for a **single-source overview**: the official guide "Getting Started with Rails" captured from the website (acronym **RGS**). It is not a complete Rails reference agent: what the guide does not say is **NOT COVERED** or, if the user asks, a labeled `[extrapolation]`.

## 1. Source, version, date and page convention

| Item | Value (read from the PDF) |
|---|---|
| File | `14_frameworks/Rails-Getting-Started-Guide.pdf`, 72 pages, ~96 thousand characters of text |
| What it is | Official Ruby on Rails guide ("More Ruby on Rails" section, RGS p.1) that builds the **"store"** app (a simple e-commerce) step by step and ends with a Kamal deploy |
| **Rails version** | **Rails 8.1.0 or newer** is the prerequisite (RGS p.2); example outputs show "Rails 8.1.0" (p.2, 6, 10); migrations use `ActiveRecord::Migration[8.1]` (p.9, 48, 49); an API link points to `v8.1.3.1` (p.51) |
| Ruby | Ruby **3.2 or newer** (p.2). The Puma example output mentions Puma 6.4.3 and ruby 3.3.5 (p.6) |
| **Date** | **Not printed.** Timestamps in the example outputs are from 2024 (p.8, 12, 15) and the API link v8.1.3.1 indicates later publication; the capture date must be read from the file metadata. Everything is [DATED] relative to **Rails 8.1.x** |
| License | Creative Commons Attribution-ShareAlike 4.0 (p.72); "Rails" is a registered trademark of David Heinemeier Hansson |
| **Page convention** | **PDF page = printed "Page N of 72"** (marker `=== PAGE N ===`). p.1 has no "Page 1 of 72" header, but the numbering matches; **no offset**. All `RGS p.N` citations follow this convention |
| Capture quality | All 72 pages have useful content; none is 404/"Page not found". Images (the Rails welcome page, browser screenshots) do not come through in the text; the text describes what they show. Code snippets appear whole in the extracted text. A few lines of text appear cut off in the directory table (p.4: the description of `.gitattributes` and a link for `script/`); the tutorial code is complete |

Important: the original task mentions the tutorial's "blog", but the guide builds the **"store"**. The word "blog" appears only as a route example `/blog/:title` (p.20). The package checklist covers the **store**.

The model's prior knowledge about Rails versions **does not apply**: everything about 8.1 comes only from the text.

## 2. Map topic -> pages -> file

| Topic | RGS pages | File |
|---|---|---|
| Introduction, philosophy (DRY, convention over configuration), directory structure, MVC | 1-5 | 01-filosofia-estrutura-e-mvc.md |
| Prerequisites, `rails new`, `bin/rails`, server, autoload/reload | 2-3, 5-7 | 02-criando-o-app-e-servidor.md |
| Model, migration, console, Active Record CRUD, validations | 8-17 | 03-active-record-e-console.md |
| Routes, `resources`, `rails routes`, URL helpers | 17-22, 26-27 | 04-rotas.md |
| Controllers, actions, ERB views, params, `form_with`, strong params, partials, `before_action`, destroy | 22-39 | 05-controllers-views-e-formularios.md |
| Authentication generator | 38-41 | 06-autenticacao.md |
| Fragment cache, Action Text, Active Storage, I18n | 41-47 | 07-cache-rich-text-storage-i18n.md |
| Inventory, associations, flash, nested routes, Action Mailer, callbacks, concern, tokens | 47-60 | 08-associacoes-mailer-e-concerns.md |
| Propshaft, import maps, Hotwire | 60-63 | 09-assets-javascript-e-hotwire.md |
| Tests, RuboCop, Brakeman, CI | 64-68 | 10-testes-qualidade-seguranca-ci.md |
| Kamal deploy, production user, Solid Queue | 68-70 | 11-deploy-kamal-e-solid-queue.md |
| Next steps, feedback, license | 71-72 | 01 (note) |
| Commands the guide shows | all | comandos-do-guia.md |
| Tutorial checklist (store) | all | checklist-store.md |
| Terms, procedures, cases, dated items | all | glossario.md, procedimentos.md, casos-e-antipadroes.md, datado.md |

## 3. Coverage per task request (honest)

Covered by the guide (tutorial level): convention over configuration, app generation, MVC, routes (`get`, `post`, `root`, `resources`, `resource`, nested), controllers, ERB views, models/Active Record, migrations (`create_table`, `add_column`), validations (`presence`, `numericality`), associations (`belongs_to`, `has_many`, `has_one_attached`, `has_rich_text`), forms (`form_with`), partials.

NOT COVERED in the guide: `has_many :through`, polymorphic associations, `scope`, validations beyond presence/numericality, advanced routes (`namespace`, `member`/`collection`, constraints), API-only/JSON Rails, any database other than SQLite, Action Cable, Active Job beyond its use by `deliver_later`, security beyond CSRF/strong params/Brakeman. Use `python -I scripts/rails_lookup.py --gaps`.

## 4. Boundaries

- Ruby language (syntax, modules, blocks, `%i[]`, safe navigation): agent **ruby-expert** (`01_programming_languages/_agents/`). This agent only explains what the guide says about Rails.
- Databases (SQL, SQLite/PostgreSQL, modeling): database agents. The guide uses SQLite by default (p.8).
- Docker, servers, DNS, CI/CD in depth: devops agents. The guide only shows the Kamal flow (p.68-70).
