"""Help desk ticket queue built on heapq.

Each ticket is a tuple (priority, number, description).
Priority 1 = emergency, 3 = routine. The unique ticket number breaks
ties, so two tickets with the same priority come out in arrival order
and Python never has to compare descriptions.

Run:  python ticket_queue.py  (prints the order tickets are worked)
"""

import csv
import heapq
import sys
from pathlib import Path

MIN_PRIORITY = 1
MAX_PRIORITY = 3
DEFAULT_CSV = Path(__file__).with_name("tickets.csv")


def validate_priority(priority):
    """Raise ValueError naming the bad value if priority is not 1-3."""
    if isinstance(priority, bool) or not isinstance(priority, int) \
            or not MIN_PRIORITY <= priority <= MAX_PRIORITY:
        raise ValueError(
            f"priority must be an integer from {MIN_PRIORITY} to "
            f"{MAX_PRIORITY}, got {priority!r}"
        )


def add_ticket(queue, priority, number, description):
    """Push a ticket onto the heap. heappush sifts it into place."""
    validate_priority(priority)
    heapq.heappush(queue, (priority, number, description))


def next_ticket(queue):
    """Pop and return the most urgent ticket, or None if the queue is empty."""
    if not queue:
        return None
    return heapq.heappop(queue)


def pending_count(queue):
    """Number of tickets still waiting."""
    return len(queue)


def load_tickets(path=DEFAULT_CSV):
    """Read tickets from a CSV in file order as (priority, number, description).

    Expects columns named priority, number (or ticket/ticket_number/id)
    and description. Falls back to column position if there is no header.
    """
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))

    header = [h.strip().lower() for h in rows[0]]
    if "priority" in header:
        def col(*names):
            for n in names:
                if n in header:
                    return header.index(n)
            raise KeyError(f"tickets.csv is missing a column like {names[0]!r}")
        p_i = col("priority")
        n_i = col("number", "ticket", "ticket_number", "ticket_no", "id")
        d_i = col("description", "issue", "summary")
        rows = rows[1:]
    else:
        p_i, n_i, d_i = 0, 1, 2

    return [
        (int(r[p_i]), int(r[n_i]), r[d_i].strip())
        for r in rows if any(cell.strip() for cell in r)
    ]


def format_ticket(ticket):
    priority, number, description = ticket
    return f"{priority} {number} {description}"


def main(path=DEFAULT_CSV):
    queue = []
    for priority, number, description in load_tickets(path):
        add_ticket(queue, priority, number, description)

    lines = []
    while (ticket := next_ticket(queue)) is not None:
        lines.append(format_ticket(ticket))
    return lines


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    print("\n".join(main(csv_path)))
