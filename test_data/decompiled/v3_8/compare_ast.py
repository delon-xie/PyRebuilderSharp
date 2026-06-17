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
# orphan @0x00FE
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
range(max(len(exp_lines), len(act_lines)))
# orphan @0x0128
# orphan @0x012A
i < len(exp_lines)
# orphan @0x013A
exp_lines[i]
# orphan @0x0142
'(missing)'
# orphan @0x0144
i < len(act_lines)
# orphan @0x0154
act_lines[i]
# orphan @0x015C
'(missing)'
# orphan @0x015E
e != a
# orphan @0x016A
print(f"Line {i}:")
print(f"  expected: {e}")
print(f"  actual:   {a}")
i > 5
# orphan @0x01A0
# [SUMMARY] 24 blocks · 12 processed · 12 orphan · 209 instr
