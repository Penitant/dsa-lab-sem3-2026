import re
import math
import copy


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
            raise IndexError("Stack is empty")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def tokenize(expression):
    pattern = r'\d+(?:\.\d+)?|[A-Za-z_]\w*|[+\-*/%^()]|='
    tokens = re.findall(pattern, expression)
    if ''.join(tokens).replace(' ', '') != re.sub(r'\s+', '', expression):
        raise ValueError("Invalid character in expression")
    return tokens


def to_postfix(tokens):
    output = []
    operators = Stack()
    precedence = {
        '+': 1, '-': 1,
        '*': 2, '/': 2, '%': 2,
        'u+': 3, 'u-': 3,
        '^': 4
    }
    functions = {'sqrt', 'abs', 'sin', 'cos', 'tan', 'log', 'exp'}
    previous = None

    for token in tokens:
        if re.fullmatch(r'\d+(?:\.\d+)?', token):
            output.append(token)
        elif re.fullmatch(r'[A-Za-z_]\w*', token):
            if token in functions:
                operators.push(token)
            else:
                output.append(token)
        elif token == '(':
            operators.push(token)
        elif token == ')':
            while not operators.is_empty() and operators.peek() != '(':
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()
            if not operators.is_empty() and operators.peek() in functions:
                output.append(operators.pop())
        elif token in '+-*/%^':
            op = token
            if token in '+-' and (previous is None or previous in '+-*/%^('):
                op = 'u' + token
            if not op.startswith('u'):
                while not operators.is_empty() and operators.peek() != '(':
                    top = operators.peek()
                    if top in functions:
                        output.append(operators.pop())
                        continue
                    top_precedence = precedence.get(top, 0)
                    current_precedence = precedence[op]
                    if top_precedence > current_precedence or (
                        top_precedence == current_precedence and op != '^'
                    ):
                        output.append(operators.pop())
                    else:
                        break
            operators.push(op)
        else:
            raise ValueError("Invalid token: " + token)
        previous = token

    while not operators.is_empty():
        item = operators.pop()
        if item == '(':
            raise ValueError("Mismatched parentheses")
        output.append(item)
    return output


def evaluate_postfix(postfix, variables, trace=False):
    values = Stack()
    functions = {
        'sqrt': math.sqrt,
        'abs': abs,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'exp': math.exp
    }
    for token in postfix:
        if re.fullmatch(r'\d+(?:\.\d+)?', token):
            values.push(float(token))
        elif token in variables:
            values.push(float(variables[token]))
        elif token in functions:
            a = values.pop()
            values.push(functions[token](a))
        elif token in ('u+', 'u-'):
            a = values.pop()
            values.push(a if token == 'u+' else -a)
        elif token in '+-*/%^':
            b = values.pop()
            a = values.pop()
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            elif token == '%':
                result = a % b
            else:
                result = a ** b
            values.push(result)
        else:
            raise ValueError("Unknown variable: " + token)
        if trace:
            print("Token:", token, "| Stack:", values.items)

    if values.size() != 1:
        raise ValueError("Invalid expression")
    return values.pop()


def calculate(expression, variables, trace=False):
    tokens = tokenize(expression)
    postfix = to_postfix(tokens)
    if trace:
        print("Postfix:", postfix)
    return evaluate_postfix(postfix, variables, trace)


def main():
    variables = {'pi': math.pi, 'e': math.e}
    undo_stack = Stack()
    redo_stack = Stack()
    history = []

    print("PyStackCalc - type help for commands")
    while True:
        try:
            line = input("calc> ").strip()
            if not line:
                continue
            if line.lower() in ('exit', 'quit'):
                break
            if line.lower() == 'help':
                print("Examples: 2 + 3 * 4, let radius = 7, vars, history, undo, redo, trace 2^3^2, exit")
                continue
            if line == 'vars':
                print(variables)
                continue
            if line == 'history':
                for number, entry in enumerate(history, 1):
                    print(str(number) + ". " + entry)
                continue
            if line == 'undo':
                if undo_stack.is_empty():
                    print("Nothing to undo")
                else:
                    redo_stack.push(copy.deepcopy(variables))
                    variables = undo_stack.pop()
                    print("Undo complete")
                continue
            if line == 'redo':
                if redo_stack.is_empty():
                    print("Nothing to redo")
                else:
                    undo_stack.push(copy.deepcopy(variables))
                    variables = redo_stack.pop()
                    print("Redo complete")
                continue

            trace = False
            if line.startswith('trace '):
                trace = True
                line = line[6:].strip()

            assignment = re.fullmatch(r'let\s+([A-Za-z_]\w*)\s*=\s*(.+)', line)
            if assignment:
                name = assignment.group(1)
                expression = assignment.group(2)
                if name in ('let', 'sqrt', 'abs', 'sin', 'cos', 'tan', 'log', 'exp'):
                    print("That name is reserved")
                    continue
                result = calculate(expression, variables, trace)
                undo_stack.push(copy.deepcopy(variables))
                redo_stack = Stack()
                variables[name] = result
                print(name, "=", result)
            else:
                result = calculate(line, variables, trace)
                print(result)
            history.append(line)
        except (ValueError, IndexError, ZeroDivisionError, OverflowError) as error:
            print("Error:", error)
        except Exception as error:
            print("Math error:", error)


if __name__ == "__main__":
    main()
