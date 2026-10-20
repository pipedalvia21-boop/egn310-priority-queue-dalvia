# Priority Queue Task Scheduler

EGN 310 — Data Structures · Felipe D'Alvia

A task scheduler that always returns the most urgent task next, built twice:
once on a binary heap (`heapq`) and once on a sorted list (`bisect`), then
benchmarked on the cost of adding a task.

**Convention:** lower priority number = runs first (1 is most urgent).
Tasks with equal priority run in the order they were added (FIFO), enforced
with an insertion counter as a tie-breaker.

## Structure

```
src/
  task.py                   Task dataclass (name, priority) with validation
  heap_scheduler.py         HeapScheduler: heapq min-heap
  sorted_list_scheduler.py  SortedListScheduler: list kept sorted with bisect
  benchmark.py              Times add_task at different queue sizes
tests/
  test_schedulers.py        14 tests run against BOTH implementations
```

## Usage

```python
from task import Task
from heap_scheduler import HeapScheduler

s = HeapScheduler()
s.add_task(Task("email report", 3))
s.add_task(Task("fix prod bug", 1))
s.add_task(Task("backup db", 2))

s.next_task().name   # 'fix prod bug'
[t.name for t in s.run_all()]   # ['backup db', 'email report']
```

`SortedListScheduler` has the identical interface: `add_task`, `next_task`,
`peek`, `run_all`, `len()`, plus `from_tasks()` for bulk loading.

## Run

```bash
pip install pytest
python -m pytest -q          # 14 passed
python src/benchmark.py
```

## Results: cost of adding one task

Each queue is pre-filled with *n* tasks, then 1,000 more are added and timed
(best of 5, microseconds per add).

| Queue size | heapq | Sorted list | Sorted list / heapq |
|-----------:|------:|------------:|--------------------:|
|      1,000 | 0.21 µs |   1.94 µs |   9× |
|     10,000 | 0.32 µs |   4.56 µs |  14× |
|    100,000 | 0.49 µs |  19.56 µs |  40× |
|  1,000,000 | 0.53 µs | 218.25 µs | 408× |

## Analysis

| Operation | heapq | Sorted list |
|-----------|-------|-------------|
| Add task  | **O(log n)** | **O(n)** |
| Next task | O(log n) | O(1) |
| Peek      | O(1) | O(1) |
| Bulk build| O(n) `heapify` | O(n log n) `sort` |

**Heap add is O(log n).** `heappush` appends to the end of the array and sifts
the item up toward the root; at most one swap per level of a tree with
log₂ n levels. Going from 1,000 to 1,000,000 tasks (1000× more) only took the
add from 0.21 µs to 0.53 µs, consistent with log₂ growing from ~10 to ~20.

**Sorted-list add is O(n).** `bisect` finds the correct slot in O(log n), but
`list.insert` must shift every element after that slot one position to the
right. With random priorities that is ~n/2 moves on average, so the cost grows
linearly: roughly 10× per 10× more tasks between 100k and 1M. At small sizes
the shift is a fast `memmove` in C, which is why the gap is only 9× at 1,000
tasks, but it widens to 408× at a million.

**The trade-off.** The sorted list wins on removal: the next task sits at the
end, so `pop()` is O(1) versus O(log n) for `heappop`. That only pays off when
tasks are added rarely and removed often. A scheduler typically receives tasks
continuously, so every task pays the add cost once and the heap is the better
choice. Python's own `queue.PriorityQueue` is built on `heapq` for this reason.

**Design note.** The sorted list stores `(-priority, -seq)` so the most urgent
task ends up at the end of the list; this is what makes `next_task` an O(1)
`pop()` instead of an O(n) `pop(0)`.
