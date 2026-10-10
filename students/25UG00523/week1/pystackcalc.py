import re
import sys


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
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3
}

RIGHT_ASSOCIATIVE = {"^"}


def tokenize(expression):
    pattern = r"\d+(?:\.\d+)?|[A-Za-z_]\w*|[()+\-*/%^=]"
    tokens = re.findall(pattern, expression)

    cleaned = re.sub(r"\s+", "", expression)
    rebuilt = "".join(tokens)

    if cleaned != rebuilt:
        raise ValueError("Invalid character in expression")

    return tokens


def infix_to_postfix(tokens):
    output = []
    operators = Stack()

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token) or re.fullmatch(
            r"[A-Za-z_]\w*", token
        ):
            output.append(token)

        elif token == "(":
            operators.push(token)

        elif token == ")":
            found_left = False

            while not operators.is_empty():
                top = operators.pop()

                if top == "(":
                    found_left = True
                    break

                output.append(top)

            if not found_left:
                raise ValueError("Mismatched parentheses")

        elif token in PRECEDENCE:
            while not operators.is_empty() and operators.peek() != "(":
                top = operators.peek()

                if (
                    PRECEDENCE[top] > PRECEDENCE[token]
                    or (
                        PRECEDENCE[top] == PRECEDENCE[token]
                        and token not in RIGHT_ASSOCIATIVE
                    )
                ):
                    output.append(operators.pop())
                else:
                    break

            operators.push(token)

        else:
            raise ValueError(f"Unknown token: {token}")

    while not operators.is_empty():
        top = operators.pop()

        if top == "(":
            raise ValueError("Mismatched parentheses")

        output.append(top)

    return output


def eval_postfix(postfix, variables):
    stack = Stack()

    for token in postfix:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            number = float(token)

            if number.is_integer():
                number = int(number)

            stack.push(number)

        elif re.fullmatch(r"[A-Za-z_]\w*", token):
            if token not in variables:
                raise ValueError(f"Unknown variable: {token}")

            stack.push(variables[token])

        elif token in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Invalid expression")

            right = stack.pop()
            left = stack.pop()

            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            elif token == "/":
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result = left / right
            elif token == "%":
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result = left % right
            elif token == "^":
                result = left ** right

            stack.push(result)

        else:
            raise ValueError(f"Invalid postfix token: {token}")

    if stack.size() != 1:
        raise ValueError("Invalid expression")

    result = stack.pop()

    if isinstance(result, float) and result.is_integer():
        return int(result)

    return result


class PyStackCalc:
    def __init__(self):
        self.variables = {
            "pi": 3.14159,
            "e": 2.71828
        }

        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def _save_state(self):
        return self.variables.copy()

    def _restore_state(self, state):
        self.variables = state.copy()

    def execute(self, command):
        command = command.strip()

        if not command:
            return None

        if command.lower() == "undo":
            if self.undo_stack.is_empty():
                raise ValueError("Nothing to undo")

            self.redo_stack.push(self._save_state())
            previous_state = self.undo_stack.pop()
            self._restore_state(previous_state)

            return None

        if command.lower() == "redo":
            if self.redo_stack.is_empty():
                raise ValueError("Nothing to redo")

            self.undo_stack.push(self._save_state())
            next_state = self.redo_stack.pop()
            self._restore_state(next_state)

            return None

        assignment = re.fullmatch(
            r"(?:let\s+)?([A-Za-z_]\w*)\s*=\s*(.+)",
            command
        )

        if assignment:
            name = assignment.group(1)
            expression = assignment.group(2)

            old_state = self._save_state()

            tokens = tokenize(expression)
            postfix = infix_to_postfix(tokens)
            value = eval_postfix(postfix, self.variables)

            self.undo_stack.push(old_state)
            self.redo_stack = Stack()

            self.variables[name] = value

            return value

        tokens = tokenize(command)
        postfix = infix_to_postfix(tokens)

        return eval_postfix(postfix, self.variables)

    def start_repl(self):
        print("PyStackCalc")
        print("Type expressions, assignments, undo, redo, or exit.")

        while True:
            try:
                command = input(">>> ").strip()

                if command.lower() in {"exit", "quit"}:
                    break

                result = self.execute(command)

                if result is not None:
                    print(result)

            except Exception as error:
                print(f"Error: {error}")


def run_tests():
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
        engine.execute("(3 + 4")
        assert False
    except ValueError:
        pass

    try:
        engine.execute("10 / 0")
        assert False
    except ZeroDivisionError:
        pass

    print("✅ All 9 test cases passed successfully!")


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()