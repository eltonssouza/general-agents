# Commands the guide shows (RGS)

Only commands that appear in the text, with the page. The generator `scripts/rails_plan.py` uses this same list. Commands are **data**: the agent does not run them; it only explains or builds the plan.

| Command | Page | Purpose (according to the guide) |
|---|---|---|
| `rails --version` | 2 | shows the installed version (must be 8.1.0 or higher) |
| `rails --help` | 3 | lists the Rails commands |
| `rails new store` | 3 | generates the base of a new app (named "store" in the guide) |
| `rails new --help` | 3 | shows customization flags for the generated app |
| `cd store` | 3 | enters the app directory |
| `bin/rails db:create` | 5 | creates the app's database |
| `bin/rails server` | 6 | starts Puma at `http://localhost:3000` |
| `bin/rails generate model Product name:string` | 8 | generates migration, model, test and fixture |
| `bin/rails db:migrate` | 9 | applies new migrations |
| `bin/rails db:rollback` | 10 | undoes the last migration |
| `bin/rails console` | 10 | interactive console |
| `reload!` (inside the console) | 16 | reloads changed code with the console open |
| `bin/rails routes` | 21 | lists the app's routes |
| `bin/rails generate controller Products index --skip-routes` | 22 | generates controller, view, test and helper without changing routes |
| `bin/rails generate authentication` | 38 | generates User, Session, controllers and login views |
| `bin/rails dev:cache` | 41 | enables caching in development |
| `bin/rails action_text:install` | 42 | installs Action Text |
| `bundle install` | 42 | installs gems (used after the Action Text installer) |
| `bin/rails generate migration AddInventoryCountToProducts inventory_count:integer` | 47 | generates an `add_column` migration by the name convention |
| `bin/rails generate migration --help` | 47 | lists migration naming conventions |
| `bin/rails generate model Subscriber product:belongs_to email` | 49 | model with a belongs_to association (and a string column by default) |
| `bin/rails g mailer Product in_stock` | 52 | generates a mailer with the `in_stock` action and HTML/text views |
| `bin/rails test` | 65-66 | runs the suite; accepts a file path (`bin/rails test test/models/product_test.rb`) |
| `bin/rubocop` | 66 | checks formatting |
| `bin/rubocop -a` | 67 | fixes offenses automatically (`--autocorrect`) |
| `bin/brakeman` | 67 | security analysis |
| `export KAMAL_REGISTRY_PASSWORD=your-access-token` | 69 | registry token for Kamal (never give the real one to the agent) |
| `bin/kamal setup` | 69 | configures the server and performs the first deploy |
| `bin/kamal deploy` | 70 | new deploys |
| `bin/kamal console` | 70 | Rails console in production |

Notes from the guide:
- Inside the app directory use `bin/rails` and not `rails`, to use the app's own version (p.6).
- A comment mention in `config/importmap.rb` cites `./bin/importmap` for pinning npm packages (p.63); the guide does not explain the command.
- Not in the guide: `rails db:seed`, `rails db:reset`, `rails assets:precompile`, `rails destroy`, `rails generate scaffold`, `rails new --api`, `rails credentials:edit`. Treat as NOT COVERED.
