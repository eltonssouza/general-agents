# 04 - Routes (RGS p.17-22, 26-27, 51, 58)

## Path of a request (RGS p.17)
To "say hello" you need at minimum **a route, a controller with an action and a view**. The route maps a request to an action; the action does the work and prepares data; the view displays it. Routes are rules in a Ruby DSL; controllers are Ruby classes whose public methods are actions; views are templates (a mix of HTML and Ruby) [from source] (RGS p.17).

## URL and HTTP methods (RGS p.17-18)
Parts of the URL `https://example.org/products?sale=true&sort=asc`: protocol, host, path, query parameters (p.18). GET fetches data; POST sends data (typically to create); PUT/PATCH update; DELETE deletes (p.18). Query parameters are usually used in the controller to filter (p.18-19).

## Defining routes in `config/routes.rb` (RGS p.18-20)
- `get "/products", to: "products#index"`: GET on `/products` goes to the `index` action of `ProductsController` (p.18).
- `post "/products", to: "products#create"` (p.19).
- `get "/products/:id", to: "products#show"`: `:id` is a parameter that captures part of the URL; `/products/1` gives `id` = 1 (p.19-20). Parameters need not be integers (`get "/blog/:title", to: "blog#show"`, p.20).
- A route does not need a protocol, domain or query (p.18).

## CRUD: 8 typical routes (RGS p.20-21)
Index, New, Create, Show, Edit, Update (PUT, full), Update (PATCH, partial), Destroy (p.20). The guide shows the 8 lines written by hand (p.21).

## `resources` (RGS p.21)
`resources :products` replaces the 8 lines. To restrict actions, the guide points to the routing guide (p.21; content not included, NOT COVERED).

## `bin/rails routes` (RGS p.21-22)
Lists the routes with columns Prefix, Verb, URI Pattern and Controller#Action. For `resources :products`: `products` (GET index, POST create), `new_product`, `edit_product`, `product` (GET show, PATCH/PUT update, DELETE destroy) (p.22). Routes for built-in resources, such as health checks, also appear (p.22).

## Root (RGS p.23)
`root "products#index"` defines the home page (p.23).

## Path and URL helpers (RGS p.26-27)
The Prefix generates helpers: `products_path` -> `/products`; `products_url` -> `http://localhost:3000/products`; `product_path(1)` -> `/products/1`; `product_url(1)`. `_path` is relative to the current domain; `_url` includes protocol, host and port and is useful in emails (p.27). `link_to` takes the text and the path/URL (p.27).

## Nested routes and singular `resource` (RGS p.51, 58)
- `resources :products do resources :subscribers, only: [ :create ] end` defines subscribers nested in products (p.51); the action uses `params[:product_id]` (p.50).
- `resource :unsubscribe, only: [ :show ]` (singular, top level) handles `/unsubscribe?token=xyz` (p.58).
- Helpers with a token: `unsubscribe_url(token: ...)` (p.59).

## Limits
NOT COVERED: `namespace`, `scope`, `member`/`collection`, constraints, route `concern`, `direct`, API routes, routes for engines. For Ruby syntax of hashes/arrays, see ruby-expert.
