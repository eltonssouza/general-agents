# 05 - Controllers, views, forms, partials and filters (RGS p.22-39)

## Generate the controller (RGS p.22)
`bin/rails generate controller Products index --skip-routes` creates the controller, the views folder, the view for the given action, a controller test and a helper; `--skip-routes` avoids touching the routes already defined [from source] (RGS p.22).

## Action and template (RGS p.22-24)
`ProductsController < ApplicationController`; `index` is an action (public method). Even when empty, Rails renders the template with the same name (`app/views/products/index.html.erb`) [from source] (RGS p.22-23). Test in the browser at `/products` (p.23).

## Instance variables and ERB (RGS p.24-25)
- Instance variables (`@products = Product.all`) share data with the view (p.24).
- ERB: `<%= %>` executes and **prints** the return value; `<% %>` executes **without printing** (p.24-25). An iteration `@products.each` must go in `<% %>`, otherwise it would print the array (p.25).
- The helper `debug @products` prints the variable as YAML and helps detect a wrong variable, such as `@product` instead of `@products` (p.24). Other helpers: Action View Helpers guide (p.24, NOT COVERED here).

## Show and params (RGS p.25-26)
`def show; @product = Product.find(params[:id]); end`; `@product` singular in `show` and `@products` plural in `index` (p.26). `params` holds the request parameters; `/products/1` -> id 1 (p.26). The view `show.html.erb` lives in `app/views/products/` (p.26). Prefer helpers: `link_to product.name, product_path(product.id)` instead of `<a href="/products/<%= product.id %>">` (p.26-27).

## New and create (RGS p.27-31)
- `new`: `@product = Product.new` to display the form (p.28). Link: `link_to "New product", new_product_path` (p.28).
- `form_with model: @product do |form|` with `form.label :name`, `form.text_field :name`, `form.submit`: the builder takes care of the **CSRF token**, the URL derived from the model and the button text (p.29). The HTML source shows `authenticity_token`, `accept-charset="UTF-8"`, names `product[name]` and a button with `data-disable-with` (p.29). With a new instance, the form sends a **POST** to `/products` (p.29).
- `create`: `@product = Product.new(product_params)`; `if @product.save` -> `redirect_to @product`; otherwise `render :new, status: :unprocessable_entity` (p.30). `redirect_to` with an object generates the `show` path (`/products/2`) (p.30-31). The **422** status tells the browser that the POST failed; the template re-renders with the data that was typed in (p.31).

## Strong parameters (RGS p.30)
```ruby
def product_params
  params.expect(product: [ :name ])
end
```
(`private` method). It requires the `:product` key and permits only the listed attributes; the other parameters are ignored, protecting against malicious users [from source] (RGS p.30). When adding fields (`:description`, `:featured_image`, `:inventory_count`), they must be included in the list (p.43, 45, 48). **[DATED]**: the guide uses `params.expect`; earlier forms of strong params do **not** appear in this PDF (NOT COVERED).

## Edit and update (RGS p.31-32)
Same structure as new/create: `edit` loads the record; `update` uses `@product.update(product_params)` and, on failure, `render :edit, status: :unprocessable_entity` (p.32).

## Partials (RGS p.33-34)
- Extract the form to `app/views/products/_form.html.erb` (name starts with `_`); replace `@product` with the **local variable** `product`; show errors with `form.object.errors.any?` / `full_messages.first` (p.33).
- Usage: `<%= render "form", product: @product %>` in `new.html.erb` and `edit.html.erb` (p.33-34).
- Local variables let you reuse the partial several times on the same page (p.33). Going deeper: Action View guide (p.34).
- Another partial: `_inventory.html.erb`, called by `render "inventory", product: @product` (p.52).

## before_action (RGS p.34-35)
`before_action :set_product, only: %i[ show edit update ]` extracts the repeated `Product.find(params[:id])` from three methods; it is DRY in action (p.34-35). `set_product` goes under `private`. Later `destroy` is added to the list (p.36-37).

## Destroy (RGS p.36-38)
`def destroy; @product.destroy; redirect_to products_path; end` (p.37). In the view: `button_to "Delete", @product, method: :delete, data: { turbo_confirm: "Are you sure?" }`; `button_to` generates a form with a button that sends DELETE; `turbo_confirm` asks for confirmation via Turbo (p.38).

## Layout and flash (RGS p.39, 50-51)
`app/views/layouts/application.html.erb` holds the HTML common to all pages (p.39); `yield` goes inside `<main>`. The **flash** passes temporary data to the next action (`redirect_to @product, notice: "..."`), displayed by `flash[:notice]` and `flash[:alert]` in the layout (p.50-51).

## Limits
NOT COVERED: JSON responses, `respond_to`, advanced `render`, custom layouts, helpers beyond those listed, `form_for`/`form_tag`, `after_action`/`skip_before_action` filters. Points to "Layouts and Rendering in Rails" (p.71).
