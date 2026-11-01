# app/controllers/products_controller.rb
class ProductsController < ApplicationController
 def show
   @product = Product.find(params[:id])
 end
 def edit
   @product = Product.find(params[:id])
 end
 def update
   @product = Product.find(params[:id])
   if @product.update(params[:product])
     redirect_to @product
   else
     render :edit
   end
 end
end
