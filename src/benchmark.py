"""Compare the cost of add_task for HeapScheduler vs SortedListScheduler.

For each size n we pre-fill a scheduler with n tasks, then time how long
it takes to add a batch of extra tasks. Reporting time PER ADD at a given
queue size isolates the insertion cost from the cost of building the queue.

Run:  python src/benchmark.py
"""

import random
import timeit

from task import Task
from heap_scheduler import HeapScheduler
from sorted_list_scheduler import SortedListScheduler

SIZES = [1_000, 10_000, 100_000, 1_000_000]
BATCH = 1_000      # extra tasks added on top of the pre-filled queue
REPEATS = 5        # best-of-5 to reduce noise


def prefilled(cls, n, rng):
    # Bulk build so setup stays fast; only the adds below are timed.
    return cls.from_tasks(Task(f"t{i}", rng.randint(1, 1_000_000)) for i in range(n))


def time_adds(cls, n):
    rng = random.Random(7)
    extra = [Task(f"x{i}", rng.randint(1, 1_000_000)) for i in range(BATCH)]
    best = float("inf")
    for _ in range(REPEATS):
        s = prefilled(cls, n, random.Random(1))
        start = timeit.default_timer()
        for t in extra:
            s.add_task(t)
        best = min(best, timeit.default_timer() - start)
    return best / BATCH * 1e6   # microseconds per add


def main():
    rows = []
    print(f"{'queue size':>12} | {'heapq (us/add)':>15} | {'sorted list (us/add)':>21} | {'list / heap':>11}")
    print("-" * 70)
    for n in SIZES:
        h = time_adds(HeapScheduler, n)
        s = time_adds(SortedListScheduler, n)
        rows.append((n, h, s))
        print(f"{n:>12,} | {h:>15.3f} | {s:>21.3f} | {s / h:>10.1f}x")
    return rows


if __name__ == "__main__":
    main()
