import re


# =========================================================
# STEP 1: STACK CLASS
# =========================================================

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
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        return self.items.copy()


# =========================================================
# STEP 2: TOKENIZER
# =========================================================

def tokenize(expression):
    """
    Convert an expression into tokens.

    Example:
        10 + 5 * (3 - 1)

    becomes:
        ['10', '+', '5', '*', '(', '3', '-', '1', ')']
    """

    pattern = r'\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_]*|[+\-*/()]'

    tokens = []
    position = 0

    while position < len(expression):

        # Ignore spaces
        if expression[position].isspace():
            position += 1
            continue

        match = re.match(pattern, expression[position:])

        if not match:
            raise ValueError(
                f"Invalid character: {expression[position]}"
            )

        token = match.group()
        tokens.append(token)

        position += len(token)

    return tokens


# =========================================================
# STEP 3: CALCULATOR
# =========================================================

class PyStackCalc:

    def __init__(self):
        self.variables = {}

    # -----------------------------------------------------
    # Check whether a token is a number
    # -----------------------------------------------------

    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    # -----------------------------------------------------
    # Get the value of a token
    # -----------------------------------------------------

    def get_value(self, token):

        if self.is_number(token):
            return float(token)

        if token in self.variables:
            return self.variables[token]

        raise NameError(f"Undefined variable: {token}")

    # -----------------------------------------------------
    # Operator precedence
    # -----------------------------------------------------

    def precedence(self, operator):

        if operator in ("+", "-"):
            return 1

        if operator in ("*", "/"):
            return 2

        return 0

    # -----------------------------------------------------
    # Apply an operation
    # -----------------------------------------------------

    def apply_operator(self, values, operator):

        if values.size() < 2:
            raise ValueError("Invalid expression")

        right = values.pop()
        left = values.pop()

        if operator == "+":
            result = left + right

        elif operator == "-":
            result = left - right

        elif operator == "*":
            result = left * right

        elif operator == "/":

            if right == 0:
                raise ZeroDivisionError("division by zero")

            result = left / right

        else:
            raise ValueError(f"Unknown operator: {operator}")

        values.push(result)

    # -----------------------------------------------------
    # Evaluate expression
    # -----------------------------------------------------

    def evaluate(self, expression):

        tokens = tokenize(expression)

        values = Stack()
        operators = Stack()

        previous_token = None

        for token in tokens:

            # ---------------------------------------------
            # Number
            # ---------------------------------------------

            if self.is_number(token):
                values.push(self.get_value(token))
                previous_token = token
                continue

            # ---------------------------------------------
            # Variable
            # ---------------------------------------------

            if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token):
                values.push(self.get_value(token))
                previous_token = token
                continue

            # ---------------------------------------------
            # Opening parenthesis
            # ---------------------------------------------

            if token == "(":
                operators.push(token)
                previous_token = token
                continue

            # ---------------------------------------------
            # Closing parenthesis
            # ---------------------------------------------

            if token == ")":

                while (
                    not operators.is_empty()
                    and operators.peek() != "("
                ):
                    operator = operators.pop()
                    self.apply_operator(values, operator)

                if operators.is_empty():
                    raise ValueError("Mismatched parentheses")

                operators.pop()  # Remove '('

                previous_token = token
                continue

            # ---------------------------------------------
            # Operator
            # ---------------------------------------------

            if token in ("+", "-", "*", "/"):

                # Handle unary minus
                if (
                    token == "-"
                    and (
                        previous_token is None
                        or previous_token in ("+", "-", "*", "/", "(")
                    )
                ):
                    values.push(0)

                while (
                    not operators.is_empty()
                    and operators.peek() != "("
                    and self.precedence(operators.peek())
                    >= self.precedence(token)
                ):
                    operator = operators.pop()
                    self.apply_operator(values, operator)

                operators.push(token)
                previous_token = token
                continue

            raise ValueError(f"Invalid token: {token}")

        # Apply remaining operators
        while not operators.is_empty():

            if operators.peek() == "(":
                raise ValueError("Mismatched parentheses")

            operator = operators.pop()
            self.apply_operator(values, operator)

        if values.size() != 1:
            raise ValueError("Invalid expression")

        result = values.pop()

        # Return integer instead of 5.0
        if result.is_integer():
            return int(result)

        return result

    # -----------------------------------------------------
    # Execute command
    # -----------------------------------------------------

    def execute(self, expression):

        expression = expression.strip()

        if not expression:
            return None

        # Variable assignment
        match = re.fullmatch(
            r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)',
            expression
        )

        if match:

            variable = match.group(1)
            value_expression = match.group(2)

            value = self.evaluate(value_expression)

            self.variables[variable] = value

            return value

        # Normal expression
        return self.evaluate(expression)


# =========================================================
# STEP 4: TEST CASES
# =========================================================

def run_tests():

    engine = PyStackCalc()

    # Test 1
    assert engine.execute("2 + 3") == 5

    # Test 2
    assert engine.execute("10 - 4") == 6

    # Test 3
    assert engine.execute("3 * 4") == 12

    # Test 4
    assert engine.execute("20 / 5") == 4

    # Test 5
    assert engine.execute("2 + 3 * 4") == 14

    # Test 6
    assert engine.execute("(2 + 3) * 4") == 20

    # Test 7
    assert engine.execute("10 / 2 + 3") == 8

    # Test 8: variables
    engine.execute("x = 10")
    assert engine.execute("x + 5") == 15

    # Test 9: division by zero
    try:
        engine.execute("100 / (4 - 4)")
        assert False, "Test 9 Failed: Should raise ZeroDivisionError"

    except ZeroDivisionError:
        pass

    print("All 9 test cases passed successfully!")


# =========================================================
# STEP 5: MAIN PROGRAM
# =========================================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()

    else:

        calculator = PyStackCalc()

        print("PyStackCalc")
        print("Type an expression or type 'exit' to quit.")

        while True:

            try:
                expression = input(">>> ")

                if expression.lower() == "exit":
                    break

                result = calculator.execute(expression)

                if result is not None:
                    print(result)

            except Exception as error:
                print("Error:", error)

