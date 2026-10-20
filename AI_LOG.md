# AI Log: Assignment 8.1

Tool: Claude (Anthropic), claude.ai, 2026-10-20.
AI was used for the code only, as permitted. COMPARISON.md was not written with AI.

## Prompts

1. "Priority queue task scheduler. Build a scheduler that returns tasks in priority order using heapq, then repeat the exercise with a sorted list and compare the cost of adding a task to each. Quiz 4 covering Modules 7 and 8 is due at the end of this module."
   - Claude built a general task scheduler (heap vs sorted list) with tests and a timing benchmark. This was later replaced to match the full assignment spec.
2. "ya esta todo hecho no?"
3. "subilo vos" / "subi el repo vos, ya tenes permisos" / "listo"
   - Claude pushed the repository to GitHub.
4. Pasted the full Assignment 8.1 instructions (help desk ticket queue).
   - Claude wrote ticket_queue.py, sorted_version.py and test_ticket_queue.py.

## What I checked myself

- Ran the worked example from the assignment through both versions and confirmed the output matches (102, 104, 101, 103).
- Ran the tests: empty queue returns None, priorities 0, 4, "1", 1.5 and True raise ValueError with the value in the message, ties come out in arrival order.
- Confirmed sorted_version.py prints MATCH against the heap version on tickets.csv.
