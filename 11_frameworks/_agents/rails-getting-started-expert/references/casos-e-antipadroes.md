# Cases and antipatterns (each rule with its support in the guide)

The linter (`scripts/rails_lint.py`) uses the rules below. Label: **[from source]** = the guide shows the practice or explains it; **[extrapolation]** = not in the guide (only emitted with `--extrapolacoes`).

| ID | Antipattern | Practice in the guide | Label | Page |
|---|---|---|---|---|
| L01 | Passing `params[:x]` straight to `new`/`update`/`create` | filter with `params.expect` (strong parameters) | [from source] | 30 |
| L02 | `render :new`/`:edit` without `status: :unprocessable_entity` | report 422 to the browser on failure | [from source] | 31 |
| L03 | `Product.find(params[:id])` repeated in 3+ actions | extract `before_action :set_product` | [from source] | 34 |
| L04 | 8 CRUD routes written by hand | `resources :products` | [from source] | 21 |
| L05 | Route `to:` without `controller#action` | format `"products#index"` | [from source] | 18 |
| L06 | Model with a plural name (`class Products`) | singular model, plural table | [from source] | 8-9 |
| L07 | Model that does not inherit from `ApplicationRecord` | `class Product < ApplicationRecord` | [from source] | 11 |
| L08 | `_path` in a mailer template | use `_url` in emails | [from source] | 27, 53 |
| L09 | `<%= collection.each do ... %>` prints the array | use `<% %>` for iteration | [from source] | 25 |
| L10 | `@variable` inside a partial | partial with a local variable | [from source] | 33 |
| L11 | Hard-coded `<a href="/products/<%= id %>">` | helpers `product_path` / `link_to` | [from source] | 26-27 |
| L12 | Migration without a version (plain `ActiveRecord::Migration`) | `ActiveRecord::Migration[8.1]` | [from source] (form shown; the reason is not explained) | 9 |
| L13 | `has_many` without `dependent:` | example uses `dependent: :destroy` | [inference] (the guide only shows the example) | 50 |
| L14 | `link_to ..., method: :delete` | the guide uses `button_to ..., method: :delete` | [extrapolation] | 38 |
| L15 | Controller file whose name does not match the class | `products_controller.rb` <-> `ProductsController` | [from source] | 23 |
| L16 | `form_for`/`form_tag` | the guide only uses `form_with` | [extrapolation] (NOT COVERED) | 29 |
| L17 | `require` of an app file | Rails loads by naming convention | [from source] | 7 |

Practical cases
1. "The description field does not save": [from source] permit `:description` in `params.expect` (p.43).
2. "Nothing appears in `index`": check `@products` (plural) and use `debug` (p.24).
3. "I want a read-only route": the guide says `resources` accepts restriction and points to the routing guide (p.21); the exact form is NOT COVERED (an `only:` example appears in nested routes, p.51, 58).
4. "I need a JSON API": NOT COVERED (the guide mentions JSON only as a view format, p.5).
5. "Use PostgreSQL": NOT COVERED; the guide uses SQLite (p.8).
