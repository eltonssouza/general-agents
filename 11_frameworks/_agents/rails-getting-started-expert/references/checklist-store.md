# Tutorial checklist ("store" app)

The guide builds the **store** app, not a "blog" (INDEX §1). `scripts/rails_store_checklist.py` **statically** inspects an app directory (read-only, without running Rails) and reports each item with its page. `--list` shows the list.

| ID | What the guide builds | RGS pages | Automatic check |
|---|---|---|---|
| S01 | Ruby 3.2+ and Rails 8.1.0+ | 2 | manual |
| S02 | Model `Product < ApplicationRecord` | 8, 11 | file `app/models/product.rb` |
| S03 | Migration `create_products` with `create_table :products`, `t.string :name`, `t.timestamps` | 8-9 | `db/migrate/*create_products*` |
| S04 | `validates :name, presence: true` | 16 | model |
| S05 | `resources :products` | 21 | `config/routes.rb` |
| S06 | `root "products#index"` | 23 | routes |
| S07 | Actions index, show, new, create, edit, update, destroy | 22-37 | controller |
| S08 | Strong params with `params.expect(product: [...])` | 30 | controller |
| S09 | `before_action :set_product` | 34-37 | controller |
| S10 | `render :new` / `render :edit` with `status: :unprocessable_entity` | 30-32 | controller |
| S11 | Views index, show, new, edit and partial `_form` | 23-34 | files in `app/views/products/` |
| S12 | `form_with model: product` in the partial | 33 | `_form.html.erb` |
| S13 | Authentication (`User`, `Session`) and `allow_unauthenticated_access only: %i[ index show ]` | 38-40 | models, controller |
| S14 | Layout with `<nav>` and a logout button if `authenticated?` | 39-40 | `application.html.erb` |
| S15 | `cache @product` in the show view | 41 | show |
| S16 | `has_rich_text :description` and `:description` permitted | 43 | model, controller |
| S17 | `has_one_attached :featured_image` and `:featured_image` permitted | 44-45 | model, controller |
| S18 | I18n: `config/locales/en.yml` and `es.yml`, `around_action :switch_locale` | 45-47 | locales, application_controller |
| S19 | Inventory: migration with `default: 0` and `numericality >= 0` | 47-48 | migrations, model |
| S20 | Subscriber `belongs_to :product` and `has_many :subscribers, dependent: :destroy` | 49-50 | models |
| S21 | `SubscribersController` and nested route `only: [ :create ]` | 50-51 | controller, routes |
| S22 | `ProductMailer#in_stock` with HTML and text views using `product_url` | 52-53 | mailer, views |
| S23 | Callback `after_update_commit :notify_subscribers, if: :back_in_stock?` | 56 | model or concern |
| S24 | Concern `Product::Notifications` | 57-58 | `app/models/product/notifications.rb` |
| S25 | Unsubscribe: `resource :unsubscribe`, `generates_token_for :unsubscribe`, `UnsubscribesController` | 58-59 | routes, model, controller |
| S26 | CSS in `app/assets/stylesheets/application.css` and `config/importmap.rb` | 60-63 | files |
| S27 | Fixtures `products.yml`/`subscribers.yml` and a test with `assert_emails` | 64-66 | test/ |
| S28 | `bin/rubocop` and `bin/brakeman` without offenses | 66-67 | manual |
| S29 | `config/deploy.yml` with `service: store` | 68-69 | file |
| S30 | `bin/kamal setup`; production user; Solid Queue | 69-70 | manual |

Honest use: passing the checklist indicates that the app **follows the shape of the tutorial**, not that it is correct or secure.
