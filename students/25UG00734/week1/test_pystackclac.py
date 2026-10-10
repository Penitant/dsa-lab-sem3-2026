from pystackcalc import PyStackCalc


def run_tests():
    print("Running PyStackCalc Test Suite...")
    engine = PyStackCalc()

    # 1. Precedence & grouping
    assert engine.execute("3 + 4 * 2") == 11, "Test 1 Failed: Precedence"
    assert engine.execute("(3 + 4) * 2") == 14, "Test 2 Failed: Parentheses"
    assert engine.execute("2 ^ 3 ^ 2") == 512, "Test 3 Failed: Right-associativity"
    assert engine.execute("( 3 + 4 ) * 2 - 8 / 4") == 12, "Test 4 Failed: Mixed arithmetic"

    # 2. Variables
    engine.execute("let x = 15")
    engine.execute("let y = x * 2 - 10")
    assert engine.variables["y"] == 20, "Test 5 Failed: Variable calculation"

    # 3. Undo / Redo
    engine.execute("undo")
    assert "y" not in engine.variables, "Test 6 Failed: Undo"
    engine.execute("redo")
    assert engine.variables["y"] == 20, "Test 7 Failed: Redo"

    # 4. Error handling
    try:
        engine.execute("(3 + 4 * 2")
        assert False, "Test 8 Failed: Should raise ValueError"
    except ValueError:
        pass

    try:
        engine.execute("100 / (4 - 4)")
        assert False, "Test 9 Failed: Should raise ZeroDivisionError"
    except ZeroDivisionError:
        pass

    print("✅ All 9 test cases passed successfully!")


run_tests()