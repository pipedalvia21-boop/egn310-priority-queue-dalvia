"""Run with:  python -m pytest -q"""

import pytest

import ticket_queue
import sorted_version

VERSIONS = [ticket_queue, sorted_version]

WORKED_EXAMPLE = [
    (2, 101, "Printer offline in Lab B"),
    (1, 102, "Payroll server down"),
    (3, 103, "New laptop setup"),
    (1, 104, "Email outage, whole floor"),
]


@pytest.fixture(params=VERSIONS, ids=["heap", "sorted"])
def mod(request):
    return request.param


def drain(mod, queue):
    out = []
    while (t := mod.next_ticket(queue)) is not None:
        out.append(t)
    return out


def test_worked_example_order(mod):
    q = []
    for t in WORKED_EXAMPLE:
        mod.add_ticket(q, *t)
    assert [t[1] for t in drain(mod, q)] == [102, 104, 101, 103]


def test_ties_come_out_in_arrival_order(mod):
    q = []
    for n in (201, 202, 203):
        mod.add_ticket(q, 2, n, "same priority")
    assert [t[1] for t in drain(mod, q)] == [201, 202, 203]


def test_empty_queue_returns_none(mod):
    q = []
    assert mod.next_ticket(q) is None
    mod.add_ticket(q, 1, 1, "x")
    mod.next_ticket(q)
    assert mod.next_ticket(q) is None


def test_pending_count(mod):
    q = []
    assert mod.pending_count(q) == 0
    mod.add_ticket(q, 3, 1, "a")
    mod.add_ticket(q, 1, 2, "b")
    assert mod.pending_count(q) == 2
    mod.next_ticket(q)
    assert mod.pending_count(q) == 1


@pytest.mark.parametrize("bad", [0, 4, -1, 99, "1", 1.5, True])
def test_out_of_range_priority_rejected(mod, bad):
    q = []
    with pytest.raises(ValueError) as exc:
        mod.add_ticket(q, bad, 1, "x")
    assert repr(bad) in str(exc.value)
    assert q == []


def test_versions_agree_on_csv(tmp_path):
    csv = tmp_path / "tickets.csv"
    csv.write_text(
        "priority,number,description\n"
        + "\n".join(f'{p},{n},"{d}"' for p, n, d in WORKED_EXAMPLE)
    )
    assert ticket_queue.main(csv) == sorted_version.main(csv)
