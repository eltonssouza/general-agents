# 10 - Tests, RuboCop, Brakeman and CI (RGS p.64-68)

## Fixtures (RGS p.64)
Generating a model creates a fixtures file in `test/fixtures`, empty by default. Fixtures are predefined data that populate the test database; they are given easy-to-remember names (p.64). Example: `tshirt:` with `name: T-Shirt` and `inventory_count: 15` in `products.yml`; `david:` and `chris:` in `subscribers.yml` with `product: tshirt` (reference by name, without managing ids) (p.64). Inserted automatically when the suite runs (p.64).

## Email test (RGS p.64-65)
`test/models/product_test.rb`: `include ActionMailer::TestHelper`; `products(:tshirt)` (fixture helper); zeroes the inventory and uses `assert_emails 2 do product.update(inventory_count: 99) end` (p.65). The guide explains each step (p.65). `bin/rails test test/models/product_test.rb` runs one file; `bin/rails test` runs everything (p.65-66). The generated mailer test (`ProductMailerTest < ActionMailer::TestCase`) is adjusted with `assert_equal "In stock", mail.subject`, `mail.to`, `mail.from` and `assert_match "Good news!", mail.body.encoded` (p.66). Example output: 2 tests, 7 assertions, 0 failures (p.66). More: "Testing Rails Applications" guide (p.66).

## RuboCop (RGS p.66-67)
A formatting linter that ships with Rails. `bin/rubocop` lists offenses; `bin/rubocop -a` (or `--autocorrect`) fixes them automatically (p.66-67). The `.rubocop.yml` file holds the configuration (p.4).

## Brakeman (RGS p.67)
A gem for checking security problems (vulnerabilities that lead to session hijacking, session fixation, redirects). `bin/brakeman` analyzes the app and emits a report (p.67). More: "Securing Rails Applications" (p.67).

## CI with GitHub Actions (RGS p.68)
The app generates the `.github` folder with a GitHub Actions configuration that runs **rubocop, brakeman and the test suite**; when pushed to a repository with Actions enabled, it runs and reports success/failure of each step (p.68).

## Security present in the guide (summary)
CSRF token from `form_with` (p.29); strong parameters (p.30); password hashing with bcrypt (p.39); unsubscribe tokens with `generates_token_for` (p.58-59); Brakeman (p.67). Other practices: NOT COVERED.

## Limits
NOT COVERED: system tests, controller/integration tests, `fixtures` with ERB, coverage, parallelization (the output merely mentions "parallelization threshold is 50", p.65), RuboCop configuration.
