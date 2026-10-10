"""PyStackCalc - a terminal calculator built using stacks.
"""

import re


# ---------- Step 1: Stack ----------
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) == 0:
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if len(self.items) == 0:
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return list(self.items)


# ---------- Step 2: Tokenizer ----------
def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens


# ---------- Step 3: Infix to Postfix (Shunting-Yard) ----------
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOCIATIVE = {"^"}  # 2 ^ 3 ^ 2 = 2 ^ (3 ^ 2) = 512


def infix_to_postfix(tokens: list[str]) -> list[str]:
    output = []
    stack = Stack()

    for tok in tokens:
        if tok in PRECEDENCE:
            # Pop operators that must be done before this one
            while not stack.is_empty() and stack.peek() in PRECEDENCE:
                top = stack.peek()
                if PRECEDENCE[top] > PRECEDENCE[tok] or (
                    PRECEDENCE[top] == PRECEDENCE[tok] and tok not in RIGHT_ASSOCIATIVE
                ):
                    output.append(stack.pop())
                else:
                    break
            stack.push(tok)
        elif tok == "(":
            stack.push(tok)
        elif tok == ")":
            # Pop until we find the matching "("
            while not stack.is_empty() and stack.peek() != "(":
                output.append(stack.pop())
            if stack.is_empty():
                raise ValueError("Mismatched parentheses")
            stack.pop()  # discard "("
        elif tok == "=":
            raise ValueError("Unexpected '='")
        else:
            output.append(tok)  # number or variable name

    # Pop whatever is left
    while not stack.is_empty():
        top = stack.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses")
        output.append(top)

    return output


# ---------- Step 4: Postfix Evaluator ----------
def eval_postfix(postfix: list[str], variables: dict):
    stack = Stack()

    for tok in postfix:
        if tok in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Malformed expression")
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
        elif tok[0].isdigit():
            stack.push(float(tok) if "." in tok else int(tok))
        else:
            if tok not in variables:
                raise ValueError("Unknown variable: " + tok)
            stack.push(variables[tok])

    if stack.size() != 1:
        raise ValueError("Malformed expression")
    return stack.pop()


# ---------- Step 5: Calculator Engine & REPL ----------
class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def execute(self, line: str):
        line = line.strip()

        if line == "undo":
            if self.undo_stack.is_empty():
                return "Nothing to undo"
            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return "Undone"

        if line == "redo":
            if self.redo_stack.is_empty():
                return "Nothing to redo"
            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return "Redone"

        tokens = tokenize(line)

        # Remove the optional word "let"
        if tokens[0] == "let":
            tokens = tokens[1:]

        # Assignment:  x = <expression>
        if len(tokens) >= 3 and tokens[1] == "=":
            name = tokens[0]
            value = eval_postfix(infix_to_postfix(tokens[2:]), self.variables)
            self.undo_stack.push(dict(self.variables))  # save old state
            self.redo_stack = Stack()                   # clear redo
            self.variables[name] = value
            return value

        # Normal expression
        return eval_postfix(infix_to_postfix(tokens), self.variables)

    def start_repl(self):
        print("PyStackCalc - type an expression, 'let x = 5', 'undo', 'redo' or 'quit'")
        while True:
            try:
                line = input(">>> ")
            except (EOFError, KeyboardInterrupt):
                break
            if line.strip() == "quit":
                break
            if line.strip() == "":
                continue
            try:
                print(self.execute(line))
            except (ValueError, ZeroDivisionError) as err:
                print("Error:", err)
        print("Goodbye!")


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
