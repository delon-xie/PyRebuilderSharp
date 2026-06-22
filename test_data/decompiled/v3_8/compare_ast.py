# Decompiled from: <module>

'Compare ASTs of expected vs decompiled'
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
except Exception:
    pass
try:
    actual_ast = ast.dump(ast.parse(decompiled), indent=2)
except Exception:
    pass
if expected_ast == actual_ast:
    print('✅ AST MATCH - test_expr_basic 3.10')
print(f"Line {i}:")
print(f"  expected: {e}")
print(f"  actual:   {a}")
# [SUMMARY] 24 blocks · 23 processed · 12 orphan · 209 instr
