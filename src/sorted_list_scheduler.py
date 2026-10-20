"""Priority-queue scheduler backed by a sorted Python list.

The list is kept sorted so the NEXT task is always at the END,
which makes removal a cheap list.pop().

Key trick: store (-priority, -seq). Sorted ascending, the largest key
(smallest priority, earliest seq) ends up last.

add_task  -> O(n)  bisect finds the slot in O(log n), but insert() must
                   shift every element after it one position to the right
next_task -> O(1)  list.pop() from the end
peek      -> O(1)
"""

import bisect
from itertools import count

from task import Task


class SortedListScheduler:
    def __init__(self):
        self._items = []         # entries: (-priority, -seq, task)
        self._seq = count()

    @classmethod
    def from_tasks(cls, tasks):
        """Bulk build in O(n log n) with one sort (cheaper than n inserts)."""
        s = cls()
        s._items = [(-t.priority, -next(s._seq), t) for t in tasks]
        s._items.sort(key=lambda e: e[:2])
        return s

    def add_task(self, task: Task) -> None:
        entry = (-task.priority, -next(self._seq), task)
        # key= keeps bisect from ever comparing Task objects
        idx = bisect.bisect_left(self._items, entry[:2], key=lambda e: e[:2])
        self._items.insert(idx, entry)

    def next_task(self) -> Task:
        if not self._items:
            raise IndexError("next_task from empty scheduler")
        return self._items.pop()[2]

    def peek(self) -> Task:
        if not self._items:
            raise IndexError("peek from empty scheduler")
        return self._items[-1][2]

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)

    def run_all(self):
        while self._items:
            yield self.next_task()
