"""Same help desk queue, built on a plain list kept sorted.

add_ticket appends the new ticket and re-sorts the whole list.
next_ticket takes the ticket at the front (index 0).

Run:  python sorted_version.py   (should match ticket_queue.py exactly)
"""

import sys

from ticket_queue import DEFAULT_CSV, format_ticket, load_tickets, validate_priority
import ticket_queue


def add_ticket(queue, priority, number, description):
    """Append the ticket, then sort the entire list again."""
    validate_priority(priority)
    queue.append((priority, number, description))
    queue.sort()


def next_ticket(queue):
    """Remove and return the front ticket, or None if the queue is empty."""
    if not queue:
        return None
    return queue.pop(0)


def pending_count(queue):
    return len(queue)


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
    sorted_lines = main(csv_path)
    heap_lines = ticket_queue.main(csv_path)
    print("\n".join(sorted_lines))
    print()
    if sorted_lines == heap_lines:
        print(f"MATCH: identical to the heap version ({len(sorted_lines)} tickets)")
    else:
        print("MISMATCH: output differs from the heap version")
        sys.exit(1)
