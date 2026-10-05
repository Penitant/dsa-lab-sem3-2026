---
title: Linked Lists
week: 2
category: Linked Lists
start: 2026-09-25
end: 2026-10-11
---

## Submission

1. Create your folder: `students/<registration-no>/week2/` (e.g. `students/24UG00388/week2/`).
2. Save each question as a separate file: `q1.py`, `q2.py`, `q3.py`, and `hots.py` (optional).
3. Open a pull request from your fork to `main` on or before **11 Oct 2026**. Touch only your own folder.

> [!NOTE]
> Use of AI tools cannot be technically restricted. However, these exercises are designed to build algorithmic thinking, which develops only through working the problems yourself. You are strongly encouraged to attempt them without AI assistance.


Use the `Node` and `LL` classes from the slides (`Element`, `next`, `Head`).

```python
class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None

class LL:
    def __init__(self):
        self.Head = None
```

---

## Q1. Build the List (Easy)

*Estimated time: ~15 min*

Add the following methods to the `LL` class:

- `add_element(x)` – insert `x` at the head
- `append(x)` – insert `x` at the tail
- `print_list()` – print all elements in order
- `length()` – return the number of nodes
- `count(x)` – return how many times `x` appears
- `find_max()` – return the largest element (`None` if the list is empty)
- `get_nth(n)` – return the element at position `n` (0-indexed); print an error if `n` is out of range

**Test case**

```python
L = LL()
L.append(4); L.append(9); L.append(4); L.append(1)
L.print_list()
print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
L.get_nth(10)
```

**Output**

```
4 9 4 1
4 2 9 4
Index out of range
```

---

## Q2. Search and Delete (Medium)

*Estimated time: ~15 min*

Add these methods to `LL`:

- `search(x)` – return the position (0-indexed) of the first occurrence of `x`, or `-1` if it is not found
- `delete_element(x)` – delete **all** occurrences of `x` (including at the head and in a row)

**Test case**

```python
# L = 1 -> 1 -> 2 -> 1 -> 3
print(L.search(2))
print(L.search(5))
L.delete_element(1)
L.print_list()
```

**Output**

```
2
-1
2 3
```

**Edge case:** deleting `7` from `7 -> 7` should leave an empty list.

---

## Q3. Merge Two Sorted Lists (Hard)

*Estimated time: ~20 min*

Write a function `merge_sorted(L1, L2)` that takes two **sorted** linked lists and returns a new sorted `LL` containing all elements of both.

Do this by walking through both lists and linking nodes. Do **not** copy the elements into a Python list and use `sort()`.

**Test case**

```python
# L1 = 1 -> 4 -> 7
# L2 = 2 -> 3 -> 8
M = merge_sorted(L1, L2)
M.print_list()
```

**Output**

```
1 2 3 4 7 8
```

**Edge case:** merging an empty list with `5 -> 6` gives `5 6`.

---

## Happy Hacking ^_^ (Optional, HOTS)

*Estimated time: ~45 min. This question is **not mandatory** and does not affect your submission or attendance.*

### Big Integer Arithmetic using Linked Lists

Python handles big integers for you, but many languages don't. Store a large number as a linked list with **one digit per node**, least significant digit first.

Example: `9134` is stored as `4 -> 3 -> 1 -> 9`

Implement:

- `from_string(s)` – build the list from a number string
- `to_string()` – convert the list back to a number string
- `add(A, B)` **and/or** `subtract(A, B)` – return a new list holding the result

**Constraints**

- Both numbers are non-negative with at most 100 digits.
- For subtraction, assume `A >= B`.
- No leading zeros in input or output (except `"0"` itself).
- You may use `int(ch)` on a single digit, but **do not** convert the whole number to a Python `int`.

**Test cases**

| Operation | Output |
|---|---|
| `"999999999999" + "1"` | `1000000000000` |
| `"12345" + "678"` | `13023` |
| `"1000" - "999"` | `1` |
| `"500" - "500"` | `0` |
