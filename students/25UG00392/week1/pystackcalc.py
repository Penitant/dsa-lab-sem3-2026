
import re
import sys


# STEP 1: Stack Class
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("peek from empty stack")

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


# STEP 2: Tokenizer
def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[+\-*/^()%=]"
    tokens = re.findall(pattern, expr)

    # Check for invalid characters
    remaining = re.sub(pattern, "", expr)

    if not tokens or remaining.strip():
        raise ValueError("Empty expression or invalid tokens")

    return tokens


# STEP 3: Infix to Postfix
precedence = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3
}

right_associative = {"^"}


def infix_to_postfix(tokens):
    output = []
    operators = Stack()

    for token in tokens:
        # Numbers and variable names
        if token.replace(".", "", 1).isdigit() or token.isidentifier():
            output.append(token)

        elif token == "(":
            operators.push(token)

        elif token == ")":
            while (
                not operators.is_empty()
                and operators.peek() != "("
            ):
                output.append(operators.pop())

            if operators.is_empty():
                raise ValueError("Mismatched parentheses")

            operators.pop()

        elif token in precedence:
            while not operators.is_empty():
                top = operators.peek()

                if top == "(":
                    break

                higher_precedence = (
                    precedence[top] > precedence[token]
                )

                equal_and_left_associative = (
                    precedence[top] == precedence[token]
                    and token not in right_associative
                )

                if higher_precedence or equal_and_left_associative:
                    output.append(operators.pop())
                else:
                    break

            operators.push(token)

        else:
            raise ValueError(f"Invalid token: {token}")

    # Pop remaining operators
    while not operators.is_empty():
        top = operators.pop()

        if top == "(":
            raise ValueError("Mismatched parentheses")

        output.append(top)

    return output


# STEP 4: Postfix Evaluator
def eval_postfix(tokens, variables):
    values = Stack()

    for token in tokens:
        # Check whether the token is a number
        try:
            number = float(token)
            values.push(number)
            continue
        except ValueError:
            pass

        # Check whether the token is a variable
        if token.isidentifier() and token not in precedence:
            if token not in variables:
                raise ValueError(f"Unknown variable: {token}")

            values.push(variables[token])
            continue

        # Evaluate operators
        if token in precedence:
            if values.size() < 2:
                raise ValueError("Invalid expression")

            b = values.pop()
            a = values.pop()

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

            elif token == "^":
                result = a ** b

            values.push(result)

        else:
            raise ValueError(f"Invalid token: {token}")

    if values.size() != 1:
        raise ValueError("Invalid expression")

    return values.pop()


# STEP 5: Calculator Engine
class PyStackCalc:
    def __init__(self):
        self.variables = {
            "pi": 3.14159,
            "e": 2.71828
        }

        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def evaluate(self, expression):
        expression = expression.strip()

        if not expression:
            raise ValueError("Expression cannot be empty")

        # Undo and redo commands
        if expression.lower() == "undo":
            self.undo()
            return None

        if expression.lower() == "redo":
            self.redo()
            return None

        # Handle "let x = 15"
        if expression.startswith("let "):
            expression = expression[4:].strip()

        # Handle variable assignment
        if "=" in expression:
            parts = expression.split("=")

            if len(parts) != 2:
                raise ValueError("Invalid assignment")

            name = parts[0].strip()
            value_expression = parts[1].strip()

            if not name.isidentifier():
                raise ValueError("Invalid variable name")

            if name in ("pi", "e"):
                raise ValueError("Cannot change built-in constants")

            if not value_expression:
                raise ValueError("Missing assignment value")

            # Calculate before modifying variables
            tokens = tokenize(value_expression)
            postfix = infix_to_postfix(tokens)
            value = eval_postfix(postfix, self.variables)

            # Save the previous variable state
            self.undo_stack.push(dict(self.variables))

            # Clear redo history after a new assignment
            self.redo_stack = Stack()

            self.variables[name] = value
            return value

        # Normal arithmetic expression
        tokens = tokenize(expression)
        postfix = infix_to_postfix(tokens)

        return eval_postfix(postfix, self.variables)

    def execute(self, expression):
        # Alias for compatibility with tests using execute()
        return self.evaluate(expression)

    def undo(self):
        if self.undo_stack.is_empty():
            print("Nothing to undo.")
            return

        self.redo_stack.push(dict(self.variables))
        self.variables = self.undo_stack.pop()

        print("Undo successful.")

    def redo(self):
        if self.redo_stack.is_empty():
            print("Nothing to redo.")
            return

        self.undo_stack.push(dict(self.variables))
        self.variables = self.redo_stack.pop()

        print("Redo successful.")

    def start_repl(self):
        print("PyStackCalc")
        print("Type 'undo', 'redo', 'vars', or 'quit'.")

        while True:
            try:
                expression = input("calc> ").strip()

                if expression.lower() in ("quit", "exit"):
                    print("Goodbye!")
                    break

                elif expression.lower() == "vars":
                    print(self.variables)

                else:
                    result = self.evaluate(expression)

                    if result is not None:
                        print(result)

            except (ValueError, ZeroDivisionError, IndexError) as error:
                print(f"Error: {error}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


# TEST CASES
def run_tests():
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()

    # 1. Basic precedence and grouping
    assert engine.evaluate("3 + 4 * 2") == 11
    assert engine.evaluate("(3 + 4) * 2") == 14
    assert engine.evaluate("2 ^ 3 ^ 2") == 512
    assert engine.evaluate("( 3 + 4 ) * 2 - 8 / 4") == 12

    # 2. Variables
    engine.evaluate("let x = 15")
    engine.evaluate("let y = x * 2 - 10")
    assert engine.variables["y"] == 20

    # 3. Undo and redo
    engine.evaluate("undo")
    assert "y" not in engine.variables

    engine.evaluate("redo")
    assert engine.variables["y"] == 20

    # 4. Error handling: mismatched parentheses
    try:
        engine.evaluate("(3 + 4 * 2")
        assert False, "Expected ValueError for unclosed parenthesis"
    except ValueError:
        pass

    # 5. Error handling: division by zero
    try:
        engine.evaluate("100 / (4 - 4)")
        assert False, "Expected ZeroDivisionError"
    except ZeroDivisionError:
        pass

    print("All 9 test cases passed successfully!")


# PROGRAM ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()
