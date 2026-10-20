"""Priority-queue scheduler backed by a binary min-heap (heapq).

add_task  -> O(log n)  heappush sifts the new item up the tree
next_task -> O(log n)  heappop moves the last item to the root and sifts it down
peek      -> O(1)      the smallest key is always at index 0
"""

import heapq
from itertools import count

from task import Task


class HeapScheduler:
    def __init__(self):
        self._heap = []          # entries: (priority, seq, task)
        self._seq = count()      # tie-breaker -> FIFO among equal priorities

    @classmethod
    def from_tasks(cls, tasks):
        """Bulk build in O(n) with heapify (cheaper than n pushes)."""
        s = cls()
        s._heap = [(t.priority, next(s._seq), t) for t in tasks]
        heapq.heapify(s._heap)
        return s

    def add_task(self, task: Task) -> None:
        heapq.heappush(self._heap, (task.priority, next(self._seq), task))

    def next_task(self) -> Task:
        if not self._heap:
            raise IndexError("next_task from empty scheduler")
        return heapq.heappop(self._heap)[2]

    def peek(self) -> Task:
        if not self._heap:
            raise IndexError("peek from empty scheduler")
        return self._heap[0][2]

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def run_all(self):
        """Yield every task in priority order, emptying the scheduler."""
        while self._heap:
            yield self.next_task()
