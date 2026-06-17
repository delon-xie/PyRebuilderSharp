# Decompiled from: <module>

# orphan @0x0078
e = None
raise
__doc__ = 'Compare ASTs of expected vs decompiled'
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
    return None
# orphan @0x00E6
e = None
raise
# orphan @0x0104
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
# orphan @0x012E
# orphan @0x0130
# orphan @0x013E
# orphan @0x0148
# orphan @0x0156
# orphan @0x0160
# orphan @0x016A
print(f"Line {i}:")
print(f"  expected: {e}")
# orphan @0x0190
# orphan @0x01A4
# orphan @0x0284
# orphan @0x02B4
# orphan @0x030E
# orphan @0x0342
# [SUMMARY] 26 blocks · 9 processed · 18 orphan · 213 instr
