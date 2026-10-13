import re

class Stack:
    """A LIFO stack implementation using a Python list."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)


def tokenize(expr: str) -> list[str]:
    """Split raw expression text into distinct tokens."""
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOCIATIVE = {"^"}


def infix_to_postfix(tokens: list[str]) -> list[str]:
    """Convert infix tokens to postfix notation using Dijkstra's Shunting-Yard algorithm."""
    output = []
    stack = Stack()

    for token in tokens:
        if re.match(r"^\d+(?:\.\d+)?$", token) or re.match(r"^[a-zA-Z_]\w*$", token):
            output.append(token)
        elif token in PRECEDENCE:
            while (not stack.is_empty() and 
                   stack.peek() in PRECEDENCE and 
                   (PRECEDENCE[stack.peek()] > PRECEDENCE[token] or 
                    (PRECEDENCE[stack.peek()] == PRECEDENCE[token] and token not in RIGHT_ASSOCIATIVE))):
                output.append(stack.pop())
            stack.push(token)
        elif token == "(":
            stack.push(token)
        elif token == ")":
            while not stack.is_empty() and stack.peek() != "(":
                output.append(stack.pop())
            if stack.is_empty():
                raise ValueError("Mismatched parentheses: missing '('")
            stack.pop()  # Discard '('
        else:
            raise ValueError(f"Unknown token: {token}")

    while not stack.is_empty():
        op = stack.pop()
        if op == "(":
            raise ValueError("Mismatched parentheses: missing ')'")
        output.append(op)

    return output


def eval_postfix(tokens: list[str], variables: dict):
    """Evaluate postfix tokens using an operand stack."""
    stack = Stack()

    for token in tokens:
        if re.match(r"^\d+(?:\.\d+)?$", token):
            val = float(token) if "." in token else int(token)
            stack.push(val)
        elif re.match(r"^[a-zA-Z_]\w*$", token):
            if token not in variables:
                raise NameError(f"Name '{token}' is not defined")
            stack.push(variables[token])
        elif token in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Invalid expression format")
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.push(a + b)
            elif token == "-":
                stack.push(a - b)
            elif token == "*":
                stack.push(a * b)
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                stack.push(a / b)
            elif token == "%":
                if b == 0:
                    raise ZeroDivisionError("modulo by zero")
                stack.push(a % b)
            elif token == "^":
                stack.push(a ** b)
        else:
            raise ValueError(f"Unexpected token in evaluation: {token}")

    if stack.size() != 1:
        raise ValueError("Invalid expression")
    return stack.pop()


class PyStackCalc:
    """Calculator engine managing variables, assignments, and undo/redo states."""
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def execute(self, expr: str):
        expr_stripped = expr.strip()
        if not expr_stripped:
            return None

        lower_expr = expr_stripped.lower()
        if lower_expr == "undo":
            if not self.undo_stack.is_empty():
                self.redo_stack.push(dict(self.variables))
                self.variables = self.undo_stack.pop()
            return None
        elif lower_expr == "redo":
            if not self.redo_stack.is_empty():
                self.undo_stack.push(dict(self.variables))
                self.variables = self.redo_stack.pop()
            return None

        # Check for variable assignment: e.g., let x = 15 or x = 15
        assign_match = re.match(r"^(?:let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)$", expr_stripped, re.IGNORECASE)
        if assign_match:
            var_name = assign_match.group(1)
            rhs_expr = assign_match.group(2)
            
            tokens = tokenize(rhs_expr)
            postfix = infix_to_postfix(tokens)
            val = eval_postfix(postfix, self.variables)

            # Save snapshot for undo, clear redo
            self.undo_stack.push(dict(self.variables))
            self.redo_stack = Stack()
            self.variables[var_name] = val
            return val

        # Evaluate normal expression
        tokens = tokenize(expr_stripped)
        postfix = infix_to_postfix(tokens)
        return eval_postfix(postfix, self.variables)

    def start_repl(self):
        """Launch interactive terminal prompt."""
        print("PyStackCalc REPL initialized. Type 'exit' or 'quit' to exit.")
        while True:
            try:
                line = input("calc> ")
                if line.strip().lower() in ("exit", "quit"):
                    break
                if not line.strip():
                    continue
                result = self.execute(line)
                if result is not None:
                    print(result)
            except (ValueError, ZeroDivisionError, NameError, IndexError) as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break


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
