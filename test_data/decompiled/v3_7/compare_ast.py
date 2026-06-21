# Decompiled from: <module>

# orphan @0x0072
e = None
# orphan @0x0046
"""Compare ASTs of expected vs decompiled"""
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
# orphan @0x009A
# orphan @0x00DE
e = None
# orphan @0x00FE
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
range(max(len(exp_lines), len(act_lines)))
# orphan @0x012A
# orphan @0x012C
i < len(exp_lines)
# orphan @0x013C
exp_lines[i]
# orphan @0x0144
'(missing)'
# orphan @0x0146
i < len(act_lines)
# orphan @0x0156
act_lines[i]
# orphan @0x015E
'(missing)'
# orphan @0x0160
e != a
# orphan @0x016C
print(f"Line {i}:")
print(f"  expected: {e}")
print(f"  actual:   {a}")
i > 5
# orphan @0x01A2
# orphan @0x01A8
# [SUMMARY] 25 blocks · 8 processed · 17 orphan · 210 instr
