#!/usr/bin/env python3
"""Compare ASTs of expected vs decompiled"""
import ast, sys

decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()

try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
except Exception as e:
    print(f"Expected AST parse error: {e}")
    sys.exit(1)

try:
    actual_ast = ast.dump(ast.parse(decompiled), indent=2)
except Exception as e:
    print(f"Actual AST parse error: {e}")
    print("---Decompiled source---")
    print(decompiled)
    print("---End---")
    sys.exit(1)

if expected_ast == actual_ast:
    print("✅ AST MATCH - test_expr_basic 3.10")
else:
    exp_lines = expected_ast.split('\n')
    act_lines = actual_ast.split('\n')
    for i in range(max(len(exp_lines), len(act_lines))):
        e = exp_lines[i] if i < len(exp_lines) else "(missing)"
        a = act_lines[i] if i < len(act_lines) else "(missing)"
        if e != a:
            print(f"Line {i}:")
            print(f"  expected: {e}")
            print(f"  actual:   {a}")
            if i > 5:
                break
