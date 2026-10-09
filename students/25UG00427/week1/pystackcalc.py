"""PyStackCalc - a stack-based calculator (infix -> postfix -> evaluate)."""

import re

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOCIATIVE = {"^"}  # 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2) = 512


# ---------------------------------------------------------------- Step 1
class Stack:
    """LIFO stack backed by a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return list(self._items)


# ---------------------------------------------------------------- Step 2
def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens


# ---------------------------------------------------------------- helpers
def is_number(token: str) -> bool:
    return re.fullmatch(r"-?\d+(?:\.\d+)?", token) is not None


def is_variable(token: str) -> bool:
    return re.fullmatch(r"[a-zA-Z_]\w*", token) is not None


def merge_unary_minus(tokens: list[str]) -> list[str]:
    """Turn a leading '-' (start, after an operator, or after '(') into part
    of the following number, so '-3 + 2' and '2 * -3' work."""
    result = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        prev = result[-1] if result else None
        if (tok == "-" and (prev is None or prev in PRECEDENCE or prev == "(")
                and i + 1 < len(tokens) and is_number(tokens[i + 1])):
            result.append("-" + tokens[i + 1])
            i += 2
        else:
            result.append(tok)
            i += 1
    return result


# ---------------------------------------------------------------- Step 3
def infix_to_postfix(tokens: list[str]) -> list[str]:
    """Shunting-Yard algorithm."""
    tokens = merge_unary_minus(tokens)
    output = []
    ops = Stack()

    for tok in tokens:
        if is_number(tok) or is_variable(tok):
            output.append(tok)
        elif tok in PRECEDENCE:
            while (not ops.is_empty() and ops.peek() in PRECEDENCE and
                   (PRECEDENCE[ops.peek()] > PRECEDENCE[tok] or
                    (PRECEDENCE[ops.peek()] == PRECEDENCE[tok]
                     and tok not in RIGHT_ASSOCIATIVE))):
                output.append(ops.pop())
            ops.push(tok)
        elif tok == "(":
            ops.push(tok)
        elif tok == ")":
            while not ops.is_empty() and ops.peek() != "(":
                output.append(ops.pop())
            if ops.is_empty():
                raise ValueError("Mismatched parentheses: missing '('")
            ops.pop()  # discard the '('
        else:
            raise ValueError(f"Unexpected token: {tok}")

    while not ops.is_empty():
        top = ops.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses: missing ')'")
        output.append(top)

    return output


# ---------------------------------------------------------------- Step 4
def eval_postfix(postfix: list[str], variables: dict):
    stack = Stack()

    for tok in postfix:
        if is_number(tok):
            stack.push(float(tok) if "." in tok else int(tok))
        elif tok in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Invalid expression: missing operand")
            b = stack.pop()
            a = stack.pop()
            if tok == "+":
                stack.push(a + b)
            elif tok == "-":
                stack.push(a - b)
            elif tok == "*":
                stack.push(a * b)
            elif tok == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.push(a / b)
            elif tok == "%":
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero")
                stack.push(a % b)
            elif tok == "^":
                stack.push(a ** b)
        elif is_variable(tok):
            if tok not in variables:
                raise ValueError(f"Undefined variable: {tok}")
            stack.push(variables[tok])
        else:
            raise ValueError(f"Unexpected token: {tok}")

    if stack.size() != 1:
        raise ValueError("Invalid expression")
    return stack.pop()


# ---------------------------------------------------------------- Step 5
class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def evaluate(self, expr: str):
        tokens = tokenize(expr)
        return eval_postfix(infix_to_postfix(tokens), self.variables)

    def _set_variable(self, name: str, value):
        self.undo_stack.push(dict(self.variables))  # snapshot before change
        self.redo_stack = Stack()                   # new change clears redo
        self.variables[name] = value

    def undo(self):
        if self.undo_stack.is_empty():
            raise ValueError("Nothing to undo")
        self.redo_stack.push(dict(self.variables))
        self.variables = self.undo_stack.pop()

    def redo(self):
        if self.redo_stack.is_empty():
            raise ValueError("Nothing to redo")
        self.undo_stack.push(dict(self.variables))
        self.variables = self.redo_stack.pop()

    def execute(self, line: str):
        line = line.strip()
        command = line.lower()

        if command == "undo":
            self.undo()
            return None
        if command == "redo":
            self.redo()
            return None

        tokens = tokenize(line)
        if tokens[0] == "let":          # optional 'let' keyword
            tokens = tokens[1:]

        # assignment:  x = <expression>
        if len(tokens) >= 3 and is_variable(tokens[0]) and tokens[1] == "=":
            name = tokens[0]
            value = eval_postfix(infix_to_postfix(tokens[2:]), self.variables)
            self._set_variable(name, value)
            return value

        return eval_postfix(infix_to_postfix(tokens), self.variables)

    def start_repl(self):
        print("PyStackCalc - type an expression, 'let x = 5', 'undo', "
              "'redo', or 'quit'.")
        while True:
            try:
                line = input("calc> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if line.strip().lower() in ("quit", "exit"):
                break
            if not line.strip():
                continue
            try:
                result = self.execute(line)
                if result is not None:
                    print(result)
            except (ValueError, ZeroDivisionError, IndexError) as err:
                print(f"Error: {err}")


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
