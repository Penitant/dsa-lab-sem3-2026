import re
import sys

class Stack:
    """A LIFO Stack implementation using a standard Python list."""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return list(self._items)


def tokenize(expr: str) -> list[str]:
    """Split raw text into distinct tokens (numbers, variables, operators, parentheses)."""
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens


# Operator precedence and associativity rules
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOCIATIVE = {"^"}


def infix_to_postfix(tokens: list[str]) -> list[str]:
    """Convert infix tokens to postfix (RPN) using Dijkstra's Shunting-Yard Algorithm."""
    output = []
    stack = Stack()
    
    for token in tokens:
        if token in PRECEDENCE:
            op1 = token
            while not stack.is_empty():
                op2 = stack.peek()
                if op2 in PRECEDENCE and (
                    (op1 not in RIGHT_ASSOCIATIVE and PRECEDENCE[op1] <= PRECEDENCE[op2]) or
                    (op1 in RIGHT_ASSOCIATIVE and PRECEDENCE[op1] < PRECEDENCE[op2])
                ):
                    output.append(stack.pop())
                else:
                    break
            stack.push(op1)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            found_left = False
            while not stack.is_empty():
                top = stack.pop()
                if top == '(':
                    found_left = True
                    break
                output.append(top)
            if not found_left:
                raise ValueError("Mismatched parentheses: missing '('")
        else:
            output.append(token)

    while not stack.is_empty():
        top = stack.pop()
        if top == '(':
            raise ValueError("Mismatched parentheses: missing ')'")
        output.append(top)
        
    return output


def eval_postfix(tokens: list[str], variables: dict) -> float | int:
    """Evaluate a postfix token list using an operand stack."""
    stack = Stack()
    
    for token in tokens:
        # Try parsing as number (int or float)
        try:
            if '.' in token:
                val = float(token)
            else:
                val = int(token)
            stack.push(val)
            continue
        except ValueError:
            pass
        
        # Check if variable
        if re.match(r"^[a-zA-Z_]\w*$", token):
            if token in variables:
                stack.push(variables[token])
            else:
                raise NameError(f"Undefined variable: {token}")
            continue
            
        # Operator evaluation
        if token in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                res = a + b
            elif token == '-':
                res = a - b
            elif token == '*':
                res = a * b
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                res = a / b
            elif token == '%':
                res = a % b
            elif token == '^':
                res = a ** b
            else:
                raise ValueError(f"Unknown operator: {token}")
            stack.push(res)
        else:
            raise ValueError(f"Invalid token: {token}")
            
    if stack.size() != 1:
        raise ValueError("Invalid expression")
    return stack.pop()


class PyStackCalc:
    """Calculator engine supporting variables, operator precedence, and undo/redo history."""
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def execute(self, line: str):
        line = line.strip()
        if not line:
            return None
            
        if line == "undo":
            if self.undo_stack.is_empty():
                print("Nothing to undo.")
                return None
            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return None
            
        if line == "redo":
            if self.redo_stack.is_empty():
                print("Nothing to redo.")
                return None
            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return None
            
        tokens = tokenize(line)
        
        # Parse variable assignments (e.g., "let x = 15" or "x = 15")
        is_assignment = False
        var_name = None
        expr_tokens = tokens
        
        if tokens[0] == "let" and len(tokens) >= 4 and tokens[2] == "=":
            is_assignment = True
            var_name = tokens[1]
            expr_tokens = tokens[3:]
        elif len(tokens) >= 3 and tokens[1] == "=" and re.match(r"^[a-zA-Z_]\w*$", tokens[0]):
            is_assignment = True
            var_name = tokens[0]
            expr_tokens = tokens[2:]
            
        postfix = infix_to_postfix(expr_tokens)
        result = eval_postfix(postfix, self.variables)
        
        if is_assignment:
            self.undo_stack.push(dict(self.variables))
            self.redo_stack = Stack()  # Clear redo history on new assignment
            self.variables[var_name] = result
            return result
        else:
            return result

    def start_repl(self):
        """Start the interactive terminal calculator."""
        print("PyStackCalc REPL. Enter mathematical expressions, variable assignments, or 'undo'/'redo' ('exit' to quit).")
        while True:
            try:
                line = input("pystackcalc> ")
                if line.strip().lower() in ("exit", "quit"):
                    break
                if not line.strip():
                    continue
                res = self.execute(line)
                if res is not None:
                    print(res)
            except (ValueError, ZeroDivisionError, NameError, IndexError) as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nExiting...")
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
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()
