
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
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


def tokenize(expr):
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)

    if not tokens:
        raise ValueError("Empty expression or invalid tokens")

    return tokens


PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3
}

RIGHT_ASSOCIATIVE = {"^"}


def infix_to_postfix(tokens):
    output = []
    operators = Stack()

    for token in tokens:

        # Number
        if token[0].isdigit() or token[0] == ".":
            output.append(token)

        # Variable
        elif token[0].isalpha() or token[0] == "_":
            output.append(token)

        # Opening parenthesis
        elif token == "(":
            operators.push(token)

        # Closing parenthesis
        elif token == ")":
            found = False

            while not operators.is_empty():
                top = operators.pop()

                if top == "(":
                    found = True
                    break

                output.append(top)

            if not found:
                raise ValueError("Mismatched parentheses")

        # Operator
        elif token in PRECEDENCE:
            while not operators.is_empty():
                top = operators.peek()

                if top == "(":
                    break

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
            raise ValueError("Invalid token: " + token)

    # Pop remaining operators
    while not operators.is_empty():
        top = operators.pop()

        if top == "(":
            raise ValueError("Mismatched parentheses")

        output.append(top)

    return output


def eval_postfix(postfix, variables):
    stack = Stack()

    for token in postfix:

        # Number
        if token[0].isdigit() or token[0] == ".":
            stack.push(float(token))

        # Variable
        elif token[0].isalpha() or token[0] == "_":
            if token not in variables:
                raise NameError("Unknown variable: " + token)

            stack.push(variables[token])

        # Operator
        else:
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
                    raise ZeroDivisionError("Cannot divide by zero")
                result = a / b
            elif token == "%":
                if b == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = a % b
            elif token == "^":
                result = a ** b
            else:
                raise ValueError("Invalid operator: " + token)

            stack.push(result)

    if stack.size() != 1:
        raise ValueError("Invalid expression")

    return stack.pop()


class PyStackCalc:
    def __init__(self):
        self.variables = {
            "pi": 3.14159,
            "e": 2.71828
        }

        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def calculate(self, expression):
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)
        return eval_postfix(postfix, self.variables)

    def assign(self, name, expression):
        value = self.calculate(expression)

        self.undo_stack.push(self.variables.copy())
        self.redo_stack = Stack()

        self.variables[name] = value

        print(name, "=", value)

    def undo(self):
        if self.undo_stack.is_empty():
            print("Nothing to undo")
            return

        self.redo_stack.push(self.variables.copy())
        self.variables = self.undo_stack.pop()

        print("Undo complete")

    def redo(self):
        if self.redo_stack.is_empty():
            print("Nothing to redo")
            return

        self.undo_stack.push(self.variables.copy())
        self.variables = self.redo_stack.pop()

        print("Redo complete")

    def execute(self, command):
        command = command.strip()

        if command == "undo":
            self.undo()
            return None

        elif command == "redo":
            self.redo()
            return None

        if command.startswith("let "):
            command = command[4:].strip()

        if "=" in command:
            name, expression = command.split("=", 1)
            name = name.strip()
            expression = expression.strip()

            if not name.isidentifier():
                raise ValueError("Invalid variable name")

            self.assign(name, expression)
            return self.variables[name]

        return self.calculate(command)

    def start_repl(self):
        print("PyStackCalc")
        print("Type exit to stop")

        while True:
            command = input(">>> ").strip()

            if command == "exit":
                print("Goodbye!")
                break

            try:
                if command == "undo":
                    self.execute("undo")

                elif command == "redo":
                    self.execute("redo")

                elif command == "vars":
                    for name, value in self.variables.items():
                        print(name, "=", value)

                else:
                    print(self.execute(command))

            except Exception as error:
                print("Error:", error)


def run_tests():
    """Automated test cases to verify the implementation."""
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()

    # 1. Basic Precedence and Grouping
    assert engine.execute("3 + 4 * 2") == 11, \
        "Test 1 Failed: Precedence"

    assert engine.execute("(3 + 4) * 2") == 14, \
        "Test 2 Failed: Parentheses"

    assert engine.execute("2 ^ 3 ^ 2") == 512, \
        "Test 3 Failed: Exponent right-associativity"

    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12, \
        "Test 4 Failed: Mixed arithmetic"

    # 2. Variables
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")

    assert engine.variables["y"] == 20, \
        "Test 5 Failed: Variable calculation"

    # 3. Undo and Redo
    engine.execute("undo")

    assert "y" not in engine.variables, \
        "Test 6 Failed: Undo should remove y"

    engine.execute("redo")

    assert engine.variables["y"] == 20, \
        "Test 7 Failed: Redo should restore y"

    # 4. Error Handling
    try:
        engine.execute("(3 + 4 * 2")
        assert False, \
            "Test 8 Failed: Missing parenthesis should raise ValueError"
    except ValueError:
        pass

    try:
        engine.execute("100 / (4 - 4)")
        assert False, \
            "Test 9 Failed: Division by zero should raise ZeroDivisionError"
    except ZeroDivisionError:
        pass

    print("All 9 test cases passed successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()
