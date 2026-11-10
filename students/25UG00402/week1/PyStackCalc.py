import re
import sys
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self.items.pop()
    def peek(self):
        return self.items[-1] if self.items else None
    def is_empty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)
    def to_list(self):
        return self.items.copy()
def tokenize(expr: str) -> list[str]:
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")
    pattern = re.compile(
        r"\s*(\d+(?:\.\d+)?|[a-zA-Z_]\w*|[+\-*/^%()=])"
    )
    tokens = []
    position = 0
    while position < len(expr):
        match = pattern.match(expr, position)
        if not match:
            raise ValueError(
                f"Invalid token at position {position}"
            )
        tokens.append(match.group(1))
        position = match.end()
    return tokens
PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
    "u+": 4,
    "u-": 4,
}
RIGHT_ASSOCIATIVE = {"^", "u+", "u-"}
def infix_to_postfix(tokens: list[str]) -> list[str]:
    output = []
    operators = Stack()
    previous = None

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            output.append(token)
        elif re.fullmatch(r"[a-zA-Z_]\w*", token):
            output.append(token)
        elif token == "(":
            operators.push(token)
        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()
        elif token in PRECEDENCE:
            op = token
            if token in {"+", "-"} and (
                previous is None or previous in PRECEDENCE
                or previous in {"(", "="}
            ):
                op = "u+" if token == "+" else "u-"
            while not operators.is_empty():
                top = operators.peek()
                if top == "(":
                    break
                higher = PRECEDENCE[top] > PRECEDENCE[op]
                equal_left = (
                    PRECEDENCE[top] == PRECEDENCE[op]
                    and op not in RIGHT_ASSOCIATIVE
                )
                if higher or equal_left:
                    output.append(operators.pop())
                else:
                    break
            operators.push(op)
        else:
            raise ValueError(f"Invalid token: {token}")
        previous = token
    while not operators.is_empty():
        top = operators.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses")
        output.append(top)
    return output
def eval_postfix(
    tokens: list[str], variables: dict
) -> int | float:
    stack = Stack()
    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            value = float(token) if "." in token else int(token)
            stack.push(value)
        elif token in {"u+", "u-"}:
            if stack.is_empty():
                raise ValueError("Missing operand")
            value = stack.pop()
            stack.push(value if token == "u+" else -value)
        elif token in {"+", "-", "*", "/", "^", "%"}:
            if stack.size() < 2:
                raise ValueError("Missing operand")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = a / b
            elif token == "%":
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero")
                result = a % b
            else:
                result = a ** b
            stack.push(result)
        else:
            if token not in variables:
                raise ValueError(f"Undefined variable: {token}")
            stack.push(variables[token])
    if stack.size() != 1:
        raise ValueError("Invalid expression")
    return stack.pop()
class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()
    def execute(self, expression: str):
        expression = expression.strip()
        if not expression:
            raise ValueError("Empty expression")
        if expression.lower() == "undo":
            if self.undo_stack.is_empty():
                raise ValueError("Nothing to undo")

            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return None
        if expression.lower() == "redo":
            if self.redo_stack.is_empty():
                raise ValueError("Nothing to redo")
            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return None
        assignment = re.fullmatch(
            r"(?:let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)",
            expression,
        )
        if assignment:
            name, value_expression = assignment.groups()

            if name in {"pi", "e"}:
                raise ValueError("Cannot overwrite a constant")
            tokens = tokenize(value_expression)
            postfix = infix_to_postfix(tokens)
            value = eval_postfix(postfix, self.variables)

            self.undo_stack.push(dict(self.variables))
            self.redo_stack = Stack()
            self.variables[name] = value
            return value
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        return eval_postfix(postfix, self.variables)
    def start_repl(self):
        print("PyStackCalc - Terminal Calculator")
        print("Type 'undo', 'redo', or 'exit' to quit.")
        while True:
            try:
                expression = input("calc> ").strip()
                if expression.lower() in {"exit", "quit"}:
                    print("Goodbye!")
                    break
                result = self.execute(expression)
                if result is not None:
                    print(result)
                elif expression.lower() in {"undo", "redo"}:
                    print("Variables restored.")
            except (ValueError, ZeroDivisionError, IndexError,
                    OverflowError) as error:
                print(f"Error: {error}")
def run_tests():
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()
    assert engine.execute("3 + 4 * 2") == 11
    assert engine.execute("(3 + 4) * 2") == 14
    assert engine.execute("2 ^ 3 ^ 2") == 512
    assert engine.execute("(3 + 4) * 2 - 8 / 4") == 12
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")
    assert engine.variables["y"] == 20
    engine.execute("undo")
    assert "y" not in engine.variables
    engine.execute("redo")
    assert engine.variables["y"] == 20
    try:
        engine.execute("(3 + 4 * 2")
        assert False, "Expected ValueError"
    except ValueError:
        pass
    try:
        engine.execute("100 / (4 - 4)")
        assert False, "Expected ZeroDivisionError"
    except ZeroDivisionError:
        pass
    print("All 9 test cases passed successfully!")
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()