# Procedures (step by step according to the guide)

Pages = RGS. Code snippets are from the guide; paraphrased here.

## P1. Create the app and start the server (p.2-7)
1. `rails --version` (>= 8.1.0). 2. `rails new store`; `cd store`. 3. `bin/rails db:create`. 4. `bin/rails server`; open `localhost:3000`.

## P2. Add a "products" CRUD resource (p.8-38)
1. `bin/rails generate model Product name:string`; `bin/rails db:migrate` (p.8-9).
2. `validates :name, presence: true` in the model (p.16).
3. `resources :products` and `root "products#index"` in `config/routes.rb` (p.21, 23).
4. `bin/rails generate controller Products index --skip-routes` (p.22) and implement the actions; `before_action :set_product`; `product_params` with `params.expect` (p.30, 34-37).
5. Views index/show/new/edit; partial `_form` with `form_with model: product` and `render "form", product: @product` (p.23-34).
6. On validation failure, `render :new`/`:edit` with `status: :unprocessable_entity` (p.30-32).
7. Delete button with `button_to ... method: :delete` (p.38).

## P3. Add a column (p.47-48)
`bin/rails generate migration AddXToYs column:type` (convention `add_<columns>_to_<table>`), adjust (for example `default: 0`), `bin/rails db:migrate`, include the field in the form and in `params.expect`, validate in the model.

## P4. Add authentication (p.38-41)
`bin/rails generate authentication`; `bin/rails db:migrate`; create a User in the console; restart the server; `allow_unauthenticated_access only:` on the public actions; `authenticated?` in the views.

## P5. Notify by email (p.47-60)
Inventory -> model Subscriber `product:belongs_to email` -> `has_many ... dependent: :destroy` -> `SubscribersController` + nested route -> partial `_inventory` -> `bin/rails g mailer Product in_stock` with `product_url` -> `after_update_commit` callback -> (optional) extract a concern -> unsubscribe with `generates_token_for`.

## P6. Test and check quality (p.64-68)
Fill in fixtures; write a test with `assert_emails`; `bin/rails test`; `bin/rubocop` (`-a`); `bin/brakeman`; CI in `.github`.

## P7. Deploy (p.68-70)
Ubuntu LTS server (1 GB+), Docker Hub account and "store" repository, edit `config/deploy.yml`, export `KAMAL_REGISTRY_PASSWORD`, `bin/kamal setup`, create a User via `bin/kamal console`, then `bin/kamal deploy`.

## P8. Quick diagnosis (from the guide)
- Null variable in the view? Use `debug @variable` and check singular/plural (p.24).
- Changed the model with the console open? `reload!` (p.16).
- New gem from the generator did not load? Restart the server (p.39, 42).
- Edited the form and the field disappears on save? Include the field in `params.expect` (p.43, 45, 48).
- Migration error? `bin/rails db:rollback` undoes the last one (p.10).
