# db/migrate/20240426151900_create_products.rb
class CreateProducts < ActiveRecord::Migration
 def change
   create_table :products do |t|
     t.timestamps
   end
 end
end
