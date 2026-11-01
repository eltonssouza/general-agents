# 02 - Creating the app, server and autoload (RGS p.2-7)

## Prerequisites (RGS p.2)
Ruby 3.2 or newer, Rails 8.1.0 or newer, a code editor. Installation: the guide points to the "Install Ruby on Rails Guide" without repeating it [from source] (RGS p.2). Verification: `rails --version` must show Rails 8.1.0 or higher (p.2). Commands preceded by `$` run in the terminal (p.2).

## Generate the app (RGS p.3)
- `rails --help` lists the commands (p.3).
- `rails new store` generates the base of a new app (p.3); then `cd store`.
- `rails new --help` shows customization flags (p.3).

## First run (RGS p.5-7)
1. `bin/rails db:create` creates the database (p.5).
2. `bin/rails server` starts the **Puma** server, which serves static files and the app (p.6). Open `http://localhost:3000` to see the default welcome page, the app's "smoke test" (p.6-7). Stop with Ctrl-C (p.7).
3. Inside the app directory, use `bin/rails` (not `rails`) to make sure the app's own Rails version is used [from source] (RGS p.6).

## Autoload and reloading in development (RGS p.7)
- In development, new or changed files are detected and (re)loaded automatically, without restarting the server [from source] (RGS p.7).
- Rails apps rarely use `require`: Rails uses naming conventions to load files (p.7). Complement from the guide (p.23): the file `products_controller.rb` is the "underscored" version of the class `ProductsController`, which enables automatic loading.
- Further reading is referred to "Autoloading and Reloading Constants" (p.7); the content of that guide is not included here [NOT COVERED].
- In the console, after changing the code with the console open, you must run `reload!` manually (p.16).

## [DATED]
Example output versions (Puma 6.4.3, ruby 3.3.5, Rails 8.1.0) and the Ruby 3.2+ requirement hold for this PDF (RGS p.2, 6).
