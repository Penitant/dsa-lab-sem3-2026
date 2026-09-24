---
title: PyStackCalc — Terminal Expression Engine & Interactive REPL
week: 1
category: Stacks
start: 2026-09-18
end: 2026-09-28
---

# Project Assignment: PyStackCalc — Terminal Expression Engine & Interactive REPL

**Course:** ECS 25 — Introduction to Computer Science & Data Structures  
**Topic:** Stacks, Infix-to-Postfix (Shunting-Yard Algorithm), Reverse Polish Notation (RPN), and State History  
**Language:** Python 3 (Standard Library only)
**Deliverables to Create & Submit:** `pystackcalc.py`
**Total Points:** 100 Points (+ 15 Bonus Points)

---

## 1. Project Overview & Motivation

When you type an equation like `(3 + 4) * 2 - 8 / 4` into Google, a Python script, or a scientific calculator, how does the machine evaluate it correctly?

Humans rely on grade-school conventions (**PEMDAS / BODMAS**):

1. **P**arentheses first
2. **E**xponents next
3. **M**ultiplication and **D**ivision (left-to-right)
4. **A**ddition and **S**ubtraction (left-to-right)

However, computers read strings of text sequentially, one character or token at a time. If a computer naively reads `2 + 3 * 4` from left to right, it might compute `(2 + 3) = 5`, then `5 * 4 = 20` (**incorrect!** The true answer is `14`).

To solve this, the renowned Dutch computer scientist **Edsger Dijkstra** invented the **Shunting-Yard Algorithm** in 1961. This algorithm translates human **Infix** expressions into **Postfix (Reverse Polish Notation — RPN)** using a **Stack**. In Postfix, operators appear _after_ their operands (e.g., `2 3 4 * +`), completely eliminating the need for parentheses and allowing linear $O(N)$ evaluation!

In this project, you will build and master **`PyStackCalc`** from the ground up: a complete terminal-based calculator engine that converts Infix expressions to Postfix, evaluates them using an operand stack, stores variables, provides terminal trace diagnostics, and implements dual-stack **Undo/Redo** functionality.

---

## 2. Learning Objectives

By completing this assignment, you will:

- Implement and manipulate the foundational **Stack (LIFO — Last-In, First-Out)** data structure from a clean slate.
- Master regular expression tokenization for parsing numbers, identifiers, and math symbols.
- Implement **Dijkstra's Shunting-Yard Algorithm** with operator precedence, associativity, and syntax validation.
- Implement an **RPN Postfix Evaluator** using an operand stack with proper error handling (division by zero, malformed input).
- Build a real-world **Variable Environment** and manage application state history using a **Dual-Stack (Undo / Redo)** model.
- Write and run unit tests to verify the correctness of each milestone.

---

## 3. Deliverables & Required File Structure

You will create the following file:

- **`pystackcalc.py`**: The primary executable file containing your `Stack` class, tokenizer, Shunting-Yard converter, evaluator, REPL, and self-test suite.

### Expected Code Organization

| Component to Implement                               | Purpose                                                                                     |
| :--------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| `class Stack`                                        | LIFO collection supporting $O(1)$ `push`, `pop`, `peek`, `is_empty`, `size`, and `to_list`. |
| `def tokenize(expr)`                                 | Regex-based lexical scanner that splits raw strings into meaningful tokens.                 |
| `PRECEDENCE`, `RIGHT_ASSOCIATIVE`                    | Precedence dictionary and right-associativity set defining operator priority.               |
| `def infix_to_postfix(tokens)`                       | Shunting-Yard converter turning Infix token lists into RPN Postfix lists.                   |
| `def eval_postfix(postfix_tokens, variables, trace)` | Evaluates Postfix tokens using a stack; optionally prints formatted terminal traces.        |
| `class PyStackCalc`                                  | REPL engine managing variables, history, and dual-stack Undo/Redo.                          |
| `def run_tests()`                                    | Self-contained test harness to verify your code against all milestone requirements.         |

---

## 4. Detailed Milestone Specifications

### Milestone 1: The LIFO Stack Class (`Stack`) — 15 Points

A Stack is an abstract data type that serves as a collection of elements with two principal operations:

- **`push(item)`**: Adds an element to the top of the stack ($O(1)$).
- **`pop()`**: Removes and returns the most recently added element ($O(1)$). If the stack is empty, raises an `IndexError("Pop attempted on an empty stack")`.

#### Required Methods:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item): ...
    def pop(self): ...
    def peek(self): ...         # Returns top element without removing it; None if empty
    def is_empty(self) -> bool: ... # True if empty, False otherwise
    def size(self) -> int: ...  # Number of elements currently in the stack
    def to_list(self) -> list: ... # Returns shallow copy of items (bottom to top)
```

---

### Milestone 2: Lexical Tokenizer (`tokenize`) — 15 Points

Before mathematical operations can be organized, raw user input like `" (3 + 4.5) * x "` must be broken down into discrete tokens:

- **Floating-point & Integer Numbers:** `\d+(?:\.\d+)?` (e.g., `42`, `3.14159`)
- **Identifiers / Variables:** `[a-zA-Z_]\w*` (e.g., `x`, `radius`, `let`, `pi`)
- **Operators & Delimiters:** `[\+\-\*\/\^\%\(\)=]` (e.g., `+`, `-`, `*`, `/`, `^`, `%`, `(`, `)`, `=`)

```python
def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens
```

_Example:_  
`tokenize("let area = pi * r ^ 2")` $\rightarrow$ `['let', 'area', '=', 'pi', '*', 'r', '^', '2']`

---

### Milestone 3: Dijkstra's Shunting-Yard Algorithm (`infix_to_postfix`) — 25 Points

Convert an infix expression into Postfix (RPN).

#### Precedence & Associativity Table:

|       Operator       | Symbol |   Precedence    |   Associativity   |                    Example                    |
| :------------------: | :----: | :-------------: | :---------------: | :-------------------------------------------: |
| **Power / Exponent** |  `^`   | **3** (Highest) | **Right-to-Left** | `2 ^ 3 ^ 2` $\rightarrow$ `2 ^ (3 ^ 2) = 512` |
|  **Multiplication**  |  `*`   |      **2**      |   Left-to-Right   |                    `4 * 3`                    |
|     **Division**     |  `/`   |      **2**      |   Left-to-Right   |        `16 / 4 / 2 = (16 / 4) / 2 = 2`        |
|      **Modulo**      |  `%`   |      **2**      |   Left-to-Right   |                 `10 % 3 = 1`                  |
|     **Addition**     |  `+`   |      **1**      |   Left-to-Right   |                   `10 + 2`                    |
|   **Subtraction**    |  `-`   | **1** (Lowest)  |   Left-to-Right   |                   `10 - 2`                    |

#### The Shunting-Yard Rules:

1. **Operands (Numbers & Identifiers):** Append directly to the output queue.
2. **Left Parenthesis `(`:** Push onto the operator stack.
3. **Right Parenthesis `)`:** Pop operators from the stack to the output queue until a matching `(` is at the top. Pop and discard the `(`. If the stack empties without finding a `(`, raise `ValueError("Syntax Error: Mismatched parentheses (extra ')')")`.
4. **Operators ($op_1$):**
   While there is an operator $op_2$ at the top of the stack (and $op_2 \neq `(`$), check:
   - If $op_2$ has strictly greater precedence than $op_1$, **OR**
   - If $op_2$ has equal precedence and $op_1$ is **Left-Associative**:
     Pop $op_2$ from the stack to output.
   - Otherwise, break.
     Then push $op_1$ onto the stack.
5. **End of Input:** Pop all remaining operators from the stack to the output queue. If any unclosed `(` or `)` remains, raise `ValueError("Syntax Error: Mismatched parentheses (unclosed '(')")`.

---

### Milestone 4: Postfix Expression Evaluator (`eval_postfix`) — 20 Points

Evaluate the RPN token list using an operand stack.

```python
def eval_postfix(postfix_tokens, variables=None, trace=False) -> float | int:
```

#### Evaluation Steps:

1. For each token in `postfix_tokens`:
   - If it is a **number**, parse as `int` or `float` and push onto `operand_stack`.
   - If it is a **variable identifier**, look it up in `variables` dict. If not found, raise `NameError(f"Undefined variable: '{token}'")`. Push value onto `operand_stack`.
   - If it is an **operator**:
     - Check if `operand_stack.size() < 2`. If so, raise `ValueError`.
     - Pop top item as **$b$** (second operand).
     - Pop next item as **$a$** (first operand).
     - Compute $res = a \text{ op } b$.
     - If dividing by zero ($b = 0$ on `/`), raise `ZeroDivisionError("Math Error: Division by zero")`.
     - Push $res$ back onto `operand_stack`.
2. After processing all tokens:
   - If `operand_stack.size() == 1`, return the final popped value.
   - If `operand_stack.size() != 1`, raise `ValueError("Malformed expression: multiple values remain on stack")`.

#### Trace Mode Diagnostics (`trace=True`):

When `trace=True` is passed, print a formatted table showing every token processed, action performed, and the stack's state at each step.

---

### Milestone 5: Variables & Dual-Stack Undo/Redo (`PyStackCalc`) — 15 Points

Calculators and code editors maintain state through history stacks.

```python
class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()  # Stores historical snapshots of self.variables
        self.redo_stack = Stack()  # Stores undone snapshots
        self.history = []
```

#### Dual-Stack State Machine Mechanics:

1. **Assignment (`let x = <expr>` or `x = <expr>`):**
   - Before modifying `self.variables`, push a copy of current variables `dict(self.variables)` onto `undo_stack`.
   - Clear `redo_stack` (a new branch of history invalidates redo actions).
   - Evaluate `<expr>` and set `self.variables[var_name] = result`.
2. **`undo` command:**
   - If `undo_stack.is_empty()`, return `"Nothing to undo."`
   - Push current state `dict(self.variables)` onto `redo_stack`.
   - Pop previous state from `undo_stack` and restore `self.variables`.
3. **`redo` command:**
   - If `redo_stack.is_empty()`, return `"Nothing to redo."`
   - Push current state `dict(self.variables)` onto `undo_stack`.
   - Pop undone state from `redo_stack` and restore `self.variables`.

---

### Milestone 6: Interactive Terminal REPL — 10 Points

The Read-Eval-Print-Loop provides a clean terminal interface:

```bash
$ python pystackcalc.py

=======================================================
  🥞 PyStackCalc Interactive Math REPL (Python 3)
  Commands: let x = 10, vars, history, undo, redo, trace <expr>, exit
=======================================================
stack-calc> (3 + 4) * 2 - 8 / 4
=> 12
stack-calc> let radius = 5
=> radius = 5
stack-calc> pi * radius ^ 2
=> 78.53975
stack-calc> trace 2 ^ 3 ^ 2
=================================================================
TOKEN    | ACTION / STEP              | STACK STATE
-----------------------------------------------------------------
2        | Push operand               | [2]
3        | Push operand               | [2, 3]
2        | Push operand               | [2, 3, 2]
^        | Apply 3 ^ 2 = 9            | [2, 9]
^        | Apply 2 ^ 9 = 512          | [512]
=================================================================
=> 512
stack-calc> undo
=> Undone! Active variables: {'pi': 3.14159, 'e': 2.71828}
stack-calc> exit
Exiting PyStackCalc. Happy coding!
```

---

## 5. Verification & Testing

Since you are writing this project from scratch, add the following self-contained test function to the bottom of your `pystackcalc.py`. This will allow you to test your progress after every milestone!

```python
def run_tests():
    """Automated unit tests validating all core assignment milestones."""
    print("Testing PyStackCalc Assignment Suite...")
    engine = PyStackCalc()

    # Milestone 3 & 4: Infix Precedence & Arithmetic
    assert engine.execute("3 + 4 * 2") == 11, "Failed: Operator precedence"
    assert engine.execute("(3 + 4) * 2") == 14, "Failed: Parentheses grouping"
    assert engine.execute("2 ^ 3 ^ 2") == 512, "Failed: Right-associative exponentiation"
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12, "Failed: Mixed arithmetic"

    # Milestone 5: Variable Assignment & Resolution
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")
    assert engine.variables["y"] == 20, "Failed: Variable assignment"

    # Milestone 5: Dual-Stack Undo / Redo
    engine.execute("undo")
    assert "y" not in engine.variables, "Failed: Undo variable rollback"
    engine.execute("redo")
    assert engine.variables["y"] == 20, "Failed: Redo variable restoration"

    # Error Handling: Unclosed Parentheses
    try:
        engine.execute("(3 + 4 * 2")
        assert False, "Failed to catch unclosed parenthesis"
    except ValueError:
        pass

    # Error Handling: Division by Zero
    try:
        engine.execute("100 / (4 - 4)")
        assert False, "Failed to catch division by zero"
    except ZeroDivisionError:
        pass

    print("SUCCESS: All 9 milestone unit tests passed! Score: 100/100")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()
```

Run your automated test suite in terminal:

```bash
python pystackcalc.py --test
```

### Expected Output:

```
Testing PyStackCalc Assignment Suite...
SUCCESS: All 9 milestone unit tests passed! Score: 100/100
```

---

## 6. Grading Rubric (100 Points Total)

| Milestone       | Description                                                                                  |   Points    |
| :-------------- | :------------------------------------------------------------------------------------------- | :---------: |
| **Milestone 1** | Stack implementation (`push`, `pop`, `peek`, `is_empty`, `size`, `IndexError` on empty pop)  | **15 pts**  |
| **Milestone 2** | Regex tokenization of numbers, floats, variables, operators, and parentheses                 | **15 pts**  |
| **Milestone 3** | Shunting-Yard Infix-to-Postfix conversion with correct precedence & associativity            | **25 pts**  |
| **Milestone 4** | Postfix RPN evaluation with operand stack, variable lookup, and `ZeroDivisionError` handling | **20 pts**  |
| **Milestone 5** | Variable assignment (`let x = ...`) and Dual-Stack Undo / Redo mechanics                     | **15 pts**  |
| **Milestone 6** | Interactive Terminal REPL, trace display table, and command handling                         | **10 pts**  |
| **Total**       |                                                                                              | **100 pts** |

---

## 7. Bonus / Extension Challenges (+15 Points)

If you complete the core requirements and want to challenge yourself further:

1. **Unary Minus Support (+5 pts):**  
   Distinguish between binary subtraction (`5 - 3`) and unary negation (`-5 + 3` or `4 * -2`). Handle unary minus by converting it to a special operator token (e.g., `NEG` with higher precedence) or prepending a `0` operand.

2. **Built-in Functions (+5 pts):**  
   Support single-argument mathematical functions like `sqrt(16)`, `abs(-5)`, `sin(pi / 2)`, and `floor(3.8)`.

3. **Prefix (Polish Notation) Output (+5 pts):**  
   Add a command `prefix <expr>` that converts an infix expression to Polish Notation using the 3-step reversal algorithm:
   1. Reverse the tokens and swap `(` $\leftrightarrow$ `)`.
   2. Run Shunting-Yard.
   3. Reverse the resulting output tokens.

---

## 8. Common Pitfalls & Debugging Tips

- **Popping Order in Non-Commutative Operations:**  
  When an operator like `-` or `/` pops two operands from the stack:
  ```python
  b = operand_stack.pop() # Top element is SECOND operand!
  a = operand_stack.pop() # Next element is FIRST operand!
  result = a - b          # NOT b - a!
  ```
- **Right-Associativity of Exponents (`^`):**  
  In Shunting-Yard, when comparing an exponent operator against a top operator of equal precedence:
  ```python
  # Notice: strict '>' for right-associative, '>=' for left-associative!
  if PRECEDENCE[top] > PRECEDENCE[token] or (
      PRECEDENCE[top] == PRECEDENCE[token] and token not in RIGHT_ASSOCIATIVE
  ):
      output.append(op_stack.pop())
  ```
- **Parentheses Never Enter Output:**  
  Parentheses are discarded during Shunting-Yard. If a `(` or `)` ever appears in your postfix output, your matching logic has a bug.
- **Deep Copies for State Snapshots:**  
  When saving states to `self.undo_stack`, ensure you push a new copy (`dict(self.variables)`), not a reference to the mutable dictionary.
