import re


# STEP 1: STACK CLASS
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
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


# STEP 2: TOKENIZER
def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = []
    position = 0

    for match in re.finditer(pattern, expr):
        if expr[position:match.start()].strip():
            raise ValueError("Invalid token in expression")
        tokens.append(match.group())
        position = match.end()

    if expr[position:].strip() or not tokens:
        raise ValueError("Empty expression or invalid tokens")

    return tokens


# STEP 3: INFIX TO POSTFIX
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
            while (
                not operators.is_empty()
                and operators.peek() in PRECEDENCE
                and (
                    PRECEDENCE[operators.peek()] > PRECEDENCE[token]
                    or (
                        PRECEDENCE[operators.peek()] == PRECEDENCE[token]
                        and token not in RIGHT_ASSOCIATIVE
                    )
                )
            ):
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
            raise ValueError("Invalid operator")

    while not operators.is_empty():
        operator = operators.pop()

        if operator == "(":
            raise ValueError("Unclosed parenthesis")

        output.append(operator)

    return output


# STEP 4: POSTFIX EVALUATOR
def eval_postfix(tokens, variables=None):
    if variables is None:
        variables = {}

    stack = Stack()

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            value = float(token) if "." in token else int(token)
            stack.push(value)

        elif token not in PRECEDENCE:
            if token not in variables:
                raise ValueError(f"Unknown variable: {token}")
            stack.push(variables[token])

        else:
            if stack.size() < 2:
                raise ValueError("Invalid expression")

            b = stack.pop()
            a = stack.pop()

            if token in ("/", "%") and b == 0:
                raise ZeroDivisionError("Division by zero")

            if token == "+":
                result = a + b
            elif token == "-":
                result = a - b
            elif token == "*":
                result = a * b
            elif token == "/":
                result = a / b
            elif token == "%":
                result = a % b
            elif token == "^":
                result = a ** b

            stack.push(result)

    if stack.size() != 1:
        raise ValueError("Invalid expression")

    return stack.pop()


# STEP 5: CALCULATOR ENGINE
class PyStackCalc:
    def __init__(self):
        self.variables = {
            "pi": 3.14159,
            "e": 2.71828
        }

        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def execute(self, command):
        command = command.strip()

        if command == "undo":
            if self.undo_stack.is_empty():
                return "Nothing to undo"

            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return "Undo successful"

        if command == "redo":
            if self.redo_stack.is_empty():
                return "Nothing to redo"

            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return "Redo successful"

        # Variable assignment
        assignment = re.fullmatch(
            r"(?:let\s+)?([a-zA-Z_]\w*)\s*=\s*(.+)",
            command
        )

        if assignment:
            name = assignment.group(1)
            expression = assignment.group(2)

            if name in ("pi", "e"):
                raise ValueError("Cannot overwrite built-in constants")

            result = self.calculate(expression)

            self.undo_stack.push(dict(self.variables))
            self.redo_stack = Stack()

            self.variables[name] = result
            return result

        return self.calculate(command)

    def calculate(self, expression):
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        return eval_postfix(postfix, self.variables)

    def start_repl(self):
        print("Welcome to PyStackCalc!")
        print("Type 'undo', 'redo' or 'exit'.")

        while True:
            try:
                command = input(">>> ").strip()

                if command in ("exit", "quit"):
                    print("Goodbye!")
                    break

                result = self.execute(command)
                print(result)

            except Exception as error:
                print("Error:", error)


# AUTOMATED TESTS
def run_tests():
    """Automated test cases to verify your implementation."""
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()

    # 1. Basic Precedence & Grouping
    assert engine.execute("3 + 4 * 2") == 11
    assert engine.execute("(3 + 4) * 2") == 14
    assert engine.execute("2 ^ 3 ^ 2") == 512
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12

    # 2. Variables
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")
    assert engine.variables["y"] == 20

    # 3. Undo / Redo
    engine.execute("undo")
    assert "y" not in engine.variables
    engine.execute("redo")
    assert engine.variables["y"] == 20

    # 4. Error Handling
    try:
        engine.execute("(3 + 4 * 2")
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        engine.execute("100 / (4 - 4)")
        assert False, "Should raise ZeroDivisionError"
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
