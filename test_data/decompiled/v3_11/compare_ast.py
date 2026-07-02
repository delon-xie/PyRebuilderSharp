# Decompiled from: <module>

"""Compare ASTs of expected vs decompiled"""
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
print(f"Expected AST parse error: {e}")
sys.exit(1)
print(f"Line {i}:")
print(f"  expected: {e}")
print(f"  actual:   {a}")
