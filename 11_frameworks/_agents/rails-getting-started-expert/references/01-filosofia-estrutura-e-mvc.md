# 01 - Philosophy, directory structure and MVC (RGS p.1-5, 71-72)

## Scope of the guide (RGS p.1)
The guide promises to teach: installing Rails, creating an app and connecting it to a database; the general layout of a Rails app; the principles of MVC and RESTful design; quickly generating the initial pieces; and deploying with Kamal [from source] (RGS p.1). It does not require prior Rails experience, but recommends learning the basics of Ruby (p.1) [from source].

## Philosophy (RGS p.2)
- Rails is a web framework written in Ruby, which makes assumptions about what every developer needs to get started [from source] (RGS p.1).
- It is "opinionated": it assumes there is a "best" way of doing things and encourages it; bringing habits from other languages may make the experience less happy [from source] (RGS p.2).
- Two principles: **DRY** (every piece of knowledge must have a single representation) and **Convention over Configuration** (Rails adopts defaults instead of requiring extensive configuration) [from source] (RGS p.2).

## Directory structure of a new app (RGS p.3-4)
| Item | Purpose according to the guide |
|---|---|
| `app/` | controllers, models, views, helpers, mailers, jobs and assets; where most of the work happens |
| `bin/` | `rails` script and other setup/update/deploy scripts |
| `config/` | routes, database and more |
| `config.ru` | Rack configuration |
| `db/` | current schema and migrations |
| `Dockerfile` | Docker configuration |
| `Gemfile`, `Gemfile.lock` | gem dependencies, used by Bundler |
| `lib/` | extended modules for the app |
| `log/` | logs |
| `public/` | static files and compiled assets, served as they are |
| `Rakefile` | locates tasks; add your own tasks in `lib/tasks` instead of editing the Rakefile |
| `README.md` | the app's manual |
| `script/` | one-off scripts and benchmarks |
| `storage/` | SQLite databases and Active Storage files (Disk service) |
| `test/` | tests, fixtures |
| `tmp/` | cache, pid |
| `vendor/` | third-party code |
| `.dockerignore`, `.gitattributes`, `.git/`, `.github/`, `.gitignore`, `.kamal/`, `.rubocop.yml`, `ruby-version` | supporting files (Docker, Git, GitHub, Kamal secrets/hooks, RuboCop, Ruby version) |
[from source] (RGS p.3-4)

## MVC (RGS p.5)
- **Model**: manages the app's data, typically database tables.
- **View**: renders responses in formats such as HTML, JSON, XML.
- **Controller**: handles user interactions and the logic of each request.
[from source] (RGS p.5)

## End of the guide (RGS p.71-72)
Suggested next step: the "Sign Up and Settings" tutorial; further reading: Active Record Basics, Layouts and Rendering, Testing, Debugging, Securing Rails Applications (p.71). The guide accepts contributions and points to the Edge Guides to check whether a problem has already been fixed in `main` (p.72). License CC BY-SA 4.0 (p.72).

## Limits
The guide does not explain the Rack layer, the middleware cycle or the contents of each file in `config/` (it points to the guide "Configuring Rails Applications", p.3). Going deeper: NOT COVERED.
