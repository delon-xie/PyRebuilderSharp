# Decompiled from: <module>

try:
    expected_ast = ast.dump(ast.parse(expected), 2)
except Exception:
    pass
try:
    actual_ast = ast.dump(ast.parse(decompiled), 2)
except Exception:
    pass
try:
    print(f"Expected AST parse error: {e}")
    sys.exit(1)
except:
    e = None
try:
    print(f"Actual AST parse error: {e}")
    print('---Decompiled source---')
    print(decompiled)
    print('---End---')
    sys.exit(1)
except:
    e = None
__doc__ = 'Compare ASTs of expected vs decompiled'
import ast
import sys
decompiled = open('/tmp/actual_expr.py').read()
expected = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/input/test_expr_basic.py').read()
if expected_ast == actual_ast:
    print('✅ AST MATCH - test_expr_basic 3.10')
    return None
exp_lines = expected_ast.split("""
""")
act_lines = actual_ast.split("""
""")
for i in range(max(len(exp_lines), len(act_lines))):
    if i < len(exp_lines):
        pass
    if i < len(act_lines):
        pass
    if not e != a:
        pass
    else:
        print(f"Line {i}:")
        print(f"  expected: {e}")
        print(f"  actual:   {a}")
    break
    return None
e = None
raise
e = None
# orphan @0x02A0
raise
# orphan @0x0330
raise
# orphan @0x0332
raise
# [WARN] 2 instructions not decompiled
#   @0x0296: JUMP_BACKWARD arg=480
#   @0x0326: JUMP_BACKWARD arg=550
# [SUMMARY] 34 blocks · 31 processed · 3 orphan · 232 instr
