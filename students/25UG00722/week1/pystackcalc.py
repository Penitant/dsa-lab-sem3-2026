import re

def precedence(op):
    if op == '^':
        return 3
    if op in '*/%':
        return 2
    if op in '+-':
        return 1
    return 0

class Stack:
    def __init__(self):
        self.stack=[]
    def PUSH(self,item):
        self.stack.append(item)
    def POP(self):
        if self.stack!=[]:
            return self.stack.pop()
        return None
    def PEEK(self):
        if self.stack!=[]:
            return self.stack[-1]
        return None
    def IS_EMPTY(self):
        if self.stack==[]:
            return 1
        else:
            return 0
    def SIZE(self):
        return len(self.stack)
    def TO_LIST(self):
        l=[]
        if self.stack!=[]:
            for i in self.stack:
                l.append(i)
        return l


def tokenize(expr: str) -> list[str]:
    pattern = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    tokens = re.findall(pattern, expr)
    if not tokens:
        raise ValueError("Empty expression or invalid tokens")
    return tokens
def is_number(token):
    return token.replace('.', '', 1).isdigit()

def infix_to_postfix(tokens):
    output = []
    stack = Stack()

    for i in tokens:
        if is_number(i) or i[0].isalpha() or i[0] == '_':
            output.append(i)

        elif i == '(':
            stack.PUSH(i)

        elif i == ')':
            while not stack.IS_EMPTY() and stack.PEEK() != '(':
                output.append(stack.POP())

            if stack.IS_EMPTY():
                raise ValueError("Mismatched parentheses")

            stack.POP()

        else:
            
            while (not stack.IS_EMPTY() and 
                   stack.PEEK() != '(' and 
                   (precedence(stack.PEEK()) > precedence(i) or 
                    (precedence(stack.PEEK()) == precedence(i) and i != '^'))):
                output.append(stack.POP())
            stack.PUSH(i)

    while not stack.IS_EMPTY():
        if stack.PEEK() == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.POP())

    return output

def eval_postfix(tokens, variables):
    stack = Stack()

    for i in tokens:
        if is_number(i):
            stack.PUSH(float(i))
        elif i[0].isalpha() or i[0] == '_':
            if i in variables:
                stack.PUSH(variables[i])
            else:
                raise ValueError("Undefined variable")

        else:
            b = stack.POP()
            a = stack.POP()

            if i == '+':
                stack.PUSH(a + b)
            elif i == '-':
                stack.PUSH(a - b)
            elif i == '*':
                stack.PUSH(a * b)
            elif i == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.PUSH(a / b)
            elif i == '%':
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero")
                stack.PUSH(a % b)
            elif i == '^':
                stack.PUSH(a ** b)

    return stack.POP()

class PyStackCalc:
    def __init__(self):
        self.variables = {"pi": 3.14159, "e": 2.71828}
        self.undo_stack = []
        self.redo_stack = []

    def calculate(self, expression):
        tokens = tokenize(expression)

        if '=' in tokens:
            name = tokens[0]

            if len(tokens) < 3 or tokens[1] != '=':
                raise ValueError("Invalid assignment")

            postfix = infix_to_postfix(tokens[2:])
            value = eval_postfix(postfix, self.variables)

            self.undo_stack.append(self.variables.copy())
            self.variables[name] = value
            self.redo_stack = []

            return value

        postfix = infix_to_postfix(tokens)
        return eval_postfix(postfix, self.variables)

    def execute(self, expr):
        expr = expr.strip()

        if expr == "undo":
            self.undo()
            return None

        if expr == "redo":
            self.redo()
            return None

        if expr.startswith("let "):
            expr = expr[4:].strip()

        return self.calculate(expr)
    
    def undo(self):
        if self.undo_stack == []:
            raise ValueError("Nothing to undo")

        self.redo_stack.append(self.variables.copy())
        self.variables = self.undo_stack.pop()

    def redo(self):
        if self.redo_stack == []:
            raise ValueError("Nothing to redo")

        self.undo_stack.append(self.variables.copy())
        self.variables = self.redo_stack.pop()

    def show_variables(self):
        return self.variables

    
    def start_repl(self):
        while True:
            try:
                expr = input("calc> ").strip()

                if expr.lower() == "exit":
                    break

                if expr == "":
                    continue

                if expr == "vars":
                    print(self.show_variables())
                else:
                    result = self.execute(expr)
                    if result is not None:
                        print(result)

            except Exception as e:
                print("Error:", e)


def main():
    calc = PyStackCalc()

    while True:
        try:
            expr = input(">>> ")

            if expr == "exit":
                break

            elif expr == "undo":
                calc.undo()
                print("Undone")

            elif expr == "redo":
                calc.redo()
                print("Redone")

            elif expr == "vars":
                print(calc.show_variables())

            else:
                result = calc.calculate(expr)
                print(result)

        except Exception as e:
            print("Error:", e)


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
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        calc = PyStackCalc()
        calc.start_repl()