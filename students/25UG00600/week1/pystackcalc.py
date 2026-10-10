import re


class Stack:
    """Simple LIFO stack backed by a Python list.
    Used for operators, values, and the undo/redo history."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)          # add on top

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()          # remove and return top

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]            # look at top without removing

    def is_empty(self):
        return len(self._items) == 0

    def clear(self):
        self._items.clear()

    def __len__(self):
        return len(self._items)


class PyStackCalc:
    # operator -> (precedence, is_right_associative)
    # higher precedence binds tighter; "u-" is unary minus
    OPS = {
        "+": (1, False),
        "-": (1, False),
        "*": (2, False),
        "/": (2, False),
        "u-": (3, True),
        "^": (4, True),    # right-assoc: 2^3^2 = 2^(3^2) = 512
    }
    # splits an expression into numbers, names and operators/parentheses
    TOKEN_RE = re.compile(r"\s*(\d+\.?\d*|\.\d+|[A-Za-z_]\w*|[-+*/^()])")
    # matches "let x = 15" or "x = 15"
    ASSIGN_RE = re.compile(r"^\s*(?:let\s+)?([A-Za-z_]\w*)\s*=\s*(.+)$")

    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}   # built-in constants
        self.undo_stack = Stack()   # earlier snapshots of self.variables
        self.redo_stack = Stack()   # snapshots that were undone

    # ---------- step 1: tokenizer ----------
    def tokenize(self, expr):
        """Turn a string like '3 + x*2' into ['3', '+', 'x', '*', '2']."""
        tokens, pos = [], 0
        expr = expr.rstrip()
        while pos < len(expr):
            m = self.TOKEN_RE.match(expr, pos)
            if not m:
                raise ValueError(f"Invalid character at position {pos}: {expr[pos:].strip()[0]!r}")
            tokens.append(m.group(1))
            pos = m.end()
        return tokens

    # ---------- step 2: shunting-yard (infix -> postfix) ----------
    def to_postfix(self, tokens):
        """Convert infix tokens to postfix (RPN) using an operator stack."""
        output = []
        ops = Stack()
        prev = None  # previous token, needed to tell unary '-' from binary '-'
        for tok in tokens:
            if re.fullmatch(r"\d+\.?\d*|\.\d+", tok) or re.fullmatch(r"[A-Za-z_]\w*", tok):
                output.append(tok)                     # numbers/variables go straight out
            elif tok == "(":
                ops.push(tok)
            elif tok == ")":
                # pop operators until the matching '('
                while not ops.is_empty() and ops.peek() != "(":
                    output.append(ops.pop())
                if ops.is_empty():
                    raise ValueError("Mismatched parentheses: unexpected ')'")
                ops.pop()                              # discard the '('
            else:
                # '-' at the start, after an operator, or after '(' is unary minus
                if tok == "-" and (prev is None or prev in self.OPS or prev == "("):
                    tok = "u-"
                if tok != "u-":   # a prefix operator never pops anything
                    prec, right = self.OPS[tok]
                    # pop operators that must run before this one
                    while (not ops.is_empty() and ops.peek() != "("
                           and (self.OPS[ops.peek()][0] > prec
                                or (self.OPS[ops.peek()][0] == prec and not right))):
                        output.append(ops.pop())
                ops.push(tok)
            prev = tok
        # flush the remaining operators
        while not ops.is_empty():
            top = ops.pop()
            if top == "(":
                raise ValueError("Mismatched parentheses: missing ')'")
            output.append(top)
        return output

    # ---------- step 3: evaluate postfix ----------
    def eval_postfix(self, postfix):
        """Evaluate RPN using a value stack."""
        vals = Stack()
        for tok in postfix:
            if tok == "u-":
                if vals.is_empty():
                    raise ValueError("Invalid expression")
                vals.push(-vals.pop())
            elif tok in self.OPS:
                if len(vals) < 2:
                    raise ValueError("Invalid expression")
                b, a = vals.pop(), vals.pop()          # b is the right operand
                if tok == "+":
                    vals.push(a + b)
                elif tok == "-":
                    vals.push(a - b)
                elif tok == "*":
                    vals.push(a * b)
                elif tok == "/":
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    vals.push(a / b)
                elif tok == "^":
                    vals.push(a ** b)
            elif tok[0].isdigit() or tok[0] == ".":
                vals.push(float(tok) if "." in tok else int(tok))   # number literal
            else:
                if tok not in self.variables:
                    raise NameError(f"Undefined variable '{tok}'")
                vals.push(self.variables[tok])          # variable lookup
        if len(vals) != 1:
            raise ValueError("Invalid expression")
        return vals.pop()

    def evaluate(self, expr):
        """tokenize -> postfix -> evaluate."""
        return self.eval_postfix(self.to_postfix(self.tokenize(expr)))

    # ---------- undo / redo (dual stack) ----------
    def _set_variable(self, name, value):
        self.undo_stack.push(dict(self.variables))   # snapshot BEFORE the change
        self.redo_stack.clear()                      # a new change kills the redo history
        self.variables[name] = value

    def undo(self):
        if self.undo_stack.is_empty():
            return "Nothing to undo"
        self.redo_stack.push(dict(self.variables))   # save current state so redo can return to it
        self.variables = self.undo_stack.pop()       # restore previous snapshot
        return "Undo done"

    def redo(self):
        if self.redo_stack.is_empty():
            return "Nothing to redo"
        self.undo_stack.push(dict(self.variables))   # so we can undo the redo again
        self.variables = self.redo_stack.pop()       # restore the undone state
        return "Redo done"

    # ---------- main entry point ----------
    def execute(self, line):
        """Run one line: a command, an assignment, or an expression."""
        line = line.strip()
        if not line:
            return None
        cmd = line.lower()
        if cmd == "undo":
            return self.undo()
        if cmd == "redo":
            return self.redo()
        if cmd == "vars":
            return dict(self.variables)

        m = self.ASSIGN_RE.match(line)
        if m:                                        # "let x = ..." or "x = ..."
            name, expr = m.group(1), m.group(2)
            value = self.evaluate(expr)              # evaluate first so errors don't change state
            self._set_variable(name, value)
            return value
        return self.evaluate(line)                   # plain expression

    def start_repl(self):
        """Interactive prompt: type expressions until 'exit'."""
        print("PyStackCalc  |  commands: let x = 5, undo, redo, vars, exit")
        while True:
            try:
                line = input(">>> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if line.strip().lower() in ("exit", "quit"):
                break
            try:
                result = self.execute(line)
                if result is not None:
                    print(result)
            except (ValueError, ZeroDivisionError, NameError) as err:
                print(f"Error: {err}")        # show the error, keep the REPL running


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

    print("All 9 test cases passed successfully!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()
