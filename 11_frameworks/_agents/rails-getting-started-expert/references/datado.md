# [DATED] - relative to the PDF (Rails 8.1.0+, Ruby 3.2+; publication date not printed)

Everything below holds for **Rails 8.1.x as described in the PDF**. Later or earlier versions: NOT COVERED; the model's prior knowledge does not apply.

| Item | What the PDF says | Page |
|---|---|---|
| Versions | Ruby 3.2+, Rails 8.1.0+; migrations `[8.1]` | 2, 9 |
| Default database | SQLite | 8 |
| Server | Puma (example output: Puma 6.4.3, ruby 3.3.5) | 6 |
| Strong params | `params.expect(product: [ ... ])` | 30 |
| Authentication | `rails generate authentication` generator with bcrypt; field `email_address` | 38-39 |
| Cache | Solid Cache, default | 41 |
| Asset pipeline | Propshaft | 60 |
| JavaScript | import maps + Hotwire | 62-63 |
| Jobs | `:async` in dev; Solid Queue in production (`SOLID_QUEUE_IN_PUMA: true`) | 70 |
| Deploy | Kamal + Thruster + Docker Hub + LetsEncrypt | 68-69 |
| CI | `.github` with rubocop, brakeman and tests | 68 |
| Rich text form | `form.rich_textarea` | 43 |
| Tokens | `generates_token_for` / `find_by_token_for` | 58-59 |
| Example output | 2024 timestamps; API link v8.1.3.1 | 8, 12, 51 |
| Cross-references | external guides (routing, i18n, security etc.) cited by name; their content is not in the PDF | various |

Usage rules: (a) if the user brings a different version, say the PDF only covers 8.1.x and label the rest as `[extrapolation]`; (b) do not state what "changed" between versions: the PDF carries no change map.
