# 06 - Authentication with the Rails generator (RGS p.38-41, 70)

## Generate (RGS p.38)
Motivation: anyone could edit/delete products. Rails ships an **authentication generator** that creates the `User` and `Session` models and the controllers and views for login [from source] (RGS p.38).
```
$ bin/rails generate authentication
$ bin/rails db:migrate
```
(p.38).

## Create a user and restart (RGS p.39)
In the console: `User.create! email_address: "...", password: "...", password_confirmation: "..."` (p.39). **Restart the server** to load the `bcrypt` gem added by the generator; BCrypt securely hashes the passwords (p.39). The guide uses example credentials and tells you to use your own (p.39).

## Default effect (RGS p.39-40)
When visiting any page, the browser asks for email and password; once they are correct, the browser stores the credentials for subsequent requests (p.39). By default the generator **restricts all pages** to authenticated users (p.40).

## Logout and layout (RGS p.39-40)
In the layout: `<%= button_to "Log out", session_path, method: :delete if authenticated? %>` inside `<nav>`, with `<main><%= yield %></main>` (p.39-40). The button sends DELETE to the session path (p.40).

## Allowing public access (RGS p.40)
`allow_unauthenticated_access only: %i[ index show ]` in the controller opens the listing and detail pages (p.40). Without `only:`, the usage shown in the guide applies to the whole controller [inference] (used in `SubscribersController` and `UnsubscribesController`, p.50, 59).

## Show links only to authenticated users (RGS p.40-41)
The `authenticated?` helper in views: `link_to "New product", new_product_path if authenticated?` (p.40); `link_to "Login", new_session_path unless authenticated?` (p.41); Edit/Delete inside `if authenticated?` (p.41). Login page: `/session/new` (p.41).

## Production (RGS p.70)
The user must exist in the production database: `bin/kamal console` and `User.create!(...)` (p.70).

## Limits
NOT COVERED: Devise, OAuth, authorization/roles, "sign up" (points to the "Sign Up and Settings" tutorial, p.71), password reset. The guide says the default authentication asks for email and password in the browser; the internal mechanisms of `Current`, `Session` and cookies are not explained.
