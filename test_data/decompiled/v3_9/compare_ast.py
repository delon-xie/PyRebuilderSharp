# Decompiled from: <module>

# orphan @0x0078
e = None
"""Compare ASTs of expected vs decompiled"""
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
try:
    expected_ast = ast.dump(ast.parse(expected), indent=2)
except Exception:
    print(f"Expected AST parse error: {e}")
    sys.exit(1)
try:
    actual_ast = ast.dump(ast.parse(decompiled), indent=2)
except Exception:
    print(f"Actual AST parse error: {e}")
    print('---Decompiled source---')
    print(decompiled)
    print('---End---')
    sys.exit(1)
if expected_ast == actual_ast:
    print('✅ AST MATCH - test_expr_basic 3.10')
# orphan @0x00E6
e = None
# orphan @0x0148
'(missing)'
# orphan @0x0162
'(missing)'
# orphan @0x0170
print(f"Line {i}:")
print(f"  expected: {e}")
print
# [SUMMARY] 22 blocks · 17 processed · 13 orphan · 211 instr
