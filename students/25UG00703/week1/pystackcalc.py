import math
import re


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return not self.items

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


TOKEN_RE = re.compile(
    r"\d+(?:\.\d*)?|\.\d+|[A-Za-z_]\w*|[()+\-*/^]"
)


def tokenize(expr):
    tokens = []
    pos = 0
    while pos < len(expr):
        if expr[pos].isspace():
            pos += 1
            continue
        match = TOKEN_RE.match(expr, pos)
        if not match:
            raise ValueError(f"Invalid character: {expr[pos]}")
        tokens.append(match.group())
        pos = match.end()
    return tokens


def infix_to_postfix(tokens):
    if isinstance(tokens, str):
        tokens = tokenize(tokens)

    output, ops = [], []
    precedence = {
        "+": 1, "-": 1, "*": 2, "/": 2,
        "u+": 3, "u-": 3, "^": 4
    }
    expect_operand = True

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d*)?|\.\d+|[A-Za-z_]\w*", token):
            if not expect_operand:
                raise ValueError("Missing operator")
            output.append(token)
            expect_operand = False

        elif token == "(":
            if not expect_operand:
                raise ValueError("Missing operator")
            ops.append(token)

        elif token == ")":
            if expect_operand:
                raise ValueError("Invalid expression")
            while ops and ops[-1] != "(":
                output.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()
            expect_operand = False

        elif token in ("+", "-", "*", "/", "^"):
            if expect_operand:
                if token not in ("+", "-"):
                    raise ValueError("Invalid expression")
                ops.append("u" + token)
                continue

            while ops and ops[-1] != "(" and (
                precedence[ops[-1]] > precedence[token]
                or (
                    precedence[ops[-1]] == precedence[token]
                    and token != "^"
                )
            ):
                output.append(ops.pop())
            ops.append(token)
            expect_operand = True

        else:
            raise ValueError(f"Invalid token: {token}")

    if expect_operand:
        raise ValueError("Incomplete expression")

    while ops:
        op = ops.pop()
        if op == "(":
            raise ValueError("Mismatched parentheses")
        output.append(op)

    return output


def eval_postfix(tokens, variables=None):
    if isinstance(tokens, str):
        tokens = tokens.split()

    variables = {"pi": math.pi, "e": math.e, **(variables or {})}
    stack = Stack()

    for token in tokens:
        if token in ("u+", "u-"):
            value = stack.pop()
            stack.push(value if token == "u+" else -value)

        elif token in ("+", "-", "*", "/", "^"):
            b, a = stack.pop(), stack.pop()
            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                result = a / b
            else:
                result = a ** b
            stack.push(result)

        else:
            try:
                value = variables[token] if token in variables else float(token)
            except ValueError:
                raise ValueError(f"Unknown variable: {token}")
            stack.push(value)

    if stack.size() != 1:
        raise ValueError("Invalid postfix expression")
    return stack.pop()


class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": math.pi, "e": math.e}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def evaluate(self, expr):
        expr = expr.strip()
        if expr.lower() in ("undo", "redo"):
            return self.command(expr.lower())

        match = re.fullmatch(
            r"(?:let\s+)?([A-Za-z_]\w*)\s*=\s*(.+)", expr
        )
        if match:
            name, rhs = match.groups()
            if name in ("pi", "e"):
                raise ValueError("Cannot overwrite constants")
            value = eval_postfix(
                infix_to_postfix(tokenize(rhs)), self.variables
            )
            self.undo_stack.push(self.variables.copy())
            self.redo_stack = Stack()
            self.variables[name] = value
            return value

        return eval_postfix(
            infix_to_postfix(tokenize(expr)), self.variables
        )

    def command(self, cmd):
        if cmd == "undo":
            if self.undo_stack.is_empty():
                raise ValueError("Nothing to undo")
            self.redo_stack.push(self.variables.copy())
            self.variables = self.undo_stack.pop()
        elif cmd == "redo":
            if self.redo_stack.is_empty():
                raise ValueError("Nothing to redo")
            self.undo_stack.push(self.variables.copy())
            self.variables = self.redo_stack.pop()
        else:
            raise ValueError("Unknown command")
        return self.variables.copy()

    def start_repl(self):
        while True:
            try:
                expr = input("calc> ").strip()
                if expr.lower() in ("exit", "quit"):
                    break
                if expr:
                    print(self.evaluate(expr))
            except (ValueError, ZeroDivisionError, IndexError,
                    OverflowError) as error:
                print("Error:", error)
            except (EOFError, KeyboardInterrupt):
                print()
                break


def run_tests():
    tests = [
        ("3 + 4 * 2", 11),
        ("(3 + 4) * 2", 14),
        ("2 ^ 3 ^ 2", 512),
        ("(3 + 4) * 2 - 8 / 4", 12),
        ("2 * -3", -6),
        ("-2 ^ 2", -4),
        ("2 ^ -3", 0.125),
    ]
    calc = PyStackCalc()

    for expr, expected in tests:
        actual = calc.evaluate(expr)
        assert math.isclose(actual, expected), (
            f"{expr}: expected {expected}, got {actual}"
        )

    calc.evaluate("let x = 15")
    assert calc.evaluate("x * 2") == 30
    calc.evaluate("x = 20")
    calc.command("undo")
    assert calc.variables["x"] == 15
    calc.command("redo")
    assert calc.variables["x"] == 20

    try:
        calc.evaluate("(3 + 4")
        raise AssertionError("Missing parenthesis was not detected")
    except ValueError:
        pass

    try:
        calc.evaluate("5 / 0")
        raise AssertionError("Division by zero was not detected")
    except ZeroDivisionError:
        pass

    print("All tests passed successfully!")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        run_tests()
    else:
        PyStackCalc().start_repl()