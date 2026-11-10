import re

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()


# Operator precedence & rules
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOC = {"^"}


def tokenize(expr):
    # Splits numbers, variables, operators, and parentheses
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens


def is_number(tok):
    return re.fullmatch(r"\d+(?:\.\d+)?", tok) is not None


def infix_to_postfix(tokens):
    output = []
    ops = Stack()
    
    for tok in tokens:
        if is_number(tok) or re.fullmatch(r"[a-zA-Z_]\w*", tok):
            output.append(tok)
        elif tok in PRECEDENCE:
            while not ops.is_empty() and ops.peek() in PRECEDENCE:
                top = ops.peek()
                if PRECEDENCE[top] > PRECEDENCE[tok] or (
                    PRECEDENCE[top] == PRECEDENCE[tok] and tok not in RIGHT_ASSOC
                ):
                    output.append(ops.pop())
                else:
                    break
            ops.push(tok)
        elif tok == "(":
            ops.push(tok)
        elif tok == ")":
            while not ops.is_empty() and ops.peek() != "(":
                output.append(ops.pop())
            if ops.is_empty():
                raise ValueError("Mismatched parentheses: extra ')'")
            ops.pop()
        else:
            raise ValueError(f"Unexpected token: {tok}")
            
    while not ops.is_empty():
        top = ops.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses: unclosed '('")
        output.append(top)
        
    return output


def eval_postfix(postfix, variables):
    stack = Stack()
    for tok in postfix:
        if is_number(tok):
            stack.push(float(tok) if "." in tok else int(tok))
        elif tok in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Malformed expression")
            b = stack.pop()
            a = stack.pop()
            
            if tok == "+": r = a + b
            elif tok == "-": r = a - b
            elif tok == "*": r = a * b
            elif tok == "/":
                if b == 0: raise ZeroDivisionError("Division by zero")
                r = a / b
            elif tok == "%":
                if b == 0: raise ZeroDivisionError("Modulo by zero")
                r = a % b
            else:
                r = a ** b
            stack.push(r)
        else:
            if tok not in variables:
                raise ValueError(f"Undefined variable: {tok}")
            stack.push(variables[tok])
            
    if stack.size() != 1:
        raise ValueError("Malformed expression")
    return stack.pop()


class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def evaluate(self, expr):
        tokens = tokenize(expr)
        return eval_postfix(infix_to_postfix(tokens), self.variables)

    def execute(self, line):
        line = line.strip()
        cmd = line.lower()
        
        if cmd == "undo":
            if self.undo_stack.is_empty():
                raise ValueError("Nothing to undo")
            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return None
            
        if cmd == "redo":
            if self.redo_stack.is_empty():
                raise ValueError("Nothing to redo")
            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return None

        tokens = tokenize(line)
        if tokens[0] == "let" and len(tokens) > 2:
            tokens = tokens[1:]
            
        if len(tokens) > 2 and tokens[1] == "=" and re.fullmatch(r"[a-zA-Z_]\w*", tokens[0]):
            name = tokens[0]
            value = eval_postfix(infix_to_postfix(tokens[2:]), self.variables)
            self.undo_stack.push(dict(self.variables))
            self.redo_stack.clear()
            self.variables[name] = value
            return value
            
        return eval_postfix(infix_to_postfix(tokens), self.variables)

    def start_repl(self):
        print("PyStackCalc loaded. Type 'quit' to exit.")
        while True:
            try:
                line = input(">>> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if line.strip().lower() in ("quit", "exit"):
                break
            if not line.strip():
                continue
            try:
                res = self.execute(line)
                if res is not None:
                    print(res)
            except Exception as err:
                print(f"Error: {err}")


def run_tests():
    print("Running test suite...")
    calc = PyStackCalc()

    assert calc.execute("3 + 4 * 2") == 11
    assert calc.execute("(3 + 4) * 2") == 14
    assert calc.execute("2 ^ 3 ^ 2") == 512
    assert calc.execute("( 3 + 4 ) * 2 - 8 / 4") == 12

    calc.execute("let x = 15")
    calc.execute("let y = x * 2 - 10")
    assert calc.variables["y"] == 20

    calc.execute("undo")
    assert "y" not in calc.variables
    calc.execute("redo")
    assert calc.variables["y"] == 20

    print("All tests passed successfully!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        PyStackCalc().start_repl()
