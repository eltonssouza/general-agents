# 09 - Assets, import maps and Hotwire (RGS p.60-63)

## Propshaft (RGS p.60-62)
It is the Rails **asset pipeline**: it serves CSS, JavaScript, images and other assets; in production it tracks each version of the assets to allow caching (p.60). The guide edits `app/assets/stylesheets/application.css` (p.60-61) and updates `show.html.erb` with `<section class="product">` and `<section class="product-info">` (p.62). Going deeper: "Asset Pipeline" guide (p.60, 63): NOT COVERED.

## Import maps (RGS p.62-63)
Rails uses **import maps** for JavaScript by default, allowing modern modules **without a build step** (p.62). The file `config/importmap.rb` contains "pins" that map a package name to a file/URL (e.g. `"@hotwired/turbo-rails"` -> `turbo.min.js`); `pin_all_from "app/javascript/controllers", under: "controllers"` maps a whole directory to a namespace (p.62-63). There are also pins for `trix` and `@rails/actiontext` (p.63). Comment in the file: "Pin npm packages by running ./bin/importmap" (p.63).

## Hotwire (RGS p.63)
A JavaScript framework that takes advantage of server-generated HTML, with three components: **Turbo** (navigation, form submission, updating parts of the page without custom JS), **Stimulus** (custom JS when needed) and **Native** (hybrid mobile apps) (p.63). The guide states that no JavaScript has been written yet, but the app already uses Hotwire: the product form is driven by Turbo (p.63); `turbo_confirm` as well (p.38).

## Limits
NOT COVERED: creating Stimulus controllers, Turbo Streams/Frames, bundlers (esbuild, webpack), Sass/Tailwind, npm. Points to "Working with JavaScript in Rails" (p.63).
