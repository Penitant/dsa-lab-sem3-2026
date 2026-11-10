import re
import sys


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


def tokenize(expr):
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)

    if not tokens or "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError("Empty expression or invalid tokens")

    return tokens


PRECEDENCE = {
    "+": 1, "-": 1,
    "*": 2, "/": 2, "%": 2,
    "^": 3
}
RIGHT_ASSOCIATIVE = {"^"}


def infix_to_postfix(tokens):
    output = []
    operators = Stack()

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?|[a-zA-Z_]\w*", token):
            output.append(token)

        elif token in PRECEDENCE:
            while (not operators.is_empty()
                   and operators.peek() in PRECEDENCE
                   and (
                       PRECEDENCE[operators.peek()] > PRECEDENCE[token]
                       or (
                           PRECEDENCE[operators.peek()] == PRECEDENCE[token]
                           and token not in RIGHT_ASSOCIATIVE
                       )
                   )):
                output.append(operators.pop())

            operators.push(token)

        elif token == "(":
            operators.push(token)

        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())

            if operators.is_empty():
                raise ValueError("Mismatched parentheses")

            operators.pop()

        else:
            raise ValueError("Invalid token: " + token)

    while not operators.is_empty():
        op = operators.pop()

        if op == "(":
            raise ValueError("Mismatched parentheses")

        output.append(op)

    return output


def eval_postfix(tokens, variables=None):
    variables = variables or {}
    stack = Stack()

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            value = float(token) if "." in token else int(token)
            stack.push(value)

        elif token in variables:
            stack.push(variables[token])

        elif token in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Invalid expression")

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
                    raise ZeroDivisionError("Division by zero")
                result = a % b
            else:
                result = a ** b

            stack.push(result)

        else:
            raise ValueError("Unknown variable: " + token)

    if stack.size() != 1:
        raise ValueError("Invalid expression")

    return stack.pop()


class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def execute(self, expression):
        expression = expression.strip()

        if expression == "undo":
            if not self.undo_stack.is_empty():
                self.redo_stack.push(dict(self.variables))
                self.variables = self.undo_stack.pop()
            return None

        if expression == "redo":
            if not self.redo_stack.is_empty():
                self.undo_stack.push(dict(self.variables))
                self.variables = self.redo_stack.pop()
            return None

        match = re.fullmatch(
            r"(?:let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)",
            expression
        )

        if match:
            name, value_expr = match.groups()
            tokens = tokenize(value_expr)
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
        print("Welcome to PyStackCalc!")
        print("Type 'undo', 'redo' or 'exit'.")

        while True:
            try:
                expression = input("calc> ").strip()

                if expression.lower() == "exit":
                    print("Goodbye!")
                    break

                result = self.execute(expression)

                if result is not None:
                    print("=", result)

            except (ValueError, ZeroDivisionError, IndexError) as error:
                print("Error:", error)


def run_tests():
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()

    assert engine.execute("3 + 4 * 2") == 11
    assert engine.execute("(3 + 4) * 2") == 14
    assert engine.execute("2 ^ 3 ^ 2") == 512
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12

    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")
    assert engine.variables["y"] == 20

    engine.execute("undo")
    assert "y" not in engine.variables

    engine.execute("redo")
    assert engine.variables["y"] == 20

    try:
        engine.execute("(3 + 4 * 2")
        assert False
    except ValueError:
        pass

    try:
        engine.execute("100 / (4 - 4)")
        assert False
    except ZeroDivisionError:
        pass

    print("All 9 test cases passed successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()