# Linked lists (Ch. 3)

Pages = PDF (printed = N − 12). Source: ODS Ch. 3 (p.73-93).

## 1. General idea
- Structures made of nodes linked by references; constant-time `get(i)`/`set(i,x)` is lost, dynamism is gained: given a reference to a node `u`, deleting `u` or inserting next to it takes constant time at any position `[from source] (ODS p.73)`.

## 2. SLList (singly linked list)
- A node with data `x` and `next`; the list stores `head`, `tail` and `n` `[from source] (ODS p.73-74)`.
- `push(x)` and `pop()` operate on `head`; `add(x)` (queue) appends at `tail` and `remove()` is equivalent to `pop()`; all O(1). There are special cases: the empty list and removal of the last element (adjusting `tail`) `[from source] (ODS p.74-76)`.
- **Theorem 3.1**: implements Stack and FIFO Queue with push/pop/add/remove in O(1) `[from source] (ODS p.76)`.
- Removal from the tail is missing: it would require updating `tail` to the predecessor, reachable only by traversing the list from `head` in n−2 steps `[from source] (ODS p.76)`.
- The book poses as an exercise to explain why a `dummy` node cannot be used in SLList to eliminate the special cases `[from source] (ODS p.90)`.

## 3. DLList (doubly linked list with a sentinel node)
- Each node has `prev` and `next`; in DLList the special cases multiply, and the cleanest way to handle them is a `dummy` node without data, so that every node has `next` and `prev` and the list forms a cycle `[from source] (ODS p.76-77)`.
- Initialization: `dummy.prev` and `dummy.next` point to `dummy` itself `[from source] (ODS p.77)`. `dummy.next` is the first node and `dummy.prev` the last `[from source] (ODS p.77)`.
- `get_node(i)`: if `i < n/2` it walks from `dummy.next`, otherwise backwards from `dummy`; cost O(1+min{i, n−i}) `[from source] (ODS p.77-78)`.
- `add_before(w,x)` creates `u` and adjusts four links (`u.prev`, `u.next`, `u.next.prev`, `u.prev.next`); `remove(w)` adjusts two (`w.prev.next`, `w.next.prev`); thanks to the `dummy`, no boundary checks `[from source] (ODS p.78-79)`.
- **Theorem 3.2**: get/set/add/remove in O(1+min{i, n−i}); ignoring `get_node`, all operations are constant. Therefore linked lists are suitable when the references to the nodes come from outside `[from source] (ODS p.80)`.
- `[inference]` `add_first`, `remove_first`, `add_last`, `remove_last` are `add(0,x)`, `remove(0)`, `add(size(),x)` and `remove(size()-1)` (ODS p.19); since `get_node` at the ends costs O(1), all four are worst-case O(1).

## 4. SEList (space-efficient linked list)
- Motivation: each DLList node has two list references and one datum `[from source] (ODS p.80)`.
- Block parameter b; each node stores a block (`BDeque`, a bounded deque derived from ArrayDeque, a fixed array of size b+1 that never grows or shrinks) `[from source] (ODS p.80-81)`.
- **Invariant**: except for the last block, each block has between b−1 and b+1 elements; hence there are at most `n/(b−1) + 1 = O(n/b)` blocks and the wasted space is O(b + n/b). With b within a constant factor of √n, the overhead approaches the √n lower bound of section 2.6.2 `[from source] (ODS p.81)`.
- Locating index i: traverses blocks from the front or the back, each step advances at least b−1 elements; cost O(1+min{i, n−i}/b) `[from source] (ODS p.81-82)`. `get`/`set` inherit this cost `[from source] (ODS p.82-83)`.
- `add(x)` at the end: allocates a new block if the last one is full. `add(i,x)` in the interior: explores blocks u₀, u₁, ... looking for space; cases: (1) finds a non-full block in r+1 ≤ b steps and shifts r elements between blocks; (2) runs off the end of the list of blocks and creates a new block; (3) after b steps all have b+1 elements: `spread` creates a block and redistributes the b(b+1) elements to leave b in each `[from source] (ODS p.83-85)`.
- `remove(i)` is symmetric (borrows from neighboring blocks; in case 3, `gather` joins b(b−1) elements into b−1 blocks and removes an empty block) `[from source] (ODS p.85-87)`.
- Time: cases 1 and 2 cost O(b) and case 3 costs O(b²), but it occurs in at most one out of every b operations. **Lemma 3.1** (potential = number of fragile nodes): m operations spend O(bm) in `spread`/`gather` `[from source] (ODS p.85, 87-89)`.
- **Theorem 3.3**: get/set O(1+min{i, n−i}/b); add/remove O(b+min{i, n−i}/b) ignoring spread/gather; O(bm) in total in them; space `n + O(b + n/b)` `[from source] (ODS p.89)`.
- Trade-off: b = 2 approaches a DLList (up to three values per node); b > n is equivalent to a single array (ArrayList) `[from source] (ODS p.89-90)`.
- `[inference]` With b ≈ √n, O(b + min{i, n−i}/b) becomes O(√n) for add/remove. The book only states the approach to the space bound (p.81).
- Variant: SEList is also called an "unrolled linked list"; XOR-lists save one pointer per node, but do not work in garbage-collected languages such as Java and Python `[from source] (ODS p.90)`.
