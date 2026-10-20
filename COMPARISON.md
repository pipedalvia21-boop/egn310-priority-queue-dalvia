# Comparison: heap vs sorted list

When there are 12 tickets in the queue and ticket number 13 arrives, the heap uses the `heappush()` function to insert it. First, it places the new ticket at the end of the heap. Then, it compares its value with its parent and swaps them if necessary until the ticket reaches its correct position. This process is called sift-up. The other 12 tickets do not need to be sorted again, although some may change positions during swaps.

In contrast, the sorted list uses two steps in `add_ticket`: first, `append()` adds the new ticket to the end of the list; then, `sort()` sorts all 13 tickets, not just the new one. This means the entire list is processed again to maintain the correct order.

In conclusion, the sorted list does more work because it runs `sort()` on every ticket after each insertion. The heap only performs the necessary comparisons and swaps to place the new element correctly. With 10,000 tickets, this difference becomes much more significant because repeatedly sorting the entire list has a higher computational cost than inserting elements into a heap.
