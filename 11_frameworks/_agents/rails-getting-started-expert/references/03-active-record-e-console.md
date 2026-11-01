# 03 - Models, migrations, Active Record and console (RGS p.8-17, 47-50)

## Generate the model and the migration (RGS p.8-9)
- `bin/rails generate model Product name:string` creates: a migration in `db/migrate`, the model `app/models/product.rb`, tests and fixtures [from source] (RGS p.8).
- Active Record maps relational databases to Ruby code and generates the SQL; the app uses **SQLite**, the Rails default (p.8).
- Model names are **singular** (one instance = one record); table names are **plural** [from source] (RGS p.8-9).
- The migration (`class CreateProducts < ActiveRecord::Migration[8.1]`) uses `create_table :products` with `t.string :name` and `t.timestamps`; `t.timestamps` defines `created_at` and `updated_at`, filled in automatically by Active Record (p.9).
- Migration = a set of database changes, which lets you track changes made in development and deploy them to production safely (p.8).
- `bin/rails db:migrate` applies new migrations (p.9); `bin/rails db:rollback` undoes the last one (p.10).
- Convention of the guide: the file path appears as a comment at the top of each snippet (p.9).

## Console (RGS p.10)
`bin/rails console` opens an interactive console in the development environment; `Rails.version` returns `"8.1.0"` in the example output (p.10).

## The model without code (RGS p.10-11)
`class Product < ApplicationRecord; end`. Rails queries the database, discovers columns and types and defines the attributes dynamically (p.11). `Product.column_names` returns `["id", "name", "created_at", "updated_at"]` (p.11).

## CRUD in the console (RGS p.11-16)
| Operation | Code in the guide | Guide's remark |
|---|---|---|
| Instantiate | `Product.new(name: "T-Shirt")` | not saved, no id/timestamps (p.11) |
| Save | `product.save` | generates `INSERT`; fills in id and timestamps (p.12) |
| Create | `Product.create(name: "Pants")` | instantiates and saves in one call (p.12) |
| List | `Product.all` | `SELECT`; returns `ActiveRecord::Relation` (p.13) |
| Filter | `Product.where(name: "Pants")` | adds `WHERE`; returns Relation (p.13) |
| Order | `Product.order(name: :asc)` | `ORDER BY` (p.13) |
| Find by id | `Product.find(1)` | `WHERE id = 1 LIMIT 1`; returns an instance (p.14) |
| Update | `product.update(name: "Shoes")` | assigns, **runs validations** and saves (p.14) |
| Update (2 steps) | `product.name = "T-Shirt"; product.save` | alternative (p.15) |
| Delete | `product.destroy` | `DELETE` (p.15) |
`Relation` is an Array-like collection with filtering, ordering and other operations (p.13). `all` is a class method (p.12).

## Validations (RGS p.16-17)
- `validates :name, presence: true` ensures every product has a name (p.16).
- Rails runs validations automatically on `create`, `update` and `save` (p.17).
- `Product.new.save` returns `false` (p.16); `product.errors` returns an `ActiveModel::Errors` and `product.errors.full_messages` gives friendly messages (`"Name can't be blank"`) (p.17).
- `numericality: { greater_than_or_equal_to: 0 }` validates `inventory_count` (p.48).
[from source]. Other validators: NOT COVERED.

## More migrations (RGS p.47-50)
- `bin/rails generate migration AddInventoryCountToProducts inventory_count:integer`: the name follows the convention `add_<columns>_to_<table>` and the generator pre-fills `add_column :products, ...` (p.47). `rails generate migration --help` lists other conventions (p.47).
- Edit the file to `add_column :products, :inventory_count, :integer, default: 0` and ensure it is never nil (p.48).
- `bin/rails generate model Subscriber product:belongs_to email`: `belongs_to` creates the `product_id` column and a foreign key (`t.belongs_to :product, null: false, foreign_key: true`); without a type, the column is `string` (p.49-50).

## Associations (RGS p.49-50)
`belongs_to :product` in `Subscriber` and `has_many :subscribers, dependent: :destroy` in `Product`; a one-to-many relationship (p.49-50). `has_one_attached` (p.44) and `has_rich_text` (p.43) are model macros for the Active Storage and Action Text features. `has_many :through`, polymorphic associations and `scope`: NOT COVERED.

## Limits and boundary
Only SQLite appears. SQL and relational modeling: database agents; Ruby syntax (`%i[]`, blocks): ruby-expert.
