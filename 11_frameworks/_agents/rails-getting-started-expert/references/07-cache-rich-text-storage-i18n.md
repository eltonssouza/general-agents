# 07 - Cache, Action Text, Active Storage and I18n (RGS p.41-47)

## Fragment cache (RGS p.41-42, 44)
- **Solid Cache** is a database-backed cache store, included by default (p.41).
- `<% cache @product do %> ... <% end %>` stores HTML in the cache; the key combines the record's `cache_key` (e.g. `"products/1"`) with the **template digest** (p.41). The key changes when the record is updated, avoiding serving stale data (p.42), and also when the view is changed (p.44).
- To enable caching in development: `bin/rails dev:cache` (p.41-42).
- In the logs: the first visit shows `Read fragment` and `Write fragment`; the second only `Read fragment` (p.42).
- Going deeper is referred to "Caching with Rails" (p.42): NOT COVERED.

## Action Text (RGS p.42-44)
`bin/rails action_text:install`, `bundle install`, `bin/rails db:migrate`; restart the server (p.42). In the model: `has_rich_text :description` (p.43). In the form: `form.rich_textarea :description` (p.43). Permit `:description` in `params.expect` (p.43). Display with `<%= @product.description %>` (p.43). The guide says the formatted text (bold/italic) appears on the page and is preserved when editing (p.44). The guide shows a `pin "trix"` and `@rails/actiontext` in the import map (p.63).

## Active Storage (RGS p.44-45)
Action Text relies on Active Storage. Dragging an image into the editor uploads it (p.44). Direct use: `has_one_attached :featured_image` in the model; `form.file_field :featured_image, accept: "image/*"` in the form; permit `:featured_image` in `params.expect`; display with `image_tag @product.featured_image if @product.featured_image.attached?` (p.44-45). The `storage/` folder holds files of the Disk service (p.4). Going deeper is referred to "Active Storage Overview" (p.45): NOT COVERED.

## I18n (RGS p.45-47)
- The `t` / `translate` helper looks up the translation by name for the current locale (p.45): `<h1><%= t "hello" %></h1>`.
- Default locale English: `config/locales/en.yml` (created by `rails new`) with `en: hello: "Hello world"`; create `config/locales/es.yml` for Spanish (p.45).
- Switching locale by URL parameter in `ApplicationController`:
```ruby
around_action :switch_locale
def switch_locale(&action)
  locale = params[:locale] || I18n.default_locale
  I18n.with_locale(locale, &action)
end
```
runs on every request, uses `params[:locale]` or the default and restores it afterwards (p.46). `?locale=es` shows Spanish; without the parameter, English (p.46).
- Relative key: `t ".title"` in the view `products/index` looks up `en.products.index.title` (p.46-47).

## [DATED] / caution
The guide only illustrates locale by parameter; it does not address the security of accepting any value in `params[:locale]` (it is an [extrapolation] that invalid values should be validated; the guide does not say so).
