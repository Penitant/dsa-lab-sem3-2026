---
title: PyStackCalc — Build Your Own Terminal Calculator
week: 1
category: Stacks
start: 2026-09-18
end: 2026-10-11
---

**File to Submit:** `pystackcalc.py`
**Language:** Python 3 (built-in standard library only)
**Run Tests:** `python pystackcalc.py --test`

---

## Submission

1. Create your folder: `students/<registration-no>/week1/` (e.g. `students/24UG00388/week1/`).
2. Save your code as `pystackcalc.py`.
3. Open a pull request from your fork to `main` on or before **11 Oct 2026**. Touch only your own folder.

---

## 💡 A Quick Note Before You Begin

> Building a working calculator from scratch is a classic Computer Science milestone. It might sound intimidating, but it is **under 150 lines of Python** broken into simple, bite-sized functions.
>
> You might be tempted to feed this prompt to an AI, but doing it yourself will give you a real "aha!" moment when your own code correctly solves `(3 + 4) * 2 - 8 / 4`. Follow the 4 steps below, test each part as you go, and you'll have it running in no time!

---

## The Big Picture: How Computers Do Math

Humans write math in **Infix** notation (`2 + 3 * 4`). We pause and look ahead because we know multiplication has higher priority than addition.

A computer, however, reads text from left to right. To make math easy for a computer, we convert it to **Postfix** (also called *Reverse Polish Notation* or RPN):

$$\text{Infix: } (3 + 4) \times 2 \quad \longrightarrow \quad \text{Postfix: } 3 \ 4 \ + \ 2 \ \times$$

In Postfix, **operators come after their numbers**. There are **no parentheses**, and the computer can evaluate the entire expression in a single pass using a **Stack**!

---

## What to Build (Step by Step)

All your code goes inside `pystackcalc.py`.

### Step 1: The Stack Class (`Stack`)
A Stack is a simple container where the **last item added is the first item removed** (LIFO: Last-In, First-Out), like a stack of plates.

Implement a class `Stack` using a standard Python list:
- `push(item)`: Append `item` to the top.
- `pop()`: Remove and return the top item. Raise `IndexError` if the stack is empty.
- `peek()`: Return the top item without removing it (or `None` if empty).
- `is_empty()`: Return `True` if empty, else `False`.
- `size()`: Return the number of items.
- `to_list()`: Return a copy of the items as a list.

---

### Step 2: The Tokenizer (`tokenize`)
Before evaluating an expression, split the raw text into distinct pieces (numbers, variable names, operators, parentheses):

```python
import re

def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens
```

*Example:* `tokenize("(3 + 4) * 2")` $\rightarrow$ `['(', '3', '+', '4', ')', '*', '2']`

---

### Step 3: Infix to Postfix (`infix_to_postfix`)
Use **Dijkstra's Shunting-Yard Algorithm** with an operator stack:

1. **Operator Precedence:**
   ```python
   PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
   RIGHT_ASSOCIATIVE = {"^"}  # 2 ^ 3 ^ 2 evaluates right-to-left: 2 ^ (3 ^ 2) = 512
   ```
2. **Loop through each token:**
   - **Number or Variable name:** Append directly to output list.
   - **Operator ($op_1$):** While the top of the stack has an operator ($op_2$) with:
     - Higher precedence, **or**
     - Equal precedence and $op_1$ is Left-associative:  
     Pop $op_2$ to the output list. Then push $op_1$ to the stack.
   - **`(`:** Push to the stack.
   - **`)`:** Pop from stack to output until you see `(`. Pop and discard `(`. (If stack empties without finding `(`, raise `ValueError`).
3. **End of input:** Pop all remaining operators to output. (If any `(` remains, raise `ValueError`).

---

### Step 4: Postfix Evaluator (`eval_postfix`)
Evaluate the postfix list using an operand stack:

1. For each token:
   - **Number:** Push its numeric value (`int` or `float`) onto the stack.
   - **Variable:** Look it up in `variables` dictionary and push its value.
   - **Operator:** Pop two values ($b = \text{pop()}$, then $a = \text{pop()}$). Compute $a \text{ op } b$ and push the result back!
     *(Check for division by zero: if $b == 0$ on `/`, raise `ZeroDivisionError`).*
2. When finished, the stack should contain exactly one number: your final answer!

---

### Step 5: Calculator Engine & REPL (`PyStackCalc`)
Wrap the components into a `PyStackCalc` class:
- Maintain a dictionary `self.variables = {"pi": 3.14159, "e": 2.71828}`.
- Support variable assignment: `let x = 15` or `x = 15`.
- **Undo / Redo (Dual Stack):**
  - Keep `self.undo_stack = Stack()` and `self.redo_stack = Stack()`.
  - When a variable changes, push a copy `dict(self.variables)` onto `undo_stack` and clear `redo_stack`.
  - Typing `undo` restores the previous snapshot; typing `redo` restores the undone state.
- Interactive terminal prompt (`calc.start_repl()`) when executed directly.

---

## 🧪 Test Cases (Self-Verification)

Add this test function to the bottom of your file. When you run `python pystackcalc.py --test`, all tests must pass:

```python
def run_tests():
    """Automated test cases to verify your implementation."""
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()

    # 1. Basic Precedence & Grouping
    assert engine.execute("3 + 4 * 2") == 11, "Test 1 Failed: Precedence (* before +)"
    assert engine.execute("(3 + 4) * 2") == 14, "Test 2 Failed: Parentheses grouping"
    assert engine.execute("2 ^ 3 ^ 2") == 512, "Test 3 Failed: Exponent right-associativity"
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12, "Test 4 Failed: Mixed arithmetic"

    # 2. Variables
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")
    assert engine.variables["y"] == 20, "Test 5 Failed: Variable calculation"

    # 3. Undo / Redo
    engine.execute("undo")
    assert "y" not in engine.variables, "Test 6 Failed: Undo should roll back variable y"
    engine.execute("redo")
    assert engine.variables["y"] == 20, "Test 7 Failed: Redo should restore variable y"

    # 4. Error Handling
    try:
        engine.execute("(3 + 4 * 2")  # Missing closing parenthesis
        assert False, "Test 8 Failed: Should raise ValueError for unclosed '('"
    except ValueError:
        pass

    try:
        engine.execute("100 / (4 - 4)")  # Division by zero
        assert False, "Test 9 Failed: Should raise ZeroDivisionError"
    except ZeroDivisionError:
        pass

    print("✅ All 9 test cases passed successfully!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()
```

---

## 🚀 Quick Run Commands

```bash
# Run automated tests to check your work:
python pystackcalc.py --test

# Launch the interactive terminal calculator:
python pystackcalc.py
```
