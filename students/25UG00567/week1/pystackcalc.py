
import re
import sys

class Stack:
    def __init__(self): self.items = []
    def push(self, x): self.items.append(x)
    def pop(self):
        if self.is_empty(): raise IndexError("Empty stack")
        return self.items.pop()
    def peek(self): return self.items[-1] if self.items else None
    def is_empty(self): return not self.items
    def size(self): return len(self.items)
    def to_list(self): return self.items.copy()

def tokenize(expr: str) -> list[str]:
    p = r"\d+(?:\.\d+)?|[a-zA-Z_]\w*|[\+\-\*\/\^\%\(\)=]"
    ts, pos = [], 0
    for m in re.finditer(p, expr):
        if expr[pos:m.start()].strip(): raise ValueError("Invalid character")
        ts.append(m.group()); pos = m.end()
    if expr[pos:].strip() or not ts: raise ValueError("Invalid expression")
    return ts

PREC = {"+":1, "-":1, "*":2, "/":2, "%":2, "u+":3, "u-":3, "^":4}
OPS = set("+-*/%^")
def num(t): return re.fullmatch(r"\d+(?:\.\d+)?", t) is not None
def var(t): return re.fullmatch(r"[a-zA-Z_]\w*", t) is not None

def infix_to_postfix(expr):
    ts = tokenize(expr) if isinstance(expr, str) else expr
    out, s, expect = [], Stack(), True
    for t in ts:
        if num(t) or var(t):
            if not expect: raise ValueError("Missing operator")
            out.append(t); expect = False
        elif t == "(":
            if not expect: raise ValueError("Missing operator")
            s.push(t); expect = True
        elif t == ")":
            if expect: raise ValueError("Invalid parentheses")
            while not s.is_empty() and s.peek() != "(": out.append(s.pop())
            if s.is_empty(): raise ValueError("Mismatched parentheses")
            s.pop(); expect = False
        elif t in OPS:
            if expect:
                if t not in "+-": raise ValueError("Missing operand")
                s.push("u"+t); continue
            while not s.is_empty() and s.peek() in PREC:
                top = s.peek()
                if PREC[top] > PREC[t] or (PREC[top] == PREC[t] and t != "^"):
                    out.append(s.pop())
                else: break
            s.push(t); expect = True
        else: raise ValueError("Invalid token")
    if expect: raise ValueError("Missing operand")
    while not s.is_empty():
        t = s.pop()
        if t == "(": raise ValueError("Mismatched parentheses")
        out.append(t)
    return out

def eval_postfix(ts, variables=None):
    variables = {} if variables is None else variables
    s = Stack()
    for t in ts:
        if num(t): s.push(float(t) if "." in t else int(t))
        elif var(t):
            if t not in variables: raise ValueError(f"Unknown variable: {t}")
            s.push(variables[t])
        elif t in ("u+", "u-"):
            a = s.pop(); s.push(a if t == "u+" else -a)
        elif t in OPS:
            b, a = s.pop(), s.pop()
            if t in ("/", "%") and b == 0: raise ZeroDivisionError("Division by zero")
            s.push({"+":lambda:a+b, "-":lambda:a-b, "*":lambda:a*b,
                    "/":lambda:a/b, "%":lambda:a%b, "^":lambda:a**b}[t]())
        else: raise ValueError("Invalid token")
    if s.size() != 1: raise ValueError("Invalid expression")
    return s.pop()

class PyStackCalc:
    def __init__(self):
        self.variables = {"pi":3.14159, "e":2.71828}
        self.undo_stack, self.redo_stack = Stack(), Stack()
    def execute(self, cmd):
        cmd = cmd.strip()
        if not cmd: raise ValueError("Empty command")
        if cmd.lower() in ("undo", "redo"):
            undo = cmd.lower() == "undo"
            src, dst = (self.undo_stack, self.redo_stack) if undo else (self.redo_stack, self.undo_stack)
            if src.is_empty(): return "Nothing to "+cmd
            dst.push(dict(self.variables)); self.variables = src.pop()
            return cmd.capitalize()+" successful"
        ts = tokenize(cmd)
        if ts[0] == "let": ts = ts[1:]
        if len(ts) >= 2 and ts[1] == "=":
            name, expr = ts[0], ts[2:]
            if not var(name) or not expr or ts.count("=") != 1: raise ValueError("Invalid assignment")
            value = eval_postfix(infix_to_postfix(expr), self.variables)
            self.undo_stack.push(dict(self.variables)); self.redo_stack = Stack()
            self.variables[name] = value; return value
        if "=" in ts or ts[0] == "let": raise ValueError("Invalid assignment")
        return eval_postfix(infix_to_postfix(ts), self.variables)
    def start_repl(self):
        while True:
            try:
                cmd = input("calc> ").strip()
                if cmd.lower() in ("exit", "quit"): break
                print(self.execute(cmd))
            except (ValueError, ZeroDivisionError, IndexError) as e: print("Error:", e)
            except (EOFError, KeyboardInterrupt): print(); break

def run_tests():
    c = PyStackCalc()
    assert c.execute("3 + 4 * 2") == 11
    assert c.execute("(3 + 4) * 2") == 14
    assert c.execute("2 ^ 3 ^ 2") == 512
    assert c.execute("(3 + 4) * 2 - 8 / 4") == 12
    c.execute("let x = 15"); c.execute("let y = x * 2 - 10")
    assert c.variables["y"] == 20
    c.execute("undo"); assert "y" not in c.variables
    c.execute("redo"); assert c.variables["y"] == 20
    try: c.execute("(3 + 4 * 2")
    except ValueError: pass
    else: assert False
    try: c.execute("100 / (4 - 4)")
    except ZeroDivisionError: pass
    else: assert False
    assert c.execute("-2 ^ 2") == -4
    assert c.execute("(-2) ^ 2") == 4
    assert c.execute("2 ^ -2") == 0.25
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test": run_tests()
    else: PyStackCalc().start_repl()
