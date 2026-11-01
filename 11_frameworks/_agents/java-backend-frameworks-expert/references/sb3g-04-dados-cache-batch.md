# SB3G-04. Spring Data, cache, batch and migration (SB3G p.100-129)

Sample project: **online bookstore** (Book, Author, Publisher; later Review) (SB3G p.100, 104).

## Spring Data JPA (SB3G p.101-111)
- Concepts: repository abstraction, SQL and NoSQL support (SB3G p.102-103).
- Gradle dependencies: `spring-boot-starter-data-jpa`, Lombok (`compileOnly` + `annotationProcessor`) (SB3G p.103).
- Entities with `@Entity`, `@Table`, `@Data` (Lombok), `@Id @GeneratedValue` (SB3G p.104). Repository: `interface BookRepository extends JpaRepository<Book, Long>` (SB3G p.104-105).
- **PostgreSQL with Docker Compose** (`postgres`, `POSTGRES_PASSWORD`, `POSTGRES_DB=bookstore`, port 5432) (SB3G p.105-106).
- `spring.datasource.url=jdbc:postgresql://localhost:5432/bookstore`, `spring.datasource.username/password`, `spring.jpa.hibernate.ddl-auto=update` (SB3G p.106).
- Relations: `@ManyToMany` Book->Author (generates `books_authors`) and `@ManyToOne` Author->Publisher (SB3G p.107-108).
- `BookController` with `@RequiredArgsConstructor` (Lombok); curl to create publisher, author and book (SB3G p.109-111).

## MongoDB (SB3G p.111-115)
- Compose with `mongo` (27017); `spring.data.mongodb.uri=mongodb://localhost:27017/bookstore` (SB3G p.112-113).
- `@Document(collection = "reviews")`, `interface ReviewRepository extends MongoRepository<Review, String>` (SB3G p.113-114). Hybrid SQL + NoSQL model (SB3G p.114).

## Cache (SB3G p.115-118)
- Dependency `spring-boot-starter-cache` and `@EnableCaching` on the main class (SB3G p.117).
- `@CacheEvict(value = "books", allEntries = true)` on POST/PUT; `@CacheEvict(value = "books", key = "#id")` on removal (SB3G p.117-118). `@Cacheable("books")` on `findById` in the repository (SB3G p.118).
- The book does **not** configure a cache provider (Caffeine, Redis) or TTL: NOT COVERED.

## Spring Batch (SB3G p.119-123)
- Dependencies: `spring-boot-starter-batch`, `starter-data-jpa`, `postgresql` (runtime) (SB3G p.120).
- Job `importPublisherJob` (`JobBuilder`, `RunIdIncrementer`) and a *chunk*-based Step of 10 with `reader`/`processor`/`writer` (SB3G p.121).
- CSV reading with `FlatFileItemReader` (`publishers.csv`), a processor that upper-cases text, `JpaItemWriter` (SB3G p.122-123).

## Migration with Liquibase (SB3G p.124-128)
- `implementation 'org.liquibase:liquibase-core'`; `spring.liquibase.change-log=classpath:/db/changelog/db.changelog-master.yaml` (SB3G p.125).
- Changelog in XML/JSON/YAML/SQL; `includeAll` with alphabetical order (SB3G p.125-126).
- Example: `001-add-published-column.yaml`, `changeSet`, `addColumn` `published` boolean default `false`; the entity gets `Boolean published` (SB3G p.126-127). The book stresses the importance of file names/order (SB3G p.126).

## Limits
- Does not cover pagination, transactions (`@Transactional`), N+1, projections, derived queries beyond reactive `findByEmail`, nor Flyway: NOT COVERED.
- `ddl-auto=update` is used in the example (SB3G p.106); [extrapolation] it is not a production recommendation from the book.
