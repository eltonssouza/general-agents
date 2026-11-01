# SB3G-06. Testing (SB3G p.160-181)

## TDD (SB3G p.161-165)
- Red/Green/Refactor cycle applied to an `AuthorService` with Mockito (`@Mock`, `when(...).thenReturn(...)`, `assertTrue`, `assertEquals`) and `@BeforeEach` for common data (SB3G p.162-164).
- The controller starts consuming the service; `EntityNotFoundException` on delete becomes 404 (SB3G p.164-165).
- Terminology: `assertThrows`, `verify` (with `times(1)`), `@InjectMocks`, `@ExtendWith(MockitoExtension.class)`, `@BeforeEach` (SB3G p.165-166).

## Controller tests with security (SB3G p.166-171)
- `@WebMvcTest(AuthorController.class)` loads only the web layer; `@Import(SecurityConfig.class)` brings in the security configuration; `@MockBean` replaces the service and `JwtDecoder`; `@WithMockUser` simulates user/roles (SB3G p.167-169).
- `MockMvcBuilders.webAppContextSetup(context).apply(springSecurity()).build()` in `@BeforeEach` (SB3G p.169).
- Role-parameterized tests (`@ParameterizedTest`, `@MethodSource`) and a 404 case with `doThrow` (SB3G p.170-171).

## Integration tests (SB3G p.171-178)
- Base class `AbstractIntegrationTest` + `AuthorControllerIntegrationTest`; isolated `application-integration-test.properties` (SB3G p.172-173).
- **Testcontainers** for Postgres (`postgres:latest`) and MongoDB (`mongo:4.4.6`); `@Container`; `@DynamicPropertySource` injects `spring.datasource.*` and `spring.data.mongodb.uri` (SB3G p.174-175). [DATED] image tags.
- **WireMock** (port 8180) simulates the OIDC provider (SB3G p.174, 176).
- Cleanup with `authorRepository.deleteAll()` in `@BeforeEach`; `@WithMockUser(authorities = {"ROLE_ADMIN"})` with real `MockMvc` and `jsonPath` (SB3G p.177-178).

## Reactive tests (SB3G p.178-181)
- `WebTestClient` with `@WebFluxTest(controllers = UserController.class, excludeAutoConfiguration = {...})`; `@MockBean` for `UserRepository` and `SecurityWebFilterChain`; assertions `expectStatus().isOk()`, `expectBodyList` (SB3G p.179-180).

## Limits
- Does not cover `@SpringBootTest` with `webEnvironment`, `@DataJpaTest`, `@ServiceConnection`, contract testing, performance testing, code coverage: NOT COVERED.
