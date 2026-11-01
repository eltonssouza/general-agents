# Procedures (each step with its origin)

Convention: `(SIGLA p.N)` = PDF page. Each step is marked `[from source]`, `[inference]` or `[extrapolation]`. The playbooks are compositions of this package; only the steps marked `[from source]` have direct backing.

## 1. Write a clear, stable unit test
1. `[from source]` Choose the smallest possible size (small: one process, no sleep, I/O or network) (SWE-G p.153-154).
2. `[from source]` Call the public API, like the user (SWE-G p.167-169).
3. `[from source]` Prefer the real implementation; if it is slow or nondeterministic, a fake from the API owner; stub only for states the real one does not produce; interaction testing only for functions that change state (SWE-G p.189-198).
4. `[from source]` Structure it as given/when/then (or arrange/act/assert) and test one behavior per test (SWE-G p.172-174; p.183 note 6).
5. `[from source]` Name it by the behavior; no logic; fail with expected versus actual (SWE-G p.174-177).
6. `[from source]` Relevant values visible in the test body; helpers/builders for the rest (SWE-G p.179-181).
7. `[inference]` If the test only passes with many stubs, the code under test may need refactoring (SWE-G p.197).

## 2. Choose the type of double (mirrors `doubles_selector.py`)
1. Is the real one fast, deterministic and with simple dependencies? Use the real one (SWE-G p.191).
2. Is there a fake maintained by the owner? Use it; otherwise ask the owner, or wrap the API and make a fake of the wrapper (SWE-G p.193-195).
3. Do I need a specific value or error? Stub, few of them (SWE-G p.197).
4. Do I need to verify a state-changing effect or the number/order of calls? Interaction testing, minimal specification (SWE-G p.198-200).
5. `[extrapolation]` Required parameter that is never used: a "dummy" value (Meszaros's term).

## 3. JUnit 4 suite (what the PDF teaches)
1. `[from source]` Test folder separate from the production one (JUNIT p.4).
2. `[from source]` `@Before`/`@After` per test; `@BeforeClass`/`@AfterClass` (static) for expensive setup (JUNIT p.3).
3. `[from source]` Group with `@RunWith(Suite.class)` or `@Category` (JUNIT p.7-8); varied data with `Parameterized` (JUNIT p.7).
4. `[extrapolation]` In JUnit 5, use the equivalence map in the JUnit file (`@BeforeEach` etc.); check the current documentation.

## 4. JMeter test plan (version 2.11 of the PDF)
1. `[from source]` Create the Thread Group: threads, ramp-up, loop count, error behavior (JMETER p.15).
2. `[from source]` Add samplers and config elements (HTTP Request Defaults, CSV Data Set Config) (JMETER p.15-19).
3. `[from source]` Timers for the interval between requests (JMETER p.18; 500 ms example, p.29).
4. `[from source]` Assertions per sample (Duration, Size) (JMETER p.29-31).
5. `[from source]` Post processors to extract values (JMETER p.20).
6. `[from source]` Few listeners; run with `jmeter -n -t plano.jmx -l resultado.jtl` (JMETER p.50).
7. `[extrapolation]` Size N with Little's Law (N = X × (R+Z)) and check that the generating machine can cope; HTML report with `-e -o` in recent versions `[DATED]` relative to the PDF.

## 5. Prepare test data (TDM)
1. `[from source]` Capture the data requirements in the user story (TDM p.3-4).
2. `[from source]` Do automatic profiling to find PII (TDM p.4).
3. `[from source]` Prefer synthetic data in the early phases; consider sub-setting or virtualization to reduce the footprint (TDM p.4-5).
4. `[from source]` If copying real data, apply non-reversible, consistent masking with a "tight" scope (TDM p.6).
5. `[from source]` Validate with an automatic scan that the PII is gone (TDM p.6-7).
6. `[from source]` Reserve pools via data views; standardize and automate the operations (TDM p.7).
7. `[from source]` Exemptions only as a last resort, with a request and a recorded window (TDM p.8).
