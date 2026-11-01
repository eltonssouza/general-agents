# 07 - Swift: concurrency (SWT p.14-15)

Source SWT (Swift version not stated). The tour shows concurrency with five constructs; the text is short and the code is in an image. [DATED] to 2026: do not assert in which version these features appeared (it is not in the text).

## async and await (SWT p.14)
- `async` marks a function that runs **asynchronously** (SWT p.14; code: `func fetchUserID(from server: String) async -> Int`) [from source].
- A **call** to an asynchronous function is marked with **`await`** in front (SWT p.14; code: `await fetchUserID(from: server)`) [from source].

## async let (SWT p.14)
- `async let` calls an asynchronous function **in parallel** with other asynchronous code; when **using** the returned value, you write `await` (SWT p.14; code: `connectUser(to:)` fires `fetchUserID` and `fetchUsername` with `async let` and then uses `await` in the interpolation) [from source].

## Task (SWT p.14)
- `Task` calls asynchronous functions **from synchronous code**, without waiting for the return (SWT p.14; code: `Task { await connectUser(to: "primary") }`) [from source].

## Task groups (SWT p.14-15)
- **Task groups** structure concurrent code (SWT p.14) [from source]. Code (p.15): `withTaskGroup(of: Int.self)` adds tasks with `group.addTask`, collects results with `for await result in group` and returns the array. The snippet is split between p.14 (start) and p.15 (body) [from source].

## Actors (SWT p.15)
- **Actors** are similar to classes, but guarantee that **different asynchronous functions can interact safely with the same instance** at the same time (SWT p.15) [from source].
- When calling a method or accessing a property of an actor, the code takes **`await`**, indicating that it may have to wait for other code already running on the actor (SWT p.15; code: `actor ServerConnection`, `await server.connect()`) [from source].

## Limits (NOT COVERED)
`@MainActor`, `Sendable`, isolation, cancellation, `AsyncSequence`/`AsyncStream`, `async` in initializers, error handling in tasks, strict concurrency mode, and **any** concept of threads/queues (Dispatch). The text says *what* each construct does, not the detailed rules.
