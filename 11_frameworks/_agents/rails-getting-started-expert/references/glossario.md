# Glossary (terms as the guide uses them)

| Term | Definition according to the guide | Page |
|---|---|---|
| DRY | every piece of knowledge must have a single representation | 2 |
| Convention over Configuration | Rails defaults instead of lengthy configuration | 2 |
| MVC | Model (data), View (rendering), Controller (interaction and logic) | 5 |
| Active Record | maps relational databases to Ruby and generates SQL | 8 |
| Migration | a set of database changes, trackable and deployable | 8 |
| `ApplicationRecord` | base class of models (`Product < ApplicationRecord`) | 11 |
| Relation | Array-like collection returned by `all`/`where`/`order` | 13 |
| Validation | data rule checked on create/update/save | 16-17 |
| Route | line that pairs an HTTP method and path to a controller#action | 18 |
| Route parameter | captured piece of the URL, such as `:id` | 19 |
| `resources` | shortcut for the CRUD routes | 21 |
| Prefix | name of the route helper in the output of `rails routes` | 26 |
| Action | public method of the controller | 17, 23 |
| Instance variable | `@x`, shares data from the controller with the view | 24 |
| ERB | Ruby embedded in HTML: `<%= %>` prints, `<% %>` does not | 24-25 |
| `params` | request parameters | 26 |
| `form_with` | form helper; handles CSRF, URL and button | 29 |
| Strong parameters | parameter filter with `params.expect` | 30 |
| Partial | reusable view, name starts with `_` | 33 |
| `before_action` | shared code that runs before actions | 34 |
| Layout | HTML common to all pages (`application.html.erb`) | 39 |
| Flash | temporary data between actions (`notice`, `alert`) | 51 |
| Solid Cache | database-backed cache store, default | 41 |
| Action Text | rich text with embeds | 42 |
| Active Storage | file uploads | 44 |
| I18n | translation; `t` looks up a key by locale | 45 |
| Action Mailer | sending email | 52 |
| Callback | lifecycle hook, such as `after_update_commit` | 56 |
| Concern | module with syntactic sugar (`ActiveSupport::Concern`) | 57 |
| `generates_token_for` | generates unique tokens for locating records | 58 |
| Propshaft | asset pipeline | 60 |
| Import map | JavaScript in modules without a build | 62 |
| Hotwire | Turbo + Stimulus + Native | 63 |
| Fixture | named test data | 64 |
| RuboCop | formatting linter | 66 |
| Brakeman | static security analysis | 67 |
| Kamal | deploy with Docker, zero downtime | 68 |
| Thruster | compresses and serves assets in the production image | 68 |
| Solid Queue | database-backed job queue, production | 70 |
