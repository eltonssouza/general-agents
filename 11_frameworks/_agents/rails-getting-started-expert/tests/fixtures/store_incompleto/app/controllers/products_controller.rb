class ProductsController < ApplicationController
 def index
   @products = Product.all
 end
 def create
   @product = Product.new(params[:product])
   if @product.save
     redirect_to @product
   else
     render :new
   end
 end
end
