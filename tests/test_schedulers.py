import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from task import Task  # noqa: E402
from heap_scheduler import HeapScheduler  # noqa: E402
from sorted_list_scheduler import SortedListScheduler  # noqa: E402

SCHEDULERS = [HeapScheduler, SortedListScheduler]


@pytest.fixture(params=SCHEDULERS, ids=lambda c: c.__name__)
def sched(request):
    return request.param()


def test_returns_tasks_in_priority_order(sched):
    for name, p in [("email", 3), ("deploy", 1), ("backup", 2), ("lint", 5)]:
        sched.add_task(Task(name, p))
    assert [t.name for t in sched.run_all()] == ["deploy", "backup", "email", "lint"]


def test_equal_priority_is_fifo(sched):
    for name in ["a", "b", "c"]:
        sched.add_task(Task(name, 2))
    sched.add_task(Task("urgent", 1))
    assert [t.name for t in sched.run_all()] == ["urgent", "a", "b", "c"]


def test_peek_does_not_remove(sched):
    sched.add_task(Task("x", 4))
    sched.add_task(Task("y", 1))
    assert sched.peek().name == "y"
    assert len(sched) == 2


def test_empty_raises(sched):
    assert not sched
    with pytest.raises(IndexError):
        sched.next_task()
    with pytest.raises(IndexError):
        sched.peek()


def test_interleaved_add_and_pop(sched):
    sched.add_task(Task("t5", 5))
    sched.add_task(Task("t2", 2))
    assert sched.next_task().name == "t2"
    sched.add_task(Task("t1", 1))
    sched.add_task(Task("t9", 9))
    assert [t.name for t in sched.run_all()] == ["t1", "t5", "t9"]


def test_both_implementations_agree_on_random_input():
    rng = random.Random(42)
    tasks = [Task(f"t{i}", rng.randint(1, 10)) for i in range(2000)]
    heap, lst = HeapScheduler(), SortedListScheduler()
    for t in tasks:
        heap.add_task(t)
        lst.add_task(t)
    assert list(heap.run_all()) == list(lst.run_all())


@pytest.mark.parametrize("cls", SCHEDULERS, ids=lambda c: c.__name__)
def test_from_tasks_matches_incremental_adds(cls):
    rng = random.Random(3)
    tasks = [Task(f"t{i}", rng.randint(1, 5)) for i in range(500)]
    bulk = cls.from_tasks(tasks)
    inc = cls()
    for t in tasks:
        inc.add_task(t)
    assert list(bulk.run_all()) == list(inc.run_all())


def test_invalid_task():
    with pytest.raises(TypeError):
        Task("bad", "high")
    with pytest.raises(ValueError):
        Task("", 1)
