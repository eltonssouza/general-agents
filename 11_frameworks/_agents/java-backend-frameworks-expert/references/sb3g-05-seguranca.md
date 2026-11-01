# SB3G-05. Security: Spring Security, OAuth2/JWT, Keycloak, RBAC (SB3G p.130-158)

## Basic configuration (SB3G p.131-135)
- `spring-boot-starter-security`; `@Configuration @EnableWebSecurity` class with `SecurityFilterChain`: CSRF disabled, `STATELESS` session, `/login` public, other requests authenticated, `httpBasic` (SB3G p.133-134). The book justifies disabled CSRF for APIs consumed by other applications (SB3G p.134).
- List of "Spring Boot 3.0" security features: authentication, authorization, defense against common threats (XSS, SQL injection), OAuth2/JWT (SB3G p.132). [inference] general statements by the author, without technical detail.

## Keycloak and OAuth2 (SB3G p.135-148)
- Keycloak as IAM via Docker Compose (image `bitnami/keycloak:latest`, its own Postgres database on port 5433, console on 8180) (SB3G p.136-138). [DATED] image, variables (`KEYCLOAK_USER`, `DB_VENDOR`...) and URLs `/auth/realms/...` (SB3G p.142) may have changed; the book itself warns that the UI changes (SB3G p.141).
- Console steps: realm `BookStoreRealm`, client `bookstore-client` (client authentication on, secret in *Credentials*), user with password (SB3G p.139-141).
- Dependencies: `spring-boot-starter-oauth2-client` and `spring-boot-starter-oauth2-resource-server` (SB3G p.141).
- Properties `spring.security.oauth2.client.registration.keycloak.*` (client-id, client-secret, scope `openid,profile,email`, `authorization-grant-type=authorization_code`, redirect-uri), `provider.keycloak.issuer-uri` and `spring.security.oauth2.resourceserver.jwt.issuer-uri` (SB3G p.142-143).
- `SecurityFilterChain` with `.oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))` (SB3G p.143-144).
- Own `/login` endpoint: `LoginRequestDto(username, password)` (record), `RestTemplate` and a call to Keycloak's token endpoint with `grant_type=password` (SB3G p.144-145). Response: `access_token`, `expires_in` 300 s, `refresh_token` (1800 s), `token_type` Bearer etc. (SB3G p.147). Token usage: header `Authorization: Bearer ...`; expires in 5 min (SB3G p.148).
- Agent warning: [extrapolation] the `password` flow is discouraged in current OAuth2; the book uses it without discussing it. The example secrets are for development.

## RBAC (SB3G p.148-153)
- Roles `user` and `admin` in Keycloak (SB3G p.149-150).
- `@EnableMethodSecurity`; rules: `POST /books`, `/authors` require `ROLE_ADMIN`; `GET` on `/books/**`, `/reviews/**`, `/authors/**`, `/publishers/**` accept `ROLE_USER` or `ROLE_ADMIN` (SB3G p.151).
- `KeycloakRoleConverter` converts the `realm_access.roles` claim into upper-case `ROLE_...` authorities (SB3G p.152-153).

## Reactive security (SB3G p.153-158)
- `SecurityWebFilterChain` with `ServerHttpSecurity`, `pathMatchers`, `authorizeExchange`; `ReactiveJwtAuthenticationConverter` and a converter that returns `Flux<GrantedAuthority>` (SB3G p.155-156). Reactive security context instead of thread-local (SB3G p.154).

## Limits
- Does not cover: Spring Authorization Server, SAML, LDAP, method security in depth (only `@EnableMethodSecurity` appears, SB3G p.151; `@PreAuthorize` is not demonstrated), CORS, security headers, key rotation, refresh token on the client: NOT COVERED. For complete Spring Security: spring-boot-reference-expert / [extrapolation].
