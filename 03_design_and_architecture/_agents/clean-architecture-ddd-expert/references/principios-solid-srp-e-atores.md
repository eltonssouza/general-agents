# SRP: responsibility as a "reason to change" and the people behind the change

Source: Robert C. Martin, **"The Single Responsibility Principle"**, post on The Clean Code Blog, May 8, 2014 (acronym `SRP`; 15-page PDF, browser printout). Content on **p.1-5**; p.6-15 are only the blog sidebar. **Convention**: `(SRP p.N)` = PDF page. Labels: `[from source]`, `[inference]`, `[extrapolation]`, `[DATED]`.

> **Correction relative to the previous version of the package.** The post does **not** state the SRP as "a module should be responsible to one, and only one, **actor**": that is the formulation of the book *Clean Architecture* (2017) `[extrapolation]`. The post uses "one and only one **reason to change**" and "gather together the things that change for the same reasons" (p.2 and p.5), and explains that the reasons for change come from **people** (a tightly coupled group representing a business function, p.4). The word "actor" does not appear in the PDF. Also **not in the post**: the helper class `regularHours()`, "merge conflicts" as a symptom, the three-class solution (`PayCalculator`, `HourReporter`, `EmployeeSaver`) and the Facade pattern. All of that is from `Clean Code`/`Clean Architecture` `[extrapolation]`.

---

## 1. The lineage of the principle

- In 1972, David Parnas published "On the Criteria To Be Used in Decomposing Systems into Modules" (CACM, December, vol. 15, no. 12). Martin cites the conclusion: it is almost always incorrect to begin the decomposition of a system with a flowchart; better to start from a list of difficult design decisions or decisions likely to change, with each module hiding one decision from the others `[from source] (SRP p.1)`. Martin reads this as: modules should be separated, at least in part, by the way they might change `[from source] (SRP p.1)`.
- Two years later, Dijkstra introduced the term *Separation of Concerns*; in the 1970s-80s, coupling and cohesion were introduced by Larry Constantine and extended by DeMarco, Page-Jones and others `[from source] (SRP p.2)`.
- In the late 1990s Martin tried to consolidate these notions into a principle, the SRP (he has a vague impression of having taken the name from Bertrand Meyer, without confirming it) `[from source] (SRP p.2)`.

## 2. The definition and the question it leaves

- SRP: each software module should have **one and only one reason to change** `[from source] (SRP p.2)`.
- This "sounds good", but leaves the question: what defines a reason to change? Do bug fixes and refactorings count? Martin answers by linking "reason to change" to "responsibility": the code is not responsible for fixes or refactorings (that belongs to the programmer); the better question is **to whom** the program is responsible, that is, to whom the program's design must answer `[from source] (SRP p.2)`.

## 3. The CFO / COO / CTO example

- In a typical organization, below the CEO are the CFO (finance), the COO (operations) and the CTO (infrastructure and technology development) `[from source] (SRP p.2-3)`.
- Java class `Employee` with `calculatePay()`, `save()` and `reportHours()` `[from source] (SRP p.3)`: `calculatePay` implements the pay calculation (contract, status, hours); `save` writes the data to the company database; `reportHours` returns a string used in audit reports `[from source] (SRP p.3)`.
- Who specifies each: the CFO specifies pay (financial responsibility); another executive, in the operations line (the COO), specifies the `reportHours` string; the CTO answers for `save` `[from source] (SRP p.3-4)`. The text uses the question "who would get fired" as a rhetorical device and the footnote admits the hyperbole `[from source] (SRP p.3, 5)`.
- Conclusion: changes to `calculatePay` come from the CFO's organization; to `reportHours`, from the COO's; to `save`, from the CTO's `[from source] (SRP p.4)`.

## 4. The central point: "this principle is about people"

- When writing a module, the requested changes should be able to come from **a single person, or from a tightly coupled group representing a narrowly defined business function**; isolate modules from the complexity of the organization and design each module to respond to the needs of only one business function `[from source] (SRP p.4)`.
- Reason: customers and managers are terrified when a program fails in a way that, to them, is unrelated to what they asked for. If changing `calculatePay` breaks `reportHours`, the COO will start demanding that nobody touch `calculatePay` `[from source] (SRP p.4)`.
- The mechanic analogy: taking the car in to fix the power window and getting the car back with the window working but not starting; nobody goes back to that mechanic `[from source] (SRP p.4-5)`.
- Applications cited by the text: that is why you don't put SQL in JSPs, don't generate HTML in the modules that compute results, business rules must not know the database schema; "that is why we separate concerns" `[from source] (SRP p.5)`.

## 5. Alternative formulation

- "Gather together the things that change for the same reasons. Separate the things that change for different reasons." Martin says this is another way of defining **cohesion and coupling**: increase cohesion among what changes for the same reasons and decrease coupling between what changes for different reasons `[from source] (SRP p.5)`.
- Final reminder: the reasons to change are people; avoid confusing those people (and yourself) by mixing code that many different groups value for different reasons `[from source] (SRP p.5)`.
- The same wording ("Gather together...") reappears in `SREL p.2`, with the remark that microservices do not solve the issue.

## 6. How to apply (explicit extrapolations)

- Using the post's Employee to **diagnose** a mix of responsibilities is faithful to the text. Proposing the refactoring into `EmployeeData` + three classes + Facade is `[extrapolation]` (it comes from another work by the author).
- "Accidental duplication" (a function shared between `calculatePay` and `reportHours`) is `[extrapolation]` based on the book Clean Architecture (2017); the post only describes the general risk of breaking what the other group did not ask to change (p.4).
- Mapping "actor" to CFO/COO/CTO is useful as a didactic label `[inference]` (the text ties change to people/business functions, p.4).
- "Each function should do only one thing" is **not** the SRP: the PDF does not discuss this confusion; the distinction is external knowledge `[extrapolation]`.
