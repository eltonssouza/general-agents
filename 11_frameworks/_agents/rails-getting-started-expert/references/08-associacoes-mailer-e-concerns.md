# 08 - Inventory, associations, Action Mailer, callbacks, concern and tokens (RGS p.47-60)

## Inventory (RGS p.47-49)
Migration `AddInventoryCountToProducts` with `default: 0` (p.48); field `form.number_field :inventory_count`; `:inventory_count` in `params.expect`; `validates :inventory_count, numericality: { greater_than_or_equal_to: 0 }` (p.48-49).

## Subscribers (RGS p.49-51)
- `bin/rails generate model Subscriber product:belongs_to email` (p.49); migration with `t.belongs_to :product, null: false, foreign_key: true` and `t.string :email` (p.49).
- `bin/rails db:migrate` (p.50); `has_many :subscribers, dependent: :destroy` in Product (p.50); `belongs_to :product` in Subscriber (p.59).
- `SubscribersController`: `allow_unauthenticated_access`, `before_action :set_product` with `Product.find(params[:product_id])`, `create` with `@product.subscribers.where(subscriber_params).first_or_create` and `redirect_to @product, notice: "You are now subscribed."`; `subscriber_params` uses `params.expect(subscriber: [ :email ])` (p.50).
- Flash displayed in the layout with `flash[:notice]` and `flash[:alert]` (p.51). Nested route `resources :subscribers, only: [ :create ]` (p.51).
- Partial `_inventory.html.erb`: if `product.inventory_count.positive?` it shows the stock; otherwise "Out of stock" and a form `form_with model: [product, Subscriber.new]` with `form.email_field :email, placeholder: ..., required: true` (p.52).

## Action Mailer (RGS p.52-55)
- `bin/rails g mailer Product in_stock` generates `app/mailers/product_mailer.rb` with the `in_stock` method and two views (HTML and text) (p.52-53).
- Mailer: `@product = params[:product]; mail to: params[:subscriber].email` (p.53). The subject can come from the I18n file `en.product_mailer.in_stock.subject` (p.53).
- In emails use **`product_url`**, not `product_path`, because the email client needs the full URL (p.53).
- Manual test in the console: `ProductMailer.with(product: product, subscriber: subscriber).in_stock.deliver_later`; the email appears in the logs (p.53-55). `deliver_later` sends it to Active Job (p.70).

## Callback (RGS p.56)
```ruby
after_update_commit :notify_subscribers, if: :back_in_stock?
def back_in_stock?
  inventory_count_previously_was.zero? && inventory_count.positive?
end
```
`after_update_commit` runs after the changes are written; `if:` makes it conditional; `inventory_count_previously_was` exposes the previous value (Active Record tracks changes). `notify_subscribers` iterates over `subscribers` and enqueues the email with `deliver_later` (p.56) [from source]. Other callbacks: NOT COVERED.

## Concern (RGS p.57-58)
`ActiveSupport::Concern` is a Ruby module with syntactic sugar (p.57). `app/models/product/notifications.rb`: `module Product::Notifications; extend ActiveSupport::Concern; included do ... end; ...; end`; the code in `included` runs as if it belonged to the class and the methods become instance methods (p.57). The model then has `include Notifications` (p.58). Advantages: organizing by feature and reusing in other models (p.58).

## Unsubscribe token (RGS p.58-60)
- Route `resource :unsubscribe, only: [ :show ]` (p.58).
- `generates_token_for :unsubscribe` in the `Subscriber` model (p.59); `Subscriber.find_by_token_for(:unsubscribe, params[:token])` in the controller (p.59); `@subscriber&.destroy` and `redirect_to root_path, notice: "Unsubscribed successfully."` (p.59). The guide states that invalid or expired tokens are handled without error (p.60).
- Links in the emails: `unsubscribe_url(token: params[:subscriber].generate_token_for(:unsubscribe))` in the HTML and text templates (p.59-60).

## Limits
NOT COVERED: SMTP/production delivery configuration, mailer previews, `has_many :through`, email validations, `deliver_now`. The `&.` and `%i[]` syntax belongs to ruby-expert.
