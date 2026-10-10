# PyStackCalc - stack-based calculator (no imports used)


# ---------- Step 1: Stack ----------
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

    def to_list(self):
        return list(self.items)


# ---------- Step 2: Tokenizer (manual, replaces re) ----------
def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            if j + 1 < len(expr) and expr[j] == "." and expr[j + 1].isdigit():
                j += 1
                while j < len(expr) and expr[j].isdigit():
                    j += 1
            tokens.append(expr[i:j])
            i = j
        elif ch.isalpha() or ch == "_":
            j = i
            while j < len(expr) and (expr[j].isalnum() or expr[j] == "_"):
                j += 1
            tokens.append(expr[i:j])
            i = j
        elif ch in "+-*/^%()=":
            tokens.append(ch)
            i += 1
        else:
            raise ValueError("Invalid character: " + ch)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens


# ---------- Step 3: Infix -> Postfix ----------
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
RIGHT_ASSOCIATIVE = {"^"}


def infix_to_postfix(tokens):
    output = []
    ops = Stack()
    for tok in tokens:
        if tok in PRECEDENCE:
            while (not ops.is_empty() and ops.peek() in PRECEDENCE and
                   (PRECEDENCE[ops.peek()] > PRECEDENCE[tok] or
                    (PRECEDENCE[ops.peek()] == PRECEDENCE[tok] and
                     tok not in RIGHT_ASSOCIATIVE))):
                output.append(ops.pop())
            ops.push(tok)
        elif tok == "(":
            ops.push(tok)
        elif tok == ")":
            while not ops.is_empty() and ops.peek() != "(":
                output.append(ops.pop())
            if ops.is_empty():
                raise ValueError("Mismatched parentheses")
            ops.pop()  # discard "("
        else:
            output.append(tok)  # number or variable
    while not ops.is_empty():
        top = ops.pop()
        if top == "(":
            raise ValueError("Mismatched parentheses")
        output.append(top)
    return output


# ---------- Step 4: Postfix evaluator ----------
def eval_postfix(postfix, variables):
    stack = Stack()
    for tok in postfix:
        if tok[0].isdigit():
            stack.push(float(tok) if "." in tok else int(tok))
        elif tok in PRECEDENCE:
            if stack.size() < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            if tok == "+":
                stack.push(a + b)
            elif tok == "-":
                stack.push(a - b)
            elif tok == "*":
                stack.push(a * b)
            elif tok == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.push(a / b)
            elif tok == "%":
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero")
                stack.push(a % b)
            elif tok == "^":
                stack.push(a ** b)
        else:
            if tok not in variables:
                raise ValueError("Unknown variable: " + tok)
            stack.push(variables[tok])
    if stack.size() != 1:
        raise ValueError("Invalid expression")
    return stack.pop()


# ---------- Step 5: Calculator engine ----------
class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def evaluate(self, tokens):
        return eval_postfix(infix_to_postfix(tokens), self.variables)

    def execute(self, line):
        line = line.strip()

        if line == "undo":
            if self.undo_stack.is_empty():
                raise ValueError("Nothing to undo")
            self.redo_stack.push(dict(self.variables))
            self.variables = self.undo_stack.pop()
            return "undo done"

        if line == "redo":
            if self.redo_stack.is_empty():
                raise ValueError("Nothing to redo")
            self.undo_stack.push(dict(self.variables))
            self.variables = self.redo_stack.pop()
            return "redo done"

        tokens = tokenize(line)
        if tokens[0] == "let":
            tokens = tokens[1:]

        # Assignment: name = expression
        if len(tokens) >= 3 and tokens[1] == "=" and \
                (tokens[0][0].isalpha() or tokens[0][0] == "_"):
            name = tokens[0]
            value = self.evaluate(tokens[2:])
            self.undo_stack.push(dict(self.variables))
            self.redo_stack = Stack()
            self.variables[name] = value
            return value

        return self.evaluate(tokens)

    def start_repl(self):
        print("PyStackCalc - commands: undo, redo, vars, quit")
        while True:
            try:
                line = input(">>> ").strip()
            except EOFError:
                break
            if not line:
                continue
            if line in ("quit", "exit"):
                break
            if line == "vars":
                print(self.variables)
                continue
            try:
                print(self.execute(line))
            except (ValueError, ZeroDivisionError, IndexError) as err:
                print("Error:", err)


if __name__ == "__main__":
    calc = PyStackCalc()
    calc.start_repl()